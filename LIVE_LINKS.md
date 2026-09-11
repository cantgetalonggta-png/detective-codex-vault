# Investigation Encyclopedia — live links

## App
- Path: `/workspace/artifacts/detective-codex-vault/app.py`
- Version: **3.0.0-encyclopedia** (plain index — no game UI, no command console)
- Port: **8080**
- Local: http://127.0.0.1:8080
- Network: http://172.16.0.2:8080

## Audio
- MP3: `audio/theories-plausibility-panel-15min.mp3` (~15m 45s)
- Script: `audio/theories-plausibility-panel-SCRIPT.md`
- Drive folder: detective-codex-2026-09-11

## Restart
```bash
streamlit run /workspace/artifacts/detective-codex-vault/app.py \
  --server.port 8080 --server.address 0.0.0.0 --server.headless true
```
