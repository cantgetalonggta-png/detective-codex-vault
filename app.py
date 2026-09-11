#!/usr/bin/env python3
"""Investigation encyclopedia — plain index of vault metadata."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data" / "FULL_EXPORT.json").read_text())
VERSION = "3.0.0-encyclopedia"

st.set_page_config(
    page_title="Investigation Encyclopedia",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
.stApp { background: #f7f5f2; color: #1a1a1a; }
h1, h2, h3 { color: #111 !important; font-family: Georgia, 'Times New Roman', serif !important; }
.block {
  background: #fff; border: 1px solid #d0d0d0; border-radius: 4px;
  padding: 1rem 1.1rem; margin-bottom: .75rem; color: #222;
  font-family: Georgia, 'Times New Roman', serif; line-height: 1.55;
}
.meta { color: #555; font-size: .92rem; }
.tag { display:inline-block; background:#eee; border:1px solid #ccc;
  padding:1px 7px; border-radius:3px; font-size:.8rem; margin-right:.3rem; }
.tag-yes { background:#e8f5e9; border-color:#a5d6a7; }
.tag-maybe { background:#fff8e1; border-color:#ffe082; }
.tag-no { background:#ffebee; border-color:#ef9a9a; }
div[data-testid="stMetricValue"] { color:#111 !important; font-size:1.1rem !important; }
section[data-testid="stSidebar"] { background:#efeee9; border-right:1px solid #ccc; }
</style>
""",
    unsafe_allow_html=True,
)

people = DATA.get("people") or []
hyps = DATA.get("hypotheses") or []
ents = DATA.get("entities") or []
locs = DATA.get("locations") or []
web = DATA.get("theory_web") or {}
my_th = DATA.get("my_theories_individual") or []
arcs = DATA.get("arcs_deepest") or []
status = DATA.get("status_board") or {}
stats = DATA.get("stats") or {}
timeline = DATA.get("timeline") or []
contras = DATA.get("contradictions") or []
confirmed = DATA.get("confirmed") or []
drive_inv = DATA.get("drive_inventory") or {}


def match(obj: Any, q: str) -> bool:
    if not q:
        return True
    return q.lower() in json.dumps(obj, default=str).lower()


def status_tag(s: str) -> str:
    s = (s or "").lower()
    if "contradict" in s or "paused" in s:
        return "tag-no"
    if "maybe" in s or "theory" in s or "open" in s or "operator" in s:
        return "tag-maybe"
    if "rs" in s or "confirm" in s or "active" in s:
        return "tag-yes"
    return ""


st.title("Investigation Encyclopedia")
st.caption(
    f"Plain index of vault metadata · version {VERSION} · export {DATA.get('version')} · "
    f"as of {DATA.get('as_of')}"
)
st.info(
    "This is a reference index only. Entries marked MAYBE or theory are not established fact. "
    "Public record items are labeled where known. No secrets. The Palm Beach Pete identity claim is contradicted."
)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("People", stats.get("n_people"))
c2.metric("Organizations", stats.get("n_entities"))
c3.metric("Places", stats.get("n_locations"))
c4.metric("Hypotheses", stats.get("n_hypotheses"))
c5.metric("Operator theories", stats.get("n_my_theories_individual"))
c6.metric("Relationship notes", stats.get("n_arcs_deep"))

with st.sidebar:
    st.header("Index")
    section = st.radio(
        "Section",
        [
            "Overview",
            "People",
            "Organizations",
            "Places",
            "Hypotheses",
            "Operator theories",
            "How theories connect",
            "Relationship notes",
            "Contradictions",
            "Confirmed public items",
            "Timeline",
            "Methods and logic steps",
            "Drive document index",
            "Sources and export",
            "Audio panel",
        ],
    )
    q = st.text_input("Search index", placeholder="Name, place, or term")
    st.caption("Public ceiling · secrets excluded · identity claim contradicted")

