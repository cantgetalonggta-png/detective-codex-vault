#!/usr/bin/env python3
"""DETECTIVE CODEX — book / old video-game style investigation desk v1.2"""
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
.codex-title { font-family: 'Press Start 2P', monospace; color: #f0c14b; font-size: 1.05rem; line-height: 1.8; }
.chapter { border: 3px double #8b6914; background: #24180f; padding: 1rem 1.2rem; border-radius: 4px; margin-bottom: .8rem; color: #e8dcc8; font-family: 'Special Elite', cursive; }
.hp-yellow { color: #fbbf24; } .hp-red { color: #f87171; } .hp-green { color: #4ade80; }
.pixel-bar { height: 12px; background: #3f2a1a; border: 2px solid #8b6914; }
.pixel-fill { height: 100%; background: linear-gradient(90deg, #b45309, #fbbf24); }
div[data-testid="stMetricValue"] { color: #f0c14b !important; font-family: 'Press Start 2P', monospace; font-size: .65rem !important; }
.arc { font-family: ui-monospace, monospace; font-size: .85rem; color: #d6c6a0; border-left: 3px solid #8b6914; padding-left: .6rem; margin: .25rem 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="codex-title">📜 DETECTIVE CODEX v1.2</p>', unsafe_allow_html=True)
st.caption("BOOK / OLD VIDEO-GAME · dual-persist GitHub+Drive · public ceiling · PBP CONTRADICTED · Meridian RETIRING")

s = DATA.get("stats") or {}
c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("PEOPLE", s.get("n_people"))
c2.metric("ENTITIES", s.get("n_entities"))
c3.metric("LOCATIONS", s.get("n_locations"))
c4.metric("HYPS", s.get("n_hypotheses"))
c5.metric("MY THEORIES", s.get("n_my_theories_individual"))
c6.metric("DEEP ARCS", s.get("n_arcs_deep"))

with st.sidebar:
    st.markdown("### 🎮 CODEX MENU")
    page = st.radio("Chapter", [
        "📖 Title Page",
        "✅ Status / Dual-Persist",
        "👤 Cast of Characters",
        "🏛 Entities & Places",
        "🟨 Hypotheses (Yellow/Red)",
        "🧠 My Theories Individually",
        "🕸 Theory Web + Narrative",
        "🔗 Deep Arcs",
        "🟥 Contradictions",
        "📅 Timeline Scroll",
        "⛓ Logic Chain",
        "📁 Drive Distill",
        "📤 Export",
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
my_th = DATA.get("my_theories_individual") or []
arcs = DATA.get("arcs_deepest") or []
status = DATA.get("status_board") or {}

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
    st.success("Codex v1.2 forces GitHub push + Drive upload and verifies both.")

elif page.startswith("✅"):
    st.subheader("Status board / dual-persist")
    dp = status.get("dual_persist") or {}
    gh = dp.get("github") or {}
    dr = dp.get("drive") or {}
    st.markdown(f"""<div class="chapter">
    <h3 class="hp-green">GitHub</h3>
    <p>Repo: <code>{gh.get('repo')}</code><br/>
    URL: {gh.get('url')}<br/>
    Prior: {gh.get('prior_status')}<br/>
    This run: <b>{gh.get('this_run')}</b></p>
    <h3 class="hp-yellow">Drive</h3>
    <p>Folder: {dr.get('folder')}<br/>
    URL: {dr.get('url')}<br/>
    Prior: <span class="hp-red">{dr.get('prior_status')}</span><br/>
    This run: <b>{dr.get('this_run')}</b></p>
    </div>""", unsafe_allow_html=True)
    hs = status.get("hypothesis_status_summary") or {}
    st.markdown("### Hypothesis status")
    st.write(f"Yellow open: {hs.get('n_yellow')} · Red contradicted: {hs.get('n_red')}")
    st.json(hs)
    st.markdown("### Never list")
    for n in status.get("never_list") or []:
        st.write("🚫 " + n)
    st.info(status.get("next",""))

elif page.startswith("👤"):
    st.subheader("Cast of Characters — every name & role")
    rows = []
    for p in people:
        if not hit(p, q): continue
        rows.append({"ID": p["id"], "Name": p["name"], "Roles": "; ".join(p.get("roles") or []),
                     "Tag": p.get("tag"), "Color": p.get("color"), "Status": p.get("status"),
                     "Pipelines": ",".join(p.get("pipelines") or [])})
    st.dataframe(rows, use_container_width=True, height=420)
    opts = [f"{p['id']} — {p['name']}" for p in people if hit(p,q)]
    if opts:
        pick = st.selectbox("Open character sheet", opts)
        p = next(x for x in people if f"{x['id']} — {x['name']}" == pick)
        st.markdown(f"""<div class="chapter"><h3>{p['name']}</h3>
        <p>ID: {p['id']}<br/>Roles: {', '.join(p.get('roles') or [])}<br/>Tag: {p.get('tag')}<br/>
        Color: {p.get('color')} · Status: {p.get('status')}<br/>
        Window: {p.get('window')}<br/>Locations: {p.get('locations')}<br/>Pipelines: {p.get('pipelines')}<br/>
        Notes: {p.get('notes','—')}<br/>
        Photo policy: {p.get('photo_policy','—')}<br/>
        {('<span class="hp-red"><b>VERDICT: '+p['verdict']+'</b></span>') if p.get('verdict') else ''}</p></div>""", unsafe_allow_html=True)

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
    st.subheader("Hypotheses — individual yellow/red chapters + deep arcs")
    filt = st.radio("Filter", ["All","Yellow only","Red only"], horizontal=True)
    for h in hyps:
        if not hit(h, q): continue
        if filt=="Yellow only" and h.get("color")!="yellow": continue
        if filt=="Red only" and h.get("color")!="red": continue
        col = "hp-red" if h.get("color")=="red" else "hp-yellow"
        conf = float(h.get("confidence") or 0)
        arcs_html = "".join([f"<div class='arc'>{a['from']} → {a['to']} [{a['type']}] <code>{a['tag']}</code> — {a['detail']}</div>" for a in (h.get("arcs_deep") or [])])
        st.markdown(f"""<div class="chapter">
        <h3 class="{col}">{h['id']} — {h['name']}</h3>
        <p>Status: <b>{h.get('status')}</b> · Confidence: {conf} · Pipeline: {h.get('pipeline')}</p>
        <div class="pixel-bar"><div class="pixel-fill" style="width:{int(conf*100)}%"></div></div>
        <p style="margin-top:.8rem">{h.get('theory')}</p>
        <p>Supporting: {', '.join(h.get('supporting') or [])}<br/>
        Ties to: {', '.join(h.get('ties_to') or [])}<br/>
        Entities: {', '.join(h.get('entities') or [])}<br/>
        Timeline: {', '.join(map(str, h.get('timeline') or []))}<br/>
        Gaps: {', '.join(h.get('gaps') or [])}</p>
        <p><b>Deep arcs</b></p>{arcs_html}
        {"<p class='hp-red'><b>VERDICT: "+h['verdict']+"</b></p>" if h.get('verdict') else ""}
        </div>""", unsafe_allow_html=True)

elif page.startswith("🧠"):
    st.subheader("My theories individually (from MY THEORIES.pdf)")
    for t in my_th:
        if not hit(t, q): continue
        col = "hp-yellow"
        st.markdown(f"""<div class="chapter">
        <h3 class="{col}">{t['id']} — {t['name']}</h3>
        <p>Status: <b>{t.get('status')}</b> · Tag: <code>{t.get('tag')}</code></p>
        <p>{t.get('summary')}</p>
        <p>Ties: {', '.join(t['ties']) if isinstance(t.get('ties'), list) else t.get('ties')}</p>
        </div>""", unsafe_allow_html=True)

elif page.startswith("🕸"):
    st.subheader("Theory web — how they all tie together")
    st.markdown(f"""<div class="chapter"><p>{web.get('spine')}</p></div>""", unsafe_allow_html=True)
    for e in web.get("edges") or []:
        st.write(f"**{e['from']}** → **{e['to']}**: {e['link']}  `[{e['tag']}]`")
    st.markdown("### My narrative")
    nc = web.get("my_narrative_control") or {}
    st.markdown(f"""<div class="chapter"><p>{nc.get('my_narrative','')}</p></div>""", unsafe_allow_html=True)
    st.info(nc.get("spine_sentence",""))
    st.markdown("### Narrative control rules")
    for r in nc.get("rules") or []:
        st.write("• " + r)

elif page.startswith("🔗"):
    st.subheader("Deep arcs — deepest relationship details")
    rows = []
    for a in arcs:
        if not hit(a, q): continue
        rows.append({"From": a.get("from"), "To": a.get("to"), "Type": a.get("type"),
                     "Tag": a.get("tag"), "Detail": a.get("detail"), "Via": a.get("hypothesis")})
    st.dataframe(rows, use_container_width=True, height=520)

elif page.startswith("🟥"):
    st.subheader("Contradictions & confirmed")
    for c in DATA.get("contradictions") or []:
        st.markdown(f"""<div class="chapter"><h3 class="hp-red">{c['id']} — {c['name']}</h3>
        <p>{c.get('notes','')} · status {c.get('status')}</p></div>""", unsafe_allow_html=True)
    st.markdown("### Confirmed (green)")
    for c in DATA.get("confirmed") or []:
        st.markdown(f"- <span class='hp-green'>{c['id']}</span> {c['name']} · {c.get('tag')}", unsafe_allow_html=True)

elif page.startswith("📅"):
    st.subheader("Timeline scroll")
    for t in DATA.get("timeline") or []:
        if not hit(t, q): continue
        st.markdown(f"""<div class="chapter"><b>{t.get('year')}</b> — {t.get('event')}
        <br/><i>{t.get('tag')}</i> · people {t.get('people')}</div>""", unsafe_allow_html=True)

elif page.startswith("⛓"):
    st.subheader("Operator logic chain")
    for sstep in DATA.get("logic_chain_steps") or []:
        st.markdown(f"""<div class="chapter"><b>Step {sstep['step']} — {sstep['role']}</b><br/>{sstep['who']} · {sstep['tag']}</div>""", unsafe_allow_html=True)
    st.markdown("### BC-PIPE")
    st.dataframe(DATA.get("bc_pipe") or [], use_container_width=True)
    st.markdown("### DM-1..10")
    st.dataframe(DATA.get("discovery_methods_dm") or [], use_container_width=True)

elif page.startswith("📁"):
    st.subheader("Drive Investigations distill — all folders")
    di = DATA.get("drive_inventory") or {}
    st.markdown("### Blocked secrets")
    for b in di.get("blocked_secrets") or []:
        st.error(f"🚫 {b['name']} ({b['folder']}) — {b['status']}")
    st.markdown("### Document distills (ingested)")
    for dd in di.get("document_distills") or []:
        st.markdown(f"""<div class="chapter"><h3>{dd['doc_id']} — {dd['source']}</h3>
        <p>Folder: {dd.get('folder')} · Status: <b>{dd.get('status')}</b></p>
        <p>{dd.get('summary')}</p>
        <p><i>{dd.get('tag_split')}</i></p></div>""", unsafe_allow_html=True)
    st.markdown("### Full folder title index")
    st.json(di.get("folders") or {})

else:
    st.subheader("Export & dual-persist")
    st.code("streamlit run /workspace/artifacts/detective-codex/app.py --server.port 8502 --server.address 0.0.0.0 --server.headless true")
    st.download_button("Download FULL_EXPORT.json", data=json.dumps(DATA, indent=2), file_name="FULL_EXPORT.json")
    md_path = ROOT/"exports"/"FULL_EXPORT.md"
    st.download_button("Download FULL_EXPORT.md", data=md_path.read_text() if md_path.exists() else "", file_name="FULL_EXPORT.md")
    st.markdown("### Dual-persist targets")
    st.write("- GitHub: `cantgetalonggta-png/detective-codex-vault`")
    st.write("- Drive: `detective-codex-2026-09-11` under skill-tree")
    st.caption(DATA.get("meridian_note"))
    st.json(DATA.get("public_links") or {})

st.markdown("---")
st.caption("DETECTIVE CODEX v1.2 · book mode · public only · dual-persist required · PBP CONTRADICTED")
