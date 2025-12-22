# Title: I built a "Serverless" Tamagotchi that lives in a GitHub repo (MIT License)

Hi r/opensource,

I'm sharing **ForkMonkey**, an experimental project I released this week.

It's a digital pet that lives entirely inside a GitHub repository. The goal was to build a self-sustaining application using **zero external infrastructure**, relying only on the GitHub ecosystem (Actions, Pages, Git history).

**Repository:** [https://github.com/roeiba/forkMonkey](https://github.com/roeiba/forkMonkey)
**License:** MIT

### The "Not Open Source" Elephant in the Room 🐘

I posted here yesterday and got some heat because the default configuration uses GPT-4o (via GitHub Models) for the evolution logic. **That's a fair point.**

I want to clarify: **The engine is 100% open source and model-agnostic.**

The core logic (`src/evolution.py`) uses an abstract `AIProvider` interface.
*   **Default:** Uses GitHub Models (free tier) for zero-setup accessibility.
*   **Open Models:** You can switch the underlying model to **Llama 3** (or any other model hosted on GitHub Models) just by setting an environment variable (`GITHUB_MODEL=Meta-Llama-3-70B-Instruct`).
*   **Bring Your Own:** It also supports Anthropic natively, and because it's standard Python, plugging in a local Ollama endpoint or HuggingFace inference is a trivial PR away.

### How it works

1.  **Repo as DB:** The state of your pet is a JSON file. Every "evolution" is a Git commit. The history of your pet is literally the `git log`.
2.  **Actions as Backend:** A cron workflow runs daily, invokes the Python engine, calculates changes, and commits them back.
3.  **Forking as functionality:** This is the mechanics I'm most proud of. "Adopting" a monkey means **Forking** the repo. This isn't just a copy; the setup script reads the *upstream* parent's DNA and mutates it. This creates a traceable genealogical tree across the entire GitHub network.

I'd love for this community to play with the **"Git as a Database"** concepts or help add providers for fully local/open-weight model execution.

Feedback and PRs welcome!
