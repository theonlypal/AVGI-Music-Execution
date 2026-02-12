# AVGI Music Execution

One-shot SwiftAPI-enforced music render flow that generates `Pyramids_instrumental.wav` (or another track name), with attestation-aware execution handling.

## Quick start

1. Install dependencies:
   ```bash
   pip install swiftapi
   ```
2. Export your live key:
   ```bash
   export SWIFTAPI_KEY="swiftapi_live_..."
   ```
3. Run the workflow:
   ```bash
   python avgi_music_execution.py
   ```

## Optional overrides

```bash
TRACK_NAME="Pyramids" MUSIC_RENDER_INTENT="Generate clean instrumental with precise plugin chain" python avgi_music_execution.py
```

## Mobile/Safari note

This repo now includes a standalone script for Codex/web execution, but shipping to a production mobile endpoint still requires your deployment target (for example, a hosted API, serverless function, or CI/CD pipeline tied to your app/backend).