if section == "Overview":
    st.subheader("What this encyclopedia contains")
    st.markdown(
        f"""
<div class="block">
<p><b>Scope:</b> {DATA.get('ceiling')}</p>
<p><b>Purpose:</b> A searchable index of people, organizations, places, hypotheses, operator theories,
relationship notes, contradictions, confirmed public items, and a timeline drawn from the vault export.
It is not a game, command console, or narrative desk.</p>
<p class="meta">Export id: {DATA.get('id')} · App: {VERSION}</p>
</div>
""",
        unsafe_allow_html=True,
    )
    spine = web.get("spine") or ""
    if spine:
        st.subheader("Operator narrative chain (labeled theory)")
        st.markdown(f'<div class="block"><p>{spine}</p></div>', unsafe_allow_html=True)
    hs = status.get("hypothesis_status_summary") or {}
    a, b = st.columns(2)
    with a:
        st.markdown("**Open or MAYBE hypotheses**")
        for hid in hs.get("yellow_open") or []:
            st.write(f"- {hid}")
    with b:
        st.markdown("**Contradicted**")
        for hid in hs.get("red_contradicted") or []:
            st.write(f"- {hid}")
    st.subheader("Limits")
    for n in DATA.get("never_list") or status.get("never_list") or []:
        st.write(f"- {n}")

elif section == "People":
    st.subheader("People")
    rows = []
    for p in people:
        if not match(p, q):
            continue
        rows.append(
            {
                "ID": p.get("id"),
                "Name": p.get("name"),
                "Roles": "; ".join(p.get("roles") or []),
                "Evidence tag": p.get("tag"),
                "Color label": p.get("color"),
                "Status": p.get("status"),
                "Notes": (p.get("notes") or "")[:160],
            }
        )
    st.dataframe(rows, use_container_width=True, height=420)
    opts = [f"{p['id']} — {p['name']}" for p in people if match(p, q)]
    if opts:
        pick = st.selectbox("Open person entry", opts)
        p = next(x for x in people if f"{x['id']} — {x['name']}" == pick)
        st.markdown(
            f"""
<div class="block">
<h3>{p.get('name')}</h3>
<p><span class="tag">{p.get('id')}</span>
<span class="tag {status_tag(str(p.get('tag')))}">{p.get('tag')}</span></p>
<p><b>Roles:</b> {', '.join(p.get('roles') or []) or '—'}</p>
<p><b>Status:</b> {p.get('status') or '—'} · <b>Color label:</b> {p.get('color') or '—'}</p>
<p><b>Time window:</b> {p.get('window') or '—'}</p>
<p><b>Places:</b> {p.get('locations') or '—'}</p>
<p><b>Pipelines:</b> {p.get('pipelines') or '—'}</p>
<p><b>Notes:</b> {p.get('notes') or '—'}</p>
<p><b>Photo policy:</b> {p.get('photo_policy') or '—'}</p>
{"<p><b>Verdict:</b> " + p.get('verdict') + "</p>" if p.get('verdict') else ""}
</div>
""",
            unsafe_allow_html=True,
        )

elif section == "Organizations":
    st.subheader("Organizations and entities")
    st.dataframe([e for e in ents if match(e, q)], use_container_width=True, height=480)

elif section == "Places":
    st.subheader("Places")
    rows = [
        {
            "ID": l.get("id"),
            "Name": l.get("name"),
            "Latitude": l.get("lat"),
            "Longitude": l.get("lon"),
            "Stage label": l.get("stage"),
            "Date note": l.get("date"),
            "Pipelines": ",".join(l.get("pipelines") or []),
        }
        for l in locs
        if match(l, q)
    ]
    st.dataframe(rows, use_container_width=True, height=360)
    m = pd.DataFrame(
        [{"lat": float(l["lat"]), "lon": float(l["lon"])} for l in locs if l.get("lat") is not None]
    )
    if not m.empty:
        st.map(m)

