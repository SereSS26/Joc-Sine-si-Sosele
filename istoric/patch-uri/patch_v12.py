import re
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

# =============================================================== HTML / CSS
rep('''canvas#cv{display:block;width:100%;height:100%;touch-action:none;}''','''#cvs,#cv{position:absolute;inset:0;display:block;width:100%;height:100%;}
#cv{touch-action:none;}''')
rep('''  <canvas id="cv"></canvas>
''','''  <canvas id="cvs"></canvas>
  <canvas id="cv"></canvas>
''')
rep('''.choices{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:6px 0 4px;}
#scrWeek .card{max-width:620px;}''','''.choices{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:6px 0 4px;}
#scrWeek .card{max-width:780px;}
.choice small{font-size:11px;font-weight:700;color:var(--muted);letter-spacing:.06em;text-transform:uppercase;margin-top:auto;}
.stat.click{cursor:pointer;border-radius:12px;padding:6px 8px;}
.stat.click:hover{background:var(--panel2);}
/* panou depozit */
.dpanel{position:absolute;z-index:4;width:260px;background:var(--panel);border-radius:18px;box-shadow:var(--shadow);padding:14px 16px 16px;}
.dpHead{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;}
.dpHead b{font-family:var(--display);font-size:26px;font-weight:900;text-transform:uppercase;line-height:1;}
.dpHead button{border:0;background:transparent;cursor:pointer;width:32px;height:32px;border-radius:10px;display:grid;place-items:center;}
.dpHead button:hover{background:var(--panel2);}
.dpRow{display:grid;grid-template-columns:26px 1fr auto;align-items:center;gap:8px;padding:6px 0;font-weight:600;}
.dpRow svg{width:24px;height:24px;}
.stepper{display:flex;align-items:center;gap:6px;}
.stepper button{width:32px;height:32px;border:0;border-radius:10px;background:var(--panel2);font-weight:800;font-size:18px;line-height:1;cursor:pointer;}
.stepper button:hover:not(:disabled){background:var(--ink);color:#fff;}
.stepper button:disabled{opacity:.3;cursor:default;}
.stepper b{min-width:22px;text-align:center;font-variant-numeric:tabular-nums;font-size:16px;}
.dpSub{font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:10px 0 7px;}
.chips{display:flex;gap:7px;flex-wrap:wrap;}
.chip{width:32px;height:32px;border-radius:10px;border:0;cursor:pointer;position:relative;}
.chip.off{opacity:.22;}
.chip:not(.off)::after{content:"";position:absolute;inset:9px;border-radius:50%;background:rgba(255,255,255,.9);}
.dpFree{font-size:12px;color:var(--muted);font-weight:600;margin-top:10px;}
.dpNote{font-size:12px;color:#A2432F;font-weight:700;margin-top:8px;line-height:1.35;}''')
rep('''@media (max-width:640px){''','''@media (max-width:760px){ .choices{grid-template-columns:1fr 1fr;} }
@media (max-width:640px){''')
rep('''      <div class="stat" id="sLoco">''','''      <div class="stat click" id="sLoco">''')
rep('''      <div class="stat" id="sTruck">''','''      <div class="stat click" id="sTruck">''')
rep('''    <div id="toast"></div>
  </div>''','''    <div id="toast"></div>
    <div class="dpanel" id="depotPanel" hidden>
      <div class="dpHead"><b data-t="depot"></b><button id="dpClose" aria-label="close"><svg viewBox="0 0 20 20" width="16" height="16"><path d="M5 5l10 10M15 5L5 15" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg></button></div>
      <div class="dpRow"><svg viewBox="0 0 24 24"><rect x="3" y="7" width="18" height="9" rx="2.5" fill="currentColor"/><rect x="15" y="9" width="4" height="3" rx="1" fill="#F7F8F4"/><circle cx="7.5" cy="18.3" r="1.6" fill="currentColor"/><circle cx="16.5" cy="18.3" r="1.6" fill="currentColor"/></svg><span data-t="trainsCap"></span><div class="stepper"><button id="dpTm">&minus;</button><b id="dpTn">0</b><button id="dpTp">+</button></div></div>
      <div class="dpRow"><svg viewBox="0 0 24 24"><rect x="2" y="6" width="13" height="10" rx="1.5" fill="#C99B5B"/><path d="M15 9h4l3 3.5V16h-7z" fill="currentColor"/><circle cx="6.5" cy="18" r="1.8" fill="currentColor"/><circle cx="17.5" cy="18" r="1.8" fill="currentColor"/></svg><span data-t="trucksCap"></span><div class="stepper"><button id="dpKm">&minus;</button><b id="dpKn">0</b><button id="dpKp">+</button></div></div>
      <div class="dpSub" data-t="serves"></div>
      <div class="chips" id="dpChips"></div>
      <div class="dpFree" id="dpFree"></div>
      <div class="dpNote" id="dpNote"></div>
    </div>
  </div>''')

# =============================================================== TEXTE
rep("  version:'Versiunea 1.1', accidentFx:'ACCIDENT',","""  depot:'Depozit', trainsCap:'Trenuri', trucksCap:'Camioane', serves:'Aprovizioneaza magazinele', have:'Ai acum: {n}',
  dpFree:'Libere: {t} trenuri, {k} camioane', dpNoRail:'Trenurile nu au cale ferata spre un magazin ales.', dpNoRoad:'Camioanele nu au drum spre un magazin ales.',
  hAssign:'Ai un vehicul liber. Da click pe un depozit gri ca sa-l pui pe traseu.', freeTip:'Vehicule libere. Da click pe un depozit ca sa le folosesti.',
  how7t:'Depozite', how7:'Da click pe un depozit ca sa alegi cate trenuri si camioane are si ce culori de magazine aprovizioneaza.',
  version:'Versiunea 1.2', accidentFx:'ACCIDENT',""")
rep("  version:'Version 1.1', accidentFx:'CRASH',","""  depot:'Depot', trainsCap:'Trains', trucksCap:'Trucks', serves:'Supplies shops', have:'You have: {n}',
  dpFree:'Free: {t} trains, {k} trucks', dpNoRail:'Trains have no railway to a chosen shop.', dpNoRoad:'Trucks have no road to a chosen shop.',
  hAssign:'You have a free vehicle. Click a grey depot to put it on a route.', freeTip:'Free vehicles. Click a depot to use them.',
  how7t:'Depots', how7:'Click a depot to choose how many trains and trucks it has and which shop colors it supplies.',
  version:'Version 1.2', accidentFx:'CRASH',""")
