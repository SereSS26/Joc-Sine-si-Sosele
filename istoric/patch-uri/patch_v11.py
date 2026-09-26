import re
P='/home/claude/joc/src/game.html'
s=open(P).read()

def section(name, new):
    global s
    hdr='// =====================================================================\n//  '+name+'\n// =====================================================================\n'
    i=s.index(hdr)+len(hdr)
    j=s.index('// =====================================================================\n',i)
    s=s[:i]+new.strip('\n')+'\n\n'+s[j:]

def rep(a,b,count=1):
    global s
    assert a in s, 'missing: '+a[:80]
    s=s.replace(a,b,count)

# ---------------------------------------------------------------- HTML
rep('''      <button class="tool" data-tool="erase" id="tErase">
        <svg viewBox="0 0 24 24"><path d="M7 7l10 10M17 7L7 17" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>
        <span class="lbl" data-t="erase"></span><kbd>5</kbd>
      </button>''','''      <button class="tool" data-tool="lights" id="tLights">
        <svg viewBox="0 0 24 24"><rect x="8" y="2.5" width="8" height="15" rx="3" fill="currentColor"/><circle cx="12" cy="6.8" r="2.1" fill="#E8604C"/><circle cx="12" cy="13.2" r="2.1" fill="#3DBE6A"/><path d="M12 17.5V22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        <span class="lbl" data-t="lights"></span><span class="cnt" id="cLights">0</span><kbd>5</kbd>
      </button>
      <button class="tool" data-tool="round" id="tRound">
        <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5" fill="none" stroke="#B9BEB2" stroke-width="5.5"/><circle cx="12" cy="12" r="8.5" fill="none" stroke="#fff" stroke-width="3.6"/><circle cx="12" cy="12" r="3.4" fill="#8DB07E"/><path d="M12 1v2.5M12 20.5V23M1 12h2.5M20.5 12H23" stroke="#B9BEB2" stroke-width="3"/></svg>
        <span class="lbl" data-t="round"></span><span class="cnt" id="cRound">0</span><kbd>6</kbd>
      </button>
      <button class="tool" data-tool="erase" id="tErase">
        <svg viewBox="0 0 24 24"><path d="M7 7l10 10M17 7L7 17" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>
        <span class="lbl" data-t="erase"></span><kbd>7</kbd>
      </button>''')
rep('''        <span id="cLoco">0</span><small data-t="trains"></small>
      </div>''','''        <span id="cLoco">0</span><small data-t="trains"></small>
      </div>
      <div class="stat" id="sTruck">
        <svg viewBox="0 0 24 24"><rect x="2" y="6" width="13" height="10" rx="1.5" fill="#C99B5B"/><path d="M15 9h4l3 3.5V16h-7z" fill="currentColor"/><circle cx="6.5" cy="18" r="1.8" fill="currentColor"/><circle cx="17.5" cy="18" r="1.8" fill="currentColor"/></svg>
        <span id="cTruck">0</span><small data-t="trucks"></small>
      </div>''')
rep('''@media (max-width:1000px){ .tool .lbl,.stat small{display:none;} .tool{padding:8px 10px;} }''','''@media (max-width:1380px){ .tool .lbl,.stat small{display:none;} .tool{padding:8px 10px;} }''')
rep('''        <li><svg viewBox="0 0 44 44"><circle cx="22" cy="22" r="18" fill="none" stroke="#D3D7CD" stroke-width="4"/>''','''        <li><svg viewBox="0 0 44 44"><path d="M22 2v40M2 22h40" stroke="#B9BEB2" stroke-width="11"/><path d="M22 2v40M2 22h40" stroke="#fff" stroke-width="8"/><circle cx="22" cy="22" r="10" fill="#B9BEB2"/><circle cx="22" cy="22" r="8.6" fill="#fff"/><circle cx="22" cy="22" r="3.6" fill="#8DB07E"/><rect x="30" y="4" width="7" height="12" rx="2.5" fill="#22262D"/><circle cx="33.5" cy="7.6" r="1.7" fill="#E8604C"/><circle cx="33.5" cy="12.4" r="1.7" fill="#3DBE6A"/></svg><div><b data-t="how5t"></b><span data-t="how5"></span></div></li>
        <li><svg viewBox="0 0 44 44"><rect x="3" y="9" width="24" height="24" rx="4" fill="#3E7BD2"/><rect x="27" y="9" width="12" height="24" rx="4" fill="#3E7BD2" opacity=".55"/><rect x="6" y="12" width="18" height="7" rx="2" fill="#2C5CA3"/><circle cx="9.5" cy="15.5" r="1.4" fill="#fff"/><circle cx="13.5" cy="15.5" r="1.4" fill="#fff"/><circle cx="17.5" cy="15.5" r="1.4" fill="#fff"/><rect x="6" y="36" width="15" height="6" rx="1.5" fill="#C99B5B"/><path d="M21 37.5h4l2 2.5V42h-6z" fill="#22262D"/></svg><div><b data-t="how6t"></b><span data-t="how6"></span></div></li>
        <li><svg viewBox="0 0 44 44"><circle cx="22" cy="22" r="18" fill="none" stroke="#D3D7CD" stroke-width="4"/>''')

# ---------------------------------------------------------------- CONSTANTE
section('CONSTANTE', r'''
const W=48,H=30,N=W*H;
const DX=[1,1,0,-1,-1,-1,0,1], DY=[0,1,1,1,0,-1,-1,-1];
const DOFF=DX.map((d,i)=>d+DY[i]*W);
const DLEN=DX.map((d,i)=>(d&&DY[i])?Math.SQRT2:1);
const DLUT=new Int8Array(9).fill(-1); for(let d=0;d<8;d++) DLUT[(DY[d]+1)*3+DX[d]+1]=d;
const STEP=1/60;
const CAR_SPEED=2.4, TRUCK_SPEED=1.9, TRAIN_SPEED=2.9, GAP=.44, WEEK_LEN=45;
const TRAIN_CARGO=6, TRUCK_CARGO=3, RZ=.42, BASE_DEMAND=1/7.5;
// niveluri magazin: stoc maxim, prag de aglomerare, pini maximi, livrari pentru nivel, multiplicator cerere
const LV=[null,
  {max:8, over:6, pins:10,need:0, mul:1},
  {max:10,over:8, pins:12,need:18,mul:1.45},
  {max:12,over:10,pins:14,need:45,mul:1.9}];
const COLORS=[
  {c:'#E8604C',l:'#F2927F',d:'#B9493A'},
  {c:'#3E7BD2',l:'#76A2E3',d:'#2C5CA3'},
  {c:'#E6A823',l:'#F1C565',d:'#AF7E10'},
  {c:'#2FA38D',l:'#68C2B0',d:'#1F7A69'},
  {c:'#9265CC',l:'#B292DD',d:'#6C489F'},
];
const INK='#22262D', FOG='#CFD4C8', ROAD='#FFFFFF', RAIL='#353A45', TIE='#8A8F96', DECK='#7E8B92';
const DEPOT='#4A505C', CRATE='#C99B5B', CRATE_D='#8E6A38', GREEN='#3DBE6A', ISLAND='#8DB07E';
const CITIES=[
  {id:'cluj',     name:{ro:'Cluj',en:'Cluj'},           land:'#E2E7DB', edge:'#C3CABB', water:'#9CC4DC', shore:'#86B1CC', mount:'#CBD2C2', treeC:'#B5C6A6', seed:1207, feats:['riverV'],           trees:.9, diff:1.00, need:0},
  {id:'timisoara',name:{ro:'Timisoara',en:'Timisoara'}, land:'#E6E5DA', edge:'#C8C8BA', water:'#98C0D8', shore:'#82ACC6', mount:'#D2D1C3', treeC:'#BCC7A4', seed:3391, feats:['riverH','lake'],    trees:.7, diff:1.06, need:80},
  {id:'brasov',   name:{ro:'Brasov',en:'Brasov'},       land:'#DFE6DE', edge:'#C0C9BF', water:'#9AC3D9', shore:'#84AFC7', mount:'#BFC9BC', treeC:'#A8BF9E', seed:5519, feats:['mountains','riverV'],trees:1.3, diff:1.10, need:80},
  {id:'constanta',name:{ro:'Constanta',en:'Constanta'}, land:'#E8E3D5', edge:'#CBC5B4', water:'#8DBCD8', shore:'#77A8C6', mount:'#D6D0BF', treeC:'#C3C8A2', seed:8123, feats:['sea','lake'],       trees:.5, diff:1.15, need:80},
  {id:'bucuresti',name:{ro:'Bucuresti',en:'Bucharest'}, land:'#E5E2DD', edge:'#C9C5BE', water:'#9BC1D6', shore:'#85ADC4', mount:'#D3CFC7', treeC:'#B9C3A8', seed:9907, feats:['riverH','lakes'],   trees:.8, diff:1.22, need:80},
];
''')

