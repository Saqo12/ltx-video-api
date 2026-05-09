# 🎬 LTX-Video API on Google Colab

**Step 1:** Open in Colab → [![](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github.com/Saqo12/ltx-video-api/blob/main/ltx_video_api.ipynb)

**Step 2:** Get your ngrok token from [dashboard.ngrok.com](https://dashboard.ngrok.com) (free account)

**Step 3:** Run the cells in order, paste your ngrok token when asked

**Step 4:** Copy the `🎬 LTX-Video API:` URL it prints → paste into your TikTok pipeline

---

## ⚠️ Important

- **Keep the Colab tab open** — sessions last ~12 hours
- **Re-run the bottom cell** if the session drops
- The T4 GPU in free Colab is enough for 512×512, 4-second clips
- For longer/higher-res videos, upgrade to Colab Pro

## API Usage

```bash
# After the API is running, call it like this:
curl -X POST "https://your-ngrok-url.ngrok.io/generate" \
  -F "prompt=A young entrepreneur working on their laptop at a coffee shop" \
  -F "duration_seconds=4" \
  -F "width=512" \
  -F "height=512" \
  --output video.mp4
```

The API returns a base64-encoded MP4, or use the `--output` flag directly.

## Cost

- **Free**: Colab T4 GPU (512×512, ~4s clips)
- **~$10/mo**: Colab Pro (A100, longer clips, more memory)
