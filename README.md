# Tiny Clause Eval

**Can a model answer simple policy questions and quote the supporting sentence?**

A small, transparent **learning experiment** in AI reliability and evidence grounding. Eight *fictional* policy documents have human-authored labels (`yes`, `no`, or `unclear`) and supporting source sentences. A deliberately naive keyword baseline is evaluated automatically. Optionally, the same task can be run with Claude using your own API key.

**Status:** Baseline executed. Claude results **not yet run** in this repository. This is not a peer-reviewed study, a novel benchmark, evidence of financial expertise, or evidence that an AI system is safe in production.

## How to run (Mac Terminal, Python 3)

1. Download or clone this repository, open Terminal, and enter its folder:

   ```bash
   cd tiny-clause-eval
   ```

2. Run the baseline (free, offline, no setup beyond Python 3):

   ```bash
   python3 eval.py --mode baseline
   ```

3. Run the five grader tests:

   ```bash
   python3 -m unittest discover -s tests -v
   ```

4. **Optional:** Evaluate the same cases with Claude (requires an Anthropic API key and may incur API charges):

   ```bash
   export ANTHROPIC_API_KEY="paste-your-key-here"
   python3 eval.py --mode claude --model claude-haiku-5-5
   unset ANTHROPIC_API_KEY
   ```

   **Keep your key private.** Never paste it into a GitHub file, screenshot, issue, or video. The API is not accessed in baseline mode. If your account does not support that model ID, pass a supported ID with `--model`.

## Experiment design

- **Question:** Can the system classify the requested policy decision and identify the exact supporting sentence?
- **Dataset:** Eight hand-written fictional policy scenarios in [`data/cases.json`](data/cases.json).
- **Labels:** `yes`, `no`, `unclear`; each case also has a human-authored `gold_evidence` sentence.
- **Baseline:** Intentionally simple keyword classifier. It checks for `case-by-case`, `not`, and `nonrefundable` and otherwise predicts `yes`. It quotes the first sentence of the policy. It cannot reliably reason about numbers or question-specific facts.
- **Claude condition (optional):** Sends each policy and question separately with the same answer/evidence schema. Model outputs are *not* filled in or fabricated.
- **Metrics:** Answer accuracy; whether the cited text appears anywhere in the source; exact gold-evidence match; and a *strict pass* requiring the correct answer and exact gold sentence.
- **Strictness:** Evidence matching ignores only differences in capitalization and whitespace. A relevant paraphrase or short partial quote may fail even when substantively correct.
- **Scoring:** All metrics are simple fractions, not statistically significant findings. This is a demonstration of evaluation mechanics, **not** evidence of general performance or deployability.

## Baseline results

The run recorded in [`results/baseline_results.json`](results/baseline_results.json) is an actual execution of `python3 eval.py --mode baseline`. It is deterministic except for insignificant execution-time measurements.

See [`RESULTS.md`](RESULTS.md) for the observed scores and limitations. To make a **model** comparison, actually run Claude; only then report its observed scores.

## What I would improve next

1. Have a second person independently review the labels and allow more than one acceptable evidence quote.
2. Use separate development and untouched evaluation cases; this tiny demonstration does not have a held-out test set.
3. Compare several prompts or model settings, repeat runs, and report uncertainty rather than single-run scores.
4. Inspect error cases manually to distinguish reasoning failures from overly strict evidence matching.

## Confidentiality and authorship

The project contains **only fictional policies**. It does not include company code, client documents, proprietary financial data, or prediction-market strategies. This starter was assembled with AI assistance. If using it in an application, describe your actual personal role in running, verifying, explaining, and extending the experiment; do not misrepresent AI-assisted work as independent implementation.

## Files

```
.
├── README.md                 # experiment and run instructions
├── eval.py                   # baseline, optional Claude API call, grader
├── data/cases.json           # eight fictional scenarios and gold labels
├── results/baseline_results.json  # measured baseline run
├── RESULTS.md                # factual interpretation of output
├── DEMO_SCRIPT.md            # optional 90-second screen recording script
├── GITHUB_UPLOAD_GUIDE.md    # beginner-friendly publishing steps
├── tests/test_eval.py        # small unit tests of the grader
└── .gitignore                # prevents accidental commit of API results/key files
```

No third-party Python packages are required. Python 3.9+ recommended.
