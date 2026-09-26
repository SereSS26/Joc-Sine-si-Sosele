# --- pasaj (drum suspendat) pe distante mari: sare peste cale ferata, apa, munti, drumuri ---
# texte
rep("uOverpassD:'Drumul trece pe deasupra caii ferate',","uOverpassD:'Drum suspendat peste pana la 7 patratele',")
rep("uOverpassD:'The road goes over the railway',","uOverpassD:'Elevated road over up to 7 tiles',")
rep("how3:'Unde drumul taie calea ferata pot avea loc accidente. O bariera opreste masinile cand vine trenul. Un pasaj duce drumul pe deasupra sinelor.',",
    "how3:'Unde drumul taie calea ferata pot avea loc accidente. O bariera opreste masinile cand vine trenul. Pasajul este un drum suspendat: trage-l in linie dreapta sau pe diagonala, peste pana la 7 patratele, iar el trece pe deasupra caii ferate, a apei, a muntilor si a altor drumuri.',")
rep("how3:'Where a road crosses the railway, accidents can happen. A barrier stops cars when a train comes. An overpass takes the road over the tracks.',",
    "how3:'Where a road crosses the railway, accidents can happen. A barrier stops cars when a train comes. An overpass is an elevated road: drag it in a straight or diagonal line over up to 7 tiles and it passes over railways, water, mountains and other roads.',")
rep("  fitTip:'Arata toata harta',","""  hVia:'Pasaj: trage in linie dreapta sau pe diagonala, peste pana la {n} patratele. Trece pe deasupra caii ferate, a apei si a drumurilor. Apasat pe o trecere la nivel, o transforma in pasaj.',
  hViaLine:'Pasajul merge doar in linie dreapta sau pe diagonala.', hViaShort:'Trage pasajul peste cel putin un patratel.', hViaLong:'Pasajul poate sari peste cel mult {n} patratele.',
  hViaEnd:'Capetele pasajului trebuie sa fie pe uscat, fara cladiri si fara cale ferata.', hViaBld:'Pasajul nu poate trece peste cladiri.',
  fitTip:'Arata toata harta',""")
rep("  fitTip:'Show the whole map',","""  hVia:'Overpass: drag in a straight or diagonal line over up to {n} tiles. It passes over railways, water and roads. Tapped on a level crossing, it turns it into an overpass.',
  hViaLine:'An overpass only goes in a straight or diagonal line.', hViaShort:'Drag the overpass over at least one tile.', hViaLong:'An overpass can jump over at most {n} tiles.',
  hViaEnd:'Both ends of an overpass must be on land, without buildings or railway.', hViaBld:'An overpass cannot pass over buildings.',
  fitTip:'Show the whole map',""")

# structuri
rep("const ctrl=new Uint8Array(N), degArr=new Uint8Array(N);","const ctrl=new Uint8Array(N), degArr=new Uint8Array(N);\nconst JUMPS=new Map(), NOJ=[], VIA_MAX=7;   // pasaje: capat -> [{n,len}]")
rep("  roadN.fill(0);railN.fill(0);roadE.fill(0);railE.fill(0);fixedT.fill(0);xing.fill(0);wreck.fill(0);barAnim.fill(0);bmap.fill(null);ctrl.fill(0);",
    "  roadN.fill(0);railN.fill(0);roadE.fill(0);railE.fill(0);fixedT.fill(0);xing.fill(0);wreck.fill(0);barAnim.fill(0);bmap.fill(null);ctrl.fill(0);JUMPS.clear();")
rep("roadVer:1,railVer:1,degVer:-1,","vias:[],roadVer:1,railVer:1,degVer:-1,")

