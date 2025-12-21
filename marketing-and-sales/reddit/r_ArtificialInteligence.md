# Title: A Genetic Algorithm + LLM experiment: Git-based Artificial Life

Hi r/ArtificialInteligence,

I'm sharing an open-source experiment that combines old-school **Genetic Algorithms** with modern **LLMs**.

**Project:** ForkMonkey
**Link:** [https://github.com/roeiba/forkMonkey](https://github.com/roeiba/forkMonkey)

**The Experiment:**
I wanted to create "Life" that survives on a code hosting platform.
Each "Monkey" is a repository.
1.  **Genetics:** It has a DNA string (hash) that determines traits (color, accessories, background).
2.  **Evolution:** You "breed" them by forking the repository. The child retains some traits and mutates others (standard GA crossover/mutation).
3.  **Intelligence:** The "Brain" is an LLM (Claude 3.5 Sonnet/GPT-4o via GitHub Models). It runs daily to interpret the DNA and 'experience' the world, updating its own mood and journal.

**No Servers:**
The interesting technical detail is that there is no persistent server. State is stored in the git history and the file system. The "Agent" wakes up during a GitHub Action, observes its state, acts, saves state, and goes back to sleep.

It's a fun exploration of autonomous agents that require zero infrastructure maintenance. It's all free, public and uses free mechanism of Github.

Would love feedback on the genetic breeding logic!