rep("weekGift:'Ai primit +15 bucati de drum. Alege inca un bonus:'","weekGift:'Ai primit +15 bucati de drum. Alege un bonus:'")
rep("weekGift:'You got +15 road pieces. Pick one more bonus:'","weekGift:'You got +15 road pieces. Pick a bonus:'")
rep("keys:'Taste: 1-7 unelte, Space pauza, F viteza, Esc meniu',","keys:'Taste: 1-7 unelte, Space pauza, F viteza, Esc meniu. Click pe depozit: trenuri si camioane.',")
rep("keys:'Keys: 1-7 tools, Space pause, F speed, Esc menu',","keys:'Keys: 1-7 tools, Space pause, F speed, Esc menu. Click a depot: trains and trucks.',")
# cum se joaca: element depozite
rep('''        <li><svg viewBox="0 0 44 44"><circle cx="22" cy="22" r="18" fill="none" stroke="#D3D7CD" stroke-width="4"/>''','''        <li><svg viewBox="0 0 44 44"><rect x="4" y="12" width="20" height="20" rx="4" fill="#4A505C"/><rect x="7.5" y="15.5" width="6" height="6" fill="#C99B5B"/><rect x="14.5" y="15.5" width="6" height="6" fill="#C99B5B"/><rect x="7.5" y="22.5" width="6" height="6" fill="#C99B5B"/><rect x="14.5" y="22.5" width="6" height="6" fill="#C99B5B"/><rect x="27" y="8" width="14" height="28" rx="4" fill="#F7F8F4" stroke="#D3D7CD" stroke-width="1.5"/><rect x="30" y="12" width="8" height="3" rx="1" fill="#22262D"/><rect x="30" y="19" width="8" height="3" rx="1" fill="#22262D"/><circle cx="31" cy="29" r="2" fill="#E8604C"/><circle cx="36" cy="29" r="2" fill="#3E7BD2"/></svg><div><b data-t="how7t"></b><span data-t="how7"></span></div></li>
        <li><svg viewBox="0 0 44 44"><circle cx="22" cy="22" r="18" fill="none" stroke="#D3D7CD" stroke-width="4"/>''')

# =============================================================== STARE: canvasuri, pool-uri
rep('''const cv=$('cv'), ctx=cv.getContext('2d');
const sc=document.createElement('canvas'), sctx=sc.getContext('2d');
let staticKey='';''','''const cv=$('cv'), ctx=cv.getContext('2d');                          // strat dinamic (vehicule, animatii)
const sc=$('cvs'), sctx=sc.getContext('2d',{alpha:false});          // strat static (drumuri, sine, case)
const tc=document.createElement('canvas'), tctx=tc.getContext('2d',{alpha:false}); // teren (rar)
let staticKey='', terrainKey='', VB=1, VX=0, VY=0;
// pool-uri ca sa nu alocam memorie la fiecare pas
const ARR_POOL=[]; let arrI=0; function parr(){let a=ARR_POOL[arrI++]; if(!a){a=[];ARR_POOL.push(a);} a.length=0; return a;}
const OCC_POOL=[]; let occI=0; function pocc(c,app,grp){let o=OCC_POOL[occI++]; if(!o){o={c:null,app:0,grp:0};OCC_POOL.push(o);} o.c=c;o.app=app;o.grp=grp;return o;}
const HC=new Int16Array(8);
function clearTree(t){ if(tree[t]){ tree[t]=0; if(G) G.terrainVer++; } }''')
rep('''     roadVer:1,railVer:1,degVer:-1,staticDirty:true,failShop:null,hints:{},''','''     roadVer:1,railVer:1,degVer:-1,terrainVer:0,xKey:-1,xList:[],iKey:-1,iList:[],wrecks:new Set(),staticDirty:true,failShop:null,hints:{},''')
rep('''  tryDepot({x:s.x+1,y:s.y+1,min:6,max:9});
  if(mode==='demo'){''','''  const d0=tryDepot({x:s.x+1,y:s.y+1,min:6,max:9});
  if(mode!=='demo'&&d0){ addTrain(d0); addTruck(d0); }
  if(mode==='demo'){''')
rep('''  fitCam(true);
  staticKey='';
}''','''  fitCam(true);
  staticKey=''; terrainKey='';
  if(typeof closeDepot==='function') closeDepot();
}''')
# tree[...] = 0  ->  clearTree(...)
s=re.sub(r'tree\[([A-Za-z_.]+)\]=0', r'clearTree(\1)', s)

# =============================================================== liste (treceri, intersectii)
rep('''function validateCtrl(){''','''function crossList(){const k=G.roadVer*1e6+G.railVer;if(G.xKey!==k){G.xList.length=0;for(let t=0;t<N;t++)if(roadN[t]&&railN[t])G.xList.push(t);G.xKey=k;}return G.xList;}
function interList(){isInter(0);if(G.iKey!==G.roadVer){G.iList.length=0;for(let t=0;t<N;t++)if(degArr[t]>=3&&roadN[t])G.iList.push(t);G.iKey=G.roadVer;}return G.iList;}
function validateCtrl(){''')

# =============================================================== vehicule pe depozite
rep('''// camioane
function findTruckJob(d){
  const rc=depotRoad(d); let best=null,bd=Infinity;
  for(const s of G.shops){ if(s.stock+s.inGoods>s.max-3) continue;''','''// vehicule atribuite depozitelor
function depotTrains(d){let n=0;for(const t of G.trains)if(t.depot===d&&!t.retire&&!t.gone)n++;return n;}
function depotTrucks(d){let n=0;for(const c of G.cars)if(c.kind==='truck'&&c.depot===d&&!c.retire&&!c.dead)n++;return n;}
function addTrain(d){ if(G.res.loco<=0) return false; G.res.loco--; G.trains.push({id:uid++,depot:d,shop:null,path:null,cum:null,s:0,seg:0,phase:'idle',cargo:0,wait:0,cool:0,held:-1,retire:false,gone:false}); return true; }
function removeTrain(d){
  const idle=G.trains.find(t=>t.depot===d&&t.phase==='idle'&&!t.retire&&!t.gone);
  if(idle){ idle.gone=true; G.trains=G.trains.filter(t=>!t.gone); G.res.loco++; return; }
  const busy=G.trains.find(t=>t.depot===d&&!t.retire&&!t.gone); if(busy) busy.retire=true;
}
function addTruck(d){ if(G.res.truck<=0) return false; G.res.truck--; const c=newVehicle('truck'); c.depot=d; G.cars.push(c); return true; }
function removeTruck(d){
  const idle=G.cars.find(c=>c.kind==='truck'&&c.depot===d&&c.phase==='idle'&&!c.retire&&!c.dead);
  if(idle){ idle.dead=true; G.res.truck++; return; }
  const busy=G.cars.find(c=>c.kind==='truck'&&c.depot===d&&!c.retire&&!c.dead); if(busy) busy.retire=true;
}
const serves=(d,s)=>((d.serve>>s.color)&1)===1;
// camioane
function findTruckJob(d){
  const rc=depotRoad(d); let best=null,bd=Infinity;
  for(const s of G.shops){ if(s.stock+s.inGoods>s.max-3||!serves(d,s)) continue;''')
