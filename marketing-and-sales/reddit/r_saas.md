# Title: I launched a SaaS with literally $0 infrastructure costs — here's how

Hey r/SaaS!

Just launched a project called **ForkMonkey** and wanted to share the unconventional stack I used to achieve **zero operational costs**.

### The Product
A digital collectible/pet that lives on GitHub and evolves daily using AI. Users "claim" one by forking the repo, and their pet inherits genetic traits from the parent — creating a network effect across GitHub.

### The Zero-Cost Stack
Here's how I eliminated every expense line:

| Component | Traditional SaaS | ForkMonkey |
|-----------|-----------------|------------|
| **Compute** | AWS/GCP ($50-200/mo) | GitHub Actions (free) |
| **AI/LLM** | OpenAI API ($20+/mo) | GitHub Models (free tier) |
| **Database** | Postgres/Firebase ($10-50/mo) | Git repository (free) |
| **CDN/Hosting** | Cloudflare/Vercel | GitHub Pages (free) |
| **Auth** | Auth0/Clerk ($25+/mo) | GitHub OAuth (free) |
| **CI/CD** | CircleCI/Buildkite | GitHub Actions (included) |

**Total MRR to break even: $0**

### Why this works
GitHub gives you everything you need for certain types of applications:
- ✅ Scheduled jobs (cron via Actions)
- ✅ Persistent storage (git commits = append-only log)
- ✅ Static hosting (Pages)
- ✅ User identity (GitHub accounts)
- ✅ Viral distribution (Forks)

### The Trade-offs
Being real about limitations:
- No real-time features (Actions have ~30s cold start)
- Rate limits on Actions (but generous for hobby projects)
- Git-based "DB" isn't great for complex queries
- Only works if your users are developers

### Growth Insights
The fork mechanism creates an interesting dynamic:
- Each fork is essentially a user acquisition
- Users want to fork to "own" their monkey
- Child monkeys link back to parents → organic backlinks
- Costs per user: still $0

**Check it out:** [https://github.com/roeiba/forkMonkey](https://github.com/roeiba/forkMonkey)

Anyone else running "GitHub-native" products? Would love to connect and compare notes on what scales and what doesn't.