# ---------------------------------------------------------------- TEXTE
section('TEXTE (fara diacritice)', r'''
const STR={
ro:{
  tagline:'Drumuri, sine si orase care cresc.', play:'Joaca', cities:'Alege orasul', citiesTitle:'Unde construiesti?',
  settings:'Setari', how:'Cum se joaca', quit:'Iesire', back:'Inapoi', resume:'Continua', restart:'Reincepe', mainMenu:'Meniu principal', paused:'Pauza',
  week:'Saptamana', deliveries:'livrari', record:'record', weeks:'saptamani', accidents:'accidente',
  road:'Drum', rail:'Cale ferata', barrier:'Bariera', overpass:'Pasaj', lights:'Semafor', round:'Sens giratoriu', erase:'Sterge',
  bridges:'poduri', trains:'trenuri', trucks:'camioane',
  language:'Limba', music:'Muzica', sfx:'Efecte sonore', fullscreen:'Ecran complet', grid:'Grila pe harta', on:'Pornit', off:'Oprit',
  unlockReq:'Fa {n} livrari in {c}', bestLbl:'Record: {n} livrari', notPlayed:'Nejucat inca', newCity:'Ai deblocat orasul {c}!',
  weekTitle:'Orasul creste', weekGift:'Ai primit +20 bucati de drum. Alege inca un bonus:',
  overTitle:'Un magazin s-a inchis', overText:'Clientii au asteptat prea mult. Iata cat a rezistat orasul tau:', again:'Joaca din nou',
  pauseTip:'Pauza (Space)', speedTip:'Viteza (F)', menuTip:'Meniu (Esc)',
  how1t:'Case si magazine', how1:'Masinile pleaca de la case spre magazinul de aceeasi culoare. Trage cu mouse-ul un drum de la iesirea casei pana la intrarea magazinului. Poti trasa si in diagonala.',
  how2t:'Marfa vine cu trenul sau cu camionul', how2:'Fiecare magazin are un stoc de marfa. Trenurile merg pe calea ferata de la depozit la platforma neagra a magazinului. Camioanele pleaca din depozit pe drumuri, la intrarea alba, si stau in trafic ca masinile.',
  how3t:'Treceri la nivel', how3:'Unde drumul taie calea ferata pot avea loc accidente. O bariera opreste masinile cand vine trenul. Un pasaj duce drumul pe deasupra sinelor.',
  how5t:'Intersectii', how5:'Unde se intalnesc 3 sau mai multe drumuri, masinile incetinesc si trec pe rand. Semaforul lasa pe rand cate o directie, fara oprire. Sensul giratoriu lasa mai multe masini deodata.',
  how6t:'Magazinele cresc', how6:'Un magazin bine servit creste pana la nivelul 3: devine mai mare, are mai multi clienti si stoc mai mare, iar la nivelul 3 primeste a doua intrare.',
  how4t:'Nu lasa clientii sa astepte', how4:'Cand un magazin are prea multi clienti, cercul din jurul lui se umple. Daca se umple complet, jocul se termina. Click dreapta sterge drumuri si sine.',
  keys:'Taste: 1-7 unelte, Space pauza, F viteza, Esc meniu',
  hStart:'Trage un drum de la iesirea caselor pana la intrarea magazinului de aceeasi culoare. Poti trasa si in diagonala.',
  hSupply:'Magazinul ramane fara marfa! Leaga depozitul gri de magazin: cu drum (pentru camion) sau cu cale ferata (pentru tren).',
  hTruck:'Ai un camion liber. Leaga intrarea alba a depozitului de drumurile spre magazine.',
  hUnguarded:'Trecere fara bariera: masinile pot fi lovite de tren. Pune o Bariera (3) sau un Pasaj (4) pe ea.',
  hAccident:'Accident! Trecerea ramane blocata cateva secunde. Pune bariere.',
  hInter:'Intersectie noua: aici masinile trec pe rand. Cand se aglomereaza, pune un Semafor (5) sau un Sens giratoriu (6).',
  hGrow:'Un magazin a crescut! Are mai multi clienti si are nevoie de mai multa marfa.',
  hNoBridge:'Nu mai ai poduri. Poti primi altele ca bonus saptamanal.',
  hNoRes:'Nu mai ai {r}. Alege bonusuri la sfarsitul saptamanii.',
  hPick:'Alege o trecere la nivel, adica locul unde drumul taie calea ferata.',
  hPickInter:'Alege o intersectie unde se intalnesc cel putin 3 drumuri (fara cale ferata).',
  hNoBarrier:'Nu mai ai bariere. Poti primi altele ca bonus saptamanal.',
  hNoOverpass:'Nu ai pasaje. Le poti alege ca bonus saptamanal.',
  hNoLights:'Nu mai ai semafoare. Poti primi altele ca bonus saptamanal.',
  hNoRound:'Nu ai sensuri giratorii. Le poti alege ca bonus saptamanal.',
  hDiag:'Doua diagonale nu se pot intersecta. Fa o intersectie pe un patratel.',
  hParallel:'Drumul poate doar traversa calea ferata, nu poate merge pe ea.',
  hDepot:'A aparut un depozit nou.',
  rnRoad:'drum', rnRail:'sina', levelFx:'NIVEL {n}',
  uLoco:'Locomotiva', uLocoD:'+1 tren (6 lazi de marfa)', uTruck:'Camion', uTruckD:'+1 camion (3 lazi, merge pe drum)',
  uRail:'Cale ferata', uRailD:'+20 bucati de sina', uBridge:'Poduri', uBridgeD:'+2 poduri peste apa',
  uRoad:'Drumuri', uRoadD:'+30 bucati de drum', uBarrier:'Bariere', uBarrierD:'+2 bariere pentru treceri',
  uOverpass:'Pasaj', uOverpassD:'Drumul trece pe deasupra caii ferate',
  uLights:'Semafoare', uLightsD:'+2 semafoare pentru intersectii', uRound:'Sens giratoriu', uRoundD:'Intersectie fluida pentru multe masini',
  version:'Versiunea 1.1', accidentFx:'ACCIDENT',
},
en:{
  tagline:'Roads, rails and growing towns.', play:'Play', cities:'Choose a city', citiesTitle:'Where do you build?',
  settings:'Settings', how:'How to play', quit:'Quit', back:'Back', resume:'Resume', restart:'Restart', mainMenu:'Main menu', paused:'Paused',
  week:'Week', deliveries:'deliveries', record:'best', weeks:'weeks', accidents:'accidents',
  road:'Road', rail:'Railway', barrier:'Barrier', overpass:'Overpass', lights:'Traffic light', round:'Roundabout', erase:'Erase',
  bridges:'bridges', trains:'trains', trucks:'trucks',
  language:'Language', music:'Music', sfx:'Sound effects', fullscreen:'Fullscreen', grid:'Map grid', on:'On', off:'Off',
  unlockReq:'Make {n} deliveries in {c}', bestLbl:'Best: {n} deliveries', notPlayed:'Not played yet', newCity:'You unlocked {c}!',
  weekTitle:'The town grows', weekGift:'You got +20 road pieces. Pick one more bonus:',
  overTitle:'A shop has closed', overText:'Customers waited too long. Here is how long your town lasted:', again:'Play again',
  pauseTip:'Pause (Space)', speedTip:'Speed (F)', menuTip:'Menu (Esc)',
  how1t:'Houses and shops', how1:'Cars drive from houses to the shop of the same color. Drag with the mouse to draw a road from the house exit to the shop entrance. Diagonals work too.',
  how2t:'Goods come by train or truck', how2:'Every shop has a stock of goods. Trains run on rails from the depot to the black platform of a shop. Trucks leave the depot on roads, to the white entrance, and get stuck in traffic like cars.',
  how3t:'Level crossings', how3:'Where a road crosses the railway, accidents can happen. A barrier stops cars when a train comes. An overpass takes the road over the tracks.',
  how5t:'Junctions', how5:'Where 3 or more roads meet, cars slow down and take turns. A traffic light lets one direction through at a time without stopping. A roundabout lets several cars in at once.',
  how6t:'Shops grow', how6:'A well served shop grows up to level 3: it gets bigger, has more customers and a larger stock, and at level 3 it opens a second entrance.',
  how4t:'Keep customers happy', how4:'When a shop has too many customers, the ring around it fills up. If it fills completely, the game is over. Right click erases roads and rails.',
  keys:'Keys: 1-7 tools, Space pause, F speed, Esc menu',
  hStart:'Drag a road from the exit of the houses to the entrance of the shop with the same color. Diagonals work too.',
  hSupply:'The shop is running out of goods! Connect the grey depot to the shop: with a road (for trucks) or with rails (for trains).',
  hTruck:'You have a free truck. Connect the white exit of the depot to the roads that lead to shops.',
  hUnguarded:'Unguarded crossing: trains can hit cars here. Put a Barrier (3) or an Overpass (4) on it.',
  hAccident:'Accident! The crossing is blocked for a few seconds. Use barriers.',
  hInter:'New junction: cars take turns here. When it gets busy, add a Traffic light (5) or a Roundabout (6).',
  hGrow:'A shop has grown! It has more customers and needs more goods.',
  hNoBridge:'No bridges left. You can get more as a weekly bonus.',
  hNoRes:'No {r} left. Pick bonuses at the end of the week.',
  hPick:'Pick a level crossing, where a road crosses the railway.',
  hPickInter:'Pick a junction where at least 3 roads meet (no railway).',
  hNoBarrier:'No barriers left. You can get more as a weekly bonus.',
  hNoOverpass:'No overpasses yet. You can pick them as a weekly bonus.',
  hNoLights:'No traffic lights left. You can get more as a weekly bonus.',
  hNoRound:'No roundabouts yet. You can pick them as a weekly bonus.',
  hDiag:'Two diagonals cannot cross. Make the junction on a tile.',
  hParallel:'A road can only cross the railway, it cannot run along it.',
  hDepot:'A new depot has appeared.',
  rnRoad:'road', rnRail:'rail', levelFx:'LEVEL {n}',
  uLoco:'Locomotive', uLocoD:'+1 train (6 crates of goods)', uTruck:'Truck', uTruckD:'+1 truck (3 crates, drives on roads)',
  uRail:'Railway', uRailD:'+20 rail pieces', uBridge:'Bridges', uBridgeD:'+2 bridges over water',
  uRoad:'Roads', uRoadD:'+30 road pieces', uBarrier:'Barriers', uBarrierD:'+2 barriers for crossings',
  uOverpass:'Overpass', uOverpassD:'The road goes over the railway',
  uLights:'Traffic lights', uLightsD:'+2 lights for junctions', uRound:'Roundabout', uRoundD:'Smooth junction for many cars',
  version:'Version 1.1', accidentFx:'CRASH',
}};
''')

