#!/usr/bin/env python3
"""Interactive book — vault theories, hypotheses, entities, findings, issues only."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA: dict[str, Any] = json.loads((ROOT / "data" / "FULL_EXPORT.json").read_text())
VERSION = "4.0.0-interactive-book"

st.set_page_config(
    page_title="Investigation Book",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── book chrome ─────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@400;600&display=swap');
.stApp { background: #e8e0d4; }
.block-container { max-width: 920px; padding-top: 1rem; }
h1,h2,h3 { font-family: 'Libre Baskerville', Georgia, serif !important; color: #1a1510 !important; }
.book-page {
  background: #faf6ef;
  border: 1px solid #c9bba8;
  box-shadow: 0 8px 28px rgba(40,30,15,.12), inset 0 0 80px rgba(180,150,100,.06);
  border-radius: 2px;
  padding: 2rem 2.4rem 2.2rem;
  margin: 0.5rem 0 1.2rem;
  color: #1f1a14;
  font-family: 'Libre Baskerville', Georgia, serif;
  line-height: 1.75;
  font-size: 1.05rem;
}
.book-page p { margin: 0.65rem 0; }
.book-page .lede { font-size: 1.12rem; color: #3a3228; }
.book-page .small { font-size: 0.92rem; color: #5a5044; font-family: 'Source Sans 3', sans-serif; }
.running-head {
  font-family: 'Source Sans 3', sans-serif;
  font-size: 0.78rem; letter-spacing: .12em; text-transform: uppercase;
  color: #7a6b58; border-bottom: 1px solid #d4c8b6; padding-bottom: .45rem; margin-bottom: 1.2rem;
}
.folio { font-family: 'Source Sans 3', sans-serif; font-size: 0.8rem; color: #8a7b68; text-align: center; margin-top: 1.4rem; }
.tag {
  display: inline-block; font-family: 'Source Sans 3', sans-serif; font-size: 0.72rem;
  padding: 2px 8px; border-radius: 2px; margin-right: 0.3rem; border: 1px solid #c9bba8;
  background: #efe8dc; color: #3a3228; letter-spacing: .03em;
}
.tag-maybe { background: #fff3cd; border-color: #e0c46a; }
.tag-yes { background: #d8f0d8; border-color: #7cbc7c; }
.tag-no { background: #f5d6d6; border-color: #d08888; }
.cover {
  text-align: center; padding: 3.5rem 2rem;
  background: linear-gradient(165deg, #2c241c 0%, #1a1510 55%, #0f0c09 100%);
  color: #f0e6d6; border-radius: 2px; margin-bottom: 1rem;
  box-shadow: 0 12px 40px rgba(0,0,0,.25);
  font-family: 'Libre Baskerville', Georgia, serif;
}
.cover h1 { color: #f5ead8 !important; font-size: 2.1rem; margin: 0.6rem 0 0.4rem; }
.cover .sub { color: #c4b49a; font-size: 1rem; margin-top: 1rem; }
.cover .rule { width: 80px; height: 1px; background: #a89070; margin: 1.2rem auto; }
.toc-item {
  font-family: 'Libre Baskerville', Georgia, serif; padding: 0.35rem 0;
  border-bottom: 1px dotted #d4c8b6; display: flex; justify-content: space-between;
}
.entry-title { font-size: 1.35rem; margin-bottom: 0.2rem; }
.section-break { text-align: center; color: #9a8b78; letter-spacing: 0.4em; margin: 1rem 0; }
div[data-testid="stMetricValue"] { color: #1a1510 !important; }
section[data-testid="stSidebar"] { background: #ddd4c6; border-right: 1px solid #c0b4a0; }
.stRadio label { font-family: 'Source Sans 3', sans-serif !important; }
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
never_list = DATA.get("never_list") or status.get("never_list") or []
nc = web.get("my_narrative_control") or {}
if isinstance(nc, list):
    nc = {"rules": nc}


def join_list(v: Any) -> str:
    if v is None:
        return "—"
    if isinstance(v, list):
        return ", ".join(str(x) for x in v) if v else "—"
    return str(v)


def tag_class(s: str) -> str:
    s = (s or "").lower()
    if "contradict" in s or "paused" in s or "red" in s:
        return "tag-no"
    if "maybe" in s or "theory" in s or "open" in s or "operator" in s or "mix" in s:
        return "tag-maybe"
    if "rs" in s or "confirm" in s:
        return "tag-yes"
    return ""


def page_shell(running: str, body_html: str, folio: str = "") -> None:
    st.markdown(
        f"""
