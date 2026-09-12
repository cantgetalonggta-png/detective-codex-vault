# Investigation Book — live links

## MANDATORY primary (preview proxy)

**https://hds-ulr0smxx8txg-6014-wcpq0.grok-code-wild.hades-www**

| Field | Value |
|-------|--------|
| Preview proxy | `:6014` → app on `:8080` |
| Host | `hds-ulr0smxx8txg` |
| Target | `agent_target=8080` · framework=`streamlit` |
| Auth | First open may go through **https://grok.com/preview-auth** (owner cookie) |

**Always use the preview proxy link above as the primary browser link.**

## Secondary (in-sandbox only)

| Where | URL |
|--------|-----|
| Local | http://127.0.0.1:8080 |
| Network | http://172.16.0.2:8080 |

## App
- Path: `/workspace/artifacts/detective-codex-vault/app.py`
- Version: **4.0.0-interactive-book**
- Port: **8080**

## Restart
```bash
streamlit run app.py --server.port 8080 --server.address 0.0.0.0 --server.headless true
```