# ---------------------------------------------------------------- STARE JOC
section('STARE JOC', r'''
let G=null, uid=1;
const cam={cx:W/2,cy:H/2,ts:24,oy:0};
let vw=0,vh=0,dpr=1;
const cv=$('cv'), ctx=cv.getContext('2d');
const sc=document.createElement('canvas'), sctx=sc.getContext('2d');
let staticKey='';
const ctrl=new Uint8Array(N), degArr=new Uint8Array(N);   // ctrl: 1 semafor, 2 sens giratoriu

function inB(x,y){if(!inGrid(x,y))return false;const b=G.bounds;return x>=b.x0&&x<=b.x1&&y>=b.y0&&y<=b.y1;}
function inBt(t){return inB(t%W,(t/W)|0);}
function tileFree(t){return !water[t]&&!mount[t]&&!bmap[t]&&!roadN[t]&&!railN[t];}
function mkCache(){return{ver:-1,dist:new Float32Array(N),prev:new Int32Array(N)};}

function newGame(ci,mode){
  const city=CITIES[ci];
  genTerrain(city,water,mount,tree);
  roadN.fill(0);railN.fill(0);roadE.fill(0);railE.fill(0);fixedT.fill(0);xing.fill(0);wreck.fill(0);barAnim.fill(0);bmap.fill(null);ctrl.fill(0);
  G={ci,city,mode,time:0,week:1,weekT:0,score:0,accidents:0,over:false,paused:false,modal:false,speed:1,tool:'road',
     res:{road:36,rail:18,bridge:3,loco:1,truck:1,barrier:1,overpass:0,lights:1,round:0},
     houses:[],shops:[],depots:[],cars:[],trains:[],fx:[],pending:[],lock:new Set(),occ:new Set(),
     bounds:{x0:15,x1:32,y0:9,y1:20},houseT:6,shopT:60,colorsUsed:1,dispT:0,trainT:0,
     roadVer:1,railVer:1,degVer:-1,staticDirty:true,failShop:null,hints:{},
     segMap:new Map(),startMap:new Map(),occ2:new Map(),nodeState:new Map()};
  const s=tryShop(0,{x:23,y:14,min:0,max:3})||tryShop(0,null);
  for(let i=0;i<3;i++) tryHouse(0,s);
  tryDepot({x:s.x+1,y:s.y+1,min:6,max:9});
  if(mode==='demo'){ G.res={road:999,rail:999,bridge:99,loco:2,truck:1,barrier:9,overpass:0,lights:0,round:0}; demoConnectAll(); }
  fitCam(true);
  staticKey='';
}
''')

