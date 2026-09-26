P='/home/claude/joc/src/game.html'
s=open(P).read()
def rep(a,b,count=1):
    global s
    assert a in s, 'missing: '+a[:90]
    s=s.replace(a,b,count)

# ---- lumini: creeaza starea la plasare
rep('''  G.res[tool]--; ctrl[t]=want; G.nodeState.delete(t); G.staticDirty=true; sfx('place');
}''','''  G.res[tool]--; ctrl[t]=want; G.nodeState.delete(t); if(want===1) nodeSt(t); G.staticDirty=true; sfx('place');
}''')

# ---- static: sensuri giratorii
rep('''  strokeSegs(roadS,.7,city.edge); dots(roadN,.35,city.edge);
  strokeSegs(roadS,.56,ROAD); dots(roadN,.28,ROAD);''','''  const rounds=[]; for(let t=0;t<N;t++) if(ctrl[t]===2) rounds.push(cxy(t));
  const discs=(r,col)=>{c.fillStyle=col;c.beginPath();for(const [x,y] of rounds){c.moveTo(x+r,y);c.arc(x,y,r,0,6.283);}c.fill();};
  strokeSegs(roadS,.7,city.edge); dots(roadN,.35,city.edge); discs(.68,city.edge);
  strokeSegs(roadS,.56,ROAD); dots(roadN,.28,ROAD); discs(.61,ROAD);
  discs(.22,city.edge); discs(.19,ISLAND);
  c.fillStyle='rgba(255,255,255,.5)'; c.beginPath(); for(const [x,y] of rounds){c.moveTo(x+.07,y-.04);c.arc(x-.02,y-.04,.07,0,6.283);} c.fill();''')

# ---- render loop: umbre, vehicule, semafoare
rep('''  for(const d of G.depots) drawShadow(d,1.72);
  for(const s of G.shops) drawShadow(s,1.72);''','''  for(const d of G.depots) drawShadow(d);
  for(const s of G.shops) drawShadow(s);''')
rep('''  for(const c of G.cars) if(c.phase!=='park'&&!c.dead) drawCar(c);''','''  drawLights();
  for(const c of G.cars) if(c.phase!=='park'&&c.phase!=='idle'&&!c.dead) drawCar(c);''')

