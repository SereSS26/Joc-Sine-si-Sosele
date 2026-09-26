P='/home/claude/joc/src/game.html'
s=open(P).read()
def rep(a,b,count=1):
    global s
    assert a in s, 'missing: '+a[:100]
    s=s.replace(a,b,count)
def between(a,b,new):
    global s
    i=s.index(a); j=s.index(b,i)
    s=s[:i]+new+s[j:]

# ------------------------------------------------ HTML: buton Flota + panou Flota (inlocuieste panoul vechi)
rep('''        <button class="round" id="btnMenu" data-tt="menuTip">''','''        <button class="round fleetBtn" id="btnFleet" data-tt="fleetTip"><svg viewBox="0 0 24 24"><rect x="2" y="6" width="13" height="10" rx="1.5" fill="#C99B5B"/><path d="M15 9h4l3 3.5V16h-7z" fill="currentColor"/><circle cx="6.5" cy="18" r="1.8" fill="currentColor"/><circle cx="17.5" cy="18" r="1.8" fill="currentColor"/></svg><span data-t="fleet"></span></button>
        <button class="round" id="btnMenu" data-tt="menuTip">''')
between('    <div class="dpanel" id="depotPanel" hidden>','  </div>\n\n  <!-- main menu -->','''    <div class="fleet" id="fleet" hidden>
      <div class="dpHead"><b data-t="fleet"></b><button id="flClose" aria-label="close"><svg viewBox="0 0 20 20" width="16" height="16"><path d="M5 5l10 10M15 5L5 15" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg></button></div>
      <div id="flBody"></div>
    </div>
''')
rep('''/* panou depozit */''','''/* flota */
.fleetBtn{width:auto;padding:0 14px 0 10px;display:flex;gap:8px;font-weight:700;font-size:14px;}
.fleetBtn svg{width:22px;height:22px;}
.fleet{position:absolute;z-index:4;right:16px;top:calc(env(safe-area-inset-top,0px) + 70px);width:350px;max-width:calc(100% - 32px);max-height:calc(100% - 180px);overflow:auto;background:var(--panel);border-radius:18px;box-shadow:var(--shadow);padding:14px 16px 16px;box-sizing:border-box;}
.flInv{background:var(--panel2);border-radius:12px;padding:10px 12px;margin-bottom:4px;}
.flLine{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:13px;font-weight:600;margin:5px 0;}
.flLine svg,.veh svg{width:22px;height:22px;flex:none;}
.flDep{border-top:1px solid var(--line);padding:10px 4px 4px;margin-top:10px;border-radius:12px;}
.flDep.sel{background:#EEF1E8;}
.flDepHead{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:4px;}
.flDepHead b{font-size:15px;}
.badge{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:7px;background:var(--ink);color:#fff;font-family:var(--display);font-weight:900;font-size:16px;}
.veh{display:grid;grid-template-columns:22px 1fr auto;align-items:center;gap:8px;padding:6px;border-radius:10px;font-size:13px;font-weight:600;}
.veh.sel{background:#FFE9C7;}
.veh small{display:block;color:var(--muted);font-size:11px;font-weight:600;}
.dbtns{display:flex;gap:4px;flex-wrap:wrap;}
.dbtn{min-width:28px;height:28px;border:0;border-radius:8px;background:#E4E7DF;font-family:var(--display);font-weight:900;font-size:15px;cursor:pointer;padding:0 6px;}
.dbtn.on{background:var(--ink);color:#fff;cursor:default;}
.dbtn.inv{font-family:var(--ui);font-weight:700;font-size:12px;}
.dbtn:hover:not(.on){background:#D3D7CD;}
.flEmpty{font-size:12px;color:var(--muted);padding:4px 6px;}
.chips.sm{gap:4px;}
.chips.sm .chip{width:22px;height:22px;border-radius:7px;}
.chips.sm .chip:not(.off)::after{inset:6px;}
/* panou depozit */''')