<div class="book-page">
  <div class="running-head">{running}</div>
  {body_html}
  <div class="folio">{folio}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ── chapter model (book order) ──────────────────────────────────────────────
CHAPTERS: list[dict[str, Any]] = []

CHAPTERS.append({"id": "cover", "part": "Front matter", "title": "Cover"})
CHAPTERS.append({"id": "how", "part": "Front matter", "title": "How to read this book"})
CHAPTERS.append({"id": "toc", "part": "Front matter", "title": "Table of contents"})
CHAPTERS.append({"id": "spine", "part": "I · Narrative", "title": "The operator spine"})
CHAPTERS.append({"id": "narrative", "part": "I · Narrative", "title": "Narrative control"})

for t in my_th:
    CHAPTERS.append(
        {
            "id": f"th:{t.get('id')}",
            "part": "II · Your theories",
            "title": f"{t.get('id')} — {t.get('name')}",
            "ref": t,
            "kind": "theory",
        }
    )

for h in hyps:
    CHAPTERS.append(
        {
            "id": f"hyp:{h.get('id')}",
            "part": "III · Hypotheses",
            "title": f"{h.get('id')} — {h.get('name')}",
            "ref": h,
            "kind": "hyp",
        }
    )

CHAPTERS.append({"id": "issues", "part": "IV · Issues & findings", "title": "Open issues and gaps"})
CHAPTERS.append({"id": "contras", "part": "IV · Issues & findings", "title": "Contradictions"})
CHAPTERS.append({"id": "confirmed", "part": "IV · Issues & findings", "title": "Confirmed public findings"})
CHAPTERS.append({"id": "docs", "part": "IV · Issues & findings", "title": "Document findings"})

CHAPTERS.append({"id": "people", "part": "V · Entities", "title": "People"})
CHAPTERS.append({"id": "orgs", "part": "V · Entities", "title": "Organizations"})
CHAPTERS.append({"id": "places", "part": "V · Entities", "title": "Places"})
CHAPTERS.append({"id": "arcs", "part": "V · Entities", "title": "Relationship notes"})

CHAPTERS.append({"id": "timeline", "part": "VI · Time & method", "title": "Timeline"})
CHAPTERS.append({"id": "logic", "part": "VI · Time & method", "title": "Logic chain and methods"})
CHAPTERS.append({"id": "links", "part": "Back matter", "title": "Connections between theories"})
CHAPTERS.append({"id": "limits", "part": "Back matter", "title": "Limits and never-list"})
CHAPTERS.append({"id": "colophon", "part": "Back matter", "title": "Colophon & sources"})

if "page_idx" not in st.session_state:
    st.session_state.page_idx = 0


def goto(i: int) -> None:
    st.session_state.page_idx = max(0, min(len(CHAPTERS) - 1, i))


# ── sidebar navigation ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📖 Book navigation")
    st.caption(f"v{VERSION} · vault only · {len(CHAPTERS)} pages")
    q = st.text_input("Search book", placeholder="theory, person, place…")
    parts: dict[str, list[int]] = {}
    for i, ch in enumerate(CHAPTERS):
        parts.setdefault(ch["part"], []).append(i)

    for part, idxs in parts.items():
        with st.expander(part, expanded=(part.startswith("II") or part.startswith("III") or part == "Front matter")):
            for i in idxs:
                label = CHAPTERS[i]["title"]
                if len(label) > 42:
                    label = label[:40] + "…"
                if st.button(label, key=f"nav_{i}", use_container_width=True):
                    goto(i)
                    st.rerun()

    st.markdown("---")
    st.caption("Source: FULL_EXPORT.json · public ceiling · no secrets")
    st.caption("Palm Beach Pete identity claim: contradicted")