# ---------------------------------------------------------------- GRAF
section('GRAF: noduri si muchii (8 directii)', r'''
function addEdge(E,a,d){E[a]|=1<<d;E[a+DOFF[d]]|=1<<((d+4)&7);}
function bumpVer(kind){if(kind==='road')G.roadVer++;else G.railVer++;G.staticDirty=true;}
function flashRes(k){
  const el={bridge:$('sBridge'),road:$('tRoad'),rail:$('tRail'),barrier:$('tBarrier'),overpass:$('tOverpass'),lights:$('tLights'),round:$('tRound')}[k];
  if(!el)return; el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash');
}
function roadDeg(t){const m=roadE[t];if(!m)return 0;let n=0;for(let d=0;d<8;d++)if((m&(1<<d))&&roadN[t+DOFF[d]])n++;return n;}
function isInter(t){
  if(G.degVer!==G.roadVer){for(let i=0;i<N;i++)degArr[i]=roadN[i]?roadDeg(i):0;G.degVer=G.roadVer;}
  return degArr[t]>=3;
}
function validateCtrl(){
  for(let t=0;t<N;t++){
    if(!ctrl[t]) continue;
    if(!roadN[t]||railN[t]||roadDeg(t)<3){ if(ctrl[t]===1)G.res.lights++; else G.res.round++; ctrl[t]=0; G.nodeState.delete(t); G.staticDirty=true; }
  }
}
function placeNode(t,kind,free){
  const NN=kind==='road'?roadN:railN;
  if(NN[t]) return true;
  if(bmap[t]||mount[t]||!inBt(t)) return false;
  if(kind==='rail'&&ctrl[t]) return false;
  if(!free){
    if(water[t]){ if(G.res.bridge<=0){flashRes('bridge');hint('hNoBridge',4);return false;} G.res.bridge--; }
    else { if(G.res[kind]<=0){flashRes(kind);hint('hNoRes',4,{r:tr(kind==='road'?'rnRoad':'rnRail')});return false;} G.res[kind]--; }
  }
  NN[t]=1; tree[t]=0; bumpVer(kind);
  if(roadN[t]&&railN[t]) newCrossing(t);
  sfx('build');
  return true;
}
function newCrossing(t){
  xing[t]=0;
  if(G.mode==='demo'){xing[t]=1;}
  else if(G.res.barrier>0){G.res.barrier--;xing[t]=1;}
  else hint('hUnguarded',7);
}
function diagBlocked(a,d){
  if(!(d&1)) return false;
  const x=a%W,y=(a/W)|0,dx=DX[d],dy=DY[d];
  const s1=idx(x+dx,y), s2=idx(x,y+dy), b=a+DOFF[d];
  if(water[s1]&&water[s2]&&!(water[a]&&water[b])) return true;
  if(mount[s1]&&mount[s2]) return true;
  if(bmap[s1]&&bmap[s2]) return true;
  const od=DLUT[(dy+1)*3+(-dx)+1];
  return ((roadE[s1]|railE[s1])&(1<<od))!==0;
}
function connect(a,b,kind,free){
  const d=dirIdx(a,b); if(d<0) return false;
  const E=kind==='road'?roadE:railE, NN=kind==='road'?roadN:railN;
  if(E[a]&(1<<d)) return true;
  if(bmap[b]) return false;
  if((kind==='road'?railE:roadE)[a]&(1<<d)){hint('hParallel',3,null,true);return false;}
  if(!NN[a]&&!placeNode(a,kind,free)) return false;
  if(diagBlocked(a,d)){hint('hDiag',3);return false;}
  if(!placeNode(b,kind,free)) return false;
  addEdge(E,a,d); bumpVer(kind);
  if(kind==='road'&&(roadDeg(a)>=3||roadDeg(b)>=3)) hint('hInter',9);
  return true;
}
function eraseTile(t){
  if(!inGrid(t%W,(t/W)|0)) return;
  const wasX=roadN[t]&&railN[t];
  let did=false;
  for(const kind of ['road','rail']){
    const NN=kind==='road'?roadN:railN, E=kind==='road'?roadE:railE, bit=kind==='road'?1:2;
    if(!NN[t]) continue;
    const fixed=fixedT[t]&bit;
    for(let d=0;d<8;d++){
      if(!(E[t]&(1<<d))) continue;
      const n=t+DOFF[d];
      if(fixed&&bmap[n]) continue;
      E[n]&=~(1<<((d+4)&7)); E[t]&=~(1<<d); did=true;
    }
    if(!fixed){ NN[t]=0; E[t]=0; if(water[t])G.res.bridge++; else G.res[kind]++; did=true; }
    bumpVer(kind);
  }
  if(wasX&&!(roadN[t]&&railN[t])){ if(xing[t]===1)G.res.barrier++; else if(xing[t]===2)G.res.overpass++; xing[t]=0; }
  if(did){ validateCtrl(); sfx('erase'); }
}
function applySpecial(t,tool){
  if(tool==='barrier'||tool==='overpass'){
    if(!(roadN[t]&&railN[t])){hint('hPick',3,null,true);return;}
    if(tool==='barrier'){
      if(xing[t]!==0) return;
      if(G.res.barrier<=0){flashRes('barrier');hint('hNoBarrier',3,null,true);return;}
      G.res.barrier--; xing[t]=1; sfx('place');
    } else {
      if(xing[t]===2) return;
      if(G.res.overpass<=0){flashRes('overpass');hint('hNoOverpass',3,null,true);return;}
      if(xing[t]===1) G.res.barrier++;
      G.res.overpass--; xing[t]=2; G.staticDirty=true; sfx('place');
    }
    return;
  }
  if(!roadN[t]||railN[t]||roadDeg(t)<3){hint('hPickInter',3,null,true);return;}
  const want=tool==='lights'?1:2;
  if(ctrl[t]===want) return;
  if(G.res[tool]<=0){flashRes(tool);hint(tool==='lights'?'hNoLights':'hNoRound',3,null,true);return;}
  if(ctrl[t]===1)G.res.lights++; else if(ctrl[t]===2)G.res.round++;
  G.res[tool]--; ctrl[t]=want; G.nodeState.delete(t); G.staticDirty=true; sfx('place');
}
''')

# ---------------------------------------------------------------- DIJKSTRA extras
rep('''function depotRail(d){if(d.rc.ver!==G.railVer){dijkstra(d.cells,railE,railN,d.rc.dist,d.rc.prev,-1);d.rc.ver=G.railVer;}return d.rc;}''',
'''function depotRail(d){if(d.rc.ver!==G.railVer){dijkstra(d.cells,railE,railN,d.rc.dist,d.rc.prev,-1);d.rc.ver=G.railVer;}return d.rc;}
function depotRoad(d){if(d.rrc.ver!==G.roadVer){dijkstra(d.cells,roadE,roadN,d.rrc.dist,d.rrc.prev,-1);d.rrc.ver=G.roadVer;}return d.rrc;}''')

