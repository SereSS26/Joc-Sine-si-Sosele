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

# ------------------------------------------------ versiunea 1.0
rep("version:'Versiunea 1.4'","version:'Versiunea 1.0'")
rep("version:'Version 1.4'","version:'Version 1.0'")

# ------------------------------------------------ HTML: buton viteza (telefon), buton reincadrare, text atingere
rep('''          <button data-sp="3" data-tt="speedTip">''','''          <button class="spCycle" id="spCycle" data-tt="speedTip">1&times;</button>
          <button data-sp="3" data-tt="speedTip">''')
rep('''    <div id="toast"></div>''','''    <div id="toast"></div>
    <button class="round" id="btnFit" hidden data-tt="fitTip"><svg viewBox="0 0 24 24"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>''')
rep('''      <div class="keys" data-t="keys"></div>''','''      <div class="keys" data-t="keys"></div>
      <div class="keys touchOnly" data-t="touchKeys"></div>''')

# ------------------------------------------------ CSS pentru telefon
rep('''@media (prefers-reduced-motion:reduce)''','''/* ---------- telefon ---------- */
html,body{overscroll-behavior:none;-webkit-tap-highlight-color:transparent;-webkit-touch-callout:none;}
button,.tool,.stat,.choice,.cityCard{touch-action:manipulation;}
.speed .spCycle{display:none;font-weight:800;font-size:13px;}
.touchOnly{display:none;}
body.touch .touchOnly{display:block;}
#btnFit{position:absolute;right:calc(16px + env(safe-area-inset-right,0px));bottom:calc(env(safe-area-inset-bottom,0px) + 84px);}
@media (max-width:760px), (max-height:520px){
  #hudTop{top:calc(env(safe-area-inset-top,0px) + 8px);left:calc(8px + env(safe-area-inset-left,0px));right:calc(8px + env(safe-area-inset-right,0px));gap:6px;}
  .city{font-size:20px;} .weekRow{font-size:10px;margin-top:3px;gap:6px;} .weekBar{width:56px;}
  .scoreBox b{font-size:30px;} .scoreBox span{font-size:9px;letter-spacing:.1em;}
  .hudRight{gap:6px;}
  .speed{padding:3px;border-radius:12px;} .speed button{width:36px;height:36px;}
  .speed button[data-sp="1"],.speed button[data-sp="2"],.speed button[data-sp="3"]{display:none;}
  .speed .spCycle{display:grid;}
  .round{width:42px;height:42px;border-radius:12px;}
  .fleetBtn{padding:0;width:42px;justify-content:center;} .fleetBtn span{display:none;}
  #toolbar{left:calc(8px + env(safe-area-inset-left,0px));right:calc(8px + env(safe-area-inset-right,0px));transform:none;bottom:calc(env(safe-area-inset-bottom,0px) + 8px);overflow-x:auto;overscroll-behavior-x:contain;justify-content:flex-start;padding:5px;gap:2px;border-radius:16px;scrollbar-width:none;}
  #toolbar::-webkit-scrollbar{display:none;}
  .tool{padding:6px 9px;min-height:44px;flex:none;gap:5px;} .tool .lbl,.tool kbd,.stat small{display:none;}
  .tool svg{width:24px;height:24px;} .tool .cnt{min-width:12px;font-size:13px;}
  .stat{flex:none;padding:0 6px;font-size:13px;gap:4px;} .stat.click{padding:6px;} .sep{margin:0 3px;flex:none;}
  #toast{bottom:calc(env(safe-area-inset-bottom,0px) + 72px);font-size:13px;padding:9px 12px;max-width:calc(100% - 24px);}
  .fleet{left:calc(8px + env(safe-area-inset-left,0px));right:calc(8px + env(safe-area-inset-right,0px));width:auto;max-width:none;top:auto;bottom:calc(env(safe-area-inset-bottom,0px) + 70px);max-height:58%;}
  .dbtn{min-width:34px;height:34px;}
  #btnFit{bottom:calc(env(safe-area-inset-bottom,0px) + 72px);right:calc(8px + env(safe-area-inset-right,0px));}
  .screen{padding:10px;}
  .card{padding:20px;border-radius:20px;max-height:calc(100% - 20px);}
  h2{font-size:32px;}
  .cities{grid-template-columns:repeat(2,1fr);gap:8px;margin:12px 0 14px;}
  .choices{grid-template-columns:repeat(2,1fr);gap:8px;}
  .choice{padding:12px;gap:4px;} .choice svg{width:28px;height:28px;} .choice b{font-size:15px;} .choice span{font-size:12px;}
  .stats{gap:18px;} .stats b{font-size:36px;}
  #scrMain{background:rgba(207,212,200,.8);}
  .mainPanel{padding:0 24px;gap:16px;max-width:none;}
}
@media (max-height:520px){
  .logo{font-size:52px;} .tagline{font-size:14px;margin-top:-6px;}
  .mainPanel{gap:12px;} .btn{padding:10px 14px;font-size:15px;}
  .mainPanel{flex-direction:column;justify-content:center;}
}
@media (prefers-reduced-motion:reduce)''')

