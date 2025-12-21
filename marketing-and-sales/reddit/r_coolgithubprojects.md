# Title: ForkMonkey: An open-source, AI-evolving pet that lives in your README

Hey r/coolgithubprojects,

Just released **ForkMonkey**, a Python-based project that turns a repository into an autonomous digital pet. It's all free, public and uses free mechanism of Github.

**Repository:** [https://github.com/roeiba/forkMonkey](https://github.com/roeiba/forkMonkey)

### How it works technically:
1.  **Python Core**: A genetic engine (`src/genetics.py`) manages DNA strings and trait inheritance.
2.  **Procedural Art**: `cairosvg` generates unique monkey avatars based on the DNA.
3.  **AI brain**: A daily GitHub Action sends the monkey's state to **GPT-4o** (via the free GitHub Models API), which decides how to mutate it based on its "personality".
4.  **Self-Updating**: The action commits the new SVG and stats back to the repo, updating the README automatically.

It's completely free to run (uses standard GitHub runners + free AI tier).

I'd love for actual devs to fork it and see if the "breeding" mechanic works as expected (children should inherit traits from your fork).

Let me know if you dig through the code!