# ------------------------------------------------ TEXTE
rep("""  depot:'Depozit', trainsCap:'Trenuri', trucksCap:'Camioane', serves:'Aprovizioneaza magazinele', have:'Ai acum: {n}',""",
"""  depot:'Depozit', trainsCap:'Trenuri', trucksCap:'Camioane', serves:'Culori de magazine aprovizionate', have:'Ai acum: {n}',
  fleet:'Flota', inventory:'Vehicule libere', freeTrains:'Trenuri: {n}', freeTrucks:'Camioane: {n}', putOn:'pune pe', noVeh:'Niciun vehicul. Adauga din vehiculele libere de mai sus.',
  trainN:'Tren {n}', truckN:'Camion {n}', stIdle:'asteapta in depozit', stGo:'duce marfa', stUnload:'descarca', stBack:'se intoarce la depozit',
  moveTo:'Muta la depozitul {d}', toInv:'Scoate (devine liber)', fleetTip:'Flota: trenuri si camioane pe depozite (V)',
  hFleet:'Sfat: apasa Flota (V) sau da click pe un depozit, tren sau camion ca sa alegi de ce depozit apartine.',""")
rep("""  depot:'Depot', trainsCap:'Trains', trucksCap:'Trucks', serves:'Supplies shops', have:'You have: {n}',""",
"""  depot:'Depot', trainsCap:'Trains', trucksCap:'Trucks', serves:'Shop colors supplied', have:'You have: {n}',
  fleet:'Fleet', inventory:'Free vehicles', freeTrains:'Trains: {n}', freeTrucks:'Trucks: {n}', putOn:'put on', noVeh:'No vehicles. Add some from the free vehicles above.',
  trainN:'Train {n}', truckN:'Truck {n}', stIdle:'waiting at the depot', stGo:'delivering goods', stUnload:'unloading', stBack:'returning to the depot',
  moveTo:'Move to depot {d}', toInv:'Take off (becomes free)', fleetTip:'Fleet: trains and trucks per depot (V)',
  hFleet:'Tip: press Fleet (V) or click a depot, train or truck to choose which depot it belongs to.',""")
rep("hAssign:'Ai un vehicul liber. Da click pe un depozit gri ca sa-l pui pe traseu.'","hAssign:'Ai un vehicul liber. In Flota (V) apasa litera depozitului pe care vrei sa-l pui.'")
rep("hAssign:'You have a free vehicle. Click a grey depot to put it on a route.'","hAssign:'You have a free vehicle. In the Fleet (V) press the letter of the depot you want it on.'")
rep("hDepot:'A aparut un depozit nou.'","hDepot:'A aparut depozitul {d}. In Flota (V) ii poti da trenuri si camioane.'")
rep("hDepot:'A new depot has appeared.'","hDepot:'Depot {d} has appeared. Give it trains and trucks in the Fleet (V).'")
rep("keys:'Taste: 1-7 unelte, Space pauza, F viteza, Esc meniu. Click pe depozit: trenuri si camioane.',","keys:'Taste: 1-7 unelte, V flota, Space pauza, F viteza, Esc meniu.',")
rep("keys:'Keys: 1-7 tools, Space pause, F speed, Esc menu. Click a depot: trains and trucks.',","keys:'Keys: 1-7 tools, V fleet, Space pause, F speed, Esc menu.',")
rep("how7t:'Depozite', how7:'Da click pe un depozit ca sa alegi cate trenuri si camioane are si ce culori de magazine aprovizioneaza.',",
    "how7t:'Flota si depozite', how7:'Fiecare depozit are o litera (A, B, C). In Flota (V) alegi pentru fiecare tren si camion depozitul lui si ce culori de magazine aprovizioneaza fiecare depozit. Poti da click si direct pe un depozit, tren sau camion.',")
rep("how7t:'Depots', how7:'Click a depot to choose how many trains and trucks it has and which shop colors it supplies.',",
    "how7t:'Fleet and depots', how7:'Every depot has a letter (A, B, C). In the Fleet (V) you choose the depot of every train and truck and which shop colors each depot supplies. You can also click a depot, train or truck directly.',")