# search jump
if q and q.strip():
    ql = q.strip().lower()
    hits = []
    for i, ch in enumerate(CHAPTERS):
        blob = json.dumps(ch, default=str).lower()
        if ql in blob or ql in ch["title"].lower():
            hits.append(i)
    # also scan people/hyps content
    for i, ch in enumerate(CHAPTERS):
        ref = ch.get("ref")
        if ref and ql in json.dumps(ref, default=str).lower() and i not in hits:
            hits.append(i)
    if hits:
        st.sidebar.markdown(f"**{len(hits)} match(es)**")
        for i in hits[:12]:
            if st.sidebar.button(f"→ {CHAPTERS[i]['title'][:36]}", key=f"hit_{i}"):
                goto(i)
                st.rerun()

idx = st.session_state.page_idx
ch = CHAPTERS[idx]

# pager
cprev, cinfo, cnext = st.columns([1, 3, 1])
with cprev:
    if st.button("← Previous", disabled=idx <= 0, use_container_width=True):
        goto(idx - 1)
        st.rerun()
with cinfo:
    st.markdown(
        f"<div style='text-align:center;font-family:Source Sans 3,sans-serif;color:#5a5044'>"
        f"Page {idx + 1} of {len(CHAPTERS)} · <b>{ch['part']}</b></div>",
        unsafe_allow_html=True,
    )
with cnext:
    if st.button("Next →", disabled=idx >= len(CHAPTERS) - 1, use_container_width=True):
        goto(idx + 1)
        st.rerun()

# ── page renderers ──────────────────────────────────────────────────────────
cid = ch["id"]

if cid == "cover":
    st.markdown(
        f"""
<div class="cover">
  <div style="font-size:.8rem;letter-spacing:.25em;text-transform:uppercase;color:#a89070">Interactive investigation book</div>
  <div class="rule"></div>
  <h1>User Vault</h1>
  <div style="font-size:1.25rem;color:#e8dcc8">Theories · Hypotheses · Entities · Findings</div>
  <div class="rule"></div>
  <div class="sub">Built only from your export metadata<br/>
  {stats.get('n_my_theories_individual')} theories · {stats.get('n_hypotheses')} hypotheses ·
  {stats.get('n_people')} people · {stats.get('n_entities')} organizations · {stats.get('n_locations')} places</div>
  <p style="margin-top:2rem;font-size:.85rem;color:#8a7b68">Export {DATA.get('version')} · as of {DATA.get('as_of')}<br/>App {VERSION}</p>
</div>
""",
        unsafe_allow_html=True,
    )
    st.info("Use the sidebar or Next to move through the book. Search jumps to matching pages.")

elif cid == "how":
    body = f"""
<p class="entry-title">How to read this book</p>
<p class="lede">Every chapter is drawn from your vault export. Nothing here is a new claim invented by the app.</p>
<p><span class="tag tag-yes">Public record / RS</span> items the vault treats as established public anchors.</p>
<p><span class="tag tag-maybe">MAYBE / theory / open</span> operator hypotheses — not proven fact.</p>
<p><span class="tag tag-no">Contradicted / paused</span> claims the vault rejects or freezes (including Palm Beach Pete identity).</p>
<p class="section-break">· · ·</p>
<p><b>Scope (ceiling):</b> {DATA.get('ceiling')}</p>
<p><b>What this book is:</b> an interactive index of your theories, hypotheses, entities, findings, gaps, contradictions, timeline, and relationship notes.</p>
<p><b>What this book is not:</b> a game, a command console, or a verdict engine.</p>
"""
    page_shell("Front matter · Reading guide", body, f"{idx + 1}")

