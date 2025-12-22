# ForkMonkey Screenshots & Videos

> 📸 Ready-to-use assets for **peerpush.net** and other marketing submissions

## Promotional Videos (MP4)
Polished video demos located in `../promo_videos/` (parent directory):

| File | Description | Best For |
|------|-------------|----------|
| `promo_full_walkthrough.mp4` | **Complete App Tour** (Dashboard, Evolution, Tree, Community) | **PeerPush Launch** |
| `promo_main_features.mp4` | **Core Features** (Dashboard, Evolution, Tree) | Rapid Demos |
| `promo_social_features.mp4` | **Social Features** (Community, Leaderboard) | Social Proof |

## Screenshots (PNG)

| # | File | Description |
|---|------|-------------|
| 1 | `01_leaderboard.png` | Rarity Leaderboard showing community rankings |
| 2 | `02_dashboard.png` | Main dashboard with monkey avatar, stats & traits |
| 3 | `03_evolution.png` | Evolution timeline showing history |
| 4 | `04_evolution_detail.png` | Evolution detail modal with DNA & story |
| 5 | `05_community.png` | Community gallery with all forked monkeys |
| 6 | `06_family_tree.png` | Family tree visualization (full view) |
| 7 | `07_family_tree_zoomed.png` | Family tree zoomed in on nodes |

## Video Recordings (WebP)

Located in the `videos/` subfolder - animated recordings showing app interaction:

| # | File | Description |
|---|------|-------------|
| 1 | `01_leaderboard_view.webp` | Scrolling through the leaderboard |
| 2 | `02_dashboard_view.webp` | Exploring the main dashboard |
| 3 | `03_evolution_view.webp` | Browsing evolution timeline & opening details |
| 4 | `04_community_view.webp` | Scrolling through community gallery |
| 5 | `05_family_tree_view.webp` | Interactive family tree with zoom/pan |

## Usage

These assets are captured from the production site:
- **URL**: https://roeiba.github.io/forkMonkey/
- **Resolution**: 1400x900 (desktop)
- **Date**: December 2025

### For PeerPush.net Submission

Recommended order for showcasing the app:
1. **Hero**: `02_dashboard.png` - Shows the core product
2. **Feature 1**: `03_evolution.png` - AI-powered evolution
3. **Feature 2**: `05_community.png` - Community & social aspect
4. **Feature 3**: `06_family_tree.png` - Fork visualization
5. **Gamification**: `01_leaderboard.png` - Competitive element

## Tools & Regeneration
A helper script `process_videos.py` is located in the parent directory (`marketing-and-sales/`).
It converts the WebP recordings into the polished MP4 promos using `ffmpeg` and `Pillow`.

**Requirements**:
- Python 3
- `Pillow` (`pip install Pillow`)
- `ffmpeg` (e.g., `brew install ffmpeg`)

**To regenerate videos:**
```bash
cd marketing-and-sales
python process_videos.py
```

---
*Last updated: December 21, 2025*