elif section == "Hypotheses":
    st.subheader("Hypotheses")
    st.caption("Each entry states the claim, status, confidence, and known gaps. MAYBE means unproven.")
    filt = st.radio("Filter", ["All", "Open / MAYBE", "Contradicted"], horizontal=True)
    for h in hyps:
        if not match(h, q):
            continue
        color = (h.get("color") or "").lower()
        if filt == "Open / MAYBE" and color == "red":
            continue
        if filt == "Contradicted" and color != "red":
            continue
        st.markdown(
            f"""
<div class="block">
<h3>{h.get('id')} — {h.get('name')}</h3>
<p>
<span class="tag {status_tag(str(h.get('status')))}">{h.get('status')}</span>
<span class="tag">confidence {h.get('confidence')}</span>
<span class="tag">{h.get('color')}</span>
</p>
<p>{h.get('theory') or '—'}</p>
<p><b>Supporting refs:</b> {', '.join(h.get('supporting') or []) or '—'}</p>
<p><b>Tied to:</b> {', '.join(h.get('ties_to') or []) or '—'}</p>
<p><b>Entities:</b> {', '.join(h.get('entities') or []) or '—'}</p>
<p><b>Timeline years:</b> {', '.join(map(str, h.get('timeline') or [])) or '—'}</p>
<p><b>Gaps:</b> {', '.join(h.get('gaps') or []) or '—'}</p>
{"<p><b>Verdict:</b> " + str(h.get('verdict')) + "</p>" if h.get('verdict') else ""}
</div>
""",
            unsafe_allow_html=True,
        )

elif section == "Operator theories":
    st.subheader("Operator theories (from MY THEORIES notes)")
    for t in my_th:
        if not match(t, q):
            continue
        ties = t.get("ties")
        ties_s = ", ".join(ties) if isinstance(ties, list) else (ties or "—")
        st.markdown(
            f"""
<div class="block">
<h3>{t.get('id')} — {t.get('name')}</h3>
<p><span class="tag {status_tag(str(t.get('status')))}">{t.get('status')}</span>
<span class="tag">{t.get('tag')}</span></p>
<p>{t.get('summary') or '—'}</p>
<p><b>Ties:</b> {ties_s}</p>
</div>
""",
            unsafe_allow_html=True,
        )

elif section == "How theories connect":
    st.subheader("How theories connect")
    st.markdown(f'<div class="block"><p>{web.get("spine") or "—"}</p></div>', unsafe_allow_html=True)
    st.markdown("**Links between hypotheses**")
    for e in web.get("edges") or []:
        st.write(f"- **{e.get('from')}** → **{e.get('to')}**: {e.get('link')}  ({e.get('tag')})")
    nc = web.get("my_narrative_control") or {}
    if nc.get("my_narrative"):
        st.markdown("**Operator narrative note**")
        st.markdown(f'<div class="block"><p>{nc.get("my_narrative")}</p></div>', unsafe_allow_html=True)
    if nc.get("spine_sentence"):
        st.info(nc.get("spine_sentence"))
    if nc.get("rules"):
        st.markdown("**Control rules**")
        for r in nc.get("rules") or []:
            st.write(f"- {r}")

elif section == "Relationship notes":
    st.subheader("Relationship notes")
    rows = [
        {
            "From": a.get("from"),
            "To": a.get("to"),
            "Type": a.get("type"),
            "Tag": a.get("tag"),
            "Detail": a.get("detail"),
            "Via hypothesis": a.get("hypothesis"),
        }
        for a in arcs
        if match(a, q)
    ]
    st.dataframe(rows, use_container_width=True, height=520)

elif section == "Contradictions":
    st.subheader("Contradictions")
    for c in contras:
        if not match(c, q):
            continue
        st.markdown(
            f"""
<div class="block">
<h3>{c.get('id')} — {c.get('name')}</h3>
<p><span class="tag tag-no">{c.get('status')}</span></p>
<p>{c.get('notes') or '—'}</p>
</div>
""",
            unsafe_allow_html=True,
        )

elif section == "Confirmed public items":
    st.subheader("Confirmed public items")
    st.caption("Items the vault treats as public-record anchors, not hypotheses.")
    for c in confirmed:
        if not match(c, q):
            continue
        st.markdown(
            f"""
<div class="block">
<p><span class="tag tag-yes">{c.get('id')}</span> <b>{c.get('name')}</b> · {c.get('tag')}</p>
</div>
""",
            unsafe_allow_html=True,
        )

elif section == "Timeline":
    st.subheader("Timeline")
    for t in timeline:
        if not match(t, q):
            continue
        st.markdown(
            f"""
<div class="block">
<p><b>{t.get('year')}</b> — {t.get('event')}</p>
<p class="meta">{t.get('tag')} · people: {t.get('people')}</p>
</div>
""",
            unsafe_allow_html=True,
        )