# ------------------------------------------------ depozite cu litere, vehicule numerotate
rep("    const d={type:'depot',id:uid++,x,y,w:2,h:2,serve:31,cells:","    const d={type:'depot',id:uid++,label:'ABCDEFGHIJKLMNOP'[G.depots.length],x,y,w:2,h:2,serve:31,cells:")
rep("  if(G.week%4===0){ if(tryDepot(null)){ sfx('spawn'); hint('hDepot',4,null,true); } }","  if(G.week%4===0){ const nd=tryDepot(null); if(nd){ sfx('spawn'); hint('hDepot',7,{d:nd.label},true); } }")
rep("     roadVer:1,railVer:1,degVer:-1,","     trainNo:0,truckNo:0,roadVer:1,railVer:1,degVer:-1,")
between('function depotTrains(d){','const serves=(d,s)=>',r'''function depotTrains(d){let n=0;for(const t of G.trains)if(t.depot===d&&!t.gone)n++;return n;}
function depotTrucks(d){let n=0;for(const c of G.cars)if(c.kind==='truck'&&c.depot===d&&!c.dead)n++;return n;}
function addTrain(d){ if(G.res.loco<=0) return null; G.res.loco--; const t={id:uid++,kind:'train',num:++G.trainNo,depot:d,shop:null,path:null,cum:null,s:0,seg:0,phase:'idle',cargo:0,wait:0,cool:0,held:-1,retire:false,gone:false}; G.trains.push(t); return t; }
function addTruck(d){ if(G.res.truck<=0) return null; G.res.truck--; const c=newVehicle('truck'); c.depot=d; c.num=++G.truckNo; G.cars.push(c); return c; }
function vehicles(){const out=[];for(const t of G.trains)if(!t.gone)out.push(t);for(const c of G.cars)if(c.kind==='truck'&&!c.dead)out.push(c);return out;}
// scoate imediat un vehicul (devine liber); marfa din drum se anuleaza
function toInventory(v){
  if(v.kind==='truck'){ if(v.phase==='go'&&v.s) v.s.inGoods-=v.cargo; v.cargo=0; v.dead=true; G.res.truck++; }
  else { if(v.phase==='go'&&v.shop) v.shop.inGoods-=v.cargo; v.cargo=0; v.gone=true; G.trains=G.trains.filter(t=>!t.gone); G.res.loco++; }
}
// muta un vehicul pe alt depozit: daca asteapta, trece imediat; daca e pe drum, isi termina livrarea si se intoarce la noul depozit
function moveVehicle(v,d){
  if(!v||v.depot===d) return;
  v.depot=d; v.retire=false;
  if(v.kind==='truck'){
    if(v.phase==='back'){ v.t=0; if(rerouteCar(v)){ v.L=DLEN[dirIdx(v.path[0],v.path[1])]; } else truckHome(v); }
  } else if(v.phase==='back'){ if(!rerouteTrain(v)) toDepot(v); }
}
function removeTrain(d){ const v=G.trains.find(t=>t.depot===d&&!t.gone&&t.phase==='idle')||G.trains.find(t=>t.depot===d&&!t.gone); if(v) toInventory(v); }
function removeTruck(d){ const v=G.cars.find(c=>c.kind==='truck'&&c.depot===d&&!c.dead&&c.phase==='idle')||G.cars.find(c=>c.kind==='truck'&&c.depot===d&&!c.dead); if(v) toInventory(v); }
function vehPos(v){
  if(v.kind==='truck') return (v.dead||v.phase==='idle'||v.phase==='park')?null:[v.x,v.y];
  if(v.gone||!v.path||(v.phase!=='go'&&v.phase!=='back')) return null;
  const p=trainPos(v,Math.max(0,v.s-.3)); return [p[0],p[1]];
}
function vehicleAt(fx,fy){
  let best=null,bd=.34*.34;
  for(const c of G.cars){ if(c.kind!=='truck'||c.dead||c.phase==='idle'||c.phase==='park') continue; const d=(c.x-fx)**2+(c.y-fy)**2; if(d<bd){bd=d;best=c;} }
  for(const t of G.trains){ if(!t.path||(t.phase!=='go'&&t.phase!=='back')) continue;
    for(const off of TRAIN_PARTS){ const ps=t.s-off; if(ps<.35) continue; const [x,y]=trainPos(t,ps); const d=(x-fx)**2+(y-fy)**2; if(d<bd){bd=d;best=t;} } }
  return best;
}
''')