# ------------------------------------------------ TEXTE
rep("  hFleet:'Sfat: apasa Flota (V) sau da click pe un depozit, tren sau camion ca sa alegi de ce depozit apartine.',","""  hFleet:'Sfat: apasa Flota (V) sau da click pe un depozit, tren sau camion ca sa alegi de ce depozit apartine.',
  fitTip:'Arata toata harta', touchKeys:'Pe telefon: trage cu un deget ca sa construiesti. Cu doua degete apropii, departezi si muti harta. Pentru stergere foloseste unealta Sterge.',
  hTouch:'Trage cu un deget ca sa construiesti. Cu doua degete apropii si muti harta.', hRotate:'Sfat: intoarce telefonul orizontal ca sa ai o harta mai mare.',""")
rep("  hFleet:'Tip: press Fleet (V) or click a depot, train or truck to choose which depot it belongs to.',","""  hFleet:'Tip: press Fleet (V) or click a depot, train or truck to choose which depot it belongs to.',
  fitTip:'Show the whole map', touchKeys:'On a phone: drag with one finger to build. Use two fingers to zoom and move the map. Use the Erase tool to remove things.',
  hTouch:'Drag with one finger to build. Use two fingers to zoom and move the map.', hRotate:'Tip: turn your phone sideways for a bigger map.',""")

# ------------------------------------------------ CAMERA: zoom si mutare
rep('''function camTarget(){
  const b=G.bounds, bw=b.x1-b.x0+2, bh=b.y1-b.y0+2;
  const top=vw<640?100:92, bot=vw<640?96:92;''','''function camTarget(){
  const f=camFit();
  if(G.mode!=='play'||G.capsule||!(G.zoom>1)) return f;
  return {cx:f.cx+(G.pan?G.pan.x:0),cy:f.cy+(G.pan?G.pan.y:0),ts:f.ts*G.zoom,oy:f.oy};
}
function maxZoom(){ return Math.max(1.5,Math.min(6,62/camFit().ts)); }
function clampPan(){
  if(!G.pan) return; const b=G.bounds, f=camFit();
  G.pan.x=clamp(f.cx+G.pan.x,b.x0,b.x1+1)-f.cx; G.pan.y=clamp(f.cy+G.pan.y,b.y0,b.y1+1)-f.cy;
}
// zoom pastrand punctul (wx,wy) al hartii sub punctul (sx,sy) al ecranului
function setZoomAt(z,sx,sy,wx,wy){
  if(!G||G.mode!=='play') return;
  z=clamp(z,1,maxZoom());
  if(z<=1.02){ G.zoom=1; G.pan=null; Object.assign(cam,camFit()); updateFitBtn(); return; }
  G.zoom=z; const f=camFit(), ts=f.ts*z;
  G.pan={x:wx-(sx-vw/2)/ts-f.cx, y:wy-(sy-vh/2-f.oy)/ts-f.cy}; clampPan();
  Object.assign(cam,camTarget()); updateFitBtn();
}
function resetZoom(){ if(!G) return; G.zoom=1; G.pan=null; updateFitBtn(); }
function updateFitBtn(){ const b=$('btnFit'); if(b) b.hidden=!(G&&G.mode==='play'&&G.zoom>1); }
function camFit(){
  const b=G.bounds, bw=b.x1-b.x0+2, bh=b.y1-b.y0+2;
  const compact=vw<=760||vh<=520;
  const top=compact?58:92, bot=compact?64:92, side=compact?8:24;''')
