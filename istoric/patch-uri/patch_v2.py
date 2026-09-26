# Reconstruieste jocul pe aspectul v1.2 (panou de depozit, fara Flota) + reparatie atribuire,
# nume nou, bonusuri, suport telefon, pasaj pe distante mari.
SRC='/home/claude/joc/src/game_v12.html'
P='/home/claude/joc/src/game.html'
s=open(SRC).read()
def rep(a,b,count=1):
    global s
    assert a in s, 'missing: '+a[:110]
    s=s.replace(a,b,count)
def between(a,b,new):
    global s
    i=s.index(a); j=s.index(b,i)
    s=s[:i]+new+s[j:]

# =================================================================== A. panoul de depozit: atribuire care merge
between('function removeTrain(d){','const serves=(d,s)=>',r'''function vehicles(){const out=[];for(const t of G.trains)if(!t.gone)out.push(t);for(const c of G.cars)if(c.kind==='truck'&&!c.dead)out.push(c);return out;}
// scoate imediat un vehicul (devine liber); marfa din drum se anuleaza
function toInventory(v){
  if(v.kind==='truck'){ if(v.phase==='go'&&v.s) v.s.inGoods-=v.cargo; v.cargo=0; v.dead=true; G.res.truck++; }
  else { if(v.phase==='go'&&v.shop) v.shop.inGoods-=v.cargo; v.cargo=0; v.gone=true; G.trains=G.trains.filter(t=>!t.gone); G.res.loco++; }
}
// muta un vehicul pe alt depozit: daca asteapta, trece imediat; daca e pe drum, isi termina livrarea si merge la noul depozit
function moveVehicle(v,d){
  if(!v||v.depot===d) return;
  v.depot=d; v.retire=false;
  if(v.kind==='truck'){
    if(v.phase==='back'){ v.t=0; if(rerouteCar(v)){ v.L=segLen(v.path[0],v.path[1]); } else truckHome(v); }
  } else if(v.phase==='back'){ if(!rerouteTrain(v)) toDepot(v); }
}
const isTrain=v=>v.kind!=='truck';
function otherHas(kind,d){ return vehicles().some(v=>(kind==='train')===isTrain(v)&&v.depot!==d); }
// "+" fara vehicule libere: ia unul de la alt depozit (intai unul care asteapta)
function pullVehicle(kind,d){
  const c=vehicles().filter(v=>(kind==='train')===isTrain(v)&&v.depot!==d);
  if(!c.length) return false;
  c.sort((a,b)=>(a.phase==='idle'?0:1)-(b.phase==='idle'?0:1));
  moveVehicle(c[0],d); return true;
}
function removeTrain(d){ const v=G.trains.find(t=>t.depot===d&&!t.gone&&t.phase==='idle')||G.trains.find(t=>t.depot===d&&!t.gone); if(v) toInventory(v); }
function addTruck(d){ if(G.res.truck<=0) return false; G.res.truck--; const c=newVehicle('truck'); c.depot=d; G.cars.push(c); return true; }
function removeTruck(d){ const v=G.cars.find(c=>c.kind==='truck'&&c.depot===d&&!c.dead&&c.phase==='idle')||G.cars.find(c=>c.kind==='truck'&&c.depot===d&&!c.dead); if(v) toInventory(v); }
''')
rep("function depotTrains(d){let n=0;for(const t of G.trains)if(t.depot===d&&!t.retire&&!t.gone)n++;return n;}","function depotTrains(d){let n=0;for(const t of G.trains)if(t.depot===d&&!t.gone)n++;return n;}")
rep("function depotTrucks(d){let n=0;for(const c of G.cars)if(c.kind==='truck'&&c.depot===d&&!c.retire&&!c.dead)n++;return n;}","function depotTrucks(d){let n=0;for(const c of G.cars)if(c.kind==='truck'&&c.depot===d&&!c.dead)n++;return n;}")
rep("  $('dpTp').disabled=G.res.loco<=0; $('dpTm').disabled=nt<=0;","  $('dpTp').disabled=G.res.loco<=0&&!otherHas('train',d); $('dpTm').disabled=nt<=0;")
rep("  $('dpKp').disabled=G.res.truck<=0; $('dpKm').disabled=nk<=0;","  $('dpKp').disabled=G.res.truck<=0&&!otherHas('truck',d); $('dpKm').disabled=nk<=0;")
rep("$('dpTp').onclick=()=>{ if(dpSel&&addTrain(dpSel)){sfx('place');updateHud(true);} refreshDepot(); };","$('dpTp').onclick=()=>{ if(dpSel&&(addTrain(dpSel)||pullVehicle('train',dpSel))){sfx('place');updateHud(true);} refreshDepot(); };")
rep("$('dpKp').onclick=()=>{ if(dpSel&&addTruck(dpSel)){sfx('place');updateHud(true);} refreshDepot(); };","$('dpKp').onclick=()=>{ if(dpSel&&(addTruck(dpSel)||pullVehicle('truck',dpSel))){sfx('place');updateHud(true);} refreshDepot(); };")
rep("if(o.k==='loco'||o.k==='truck'){G.hints.hAssign=0;hint('hAssign',8);}};","if(o.k==='loco'||o.k==='truck'){G.hints.hAssign=0;hint('hAssign',8);if(G.depots.length)openDepot(G.depots[0]);}};")
rep('''function placeDepotPanel(){
  const p=$('depotPanel'), d=dpSel, pw=p.offsetWidth||260, ph=p.offsetHeight||250;''','''function placeDepotPanel(){
  const p=$('depotPanel'), d=dpSel, pw=p.offsetWidth||260, ph=p.offsetHeight||250;
  if(vw<=760||vh<=520){ if(p.style.left){ p.style.left=''; p.style.top=''; } return; }''')