rep('''function truckHome(c,cool){ if(c.phase==='go'&&c.s) c.s.inGoods-=c.cargo; c.cargo=0; c.phase='idle'; c.cool=cool||1; c.path=null; }''',
    '''function truckHome(c,cool){ if(c.phase==='go'&&c.s) c.s.inGoods-=c.cargo; c.cargo=0; c.phase='idle'; c.cool=cool||1; c.path=null; if(c.retire&&!c.dead){c.dead=true;G.res.truck++;} }''')
rep('''    } else { c.phase='idle'; c.cool=.4; c.path=null; }
    return;
  }
  if(c.phase==='go'){''','''    } else { c.phase='idle'; c.cool=.4; c.path=null; if(c.retire){c.dead=true;G.res.truck++;} }
    return;
  }
  if(c.phase==='go'){''')
rep('''function occAdd(n,c,app){let l=G.occ2.get(n);if(!l){l=[];G.occ2.set(n,l);}l.push({c,app,grp:dirIdx(n,app)&3});}''',
    '''function occAdd(n,c,app){let l=G.occ2.get(n);if(!l){l=parr();G.occ2.set(n,l);}l.push(pocc(c,app,dirIdx(n,app)&3));}''')
# trenuri: filtru culori + retragere
rep('''  for(const s of G.shops){ if(s.stock+s.inGoods>s.max-4) continue;''','''  for(const s of G.shops){ if(s.stock+s.inGoods>s.max-4||!serves(d,s)) continue;''')
rep('''function toDepot(tr){ if(tr.phase==='go'&&tr.shop) tr.shop.inGoods-=tr.cargo; tr.cargo=0; tr.phase='idle'; tr.path=null; tr.cool=1; tr.held=-1; }''',
    '''function toDepot(tr){ if(tr.phase==='go'&&tr.shop) tr.shop.inGoods-=tr.cargo; tr.cargo=0; tr.phase='idle'; tr.path=null; tr.cool=1; tr.held=-1; if(tr.retire&&!tr.gone){tr.gone=true;G.res.loco++;} }''')
rep('''  } else { tr.phase='idle'; tr.path=null; tr.cool=.4; }
}''','''  } else { tr.phase='idle'; tr.path=null; tr.cool=.4; if(tr.retire&&!tr.gone){tr.gone=true;G.res.loco++;} }
}''')
rep('''  wreck[n]=9; G.accidents++;''','''  wreck[n]=9; G.wrecks.add(n); G.accidents++;''')

# =============================================================== SIMULARE (pool-uri, liste, fara atribuire automata)
rep('''function houseCount(c){let n=0;for(const h of G.houses)if(h.color===c)n++;return n;}''','''function houseCount(c){let n=0;for(const h of G.houses)if(h.color===c)n++;return n;}
function countHouses(){HC.fill(0);for(const h of G.houses)HC[h.color]++;}''')
rep('''  const demo=G.mode==='demo';
  for(const s of G.shops){
    const hc=houseCount(s.color), L=LV[s.level];''','''  const demo=G.mode==='demo';
  countHouses();
  let anySupply=G.trains.length>0; if(!anySupply) for(const c of G.cars) if(c.kind==='truck'){anySupply=true;break;}
  for(const s of G.shops){
    const hc=HC[s.color], L=LV[s.level];''')
rep('''    if(s.stock<=3&&!G.trains.length&&!G.cars.some(c=>c.kind==='truck')) hint('hSupply',9);''','''    if(s.stock<=3&&!anySupply) hint('hSupply',9);''')
rep('''  G.segMap.clear(); G.startMap.clear(); G.occ2.clear();
  for(const c of G.cars){
    if(c.dead||c.phase==='park'||c.phase==='idle') continue;
    const a=c.path[c.i], b=c.path[c.i+1], k=a*N+b;
    let l=G.segMap.get(k); if(!l){l=[];G.segMap.set(k,l);} l.push(c);
    let m=G.startMap.get(a); if(!m){m=[];G.startMap.set(a,m);} m.push(c);''','''  G.segMap.clear(); G.startMap.clear(); G.occ2.clear(); arrI=0; occI=0;
  for(const c of G.cars){
    if(c.dead||c.phase==='park'||c.phase==='idle') continue;
    const a=c.path[c.i], b=c.path[c.i+1], k=a*N+b;
    let l=G.segMap.get(k); if(!l){l=parr();G.segMap.set(k,l);} l.push(c);
    let m=G.startMap.get(a); if(!m){m=parr();G.startMap.set(a,m);} m.push(c);''')
rep('''  if(G.trainT<=0){
    G.trainT=.5;
    for(const d of G.depots){''','''  if(G.trainT<=0&&demo){
    G.trainT=.5;
    for(const d of G.depots){''')
rep('''    if(G.res.truck>0&&G.time>25&&!G.cars.some(c=>c.kind==='truck')) hint('hTruck',8);
  }''','''  }
  if(!demo&&(G.res.loco>0||G.res.truck>0)&&G.time>3) hint('hAssign',8);''')
rep('''  for(const t of G.trains) stepTrain(t,dt);''','''  for(const t of G.trains) stepTrain(t,dt);
  if(G.trains.some(t=>t.gone)) G.trains=G.trains.filter(t=>!t.gone);''')
rep('''  for(let i=0;i<N;i++) if(wreck[i]>0){ wreck[i]-=dt; if(wreck[i]<0) wreck[i]=0; }''','''  for(const t of G.wrecks){ wreck[t]-=dt; if(wreck[t]<=0){ wreck[t]=0; G.wrecks.delete(t); } }''')

# =============================================================== SAPTAMANI: toate variantele
rep('''  let opts=pickUpgrades(3);
  if(G.week===2&&!opts.some(o=>o.k==='loco'||o.k==='truck')) opts[0]=UPG[Math.random()<.5?0:1];
  if(G.week===3&&!opts.some(o=>o.k==='lights'||o.k==='round')) opts[2]=UPG[7];
  G.lastOpts=opts;''','''  const opts=UPG;
  G.lastOpts=opts;''')
rep('''    btn.innerHTML=ICONS[o.k]+'<b>'+tr(o.t)+'</b><span>'+tr(o.d)+'</span>';
    btn.onclick=()=>{o.f();G.modal=false;show(null);updateHud(true);sfx('place');};''','''    btn.innerHTML=ICONS[o.k]+'<b>'+tr(o.t)+'</b><span>'+tr(o.d)+'</span><small>'+tr('have',{n:haveCount(o.k)})+'</small>';
    btn.onclick=()=>{o.f();G.modal=false;show(null);updateHud(true);sfx('place');if(o.k==='loco'||o.k==='truck'){G.hints.hAssign=0;hint('hAssign',8);}};''')
rep('''function gameOver(s){''','''function haveCount(k){
  if(k==='loco') return G.res.loco+G.trains.length;
  if(k==='truck'){let n=G.res.truck;for(const c of G.cars)if(c.kind==='truck')n++;return n;}
  return G.res[k];
}
function gameOver(s){''')