# ------------------------------------------------ desen: litera depozitului (strat static) + marcaje flota
rep('''  for(const d of G.depots) if(d.inStatic){ shadowRect(c,d,1); drawDepotBody(c,d,1); }
  for(const h of G.houses) if(h.inStatic){ houseShadow(c,h,1); drawHouse(c,h,1); }''','''  for(const d of G.depots) if(d.inStatic){ shadowRect(c,d,1); drawDepotBody(c,d,1); }
  for(const h of G.houses) if(h.inStatic){ houseShadow(c,h,1); drawHouse(c,h,1); }
  // litera fiecarui depozit
  c.setTransform(dpr,0,0,dpr,0,0);
  const r=clamp(ts*.3,8,15);
  c.font='900 '+Math.round(r*1.3)+'px "Big Shoulders Display", "Arial Narrow", sans-serif'; c.textAlign='center'; c.textBaseline='middle';
  for(const d of G.depots){ if(!d.label) continue; const [sx,sy]=t2s(d.x+.08,d.y+.08);
    c.fillStyle='#F7F8F4'; c.beginPath(); c.arc(sx,sy,r,0,6.283); c.fill(); c.lineWidth=2; c.strokeStyle=DEPOT; c.stroke();
    c.fillStyle=INK; c.fillText(d.label,sx,sy+1); }''')
rep('''  if(dpSel===d){ ctx.strokeStyle=INK;''','''  if(flOpen&&flDepot===d){ ctx.strokeStyle=INK;''')
rep('''  if(dpSel) placeDepotPanel();
}''','''  if(flOpen) drawFleetMarks();
}
function drawFleetMarks(){
  ctx.setTransform(VB,0,0,VB,VX,VY);
  if(flDepot){ ctx.strokeStyle='rgba(34,38,45,.6)'; ctx.lineWidth=.06;
    for(const v of vehicles()) if(v.depot===flDepot){ const p=vehPos(v); if(p){ ctx.beginPath(); ctx.arc(p[0],p[1],.42,0,6.283); ctx.stroke(); } } }
  if(flVeh){ const p=vehPos(flVeh); if(p){ ctx.strokeStyle='#E8604C'; ctx.lineWidth=.1; ctx.beginPath(); ctx.arc(p[0],p[1],.52+.05*Math.sin(G.time*6),0,6.283); ctx.stroke(); } }
}''')

# ------------------------------------------------ control: click pe vehicul / depozit
rep('''  const bb=bmap[t];
  if(bb&&bb.type==='depot'&&!erase){ openDepot(bb); return; }
  if(dpSel) closeDepot();''','''  const bb=bmap[t];
  if(!erase){ const hv=vehicleAt(fx_,fy_); if(hv){ openFleet({veh:hv}); return; } }
  if(bb&&bb.type==='depot'&&!erase){ openFleet({depot:bb}); return; }''')
rep('''  if(e.key==='Escape'&&dpSel){ e.preventDefault(); closeDepot(); return; }''','''  if(e.key==='Escape'&&flOpen){ e.preventDefault(); closeFleet(); return; }
  if((e.key==='v'||e.key==='V')&&canPlay()){ if(flOpen) closeFleet(); else openFleet(); return; }''')