# ---------------------------------------------------------------- CLADIRI
section('CLADIRI', r'''
function nearBig(x,y){
  for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){if(!inGrid(x+dx,y+dy))continue;const b=bmap[idx(x+dx,y+dy)];if(b&&b.type!=='house')return true;}
  return false;
}
function addHouse(x,y,color,d){
  const t=idx(x,y), h={type:'house',id:uid++,x,y,t,color,home:2,dir:d,born:G.time};
  bmap[t]=h; tree[t]=0; G.houses.push(h);
  const n=t+DOFF[d];
  if(!roadN[n]){roadN[n]=1;fixedT[n]|=1;tree[n]=0;}
  addEdge(roadE,t,d); bumpVer('road');
  return h;
}
function tryHouse(color,nearShop){
  const same=G.houses.filter(h=>h.color===color);
  const shops=nearShop?[nearShop]:G.shops.filter(s=>s.color===color);
  const b=G.bounds;
  for(let a=0;a<160;a++){
    let x,y;
    if(!nearShop&&same.length&&Math.random()<.7&&a<100){const h=pick(same);x=h.x+ri(-2,2);y=h.y+ri(-2,2);}
    else if(shops.length&&a<130){const s=pick(shops),ang=rnd(0,6.283),d=rnd(4.5,8.5)+s.level*.5;x=Math.round(s.x+s.w/2-.5+Math.cos(ang)*d);y=Math.round(s.y+s.h/2-.5+Math.sin(ang)*d);}
    else {x=ri(b.x0,b.x1);y=ri(b.y0,b.y1);}
    if(!inB(x,y)) continue;
    const t=idx(x,y);
    if(!tileFree(t)||nearBig(x,y)) continue;
    let tgt=null,td=1e9; for(const s of shops){const dd=Math.hypot(s.x+1-x,s.y+1-y);if(dd<td){td=dd;tgt=s;}}
    let best=-1,bs=-1e9;
    for(const d of [0,2,4,6]){
      const nx=x+DX[d],ny=y+DY[d]; if(!inB(nx,ny)) continue;
      const n=idx(nx,ny);
      if(water[n]||mount[n]||bmap[n]||railN[n]||ctrl[n]) continue;
      let sc_=Math.random()*.6;
      if(tgt){const vx=tgt.x+1-(x+.5),vy=tgt.y+1-(y+.5),L=Math.hypot(vx,vy)||1;sc_+=(DX[d]*vx+DY[d]*vy)/L;}
      if(sc_>bs){bs=sc_;best=d;}
    }
    if(best<0) continue;
    return addHouse(x,y,color,best);
  }
  return null;
}
const SIDES=[
  {d:0,tiles:[[2,0],[2,1]],cells:[[1,0],[1,1]]},
  {d:2,tiles:[[0,2],[1,2]],cells:[[0,1],[1,1]]},
  {d:4,tiles:[[-1,0],[-1,1]],cells:[[0,0],[0,1]]},
  {d:6,tiles:[[0,-1],[1,-1]],cells:[[0,0],[1,0]]},
];
function areaOk(x,y){
  for(let yy=y-1;yy<=y+2;yy++)for(let xx=x-1;xx<=x+2;xx++){
    const inner=xx>=x&&xx<=x+1&&yy>=y&&yy<=y+1;
    if(inner){ if(!inB(xx,yy)||!tileFree(idx(xx,yy))) return false; }
    else if(inGrid(xx,yy)&&bmap[idx(xx,yy)]) return false;
  }
  return true;
}
function okDoor(x,y,kind){
  if(!inB(x,y)) return false;
  const t=idx(x,y);
  if(water[t]||mount[t]||bmap[t]||ctrl[t]) return false;
  return kind==='road'?!railN[t]:!roadN[t];
}
function findSide(x,y,order,kind){
  for(const S of order){
    const ks=Math.random()<.5?[0,1]:[1,0];
    for(const k of ks){const [ox,oy]=S.tiles[k];if(okDoor(x+ox,y+oy,kind))return {S,k};}
  }
  return null;
}
function sideOrder(x,y,rand){
  const b=G.bounds, cx=(b.x0+b.x1+1)/2, cy=(b.y0+b.y1+1)/2;
  return [...SIDES].map(S=>({S,v:DX[S.d]*(cx-(x+1))+DY[S.d]*(cy-(y+1))+Math.random()*rand})).sort((a,b)=>b.v-a.v).map(o=>o.S);
}
function placeSpot(near,a){
  const b=G.bounds;
  if(near&&a<160){const ang=rnd(0,6.283),d=rnd(near.min,near.max);return [Math.round(near.x+Math.cos(ang)*d),Math.round(near.y+Math.sin(ang)*d)];}
  return [ri(b.x0+1,b.x1-2),ri(b.y0+1,b.y1-2)];
}
function tooClose(x,y,a){return [...G.shops,...G.depots].some(o=>Math.hypot(o.x-x,o.y-y)<(a<300?6.5:4.5));}
function makeDoor(o,S,k,kind){
  const [ox_,oy_]=S.tiles[k], [cx_,cy_]=S.cells[k];
  const t=idx(o.x+ox_,o.y+oy_), E=kind==='road'?roadE:railE, NN=kind==='road'?roadN:railN, bit=kind==='road'?1:2;
  if(!NN[t]){NN[t]=1;fixedT[t]|=bit;} tree[t]=0;
  addEdge(E,idx(o.x+cx_,o.y+cy_),S.d); bumpVer(kind);
  return {d:S.d,cx:o.x+cx_,cy:o.y+cy_};
}
function tryShop(color,near){
  for(let a=0;a<420;a++){
    const [x,y]=placeSpot(near,a);
    if(!areaOk(x,y)||tooClose(x,y,a)) continue;
    const rd=findSide(x,y,sideOrder(x,y,4),'road'); if(!rd) continue;
    const opp=SIDES.find(S=>S.d===((rd.S.d+4)&7));
    const rl=findSide(x,y,[opp,...SIDES.filter(S=>S!==opp&&S!==rd.S)],'rail'); if(!rl) continue;
    const s={type:'shop',id:uid++,x,y,w:2,h:2,color,cells:[idx(x,y),idx(x+1,y),idx(x,y+1),idx(x+1,y+1)],
      level:1,served:0,demand:0,pinAcc:.3,stock:6,max:LV[1].max,inCars:0,inGoods:0,timer:0,born:G.time,grown:-99,rc:mkCache()};
    for(const c of s.cells){bmap[c]=s;tree[c]=0;}
    s.door=makeDoor(s,rd.S,rd.k,'road'); s.dock=makeDoor(s,rl.S,rl.k,'rail'); s.door2=null;
    G.shops.push(s);
    return s;
  }
  return null;
}
function tryDepot(near){
  for(let a=0;a<420;a++){
    const [x,y]=placeSpot(near,a);
    if(!areaOk(x,y)||tooClose(x,y,a)) continue;
    const rl=findSide(x,y,sideOrder(x,y,2),'rail'); if(!rl) continue;
    const opp=SIDES.find(S=>S.d===((rl.S.d+4)&7));
    const rd=findSide(x,y,[opp,...SIDES.filter(S=>S!==opp&&S!==rl.S)],'road'); if(!rd) continue;
    const d={type:'depot',id:uid++,x,y,w:2,h:2,cells:[idx(x,y),idx(x+1,y),idx(x,y+1),idx(x+1,y+1)],born:G.time,rc:mkCache(),rrc:mkCache()};
    for(const c of d.cells){bmap[c]=d;tree[c]=0;}
    d.dock=makeDoor(d,rl.S,rl.k,'rail'); d.door=makeDoor(d,rd.S,rd.k,'road');
    G.depots.push(d);
    return d;
  }
  return null;
}
// magazinul creste: nivel nou, stoc mai mare, se extinde daca are loc, la nivelul 3 primeste a doua intrare
function growShop(s){
  s.level++; s.max=LV[s.level].max; s.grown=G.time;
  const opts=[];
  for(const d of [0,2,4,6]){
    if(d===s.door.d||d===s.dock.d||(s.door2&&d===s.door2.d)) continue;
    if((d===0||d===4)&&s.w>=3) continue;
    if((d===2||d===6)&&s.h>=3) continue;
    const cells=[];
    if(d===0) for(let y=s.y;y<s.y+s.h;y++) cells.push([s.x+s.w,y]);
    if(d===4) for(let y=s.y;y<s.y+s.h;y++) cells.push([s.x-1,y]);
    if(d===2) for(let x=s.x;x<s.x+s.w;x++) cells.push([x,s.y+s.h]);
    if(d===6) for(let x=s.x;x<s.x+s.w;x++) cells.push([x,s.y-1]);
    if(cells.every(([x,y])=>inB(x,y)&&tileFree(idx(x,y)))) opts.push({d,cells});
  }
  if(opts.length){
    const o=pick(opts);
    for(const [x,y] of o.cells){const t=idx(x,y);bmap[t]=s;tree[t]=0;s.cells.push(t);}
    if(o.d===0) s.w++; else if(o.d===4){s.x--;s.w++;} else if(o.d===2) s.h++; else {s.y--;s.h++;}
  }
  if(s.level===3&&!s.door2){
    const cand=[];
    for(const c of s.cells){const x=c%W,y=(c/W)|0;
      for(const d of [0,2,4,6]){const nx=x+DX[d],ny=y+DY[d]; if(!inGrid(nx,ny)||bmap[idx(nx,ny)]===s) continue;
        if(d===s.dock.d||!okDoor(nx,ny,'road')) continue; if(Math.abs(nx-(s.door.cx+DX[s.door.d]))+Math.abs(ny-(s.door.cy+DY[s.door.d]))<2) continue;
        cand.push({c,d,n:idx(nx,ny),pref:d!==s.door.d?1:0});}}
    cand.sort((a,b)=>b.pref-a.pref||Math.random()-.5);
    if(cand.length){const o=cand[0]; if(!roadN[o.n]){roadN[o.n]=1;fixedT[o.n]|=1;} tree[o.n]=0; addEdge(roadE,o.c,o.d); s.door2={d:o.d,cx:o.c%W,cy:(o.c/W)|0};}
  }
  bumpVer('road'); bumpVer('rail');
  fx(s.x+s.w/2,s.y-.2,tr('levelFx',{n:s.level}),COLORS[s.color].d);
  sfx('grow'); hint('hGrow',6);
}

// demo / teste: legare automata
function autoRoute(from,goals,kind){
  const prev=new Int32Array(N).fill(-2), q=[from]; prev[from]=-1;
  const NN=kind==='road'?roadN:railN, OTHER=kind==='road'?railN:roadN, OE=kind==='road'?railE:roadE;
  for(let h=0;h<q.length;h++){
    const t=q[h];
    for(let d=0;d<8;d++){
      const x=t%W+DX[d],y=((t/W)|0)+DY[d]; if(!inB(x,y)) continue;
      const n=idx(x,y); if(prev[n]!==-2) continue;
      if(diagBlocked(t,d)) continue;
      if(OE[t]&(1<<d)) continue;
      if(goals.has(n)){prev[n]=t;const p=[];let k=n;while(k!==-1){p.push(k);k=prev[k];}return p.reverse();}
      if(bmap[n]||mount[n]||(fixedT[n]&&!NN[n])) continue;
      if(OTHER[n]&&kind==='rail') continue;
      if(ctrl[n]&&kind==='rail') continue;
      prev[n]=t; q.push(n);
    }
  }
  return null;
}
function doorTiles(o,kind){const E=kind==='road'?roadE:railE, out=new Set();for(const c of o.cells)for(let d=0;d<8;d++)if(E[c]&(1<<d))out.add(c+DOFF[d]);return out;}
function autoConnect(from,goals,kind,free){const p=autoRoute(from,goals,kind);if(!p)return false;for(let i=0;i+1<p.length;i++)if(!connect(p[i],p[i+1],kind,free))return false;return true;}
function demoConnectAll(){
  for(const s of G.shops) for(const d of G.depots) autoConnect([...doorTiles(d,'rail')][0],doorTiles(s,'rail'),'rail',true);
  for(const d of G.depots) for(const s of G.shops) autoConnect([...doorTiles(d,'road')][0],doorTiles(s,'road'),'road',true);
  for(const s of G.shops){
    const goal=doorTiles(s,'road');
    for(const h of G.houses) if(h.color===s.color) autoConnect(h.t+DOFF[h.dir],goal,'road',true);
  }
}
''')

