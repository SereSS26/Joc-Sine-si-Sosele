// Sine si Sosele - filmeaza jocul si face imaginile pentru pagina de prezentare si pentru Steam.
// Nu il rulezi direct: porneste  python3 unelte/media-pagina.py  (care il apeleaza si apoi face video-ul si imaginile finale).
const _path=require('path'),_fs=require('fs'),{pathToFileURL:_url}=require('url');
const { chromium } = require('playwright');
const { construiesteOras } = require('./oras-demo');
const ROOT=_path.resolve(__dirname,'..'), OUT=_path.join(__dirname,'capturi','media');
const GAME=_url(_path.join(ROOT,'game','index.html')).href;
const FPS=30, SECUNDE=+(process.env.SECUNDE||14);
_fs.rmSync(OUT,{recursive:true,force:true}); _fs.mkdirSync(_path.join(OUT,'cadre'),{recursive:true});

// camera pe o anumita patratica (tile), cu zoom fata de incadrarea normala
async function camera(p,tile,zoom){
  await p.evaluate(({tile,zoom})=>{
    const T=window.__TJ,G=T.G,b=G.bounds,bw=b.x1-b.x0+2,bh=b.y1-b.y0+2;
    const x=tile%T.W+.5, y=Math.floor(tile/T.W)+.5;
    G.capsule={zoom,dx:(x-(b.x0+b.x1+1)/2)/bw,dy:(y-(b.y0+b.y1+1)/2)/bh};
    T.fitCam(true); G.staticDirty=true;
  },{tile,zoom});
}
const ascundeHud=p=>p.evaluate(()=>{document.getElementById('hud').hidden=true;});
// Math.random cu samanta fixa: la fiecare rulare iese acelasi oras, deci aceleasi imagini
const SAMANTA=+(process.env.SAMANTA||7);
const initRandom=`(()=>{let a=${SAMANTA}>>>0;Math.random=function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};})();`;
const pas=(p,n)=>p.evaluate(n=>{const T=window.__TJ,G=T.G;for(let i=0;i<n;i++){if(G.modal){G.modal=false;document.getElementById('scrWeek').hidden=true;}for(const s of G.shops)if(s.timer>.5)s.timer=.5;T.step(1/60);}},n);