rep('''  const ts=Math.min((vw-24)/bw,(vh-top-bot)/bh);
  return {cx:(b.x0+b.x1+1)/2,cy:(b.y0+b.y1+1)/2,ts,oy:(top-bot)/2};''','''  const ts=Math.min((vw-side)/bw,(vh-top-bot)/bh);
  return {cx:(b.x0+b.x1+1)/2,cy:(b.y0+b.y1+1)/2,ts,oy:(top-bot)/2};''')

# ------------------------------------------------ CONTROL: atingere, doua degete, rotita
between('cv.addEventListener(\'pointerdown\',e=>{\n  if(!canPlay()) return;','function registerTile(t){',r'''function beginAction(e){
  const [fx_,fy_]=ptrTile(e), x=Math.floor(fx_), y=Math.floor(fy_);
  if(!inGrid(x,y)) return;
  const t=idx(x,y);
  const erase=e.button===2||G.tool==='erase';
  const bb=bmap[t];
  if(!erase){ const hv=vehicleAt(fx_,fy_,e.pointerType==='touch'?.62:.34); if(hv){ openFleet({veh:hv}); return; } }
  if(bb&&bb.type==='depot'&&!erase){ openFleet({depot:bb}); return; }
  if(!erase&&(G.tool==='barrier'||G.tool==='overpass'||G.tool==='lights'||G.tool==='round')){ applySpecial(t,G.tool); updateHud(); return; }
  if(e.pointerType!=='touch'){ try{cv.setPointerCapture(e.pointerId);}catch(_){} }
  drag={erase,kind:G.tool==='rail'?'rail':'road',last:-1,id:e.pointerId};
  registerTile(t);
  updateHud();
}
function moveAction(e){
  const [fx_,fy_]=ptrTile(e), x=Math.floor(fx_), y=Math.floor(fy_);
  if(!drag||!inGrid(x,y)) return;
  const t=idx(x,y);
  if(t===drag.last) return;
  const near=Math.hypot(fx_-x-.5,fy_-y-.5)<(e.pointerType==='touch'?.47:.44);
  const adj=drag.last>=0&&dirIdx(drag.last,t)>=0;
  if(near||!adj||drag.last<0) registerTile(t);
  updateHud();
}
// atingere: un deget construieste (dupa o mica miscare sau pauza), doua degete = zoom si mutare
const touches=new Map(); let pend=null, pinch=null, pinchLock=false;
function startPinch(){
  const [a,b]=[...touches.values()], r=cv.getBoundingClientRect();
  const mx=(a.x+b.x)/2-r.left, my=(a.y+b.y)/2-r.top, w=s2t(mx,my);
  pinch={d0:Math.hypot(a.x-b.x,a.y-b.y)||1,z0:G.zoom||1,wx:w[0],wy:w[1]};
}
function updatePinch(){
  const [a,b]=[...touches.values()], r=cv.getBoundingClientRect();
  const d=Math.hypot(a.x-b.x,a.y-b.y)||1;
  setZoomAt(pinch.z0*d/pinch.d0,(a.x+b.x)/2-r.left,(a.y+b.y)/2-r.top,pinch.wx,pinch.wy);
}
cv.addEventListener('pointerdown',e=>{
  if(e.pointerType==='touch'){
    touches.set(e.pointerId,{x:e.clientX,y:e.clientY});
    try{cv.setPointerCapture(e.pointerId);}catch(_){}
    if(!G||G.mode!=='play'||G.over||G.modal) return;
    if(touches.size>=2){ pend=null; drag=null; pinchLock=true; if(touches.size===2) startPinch(); return; }
    if(pinchLock||!canPlay()) return;
    pend={e:{clientX:e.clientX,clientY:e.clientY,pointerId:e.pointerId,button:0,pointerType:'touch'},t0:performance.now()};
    return;
  }
  if(!canPlay()) return;
  beginAction(e);
});
cv.addEventListener('pointermove',e=>{
  if(e.pointerType==='touch'){
    if(!touches.has(e.pointerId)) return;
    touches.set(e.pointerId,{x:e.clientX,y:e.clientY});
    if(pinch&&touches.size>=2){ updatePinch(); return; }
    if(pend&&pend.e.pointerId===e.pointerId){
      const dx=e.clientX-pend.e.clientX, dy=e.clientY-pend.e.clientY;
      if(dx*dx+dy*dy<64&&performance.now()-pend.t0<110) return;
      const p0=pend.e; pend=null; if(canPlay()) beginAction(p0);
    }
    if(drag&&drag.id===e.pointerId) moveAction(e);
    return;
  }
  const [fx_,fy_]=ptrTile(e), x=Math.floor(fx_), y=Math.floor(fy_);
  hover=[x,y];
  if(!drag&&G&&G.mode==='play'){ const b=inGrid(x,y)&&bmap[idx(x,y)]; const cur=(b&&b.type==='depot')||vehicleAt(fx_,fy_)?'pointer':'crosshair'; if(cv.style.cursor!==cur) cv.style.cursor=cur; }
  moveAction(e);
});
function endPointer(e){
  if(e.pointerType==='touch'){
    touches.delete(e.pointerId);
    if(pinch&&touches.size<2) pinch=null;
    if(touches.size===0) pinchLock=false;
    if(pend&&pend.e.pointerId===e.pointerId){ const p0=pend.e; pend=null; if(canPlay()) beginAction(p0); drag=null; return; }
    if(drag&&drag.id===e.pointerId) drag=null;
    return;
  }
  drag=null;
}
cv.addEventListener('pointerup',endPointer); cv.addEventListener('pointercancel',endPointer);
cv.addEventListener('pointerleave',e=>{ if(e.pointerType!=='touch') hover=null; });
cv.addEventListener('contextmenu',e=>e.preventDefault());
cv.addEventListener('wheel',e=>{
  if(!G||G.mode!=='play'||G.over||G.modal) return;
  e.preventDefault();
  const r=cv.getBoundingClientRect(), sx=e.clientX-r.left, sy=e.clientY-r.top, w=s2t(sx,sy);
  setZoomAt((G.zoom||1)*(e.deltaY<0?1.15:1/1.15),sx,sy,w[0],w[1]);
},{passive:false});
$('btnFit').onclick=resetZoom;
''')
rep("function vehicleAt(fx,fy){\n  let best=null,bd=.34*.34;","function vehicleAt(fx,fy,rad){\n  let best=null,bd=(rad||.34)*(rad||.34);")

