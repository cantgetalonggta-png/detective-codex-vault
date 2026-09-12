const SPIN=[
["2008 NPA / Acosta","Public defense: better than a state walkaway; jail plus registry.","NPA is a real public document with co-conspirator non-prosecution language and victims kept in the dark (RS). We-jailed-him erases the shield text you logged.","NPA RS / intel-motive MAYBE"],
["MCC death 2019","Official lane: suicide. Other questions treated as crank.","Death is a public-record event (RS). Staging is separately tagged MAYBE. Collapsing those layers is the spin.","Death RS / staged cluster MAYBE"],
["Names on logs = guilt","A flight-log or lawsuit name flattened into they ran the machine.","CONTRA-ASSOC: association is not conviction. You logged names and refused the leap.","Hygiene rule"],
["Palm Beach Pete identity","Lookalike threads treat identity collapse as proven.","Vault verdict: CONTRADICTED. Kept only as hygiene so it cannot pollute the spine.","CONTRA-PBP"],
["Wexner money control","Financial advisor, ended ~2007, later alleged misappropriation.","PoA era is public fact (RS). Designed leverage stays MAYBE. Spin treats PoA as a footnote.","PoA RS / crossover MAYBE"],
["Eastern feeder","Press treats modeling/aviation orbits as isolated side characters.","Your theory: recruiter-fixer-pilot-scout continuity engine (MAYBE). Gaps stay listed.","Orbits public / engine MAYBE"],
["Drive wipe Dec 2025","Dismissal: user error, empty folder.","Wipe timed with unseals; printed backups; folder existed but listed zero files. Dual-persist is countermeasure, not named-actor proof.","Operator security note"],
["Redaction spike 2026","Official frame: privacy and bureaucracy.","Dump existence is public; motive is MAYBE. Black bars are not automatic cover-up.","Dump RS / motive MAYBE"],
["Method = truth","A clever method treated as a proven claim.","CONTRA-METHOD: method validity is not claim truth.","Standing hygiene"],
["Your 2020-2026 grind","Bucketed as conspiracy content; only headlines exist.","Years on public unseals, flight logs, scraps, printed backups. The gaslight is erasing the public-record layer and talking only about yellow theories.","Operator narrative"]
];
const SRC=["vault.json","../data/FULL_EXPORT.json","https://raw.githubusercontent.com/cantgetalonggta-png/detective-codex-vault/main/data/FULL_EXPORT.json"];
const NAV=[],BODIES={}; let idx=0;
const esc=s=>String(s==null?"":s).replace(/[&<>\"]/g,c=>({"&":"&","<":"<",">":">"}[c]||c));
const join=v=>!v?"—":Array.isArray(v)?(v.length?v.join(", "):"—"):String(v);
const tc=s=>{s=(s||"").toLowerCase();return /contradict|paused|red/.test(s)?"no":/maybe|theory|open|operator|mix/.test(s)?"maybe":/rs|confirm/.test(s)?"yes":"";};
function add(id,part,title,body){NAV.push({id:id,part:part,title:title});BODIES[id]=body;}
function build(d){
  const st=d.stats||{},web=d.theory_web||{};
  let nc=web.my_narrative_control||{}; if(Array.isArray(nc)) nc={rules:nc};
  add("cover","Front matter","Cover","<div class=cover><h1>User Vault</h1><p>Theories · Hypotheses · Entities · Findings · Narrative spin</p></div>");
  add("how","Front matter","How to read","<h2>How to read</h2><p>Generated from FULL_EXPORT.json. RS = public anchors. MAYBE = hypotheses. Contradicted = frozen.</p>");
  add("spin","I · Narrative","Narrative spin vs your findings","<h2>Narrative spin vs your findings</h2>"+SPIN.map(function(r,i){return "<div class='card spin'><h3>"+(i+1)+". "+esc(r[0])+"</h3><p><b>Mainstream / official</b><br>"+esc(r[1])+"</p><p><b>Your finding</b><br>"+esc(r[2])+"</p><p class='tag maybe'>"+esc(r[3])+"</p></div>";}).join(""));
  add("spine","I · Narrative","Operator spine","<h2>Operator spine</h2><p>"+esc(web.spine)+"</p><p>"+esc(nc.spine_sentence)+"</p><p>"+esc(nc.my_narrative)+"</p>");
  (d.my_theories_individual||[]).forEach(function(t){add("th-"+t.id,"II · Theories",t.id+" — "+t.name,"<h2>"+esc(t.id)+" — "+esc(t.name)+"</h2><p class='tag "+tc(t.status)+"'>"+esc(t.status)+"</p><p>"+esc(t.summary)+"</p>");});
  (d.hypotheses||[]).forEach(function(h){add("hyp-"+h.id,"III · Hypotheses",h.id+" — "+h.name,"<h2>"+esc(h.id)+" — "+esc(h.name)+"</h2><p class='tag "+tc(h.status)+"'>"+esc(h.status)+"</p><p>"+esc(h.theory)+"</p><p>Gaps: "+esc(join(h.gaps))+"</p>");});
  add("issues","IV · Issues","Open gaps","<h2>Open gaps</h2><ul>"+(d.hypotheses||[]).flatMap(function(h){return (h.gaps||[]).map(function(g){return "<li><b>"+esc(h.id)+"</b> — "+esc(g)+"</li>";});}).join("")+"</ul>");
  add("contras","IV · Issues","Contradictions","<h2>Contradictions</h2>"+(d.contradictions||[]).map(function(c){return "<div class=card><h3>"+esc(c.id)+" — "+esc(c.name)+"</h3><span class='tag no'>"+esc(c.status)+"</span><p>"+esc(c.notes)+"</p></div>";}).join(""));
  add("confirmed","IV · Issues","Confirmed findings","<h2>Confirmed public findings</h2>"+(d.confirmed||[]).map(function(c){return "<p><span class='tag yes'>"+esc(c.id)+"</span> <b>"+esc(c.name)+"</b></p>";}).join(""));
  var di=d.drive_inventory||{};
  add("docs","IV · Issues","Documents","<h2>Documents</h2>"+(di.document_distills||[]).map(function(x){return "<div class=card><h3>"+esc(x.doc_id)+"</h3><p>"+esc(x.summary)+"</p></div>";}).join(""));
  add("people","V · Entities","People","<h2>People</h2>"+(d.people||[]).map(function(p){return "<div class=card><h3>"+esc(p.name)+" <span class='tag "+tc(p.tag)+"'>"+esc(p.tag)+"</span></h3><p>"+esc(join(p.roles))+"</p></div>";}).join(""));
  add("orgs","V · Entities","Organizations","<h2>Organizations</h2>"+(d.entities||[]).map(function(e){return "<div class=card><h3>"+esc(e.name)+"</h3><p>"+esc(e.role)+"</p></div>";}).join(""));
  add("places","V · Entities","Places","<h2>Places</h2>"+(d.locations||[]).map(function(l){return "<div class=card><h3>"+esc(l.name)+"</h3><p>"+esc(l.stage)+"</p></div>";}).join(""));
  add("arcs","V · Entities","Relationships","<h2>Relationships</h2>"+(d.arcs_deepest||[]).map(function(a){return "<div class=card><p><b>"+esc(a.from)+"</b> → <b>"+esc(a.to)+"</b> <span class='tag "+tc(a.tag)+"'>"+esc(a.tag)+"</span></p><p>"+esc(a.detail)+"</p></div>";}).join(""));
  add("timeline","VI · Time","Timeline","<h2>Timeline</h2>"+(d.timeline||[]).map(function(t){return "<div class=card><p><b>"+esc(t.year)+"</b> — "+esc(t.event)+"</p></div>";}).join(""));
  add("logic","VI · Time","Methods","<h2>Logic and methods</h2>"+(d.logic_chain_steps||[]).map(function(s){return "<p><b>Step "+esc(s.step)+" — "+esc(s.role)+"</b></p>";}).join(""));
  add("links","Back matter","Connections","<h2>Connections</h2>"+(web.edges||[]).map(function(e){return "<p><b>"+esc(e.from)+"</b> → <b>"+esc(e.to)+"</b></p>";}).join(""));
  add("limits","Back matter","Limits","<h2>Limits</h2><ul>"+(d.never_list||[]).map(function(n){return "<li>"+esc(n)+"</li>";}).join("")+"</ul>");
  add("colophon","Back matter","Colophon","<h2>Colophon</h2><p>No login. Source FULL_EXPORT.json.</p><p>https://github.com/cantgetalonggta-png/detective-codex-vault</p>");
}
function renderNav(){
  var q=(document.getElementById("q").value||"").toLowerCase();
  var html="",last="";
  NAV.forEach(function(n,i){
    var hay=(n.part+" "+n.title+" "+(BODIES[n.id]||"")).toLowerCase();
    if(q&&hay.indexOf(q)<0) return;
    if(n.part!==last){html+="<div class=part>"+n.part+"</div>";last=n.part;}
    html+="<button class='"+(i===idx?"active":"")+"' onclick='jump("+i+")'>"+n.title+"</button>";
  });
  document.getElementById("nav").innerHTML=html||"<p>No matches.</p>";
}
function show(){var n=NAV[idx];document.getElementById("page").innerHTML=BODIES[n.id]||"";document.getElementById("pos").textContent=(idx+1)+" / "+NAV.length+" · "+n.part;renderNav();window.scrollTo(0,0);}
function jump(i){idx=i;show();}
function go(d){idx=Math.max(0,Math.min(NAV.length-1,idx+d));show();}
document.addEventListener("keydown",function(e){if(e.key==="ArrowRight")go(1);if(e.key==="ArrowLeft")go(-1);});
(async function(){
  var last="";
  for(var i=0;i<SRC.length;i++){
    try{var r=await fetch(SRC[i]); if(!r.ok) throw new Error(r.status); build(await r.json()); show(); return;}
    catch(e){last=String(e);}
  }
  document.getElementById("page").innerHTML="<p>Could not load vault: "+esc(last)+"</p>";
})();
