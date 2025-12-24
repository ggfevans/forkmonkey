# Experiment 2: Video-Based Frame Extraction

## Approach

Generate videos of the monkey in motion using Gemini AI video generation, then extract frames and convert to animated GIFs.

## Method

1. **Video Generation:** Use Gemini Video Generation to create ~6 second videos with white background
2. **Frame Extraction:** Use ffmpeg to extract frames at 4 FPS from the video
3. **Processing:** Remove white background, resize to 111×101, and remove semi-transparency
4. **Assembly:** Select evenly-spaced frames to create smooth animation cycle GIFs

## Results

✅ **Pros:**
- **Single API call per animation** (vs 6-8 calls in Experiment 1)
- **8x faster** generation (~30 seconds vs 4 minutes per animation)
- **28-42% smaller files**
- **Lower cost** (1 video generation vs multiple image generations)
- **Smooth, natural motion** from video
- **Easy to extract different cycles** from same video

❌ **Cons:**
- Less control over specific poses
- Limited to motion shown in video
- One animation type per video
- Requires video processing tools (ffmpeg)

## Animations Created

### 1. Walking Animation
- **Video:** `walking_monkey.mp4` (5.9 sec, 141 frames)
- **GIF:** `brown_walk_8fps.gif` (12.0 KB, 6 frames)
- **Savings:** 42% smaller than Experiment 1 (20.8 KB)

### 2. Running Animation
- **Video:** `running_monkey.mp4` (5.9 sec, 141 frames)
- **GIF:** `brown_run_8fps.gif` (20.1 KB, 8 frames)
- **Savings:** 28% smaller than Experiment 1 (28.0 KB)

## Technical Details

- **AI Model:** Gemini Video Generation
- **Video Specs:** 1920×1080, 24 FPS, ~6 seconds
- **Extraction:** 4 FPS = ~24 frames extracted per video
- **Generation Time:** ~30 seconds per video
- **Processing Time:** ~5 seconds per GIF
- **Total Size:** 32.1 KB (2 GIFs)

## Comparison with Experiment 1

| Animation | Experiment 1 | Experiment 2 | Savings |
|-----------|--------------|--------------|---------|
| Walk | 20.8 KB | 12.0 KB | **42%** |
| Run | 28.0 KB | 20.1 KB | **28%** |
| **Total** | **48.8 KB** | **32.1 KB** | **34%** |

### Overall Metrics

| Metric | Experiment 1 | Experiment 2 | Winner |
|--------|--------------|--------------|--------|
| API Calls | 14 (2 animations) | 2 (2 animations) | ✅ Exp 2 |
| Generation Time | ~8 min | ~1 min | ✅ Exp 2 |
| File Size | 48.8 KB | 32.1 KB | ✅ Exp 2 |
| Control | High | Medium | ✅ Exp 1 |
| Motion Quality | Good | Excellent | ✅ Exp 2 |

## File Structure

```
experiment2/
├── videos/
│   ├── walking_monkey.mp4     # Walking video
│   └── running_monkey.mp4     # Running video
├── frames/
│   └── frame_*.png            # Walking frames
├── frames_run/
│   └── run_frame_*.png        # Running frames
├── gifs/
│   ├── brown_walk_8fps.gif    # Walking GIF (12 KB)
│   └── brown_run_8fps.gif     # Running GIF (20 KB)
├── scripts/
│   ├── video_to_gif.py        # Walking conversion
│   └── create_run_gif.py      # Running conversion
└── README.md                  # This file
```

## Usage

### Generate Videos

Use Gemini API to generate videos with prompts like:

```python
# Walking
"A cute brown monkey walking with a golden fork, pixel art style, 
white background, side view, 2-3 walking cycles"

# Running
"A cute brown monkey running fast with a golden fork, pixel art style,
white background, side view, energetic motion, 2-3 running cycles"
```

### Extract and Convert

```bash
# Walking animation
python3 scripts/video_to_gif.py

# Running animation
python3 scripts/create_run_gif.py
```

## Conclusion

**Experiment 2 is the clear winner for motion-based animations!**

### Key Achievements:
- ✅ **86% fewer API calls** (2 vs 14)
- ✅ **8x faster generation** (1 min vs 8 min)
- ✅ **34% smaller files** (32 KB vs 49 KB)
- ✅ **Smoother, more natural motion**
- ✅ **Lower costs**

### Recommended Hybrid Approach:

**Use Video Generation (Exp 2) for:**
- ✅ Walk animation
- ✅ Run animation
- ✅ Any motion-based animations

**Use Image Generation (Exp 1) for:**
- ✅ Idle animation (static pose with subtle breathing)
- ✅ Swipe animation (eating with fork)
- ✅ With ball animation (holding ball)

This hybrid approach:
- Minimizes API calls (~5 total vs 27)
- Reduces generation time (~3 min vs 19 min)
- Produces smaller files (~55 KB vs 93 KB)
- Maintains high quality across all animation types

## Next Steps

1. ✅ Walking animation complete
2. ✅ Running animation complete
3. ⏳ Consider generating idle animation via video (subtle breathing/movement)
4. ⏳ Combine best results from both experiments
5. ⏳ Create complete asset set for VS Code Pets integration
