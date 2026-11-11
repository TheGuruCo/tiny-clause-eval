# Observed Results — Tiny Clause Eval

**Status:** Baseline run completed and unit tests passed on November 9, 2026. **No Claude API run has been performed.**

## Actual baseline measurements

Command: `python3 eval.py --mode baseline`

| Metric | Observed count | Rate |
| --- | ---: | ---: |
| Correct decision (`yes`, `no`, or `unclear`) | 6 / 8 | 75.0% |
| Evidence string occurs in source document | 8 / 8 | 100.0% |
| Exact reference sentence matched | 7 / 8 | 87.5% |
| Strict pass (correct answer **and** exact reference sentence) | 5 / 8 | 62.5% |

Full machine-readable output: [`results/baseline_results.json`](results/baseline_results.json).

## What went wrong

- **C03:** The keyword baseline predicted `no` correctly, but quoted the *first* sentence. The gold supporting sentence was the *second* sentence. Merely quoting text that appears in a policy does not prove evidence relevance.
- **C04:** The baseline predicted `yes` but missed that the $50 threshold applies to the **before-tax** total. The correct answer is `no`.
- **C08:** The baseline predicted `no` when the fictional policy explicitly said international purchase eligibility was **not specified**. The correct answer is `unclear`.

## Interpretation

The scores describe a *hand-built keyword baseline on eight examples*, not an AI language model. The small dataset, hand-written labels, single run, unblinded development, and exact-string evidence metric make the results unsuitable for generalization. The classifier was deliberately simple and is not intended to solve real policies.

**Claude comparison:** Not yet executed, so there are no model accuracy, cost, or latency claims.

## Suggested genuine next step

Run the optional Claude condition, inspect each generated citation manually, and document the actual output before making claims about model performance. Add independent labels and a held-out test set before scaling this into a serious benchmark.
