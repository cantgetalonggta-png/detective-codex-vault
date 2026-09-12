const SPIN=[
["2008 NPA framed as a simple jail deal","Official/public defense: the Acosta deal was better than a state walkaway; it put him in jail and on a registry.","Vault finding: the NPA is a public document (CF-NPA / RS). Co-conspirator non-prosecution language and victims kept in the dark are in the filing. Calling that a simple jail-only story erases the shield text you logged. Intel-asset motive stays MAYBE (HYP-ACOSTA-SHIELD, TH-04).","NPA existence RS · intel-motive MAYBE"],
["MCC 2019 treated as a closed suicide","Official lane: suicide. Other questions treated as crank.","Vault finding: death is a public-record event (CF-MCC / RS). Staging / cleanup-physics is a separate MAYBE class (HYP-CLEANUP-DEATHS, TH-05). Collapsing those two layers is the spin.","Death fact RS · staged cluster MAYBE"],
["A name on a log equals guilt","Flight-log or lawsuit names flattened into they ran the machine.","Vault finding: CONTRA-ASSOC — association is not conviction. You logged names and refused the leap.","CONTRA-ASSOC hygiene"],
["Palm Beach Pete is Epstein","Lookalike / name-similarity threads treat identity collapse as proven.","Vault verdict: CONTRADICTED (CONTRA-PBP, HYP-PBP-IDENTITY, CF-PBP-CONTRA). Kept only so the branch cannot pollute the spine. Never promote as RS.","CONTRA-PBP · red dead-end"],
["Wexner money control is a footnote","Financial advisor; relationship ended ~2007; later alleged misappropriation.","Vault finding: power-of-attorney era is public fact (CF-POA / RS). Designed leverage and Maxwell-crossover stay MAYBE (HYP-WEXNER-MAXWELL).","PoA RS · crossover MAYBE"],
["Eastern feeder is isolated side characters","Press treats named modeling/aviation orbits as disconnected extras.","Vault theory: recruiter-fixer-pilot-scout with Nadia as continuity engine (HYP-EF-FEEDER, TH-03) — MAYBE. Named public orbits are not a proven command hierarchy.","Named orbits public · engine MAYBE"],
["Drive wipe was user error / empty folder","Dismissal: nothing was there; user error; empty Drive.","Vault finding (operator note, not actor proof): wipe timed with unseals; printed backups retained; folder existed but listed zero files (HYP-DRIVE-WIPE, TH-07). Dual-persist is the countermeasure.","Operator security note · not named-actor proof"],
["2026 redaction spike is just privacy","Official frame: privacy, ongoing investigation, bureaucracy.","Vault finding: dump existence is public; motive for timing/volume is MAYBE (TH-09). Black bars are not automatic proof of a cover-up.","Dump RS · motive MAYBE"],
["A clever method proves the claim","DM-1..10 treated as if method validity equals claim truth.","Vault finding: CONTRA-METHOD — method validity is not claim truth.","CONTRA-METHOD"],
["Your 2020-2026 grind is forum noise","Bucketed as conspiracy content; only headlines exist.","Vault narrative: years on public unseals, flight logs, Slovak scraps, printed backups after the wipe (TH-10). The gaslight is erasing the public-record layer and talking only about yellow theories.","Operator narrative · tags mandatory"],
["GitHub/Drive empty means you invented it","If the folder looks empty, the work never happened.","Vault status_board: GitHub already had files; Drive folder was created but uploads never landed; sandbox FS had wiped local copies before.","why_dual_persist_lagged · operator note"],
["Robert Maxwell 1991 ends the inheritance question","Death date treated as closing the Maxwell-infrastructure story.","Vault finding: death date is RS (CF-RMX). Inheritance/shield hinge remains MAYBE (HYP-WEXNER-MAXWELL). Date is not a closed theory.","Death date RS · hinge MAYBE"],
["Zuzana / Brovary never mattered","If a name drops out of later dumps, the person was never in the chain.","Vault theory: Brovary ghost-quote / vanish marker is MAYBE (TH-08), tied to HYP-EF-FEEDER.","TH-08 MAYBE"],
["Pergamon ads are proven lure infrastructure","1987 classifieds and PO-box stories treated as settled fact.","Vault split: Pergamon/Maxwell public existence is RS. Ads / Rue de Rivoli / Polaroid lure chain is MAYBE (TH-02).","Org public · ads chain MAYBE"],
["Dubai logistics is a proven exit","Post-2019 freight/visa stories treated as closed.","Vault tag: theory_MAYBE at low confidence (HYP-DUBAI-PIVOT, TH-06). No RS promotion.","MAYBE · do not promote"],
["Cleanup deaths are all one proven plot","Individual public death dates collapsed into one staged conspiracy.","Vault split: individual death facts can be RS. The staged-cluster / physics class is MAYBE at low confidence (HYP-CLEANUP-DEATHS).","Dates RS · cluster MAYBE"]
];
const SRC=["https://raw.githubusercontent.com/cantgetalonggta-png/detective-codex-vault/main/data/FULL_EXPORT.json","vault.json","data/FULL_EXPORT.json","../data/FULL_EXPORT.json"];
const NAV=[],BODIES={}; let idx=0;
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]));
const join=v=>!v?"—":Array.isArray(v)?(v.length?v.join(", "):"—"):String(v);
const tc=s=>{s=(s||"").toLowerCase();return /contradict|paused|red/.test(s)?"no":/maybe|theory|open|operator|mix|ops/.test(s)?"maybe":/rs|confirm|active/.test(s)?"yes":"";};
function add(id,part,title,body){NAV.push({id,part,title});BODIES[id]=body;}
function build(d){
  if(Array.isArray(d)){d.forEach(p=>add(p.id,p.part,p.title,p.body));return;}
  const st=d.stats||{},web=d.theory_web||{};
  let nc=web.my_narrative_control||{}; if(Array.isArray(nc)) nc={rules:nc};
  const di=d.drive_inventory||{},sb=d.status_board||{},hs=sb.hypothesis_status_summary||{};
  add("cover","Front matter","Cover","<div class='cover'><div class='kicker'>Interactive investigation book</div><h1>User Vault</h1><p>"+esc(st.n_my_theories_individual)+" theories · "+esc(st.n_hypotheses)+" hypotheses · "+esc(st.n_people)+" people</p><p class='small'>"+esc(d.version)+" · "+esc(d.as_of)+"</p></div>");
  add("how","Front matter","How to read","<h2>How to read this book</h2><p class='lede'>Generated from FULL_EXPORT.json. No new claims. No login.</p><p><span class='tag yes'>RS</span> public anchors. <span class='tag maybe'>MAYBE</span> hypotheses. <span class='tag no'>Contradicted</span> frozen (PBP included).</p><p>"+esc(d.ceiling)+"</p>");
  add("spin","I · Narrative","Narrative spin vs your findings","<h2>Narrative spin vs your findings</h2><p class='lede'>Official or mainstream framing vs what you logged. Yellow stays yellow. Red stays red.</p>"+SPIN.map((r,i)=>"<div class='card spin'><h3>"+(i+1)+". "+esc(r[0])+"</h3><p><b>Mainstream / official frame</b><br>"+esc(r[1])+"</p><p><b>Your logged finding</b><br>"+esc(r[2])+"</p><p class='small'><span class='tag maybe'>"+esc(r[3])+"</span></p></div>").join(""));
  add("spine","I · Narrative","Operator spine","<h2>"+esc(web.title||"Operator spine")+"</h2><p>"+esc(web.spine)+"</p><p class='lede'>"+esc(nc.spine_sentence)+"</p><p>"+esc(nc.my_narrative)+"</p><ul>"+(nc.rules||[]).map(r=>"<li>"+esc(r)+"</li>").join("")+"</ul>");
  (d.my_theories_individual||[]).forEach(t=>add("th-"+t.id,"II · Your theories",t.id+" — "+t.name,"<h2>"+esc(t.id)+" — "+esc(t.name)+"</h2><p><span class='tag "+tc(t.status)+"'>"+esc(t.status)+"</span></p><p class='lede'>"+esc(t.summary)+"</p><p class='small'><b>Ties:</b> "+esc(join(t.ties))+"</p>"));
  (d.hypotheses||[]).forEach(h=>add("hyp-"+h.id,"III · Hypotheses",h.id+" — "+h.name,"<h2>"+esc(h.id)+" — "+esc(h.name)+"</h2><p><span class='tag "+tc(h.status)+"'>"+esc(h.status)+"</span> confidence "+esc(h.confidence)+"</p><p class='lede'>"+esc(h.theory)+"</p><p class='small'><b>Gaps:</b> "+esc(join(h.gaps))+"</p>"));
  add("issues","IV · Issues","Open issues and gaps","<h2>Open issues and gaps</h2><ul>"+((d.hypotheses||[]).flatMap(h=>(h.gaps||[]).map(g=>"<li><b>"+esc(h.id)+"</b> — "+esc(g)+"</li>")).join("")||"<li>None</li>")+"</ul>");
  add("contras","IV · Issues","Contradictions","<h2>Contradictions</h2>"+(d.contradictions||[]).map(c=>"<div class='card'><h3>"+esc(c.id)+" — "+esc(c.name)+"</h3><p><span class='tag no'>"+esc(c.status)+"</span></p><p>"+esc(c.notes||"")+"</p></div>").join(""));
  add("confirmed","IV · Issues","Confirmed public findings","<h2>Confirmed public findings</h2>"+(d.confirmed||[]).map(c=>"<p><span class='tag yes'>"+esc(c.tag)+"</span> <b>"+esc(c.id)+"</b> — "+esc(c.name)+"</p>").join(""));
  add("docs","IV · Issues","Documents","<h2>Documents</h2>"+(di.document_distills||[]).map(x=>"<div class='card'><h3>"+esc(x.doc_id)+"</h3><p>"+esc(x.summary)+"</p></div>").join(""));
  add("people","V · Entities","People","<h2>People</h2>"+(d.people||[]).map(p=>"<div class='card'><h3>"+esc(p.name)+" <span class='tag "+tc(p.tag)+"'>"+esc(p.tag)+"</span></h3><p>"+esc(join(p.roles))+"</p></div>").join(""));
  add("orgs","V · Entities","Organizations","<h2>Organizations</h2>"+(d.entities||[]).map(e=>"<div class='card'><h3>"+esc(e.name)+"</h3><p>"+esc(e.role)+"</p></div>").join(""));
  add("places","V · Entities","Places","<h2>Places</h2>"+(d.locations||[]).map(l=>"<div class='card'><h3>"+esc(l.name)+"</h3><p>"+esc(l.stage)+" · "+esc(l.date)+"</p></div>").join(""));
  add("arcs","V · Entities","Relationships","<h2>Relationships</h2>"+(d.arcs_deepest||[]).map(a=>"<div class='card'><p><b>"+esc(a.from)+"</b> → <b>"+esc(a.to)+"</b> <span class='tag "+tc(a.tag)+"'>"+esc(a.tag)+"</span></p><p>"+esc(a.detail)+"</p></div>").join(""));
  add("timeline","VI · Time","Timeline","<h2>Timeline</h2>"+(d.timeline||[]).map(t=>"<div class='card'><p><b>"+esc(t.year)+"</b> — "+esc(t.event)+" <span class='tag "+tc(t.tag)+"'>"+esc(t.tag)+"</span></p></div>").join(""));
  add("logic","VI · Time","Methods","<h2>Logic and methods</h2>"+(d.logic_chain_steps||[]).map(s=>"<p><b>Step "+esc(s.step)+" — "+esc(s.role)+"</b> · "+esc(s.who)+"</p>").join(""));
  add("links","Back matter","Connections","<h2>Connections</h2>"+(web.edges||[]).map(e=>"<p><b>"+esc(e.from)+"</b> → <b>"+esc(e.to)+"</b> · "+esc(e.link||e.tag)+"</p>").join(""));
  add("limits","Back matter","Limits and status","<h2>Limits</h2><ul>"+(d.never_list||[]).map(n=>"<li>"+esc(n)+"</li>").join("")+"</ul><p>Yellow: "+esc(join(hs.yellow_open))+"</p><p>Red: "+esc(join(hs.red_contradicted))+"</p>");
  add("colophon","Back matter","Colophon","<h2>Colophon</h2><p>No login. Source FULL_EXPORT.json.</p><p>PBP identity remains CONTRADICTED. MAYBE is not fact.</p>");
}
function renderNav(){
  const q=(document.getElementById("q").value||"").toLowerCase();
  let html="", last="";
  NAV.forEach((n,i)=>{
    const hay=(n.part+" "+n.title+" "+(BODIES[n.id]||"")).toLowerCase();
    if(q && !hay.includes(q)) return;
    if(n.part!==last){ html += "<div class='part'>"+n.part+"</div>"; last=n.part; }
    html += "<button class='"+(i===idx?"active":"")+"' onclick='jump("+i+")'>"+n.title+"</button>";
  });
  document.getElementById("nav").innerHTML = html || "<p>No matches.</p>";
}
function show(){const n=NAV[idx];document.getElementById("page").innerHTML=BODIES[n.id]||"";document.getElementById("pos").textContent=(idx+1)+" / "+NAV.length+" · "+n.part;renderNav();window.scrollTo(0,0);}
function jump(i){idx=i;show();}
function go(d){idx=Math.max(0,Math.min(NAV.length-1,idx+d));show();}
document.addEventListener("keydown",e=>{if(e.key==="ArrowRight")go(1);if(e.key==="ArrowLeft")go(-1);});
(async()=>{
  let last="";
  for(const u of SRC){
    try{const r=await fetch(u); if(!r.ok) throw new Error(r.status); build(await r.json()); show(); return;}
    catch(e){last=String(e);}
  }
  document.getElementById("page").innerHTML="<p>Could not load vault: "+esc(last)+"</p>";
})();
