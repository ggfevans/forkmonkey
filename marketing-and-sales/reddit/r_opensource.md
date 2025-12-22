# Title: I built a digital pet that lives entirely in a GitHub repo (Actions = Backend, Git = DB)

Hi r/opensource,

I wanted to share a fun open-source experiment I just released: **ForkMonkey**.

It's a Tamagotchi-style pet that lives inside a GitHub repository. The unique part is that it runs on **zero external infrastructure**—it exploits the GitHub ecosystem to function as a full app.

**Repository:** [https://github.com/roeiba/forkMonkey](https://github.com/roeiba/forkMonkey)
**Demo:** [https://roeiba.github.io/forkMonkey/](https://roeiba.github.io/forkMonkey/)

### How it works (The Stack):

*   **The "Backend":** A GitHub Actions workflow runs every night (cron job).
*   **The "Brain":** It uses the free tier of GitHub Models (GPT-4o) to generate a daily "event" based on the monkey's current state and history.
*   **The "Database":** It commits the daily update to a `history.json` file. The Git history itself acts as an append-only ledger of your pet's life.
*   **The "Frontend":** A static site hosted on GitHub Pages that visualizes the JSON data.
*   **The "Breeding" Mechanism:** This is the cool part—when you **Fork** the repository, the setup script reads the "parent" monkey's DNA from the upstream repo, mixes it with random mutations, and generates a new unique monkey in your fork. This creates a traversable "family tree" of forks across the platform.

### Why Open Source?

The goal is to see how far we can push "Serverless" by just using a code repository as the entire application platform.

It's 100% hackable:
*   Want a different AI persona? Edit the system prompt in `src/ai.py`.
*   Want different visual traits? Modify the SVG generator in `src/visualizer.py`.
*   Want to change the game rules? Tweak the mutation rates in `src/genetics.py`.

It's under MIT license. I'd love to see people fork it not just to play, but to mod it entirely into different creatures or games.

Would love any feedback or PRs!
