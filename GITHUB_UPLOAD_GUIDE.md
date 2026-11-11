# Put Tiny Clause Eval on GitHub (beginner friendly)

## Option A: GitHub Desktop (no Git commands)

1. Extract `tiny-clause-eval.zip` on your computer.
2. Install and sign in to **GitHub Desktop** from https://desktop.github.com/ if you don't already use it.
3. In GitHub Desktop, use **File > Add local repository**, choose the extracted `tiny-clause-eval` folder, and select **Create a repository here** if prompted.
4. Enter a brief summary, such as `Initial synthetic policy evaluation project`, then click **Commit to main**.
5. Click **Publish repository**. Choose a public repository only when you're comfortable sharing the files. This project contains no company data.
6. Open the published repository URL and confirm you can see `README.md`, `eval.py`, `data/`, `results/`, and `tests/`.

## Option B: Command line (only if you already use Git)

Create a new empty repository in your GitHub account called `tiny-clause-eval`, **without** initializing it with a README or license. Then inside your local project folder:

```bash
git init
git add .
git commit -m "Add small synthetic AI evaluation experiment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/tiny-clause-eval.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username. GitHub may ask you to authenticate.

## Before submitting to Anthropic

- Open `README.md` and understand the purpose of every metric.
- Run both the baseline and unit tests on **your own machine**.
- Explain that the starter was developed with AI assistance if asked about authorship.
- Do not claim Claude was evaluated until you personally run and document that experiment.
- Link the **repository URL**, not a confidential Gather project.