(async()=>{
  const b=await chromium.launch();
  const errs=[];
  const pagina=async opts=>{ const ctx=await b.newContext(opts); await ctx.addInitScript(initRandom); const p=await ctx.newPage(); p.on('pageerror',e=>errs.push(e.message)); return [ctx,p]; };

  // ---------------- 1. video pentru prima pagina: cadru cu cadru, cu ceasul paginii controlat
  {
    const [ctx,p]=await pagina({viewport:{width:1280,height:720},deviceScaleFactor:1.5});
    await p.clock.install({time:0}); await p.goto(GAME); await p.clock.runFor(1500);
    await construiesteOras(p,0,7);
    await p.clock.pauseAt(1e6);
    await ascundeHud(p);
    await p.evaluate(()=>{const T=window.__TJ,G=T.G;G.mode='demo';G.city=Object.assign({},G.city,{diff:G.city.diff*1.5/.55});G.capsule={zoom:1.08,dx:0,dy:0};T.fitCam(true);G.staticDirty=true;});
    await p.clock.runFor(4000);
    const n=FPS*SECUNDE;
    for(let i=0;i<n;i++){
      await p.clock.runFor(1000/FPS);
      await p.screenshot({path:_path.join(OUT,'cadre',String(i).padStart(4,'0')+'.jpg'),type:'jpeg',quality:94});
    }
    console.log('video: '+n+' cadre');
    await ctx.close();
  }

  // ---------------- 2. prim-planuri pentru caracteristici (900x600, retina)
  {
    const [ctx,p]=await pagina({viewport:{width:900,height:600},deviceScaleFactor:2});
    await p.goto(GAME); await p.waitForTimeout(700);
    const info=await construiesteOras(p,0,8);
    await ascundeHud(p);
    const shot=async(name,tile,zoom)=>{ await camera(p,tile,zoom); await p.waitForTimeout(250); await p.screenshot({path:_path.join(OUT,name+'.png')}); };
    await p.evaluate(()=>{window.__TJ.G.paused=true;});
    // trecere la nivel cu bariera: asteptam un tren chiar pe trecere
    const trecere=await p.evaluate(({xings:all})=>{
      const T=window.__TJ,G=T.G,b=G.bounds;
      // doar treceri departe de marginea hartii, ca prim-planul sa fie plin
      const inner=all.filter(t=>{const x=t%T.W,y=Math.floor(t/T.W);return x-b.x0>=6&&b.x1-x>=6&&y-b.y0>=4&&b.y1-y>=4;});
      const xings=inner.length?inner:all;
      for(let i=0;i<60*120;i++){
        for(const tr of G.trains){ if(!tr.path||tr.gone) continue;
          for(const x of xings){ const j=tr.path.indexOf(x); if(j>=0&&j>=tr.seg&&j<=tr.seg+1) return x; }
        }
        if(G.modal){G.modal=false;document.getElementById('scrWeek').hidden=true;} for(const s of G.shops)if(s.timer>.5)s.timer=.5; T.step(1/60);
      }
      return xings[0];
    },{xings:info.xings});
    await shot('prim-trecere',trecere,3.0);
    const rnd=await p.evaluate(({round})=>{const T=window.__TJ,b=T.G.bounds,cx=(b.x0+b.x1)/2,cy=(b.y0+b.y1)/2;return [...round].sort((u,v)=>Math.hypot(u%T.W-cx,Math.floor(u/T.W)-cy)-Math.hypot(v%T.W-cx,Math.floor(v/T.W)-cy))[0];},{round:info.round});
    await shot('prim-giratoriu',rnd,3.6);
    await shot('prim-semafor',info.lights[0],3.2);
    const dep=await p.evaluate(()=>{const T=window.__TJ,G=T.G,d=G.depots[0];return Math.round(d.y+.5)*T.W+Math.round(d.x+.5);});
    await shot('prim-depozit',dep,2.8);
    const mag=await p.evaluate(()=>{const T=window.__TJ,G=T.G;const s=[...G.shops].sort((a,b)=>b.level-a.level||b.score-a.score)[0];return Math.round(s.y+.5)*T.W+Math.round(s.x+.5);});
    await shot('prim-magazin',mag,2.8);
    // pasaj lung peste rau
    const via=await p.evaluate(()=>{
      const T=window.__TJ,G=T.G,W=T.W,b=G.bounds; G.res.overpass=3; G.res.road=200;
      const rows=[]; for(let y=b.y0+3;y<=b.y1-3;y++) rows.push(y); const my=(b.y0+b.y1)/2; rows.sort((u,v)=>Math.abs(u-my)-Math.abs(v-my));
      for(const y of rows){ let x0=-1,x1=-1; for(let x=b.x0;x<=b.x1;x++){ if(T.water[y*W+x]){ if(x0<0)x0=x; x1=x; } }
        if(x0<0) continue; const a=y*W+x0-2, c=y*W+x1+2; if(!T.viaCheck(a,c).ok) continue;
        if(!T.buildVia(a,c)) continue;
        const near=(t)=>{let best=null,bd=1e9;const tx=t%W,ty=Math.floor(t/W);for(const s of G.shops){const d=Math.hypot(s.x-tx,s.y-ty);if(d<bd){bd=d;best=s;}}return best;};
        T.autoConnect(a,T.doorTiles(near(a),'road'),'road',false); T.autoConnect(c,T.doorTiles(near(c),'road'),'road',false);
        return {a,c,mid:y*W+Math.round((x0+x1)/2)};
      }
      return null;});
    if(via){ await p.evaluate(()=>{window.__TJ.G.paused=false;}); await pas(p,60*20); await p.evaluate(()=>{window.__TJ.G.paused=true;}); await shot('prim-pasaj',via.mid,2.2); }
    else console.log('fara pasaj peste rau');
    await ctx.close();
  }

  // ---------------- 3. orasele (fara interfata), pentru cartonase
  for(let ci=0;ci<5;ci++){
    const [ctx,p]=await pagina({viewport:{width:960,height:600},deviceScaleFactor:1.5});
    await p.goto(GAME); await p.waitForTimeout(700);
    await construiesteOras(p,ci,6);
    await ascundeHud(p);
    await p.evaluate(()=>{const T=window.__TJ,G=T.G;G.mode='demo';G.capsule={zoom:1.04,dx:0,dy:0};T.fitCam(true);G.staticDirty=true;});
    await p.waitForTimeout(1500);
    await p.screenshot({path:_path.join(OUT,'oras-'+ci+'.png')});
    await ctx.close();
  }

  // ---------------- 4. capturi de joc cu interfata (1920x1080) - galerie si Steam
  const shots=[[0,7],[2,6],[3,6],[4,7],[1,5]];
  for(let k=0;k<shots.length;k++){
    const [ci,wk]=shots[k];
    const [ctx,p]=await pagina({viewport:{width:1920,height:1080}});
    await p.goto(GAME); await p.waitForTimeout(700);
    await construiesteOras(p,ci,wk);
    await p.waitForTimeout(700);
    await p.screenshot({path:_path.join(OUT,'captura-'+(k+1)+'.png')});
    await ctx.close();
  }

  // ---------------- 5. telefon: vertical si orizontal
  for(const [name,w,h] of [['telefon-vertical',390,844],['telefon-orizontal',844,390]]){
    const [ctx,p]=await pagina({viewport:{width:w,height:h},deviceScaleFactor:3,isMobile:true,hasTouch:true});
    await p.goto(GAME); await p.waitForTimeout(700);
    await construiesteOras(p,3,6);
    // pe vertical: zoom (ca dupa ciupire cu doua degete) pe zona cu cele mai multe case
    if(h>w) await p.evaluate(()=>{const T=window.__TJ,G=T.G,b=G.bounds;let mx=0,my=0;for(const q of G.houses){mx+=q.x;my+=q.y;}mx/=G.houses.length;my/=G.houses.length;
      G.zoom=2.6;G.pan={x:mx+.5-(b.x0+b.x1+1)/2,y:my+.5-(b.y0+b.y1+1)/2};T.fitCam(true);G.staticDirty=true;});
    await p.waitForTimeout(900);
    await p.screenshot({path:_path.join(OUT,name+'.png')});
    await ctx.close();
  }

  // ---------------- 6. imagine pentru share (Open Graph) 1200x630
  {
    const [ctx,p]=await pagina({viewport:{width:1200,height:630}});
    await p.goto(GAME); await p.waitForTimeout(700);
    await construiesteOras(p,0,6);
    await ascundeHud(p);
    await p.evaluate(()=>{
      const T=window.__TJ,G=T.G; G.mode='demo'; G.capsule={zoom:1.05,dx:-.12,dy:0}; T.fitCam(true); G.staticDirty=true;
      const d=document.createElement('div');
      d.innerHTML='<div style="font-family:\'Big Shoulders Display\';font-weight:900;text-transform:uppercase;line-height:.82;font-size:150px;color:#22262D">Sine si<span style="display:block;color:#E8604C">Sosele</span></div>'+
        '<div style="font-family:Barlow;font-weight:600;font-size:30px;color:#4A515C;margin-top:26px;max-width:470px;line-height:1.25">Masini, trenuri si camioane intr-un singur oras.</div>';
      d.style.cssText='position:fixed;z-index:9;inset:0;display:flex;flex-direction:column;justify-content:center;padding-left:72px;background:linear-gradient(90deg,rgba(226,231,219,.98) 0,rgba(226,231,219,.92) 42%,rgba(226,231,219,0) 66%)';
      document.getElementById('app').appendChild(d);
    });
    await p.waitForTimeout(1200);
    await p.screenshot({path:_path.join(OUT,'og.png')});
    await ctx.close();
  }

  console.log('erori:',errs.length?errs:'niciuna');
  await b.close();
})();