elif cid == "toc":
    rows = []
    for i, c in enumerate(CHAPTERS):
        if c["id"] == "toc":
            continue
        rows.append(
            f'<div class="toc-item"><span>{c["part"]} — {c["title"]}</span><span>{i + 1}</span></div>'
        )
    body = f'<p class="entry-title">Table of contents</p>' + "".join(rows)
    page_shell("Front matter · Contents", body, f"{idx + 1}")

elif cid == "spine":
    spine = web.get("spine") or "—"
    title = web.get("title") or "Operator spine"
    body = f"""
<p class="entry-title">{title}</p>
<p class="lede">This is the operator narrative chain from your theory web. It is labeled theory structure, not a finding of fact.</p>
<p>{spine}</p>
"""
    page_shell("Part I · Narrative", body, f"{idx + 1}")

elif cid == "narrative":
    rules = nc.get("rules") or []
    narrative = nc.get("my_narrative") or ""
    spine_s = nc.get("spine_sentence") or ""
    body = f"""
<p class="entry-title">Narrative control</p>
<p class="lede">{spine_s or 'Rules that keep the spine from swallowing contradicted branches.'}</p>
<p>{narrative or '—'}</p>
<p class="section-break">· · ·</p>
<p><b>Rules</b></p>
<ul>
{''.join(f'<li>{r}</li>' for r in rules) if rules else '<li>—</li>'}
</ul>
"""
    page_shell("Part I · Narrative", body, f"{idx + 1}")

elif ch.get("kind") == "theory":
    t = ch["ref"]
    body = f"""
<p class="entry-title">{t.get('id')} — {t.get('name')}</p>
<p>
<span class="tag {tag_class(str(t.get('status')))}">{t.get('status')}</span>
<span class="tag">{t.get('tag')}</span>
<span class="tag">{t.get('color')}</span>
</p>
<p class="lede">{t.get('summary') or '—'}</p>
<p class="small"><b>Ties:</b> {join_list(t.get('ties'))}</p>
"""
    page_shell("Part II · Your theories", body, f"{idx + 1} · {t.get('id')}")

elif ch.get("kind") == "hyp":
    h = ch["ref"]
    conf = h.get("confidence")
    arcs_h = h.get("arcs_deep") or []
    arcs_html = "".join(
        f"<li><b>{a.get('from')}</b> → <b>{a.get('to')}</b> [{a.get('type')}] "
        f"<i>{a.get('tag')}</i> — {a.get('detail')}</li>"
        for a in arcs_h
    )
    verdict = f"<p><b>Verdict:</b> {h.get('verdict')}</p>" if h.get("verdict") else ""
    body = f"""
<p class="entry-title">{h.get('id')} — {h.get('name')}</p>
<p>
<span class="tag {tag_class(str(h.get('status')))}">{h.get('status')}</span>
<span class="tag">confidence {conf}</span>
<span class="tag">{h.get('color')}</span>
<span class="tag">pipeline {h.get('pipeline') or '—'}</span>
</p>
<p class="lede">{h.get('theory') or '—'}</p>
<p class="small"><b>Supporting:</b> {join_list(h.get('supporting'))}</p>
<p class="small"><b>Contradicting:</b> {join_list(h.get('contradicting'))}</p>
<p class="small"><b>Entities:</b> {join_list(h.get('entities'))}</p>
<p class="small"><b>Ties to:</b> {join_list(h.get('ties_to'))}</p>
<p class="small"><b>Timeline years:</b> {join_list(h.get('timeline'))}</p>
<p class="small"><b>Gaps / open issues:</b> {join_list(h.get('gaps'))}</p>
{verdict}
<p class="section-break">· · ·</p>
<p><b>Deep arcs on this hypothesis</b></p>
<ul>{arcs_html or '<li>None listed.</li>'}</ul>
"""
    page_shell("Part III · Hypotheses", body, f"{idx + 1} · {h.get('id')}")

