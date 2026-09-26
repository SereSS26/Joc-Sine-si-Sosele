// Sine si Sosele - test pentru intersectii: fara control, semafor, sens giratoriu; capturi in unelte/capturi
// Ruleaza din folderul proiectului: node unelte/test-intersectii.js
const _path=require('path'),_fs=require('fs'),{pathToFileURL:_url}=require('url');
const ROOT=_path.resolve(__dirname,'..'), CAP=_path.join(__dirname,'capturi'); _fs.mkdirSync(CAP,{recursive:true});
const GAME=_url(_path.join(ROOT,'index.html')).href, GAME_DESKTOP=_url(_path.join(ROOT,'game','index.html')).href;
const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1400,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.goto(GAME); await p.waitForTimeout(600);
 for(const mode of [2,1]){
  const r=await p.evaluate((mode)=>{
   const T=window.__TJ; let G,W; for(let tries=0;tries<20;tries++){ T.startCity(0); G=T.G; W=T.W; const idx=(x,y)=>y*W+x; let ok2=false; for(let y=14;y<16&&!ok2;y++)for(let x=20;x<28&&!ok2;x++){let ok=true;for(let k=-5;k<=5;k++)for(const [xx,yy] of [[x+k,y],[x,y+k]])if(!T.__free(yy*W+xx))ok=false; if(ok)ok2=true;} if(ok2)break; }
   G.res.road=999; G.res.lights=5; G.res.round=5; G.shops.forEach(s=>{s.pinAcc=-1e9;}); G.houseT=1e9; G.shopT=1e9;
   // gaseste un centru liber cu brate de 5
   const idx=(x,y)=>y*W+x; let C=null;
   for(let y=11;y<19&&!C;y++)for(let x=17;x<31&&!C;x++){let ok=true;for(let k=-5;k<=5;k++){for(const [xx,yy] of [[x+k,y],[x,y+k]]){const t=idx(xx,yy);if(!T.__free(t))ok=false;}}if(ok)C=[x,y];}
   if(!C) return 'no center';
   const [cx,cy]=C;
   for(let k=-5;k<5;k++){T.connect(idx(cx+k,cy),idx(cx+k+1,cy),'road',true);T.connect(idx(cx,cy+k),idx(cx,cy+k+1),'road',true);}
   const c0=idx(cx,cy);
   if(mode===1) T.applySpecial(c0,'lights'); if(mode===2) T.applySpecial(c0,'round');
   const ends=[idx(cx-5,cy),idx(cx+5,cy),idx(cx,cy-5),idx(cx,cy+5)];
   const line=(a,b)=>{const out=[];let x=a%W,y=(a/W)|0;const bx=b%W,by=(b/W)|0;out.push(a);while(x!==bx||y!==by){x+=Math.sign(bx-x);y+=Math.sign(by-y);out.push(idx(x,y));}return out;};
   let done=0, spawned=0, tt=0; window.__done=0;
   const dummy=()=>({home:0,t:-1});
   const T0=G.time;
   for(let i=0;i<60*90;i++){
     if(i%24===0){ // ~2.5 masini/s in total
       const a=ends[spawned%4], bIdx=[1,0,3,2][spawned%4]; const bb=ends[(spawned%4+1+(spawned>>2)%3)%4];
       const path=line(a,c0).concat(line(c0,bb).slice(1));
       const h={home:0,t:path[path.length-1],x:0,y:0,dir:0};
       const car={id:9e6+spawned,kind:'car',h,s:null,depot:null,path,i:0,t:0,L:1,phase:'back',wait:0,cool:0,blk:0,xw:0,ghost:false,color:spawned%5,x:0,y:0,ang:0,cargo:0,dead:false,born:G.time};
       G.cars.push(car); spawned++;
     }
     const before=G.cars.filter(c=>c.id>=9e6).map(c=>c.id);
     T.step(1/60);
     const after=new Set(G.cars.filter(c=>c.id>=9e6).map(c=>c.id));
     for(const id of before) if(!after.has(id)) done++;
     if(mode>0&&i===60*45) window.__snap=true;
   }
   const queued=G.cars.filter(c=>c.id>=9e6).length;
   return {mode:['fara control','semafor','sens giratoriu'][mode],spawned,done,queued,center:C};
  },mode);
  console.log(JSON.stringify(r));
  await p.evaluate(()=>{const G=window.__TJ.G;G.modal=false;document.getElementById('scrWeek').hidden=true;document.getElementById('toast').classList.remove('show');G.weekT=0;});
  await p.waitForTimeout(500);
  if(mode>0) await p.screenshot({path:_path.join(CAP,'inter')+mode+'.png',clip:{x:560,y:200,width:560,height:460}});
 }
 console.log('errors',errs);
 await b.close();
})();
