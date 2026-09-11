#!/usr/bin/env python3
"""DETECTIVE CODEX v2.0 — book / old video-game detective desk + globe + constellation."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "FULL_EXPORT.json"
DATA: dict[str, Any] = json.loads(DATA_PATH.read_text())

VERSION = "2.0.0-globe-desk"
st.set_page_config(
    page_title="Detective Codex Desk",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── styles ──────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Special+Elite&family=Cinzel:wght@600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');
.stApp {
  background: #120c08;
  background-image:
    radial-gradient(ellipse at 20% 0%, #2a1a10 0%, transparent 55%),
    radial-gradient(ellipse at 80% 100%, #1a120c 0%, #0a0705 60%);
}
h1,h2,h3 { font-family: 'Cinzel', serif !important; color: #e8d5a3 !important; letter-spacing: .04em; }
.codex-title {
  font-family: 'Press Start 2P', monospace; color: #f0c14b; font-size: 1.05rem;
  line-height: 1.9; text-shadow: 0 0 12px rgba(240,193,75,.35);
}
.subtitle { font-family: 'Special Elite', cursive; color: #b8a078; font-size: 1rem; }
.chapter {
  border: 3px double #8b6914; background: linear-gradient(160deg, #24180f 0%, #1a120c 100%);
  padding: 1rem 1.25rem; border-radius: 6px; margin-bottom: .85rem; color: #e8dcc8;
  font-family: 'Special Elite', cursive; box-shadow: inset 0 0 40px rgba(0,0,0,.35);
}
.badge {
  display: inline-block; padding: 2px 8px; border: 1px solid #8b6914; border-radius: 3px;
  font-family: 'IBM Plex Mono', monospace; font-size: .72rem; margin-right: .35rem;
}
.hp-yellow { color: #fbbf24 !important; } .hp-red { color: #f87171 !important; }
.hp-green { color: #4ade80 !important; } .hp-blue { color: #60a5fa !important; }
.hp-gray { color: #9ca3af !important; }
.pixel-bar { height: 12px; background: #3f2a1a; border: 2px solid #8b6914; margin: .4rem 0 .7rem; }
.pixel-fill { height: 100%; background: linear-gradient(90deg, #b45309, #fbbf24); }
.arc {
  font-family: 'IBM Plex Mono', monospace; font-size: .82rem; color: #d6c6a0;
  border-left: 3px solid #8b6914; padding-left: .65rem; margin: .3rem 0;
}
.cmd-out {
  font-family: 'IBM Plex Mono', monospace; background: #0d0a08; border: 1px solid #8b6914;
  color: #c8b98a; padding: .9rem 1rem; white-space: pre-wrap; border-radius: 4px;
}
div[data-testid="stMetricValue"] {
  color: #f0c14b !important; font-family: 'Press Start 2P', monospace !important; font-size: .62rem !important;
}
div[data-testid="stMetricLabel"] { color: #b8a078 !important; }
section[data-testid="stSidebar"] {
  background: #160f0a; border-right: 2px solid #5c4018;
}
.stRadio label { font-family: 'Special Elite', cursive !important; color: #dcc9a0 !important; }
hr { border-color: #5c4018 !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ── data helpers ────────────────────────────────────────────────────────────
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


def hit(obj: Any, q: str) -> bool:
    if not q:
        return True
    return q.lower() in json.dumps(obj, default=str).lower()


def color_for_stage(stage: str) -> str:
    return {
        "lead": "#60a5fa",
        "field": "#fbbf24",
        "evidence": "#4ade80",
        "transit": "#a78bfa",
        "critical": "#f87171",
        "archive": "#9ca3af",
    }.get((stage or "").lower(), "#f0c14b")


def conf_bar(conf: float) -> str:
    pct = max(0, min(100, int(float(conf or 0) * 100)))
    return f'<div class="pixel-bar"><div class="pixel-fill" style="width:{pct}%"></div></div>'


# ── globe / map ─────────────────────────────────────────────────────────────
def build_globe_figure() -> go.Figure:
    """Interactive world map with location pins + pipeline arcs."""
    lat, lon, text, colors, sizes = [], [], [], [], []
    for l in locs:
        if l.get("lat") is None or l.get("lon") is None:
            continue
        lat.append(float(l["lat"]))
        lon.append(float(l["lon"]))
        pipes = ", ".join(l.get("pipelines") or [])
        text.append(
            f"<b>{l.get('name')}</b><br>id={l.get('id')}<br>stage={l.get('stage')}"
            f"<br>date={l.get('date')}<br>pipelines={pipes}"
        )
        colors.append(color_for_stage(str(l.get("stage") or "")))
        sizes.append(14 if l.get("stage") in ("evidence", "critical", "field") else 10)

    fig = go.Figure()
    fig.add_trace(
        go.Scattergeo(
            lon=lon,
            lat=lat,
            text=text,
            hoverinfo="text",
            mode="markers",
            marker=dict(size=sizes, color=colors, line=dict(width=1, color="#1a120b"), opacity=0.95),
            name="Locations",
        )
    )

    # draw simple arcs between sequential timeline-ish locations sharing pipelines
    by_pipe: dict[str, list] = {}
    for l in locs:
        if l.get("lat") is None:
            continue
        for p in l.get("pipelines") or ["_"]:
            by_pipe.setdefault(p, []).append(l)

    drawn = 0
    for pipe, nodes in by_pipe.items():
        if len(nodes) < 2 or pipe == "_":
            continue
        nodes = sorted(nodes, key=lambda x: str(x.get("date") or ""))
        for i in range(len(nodes) - 1):
            a, b = nodes[i], nodes[i + 1]
            fig.add_trace(
                go.Scattergeo(
                    lon=[float(a["lon"]), float(b["lon"])],
                    lat=[float(a["lat"]), float(b["lat"])],
                    mode="lines",
                    line=dict(width=1.2, color="rgba(240,193,75,0.45)"),
                    hoverinfo="text",
                    text=f"{pipe}: {a.get('name')} → {b.get('name')}",
                    showlegend=False,
                )
            )
            drawn += 1
            if drawn > 40:
                break
        if drawn > 40:
            break

    fig.update_geos(
        projection_type="orthographic",
        showland=True,
        landcolor="#1f1610",
        showocean=True,
        oceancolor="#0b1520",
        showcountries=True,
        countrycolor="#3a2a18",
        showlakes=True,
        lakecolor="#0b1520",
        bgcolor="#0a0705",
        coastlinecolor="#8b6914",
        lonaxis_showgrid=True,
        lataxis_showgrid=True,
        lonaxis_gridcolor="rgba(139,105,20,0.25)",
        lataxis_gridcolor="rgba(139,105,20,0.25)",
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor="#0a0705",
        plot_bgcolor="#0a0705",
        height=560,
        title=dict(text="GLOBE LAYER — vault locations + pipeline arcs", font=dict(color="#e8d5a3", size=14)),
        legend=dict(font=dict(color="#c8b98a")),
    )
    return fig


def build_constellation_figure() -> go.Figure:
    """Hypothesis + theory web constellation (network graph)."""
    G = nx.Graph()
    for h in hyps:
        G.add_node(h["id"], kind="hyp", color=h.get("color", "yellow"), label=h.get("name", h["id"]))
    for t in my_th:
        G.add_node(t["id"], kind="theory", color="yellow", label=t.get("name", t["id"]))
    for c in contras:
        G.add_node(c["id"], kind="contra", color="red", label=c.get("name", c["id"]))
    for c in confirmed[:8]:
        G.add_node(c["id"], kind="confirmed", color="green", label=c.get("name", c["id"]))

    for e in web.get("edges") or []:
        if e.get("from") in G and e.get("to") in G:
            G.add_edge(e["from"], e["to"], label=e.get("link", ""), tag=e.get("tag", ""))
    # hyp ↔ contra for PBP
    if "HYP-PBP-IDENTITY" in G and "CONTRA-PBP" in G:
        G.add_edge("HYP-PBP-IDENTITY", "CONTRA-PBP", label="contradicted", tag="RED")

    if G.number_of_nodes() == 0:
        return go.Figure()

    pos = nx.spring_layout(G, seed=42, k=1.4 / max(1, math.sqrt(G.number_of_nodes())))
    edge_x, edge_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y, mode="lines",
        line=dict(width=1.2, color="rgba(139,105,20,0.55)"),
        hoverinfo="none", showlegend=False,
    )

    node_x, node_y, node_text, node_color, node_size = [], [], [], [], []
    color_map = {"yellow": "#fbbf24", "red": "#f87171", "green": "#4ade80", "blue": "#60a5fa"}
    for n, attr in G.nodes(data=True):
        x, y = pos[n]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"<b>{n}</b><br>{attr.get('label')}<br>kind={attr.get('kind')}")
        node_color.append(color_map.get(attr.get("color", "yellow"), "#f0c14b"))
        node_size.append(22 if attr.get("kind") == "hyp" else 16)

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=[n for n in G.nodes()],
        textposition="top center",
        textfont=dict(size=9, color="#e8d5a3"),
        hovertext=node_text, hoverinfo="text",
        marker=dict(size=node_size, color=node_color, line=dict(width=1.5, color="#1a120b")),
        showlegend=False,
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title=dict(text="HYPOTHESIS CONSTELLATION — yellow theories · red contradictions · green confirmed", font=dict(color="#e8d5a3", size=14)),
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="#0a0705",
        plot_bgcolor="#120c08",
        height=520,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    )
    return fig


# ── command console ─────────────────────────────────────────────────────────
COMMAND_HELP = """Commands:
  help | status | documents | entities | people | locations
  hypotheses | expand hypotheses | yellow | red
  my theories | theory web | narrative | arcs
  contradictions | confirmed | timeline | rings
  east 66 | nadia | pbp | dubai | dalton | wexner
  drive | never | export | globe | constellation
