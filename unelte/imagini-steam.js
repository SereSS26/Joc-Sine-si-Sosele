// Sine si Sosele - genereaza imaginile pentru pagina de Steam in folderul store/
// Ruleaza din folderul proiectului: node unelte/imagini-steam.js
const _path=require('path'),_fs=require('fs'),{pathToFileURL:_url}=require('url');
const ROOT=_path.resolve(__dirname,'..'), CAP=_path.join(__dirname,'capturi'); _fs.mkdirSync(CAP,{recursive:true});
const GAME=_url(_path.join(ROOT,'index.html')).href, GAME_DESKTOP=_url(_path.join(ROOT,'game','index.html')).href;
const { chromium } = require('playwright');
const OUT=_path.join(ROOT,'store')+'/';
async function prepare(p,ci,weeks,lang){
  await p.goto(GAME_DESKTOP); await p.waitForTimeout(600);
  await p.evaluate(({ci,weeks,lang})=>{
    const T=window.__TJ;
    T.startCity(ci);
    const G=T.G; G.res.road=999;G.res.rail=999;G.res.bridge=99;G.res.barrier=99;G.res.overpass=0;G.res.loco=2;G.res.truck=2;G.res.lights=0;G.res.round=0;
    const linkedH=new Set(), linkedS=new Set();
    const bot=()=>{
      for(const s of G.shops){ if(linkedS.has(s.id))continue;
        let best=null,bd=1e9; for(const d of G.depots){const dd=Math.hypot(d.x-s.x,d.y-s.y);if(dd<bd){bd=dd;best=d;}}
        if(best&&T.autoConnect([...T.doorTiles(best,'rail')][0],T.doorTiles(s,'rail'),'rail',false)){linkedS.add(s.id);G.res.loco++;}
      }
      for(const d of G.depots){ if(d.__r) continue; const s=G.shops[0]; if(s&&T.autoConnect([...T.doorTiles(d,'road')][0],T.doorTiles(s,'road'),'road',false)){d.__r=1;G.res.truck++;} }
      for(const h of G.houses){ if(linkedH.has(h.id))continue;
        let best=null,bd=1e9; for(const s of G.shops) if(s.color===h.color){const dd=Math.hypot(s.x-h.x,s.y-h.y);if(dd<bd){bd=dd;best=s;}}
        const door=h.t+[1,T.W+1,T.W,T.W-1,-1,-T.W-1,-T.W,-T.W+1][h.dir];
        if(best&&T.autoConnect(door,T.doorTiles(best,'road'),'road',false)) linkedH.add(h.id);
      }
    };
    const assign=()=>{ let i=0; while(G.res.loco>0) T.addTrain(G.depots[(i++)%G.depots.length]); i=0; while(G.res.truck>0) T.addTruck(G.depots[(i++)%G.depots.length]); };
    let n=0;
    while(G.week<weeks&&n<60*60*12){
      if(G.modal){G.modal=false;document.getElementById('scrWeek').hidden=true;}
      for(const s of G.shops) if(s.timer>.5) s.timer=.5;
      if(n%60===0){ bot(); assign(); }
      T.step(1/60); n++;
    }
    // intersectii: sensuri giratorii si semafoare
    { const cand=[]; for(let t=0;t<T.N;t++) if(T.roadN[t]&&!T.railN[t]&&T.isInter(t)) cand.push([t,T.roadDeg(t)]); cand.sort((a,b)=>b[1]-a[1]);
      G.res.round=2; G.res.lights=3; for(const [t] of cand.slice(0,2)) T.applySpecial(t,'round'); for(const [t] of cand.slice(2,5)) T.applySpecial(t,'lights'); }
    for(let i=0;i<600;i++){ if(G.modal){G.modal=false;document.getElementById('scrWeek').hidden=true;} T.step(1/60); }
    // un pasaj pentru varietate
    let did=false; for(let t=0;t<T.N;t++) if(T.roadN[t]&&T.railN[t]){ if(!did){T.xing[t]=2;did=true;} else T.xing[t]=1; }
    for(let i=0;i<240;i++){ if(G.modal){G.modal=false;document.getElementById('scrWeek').hidden=true;} T.step(1/60); }
    G.res={road:24,rail:12,bridge:2,loco:0,truck:1,barrier:2,overpass:1,lights:1,round:0};
    G.weekT=19; G.staticDirty=true; G.fx=[];
    document.getElementById('toast').classList.remove('show');
    document.getElementById('scrWeek').hidden=true;
  },{ci,weeks,lang});
  await p.waitForTimeout(700);
}
(async()=>{
  const b=await chromium.launch();
  // capturi 1920x1080
  const shots=[[0,7],[2,6],[3,6],[4,7],[1,5]];
  let k=1;
  for(const [ci,wk] of shots){
    const p=await b.newPage({viewport:{width:1920,height:1080}});
    await prepare(p,ci,wk);
    await p.evaluate(()=>{const G=window.__TJ.G;G.paused=false;});
    await p.waitForTimeout(400);
    await p.screenshot({path:OUT+'screenshot_'+(k++)+'.png'});
    await p.close();
  }
  // capsule
  const caps=[['header_capsule',920,430,'left'],['small_capsule',462,174,'center'],['main_capsule',1232,706,'left'],['vertical_capsule',748,896,'top'],['library_capsule',600,900,'top'],['library_hero',1920,620,'none'],['page_background',1438,810,'none']];
  for(const [name,w,h,logo] of caps){
    const scale=name==='library_hero'?2:1;
    const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:scale});
    await prepare(p,0,6);
    await p.evaluate(({logo,w,h,name})=>{
      document.getElementById('hud').hidden=true;
      const G=window.__TJ.G; G.mode='demo'; G.staticDirty=true;
      const Z={header_capsule:{zoom:1.05,dx:-.12,dy:0},small_capsule:{zoom:1.1,dx:0,dy:0},main_capsule:{zoom:1.05,dx:-.12,dy:0},vertical_capsule:{zoom:1.14,dx:0,dy:.02},library_capsule:{zoom:1.14,dx:0,dy:.02},library_hero:{zoom:1,dx:0,dy:0},page_background:{zoom:1,dx:0,dy:0}};
      G.capsule=Z[name]; window.__TJ.fitCam(true);
      if(name==='page_background'){document.body.style.filter='saturate(.6) opacity(.5)';}
      if(logo==='none')return;
      const d=document.createElement('div');
      const size=logo==='center'?Math.min(w/6.2,h/1.9):logo==='top'?w/5.2:Math.min(w/7.5,h/3.4);
      d.innerHTML='<div style="font-family:\'Big Shoulders Display\';font-weight:900;text-transform:uppercase;line-height:.82;font-size:'+size+'px;color:#22262D">Sine si<span style="display:block;color:#E8604C">Sosele</span></div>';
      const base='position:fixed;z-index:9;display:flex;';
      if(logo==='left') d.style.cssText=base+'inset:0;align-items:center;padding-left:'+(w*.06)+'px;background:linear-gradient(90deg,rgba(226,231,219,.97) 0,rgba(226,231,219,.9) 38%,rgba(226,231,219,0) 62%)';
      if(logo==='center') d.style.cssText=base+'inset:0;align-items:center;justify-content:center;text-align:center;background:rgba(226,231,219,.84)';
      if(logo==='top') d.style.cssText=base+'inset:0;align-items:flex-start;padding:'+(h*.07)+'px '+(w*.08)+'px;background:linear-gradient(180deg,rgba(226,231,219,.97) 0,rgba(226,231,219,.88) 30%,rgba(226,231,219,0) 55%)';
      document.getElementById('app').appendChild(d);
    },{logo,w,h,name});
    await p.waitForTimeout(900);
    await p.screenshot({path:OUT+name+'.png'});
    await p.close();
  }
  // logo transparent 1280x720
  const p=await b.newPage({viewport:{width:1280,height:720}});
  await p.goto(GAME_DESKTOP); await p.waitForTimeout(500);
  await p.evaluate(()=>{document.body.innerHTML='<div style="height:720px;display:flex;align-items:center;justify-content:center"><div style="font-family:\'Big Shoulders Display\';font-weight:900;text-transform:uppercase;line-height:.82;font-size:230px;color:#22262D;text-align:center">Sine si<span style="display:block;color:#E8604C">Sosele</span></div></div>';document.body.style.background='transparent';});
  await p.waitForTimeout(300); await p.screenshot({path:OUT+'library_logo.png',omitBackground:true});
  await b.close();
})();