# ---------------------------------------------------------------- MASINI
section('MASINI', r'''
function dispatch(){
  for(const s of G.shops){
    let guard=4;
    while(guard--&&s.demand-s.inCars>0&&s.stock-s.inCars>0){
      const rc=shopRoad(s); let best=null,bd=Infinity;
      for(const h of G.houses) if(h.color===s.color&&h.home>0&&rc.dist[h.t]<bd){bd=rc.dist[h.t];best=h;}
      if(!best) break;
      const p=trace(rc.prev,best.t);
      best.home--; s.inCars++;
      const c=newVehicle('car'); Object.assign(c,{h:best,s,path:p,color:s.color,x:best.x+.5,y:best.y+.5,ang:best.dir*Math.PI/4,phase:'go'});
      c.L=DLEN[dirIdx(p[0],p[1])];
      G.cars.push(c);
    }
  }
}
function newVehicle(kind){return {id:uid++,kind,h:null,s:null,depot:null,path:null,i:0,t:0,L:1,phase:'idle',wait:0,cool:0,blk:0,xw:0,ghost:false,color:0,x:0,y:0,ang:0,cargo:0,dead:false};}
// camioane
function findTruckJob(d){
  const rc=depotRoad(d); let best=null,bd=Infinity;
  for(const s of G.shops){ if(s.stock+s.inGoods>s.max-2) continue; for(const c of s.cells) if(rc.dist[c]<bd){bd=rc.dist[c];best=c;} }
  return best===null?null:trace(rc.prev,best).reverse();
}
function startTruck(c,p){
  const s=bmap[p[p.length-1]]; c.s=s; c.cargo=TRUCK_CARGO; s.inGoods+=TRUCK_CARGO;
  c.path=p; c.i=0; c.t=0; c.phase='go'; c.L=DLEN[dirIdx(p[0],p[1])]; c.ghost=false; c.blk=0; c.xw=0;
  const [x,y]=cxy(p[0]); c.x=x; c.y=y; c.ang=dirIdx(p[0],p[1])*Math.PI/4;
}
function truckHome(c,cool){ if(c.phase==='go'&&c.s) c.s.inGoods-=c.cargo; c.cargo=0; c.phase='idle'; c.cool=cool||1; c.path=null; }
function cancelCar(c){
  if(c.kind==='truck'){truckHome(c);return;}
  if(c.phase==='go') c.s.inCars--; c.h.home++; c.dead=true;
}
function rerouteCar(c){
  const a=c.path[c.i];
  if(c.phase==='go'){const rc=shopRoad(c.s);if(rc.dist[a]<Infinity){c.path=trace(rc.prev,a);c.i=0;return true;}return false;}
  if(c.kind==='truck'){const rc=depotRoad(c.depot);if(rc.dist[a]<Infinity){c.path=trace(rc.prev,a);c.i=0;return true;}return false;}
  if(dijkstra([c.h.t],roadE,roadN,tmpDist,tmpPrev,a)>=0){c.path=trace(tmpPrev,a);c.i=0;return true;}
  return false;
}
function carBlocked(c){
  const a=c.path[c.i], b=c.path[c.i+1];
  const same=G.segMap.get(a*N+b);
  if(same) for(const o of same){ if(o===c) continue; const g=GAP+(o.kind==='truck'?.14:0); if((o.t>c.t||(o.t===c.t&&o.id<c.id))&&(o.t-c.t)*c.L<g) return true; }
  const nx=G.startMap.get(b);
  if(nx) for(const o of nx){ const g=GAP+(o.kind==='truck'?.14:0); if(o.path[o.i+1]!==a&&o.t*o.L+(1-c.t)*c.L<g) return true; }
  return false;
}
function carMustStop(b){
  if(wreck[b]>0) return true;
  if(!(roadN[b]&&railN[b])) return false;
  const x=xing[b]; if(x===2) return false;
  return x===1?G.lock.has(b):G.occ.has(b);
}
// --- intersectii
const NO_OCC=[];
function nodeSt(t){let ns=G.nodeState.get(t);if(!ns){ns={phase:-1,t:0,waits:[0,0,0,0],prio:-1};G.nodeState.set(t,ns);}return ns;}
function occAdd(n,c,app){let l=G.occ2.get(n);if(!l){l=[];G.occ2.set(n,l);}l.push({c,app,grp:dirIdx(n,app)&3});}
function zoneF(n){return ctrl[n]===1?1:ctrl[n]===2?.82:.6;}
function canEnter(c,b,a){
  const occ=G.occ2.get(b)||NO_OCC, k=ctrl[b];
  if(c.xw>6) return true;
  if(k===2){ let n=0; for(const o of occ) if(o.c!==c) n++; return n<3; }
  const ns=nodeSt(b), g=dirIdx(b,a)&3;
  if(k===1){
    if(ns.phase!==g){ ns.waits[g]++; return false; }
    for(const o of occ) if(o.c!==c&&o.grp!==g) return false;
    return true;
  }
  if(ns.prio!==-1&&ns.prio!==a){ return false; }
  for(const o of occ) if(o.c!==c&&o.app!==a){ if(c.xw>1.1&&ns.prio===-1) ns.prio=a; return false; }
  if(ns.prio===a) ns.prio=-1;
  return true;
}
function lightsUpdate(dt){
  for(const [t,ns] of G.nodeState){
    if(ctrl[t]!==1) continue;
    const m=roadE[t]; let groups=0;
    for(let d=0;d<8;d++) if((m&(1<<d))&&roadN[t+DOFF[d]]) groups|=1<<(d&3);
    if(ns.phase<0||!(groups&(1<<ns.phase))){ for(let g=0;g<4;g++) if(groups&(1<<g)){ns.phase=g;break;} ns.t=2.6; }
    ns.t-=dt;
    if(ns.t<=0){ for(let k=1;k<4;k++){const g=(ns.phase+k)&3; if((groups&(1<<g))&&ns.waits[g]>0){ns.phase=g;ns.t=2.6;break;}} }
    ns.waits[0]=ns.waits[1]=ns.waits[2]=ns.waits[3]=0;
  }
}
function stepCar(c,dt){
  if(c.phase==='idle'){ c.cool-=dt; if(c.cool<=0){ c.cool=.8; const p=findTruckJob(c.depot); if(p) startTruck(c,p); } return; }
  if(c.phase==='park'){
    c.wait-=dt; if(c.wait>0) return;
    if(c.kind==='truck'){
      const rc=depotRoad(c.depot), end=c.path[c.path.length-1];
      if(rc.dist[end]===Infinity){truckHome(c);return;}
      c.path=trace(rc.prev,end);
    } else {
      const rc=shopRoad(c.s);
      if(rc.dist[c.h.t]===Infinity){c.h.home++;c.dead=true;return;}
      c.path=trace(rc.prev,c.h.t).reverse();
    }
    c.i=0; c.t=0; c.phase='back'; c.ghost=false; c.blk=0; c.xw=0;
    c.L=DLEN[dirIdx(c.path[0],c.path[1])];
    return;
  }
  const a=c.path[c.i], b=c.path[c.i+1];
  let sp=c.kind==='truck'?TRUCK_SPEED:CAR_SPEED;
  const rem=(1-c.t)*c.L, bInter=isInter(b);
  if(bInter&&rem<RZ) sp*=zoneF(b); else if(c.i>0&&c.t*c.L<RZ&&isInter(a)) sp*=zoneF(a);
  let nt=c.t+sp*dt/c.L;
  if(!c.ghost&&carBlocked(c)){ c.blk+=dt; nt=c.t; if(c.blk>5) c.ghost=true; } else c.blk=0;
  const cap=1-.6/c.L;
  if(c.t<=cap&&carMustStop(b)) nt=Math.min(nt,cap);
  if(bInter&&rem>=RZ-1e-6){
    const sl=1-RZ/c.L;
    if(nt>sl){
      if(canEnter(c,b,a)){ c.xw=0; occAdd(b,c,a); }
      else { nt=Math.max(c.t,sl); c.xw+=dt; }
    }
  }
  c.t=nt;
  if(c.t>=1){
    c.t-=1; c.i++; c.ghost=false; c.blk=0;
    if(c.i>=c.path.length-1){ c.t=0; arriveCar(c); return; }
    let d=dirIdx(c.path[c.i],c.path[c.i+1]);
    if(!(roadE[c.path[c.i]]&(1<<d))){ if(!rerouteCar(c)){cancelCar(c);return;} d=dirIdx(c.path[0],c.path[1]); c.t=0; }
    c.t=c.t*c.L/DLEN[d]; c.L=DLEN[d];
  }
  carPos(c);
}
const RR=.4;
function carPos(c){
  const a=c.path[c.i], b=c.path[c.i+1];
  const ax=a%W+.5, ay=((a/W)|0)+.5, bx=b%W+.5, by=((b/W)|0)+.5;
  const dx=bx-ax, dy=by-ay, l=Math.hypot(dx,dy)||1;
  let x=ax+dx*c.t-dy/l*.17, y=ay+dy*c.t+dx/l*.17, ta=Math.atan2(dy,dx);
  const rem=(1-c.t)*c.L, done=c.t*c.L;
  let arc=null;
  if(ctrl[b]===2&&rem<RZ&&c.i+2<c.path.length) arc=[b,a,c.path[c.i+2],(RZ-rem)/RZ*.5];
  else if(ctrl[a]===2&&done<RZ&&c.i>0) arc=[a,c.path[c.i-1],b,.5+done/RZ*.5];
  if(arc){
    const [n,p,q,u]=arc, nx=n%W+.5, ny=((n/W)|0)+.5;
    const ti=Math.atan2(((p/W)|0)+.5-ny,p%W+.5-nx), to=Math.atan2(((q/W)|0)+.5-ny,q%W+.5-nx);
    let dl=to-ti; while(dl>=0) dl-=6.2832; while(dl<-6.2832) dl+=6.2832; if(dl>-.01) dl=-6.2832;
    const th=ti+dl*u; x=nx+Math.cos(th)*RR; y=ny+Math.sin(th)*RR; ta=th-Math.PI/2;
  }
  c.x=x; c.y=y;
  let d=ta-c.ang; while(d>Math.PI)d-=6.2832; while(d<-Math.PI)d+=6.2832; c.ang+=d*(arc?.6:.3);
}
function arriveCar(c){
  if(c.kind==='truck'){
    if(c.phase==='go'){
      const s=c.s; s.stock=Math.min(s.max,s.stock+c.cargo); s.inGoods-=c.cargo;
      fx(s.x+s.w/2,s.y+s.h+.1,'+'+c.cargo,INK); sfx('goods');
      c.cargo=0; c.phase='park'; c.wait=.6;
    } else { c.phase='idle'; c.cool=.4; c.path=null; }
    return;
  }
  if(c.phase==='go'){
    const s=c.s; s.stock--; s.demand--; s.inCars--; s.served++; G.score++;
    fx(s.x+s.w/2,s.y+.1,'+1',COLORS[s.color].d); sfx('deliver',s.color);
    if(s.level<3&&s.served>=LV[s.level+1].need) growShop(s);
    c.phase='park'; c.wait=.6;
  } else { c.h.home++; c.dead=true; }
}
function carNear(n,r2){
  const bx=n%W+.5, by=((n/W)|0)+.5;
  for(const c of G.cars){ if(c.dead||c.phase==='park'||c.phase==='idle') continue; const dx=c.x-bx,dy=c.y-by; if(dx*dx+dy*dy<r2) return c; }
  return null;
}
''')

