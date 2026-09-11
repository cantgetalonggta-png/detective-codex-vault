#!/usr/bin/env python3
"""DETECTIVE CODEX — book / old video-game style investigation desk"""
from __future__ import annotations
import json
from pathlib import Path
import streamlit as st
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data" / "FULL_EXPORT.json").read_text())

st.set_page_config(page_title="Detective Codex", page_icon="📜", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Special+Elite&family=Cinzel:wght@600&display=swap');
.stApp { background: #1a120b; background-image: radial-gradient(ellipse at top, #2a1c12 0%, #0d0a08 70%); }
h1,h2,h3 { font-family: 'Cinzel', serif !important; color: #e8d5a3 !important; }
.codex-title { font-family: 'Press Start 2P', monospace; color: #f0c14b; font-size: 1.1rem; line-height: 1.8; }
.chapter { border: 3px double #8b6914; background: #24180f; padding: 1rem 1.2rem; border-radius: 4px; margin-bottom: .8rem; color: #e8dcc8; font-family: 'Special Elite', cursive; }
.hp-yellow { color: #fbbf24; } .hp-red { color: #f87171; } .hp-green { color: #4ade80; }
.pixel-bar { height: 12px; background: #3f2a1a; border: 2px solid #8b6914; }
.pixel-fill { height: 100%; background: linear-gradient(90deg, #b45309, #fbbf24); }
div[data-testid="stMetricValue"] { color: #f0c14b !important; font-family: 'Press Start 2P', monospace; font-size: .7rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="codex-title">📜 DETECTIVE CODEX</p>', unsafe_allow_html=True)
st.caption("BOOK / OLD VIDEO-GAME STYLE · your vault · public ceiling · PBP CONTRADICTED · Meridian world-map retiring")

s = DATA.get("stats") or {}
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("PEOPLE", s.get("n_people"))
c2.metric("ENTITIES", s.get("n_entities"))
c3.metric("LOCATIONS", s.get("n_locations"))
c4.metric("THEORIES", s.get("n_hypotheses"))
c5.metric("DRIVE FOLDERS", s.get("n_drive_folders_indexed"))

with st.sidebar:
    st.markdown("### 🎮 CODEX MENU")
    page = st.radio("Chapter", [
        "📖 Title Page",
        "👤 Cast of Characters",
        "🏛 Entities & Places",
        "🟨 Theories (Yellow)",
        "🟥 Contradictions",
        "🕸 Theory Web",
        "📅 Timeline Scroll",
        "⛓ Logic Chain",
        "📁 Drive Distill",
        "📤 Export / Dual-Persist",
    ])
    st.markdown("---")
    st.error("🚫 NEVER secrets · NEVER victim photos")
    st.warning("PBP identity = CONTRADICTED")
    q = st.text_input("Search codex", "")

def hit(obj, q):
    if not q: return True
    return q.lower() in json.dumps(obj, default=str).lower()

people = DATA.get("people") or []
hyps = DATA.get("hypotheses") or []
ents = DATA.get("entities") or []
locs = DATA.get("locations") or []
web = DATA.get("theory_web") or {}

if page.startswith("📖"):
    st.markdown(f"""
    <div class="chapter">
    <h2>User Vault — Epstein Investigation</h2>
    <p>{DATA.get('ceiling')}</p>
    <p><b>App style:</b> {DATA.get('app_style')}</p>
    <p><b>As-of:</b> {DATA.get('as_of')} · v{DATA.get('version')}</p>
    <hr/>
    <p>{(web.get('my_narrative_control') or {}).get('spine_sentence','')}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### Why dual-persist lagged")
    for x in DATA.get("why_dual_persist_lagged") or []:
        st.write("• " + x)
    st.success("This codex is the dual-persist payload for GitHub + Drive.")

elif page.startswith("👤"):
    st.subheader("Cast of Characters — every name & role")
    rows = []
    for p in people:
        if not hit(p, q): continue
        rows.append({"ID": p["id"], "Name": p["name"], "Roles": "; ".join(p.get("roles") or []),
                     "Tag": p.get("tag"), "Color": p.get("color"), "Pipelines": ",".join(p.get("pipelines") or [])})
    st.dataframe(rows, use_container_width=True, height=420)
    pick = st.selectbox("Open character sheet", [f"{p['id']} — {p['name']}" for p in people if hit(p,q)])
    p = next(x for x in people if f"{x['id']} — {x['name']}" == pick)
    st.markdown(f"""<div class="chapter"><h3>{p['name']}</h3>
    <p>ID: {p['id']}<br/>Roles: {', '.join(p.get('roles') or [])}<br/>Tag: {p.get('tag')}<br/>
    Window: {p.get('window')}<br/>Locations: {p.get('locations')}<br/>Pipelines: {p.get('pipelines')}<br/>
    Photo policy: {p.get('photo_policy','—')}</p></div>""", unsafe_allow_html=True)

elif page.startswith("🏛"):
    a,b = st.tabs(["Entities", "Locations"])
    with a:
        st.dataframe([e for e in ents if hit(e,q)], use_container_width=True, height=400)
    with b:
        st.dataframe([l for l in locs if hit(l,q)], use_container_width=True, height=300)
        m = pd.DataFrame([{"lat": float(l["lat"]), "lon": float(l["lon"])} for l in locs if l.get("lat") is not None])
        if not m.empty:
            st.map(m, size=40, color="#f0c14b")

elif page.startswith("🟨"):
    st.subheader("Theories — individual yellow/red chapters")
    for h in hyps:
        if not hit(h, q): continue
        col = "hp-red" if h.get("color")=="red" else "hp-yellow"
        conf = float(h.get("confidence") or 0)
        st.markdown(f"""<div class="chapter">
        <h3 class="{col}">{h['id']} — {h['name']}</h3>
        <p>Status: <b>{h.get('status')}</b> · Confidence: {conf}</p>
        <div class="pixel-bar"><div class="pixel-fill" style="width:{int(conf*100)}%"></div></div>
        <p style="margin-top:.8rem">{h.get('theory')}</p>
        <p>Ties to: {', '.join(h.get('ties_to') or [])}<br/>
        Entities: {', '.join(h.get('entities') or [])}<br/>
        Timeline: {', '.join(map(str, h.get('timeline') or []))}<br/>
        Gaps: {', '.join(h.get('gaps') or [])}</p>
        {"<p class='hp-red'><b>VERDICT: "+h['verdict']+"</b></p>" if h.get('verdict') else ""}
        </div>""", unsafe_allow_html=True)

elif page.startswith("🟥"):
    st.subheader("Contradictions & confirmed")
    for c in DATA.get("contradictions") or []:
        st.markdown(f"""<div class="chapter"><h3 class="hp-red">{c['id']} — {c['name']}</h3>
        <p>{c.get('notes','')} · status {c.get('status')}</p></div>""", unsafe_allow_html=True)
    st.markdown("### Confirmed (green)")
    for c in DATA.get("confirmed") or []:
        st.markdown(f"- <span class='hp-green'>{c['id']}</span> {c['name']} · {c.get('tag')}", unsafe_allow_html=True)

elif page.startswith("🕸"):
    st.subheader("Theory web — how they all tie together")
    st.markdown(f"""<div class="chapter"><p>{web.get('spine')}</p></div>""", unsafe_allow_html=True)
    for e in web.get("edges") or []:
        st.write(f"**{e['from']}** → **{e['to']}**: {e['link']}  `[{e['tag']}]`")
    st.markdown("### My narrative control")
    nc = web.get("my_narrative_control") or {}
    st.info(nc.get("spine_sentence",""))
    for r in nc.get("rules") or []:
        st.write("• " + r)

elif page.startswith("📅"):
    st.subheader("Timeline scroll")
    for t in DATA.get("timeline") or []:
        if not hit(t, q): continue
        st.markdown(f"""<div class="chapter"><b>{t.get('year')}</b> — {t.get('event')}
        <br/><i>{t.get('tag')}</i></div>""", unsafe_allow_html=True)

elif page.startswith("⛓"):
    st.subheader("Operator logic chain")
    for s in DATA.get("logic_chain_steps") or []:
        st.markdown(f"""<div class="chapter"><b>Step {s['step']} — {s['role']}</b><br/>{s['who']} · {s['tag']}</div>""", unsafe_allow_html=True)
    st.markdown("### BC-PIPE")
    st.dataframe(DATA.get("bc_pipe") or [], use_container_width=True)
    st.markdown("### DM-1..10")
    st.dataframe(DATA.get("discovery_methods_dm") or [], use_container_width=True)

elif page.startswith("📁"):
    st.subheader("Drive Investigations distill")
    di = DATA.get("drive_inventory") or {}
    st.json(di)
    st.markdown(Path("/workspace/artifacts/drive-distill-2026-09-11-full/DRIVE_FOLDER_DISTILL.md").read_text() if Path("/workspace/artifacts/drive-distill-2026-09-11-full/DRIVE_FOLDER_DISTILL.md").exists() else "_missing_")

else:
    st.subheader("Export & dual-persist")
    st.code("streamlit run /workspace/artifacts/detective-codex/app.py --server.port 8502 --server.address 0.0.0.0 --server.headless true")
    st.download_button("Download FULL_EXPORT.json", data=json.dumps(DATA, indent=2), file_name="FULL_EXPORT.json")
    st.download_button("Download FULL_EXPORT.md", data=(ROOT/"exports"/"FULL_EXPORT.md").read_text() if (ROOT/"exports"/"FULL_EXPORT.md").exists() else "", file_name="FULL_EXPORT.md")
    st.markdown("### Dual-persist targets")
    st.write("- GitHub: `cantgetalonggta-png/detective-codex-vault` (new or existing)")
    st.write("- Drive: skill-tree / Grok-Agent-Vault public distill folder")
    st.caption(DATA.get("meridian_note"))

st.markdown("---")
st.caption("DETECTIVE CODEX · book mode · public only · dual-persist required")