# viteza: buton ciclic pe telefon
rep('''  for(const b of document.querySelectorAll('#speedCtl button')) b.classList.toggle('on',(+b.dataset.sp)===(G.paused?0:G.speed));
}
for(const b of document.querySelectorAll('#speedCtl button')) b.addEventListener('click',()=>setSpeed(+b.dataset.sp));''','''  for(const b of document.querySelectorAll('#speedCtl button[data-sp]')) b.classList.toggle('on',(+b.dataset.sp)===(G.paused?0:G.speed));
  const sc_=$('spCycle'); sc_.textContent=G.speed+'×'; sc_.classList.toggle('on',!G.paused);
}
for(const b of document.querySelectorAll('#speedCtl button[data-sp]')) b.addEventListener('click',()=>setSpeed(+b.dataset.sp));
$('spCycle').addEventListener('click',()=>{ if(!G) return; setSpeed(G.paused?G.speed:(G.speed%3)+1); });''')

# pornire oras: zoom resetat, indicii pentru telefon
rep('''  setTool('road'); G.paused=false; G.speed=1; setSpeed(1);''','''  setTool('road'); G.paused=false; G.speed=1; setSpeed(1); G.zoom=1; G.pan=null; updateFitBtn();''')
rep('''  hint('hStart',9);''','''  hint('hStart',9);
  if(IS_TOUCH){ setTimeout(()=>{ if(G&&G.mode==='play'&&!G.over){ G.hints.hTouch=0; hint(vh>vw?'hRotate':'hTouch',7); } },9500); }''')
rep('''function toMenu(){''','''const IS_TOUCH=matchMedia('(pointer:coarse)').matches||('ontouchstart' in window);
if(IS_TOUCH) document.body.classList.add('touch');
function toMenu(){''')
rep('''  closeFleet();
  newGame(''','''  closeFleet(); updateFitBtn();
  newGame(''') if "  closeFleet();\n  newGame(" in s else None
rep('''  $('hud').hidden=true; show('scrMain');''','''  $('hud').hidden=true; show('scrMain'); updateFitBtn();''')

# rezolutie: pe ecrane foarte dense limitam la 2x
open(P,'w').write(s)
print('ok mobile')