# ---- drawShadow / drawShop / drawDepot / drawCar
a=s.index('function drawShadow(o,sz)')
b=s.index('function drawHouse(h)')
s=s[:a]+'''function drawShadow(o){const k=pop((G.time-o.born)*2.5),w=(o.w-.28)*k,h=(o.h-.28)*k,cx=o.x+o.w/2,cy=o.y+o.h/2;ctx.fillStyle='rgba(50,56,46,.18)';rr(ctx,cx-w/2+.07,cy-h/2+.11,w,h,.28);ctx.fill();}
function notch(o,color,w){const px=o.cx+.5+DX[o.d]*.43, py=o.cy+.5+DY[o.d]*.43; ctx.fillStyle=color; ctx.save(); ctx.translate(px,py); ctx.rotate(o.d*Math.PI/4); rr(ctx,-.07,-w/2,.14,w,.04); ctx.fill(); ctx.restore();}
'''+s[b:]
a=s.index('function drawShop(s){')
b=s.index('function drawCar(c){')
s=s[:a]+r'''function drawShop(s){
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
  notch(s.door,'#fff',.34); if(s.door2) notch(s.door2,'#fff',.34); notch(s.dock,'#2B303A',.5);
  const cols=Math.max(4,Math.floor((sw-.36)/.25)), rows=Math.ceil(L.pins/cols);
  ctx.fillStyle=col.d; rr(ctx,left+.18,top+.18,sw-.36,.12+rows*.27,.12); ctx.fill();
  for(let i=0;i<s.demand;i++){
    const r=Math.floor(i/cols), c=i%cols, n=Math.min(cols,s.demand-r*cols);
    ctx.fillStyle=i>=L.over?'#FFD7CF':'#fff';
    ctx.beginPath(); ctx.arc(cx+(c-(n-1)/2)*.25,top+.18+.195+r*.27,.085,0,6.283); ctx.fill();
  }
  const bw=(sw-.4)/s.max;
  for(let i=0;i<s.max;i++){
    ctx.fillStyle=i<s.stock?'rgba(255,255,255,.95)':'rgba(0,0,0,.18)';
    rr(ctx,left+.2+i*bw,top+sh-.2-.32,bw-.04,.32,.035); ctx.fill();
  }
  if(s.stock===0&&Math.floor(G.time*3)%2===0){ctx.strokeStyle=INK;ctx.lineWidth=.07;rr(ctx,left-.06,top-.06,sw+.12,sh+.12,.32);ctx.stroke();}
}
function drawDepot(d){
  const k=pop((G.time-d.born)*2.5), cx=d.x+1, cy=d.y+1, sz=1.72*k;
  ctx.fillStyle=DEPOT; rr(ctx,cx-sz/2,cy-sz/2,sz,sz,.24*k); ctx.fill();
  if(k<1) return;
  notch(d.dock,'#2B303A',.5); notch(d.door,'#fff',.34);
  ctx.lineWidth=.035; ctx.strokeStyle=CRATE_D;
  for(const [ox_,oy_] of [[-.5,-.5],[.06,-.5],[-.5,.06],[.06,.06]]){
    ctx.fillStyle=CRATE; rr(ctx,cx+ox_,cy+oy_,.44,.44,.06); ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx+ox_+.07,cy+oy_+.07); ctx.lineTo(cx+ox_+.37,cy+oy_+.37); ctx.moveTo(cx+ox_+.37,cy+oy_+.07); ctx.lineTo(cx+ox_+.07,cy+oy_+.37); ctx.stroke();
  }
  const idleT=G.trains.filter(t=>t.depot===d&&t.phase==='idle').length, idleK=G.cars.filter(c=>c.kind==='truck'&&c.depot===d&&c.phase==='idle').length;
  ctx.fillStyle='#fff'; for(let i=0;i<idleT;i++){rr(ctx,cx-.78+i*.3,cy+.66,.24,.11,.04);ctx.fill();}
  ctx.fillStyle=CRATE; for(let i=0;i<idleK;i++){rr(ctx,cx+.6-i*.22,cy+.64,.16,.14,.03);ctx.fill();}
}
function drawLights(){
  for(const [t,ns] of G.nodeState){
    if(ctrl[t]!==1) continue;
    const [x,y]=cxy(t);
    for(let d=0;d<8;d++){
      if(!(roadE[t]&(1<<d))||!roadN[t+DOFF[d]]) continue;
      const ux=DX[d]/DLEN[d], uy=DY[d]/DLEN[d], px=x+ux*.52+uy*.36, py=y+uy*.52-ux*.36;
      ctx.fillStyle=INK; ctx.beginPath(); ctx.arc(px,py,.1,0,6.283); ctx.fill();
      ctx.fillStyle=(d&3)===ns.phase?GREEN:'#E8604C'; ctx.beginPath(); ctx.arc(px,py,.064,0,6.283); ctx.fill();
    }
  }
}
'''+s[b:]
a=s.index('function drawCar(c){')
b=s.index('function drawTrain(tr){')
s=s[:a]+r'''function drawCar(c){
  ctx.save(); ctx.translate(c.x,c.y); ctx.rotate(c.ang);
  if(c.kind==='truck'){
    ctx.fillStyle='rgba(40,44,40,.2)'; rr(ctx,-.25,-.1,.54,.28,.07); ctx.fill();
    ctx.fillStyle=c.phase==='go'?CRATE:'#A7ACB2'; rr(ctx,-.29,-.14,.4,.28,.05); ctx.fill();
    ctx.strokeStyle=c.phase==='go'?CRATE_D:'#80858C'; ctx.lineWidth=.03; ctx.stroke();
    ctx.fillStyle='#2B303A'; rr(ctx,.12,-.125,.17,.25,.05); ctx.fill();
    ctx.fillStyle='#5E6676'; rr(ctx,.2,-.09,.06,.18,.02); ctx.fill();
  } else {
    const col=COLORS[c.color];
    ctx.fillStyle='rgba(40,44,40,.2)'; rr(ctx,-.18,-.08,.4,.24,.08); ctx.fill();
    ctx.fillStyle=col.c; rr(ctx,-.2,-.115,.4,.23,.085); ctx.fill();
    ctx.fillStyle=col.l; rr(ctx,-.08,-.085,.15,.17,.04); ctx.fill();
  }
  ctx.restore();
}
'''+s[b:]

