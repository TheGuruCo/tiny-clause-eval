# Optional 90-second demo (only after you run the code yourself)

**0:00–0:15** Show the README and explain: "This is a small synthetic evaluation I used to practice designing reliable AI measurements. The goal is to test both the answer and its cited evidence."

**0:15–0:35** Open `data/cases.json`. Point to one policy, its question, the expected answer, and the exact supporting sentence. Explain why human labels matter.

**0:35–1:00** Open Terminal and run `python3 eval.py --mode baseline`. Point to the per-case PASS/FAIL results and summary. Say: "This keyword baseline is not an LLM; its errors show why we need real evaluation rather than trusting outputs."

**1:00–1:15** Show `RESULTS.md`. Explain one failure case (a numeric condition) and the strict evidence-matching limitation.

**1:15–1:30** Say: "My next experiment would be to run the same cases with Claude, audit source quotes, and expand into a blinded evaluation set. This eight-case sample is deliberately too small to establish generalization."

**IMPORTANT:** If you actually run the Claude condition, you can show its *real* results instead. Never imply the Claude experiment was run if it wasn't. Keep your API key and other terminal secrets out of the recording.