# ajutoare pentru segmente lungi
rep("function roadDeg(t){const m=roadE[t];if(!m)return 0;let n=0;for(let d=0;d<8;d++)if((m&(1<<d))&&roadN[t+DOFF[d]])n++;return n;}",
r'''function roadDeg(t){const m=roadE[t];let n=(JUMPS.get(t)||NOJ).length;if(!m)return n;for(let d=0;d<8;d++)if((m&(1<<d))&&roadN[t+DOFF[d]])n++;return n;}
function dirTo(a,b){const dx=Math.sign(b%W-a%W),dy=Math.sign(((b/W)|0)-((a/W)|0));return DLUT[(dy+1)*3+dx+1];}
function segLen(a,b){const d=dirIdx(a,b);if(d>=0)return DLEN[d];return Math.hypot(b%W-a%W,((b/W)|0)-((a/W)|0));}
function edgeOk(a,b){const d=dirIdx(a,b);if(d>=0)return (roadE[a]&(1<<d))!==0;const J=JUMPS.get(a);return !!(J&&J.some(j=>j.n===b));}
// ---------- pasaje
function viaCheck(a,b){
  const ax=a%W, ay=(a/W)|0, bx=b%W, by=(b/W)|0, dx=bx-ax, dy=by-ay;
  if(a===b) return {ok:false};
  if(!(dx===0||dy===0||Math.abs(dx)===Math.abs(dy))) return {ok:false,reason:'hViaLine'};
  const len=Math.max(Math.abs(dx),Math.abs(dy));
  if(len<2) return {ok:false,reason:'hViaShort'};
  if(len>VIA_MAX+1) return {ok:false,reason:'hViaLong'};
  for(const t of [a,b]) if(!inBt(t)||water[t]||mount[t]||bmap[t]||railN[t]) return {ok:false,reason:'hViaEnd'};
  const sx=Math.sign(dx), sy=Math.sign(dy), tiles=[];
  for(let k=1;k<len;k++){ const t=idx(ax+sx*k,ay+sy*k); if(bmap[t]) return {ok:false,reason:'hViaBld'}; tiles.push(t); }
  if(G.vias.some(v=>(v.a===a&&v.b===b)||(v.a===b&&v.b===a))) return {ok:false};
  return {ok:true,len:Math.hypot(dx,dy),tiles};
}
function jumpAdd(a,b,len){ let l=JUMPS.get(a); if(!l){l=[];JUMPS.set(a,l);} l.push({n:b,len}); }
function buildVia(a,b){
  const c=viaCheck(a,b);
  if(!c.ok){ if(c.reason) hint(c.reason,4,{n:VIA_MAX},true); return false; }
  if(G.res.overpass<=0){ flashRes('overpass'); hint('hNoOverpass',3,null,true); return false; }
  const need=(roadN[a]?0:1)+(roadN[b]?0:1);
  if(G.res.road<need){ flashRes('road'); hint('hNoRes',4,{r:tr('rnRoad')}); return false; }
  placeNode(a,'road',false); placeNode(b,'road',false);
  G.res.overpass--;
  G.vias.push({a,b,len:c.len,tiles:c.tiles}); jumpAdd(a,b,c.len); jumpAdd(b,a,c.len);
  bumpVer('road'); sfx('place'); return true;
}
function removeVia(v){
  G.vias.splice(G.vias.indexOf(v),1);
  for(const [x,y] of [[v.a,v.b],[v.b,v.a]]){ const l=JUMPS.get(x); if(l){ const i=l.findIndex(j=>j.n===y); if(i>=0) l.splice(i,1); if(!l.length) JUMPS.delete(x); } }
  G.res.overpass++; bumpVer('road');
}
function finishVia(d){
  if(d.a===d.b){ if(roadN[d.a]&&railN[d.a]) applySpecial(d.a,'overpass'); else hint('hVia',6,{n:VIA_MAX},true); } else buildVia(d.a,d.b);
  updateHud();
}''')

# stergere: capetele pasajului sau pasajul de deasupra unui patratel gol
rep("function eraseTile(t){\n  if(!inGrid(t%W,(t/W)|0)) return;","""function eraseTile(t){
  if(!inGrid(t%W,(t/W)|0)) return;
  let viaGone=false;
  for(const v of [...G.vias]) if(v.a===t||v.b===t){ removeVia(v); viaGone=true; }
  if(!roadN[t]&&!railN[t]){ const v=G.vias.find(v=>v.tiles.includes(t)); if(v){ removeVia(v); sfx('erase'); validateCtrl(); return; } }
  if(viaGone) validateCtrl();""")

# drumuri optime: pasajele sunt muchii ale grafului de drumuri
rep("""    const m=E[t]; if(!m) continue;
    for(let k=0;k<8;k++){ if(!(m&(1<<k))) continue; const n=t+DOFF[k], nd=d+DLEN[k]; if(nd<dist[n]){dist[n]=nd;prev[n]=t;hpush(n,nd);} }""",
"""    const m=E[t];
    if(m) for(let k=0;k<8;k++){ if(!(m&(1<<k))) continue; const n=t+DOFF[k], nd=d+DLEN[k]; if(nd<dist[n]){dist[n]=nd;prev[n]=t;hpush(n,nd);} }
    if(E===roadE){ const J=JUMPS.get(t); if(J) for(const j of J){ const nd=d+j.len; if(nd<dist[j.n]){dist[j.n]=nd;prev[j.n]=t;hpush(j.n,nd);} } }""")