# ---- cursor: candidati pentru semafor / giratoriu
rep('''  if(tool==='barrier'||tool==='overpass'){
    const pulse=.3+.1*Math.sin(G.time*6);''','''  if(tool==='lights'||tool==='round'){
    const pulse=.3+.1*Math.sin(G.time*6), want=tool==='lights'?1:2;
    for(let q=0;q<N;q++) if(roadN[q]&&!railN[q]&&ctrl[q]!==want&&isInter(q)){const [px,py]=cxy(q);ctx.strokeStyle='rgba(34,38,45,.55)';ctx.lineWidth=.05;ctx.beginPath();ctx.arc(px,py,.55+pulse*.2,0,6.283);ctx.stroke();}
  }
  if(tool==='barrier'||tool==='overpass'){
    const pulse=.3+.1*Math.sin(G.time*6);''')

# ---- control
rep('''  if(!erase&&(G.tool==='barrier'||G.tool==='overpass')){ applySpecial(t,G.tool); updateHud(); return; }''',
    '''  if(!erase&&(G.tool==='barrier'||G.tool==='overpass'||G.tool==='lights'||G.tool==='round')){ applySpecial(t,G.tool); updateHud(); return; }''')
rep('''  const tools={'1':'road','2':'rail','3':'barrier','4':'overpass','5':'erase'};''','''  const tools={'1':'road','2':'rail','3':'barrier','4':'overpass','5':'lights','6':'round','7':'erase'};''')

# ---- interfata
rep('''  setTxt('cRoad',String(r.road)); setTxt('cRail',String(r.rail)); setTxt('cBarrier',String(r.barrier)); setTxt('cOverpass',String(r.overpass));
  setTxt('cBridge',String(r.bridge)); setTxt('cLoco',String(r.loco));''','''  setTxt('cRoad',String(r.road)); setTxt('cRail',String(r.rail)); setTxt('cBarrier',String(r.barrier)); setTxt('cOverpass',String(r.overpass));
  setTxt('cLights',String(r.lights)); setTxt('cRound',String(r.round));
  setTxt('cBridge',String(r.bridge)); setTxt('cLoco',String(r.loco)); setTxt('cTruck',String(r.truck));''')
rep('''  const tips={tRoad:'road',tRail:'rail',tBarrier:'barrier',tOverpass:'overpass',tErase:'erase'};''',
    '''  const tips={tRoad:'road',tRail:'rail',tBarrier:'barrier',tOverpass:'overpass',tLights:'lights',tRound:'round',tErase:'erase',sLoco:'trains',sTruck:'trucks',sBridge:'bridges'};''')

# ---- audio
rep('''    case 'week': [523,659,784].forEach((f,i)=>tone(f,.35,'sine',.05,i*.1)); break;''','''    case 'week': [523,659,784].forEach((f,i)=>tone(f,.35,'sine',.05,i*.1)); break;
    case 'grow': [392,523,659,784].forEach((f,i)=>tone(f,.3,'triangle',.045,i*.07)); break;''')

# ---- export pentru teste
rep('''window.__TJ={get G(){return G;},fitCam,''','''window.__TJ={get G(){return G;},fitCam,shopRoad,depotRoad,depotRail,isInter,roadDeg,ctrl,pickUpgrades,UPG,LV,growShop,''')

open(P,'w').write(s)
print('patched part 2')