"""


def run_command(cmd: str) -> str:
    c = (cmd or "").strip().lower()
    if not c or c in ("help", "?"):
        return COMMAND_HELP
    if c in ("status", "dual-persist", "persist"):
        dp = status.get("dual_persist") or {}
        gh = dp.get("github") or {}
        dr = dp.get("drive") or {}
        hs = status.get("hypothesis_status_summary") or {}
        return (
            f"VERSION {VERSION} · export {DATA.get('version')}\n"
            f"GitHub: {gh.get('url')} · {gh.get('this_run')}\n"
            f"Drive:  {dr.get('url')} · {dr.get('this_run')}\n"
            f"Yellow hyps: {hs.get('n_yellow')} · Red: {hs.get('n_red')}\n"
            f"Ceiling: {DATA.get('ceiling')}"
        )
    if c in ("documents", "docs", "my documents", "show my documents"):
        distills = (drive_inv.get("document_distills") or [])
        lines = [f"[{d.get('doc_id')}] {d.get('source')} · {d.get('status')}" for d in distills]
        return f"Document distills ({len(lines)}):\n" + ("\n".join(lines) or "(none)")
    if c in ("entities", "show entities"):
        return "\n".join(f"{e.get('id')} · {e.get('name')} · {e.get('type')} · {e.get('tag')}" for e in ents)
    if c in ("people", "cast", "my people"):
        return "\n".join(
            f"{p.get('id')} · {p.get('name')} · {p.get('color')} · {p.get('tag')}" for p in people
        )
    if c in ("locations", "places", "map pins"):
        return "\n".join(
            f"{l.get('id')} · {l.get('name')} · ({l.get('lat')},{l.get('lon')}) · {l.get('stage')}"
            for l in locs
        )
    if c in ("hypotheses", "expand hypotheses", "hyps", "show clusters"):
        lines = []
        for h in hyps:
            lines.append(
                f"{h.get('id')} [{h.get('color')}/{h.get('status')}] conf={h.get('confidence')} — {h.get('name')}"
            )
        return "Hypotheses:\n" + "\n".join(lines)
    if c == "yellow":
        return "\n".join(
            f"{h['id']} · {h['name']} · {h.get('status')}" for h in hyps if h.get("color") == "yellow"
        )
    if c == "red":
        return "\n".join(
            f"{h['id']} · {h['name']} · {h.get('status')} · {h.get('verdict','')}"
            for h in hyps if h.get("color") == "red"
        ) or "No red hyps."
    if c in ("my theories", "theories"):
        return "\n".join(f"{t.get('id')} · {t.get('name')} · {t.get('status')}" for t in my_th)
    if c in ("theory web", "web", "spine"):
        return (web.get("spine") or "") + "\n\n" + "\n".join(
            f"{e.get('from')} → {e.get('to')}: {e.get('link')} [{e.get('tag')}]"
            for e in (web.get("edges") or [])
        )
    if c in ("narrative", "my narrative"):
        nc = web.get("my_narrative_control") or {}
        return f"{nc.get('spine_sentence','')}\n\n{nc.get('my_narrative','')}"
    if c in ("arcs", "deep arcs"):
        return "\n".join(
            f"{a.get('from')} → {a.get('to')} [{a.get('type')}] {a.get('tag')} — {a.get('detail')}"
            for a in arcs[:40]
        )
    if c in ("contradictions", "contra"):
        return "\n".join(
            f"{c_.get('id')} · {c_.get('name')} · {c_.get('status')} — {c_.get('notes')}" for c_ in contras
        )
    if c in ("confirmed", "green"):
        return "\n".join(f"{c_.get('id')} · {c_.get('name')} · {c_.get('tag')}" for c_ in confirmed)
    if c in ("timeline", "rings", "timeline rings"):
        return "\n".join(f"{t.get('year')} — {t.get('event')} [{t.get('tag')}]" for t in timeline)
    if "east 66" in c or c in ("e66", "301 e66"):
        hits = [h for h in hyps if "E66" in h.get("id", "")]
        loc_hits = [l for l in locs if "66" in str(l.get("name", "")) or "E66" in l.get("id", "")]
        return (
            "HYP-E66-VERTICAL:\n"
            + "\n".join(f"  {h.get('name')} · {h.get('status')} · {h.get('theory','')[:240]}" for h in hits)
            + "\n\nLocations:\n"
            + "\n".join(f"  {l.get('id')} {l.get('name')}" for l in loc_hits)
        )
    if "nadia" in c:
        p_hits = [p for p in people if "nadia" in json.dumps(p).lower()]
        h_hits = [h for h in hyps if "nadia" in json.dumps(h).lower() or "EF-FEEDER" in h.get("id", "")]
        return (
            "Nadia / Eastern feeder:\n"
            + "\n".join(f"PERSON {p.get('id')} {p.get('name')} · {p.get('tag')}" for p in p_hits)
            + "\n"
            + "\n".join(f"HYP {h.get('id')} {h.get('name')} · {h.get('status')}" for h in h_hits)
        )
    if c in ("pbp", "palm beach pete", "simel"):
        h = next((x for x in hyps if x.get("id") == "HYP-PBP-IDENTITY"), None)
        c_ = next((x for x in contras if x.get("id") == "CONTRA-PBP"), None)
        return (
            "PBP IDENTITY — RED / CONTRADICTED (hygiene only; never promote as RS)\n"
            + (f"Hyp: {h.get('name')} · {h.get('status')} · {h.get('verdict')}\nTheory: {h.get('theory')}\n" if h else "")
            + (f"Contra: {c_.get('notes')}" if c_ else "")
        )
    if "dubai" in c:
        h = next((x for x in hyps if "DUBAI" in x.get("id", "")), None)
        return f"{h.get('id')} · {h.get('name')} · {h.get('status')}\n{h.get('theory')}" if h else "No Dubai hyp."
    if "dalton" in c:
        h = next((x for x in hyps if "DALTON" in x.get("id", "")), None)
        return f"{h.get('id')} · {h.get('name')} · {h.get('status')}\n{h.get('theory')}" if h else "No Dalton hyp."
    if "wexner" in c or "maxwell" in c:
        h = next((x for x in hyps if "WEXNER" in x.get("id", "")), None)
        return f"{h.get('id')} · {h.get('name')} · {h.get('status')}\n{h.get('theory')}" if h else "No Wexner–Maxwell hyp."
    if c in ("drive", "drive distill"):
        folders = drive_inv.get("folders") or {}
        return f"Drive folders indexed: {len(folders)}\n" + "\n".join(f"- {k}" for k in list(folders)[:20])
    if c in ("never", "ceiling"):
        return "NEVER:\n" + "\n".join(f"🚫 {n}" for n in (DATA.get("never_list") or status.get("never_list") or []))
    if c in ("export", "version"):
        return f"Export id={DATA.get('id')} version={DATA.get('version')} app={VERSION}\nPath: {DATA_PATH}"
    if c in ("globe", "constellation"):
        return "Open chapter: 🌐 Globe Layer  or  ✨ Constellation  in the menu."
    # fuzzy search
    results = []
    for collection, label in (
        (people, "PERSON"),
        (ents, "ENTITY"),
        (locs, "LOC"),
        (hyps, "HYP"),
        (my_th, "THEORY"),
        (arcs, "ARC"),
        (timeline, "TIME"),
    ):
        for obj in collection:
            if c in json.dumps(obj, default=str).lower():
                name = obj.get("name") or obj.get("id") or obj.get("event") or obj.get("from")
                results.append(f"{label} · {name}")
                if len(results) >= 25:
                    break
        if len(results) >= 25:
            break
    if results:
        return f"Search hits for '{cmd}':\n" + "\n".join(results)
    return f"Unknown command '{cmd}'. Type help."


# ── header ──────────────────────────────────────────────────────────────────
st.markdown(f'<p class="codex-title">📜 DETECTIVE CODEX DESK v{VERSION}</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">BOOK / OLD VIDEO-GAME · GLOBE · CONSTELLATION · dual-persist GitHub+Drive · '
    "public ceiling · PBP CONTRADICTED · Meridian RETIRED</p>",
    unsafe_allow_html=True,
)

m1, m2, m3, m4, m5, m6, m7 = st.columns(7)
m1.metric("PEOPLE", stats.get("n_people"))
m2.metric("ENTITIES", stats.get("n_entities"))
m3.metric("LOCS", stats.get("n_locations"))
m4.metric("HYPS", stats.get("n_hypotheses"))
m5.metric("THEORIES", stats.get("n_my_theories_individual"))
m6.metric("ARCS", stats.get("n_arcs_deep"))
m7.metric("TIMELINE", stats.get("n_timeline"))

# ── sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎮 CODEX MENU")
    page = st.radio(
        "Chapter",
        [
            "📖 Title Page",
            "⌨️ Command Console",
            "🌐 Globe Layer",
            "✨ Constellation",
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
        ],
        index=0,
    )
    st.markdown("---")
    st.error("🚫 NEVER secrets · NEVER victim photos · NEVER CSAM")
    st.warning("PBP identity = CONTRADICTED (hygiene only)")
    q = st.text_input("🔎 Search codex", "")
    st.caption(f"Data: {DATA.get('version')} · as_of {DATA.get('as_of')}")

# ── chapters ────────────────────────────────────────────────────────────────
if page.startswith("📖"):
    nc = web.get("my_narrative_control") or {}
    st.markdown(
        f"""
    <div class="chapter">
      <h2>User Vault — Epstein Investigation</h2>
      <p><span class="badge hp-green">PUBLIC CEILING</span>
         <span class="badge hp-yellow">YELLOW THEORIES</span>
         <span class="badge hp-red">PBP RED</span></p>
      <p>{DATA.get('ceiling')}</p>
      <p><b>App style:</b> {DATA.get('app_style')} + interactive globe + constellation</p>
      <p><b>As-of:</b> {DATA.get('as_of')} · export v{DATA.get('version')} · app v{VERSION}</p>
      <hr/>
      <p><b>Spine:</b> {nc.get('spine_sentence') or web.get('spine','')}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Yellow open / MAYBE")
        for hid in (status.get("hypothesis_status_summary") or {}).get("yellow_open") or []:
            st.markdown(f"- <span class='hp-yellow'>{hid}</span>", unsafe_allow_html=True)
    with c2:
        st.markdown("### Red CONTRADICTED")
        for hid in (status.get("hypothesis_status_summary") or {}).get("red_contradicted") or []:
            st.markdown(f"- <span class='hp-red'>{hid}</span>", unsafe_allow_html=True)
    st.markdown("### Why dual-persist lagged")
    for x in DATA.get("why_dual_persist_lagged") or []:
        st.write("• " + x)
    st.success("Codex v2 forces live desk + globe + constellation from FULL_EXPORT.json.")
    st.info(DATA.get("meridian_note") or "Meridian RETIRED.")

