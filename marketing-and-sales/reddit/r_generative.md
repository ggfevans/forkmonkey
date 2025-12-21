# Title: I made a genetic algorithm for "Monkey" generation that runs in GitHub Actions

Hi r/generative!

I've been playing around with procedural generation and genetic inheritance. I built a system called **ForkMonkey** where the "agents" are GitHub repositories. It's all free, public and uses free mechanism of Github.

**The output:** [Imgur link or upload image of 4-6 monkeys]
**The Code:** [https://github.com/roeiba/forkMonkey](https://github.com/roeiba/forkMonkey)

### The Generative System:
*   **DNA**: A 64-bit style hash representing traits (Color, Expression, Accessories, Pattern, Background).
*   **Mutation**: Every 24 hours, an LLM (GPT-4o) acts as a high-level mutation function—it chooses specific traits to shift based on aesthetic coherence rather than pure randomness.
*   **Crossover**: When you "fork" a repo, it treats the original as a parent. The child initializes with 50% of the parent's genes and 50% random noise.

The avatars are generated as SVGs on the fly using Python (`cairosvg`).

It's a fun experiment in "slow" generative art where the piece evolves once per day forever.

Thought this community might appreciate the mechanics!