# ---------------------------------------------------------------- TRENURI (partial replacements)
rep('''  for(const s of G.shops){ if(s.stock+s.inGoods>s.max-3) continue; for(const c of s.cells) if(rc.dist[c]<bd){bd=rc.dist[c];best=c;} }''',
    '''  for(const s of G.shops){ if(s.stock+s.inGoods>s.max-4) continue; for(const c of s.cells) if(rc.dist[c]<bd){bd=rc.dist[c];best=c;} }''')
rep('''  const s=bmap[p[p.length-1]]; tr.shop=s; tr.cargo=CARGO; s.inGoods+=CARGO;''','''  const s=bmap[p[p.length-1]]; tr.shop=s; tr.cargo=TRAIN_CARGO; s.inGoods+=TRAIN_CARGO;''')
rep('''    fx(s.x+1,s.y+2.1,'+'+tr.cargo,INK); sfx('goods');''','''    fx(s.x+s.w/2,s.y+s.h+.1,'+'+tr.cargo,INK); sfx('goods');''')
rep('''          if(c.dead||c.phase==='park') continue;
          const dx=c.x-px,dy=c.y-py;''','''          if(c.dead||c.phase==='park'||c.phase==='idle') continue;
          const dx=c.x-px,dy=c.y-py;''')
rep('''  wreck[n]=9; G.accidents++;
  if(c.phase==='go') c.s.inCars--;
  c.dead=true; G.pending.push({t:12,h:c.h});''','''  wreck[n]=9; G.accidents++;
  if(c.kind==='truck'){ truckHome(c,12); }
  else { if(c.phase==='go') c.s.inCars--; c.dead=true; G.pending.push({t:12,h:c.h}); }''')

