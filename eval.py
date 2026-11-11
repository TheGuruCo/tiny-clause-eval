#!/usr/bin/env python3
"""Tiny Clause Eval: small, synthetic policy interpretation experiment.

No dependencies beyond Python's standard library. The baseline makes NO API calls.
The optional Claude mode requires a paid Anthropic API key.
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).parent
CASES_PATH = ROOT / "data" / "cases.json"
ANSWERS = {"yes", "no", "unclear"}


def norm(value):
    """Normalize whitespace and case only; this is intentionally strict."""
    return " ".join(str(value).lower().split())


def baseline(policy, question):
    """Deliberately simplistic keyword baseline, NOT a semantic policy solver.

    It does not understand quantities, deadlines, or question-specific logic.
    It quotes the policy's first sentence, even when a later sentence matters.
    """
    p = policy.lower()
    if "case-by-case" in p:
        answer = "unclear"
    elif "not" in p or "nonrefundable" in p:
        answer = "no"
    else:
        answer = "yes"
    first_sentence = policy.split(". ", 1)[0].rstrip(".") + "."
    return {"answer": answer, "evidence": first_sentence}


def parse_json_response(value):
    """Accept a plain JSON object, or an object inside a Markdown JSON fence."""
    value = value.strip()
    if value.startswith("```"):
        value = re.sub(r"^```(?:json)?\s*", "", value, flags=re.I)
        value = re.sub(r"\s*```$", "", value)
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("Model output must be a JSON object")
    return parsed


def call_claude(policy, question, model):
    """Use the Anthropic Messages API. API key is never stored in results."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is missing. Use --mode baseline or set the key.")
    payload = {
        "model": model,
        "max_tokens": 220,
        "temperature": 0,
        "system": (
            "Answer the question using only the provided fictional policy. "
            "Return ONLY a JSON object with two string keys: answer and evidence. "
            "answer must be yes, no, or unclear. "
            "For evidence, copy the COMPLETE sentence from the policy that best "
            "supports your decision EXACTLY, including punctuation. "
            "Use unclear when the facts or policy do not establish a definite answer. "
            "Do not add explanations or code fences."
        ),
        "messages": [{
            "role": "user",
            "content": f"Policy: {policy}\n\nQuestion: {question}"
        }],
    }
    request = Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=45) as response:
            body = json.load(response)
    except HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")[:400]
        raise RuntimeError(f"Claude API returned HTTP {exc.code}: {details}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach Claude API: {exc.reason}") from exc
    content = "".join(b.get("text", "") for b in body.get("content", []) if b.get("type") == "text")
    try:
        prediction = parse_json_response(content)
    except (ValueError, json.JSONDecodeError) as exc:
        prediction = {"answer": "invalid", "evidence": "", "parse_error": str(exc), "raw_output": content[:500]}
    return prediction, body.get("usage", {})


def grade(case, prediction):
    answer = str(prediction.get("answer", "")).lower().strip()
    evidence = str(prediction.get("evidence", "")).strip()
    valid_format = answer in ANSWERS and bool(evidence)
    answer_correct = answer == case["gold_answer"]
    # Two distinct checks: copied text exists in source, and EXACT gold sentence matches.
    source_supported = bool(evidence) and norm(evidence) in norm(case["policy"])
    gold_evidence_match = bool(evidence) and norm(evidence) == norm(case["gold_evidence"])
    return {
        "valid_format": valid_format,
        "answer_correct": answer_correct,
        "evidence_appears_in_policy": source_supported,
        "gold_evidence_match": gold_evidence_match,
        "strict_pass": answer_correct and gold_evidence_match and valid_format,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate policy interpretation on 8 synthetic cases")
    parser.add_argument("--mode", choices=["baseline", "claude"], default="baseline")
    parser.add_argument("--model", default="claude-haiku-5-5", help="Claude API model ID (Claude mode only)")
    parser.add_argument("--output", help="Override JSON results file location")
    args = parser.parse_args()
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    rows = []
    print(f"\nTiny Clause Eval | mode={args.mode} | {len(cases)} fictional policies\n")
    for case in cases:
        start = time.perf_counter()
        try:
            if args.mode == "baseline":
                prediction, usage = baseline(case["policy"], case["question"]), {}
            else:
                prediction, usage = call_claude(case["policy"], case["question"], args.model)
        except RuntimeError as exc:
            print(f"ERROR on {case['id']}: {exc}", file=sys.stderr)
            print("No experiment results were written for this incomplete run.", file=sys.stderr)
            sys.exit(1)
        latency_ms = round((time.perf_counter() - start) * 1000, 1)
        score = grade(case, prediction)
        rows.append({
            "id": case["id"], "gold_answer": case["gold_answer"],
            "predicted_answer": prediction.get("answer", ""),
            "gold_evidence": case["gold_evidence"],
            "predicted_evidence": prediction.get("evidence", ""),
            "scores": score, "latency_ms": latency_ms, "usage": usage,
            **({"parse_error": prediction["parse_error"]} if "parse_error" in prediction else {})
        })
        symbol = "PASS" if score["strict_pass"] else "FAIL"
        print(f"{case['id']}: {symbol:4} | predicted={str(prediction.get('answer', '')):7} "
              f"gold={case['gold_answer']:7} | evidence={'yes' if score['gold_evidence_match'] else 'no'}")
    n = len(rows)
    counts = {metric: sum(bool(r["scores"][metric]) for r in rows) for metric in (
        "answer_correct", "evidence_appears_in_policy", "gold_evidence_match", "strict_pass"
    )}
    report = {
        "project": "Tiny Clause Eval (synthetic toy experiment)",
        "mode": args.mode,
        "model": args.model if args.mode == "claude" else None,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "sample_size": n,
        "summary_counts": counts,
        "summary_percent": {k: round(100 * v / n, 1) for k, v in counts.items()},
        "total_model_tokens": sum(r["usage"].get("input_tokens", 0) + r["usage"].get("output_tokens", 0) for r in rows),
        "limitations": "8 hand-written fictional cases; small convenience sample, strict evidence matching, no generalization or profitability claim.",
        "cases": rows,
    }
    target = Path(args.output) if args.output else ROOT / "results" / f"{args.mode}_results.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("\nRESULTS (number correct out of 8)")
    for k, v in counts.items():
        print(f"  {k:29} {v}/{n} ({100*v/n:.1f}%)")
    print(f"\nSaved to: {target}\n")


if __name__ == "__main__":
    main()