# =============================================================== CAMERA: redimensionare pentru 2 canvasuri
rep('''  sc.width=cv.width; sc.height=cv.height;
  if(G) fitCam(true);
  staticKey='';''','''  sc.width=cv.width; sc.height=cv.height; tc.width=cv.width; tc.height=cv.height;
  if(G) fitCam(true);
  staticKey=''; terrainKey='';''')

# =============================================================== RANDARE (rescrisa)
between('function renderStatic(){','let hover=null, hoverF=null;', r'''function renderTerrain(){
  const c=tctx, ts=cam.ts, city=G.city, b=G.bounds;
  c.setTransform(1,0,0,1,0,0); c.fillStyle=FOG; c.fillRect(0,0,tc.width,tc.height);
  c.setTransform(dpr*ts,0,0,dpr*ts,dpr*ox(),dpr*oy());
  const bw=b.x1-b.x0+1, bh=b.y1-b.y0+1;
  c.fillStyle='rgba(60,66,56,.10)'; rr(c,b.x0+.12,b.y0+.22,bw,bh,.7); c.fill();
  c.fillStyle=city.land; rr(c,b.x0,b.y0,bw,bh,.7); c.fill();
  c.save(); rr(c,b.x0,b.y0,bw,bh,.7); c.clip();
  const x0=Math.max(0,b.x0-1), x1=Math.min(W-1,b.x1+1), y0=Math.max(0,b.y0-1), y1=Math.min(H-1,b.y1+1);
  c.fillStyle=city.mount;
  for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++) if(mount[y*W+x]) c.fillRect(x-.02,y-.02,1.04,1.04);
  for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){const t=y*W+x; if(!mount[t]||hash(t)>=.55) continue;
    const px=x+.5+(hash(t+7)-.5)*.3, py=y+.55;
    c.beginPath();c.moveTo(px-.3,py+.22);c.lineTo(px,py-.26);c.lineTo(px+.3,py+.22);c.closePath();c.fillStyle='rgba(120,130,112,.28)';c.fill();
    c.beginPath();c.moveTo(px-.1,py-.08);c.lineTo(px,py-.26);c.lineTo(px+.1,py-.08);c.closePath();c.fillStyle='rgba(255,255,255,.7)';c.fill();}
  c.fillStyle=city.shore; for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++) if(water[y*W+x]) c.fillRect(x-.1,y-.1,1.2,1.2);
  c.fillStyle=city.water; for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++) if(water[y*W+x]) c.fillRect(x-.01,y-.01,1.02,1.02);
  c.strokeStyle='rgba(255,255,255,.35)'; c.lineWidth=.05; c.lineCap='round'; c.beginPath();
  for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){const t=y*W+x; if(!water[t]||hash(t*3)>=.18) continue; const px=x+.25+hash(t)*.3, py=y+.3+hash(t+1)*.4; c.moveTo(px,py); c.quadraticCurveTo(px+.12,py-.08,px+.24,py); c.quadraticCurveTo(px+.36,py+.08,px+.48,py);}
  c.stroke();
  c.fillStyle='rgba(60,70,50,.13)'; c.beginPath();
  for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){const t=y*W+x; if(!tree[t]) continue; const n=1+Math.floor(hash(t)*3); for(let i=0;i<n;i++){const px=x+.25+hash(t*7+i)*.5,py=y+.25+hash(t*11+i)*.5,r=.14+hash(t*13+i)*.1; c.moveTo(px+.04+r,py+.06); c.arc(px+.04,py+.06,r,0,6.283);}}
  c.fill();
  c.fillStyle=city.treeC; c.beginPath();
  for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){const t=y*W+x; if(!tree[t]) continue; const n=1+Math.floor(hash(t)*3); for(let i=0;i<n;i++){const px=x+.25+hash(t*7+i)*.5,py=y+.25+hash(t*11+i)*.5,r=.14+hash(t*13+i)*.1; c.moveTo(px+r,py); c.arc(px,py,r,0,6.283);}}
  c.fill();
  if(SAVE.settings.grid){
    c.fillStyle='rgba(34,38,45,.10)'; c.beginPath();
    for(let y=b.y0;y<=b.y1;y++)for(let x=b.x0;x<=b.x1;x++){const t=idx(x,y);if(water[t]||mount[t]||tree[t])continue;c.moveTo(x+.545,y+.5);c.arc(x+.5,y+.5,.045,0,6.283);}
    c.fill();
  }
  c.restore();
}
function renderStatic(){
  const b=G.bounds;
  const tk=[cam.cx.toFixed(3),cam.cy.toFixed(3),cam.ts.toFixed(3),cam.oy.toFixed(1),vw,vh,SAVE.settings.grid,G.terrainVer,b.x0,b.x1,b.y0,b.y1,G.ci].join('|');
  if(tk!==terrainKey){ renderTerrain(); terrainKey=tk; }
  const c=sctx, ts=cam.ts, city=G.city;
  c.setTransform(1,0,0,1,0,0); c.drawImage(tc,0,0);
  c.setTransform(dpr*ts,0,0,dpr*ts,dpr*ox(),dpr*oy());
  const segs=(E,filter)=>{const out=[];for(let t=0;t<N;t++){const m=E[t];if(!m)continue;for(let d=0;d<4;d++)if(m&(1<<d)){const n=t+DOFF[d];if(!filter||filter(t,n))out.push(t,n);}}return out;};
  const strokeSegs=(sg,w,col)=>{c.strokeStyle=col;c.lineWidth=w;c.lineCap='round';c.lineJoin='round';c.beginPath();for(let i=0;i<sg.length;i+=2){const a=sg[i],b2=sg[i+1];c.moveTo(a%W+.5,((a/W)|0)+.5);c.lineTo(b2%W+.5,((b2/W)|0)+.5);}c.stroke();};
  const dots=(NN,r,col,filter)=>{c.fillStyle=col;c.beginPath();for(let t=0;t<N;t++)if(NN[t]&&(!filter||filter(t))){const x=t%W+.5,y=((t/W)|0)+.5;c.moveTo(x+r,y);c.arc(x,y,r,0,6.283);}c.fill();};
  const roadS=segs(roadE), railS=segs(railE);
  const wet=(a,b2)=>water[a]||water[b2];
  // poduri
  strokeSegs(segs(roadE,wet),.86,DECK); strokeSegs(segs(railE,wet),.56,DECK);
  dots(roadN,.43,DECK,t=>water[t]); dots(railN,.28,DECK,t=>water[t]&&!roadN[t]);
  // drumuri + sensuri giratorii
  const rounds=[]; for(let t=0;t<N;t++) if(ctrl[t]===2) rounds.push(cxy(t));
  const discs=(r,col)=>{c.fillStyle=col;c.beginPath();for(const [x,y] of rounds){c.moveTo(x+r,y);c.arc(x,y,r,0,6.283);}c.fill();};
  strokeSegs(roadS,.7,city.edge); dots(roadN,.35,city.edge); discs(.76,city.edge);
  strokeSegs(roadS,.56,ROAD); dots(roadN,.28,ROAD); discs(.68,ROAD);
  discs(.25,city.edge); discs(.22,ISLAND);
  c.fillStyle='rgba(255,255,255,.5)'; c.beginPath(); for(const [x,y] of rounds){c.moveTo(x+.07,y-.04);c.arc(x-.02,y-.04,.07,0,6.283);} c.fill();
  // sine
  c.strokeStyle=TIE; c.lineWidth=.06; c.lineCap='butt'; c.beginPath();
  const tieSeg=(ax,ay,bx,by)=>{const dx=bx-ax,dy=by-ay,L=Math.hypot(dx,dy),nx=-dy/L*.2,ny=dx/L*.2,n=Math.max(1,Math.round(L*4));for(let i=0;i<n;i++){const f=(i+.5)/n,px=ax+dx*f,py=ay+dy*f;c.moveTo(px-nx,py-ny);c.lineTo(px+nx,py+ny);}};
  for(let i=0;i<railS.length;i+=2){const a=railS[i],b2=railS[i+1];tieSeg(a%W+.5,((a/W)|0)+.5,b2%W+.5,((b2/W)|0)+.5);}
  for(let t=0;t<N;t++) if(railN[t]&&!railE[t]){const x=t%W+.5,y=((t/W)|0)+.5;tieSeg(x-.3,y,x+.3,y);}
  c.stroke();
  strokeSegs(railS,.13,RAIL);
  dots(railN,.065,RAIL);
  // pasaje
  for(const t of crossList()){
    if(xing[t]!==2) continue;
    const x=t%W+.5, y=((t/W)|0)+.5;
    const half=[];for(let d=0;d<8;d++)if(roadE[t]&(1<<d))half.push([x+DX[d]*.5,y+DY[d]*.5]);
    const draw=(w,col,r)=>{c.strokeStyle=col;c.lineWidth=w;c.lineCap='round';c.beginPath();for(const [px,py] of half){c.moveTo(x,y);c.lineTo(px,py);}c.stroke();c.fillStyle=col;c.beginPath();c.arc(x,y,r,0,6.283);c.fill();};
    c.fillStyle='rgba(40,44,40,.18)'; c.beginPath(); c.arc(x+.06,y+.1,.46,0,6.283); c.fill();
    draw(.84,DECK,.42); draw(.56,ROAD,.28);
  }
  // cladiri care nu se mai misca: depozite si case
  for(const d of G.depots) if(d.inStatic){ shadowRect(c,d,1); drawDepotBody(c,d,1); }
  for(const h of G.houses) if(h.inStatic){ houseShadow(c,h,1); drawHouse(c,h,1); }
}

function render(rdt){
  const key=[cam.cx.toFixed(3),cam.cy.toFixed(3),cam.ts.toFixed(3),cam.oy.toFixed(1),vw,vh,SAVE.settings.grid].join('|');
  if(G.staticDirty||key!==staticKey){renderStatic();staticKey=key;G.staticDirty=false;}
  ctx.setTransform(1,0,0,1,0,0); ctx.clearRect(0,0,cv.width,cv.height);
  const ts=cam.ts; VB=dpr*ts; VX=dpr*ox(); VY=dpr*oy();
  ctx.setTransform(VB,0,0,VB,VX,VY);
  drawCrossings(rdt);
  let promote=false;
  for(const d of G.depots){
    if(!d.inStatic){ const k=pop((G.time-d.born)*2.5); shadowRect(ctx,d,k); drawDepotBody(ctx,d,k); if(G.time-d.born>.5){d.inStatic=true;promote=true;} }
    drawDepotExtras(d);
  }
  for(const s of G.shops) shadowRect(ctx,s,pop((G.time-s.born)*2.5));
  for(const h of G.houses){
    if(h.inStatic) continue;
    const k=pop((G.time-h.born)*3); houseShadow(ctx,h,k); drawHouse(ctx,h,k);
    if(G.time-h.born>.45){h.inStatic=true;promote=true;}
  }
  if(promote) G.staticDirty=true;
  for(const s of G.shops) drawShop(s);
  drawLights();
  for(const c of G.cars) if(c.phase!=='park'&&c.phase!=='idle'&&!c.dead) drawCar(c);
  for(const t of G.trains) if(t.path&&(t.phase==='go'||t.phase==='back')) drawTrain(t);
  ctx.setTransform(VB,0,0,VB,VX,VY);
  drawWrecks();
  drawCursor();
  // fx in spatiul ecranului
  if(G.fx.length){
    ctx.setTransform(dpr,0,0,dpr,0,0);
    ctx.textAlign='center'; ctx.textBaseline='middle';
    const fs=Math.round(clamp(ts*.62,13,22));
    ctx.font='700 '+fs+'px Barlow, "Segoe UI", sans-serif'; ctx.lineWidth=4; ctx.strokeStyle='rgba(255,255,255,.85)';
    for(const f of G.fx){
      const [sx,sy]=t2s(f.x,f.y-f.t*.8);
      ctx.globalAlpha=1-f.t*f.t;
      ctx.strokeText(f.text,sx,sy); ctx.fillStyle=f.color; ctx.fillText(f.text,sx,sy);
    }
    ctx.globalAlpha=1;
  }
  if(dpSel) placeDepotPanel();
}
function vt(x,y,a){const cs=Math.cos(a)*VB, sn=Math.sin(a)*VB; ctx.setTransform(cs,sn,-sn,cs,VX+x*VB,VY+y*VB);}
function shadowRect(g,o,k){const w=(o.w-.28)*k,h=(o.h-.28)*k,cx=o.x+o.w/2,cy=o.y+o.h/2;g.fillStyle='rgba(50,56,46,.18)';rr(g,cx-w/2+.07,cy-h/2+.11,w,h,.28);g.fill();}
function houseShadow(g,h,k){g.fillStyle='rgba(50,56,46,.16)';rr(g,h.x+.2+.06,h.y+.2+.09,.62*k,.62*k,.12);g.fill();}
function notch(g,o,color,w){const px=o.cx+.5+DX[o.d]*.43, py=o.cy+.5+DY[o.d]*.43, a=o.d*Math.PI/4, cs=Math.cos(a), sn=Math.sin(a);
  g.fillStyle=color; g.beginPath();
  const pts=[[-.07,-w/2],[.07,-w/2],[.07,w/2],[-.07,w/2]];
  for(let i=0;i<4;i++){const [lx,ly]=pts[i];const X=px+lx*cs-ly*sn, Y=py+lx*sn+ly*cs; if(i)g.lineTo(X,Y); else g.moveTo(X,Y);}
  g.closePath(); g.fill();}
function drawHouse(g,h,k){
  const col=COLORS[h.color], x=h.x+.5, y=h.y+.5, s_=.62*k, r=.12*k;
  g.save(); g.translate(x,y); g.rotate(h.dir*Math.PI/4);
  g.fillStyle=col.c; rr(g,-s_/2,-s_/2,s_,s_,r); g.fill();
  g.fillStyle=col.d; g.beginPath(); g.moveTo(-s_/2,0); g.lineTo(s_/2,0); g.lineTo(s_/2,s_/2-r); g.arcTo(s_/2,s_/2,s_/2-r,s_/2,r); g.lineTo(-s_/2+r,s_/2); g.arcTo(-s_/2,s_/2,-s_/2,s_/2-r,r); g.closePath(); g.fill();
  g.fillStyle='rgba(255,255,255,.9)'; rr(g,s_/2-.07,-.07,.1,.14,.03); g.fill();
  g.restore();
}
function drawShop(s){
  const k=pop((G.time-s.born)*2.5), col=COLORS[s.color], L=LV[s.level];
  const gt=G.time-s.grown, bump=gt>=0&&gt<.7?1+.1*Math.sin(gt/.7*Math.PI):1;
  const cx=s.x+s.w/2, cy=s.y+s.h/2, sw=(s.w-.28)*k*bump, sh=(s.h-.28)*k*bump;
  if(s.timer>0){
    const pulse=G.failShop===s?1+.07*Math.sin(G.time*14):1, R=(Math.hypot(s.w,s.h)/2*.84+.22)*pulse;
    ctx.lineWidth=.16; ctx.strokeStyle='rgba(34,38,45,.13)'; ctx.beginPath(); ctx.arc(cx,cy,R,0,6.283); ctx.stroke();
    ctx.strokeStyle=s.timer>.66?'#D8452F':INK; ctx.lineCap='round';
    ctx.beginPath(); ctx.arc(cx,cy,R,-Math.PI/2,-Math.PI/2+6.283*s.timer); ctx.stroke();
  }
  ctx.fillStyle=col.c; rr(ctx,cx-sw/2,cy-sh/2,sw,sh,.28*k); ctx.fill();
  if(k<1) return;
  const left=cx-sw/2, top=cy-sh/2;
  if(s.level>=2){ ctx.strokeStyle='rgba(255,255,255,.4)'; ctx.lineWidth=.05; rr(ctx,left+.06,top+.06,sw-.12,sh-.12,.23); ctx.stroke(); }
  if(s.level>=3){ rr(ctx,left+.13,top+.13,sw-.26,sh-.26,.18); ctx.stroke(); }
  notch(ctx,s.door,'#fff',.34); if(s.door2) notch(ctx,s.door2,'#fff',.34); notch(ctx,s.dock,'#2B303A',.5);
  const cols=Math.max(4,Math.floor((sw-.36)/.25)), rows=Math.ceil(L.pins/cols);
  ctx.fillStyle=col.d; rr(ctx,left+.18,top+.18,sw-.36,.12+rows*.27,.12); ctx.fill();
  ctx.fillStyle='#fff'; ctx.beginPath();
  for(let i=0;i<s.demand&&i<L.over;i++){ const r=Math.floor(i/cols), c=i%cols, n=Math.min(cols,s.demand-r*cols), px=cx+(c-(n-1)/2)*.25, py=top+.18+.195+r*.27; ctx.moveTo(px+.085,py); ctx.arc(px,py,.085,0,6.283); }
  ctx.fill();
  if(s.demand>L.over){ ctx.fillStyle='#FFD7CF'; ctx.beginPath();
    for(let i=L.over;i<s.demand;i++){ const r=Math.floor(i/cols), c=i%cols, n=Math.min(cols,s.demand-r*cols), px=cx+(c-(n-1)/2)*.25, py=top+.18+.195+r*.27; ctx.moveTo(px+.085,py); ctx.arc(px,py,.085,0,6.283); }
    ctx.fill(); }
  const bw=(sw-.4)/s.max;
  ctx.fillStyle='rgba(255,255,255,.95)'; ctx.beginPath();
  for(let i=0;i<s.stock;i++) ctx.rect(left+.2+i*bw,top+sh-.52,bw-.04,.32);
  ctx.fill();
  ctx.fillStyle='rgba(0,0,0,.18)'; ctx.beginPath();
  for(let i=s.stock;i<s.max;i++) ctx.rect(left+.2+i*bw,top+sh-.52,bw-.04,.32);
  ctx.fill();
  if(s.stock===0&&Math.floor(G.time*3)%2===0){ctx.strokeStyle=INK;ctx.lineWidth=.07;rr(ctx,left-.06,top-.06,sw+.12,sh+.12,.32);ctx.stroke();}
}
function drawDepotBody(g,d,k){
  const cx=d.x+1, cy=d.y+1, sz=1.72*k;
  g.fillStyle=DEPOT; rr(g,cx-sz/2,cy-sz/2,sz,sz,.24*k); g.fill();
  if(k<1) return;
  notch(g,d.dock,'#2B303A',.5); notch(g,d.door,'#fff',.34);
  g.lineWidth=.035; g.strokeStyle=CRATE_D;
  for(const [ox_,oy_] of [[-.5,-.5],[.06,-.5],[-.5,.06],[.06,.06]]){
    g.fillStyle=CRATE; rr(g,cx+ox_,cy+oy_,.44,.44,.06); g.fill(); g.stroke();
    g.beginPath(); g.moveTo(cx+ox_+.07,cy+oy_+.07); g.lineTo(cx+ox_+.37,cy+oy_+.37); g.moveTo(cx+ox_+.37,cy+oy_+.07); g.lineTo(cx+ox_+.07,cy+oy_+.37); g.stroke();
  }
}
function drawDepotExtras(d){
  const cx=d.x+1, cy=d.y+1;
  let idleT=0, idleK=0;
  for(const t of G.trains) if(t.depot===d&&t.phase==='idle') idleT++;
  for(const c of G.cars) if(c.kind==='truck'&&c.depot===d&&c.phase==='idle') idleK++;
  if(idleT){ ctx.fillStyle='#fff'; ctx.beginPath(); for(let i=0;i<idleT&&i<5;i++) ctx.rect(cx-.78+i*.3,cy+.66,.24,.11); ctx.fill(); }
  if(idleK){ ctx.fillStyle=CRATE; ctx.beginPath(); for(let i=0;i<idleK&&i<5;i++) ctx.rect(cx+.6-i*.22,cy+.64,.16,.14); ctx.fill(); }
  // culori deservite (doar daca nu sunt toate)
  let all=true; for(let c=0;c<G.colorsUsed;c++) if(!((d.serve>>c)&1)) all=false;
  if(!all){ let n=0; for(let c=0;c<G.colorsUsed;c++) if((d.serve>>c)&1){ ctx.fillStyle=COLORS[c].c; ctx.beginPath(); ctx.arc(cx-.7+n*.26,cy-1.08,.1,0,6.283); ctx.fill(); n++; } }
  if(dpSel===d){ ctx.strokeStyle=INK; ctx.lineWidth=.08; ctx.setLineDash([.18,.12]); ctx.lineDashOffset=-G.time*.6; rr(ctx,cx-1.08,cy-1.08,2.16,2.16,.36); ctx.stroke(); ctx.setLineDash([]); }
}
function drawLights(){
  for(const [t,ns] of G.nodeState){
    if(ctrl[t]!==1) continue;
    const x=t%W+.5, y=((t/W)|0)+.5;
    for(let d=0;d<8;d++){
      if(!(roadE[t]&(1<<d))||!roadN[t+DOFF[d]]) continue;
      const ux=DX[d]/DLEN[d], uy=DY[d]/DLEN[d], px=x+ux*.52+uy*.36, py=y+uy*.52-ux*.36;
      ctx.fillStyle=INK; ctx.beginPath(); ctx.arc(px,py,.125,0,6.283); ctx.fill();
      ctx.fillStyle=(d&3)===ns.phase?GREEN:'#E8604C'; ctx.beginPath(); ctx.arc(px,py,.08,0,6.283); ctx.fill();
    }
  }
}
function drawCar(c){
  vt(c.x,c.y,c.ang);
  if(c.kind==='truck'){
    ctx.fillStyle='rgba(40,44,40,.2)'; rr(ctx,-.25,-.1,.54,.28,.07); ctx.fill();
    ctx.fillStyle=c.phase==='go'?CRATE:'#A7ACB2'; rr(ctx,-.29,-.14,.4,.28,.05); ctx.fill();
    ctx.strokeStyle=c.phase==='go'?CRATE_D:'#80858C'; ctx.lineWidth=.03; ctx.stroke();
    ctx.fillStyle='#2B303A'; rr(ctx,.12,-.125,.17,.25,.05); ctx.fill();
    ctx.fillStyle='#5E6676'; ctx.fillRect(.2,-.09,.06,.18);
  } else {
    const col=COLORS[c.color];
    ctx.fillStyle='rgba(40,44,40,.2)'; rr(ctx,-.18,-.08,.4,.24,.08); ctx.fill();
    ctx.fillStyle=col.c; rr(ctx,-.2,-.115,.4,.23,.085); ctx.fill();
    ctx.fillStyle=col.l; ctx.fillRect(-.08,-.085,.15,.17);
  }
}
function drawTrain(tr){
  const total=tr.cum[tr.cum.length-1];
  for(let i=TRAIN_PARTS.length-1;i>=0;i--){
    const ps=tr.s-TRAIN_PARTS[i]; if(ps<.35||ps>total-.35) continue;
    const [x,y,a]=trainPos(tr,ps);
    vt(x,y,a);
    ctx.fillStyle='rgba(40,44,40,.22)'; rr(ctx,-.3,-.12,.64,.34,.08); ctx.fill();
    if(i===0){
      ctx.fillStyle='#2B303A'; rr(ctx,-.33,-.17,.66,.34,.09); ctx.fill();
      ctx.fillStyle='#5E6676'; ctx.fillRect(-.26,-.1,.3,.2);
      ctx.fillStyle='#F4D35E'; ctx.beginPath(); ctx.arc(.26,-.08,.04,0,6.283); ctx.arc(.26,.08,.04,0,6.283); ctx.fill();
    } else {
      const loaded=tr.phase==='go';
      ctx.fillStyle=loaded?CRATE:'#A7ACB2'; rr(ctx,-.3,-.155,.6,.31,.06); ctx.fill();
      if(loaded){ctx.strokeStyle=CRATE_D; ctx.lineWidth=.035; ctx.beginPath();ctx.moveTo(-.02,-.15);ctx.lineTo(-.02,.15);ctx.moveTo(-.3,0);ctx.lineTo(.3,0);ctx.stroke();}
    }
  }
}
function drawCrossings(rdt){
  const blink=Math.floor(G.time*4)%2===0;
  for(const t of crossList()){
    const x=xing[t]; if(x===2) continue;
    const px=t%W+.5, py=((t/W)|0)+.5;
    if(x===0){
      const sx=px+.36, sy=py-.36;
      ctx.fillStyle='#F2C230'; ctx.beginPath(); ctx.moveTo(sx,sy-.17); ctx.lineTo(sx+.17,sy); ctx.lineTo(sx,sy+.17); ctx.lineTo(sx-.17,sy); ctx.closePath(); ctx.fill();
      ctx.strokeStyle=INK; ctx.lineWidth=.04; ctx.beginPath(); ctx.moveTo(sx-.06,sy-.06); ctx.lineTo(sx+.06,sy+.06); ctx.moveTo(sx+.06,sy-.06); ctx.lineTo(sx-.06,sy+.06); ctx.stroke();
      continue;
    }
    const locked=G.lock.has(t);
    barAnim[t]+=((locked?1:0)-barAnim[t])*Math.min(1,rdt*7);
    let rd=0; for(let d=0;d<8;d++) if(railE[t]&(1<<d)){rd=d;break;}
    const a=barAnim[t];
    vt(px,py,rd*Math.PI/4);
    for(const sgn of [-1,1]){
      const yy=sgn*.37, x0=sgn*.36, len=.12+.56*a, x1=x0-sgn*len;
      ctx.lineCap='round'; ctx.strokeStyle='#fff'; ctx.lineWidth=.1; ctx.beginPath(); ctx.moveTo(x0,yy); ctx.lineTo(x1,yy); ctx.stroke();
      ctx.lineCap='butt'; ctx.strokeStyle='#E8604C'; ctx.beginPath();
      for(let q=.09;q<len;q+=.18){ const qa=x0-sgn*q, qb=x0-sgn*Math.min(len,q+.09); ctx.moveTo(qa,yy); ctx.lineTo(qb,yy); }
      ctx.stroke();
      ctx.fillStyle=INK; ctx.beginPath(); ctx.arc(x0,yy,.07,0,6.283); ctx.fill();
      if(locked){ctx.fillStyle=blink?'#FF4A33':'#7A2E26';ctx.beginPath();ctx.arc(x0,yy,.04,0,6.283);ctx.fill();}
    }
  }
  ctx.setTransform(VB,0,0,VB,VX,VY);
}
function drawWrecks(){
  for(const t of G.wrecks){
    const x=t%W+.5, y=((t/W)|0)+.5, f=wreck[t]/9;
    for(let i=0;i<3;i++){const ph=(G.time*.8+i/3)%1;ctx.fillStyle='rgba(90,94,100,'+(.35*(1-ph))+')';ctx.beginPath();ctx.arc(x+(i-1)*.14,y-.2-ph*.5,.1+ph*.18,0,6.283);ctx.fill();}
    ctx.fillStyle='#F28C28'; ctx.beginPath();
    for(let i=0;i<10;i++){const r=i%2?.14:.3,a=i*Math.PI/5+G.time*.5;ctx.lineTo(x+Math.cos(a)*r,y+Math.sin(a)*r);}
    ctx.closePath(); ctx.fill();
    ctx.fillStyle='#E8604C'; ctx.beginPath(); ctx.arc(x,y,.1,0,6.283); ctx.fill();
    ctx.strokeStyle=INK; ctx.lineWidth=.06; ctx.lineCap='round'; ctx.beginPath(); ctx.arc(x,y,.45,-Math.PI/2,-Math.PI/2+6.283*f); ctx.stroke();
  }
}
''')