elif cid == "issues":
    items = []
    for h in hyps:
        for g in h.get("gaps") or []:
            items.append(f"<li><b>{h.get('id')}</b> — {g}</li>")
    body = f"""
<p class="entry-title">Open issues and gaps</p>
<p class="lede">Collected only from hypothesis gap fields in your export.</p>
<ul>{''.join(items) if items else '<li>No gaps listed.</li>'}</ul>
"""
    page_shell("Part IV · Issues & findings", body, f"{idx + 1}")

elif cid == "contras":
    blocks = []
    for c in contras:
        blocks.append(
            f"""
<p><b>{c.get('id')} — {c.get('name')}</b>
<span class="tag tag-no">{c.get('status')}</span></p>
<p>{c.get('notes') or '—'}</p>
"""
        )
    body = f'<p class="entry-title">Contradictions</p>' + (
        "".join(blocks) if blocks else "<p>None listed.</p>"
    )
    page_shell("Part IV · Issues & findings", body, f"{idx + 1}")

elif cid == "confirmed":
    blocks = []
    for c in confirmed:
        blocks.append(
            f'<p><span class="tag tag-yes">{c.get("id")}</span> <b>{c.get("name")}</b> · {c.get("tag")}</p>'
        )
    body = f"""
<p class="entry-title">Confirmed public findings</p>
<p class="lede">Items your vault treats as public-record anchors, not hypotheses.</p>
{''.join(blocks) if blocks else '<p>None listed.</p>'}
"""
    page_shell("Part IV · Issues & findings", body, f"{idx + 1}")

elif cid == "docs":
    blocks = []
    for dd in drive_inv.get("document_distills") or []:
        blocks.append(
            f"""
<p><b>{dd.get('doc_id')} — {dd.get('source')}</b></p>
<p class="small">Folder: {dd.get('folder')} · Status: {dd.get('status')}</p>
<p>{dd.get('summary') or '—'}</p>
<p class="small">{dd.get('tag_split') or ''}</p>
<hr style="border:none;border-top:1px solid #e0d6c6;margin:1rem 0"/>
"""
        )
    blocked = drive_inv.get("blocked_secrets") or []
    block_html = "".join(
        f"<li>{b.get('name')} ({b.get('folder')}) — {b.get('status')}</li>" for b in blocked
    )
    body = f"""
<p class="entry-title">Document findings</p>
<p class="lede">Distills ingested from your Drive inventory (public metadata only).</p>
{''.join(blocks) if blocks else '<p>No distills.</p>'}
<p class="section-break">· · ·</p>
<p><b>Blocked secret files (not ingested)</b></p>
<ul>{block_html or '<li>None listed.</li>'}</ul>
"""
    page_shell("Part IV · Issues & findings", body, f"{idx + 1}")

elif cid == "people":
    # filter by search if active
    rows = []
    for p in people:
        if q and q.lower() not in json.dumps(p, default=str).lower():
            continue
        rows.append(
            f"""
<p><b>{p.get('name')}</b> <span class="tag">{p.get('id')}</span>
<span class="tag {tag_class(str(p.get('tag')))}">{p.get('tag')}</span>
<span class="tag">{p.get('color')}</span></p>
<p class="small">Roles: {join_list(p.get('roles'))} · Status: {p.get('status') or '—'} ·
Window: {p.get('window') or '—'} · Places: {join_list(p.get('locations'))} ·
Pipelines: {join_list(p.get('pipelines'))}</p>
{"<p class='small'>Aliases: " + join_list(p.get('aliases')) + "</p>" if p.get('aliases') else ""}
{"<p class='small'><b>Verdict:</b> " + str(p.get('verdict')) + "</p>" if p.get('verdict') else ""}
<hr style="border:none;border-top:1px solid #e0d6c6;margin:.8rem 0"/>
"""
        )
    body = f"""
<p class="entry-title">People</p>
<p class="lede">{len(people)} person entries from the vault cast list.</p>
{''.join(rows) if rows else '<p>No people (or no search matches).</p>'}
"""
    page_shell("Part V · Entities", body, f"{idx + 1}")