elif page.startswith("⌨️"):
    st.subheader("Investigator command console")
    st.markdown(
        '<div class="chapter">Type natural investigator commands. Engine answers from vault metadata only.</div>',
        unsafe_allow_html=True,
    )
    if "cmd_history" not in st.session_state:
        st.session_state.cmd_history = []
    presets = st.multiselect(
        "Quick commands",
        [
            "help",
            "status",
            "expand hypotheses",
            "timeline rings",
            "East 66",
            "Nadia",
            "PBP",
            "theory web",
            "narrative",
            "my theories",
            "contradictions",
            "globe",
        ],
    )
    cmd = st.text_input("Command", value=presets[-1] if presets else "", placeholder="Expand hypotheses")
    if st.button("▶ Run", type="primary") or (cmd and presets):
        out = run_command(cmd)
        st.session_state.cmd_history.append((cmd, out))
    for c, o in reversed(st.session_state.cmd_history[-8:]):
        st.markdown(f"**› {c}**")
        st.markdown(f'<div class="cmd-out">{o}</div>', unsafe_allow_html=True)

elif page.startswith("🌐"):
    st.subheader("Globe Layer — locations + pipeline arcs")
    st.markdown(
        f"""
    <div class="chapter">
      <span class="badge hp-blue">GLOBE</span>
      Orthographic world view from vault <code>locations[]</code> ({len(locs)} pins).
      Arcs follow shared pipeline IDs (E66 / DW / etc). Color = stage.
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(build_globe_figure(), use_container_width=True)
    stage_counts = pd.Series([l.get("stage") for l in locs]).value_counts().to_dict()
    st.write("Stages:", stage_counts)
    st.dataframe(
        [
            {
                "ID": l.get("id"),
                "Name": l.get("name"),
                "Lat": l.get("lat"),
                "Lon": l.get("lon"),
                "Stage": l.get("stage"),
                "Date": l.get("date"),
                "Pipelines": ",".join(l.get("pipelines") or []),
            }
            for l in locs
            if hit(l, q)
        ],
        use_container_width=True,
        height=280,
    )

elif page.startswith("✨"):
    st.subheader("Hypothesis constellation")
    st.markdown(
        """
    <div class="chapter">
      <span class="badge hp-yellow">YELLOW</span> open theories ·
      <span class="badge hp-red">RED</span> contradicted ·
      <span class="badge hp-green">GREEN</span> confirmed RS pins ·
      edges from theory_web
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(build_constellation_figure(), use_container_width=True)
    st.markdown("### Theory-web edges")
    for e in web.get("edges") or []:
        st.markdown(
            f"<div class='arc'>{e.get('from')} → {e.get('to')} — {e.get('link')} "
            f"<code>{e.get('tag')}</code></div>",
            unsafe_allow_html=True,
        )

elif page.startswith("✅"):
    st.subheader("Status board / dual-persist")
    dp = status.get("dual_persist") or {}
    gh = dp.get("github") or {}
    dr = dp.get("drive") or {}
    st.markdown(
        f"""<div class="chapter">
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
    </div>""",
        unsafe_allow_html=True,
    )
    hs = status.get("hypothesis_status_summary") or {}
    st.markdown("### Hypothesis status")
    st.write(f"Yellow open: {hs.get('n_yellow')} · Red contradicted: {hs.get('n_red')}")
    st.json(hs)
    st.markdown("### Never list")
    for n in status.get("never_list") or DATA.get("never_list") or []:
        st.write("🚫 " + n)
    if status.get("next"):
        st.info(status.get("next"))

elif page.startswith("👤"):
    st.subheader("Cast of Characters — every name & role")
    rows = []
    for p in people:
        if not hit(p, q):
            continue
        rows.append(
            {
                "ID": p.get("id"),
                "Name": p.get("name"),
                "Roles": "; ".join(p.get("roles") or []),
                "Tag": p.get("tag"),
                "Color": p.get("color"),
                "Status": p.get("status"),
                "Pipelines": ",".join(p.get("pipelines") or []),
            }
        )
    st.dataframe(rows, use_container_width=True, height=420)
    opts = [f"{p['id']} — {p['name']}" for p in people if hit(p, q)]
    if opts:
        pick = st.selectbox("Open character sheet", opts)
        p = next(x for x in people if f"{x['id']} — {x['name']}" == pick)
        verdict = (
            f"<span class='hp-red'><b>VERDICT: {p['verdict']}</b></span>" if p.get("verdict") else ""
        )
        st.markdown(
            f"""<div class="chapter"><h3>{p.get('name')}</h3>
        <p>ID: {p.get('id')}<br/>Roles: {', '.join(p.get('roles') or [])}<br/>Tag: {p.get('tag')}<br/>
        Color: {p.get('color')} · Status: {p.get('status')}<br/>
        Window: {p.get('window')}<br/>Locations: {p.get('locations')}<br/>Pipelines: {p.get('pipelines')}<br/>
        Notes: {p.get('notes','—')}<br/>
        Photo policy: {p.get('photo_policy','—')}<br/>{verdict}</p></div>""",
            unsafe_allow_html=True,
        )

elif page.startswith("🏛"):
    a, b = st.tabs(["Entities", "Locations"])
    with a:
        st.dataframe([e for e in ents if hit(e, q)], use_container_width=True, height=400)
    with b:
        st.dataframe([l for l in locs if hit(l, q)], use_container_width=True, height=300)
        m = pd.DataFrame(
            [{"lat": float(l["lat"]), "lon": float(l["lon"])} for l in locs if l.get("lat") is not None]
        )
        if not m.empty:
            st.map(m, size=40, color="#f0c14b")

elif page.startswith("🟨"):
    st.subheader("Hypotheses — yellow/red chapters + deep arcs")
    filt = st.radio("Filter", ["All", "Yellow only", "Red only"], horizontal=True)
    for h in hyps:
        if not hit(h, q):
            continue
        if filt == "Yellow only" and h.get("color") != "yellow":
            continue
        if filt == "Red only" and h.get("color") != "red":
            continue
        col = "hp-red" if h.get("color") == "red" else "hp-yellow"
        conf = float(h.get("confidence") or 0)
        arcs_html = "".join(
            [
                f"<div class='arc'>{a.get('from')} → {a.get('to')} [{a.get('type')}] "
                f"<code>{a.get('tag')}</code> — {a.get('detail')}</div>"
                for a in (h.get("arcs_deep") or [])
            ]
        )
        verdict = f"<p class='hp-red'><b>VERDICT: {h['verdict']}</b></p>" if h.get("verdict") else ""
        st.markdown(
            f"""<div class="chapter">
        <h3 class="{col}">{h.get('id')} — {h.get('name')}</h3>
        <p>Status: <b>{h.get('status')}</b> · Confidence: {conf} · Pipeline: {h.get('pipeline')}</p>
        {conf_bar(conf)}
        <p style="margin-top:.5rem">{h.get('theory')}</p>
        <p>Supporting: {', '.join(h.get('supporting') or [])}<br/>
        Ties to: {', '.join(h.get('ties_to') or [])}<br/>
        Entities: {', '.join(h.get('entities') or [])}<br/>
        Timeline: {', '.join(map(str, h.get('timeline') or []))}<br/>
        Gaps: {', '.join(h.get('gaps') or [])}</p>
        <p><b>Deep arcs</b></p>{arcs_html}{verdict}
        </div>""",
            unsafe_allow_html=True,
        )

elif page.startswith("🧠"):
    st.subheader("My theories individually (from MY THEORIES.pdf)")
    for t in my_th:
        if not hit(t, q):
            continue
        st.markdown(
            f"""<div class="chapter">
        <h3 class="hp-yellow">{t.get('id')} — {t.get('name')}</h3>
        <p>Status: <b>{t.get('status')}</b> · Tag: <code>{t.get('tag')}</code></p>
        <p>{t.get('summary')}</p>
        <p>Ties: {', '.join(t['ties']) if isinstance(t.get('ties'), list) else t.get('ties')}</p>
        </div>""",
            unsafe_allow_html=True,
        )

elif page.startswith("🕸"):
    st.subheader("Theory web — how they all tie together")
    st.markdown(f"""<div class="chapter"><p>{web.get('spine')}</p></div>""", unsafe_allow_html=True)
    for e in web.get("edges") or []:
        st.write(f"**{e.get('from')}** → **{e.get('to')}**: {e.get('link')}  `[{e.get('tag')}]`")
    st.markdown("### My narrative")
    nc = web.get("my_narrative_control") or {}
    st.markdown(f"""<div class="chapter"><p>{nc.get('my_narrative','')}</p></div>""", unsafe_allow_html=True)
    st.info(nc.get("spine_sentence", ""))
    st.markdown("### Narrative control rules")
    for r in nc.get("rules") or []:
        st.write("• " + r)

elif page.startswith("🔗"):
    st.subheader("Deep arcs — deepest relationship details")
    rows = []
    for a in arcs:
        if not hit(a, q):
            continue
        rows.append(
            {
                "From": a.get("from"),
                "To": a.get("to"),
                "Type": a.get("type"),
                "Tag": a.get("tag"),
                "Detail": a.get("detail"),
                "Via": a.get("hypothesis"),
            }
        )
    st.dataframe(rows, use_container_width=True, height=520)

elif page.startswith("🟥"):
    st.subheader("Contradictions & confirmed")
    for c in contras:
        st.markdown(
            f"""<div class="chapter"><h3 class="hp-red">{c.get('id')} — {c.get('name')}</h3>
        <p>{c.get('notes','')} · status {c.get('status')}</p></div>""",
            unsafe_allow_html=True,
        )
    st.markdown("### Confirmed (green)")
    for c in confirmed:
        st.markdown(
            f"- <span class='hp-green'>{c.get('id')}</span> {c.get('name')} · {c.get('tag')}",
            unsafe_allow_html=True,
        )

elif page.startswith("📅"):
    st.subheader("Timeline scroll")
    for t in timeline:
        if not hit(t, q):
            continue
        st.markdown(
            f"""<div class="chapter"><b>{t.get('year')}</b> — {t.get('event')}
        <br/><i>{t.get('tag')}</i> · people {t.get('people')}</div>""",
            unsafe_allow_html=True,
        )

elif page.startswith("⛓"):
    st.subheader("Operator logic chain")
    for sstep in DATA.get("logic_chain_steps") or []:
        st.markdown(
            f"""<div class="chapter"><b>Step {sstep.get('step')} — {sstep.get('role')}</b>
            <br/>{sstep.get('who')} · {sstep.get('tag')}</div>""",
            unsafe_allow_html=True,
        )
    st.markdown("### BC-PIPE")
    st.dataframe(DATA.get("bc_pipe") or [], use_container_width=True)
    st.markdown("### DM-1..10")
    st.dataframe(DATA.get("discovery_methods_dm") or [], use_container_width=True)

elif page.startswith("📁"):
    st.subheader("Drive Investigations distill")
    st.markdown("### Blocked secrets")
    for b in drive_inv.get("blocked_secrets") or []:
        st.error(f"🚫 {b.get('name')} ({b.get('folder')}) — {b.get('status')}")
    st.markdown("### Document distills (ingested)")
    for dd in drive_inv.get("document_distills") or []:
        st.markdown(
            f"""<div class="chapter"><h3>{dd.get('doc_id')} — {dd.get('source')}</h3>
        <p>Folder: {dd.get('folder')} · Status: <b>{dd.get('status')}</b></p>
        <p>{dd.get('summary')}</p>
        <p><i>{dd.get('tag_split')}</i></p></div>""",
            unsafe_allow_html=True,
        )
    st.markdown("### Full folder title index")
    st.json(drive_inv.get("folders") or {})

else:
    st.subheader("Export & dual-persist")
    st.code(
        "streamlit run /workspace/artifacts/detective-codex-vault/app.py "
        "--server.port 8080 --server.address 0.0.0.0 --server.headless true"
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
    st.markdown("### Dual-persist targets")
    st.write("- GitHub: `cantgetalonggta-png/detective-codex-vault`")
    st.write("- Drive: `detective-codex-2026-09-11` under skill-tree")
    st.caption(DATA.get("meridian_note"))
    st.json(DATA.get("public_links") or {})

st.markdown("---")
st.caption(
    f"DETECTIVE CODEX v{VERSION} · book + globe + constellation · public only · dual-persist · PBP CONTRADICTED"
)
