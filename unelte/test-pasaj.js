// Sine si Sosele - test pentru pasaj (drum suspendat peste pana la 10 patratele); salveaza capturi in unelte/capturi
// Ruleaza din folderul proiectului: node unelte/test-pasaj.js
const _path=require('path'),_fs=require('fs'),{pathToFileURL:_url}=require('url');
const ROOT=_path.resolve(__dirname,'..'), CAP=_path.join(__dirname,'capturi'); _fs.mkdirSync(CAP,{recursive:true});
const GAME=_url(_path.join(ROOT,'index.html')).href, GAME_DESKTOP=_url(_path.join(ROOT,'game','index.html')).href;
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto(GAME);await p.waitForTimeout(800);
await p.click('#mPlay'); await p.click('.cityCard'); await p.waitForTimeout(400);
const pick=await p.evaluate(()=>{const T=window.__TJ,G=T.G,W=T.W,b=G.bounds; G.res.overpass=2; G.res.road=60;
  for(let y=b.y0+2;y<=b.y1-2;y++){ let x0=-1,x1=-1; for(let x=b.x0;x<=b.x1;x++){ if(T.water[y*W+x]){ if(x0<0)x0=x; x1=x; } }
    if(x0<0) continue; const a=y*W+x0-2, c=y*W+x1+2; const r=T.viaCheck(a,c); if(r.ok) return {a,c,span:x1-x0+5,y,A:T.t2s(x0-2+.5,y+.5),C:T.t2s(x1+2+.5,y+.5)}; }
  return null;});
console.log('pasaj peste rau',JSON.stringify(pick&&{span:pick.span,row:pick.y}));
await p.keyboard.press('4');
console.log('hint:',await p.evaluate(()=>document.getElementById('toast').textContent));
await p.mouse.move(pick.A[0],pick.A[1]); await p.mouse.down();
for(let k=1;k<=10;k++){ await p.mouse.move(pick.A[0]+(pick.C[0]-pick.A[0])*k/10,pick.A[1]); await p.waitForTimeout(20); }
await p.screenshot({path:_path.join(CAP,'via_preview.png')});
await p.mouse.up(); await p.waitForTimeout(200);
const r1=await p.evaluate(()=>{const G=window.__TJ.G;return {vias:G.vias.length,overpass:G.res.overpass,road:G.res.road};});
console.log('dupa tragere',JSON.stringify(r1));
// o masina trece pe pasaj pana la magazin
const run=await p.evaluate(({a,c})=>{const T=window.__TJ,G=T.G,s=G.shops[0];
  T.autoConnect(a,T.doorTiles(s,'road'),'road',false);
  const rc=T.shopRoad(s); const reach=rc.dist[c]<Infinity; if(!reach) return {reach};
  // masina de proba care porneste din capatul de dincolo de rau
  const h=G.houses[0]; h.home--; s.inCars++; s.demand++; const path=[];
  let k=c; const prev=rc.prev; while(k!==-1){path.push(k);k=prev[k];}
  const car={id:777777,kind:'car',h,s,depot:null,path,i:0,t:0,L:Math.hypot(1,0),phase:'go',wait:0,cool:0,blk:0,xw:0,ghost:false,color:s.color,x:0,y:0,ang:0,cargo:0,dead:false};
  car.L=Math.hypot((path[1]%T.W)-(path[0]%T.W),Math.floor(path[1]/T.W)-Math.floor(path[0]/T.W));
  G.cars.push(car); const sc0=G.score; let air=0;
  for(let i=0;i<60*12;i++){ for(const x of G.shops) x.timer=0; if(G.modal){G.modal=false;} T.step(1/60); if(car.air) air++; if(car.phase!=='go') break; }
  return {reach,firstJump:path.length>1&&Math.abs(path[1]-path[0])>1,airSteps:air,delivered:G.score-sc0};},{a:pick.a,c:pick.c});
console.log('masina pe pasaj',JSON.stringify(run));
await p.waitForTimeout(300);
await p.screenshot({path:_path.join(CAP,'via.png')});
// stergerea unui capat scoate pasajul si il da inapoi
await p.keyboard.press('7'); await p.mouse.click(pick.C[0],pick.C[1]); await p.waitForTimeout(100);
console.log('dupa stergere',JSON.stringify(await p.evaluate(()=>({vias:window.__TJ.G.vias.length,overpass:window.__TJ.G.res.overpass}))));
// prea lung / nu in linie
console.log('prea lung ok?',await p.evaluate(({a})=>window.__TJ.viaCheck(a,a+12).reason,{a:pick.a}),'| nu in linie:',await p.evaluate(({a})=>window.__TJ.viaCheck(a,a+3+2*window.__TJ.W).reason,{a:pick.a}));
console.log('errors',errs); await b.close();})();