# cursor: liste in loc de scanarea intregii harti
rep('''  if(tool==='lights'||tool==='round'){
    const pulse=.3+.1*Math.sin(G.time*6), want=tool==='lights'?1:2;
    for(let q=0;q<N;q++) if(roadN[q]&&!railN[q]&&ctrl[q]!==want&&isInter(q)){''','''  if(tool==='lights'||tool==='round'){
    const pulse=.3+.1*Math.sin(G.time*6), want=tool==='lights'?1:2;
    for(const q of interList()) if(!railN[q]&&ctrl[q]!==want){''')
rep('''    for(let q=0;q<N;q++) if(roadN[q]&&railN[q]&&(tool==='overpass'?xing[q]!==2:xing[q]===0)){''','''    for(const q of crossList()) if(tool==='overpass'?xing[q]!==2:xing[q]===0){''')

# =============================================================== CONTROL: click pe depozit
rep("""  const erase=e.button===2||G.tool==='erase';
  if(!erase&&(G.tool==='barrier'""","""  const erase=e.button===2||G.tool==='erase';
  const bb=bmap[t];
  if(bb&&bb.type==='depot'&&!erase){ openDepot(bb); return; }
  if(dpSel) closeDepot();
  if(!erase&&(G.tool==='barrier'""")
rep('''  if(e.key==='Escape'){ e.preventDefault();''','''  if(e.key==='Escape'&&dpSel){ e.preventDefault(); closeDepot(); return; }
  if(e.key==='Escape'){ e.preventDefault();''')