elif section == "Methods and logic steps":
    st.subheader("Logic chain steps")
    for sstep in DATA.get("logic_chain_steps") or []:
        st.markdown(
            f"""
<div class="block">
<p><b>Step {sstep.get('step')} — {sstep.get('role')}</b></p>
<p>{sstep.get('who')} · {sstep.get('tag')}</p>
</div>
""",
            unsafe_allow_html=True,
        )
    st.subheader("BC-PIPE notes")
    st.dataframe(DATA.get("bc_pipe") or [], use_container_width=True)
    st.subheader("Discovery methods")
    st.dataframe(DATA.get("discovery_methods_dm") or [], use_container_width=True)

elif section == "Drive document index":
    st.subheader("Drive document index")
    st.markdown("**Blocked secret files (not ingested)**")
    for b in drive_inv.get("blocked_secrets") or []:
        st.warning(f"{b.get('name')} ({b.get('folder')}) — {b.get('status')}")
    st.markdown("**Document summaries ingested**")
    for dd in drive_inv.get("document_distills") or []:
        if not match(dd, q):
            continue
        st.markdown(
            f"""
<div class="block">
<h3>{dd.get('doc_id')} — {dd.get('source')}</h3>
<p class="meta">Folder: {dd.get('folder')} · Status: {dd.get('status')}</p>
<p>{dd.get('summary')}</p>
<p class="meta">{dd.get('tag_split')}</p>
</div>
""",
            unsafe_allow_html=True,
        )
    with st.expander("Folder title index (raw)"):
        st.json(drive_inv.get("folders") or {})

elif section == "Sources and export":
    st.subheader("Sources and export")
    dp = (status.get("dual_persist") or {})
    gh = dp.get("github") or {}
    dr = dp.get("drive") or {}
    st.markdown(
        f"""
<div class="block">
<p><b>GitHub:</b> {gh.get('url') or 'https://github.com/cantgetalonggta-png/detective-codex-vault'}</p>
<p><b>Drive folder:</b> {dr.get('url') or 'detective-codex-2026-09-11'}</p>
<p><b>Meridian map app:</b> retired. This encyclopedia is the reference surface.</p>
</div>
""",
        unsafe_allow_html=True,
    )
    st.download_button(
        "Download FULL_EXPORT.json",
        data=json.dumps(DATA, indent=2),
        file_name="FULL_EXPORT.json",
        mime="application/json",
    )
    md_path = ROOT / "exports" / "FULL_EXPORT.md"
    if md_path.exists():
        st.download_button(
            "Download FULL_EXPORT.md",
            data=md_path.read_text(),
            file_name="FULL_EXPORT.md",
            mime="text/markdown",
        )
    st.json(DATA.get("public_links") or {})

else:  # Audio panel
    st.subheader("Audio panel")
    audio_path = ROOT / "audio" / "theories-plausibility-panel-15min.mp3"
    st.markdown(
        """
<div class="block">
<p>Multi-speaker discussion of vault <b>hypotheses and operator theories only</b>, focused on whether
each claim could be plausible, what public facts support or limit it, and where evidence is missing.
This is synthetic multi-voice analysis grounded in the vault export and public reporting — not a live
recording of external people, and not a verdict.</p>
</div>
""",
        unsafe_allow_html=True,
    )
    if audio_path.exists():
        st.audio(str(audio_path))
        st.caption(f"File: {audio_path.name} · size {audio_path.stat().st_size // 1024} KB")
    else:
        st.warning("Audio file not found yet. Generate and place theories-plausibility-panel-15min.mp3 in audio/.")
    script_path = ROOT / "audio" / "theories-plausibility-panel-SCRIPT.md"
    if script_path.exists():
        with st.expander("Panel script (text)"):
            st.markdown(script_path.read_text()[:50000])

st.markdown("---")
st.caption(
    f"Investigation Encyclopedia {VERSION} · metadata index only · public ceiling · "
    "Palm Beach Pete identity claim contradicted"
)