elif cid == "orgs":
    rows = []
    for e in ents:
        if q and q.lower() not in json.dumps(e, default=str).lower():
            continue
        rows.append(
            f"""
<p><b>{e.get('name')}</b> <span class="tag">{e.get('id')}</span>
<span class="tag">{e.get('type')}</span>
<span class="tag {tag_class(str(e.get('tag')))}">{e.get('tag')}</span></p>
<p class="small">Role: {e.get('role') or '—'} · Pipelines: {join_list(e.get('pipelines'))}</p>
<hr style="border:none;border-top:1px solid #e0d6c6;margin:.8rem 0"/>
"""
        )
    body = f"""
<p class="entry-title">Organizations</p>
<p class="lede">{len(ents)} entity entries.</p>
{''.join(rows) if rows else '<p>None.</p>'}
"""
    page_shell("Part V · Entities", body, f"{idx + 1}")

elif cid == "places":
    rows = []
    for l in locs:
        if q and q.lower() not in json.dumps(l, default=str).lower():
            continue
        rows.append(
            f"""
<p><b>{l.get('name')}</b> <span class="tag">{l.get('id')}</span>
<span class="tag">{l.get('stage')}</span></p>
<p class="small">Date note: {l.get('date') or '—'} · Coordinates: {l.get('lat')}, {l.get('lon')} ·
Pipelines: {join_list(l.get('pipelines'))}</p>
<hr style="border:none;border-top:1px solid #e0d6c6;margin:.8rem 0"/>
"""
        )
    body = f"""
<p class="entry-title">Places</p>
<p class="lede">{len(locs)} location entries with optional map pins below.</p>
{''.join(rows) if rows else '<p>None.</p>'}
"""
    page_shell("Part V · Entities", body, f"{idx + 1}")
    try:
        import pandas as pd

        m = [
            {"lat": float(l["lat"]), "lon": float(l["lon"])}
            for l in locs
            if l.get("lat") is not None and l.get("lon") is not None
        ]
        if m:
            st.map(pd.DataFrame(m), size=40)
    except Exception:
        pass

elif cid == "arcs":
    rows = []
    for a in arcs:
        if q and q.lower() not in json.dumps(a, default=str).lower():
            continue
        rows.append(
            f"""
<p><b>{a.get('from')}</b> → <b>{a.get('to')}</b>
<span class="tag">{a.get('type')}</span>
<span class="tag {tag_class(str(a.get('tag')))}">{a.get('tag')}</span></p>
<p class="small">{a.get('detail') or '—'} · via {a.get('hypothesis') or '—'}</p>
<hr style="border:none;border-top:1px solid #e0d6c6;margin:.8rem 0"/>
"""
        )
    body = f"""
<p class="entry-title">Relationship notes</p>
<p class="lede">{len(arcs)} deep arcs from the export.</p>
{''.join(rows) if rows else '<p>None.</p>'}
"""
    page_shell("Part V · Entities", body, f"{idx + 1}")

elif cid == "timeline":
    rows = []
    for t in timeline:
        if q and q.lower() not in json.dumps(t, default=str).lower():
            continue
        rows.append(
            f"""
<p><b>{t.get('year')}</b> — {t.get('event')}</p>
<p class="small">{t.get('tag')} · people: {join_list(t.get('people'))}</p>
<hr style="border:none;border-top:1px solid #e0d6c6;margin:.8rem 0"/>
"""
        )
    body = f"""
<p class="entry-title">Timeline</p>
<p class="lede">{len(timeline)} dated entries.</p>
{''.join(rows) if rows else '<p>None.</p>'}
"""
    page_shell("Part VI · Time & method", body, f"{idx + 1}")

