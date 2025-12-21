# Title: I wrote a Python script that "evolves" this vector art daily using AI (genetic algorithm)

**Image/Video:**
[Upload `monkey_evolution/evolution.gif`]

**Description/Body:**
Hey everyone, sharing a project where code creates the art.

I built a system called **ForkMonkey**.
It's a Python script that generates SVGs programmatically.
What you see in the GIF is the "evolution" of one character over roughly 20 generations.

**The Process:**
1.  **DNA**: Each monkey has a DNA string that defines colors, shapes, and accessories.
2.  **AI**: Every day, a GitHub Action runs and feeds the current state to an LLM (Claude/GPT via GitHub Models).
3.  **Mutation**: The AI or a random algorithm mutates the DNA, changing the visual traits (like converting a solid background to a gradient, or adding a hat).
4.  **Rendering**: The script uses `cairosvg` to render the new vector image.

I thought this community might appreciate the intersection of Code + Art.

It's all free, public and uses free mechanism of Github.
**Repo (Code):** [https://github.com/roeiba/forkMonkey](https://github.com/roeiba/forkMonkey)
