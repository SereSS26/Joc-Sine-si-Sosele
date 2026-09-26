// Sine si Sosele - test pe telefoane emulate (iPhone 13, Pixel 7), vertical si orizontal, cu atingeri reale; capturi in unelte/capturi
// Ruleaza din folderul proiectului: node unelte/test-telefon.js
const _path=require('path'),_fs=require('fs'),{pathToFileURL:_url}=require('url');
const ROOT=_path.resolve(__dirname,'..'), CAP=_path.join(__dirname,'capturi'); _fs.mkdirSync(CAP,{recursive:true});
const GAME=_url(_path.join(ROOT,'index.html')).href, GAME_DESKTOP=_url(_path.join(ROOT,'game','index.html')).href;
const { chromium, devices } = require('playwright');
const DEV=process.argv[2]||'iPhone 13', TAG=process.argv[3]||'p';
(async()=>{
 const b=await chromium.launch();
 const ctx=await b.newContext({...devices[DEV]});
 const p=await ctx.newPage(); const cdp=await ctx.newCDPSession(p);
 const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 const vp=p.viewportSize(); console.log(DEV,'viewport',JSON.stringify(vp));
 await p.goto(GAME); await p.waitForTimeout(1500);
 await p.screenshot({path:_path.join(CAP,`${TAG}_1menu.png`)});
 await p.tap('#mPlay'); await p.waitForTimeout(300);
 await p.screenshot({path:_path.join(CAP,`${TAG}_2cities.png`)});
 await p.tap('.cityCard'); await p.waitForTimeout(800);
 const touchClass=await p.evaluate(()=>document.body.classList.contains('touch'));
 // traseu cu degetul: de la iesirea unei case la intrarea magazinului
 const route=await p.evaluate(()=>{const T=window.__TJ,G=T.G,W=T.W;const h=G.houses[0],s=G.shops[0];
   const door=h.t+[1,W+1,W,W-1,-1,-W-1,-W,-W+1][h.dir];
   const path=T.autoRoute(door,T.doorTiles(s,'road'),'road');
   return path.map(t=>T.t2s(t%W+.5,Math.floor(t/W)+.5));});
 const touch=(type,pts)=>cdp.send('Input.dispatchTouchEvent',{type,touchPoints:pts.map((q,i)=>({x:q[0],y:q[1],id:i}))});
 await touch('touchStart',[route[0]]);
 for(let i=1;i<route.length;i++){ const [ax,ay]=route[i-1],[bx,by]=route[i]; for(let k=1;k<=4;k++){ await touch('touchMove',[[ax+(bx-ax)*k/4,ay+(by-ay)*k/4]]); await p.waitForTimeout(12);} }
 await touch('touchEnd',[]);
 await p.waitForTimeout(200);
 const conn=await p.evaluate(()=>{const T=window.__TJ,G=T.G;const s=G.shops[0],h=G.houses[0];return {connected:T.shopRoad(s).dist[h.t]<Infinity,road:G.res.road,tiles:route=null};});
 console.log('finger road: route tiles',route.length,'connected',conn.connected,'road left',conn.road,'touch class',touchClass);
 // doua degete: zoom
 const cx=vp.width/2, cy=vp.height/2;
 await touch('touchStart',[[cx-30,cy],[cx+30,cy]]);
 for(let k=1;k<=10;k++){ await touch('touchMove',[[cx-30-k*12,cy],[cx+30+k*12,cy]]); await p.waitForTimeout(16); }
 // mutare cu doua degete
 for(let k=1;k<=6;k++){ await touch('touchMove',[[cx-150+k*10,cy+k*6],[cx+150+k*10,cy+k*6]]); await p.waitForTimeout(16); }
 await touch('touchEnd',[]);
 await p.waitForTimeout(300);
 const z=await p.evaluate(()=>({zoom:window.__TJ.G.zoom,roadAfterPinch:window.__TJ.G.res.road,fitBtn:!document.getElementById('btnFit').hidden}));
 console.log('pinch zoom',JSON.stringify(z),'(road must not change during pinch)');
 await p.screenshot({path:_path.join(CAP,`${TAG}_3zoom.png`)});
 // butonul de reincadrare
 await p.tap('#btnFit'); await p.waitForTimeout(400);
 console.log('fit button -> zoom',await p.evaluate(()=>window.__TJ.G.zoom));
 // atingere pe depozit
 const dp=await p.evaluate(()=>{const T=window.__TJ,d=T.G.depots[0];return T.t2s(d.x+1,d.y+1);});
 await touch('touchStart',[dp]); await p.waitForTimeout(40); await touch('touchEnd',[]); await p.waitForTimeout(300);
 console.log('tap depot -> depot panel open',await p.evaluate(()=>!document.getElementById('depotPanel').hidden));
 await p.screenshot({path:_path.join(CAP,`${TAG}_4fleet.png`)});
 await p.tap('#dpClose');
 // viteza ciclica
 const spVisible=await p.evaluate(()=>getComputedStyle(document.getElementById('spCycle')).display!=='none');
 if(spVisible){ await p.tap('#spCycle'); await p.waitForTimeout(100); }
 console.log('speed cycle visible',spVisible,'speed',await p.evaluate(()=>window.__TJ.G.speed));
 // unealta sterge din bara derulabila
 await p.evaluate(()=>document.getElementById('tErase').scrollIntoView());
 await p.tap('#tErase'); console.log('tool',await p.evaluate(()=>window.__TJ.G.tool));
 // saptamana: alegem un bonus cu atingere
 await p.evaluate(()=>window.__TJ.endWeek()); await p.waitForTimeout(300);
 await p.screenshot({path:_path.join(CAP,`${TAG}_5week.png`)});
 await p.tap('#choices .choice:nth-child(9)'); await p.waitForTimeout(200);
 console.log('week choice ok, round',await p.evaluate(()=>window.__TJ.G.res.round));
 // un minut de joc
 await p.evaluate(()=>{window.__TJ.setSpeed(1);}); await p.waitForTimeout(2500);
 await p.screenshot({path:_path.join(CAP,`${TAG}_6play.png`)});
 // cat de mare e un patratel pe ecran si daca bara de unelte incape
 console.log('layout',JSON.stringify(await p.evaluate(()=>{const tb=document.getElementById('toolbar').getBoundingClientRect();return {toolbarW:Math.round(tb.width),scrollW:document.getElementById('toolbar').scrollWidth,vw:innerWidth,vh:innerHeight};})));
 console.log('errors',errs);
 await b.close();
})();