elif cid == "logic":
    steps = DATA.get("logic_chain_steps") or []
    dm = DATA.get("discovery_methods_dm") or []
    bc = DATA.get("bc_pipe") or []
    step_html = "".join(
        f"<p><b>Step {s.get('step')} — {s.get('role')}</b><br/>"
        f"<span class='small'>{s.get('who')} · {s.get('tag')}</span></p>"
        for s in steps
    )
    dm_html = "".join(
        f"<li><b>{x.get('id')}</b> — {x.get('name')} · {x.get('tag')}</li>" for x in dm
    )
    bc_html = "".join(f"<li><b>{x.get('id')}</b> — {x.get('note')}</li>" for x in bc)
    body = f"""
<p class="entry-title">Logic chain and methods</p>
<p class="section-break">Logic steps</p>
{step_html or '<p>—</p>'}
<p class="section-break">Discovery methods</p>
<ul>{dm_html or '<li>—</li>'}</ul>
<p class="section-break">BC-PIPE notes</p>
<ul>{bc_html or '<li>—</li>'}</ul>
"""
    page_shell("Part VI · Time & method", body, f"{idx + 1}")

elif cid == "links":
    edges = web.get("edges") or []
    e_html = "".join(
        f"<p><b>{e.get('from')}</b> → <b>{e.get('to')}</b><br/>"
        f"<span class='small'>{e.get('link')} · {e.get('tag')}</span></p>"
        for e in edges
    )
    body = f"""
<p class="entry-title">Connections between theories</p>
<p class="lede">Edges from your theory web — how hypotheses link.</p>
{e_html or '<p>No edges.</p>'}
"""
    page_shell("Back matter · Links", body, f"{idx + 1}")

elif cid == "limits":
    n_html = "".join(f"<li>{n}</li>" for n in never_list)
    body = f"""
<p class="entry-title">Limits and never-list</p>
<p class="lede">Hard limits recorded in the vault. The app does not ingest or promote these.</p>
<ul>{n_html or '<li>—</li>'}</ul>
<p class="section-break">· · ·</p>
<p class="small">{DATA.get('meridian_note') or ''}</p>
"""
    page_shell("Back matter · Limits", body, f"{idx + 1}")

else:  # colophon
    gh = ((status.get("dual_persist") or {}).get("github") or {})
    dr = ((status.get("dual_persist") or {}).get("drive") or {})
    pl = DATA.get("public_links") or {}
    body = f"""
<p class="entry-title">Colophon & sources</p>
<p>This interactive book is generated only from <code>data/FULL_EXPORT.json</code>.</p>
<p class="small">Export id: {DATA.get('id')}<br/>
Export version: {DATA.get('version')}<br/>
App version: {VERSION}<br/>
As of: {DATA.get('as_of')}</p>
<p><b>GitHub:</b> {gh.get('url') or pl.get('github_vault') or '—'}</p>
<p><b>Drive:</b> {dr.get('url') or pl.get('drive_codex') or '—'}</p>
<p><b>IA:</b> {pl.get('ia_epsteindocs') or '—'}</p>
<p class="section-break">· · ·</p>
<p class="small">Counts — people {stats.get('n_people')}, entities {stats.get('n_entities')},
locations {stats.get('n_locations')}, hypotheses {stats.get('n_hypotheses')},
theories {stats.get('n_my_theories_individual')}, arcs {stats.get('n_arcs_deep')},
timeline {stats.get('n_timeline')}.</p>
"""
    page_shell("Back matter · Colophon", body, f"{idx + 1}")

# bottom pager
st.markdown("---")
b1, b2, b3 = st.columns([1, 2, 1])
with b1:
    if st.button("← Prev", key="bprev", disabled=idx <= 0, use_container_width=True):
        goto(idx - 1)
        st.rerun()
with b2:
    # quick jump select
    labels = [f"{i+1}. {c['title'][:50]}" for i, c in enumerate(CHAPTERS)]
    pick = st.selectbox("Jump to page", labels, index=idx, label_visibility="collapsed")
    new_i = labels.index(pick)
    if new_i != idx:
        goto(new_i)
        st.rerun()
with b3:
    if st.button("Next →", key="bnext", disabled=idx >= len(CHAPTERS) - 1, use_container_width=True):
        goto(idx + 1)
        st.rerun()

st.caption(
    f"Investigation Book {VERSION} · solely from your vault · public ceiling · "
    "contradicted identity claim quarantined"
)