# =================================================================== B. nume, bonusuri, versiune
rep("<title>Tiny Junctions</title>","<title>Sine si Sosele</title>")
rep('<h1 class="logo">Tiny<span>Junctions</span></h1>','<h1 class="logo">Sine si<span>Sosele</span></h1>')
rep("{k:'bridge',t:'uBridge',d:'uBridgeD',w:1.3,f:()=>G.res.bridge+=2}","{k:'bridge',t:'uBridge',d:'uBridgeD',w:1.3,f:()=>G.res.bridge+=7}")
rep("{k:'lights',t:'uLights',d:'uLightsD',w:2,f:()=>G.res.lights+=2}","{k:'lights',t:'uLights',d:'uLightsD',w:2,f:()=>G.res.lights+=5}")
rep("{k:'round',t:'uRound',d:'uRoundD',w:1.3,f:()=>G.res.round+=1}","{k:'round',t:'uRound',d:'uRoundD',w:1.3,f:()=>G.res.round+=3}")
rep("uBridgeD:'+2 poduri peste apa'","uBridgeD:'+7 bucati de pod peste apa'")
rep("uLightsD:'+2 semafoare pentru intersectii'","uLightsD:'+5 semafoare pentru intersectii'")
rep("uRoundD:'Intersectie fluida pentru multe masini'","uRoundD:'+3 sensuri giratorii'")
rep("uBridgeD:'+2 bridges over water'","uBridgeD:'+7 bridge pieces over water'")
rep("uLightsD:'+2 lights for junctions'","uLightsD:'+5 traffic lights for junctions'")
rep("uRoundD:'Smooth junction for many cars'","uRoundD:'+3 roundabouts'")
rep("version:'Versiunea 1.2'","version:'Versiunea 1.0'"); rep("version:'Version 1.2'","version:'Version 1.0'")

# =================================================================== C. telefon
exec(open('/home/claude/joc/src/patch_v2_mobile.py').read())
# =================================================================== E. pasaj pe distante mari
exec(open('/home/claude/joc/src/patch_v2_via.py').read())

open(P,'w').write(s)
print('ok v2')
