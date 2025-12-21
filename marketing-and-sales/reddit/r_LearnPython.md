# Title: I built a serverless "Digital Pet" using Python, GitHub Actions, and Typer - Source Code Review?

Hey Pythonistas,

I just finished a side project and I'd love some eyes on the code.
It's called **ForkMonkey**, and it's a Tamagotchi-style pet that lives in a GitHub repo. It's all free, public and uses free mechanism of Github.

**Repo:** [https://github.com/roeiba/forkMonkey](https://github.com/roeiba/forkMonkey)

**Local Setup:**
I used `uv` for dependency management (highly recommend!) and `typer` + `rich` for the CLI interface.

**What to look at:**
I'm particularly interested in feedback on:
1.  `src/genetics.py`: This handles the bitwise operations for the DNA inheritance. I tried to keep it clean using `pydantic` models for the traits.
2.  `src/engine.py`: This is the main loop that wakes up the agent.
3.  **Testing**: I haven't added enough unit tests for the genetic crossover logic yet.

**The "Stack":**
-   **Python 3.12**
-   **Pydantic** (Data validation/Schema)
-   **Azure AI / GitHub Models SDK** (for the AI personality)
-   **CairoSVG** (for generating the dynamic images)

If you're looking for a project to contribute to, I have a few "Generic" TODOs left, specifically around adding more "Accessories" to the SVG generator.

Cheers!