# vehicule pe segmente lungi
rep("      c.L=DLEN[dirIdx(p[0],p[1])];\n      G.cars.push(c);","      c.L=segLen(p[0],p[1]);\n      G.cars.push(c);")
rep("c.path=p; c.i=0; c.t=0; c.phase='go'; c.L=DLEN[dirIdx(p[0],p[1])];","c.path=p; c.i=0; c.t=0; c.phase='go'; c.L=segLen(p[0],p[1]);")
rep("c.ang=dirIdx(p[0],p[1])*Math.PI/4;","c.ang=dirTo(p[0],p[1])*Math.PI/4;")
rep("    c.L=DLEN[dirIdx(c.path[0],c.path[1])];\n    return;","    c.L=segLen(c.path[0],c.path[1]);\n    return;")
rep("""    let d=dirIdx(c.path[c.i],c.path[c.i+1]);
    if(!(roadE[c.path[c.i]]&(1<<d))){ if(!rerouteCar(c)){cancelCar(c);return;} d=dirIdx(c.path[0],c.path[1]); c.t=0; }
    c.t=c.t*c.L/DLEN[d]; c.L=DLEN[d];""","""    if(!edgeOk(c.path[c.i],c.path[c.i+1])){ if(!rerouteCar(c)){cancelCar(c);return;} c.t=0; }
    const nl=segLen(c.path[c.i],c.path[c.i+1]); c.t=c.t*c.L/nl; c.L=nl;""")
rep("l.push(pocc(c,app,dirIdx(n,app)&3));","l.push(pocc(c,app,dirTo(n,app)&3));")
rep("  const ns=nodeSt(b), g=dirIdx(b,a)&3;","  const ns=nodeSt(b), g=dirTo(b,a)&3;")
rep("    for(let d=0;d<8;d++) if((m&(1<<d))&&roadN[t+DOFF[d]]) groups|=1<<(d&3);","    for(let d=0;d<8;d++) if((m&(1<<d))&&roadN[t+DOFF[d]]) groups|=1<<(d&3);\n    for(const j of (JUMPS.get(t)||NOJ)) groups|=1<<(dirTo(t,j.n)&3);")
rep("  c.x=x; c.y=y;\n","  c.x=x; c.y=y; c.air=dirIdx(a,b)<0;\n")
rep("  for(const c of G.cars){ if(c.dead||c.phase==='park'||c.phase==='idle') continue; const dx=c.x-bx","  for(const c of G.cars){ if(c.dead||c.phase==='park'||c.phase==='idle'||c.air) continue; const dx=c.x-bx")
rep("          if(c.dead||c.phase==='park'||c.phase==='idle') continue;\n          const dx=c.x-px,dy=c.y-py;","          if(c.dead||c.phase==='park'||c.phase==='idle'||c.air) continue;\n          const dx=c.x-px,dy=c.y-py;")

# desen: tablierul pasajelor (strat static)
rep("  // cladiri care nu se mai misca: depozite si case","""  // pasaje lungi
  for(const v of G.vias){
    const ax=v.a%W+.5, ay=((v.a/W)|0)+.5, bx=v.b%W+.5, by=((v.b/W)|0)+.5;
    c.fillStyle='rgba(58,64,70,.55)';
    for(const t of v.tiles){ const x=t%W+.5, y=((t/W)|0)+.5; c.beginPath(); c.arc(x+.06,y+.1,.13,0,6.283); c.fill(); }
    c.lineCap='round';
    c.strokeStyle='rgba(40,44,40,.2)'; c.lineWidth=.92; c.beginPath(); c.moveTo(ax+.1,ay+.16); c.lineTo(bx+.1,by+.16); c.stroke();
    c.strokeStyle=DECK; c.lineWidth=.84; c.beginPath(); c.moveTo(ax,ay); c.lineTo(bx,by); c.stroke();
    c.strokeStyle=ROAD; c.lineWidth=.56; c.beginPath(); c.moveTo(ax,ay); c.lineTo(bx,by); c.stroke();
  }
  // cladiri care nu se mai misca: depozite si case""")
# previzualizare in timp ce tragi pasajul
rep("function drawCursor(){\n  if(!hover||G.mode!=='play'||G.over||G.modal) return;","""function drawCursor(){
  if(drag&&drag.via&&drag.b!==drag.a&&G.mode==='play'){
    const ok=viaCheck(drag.a,drag.b).ok, ax=drag.a%W+.5, ay=((drag.a/W)|0)+.5, bx=drag.b%W+.5, by=((drag.b/W)|0)+.5;
    ctx.lineCap='round'; ctx.strokeStyle=ok?'rgba(34,38,45,.45)':'rgba(216,69,47,.55)'; ctx.lineWidth=.6;
    ctx.beginPath(); ctx.moveTo(ax,ay); ctx.lineTo(bx,by); ctx.stroke();
  }
  if(!hover||G.mode!=='play'||G.over||G.modal) return;""")
# sfat cand alegi unealta Pasaj
rep("function setTool(t){ G.tool=t;","function setTool(t){ G.tool=t; if(t==='overpass') hint('hVia',9,{n:VIA_MAX});")
# cursor: candidatii pentru pasaj sunt si trecerile la nivel (deja desenate); export pentru teste
rep("window.__TJ={get G(){return G;},","window.__TJ={get G(){return G;},buildVia,viaCheck,vehicles,pullVehicle,")
