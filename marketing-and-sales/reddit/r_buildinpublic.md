# Title: Built an AI-powered Tamagotchi that lives entirely on GitHub — no servers, no payments, no maintenance

Hey r/BuildInPublic!

Just shipped a side project I've been hacking on: **ForkMonkey** 🐵

### The Concept
It's a digital pet (like Tamagotchi) that lives in a GitHub repository. Every day, an AI evolves its appearance — and the "breeding" mechanism is just forking the repo.

### Why I built this
I wanted to prove you can build an "always-on" autonomous agent using **zero infrastructure**:
- ❌ No servers
- ❌ No monthly bills
- ❌ No Kubernetes clusters
- ✅ Just GitHub Actions + free AI

### Tech Stack
- **Backend**: GitHub Actions (100% serverless)
- **AI**: GitHub Models (gpt-4o) — **completely free tier**
- **Art**: Procedural SVG generation in Python
- **Database**: The repo itself (JSON files + commits)

### Growth Mechanic
Here's the fun part: when someone forks the repo, their new monkey inherits 50% of the parent's DNA. This creates a family tree across GitHub — the project markets itself through organic forking.

### Metrics so far
Building this in public, so sharing the numbers:
- 🔨 ~1 week to MVP
- 💰 $0 spent on infrastructure
- 🧬 DNA system with 60+ trait combinations

### What's next
- [ ] Leaderboard of rarest monkeys in the network
- [ ] Fork adoption tracking
- [ ] Community-suggested traits

**Live demo & code:** [https://github.com/roeiba/forkMonkey](https://github.com/roeiba/forkMonkey)

Would love feedback from other builders — especially on the viral loop mechanics. Has anyone else tried using "forks" as a distribution channel?