# ---------------------------------------------------------------- SIMULARE
section('SIMULARE', r'''
function houseCount(c){let n=0;for(const h of G.houses)if(h.color===c)n++;return n;}
function weekMul(){return Math.min(1.9,1+.06*(G.week-1));}
function step(dt){
  G.time+=dt;
  computeLocks();
  lightsUpdate(dt);
  // cerere
  const demo=G.mode==='demo';
  for(const s of G.shops){
    const hc=houseCount(s.color), L=LV[s.level];
    if(hc>0){
      const rate=BASE_DEMAND*L.mul*weekMul()*G.city.diff*Math.min(1,hc/(2+s.level))*(demo?.55:1);
      s.pinAcc+=dt*rate;
      if(s.pinAcc>=1){s.pinAcc-=1;if(s.demand<L.pins)s.demand++;}
    }
    if(s.demand>=L.over) s.timer+=dt/26; else s.timer=Math.max(0,s.timer-dt/12);
    if(s.timer>=1){ if(demo){s.timer=0;s.demand=2;} else {gameOver(s);return;} }
    if(s.stock<=3&&!G.trains.length&&!G.cars.some(c=>c.kind==='truck')) hint('hSupply',9);
  }
  G.dispT-=dt; if(G.dispT<=0){G.dispT=.3;dispatch();}
  // index segmente + ocupare intersectii
  G.segMap.clear(); G.startMap.clear(); G.occ2.clear();
  for(const c of G.cars){
    if(c.dead||c.phase==='park'||c.phase==='idle') continue;
    const a=c.path[c.i], b=c.path[c.i+1], k=a*N+b;
    let l=G.segMap.get(k); if(!l){l=[];G.segMap.set(k,l);} l.push(c);
    let m=G.startMap.get(a); if(!m){m=[];G.startMap.set(a,m);} m.push(c);
    if((1-c.t)*c.L<RZ-1e-6&&isInter(b)) occAdd(b,c,a);
    else if(c.i>0&&c.t*c.L<RZ&&isInter(a)) occAdd(a,c,c.path[c.i-1]);
  }
  for(const c of G.cars) if(!c.dead) stepCar(c,dt);
  // vehicule noi
  G.trainT-=dt;
  if(G.trainT<=0){
    G.trainT=.5;
    for(const d of G.depots){
      if(G.res.loco<=0) break;
      if(G.trains.some(t=>t.depot===d&&t.phase==='idle')) continue;
      const p=findJob(d);
      if(p){ G.res.loco--; const t={id:uid++,depot:d,shop:null,path:null,cum:null,s:0,seg:0,phase:'idle',cargo:0,wait:0,cool:0,held:-1}; G.trains.push(t); startJob(t,p); }
    }
    for(const d of G.depots){
      if(G.res.truck<=0) break;
      if(G.cars.some(c=>c.kind==='truck'&&c.depot===d&&c.phase==='idle')) continue;
      const p=findTruckJob(d);
      if(p){ G.res.truck--; const c=newVehicle('truck'); c.depot=d; G.cars.push(c); startTruck(c,p); }
    }
    if(G.res.truck>0&&G.time>25&&!G.cars.some(c=>c.kind==='truck')) hint('hTruck',8);
  }
  for(const t of G.trains) stepTrain(t,dt);
  checkAccidents();
  if(G.cars.some(c=>c.dead)) G.cars=G.cars.filter(c=>!c.dead);
  // epave & masini pierdute
  for(let i=0;i<N;i++) if(wreck[i]>0){ wreck[i]-=dt; if(wreck[i]<0) wreck[i]=0; }
  if(G.pending.length){ for(const p of G.pending){p.t-=dt;if(p.t<=0)p.h.home++;} G.pending=G.pending.filter(p=>p.t>0); }
  // aparitii
  G.houseT-=dt;
  if(G.houseT<=0){
    G.houseT=Math.max(2.6,7-.3*G.week)*rnd(.7,1.3);
    let cap=2; for(const s of G.shops) cap+=3+2*s.level;
    if(demo) cap=Math.min(cap,G.shops.length*5);
    if(G.houses.length<cap) spawnHouse();
  }
  if(!demo){
    G.shopT-=dt; if(G.shopT<=0){G.shopT=Math.max(38,72-2.5*G.week)*rnd(.85,1.15);spawnShop();}
    G.weekT+=dt; if(G.weekT>=WEEK_LEN) endWeek();
  }
}
function spawnHouse(){
  const colors=[...new Set(G.shops.map(s=>s.color))];
  let best=null,bw=-1;
  for(const c of colors){let want=0;for(const s of G.shops)if(s.color===c)want+=3+2*s.level;const w=want/(houseCount(c)+1)*rnd(.6,1.4);if(w>bw){bw=w;best=c;}}
  if(best===null) return;
  const h=tryHouse(best,null);
  if(h){ sfx('spawn'); if(G.mode==='demo') demoConnectAll(); }
}
function spawnShop(){
  let color;
  const canNew=G.colorsUsed<COLORS.length&&G.week>=2;
  if(canNew&&(G.shops.length>=G.colorsUsed*1.5||Math.random()<.45)) color=G.colorsUsed; else color=ri(0,G.colorsUsed-1);
  const s=tryShop(color,null); if(!s) return;
  if(color===G.colorsUsed){G.colorsUsed++;for(let i=0;i<2;i++)tryHouse(color,s);}
  sfx('spawn');
}
''')

# ---------------------------------------------------------------- SAPTAMANI
rep('''  overpass:'<svg viewBox="0 0 24 24"><path d="M12 3v18" stroke="#22262D" stroke-width="2.4" stroke-linecap="round"/><rect x="3" y="8" width="18" height="8" rx="2" fill="#8A949A"/><rect x="3" y="9.5" width="18" height="5" fill="#fff"/></svg>',
};''','''  overpass:'<svg viewBox="0 0 24 24"><path d="M12 3v18" stroke="#22262D" stroke-width="2.4" stroke-linecap="round"/><rect x="3" y="8" width="18" height="8" rx="2" fill="#8A949A"/><rect x="3" y="9.5" width="18" height="5" fill="#fff"/></svg>',
  truck:'<svg viewBox="0 0 24 24"><rect x="2" y="6" width="13" height="10" rx="1.5" fill="#C99B5B"/><path d="M15 9h4l3 3.5V16h-7z" fill="#22262D"/><circle cx="6.5" cy="18" r="1.8" fill="#22262D"/><circle cx="17.5" cy="18" r="1.8" fill="#22262D"/></svg>',
  lights:'<svg viewBox="0 0 24 24"><rect x="8" y="2.5" width="8" height="15" rx="3" fill="#22262D"/><circle cx="12" cy="6.8" r="2.1" fill="#E8604C"/><circle cx="12" cy="13.2" r="2.1" fill="#3DBE6A"/><path d="M12 17.5V22" stroke="#22262D" stroke-width="2" stroke-linecap="round"/></svg>',
  round:'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5" fill="none" stroke="#B9BEB2" stroke-width="5.5"/><circle cx="12" cy="12" r="8.5" fill="none" stroke="#fff" stroke-width="3.6"/><circle cx="12" cy="12" r="3.4" fill="#8DB07E"/></svg>',
};''')
rep('''const UPG=[
  {k:'loco',t:'uLoco',d:'uLocoD',f:()=>G.res.loco++},
  {k:'rail',t:'uRail',d:'uRailD',f:()=>G.res.rail+=20},
  {k:'bridge',t:'uBridge',d:'uBridgeD',f:()=>G.res.bridge+=2},
  {k:'road',t:'uRoad',d:'uRoadD',f:()=>G.res.road+=30},
  {k:'barrier',t:'uBarrier',d:'uBarrierD',f:()=>G.res.barrier+=2},
  {k:'overpass',t:'uOverpass',d:'uOverpassD',f:()=>G.res.overpass+=1},
];''','''const UPG=[
  {k:'loco',t:'uLoco',d:'uLocoD',w:3,f:()=>G.res.loco++},
  {k:'truck',t:'uTruck',d:'uTruckD',w:3,f:()=>G.res.truck++},
  {k:'rail',t:'uRail',d:'uRailD',w:2,f:()=>G.res.rail+=20},
  {k:'road',t:'uRoad',d:'uRoadD',w:2,f:()=>G.res.road+=30},
  {k:'bridge',t:'uBridge',d:'uBridgeD',w:1.3,f:()=>G.res.bridge+=2},
  {k:'barrier',t:'uBarrier',d:'uBarrierD',w:1.5,f:()=>G.res.barrier+=2},
  {k:'overpass',t:'uOverpass',d:'uOverpassD',w:1,f:()=>G.res.overpass+=1},
  {k:'lights',t:'uLights',d:'uLightsD',w:2,f:()=>G.res.lights+=2},
  {k:'round',t:'uRound',d:'uRoundD',w:1.3,f:()=>G.res.round+=1},
];
function pickUpgrades(n){
  const pool=[...UPG], out=[];
  while(out.length<n&&pool.length){let sum=0;for(const u of pool)sum+=u.w;let r=Math.random()*sum;let i=0;for(;i<pool.length-1;i++){r-=pool[i].w;if(r<=0)break;}out.push(pool.splice(i,1)[0]);}
  return out;
}''')
rep('''  let opts=[...UPG].sort(()=>Math.random()-.5).slice(0,2);
  if(G.week===2&&!opts.some(o=>o.k==='loco')) opts[0]=UPG[0];
  if(G.week===3&&!opts.some(o=>o.k==='barrier'||o.k==='overpass')) opts[1]=UPG[4];''','''  let opts=pickUpgrades(3);
  if(G.week===2&&!opts.some(o=>o.k==='loco'||o.k==='truck')) opts[0]=UPG[Math.random()<.5?0:1];
  if(G.week===3&&!opts.some(o=>o.k==='lights'||o.k==='round')) opts[2]=UPG[7];
  G.lastOpts=opts;''')
rep('''.choices{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:6px 0 4px;}''','''.choices{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:6px 0 4px;}
#scrWeek .card{max-width:620px;}''')

open(P,'w').write(s)
print('patched part 1')