# =============================================================== INTERFATA: panou depozit
rep('''function startCity(ci){''','''// ---------- panou depozit
let dpSel=null, dpRefreshT=0;
function openDepot(d){
  if(d.serve===undefined) d.serve=31;
  dpSel=d; $('depotPanel').hidden=false; refreshDepot(); placeDepotPanel(); sfx('place');
}
function closeDepot(){ dpSel=null; const p=$('depotPanel'); if(p) p.hidden=true; }
function placeDepotPanel(){
  const p=$('depotPanel'), d=dpSel, pw=p.offsetWidth||260, ph=p.offsetHeight||250;
  let [sx,sy]=t2s(d.x+2.4,d.y-.2);
  if(sx+pw>vw-12){ const l=t2s(d.x-.4,d.y-.2); sx=l[0]-pw; }
  sx=clamp(sx,12,vw-pw-12); sy=clamp(sy,76,vh-ph-96);
  p.style.left=sx+'px'; p.style.top=sy+'px';
}
function refreshDepot(){
  const d=dpSel; if(!d) return;
  const nt=depotTrains(d), nk=depotTrucks(d);
  $('dpTn').textContent=nt; $('dpKn').textContent=nk;
  $('dpTp').disabled=G.res.loco<=0; $('dpTm').disabled=nt<=0;
  $('dpKp').disabled=G.res.truck<=0; $('dpKm').disabled=nk<=0;
  const box=$('dpChips');
  if(box.childElementCount!==G.colorsUsed){
    box.innerHTML='';
    for(let c=0;c<G.colorsUsed;c++){ const b=document.createElement('button'); b.className='chip'; b.style.background=COLORS[c].c; b.onclick=()=>{ dpSel.serve^=(1<<c); if(!(dpSel.serve&((1<<G.colorsUsed)-1))) dpSel.serve|=(1<<c); refreshDepot(); sfx('place'); }; box.appendChild(b); }
  }
  [...box.children].forEach((b,c)=>b.classList.toggle('off',!((d.serve>>c)&1)));
  $('dpFree').textContent=tr('dpFree',{t:G.res.loco,k:G.res.truck});
  const chosen=G.shops.filter(s=>serves(d,s));
  const rr_=depotRail(d), rd=depotRoad(d);
  const notes=[];
  if(nt>0&&!chosen.some(s=>s.cells.some(c=>rr_.dist[c]<Infinity))) notes.push(tr('dpNoRail'));
  if(nk>0&&!chosen.some(s=>s.cells.some(c=>rd.dist[c]<Infinity))) notes.push(tr('dpNoRoad'));
  $('dpNote').textContent=notes.join(' ');
}
$('dpClose').onclick=closeDepot;
$('dpTp').onclick=()=>{ if(dpSel&&addTrain(dpSel)){sfx('place');updateHud(true);} refreshDepot(); };
$('dpTm').onclick=()=>{ if(dpSel){removeTrain(dpSel);sfx('erase');updateHud(true);} refreshDepot(); };
$('dpKp').onclick=()=>{ if(dpSel&&addTruck(dpSel)){sfx('place');updateHud(true);} refreshDepot(); };
$('dpKm').onclick=()=>{ if(dpSel){removeTruck(dpSel);sfx('erase');updateHud(true);} refreshDepot(); };
function openNextDepot(){ if(!G||G.mode!=='play'||!G.depots.length) return; const i=dpSel?G.depots.indexOf(dpSel):-1; openDepot(G.depots[(i+1)%G.depots.length]); }
$('sLoco').onclick=openNextDepot; $('sTruck').onclick=openNextDepot;

function startCity(ci){''')
rep('''  const tips={tRoad:'road',tRail:'rail',tBarrier:'barrier',tOverpass:'overpass',tLights:'lights',tRound:'round',tErase:'erase',sLoco:'trains',sTruck:'trucks',sBridge:'bridges'};''',
    '''  const tips={tRoad:'road',tRail:'rail',tBarrier:'barrier',tOverpass:'overpass',tLights:'lights',tRound:'round',tErase:'erase',sLoco:'freeTip',sTruck:'freeTip',sBridge:'bridges'};''')
rep('''function toMenu(){''','''function toMenu(){
  closeDepot();''')
rep('''function openPause(){''','''function openPause(){ closeDepot();''')
rep('''function gameOver(s){
  G.over=true;''','''function gameOver(s){
  closeDepot();
  G.over=true;''')
# depozite noi: toate culorile
rep('''    const d={type:'depot',id:uid++,x,y,w:2,h:2,cells:''','''    const d={type:'depot',id:uid++,x,y,w:2,h:2,serve:31,cells:''')

# =============================================================== BUCLA: reimprospatare panou
rep('''  if(toastT>0){ toastT-=rdt; if(toastT<=0) $('toast').classList.remove('show'); }''','''  if(toastT>0){ toastT-=rdt; if(toastT<=0) $('toast').classList.remove('show'); }
  if(dpSel){ dpRefreshT-=rdt; if(dpRefreshT<=0){ dpRefreshT=.25; refreshDepot(); } }''')
rep('''window.__TJ={get G(){return G;},render,''','''window.__TJ={get G(){return G;},render,addTrain,addTruck,removeTrain,removeTruck,openDepot,closeDepot,''')

open(P,'w').write(s)
print('ok v12')
