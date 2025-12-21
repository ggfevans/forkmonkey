# Title: I built a "Tamagotchi" that lives in a GitHub Repo using the new GitHub Models (Claude/GPT-4o)

Hey everyone,

I wanted to share a weird experiment I've been working on called **ForkMonkey**.

**The Concept:**
It's an autonomous digital pet that lives entirely inside a GitHub repository. It doesn't run on a server. Instead, it uses GitHub Actions + the new free **GitHub Models** (which gives you free access to models like Claude 3.5 Sonnet and GPT-4o) to "live", evolve, and interact.

**How it utilizes AI:**
Every day (via cron), the " Monkey" wakes up. The Python script grabs the pet's current state (DNA, happiness, hunger) and feeds it into an LLM (I'm using Claude 3.5 Sonnet via the GitHub Models API).
The AI decides:
1.  How the monkey is feeling based on its stats.
2.  What it wants to say in its daily "diary" (commit message/README update).
3.  If it wants to mutate or change its visual appearance (SVG generation).

**Why this sub?**
I think this is a cool example of what you can build with "Serverless AI" now. You don't need a heavy backend or API keys that cost money. GitHub gives you a decent free tier for these models, and Actions are free for public repos.

It's basically an autonomous agent that costs $0 to run. It's all free, public and uses free mechanism of Github.

**Repo:** [https://github.com/roeiba/forkMonkey](https://github.com/roeiba/forkMonkey)

Let me know what you think about using LLMs for "Artificial Life" simulations like this!