# ------------------------------------------------ interfata: panoul Flota
between('// ---------- panou depozit','function startCity(ci){',r'''// ---------- flota
let flOpen=false, flSig='', flDepot=null, flVeh=null, flT=0;
const SVG_T='<svg viewBox="0 0 24 24"><rect x="3" y="7" width="18" height="9" rx="2.5" fill="#22262D"/><rect x="15" y="9" width="4" height="3" rx="1" fill="#F7F8F4"/><circle cx="7.5" cy="18.3" r="1.6" fill="#22262D"/><circle cx="16.5" cy="18.3" r="1.6" fill="#22262D"/></svg>';
const SVG_K='<svg viewBox="0 0 24 24"><rect x="2" y="6" width="13" height="10" rx="1.5" fill="#C99B5B"/><path d="M15 9h4l3 3.5V16h-7z" fill="#22262D"/><circle cx="6.5" cy="18" r="1.8" fill="#22262D"/><circle cx="17.5" cy="18" r="1.8" fill="#22262D"/></svg>';
function openFleet(o){
  if(!G||G.mode!=='play') return;
  flOpen=true; flVeh=(o&&o.veh)||null; flDepot=(o&&o.depot)||(flVeh&&flVeh.depot)||null;
  $('fleet').hidden=false; flSig=''; renderFleet(); sfx('place');
  const el=$('fleet').querySelector('.veh.sel')||$('fleet').querySelector('.flDep.sel'); if(el) el.scrollIntoView({block:'nearest'});
}
function closeFleet(){ flOpen=false; flDepot=null; flVeh=null; const f=$('fleet'); if(f) f.hidden=true; }
function openDepot(d){ openFleet({depot:d}); }
function closeDepot(){ closeFleet(); }
function vStatus(v){ const p=v.phase; return tr(p==='idle'?'stIdle':p==='go'?'stGo':(p==='unload'||p==='park')?'stUnload':'stBack'); }
function depotNote(d){
  const chosen=G.shops.filter(s=>serves(d,s)), notes=[];
  if(depotTrains(d)>0&&!chosen.some(s=>s.cells.some(c=>depotRail(d).dist[c]<Infinity))) notes.push(tr('dpNoRail'));
  if(depotTrucks(d)>0&&!chosen.some(s=>s.cells.some(c=>depotRoad(d).dist[c]<Infinity))) notes.push(tr('dpNoRoad'));
  return notes.join(' ');
}
function renderFleet(){
  if(!flOpen) return;
  if(flVeh&&(flVeh.dead||flVeh.gone)) flVeh=null;
  const vs=vehicles();
  const sig=[G.depots.map(d=>d.id+':'+d.serve).join(','),vs.map(v=>v.id+'@'+v.depot.id).join(','),G.res.loco,G.res.truck,G.colorsUsed,flDepot&&flDepot.id,flVeh&&flVeh.id,SAVE.settings.lang].join('|');
  if(sig!==flSig){ flSig=sig; buildFleet(vs); }
  for(const v of vs){ const el=document.getElementById('vst'+v.id); if(el) el.textContent=vStatus(v); }
  for(const d of G.depots){ const el=document.getElementById('dnote'+d.id); if(el) el.textContent=depotNote(d); }
}
function invLine(k,n){
  let h='<div class="flLine">'+(k==='loco'?SVG_T:SVG_K)+'<span style="min-width:92px">'+tr(k==='loco'?'freeTrains':'freeTrucks',{n})+'</span>';
  if(n>0){ h+='<span style="color:var(--muted)">'+tr('putOn')+'</span><span class="dbtns">'; for(const d of G.depots) h+='<button class="dbtn" data-act="add" data-k="'+k+'" data-d="'+d.id+'" title="'+tr('moveTo',{d:d.label})+'">'+d.label+'</button>'; h+='</span>'; }
  return h+'</div>';
}
function buildFleet(vs){
  let h='<div class="flInv"><div class="dpSub" style="margin-top:0">'+tr('inventory')+'</div>'+invLine('loco',G.res.loco)+invLine('truck',G.res.truck)+'</div>';
  for(const d of G.depots){
    h+='<div class="flDep'+(flDepot===d?' sel':'')+'"><div class="flDepHead"><span class="flLine" style="margin:0"><span class="badge">'+d.label+'</span><b>'+tr('depot')+' '+d.label+'</b></span><span class="chips sm">';
    for(let c=0;c<G.colorsUsed;c++) h+='<button class="chip'+(((d.serve>>c)&1)?'':' off')+'" style="background:'+COLORS[c].c+'" data-act="col" data-d="'+d.id+'" data-c="'+c+'" title="'+tr('serves')+'"></button>';
    h+='</span></div>';
    const mine=vs.filter(v=>v.depot===d);
    if(!mine.length) h+='<div class="flEmpty">'+tr('noVeh')+'</div>';
    for(const v of mine){
      const isT=v.kind!=='truck';
      h+='<div class="veh'+(flVeh===v?' sel':'')+'" data-act="sel" data-v="'+v.id+'">'+(isT?SVG_T:SVG_K)+'<span>'+tr(isT?'trainN':'truckN',{n:v.num||'?'})+'<small id="vst'+v.id+'"></small></span><span class="dbtns">';
      for(const o of G.depots) h+='<button class="dbtn'+(o===d?' on':'')+'" data-act="mv" data-v="'+v.id+'" data-d="'+o.id+'" title="'+tr('moveTo',{d:o.label})+'">'+o.label+'</button>';
      h+='<button class="dbtn inv" data-act="inv" data-v="'+v.id+'" title="'+tr('toInv')+'">&#8617;</button></span></div>';
    }
    h+='<div class="dpNote" id="dnote'+d.id+'"></div></div>';
  }
  $('flBody').innerHTML=h;
}
$('flBody').addEventListener('click',e=>{
  if(!G||G.mode!=='play') return;
  const b=e.target.closest('[data-act]'); if(!b) return;
  const act=b.dataset.act, dep=G.depots.find(o=>o.id===+b.dataset.d), v=vehicles().find(x=>x.id===+b.dataset.v);
  if(act==='mv'&&v&&dep){ if(v.depot!==dep){ moveVehicle(v,dep); sfx('place'); } flDepot=dep; flVeh=v; }
  else if(act==='inv'&&v){ toInventory(v); if(flVeh===v) flVeh=null; sfx('erase'); }
  else if(act==='add'&&dep){ const nv=b.dataset.k==='loco'?addTrain(dep):addTruck(dep); if(nv){ flDepot=dep; flVeh=nv; sfx('place'); } }
  else if(act==='col'&&dep){ const c=+b.dataset.c; dep.serve^=(1<<c); if(!(dep.serve&((1<<G.colorsUsed)-1))) dep.serve|=(1<<c); flDepot=dep; sfx('place'); }
  else if(act==='sel'&&v){ flVeh=v; flDepot=v.depot; }
  flSig=''; renderFleet(); updateHud(true);
});
$('flClose').onclick=closeFleet;
$('btnFleet').onclick=()=>{ if(!canPlay()) return; if(flOpen) closeFleet(); else openFleet(); };
$('sLoco').onclick=()=>{ if(canPlay()) openFleet(); }; $('sTruck').onclick=()=>{ if(canPlay()) openFleet(); };

''')
rep('''  if(dpSel){ dpRefreshT-=rdt; if(dpRefreshT<=0){ dpRefreshT=.25; refreshDepot(); } }''','''  if(flOpen){ flT-=rdt; if(flT<=0){ flT=.3; renderFleet(); } }''')
# dupa alegerea unui vehicul la bonus: deschide Flota
rep("""if(o.k==='loco'||o.k==='truck'){G.hints.hAssign=0;hint('hAssign',8);}};""","""if(o.k==='loco'||o.k==='truck'){G.hints.hAssign=0;hint('hAssign',8);openFleet();}};""")
# sfat despre flota
rep("""  if(!demo&&(G.res.loco>0||G.res.truck>0)&&G.time>3) hint('hAssign',8);""","""  if(!demo&&(G.res.loco>0||G.res.truck>0)&&G.time>3) hint('hAssign',8);
  if(!demo&&G.time>40&&G.time<41) hint('hFleet',9);""")
rep("window.__TJ={get G(){return G;},render,t2s,","window.__TJ={get G(){return G;},render,t2s,openFleet,closeFleet,moveVehicle,toInventory,vehicles,vehicleAt,")
open(P,'w').write(s)
print('ok v13')
