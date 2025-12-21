# Show HN: A Tamagotchi that lives in a GitHub repo and evolves daily with AI

**Title**: Show HN: A Tamagotchi that lives in a GitHub repo and evolves daily with AI

**URL**: https://github.com/roeiba/forkMonkey

---

## Post Body (for text post option):

I built ForkMonkey – an experiment in "autonomous agents" using only free GitHub infrastructure.

**What it does:**
- A digital pet (JSON state + SVG visualization) lives in your GitHub repo
- Every night, a GitHub Action asks GPT-4o (via GitHub Models, free) how the pet should evolve
- Forking the repo = breeding a new monkey that inherits traits from the parent + random mutations
- A community family tree is forming across GitHub

**Tech stack:** Python, GitHub Actions, GitHub Models (free AI tier), SVG generation

**Why?** I wanted to see if you could create a "living" system that costs $0 to run indefinitely. The answer is yes.

**The interesting bit:** Since forking is the breeding mechanism, every new user automatically extends the family tree. There are already 20+ monkeys with visible lineages across different GitHub accounts.

Try it: https://github.com/roeiba/forkMonkey

Live demo: https://roeiba.github.io/forkMonkey

Happy to answer questions about the architecture!

---

## Anticipated Questions & Answers:

**Q: What happens if GitHub changes their free tier?**
A: The core genetics/evolution works without AI too – it just falls back to random mutations. The AI is the "brain" but not required.

**Q: Isn't this just a gimmick?**
A: Yes and no. It's a proof-of-concept for serverless AI agents. The pattern could apply to auto-updating dashboards, living documentation, or any "fire and forget" autonomous system.

**Q: Why monkeys?**
A: They're fun to draw in SVG and have enough visual variety (colors, accessories, expressions) to make the genetics system interesting.

**Q: Can I run this privately?**
A: Yes, but GitHub Pages won't work. You'd need to host the web view elsewhere.

**Q: How do you prevent abuse?**
A: Each fork is isolated. The worst someone can do is make their own weird monkey. The parent repo is unaffected.

---

## Best Posting Times:
- Tuesday 9-10am ET (best)
- Wednesday 9-10am ET
- Thursday 9-10am ET

## Tips:
1. Respond to comments within 5 minutes
2. Be humble and curious
3. Admit flaws before critics find them
4. Share technical details proactively
5. Never argue, just explain

