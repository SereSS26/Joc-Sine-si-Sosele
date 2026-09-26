// Sine si Sosele - bot care joaca singur toate orasele si masoara cate saptamani supravietuieste (pentru echilibrare)
// Ruleaza din folderul proiectului: node unelte/bot-echilibru.js
const _path=require('path'),_fs=require('fs'),{pathToFileURL:_url}=require('url');
const ROOT=_path.resolve(__dirname,'..'), CAP=_path.join(__dirname,'capturi'); _fs.mkdirSync(CAP,{recursive:true});
const GAME=_url(_path.join(ROOT,'index.html')).href, GAME_DESKTOP=_url(_path.join(ROOT,'game','index.html')).href;
// Bot de echilibrare: joaca cu resurse limitate si raporteaza cat rezista
const { chromium } = require('playwright');
const CITY=process.argv[2]?+process.argv[2]:0, RUNS=+(process.argv[3]||3), SHOT=process.argv[4]||'';
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1600,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push('PAGEERR '+e.message)); p.on('console',m=>{if(m.type()==='error'&&!/ERR_TUNNEL|Failed to load/.test(m.text()))errs.push(m.text())});
 await p.goto(GAME); await p.waitForTimeout(800);
 const results=[];
 for(let run=0;run<RUNS;run++){
  await p.evaluate((ci)=>{
    const T=window.__TJ; T.startCity(ci); const G=T.G;
    window.BOT={heat:new Map(),log:[],lastSec:-1};
  },CITY);
  let done=false, guard=0;
  while(!done&&guard++<400){
    done=await p.evaluate(()=>{
      const T=window.__TJ, G=T.G, W=T.W, N=T.N, B=window.BOT;
      const DOFF=[1,W+1,W,W-1,-1,-W-1,-W,-W+1];
      const cost=(path,kind)=>{let n=0,br=0;const NN=kind==='road'?T.roadN:T.railN;for(const t of path){if(G.shops.concat(G.depots,G.houses).some(o=>o.cells?o.cells.includes(t):o.t===t))continue;if(!NN[t]){if(isWater(t))br++;else n++;}}return {n,br};};
      const isWater=t=>{const w=window.__TJ.water;return w?w[t]:0;};
      const tryBuild=(from,goals,kind)=>{
        const path=window.__TJ.autoRoute(from,goals,kind); if(!path) return false;
        const c=cost(path,kind); if(c.n>G.res[kind]||c.br>G.res.bridge) return false;
        for(let i=0;i+1<path.length;i++) if(!T.connect(path[i],path[i+1],kind,false)) return false;
        return true;
      };
      const netGoals=(s)=>{const rc=T.shopRoad(s),g=new Set(T.doorTiles(s,'road'));for(let t=0;t<N;t++)if(T.roadN[t]&&rc.dist[t]<Infinity)g.add(t);return g;};
      const bot=()=>{
        // aprovizionare: fiecare magazin trebuie legat de un depozit (drum pentru camioane sau cale ferata pentru trenuri)
        for(const s of G.shops){
          let railOk=false, roadOk=false;
          for(const d of G.depots){ if(s.cells.some(c=>T.depotRail(d).dist[c]<Infinity)) railOk=true; if(s.cells.some(c=>T.depotRoad(d).dist[c]<Infinity)) roadOk=true; }
          const ds=[...G.depots].sort((a,b)=>Math.hypot(a.x-s.x,a.y-s.y)-Math.hypot(b.x-s.x,b.y-s.y));
          if(!roadOk&&(G.res.truck>0||G.cars.some(c=>c.kind==='truck')||!railOk)){
            for(const d of ds.slice(0,2)){ const rc=T.depotRoad(d), g=new Set(T.doorTiles(d,'road')); for(let t=0;t<N;t++) if(T.roadN[t]&&rc.dist[t]<Infinity) g.add(t);
              if(tryBuild([...T.doorTiles(s,'road')][0],g,'road')) {roadOk=true;break;} }
          }
          if(!railOk&&(G.res.loco>0||G.trains.length)&&G.res.rail>=4){
            for(const d of ds.slice(0,2)){ const rc=T.depotRail(d), g=new Set(T.doorTiles(d,'rail')); for(let t=0;t<N;t++) if(T.railN[t]&&rc.dist[t]<Infinity&&!T.roadN[t]) g.add(t);
              if(tryBuild([...T.doorTiles(s,'rail')][0],g,'rail')) break; }
          }
        }
        // magazin fara nicio casa legata: leaga-l de reteaua casele de aceeasi culoare
        for(const s of G.shops){
          const rc=T.shopRoad(s); if(G.houses.some(h=>h.color===s.color&&rc.dist[h.t]<Infinity)) continue;
          const other=G.shops.find(o=>o!==s&&o.color===s.color&&G.houses.some(h=>h.color===o.color&&T.shopRoad(o).dist[h.t]<Infinity));
          if(other) tryBuild([...T.doorTiles(s,'road')][0],netGoals(other),'road');
        }
        // case
        for(const h of G.houses){
          const same=G.shops.filter(s=>s.color===h.color); if(!same.length) continue;
          if(same.some(s=>T.shopRoad(s).dist[h.t]<Infinity)) continue;
          const s=same.sort((a,b)=>Math.hypot(a.x-h.x,a.y-h.y)-Math.hypot(b.x-h.x,b.y-h.y))[0];
          if(!tryBuild(h.t+DOFF[h.dir],netGoals(s),'road')) B.fails=(B.fails||0)+1;
        }
        // ASSIGN: vehicule libere pe depozitele care au legaturi
        while(G.res.loco>0){ const ds=G.depots.filter(d=>G.shops.some(s=>s.cells.some(c=>T.depotRail(d).dist[c]<Infinity))); if(!ds.length) break; ds.sort((a,b)=>G.trains.filter(t=>t.depot===a).length-G.trains.filter(t=>t.depot===b).length); T.addTrain(ds[0]); }
        while(G.res.truck>0){ const ds=G.depots.filter(d=>G.shops.some(s=>s.cells.some(c=>T.depotRoad(d).dist[c]<Infinity))); if(!ds.length) break; ds.sort((a,b)=>G.cars.filter(c=>c.kind==='truck'&&c.depot===a).length-G.cars.filter(c=>c.kind==='truck'&&c.depot===b).length); T.addTruck(ds[0]); }
        // treceri
        for(let t=0;t<N;t++) if(T.roadN[t]&&T.railN[t]&&T.xing[t]===0){ if(G.res.barrier>0) T.applySpecial(t,'barrier'); else if(G.res.overpass>0) T.applySpecial(t,'overpass'); }
        // intersectii aglomerate
        const hot=[...B.heat.entries()].filter(([t])=>T.isInter(t)&&!T.ctrl[t]&&!T.railN[t]).sort((a,b)=>b[1]-a[1]);
        for(const [t,hv] of hot){ if(hv<40) break; if(G.res.round>0) T.applySpecial(t,'round'); else if(G.res.lights>0) T.applySpecial(t,'lights'); else break; }
      };
      const pickUp=()=>{
        const opts=G.lastOpts||[]; const ks=opts.map(o=>o.k);
        const veh=G.trains.length+G.cars.filter(c=>c.kind==='truck').length+G.res.loco+G.res.truck;
        const low=G.shops.filter(s=>s.stock<=3).length;
        const hotN=[...B.heat.entries()].filter(([t,h])=>h>40&&T.isInter(t)&&!T.ctrl[t]).length;
        const prefs=[];
        if(G.res.loco>0) prefs.push('rail');
        if(low>0||veh<G.shops.length*0.8) prefs.push(G.res.rail>=10?'loco':'truck','truck','loco');
        if(G.res.road<15) prefs.push('road');
        if(G.res.rail<6) prefs.push('rail');
        if(hotN>0) prefs.push('round','lights');
        if(G.res.bridge<1) prefs.push('bridge');
        prefs.push('loco','truck','road','round','lights','barrier','rail','bridge','overpass');
        const k=prefs.find(x=>ks.includes(x));
        const btns=[...document.querySelectorAll('#choices .choice')];
        btns[Math.max(0,ks.indexOf(k))].click();
      };
      for(let i=0;i<60*20;i++){
        if(G.over) break;
        if(G.modal){ pickUp(); }
        const sec=Math.floor(G.time);
        if(sec!==B.lastSec){ B.lastSec=sec; bot(); }
        T.step(1/60);
        for(const [t,l] of G.occ2){ B.heat.set(t,(B.heat.get(t)||0)*0.9995+l.length*.02); }
      }
      if(G.over){
        const f=G.failShop;
        B.result={week:G.week,score:G.score,acc:G.accidents,shops:G.shops.length,lv:G.shops.map(s=>s.level).join(''),
          houses:G.houses.length,veh:G.trains.length+'T/'+G.cars.filter(c=>c.kind==='truck').length+'K',
          fail:{stock:f.stock,demand:f.demand,level:f.level,inCars:f.inCars,inGoods:f.inGoods,conn:T.shopRoad(f).dist[f.cells[0]]!==undefined},
          hfail:B.fails||0,unconn:G.houses.filter(h=>!G.shops.some(s=>s.color===h.color&&T.shopRoad(s).dist[h.t]<Infinity)).length,ctrl:[...T.ctrl].filter(x=>x===1).length+'L/'+[...T.ctrl].filter(x=>x===2).length+'R', res:JSON.stringify(G.res)};
        return true;
      }
      return G.week>=30;
    });
  }
  const r=await p.evaluate(()=>window.BOT.result||{week:window.__TJ.G.week,score:window.__TJ.G.score,note:'survived'});
  results.push(r); console.log('city',CITY,'run',run,JSON.stringify(r));
  if(SHOT&&run===0){ await p.evaluate(()=>{document.getElementById('scrOver').hidden=true;}); await p.waitForTimeout(300); await p.screenshot({path:SHOT}); }
 }
 const wk=results.map(r=>r.week); console.log('SUMMARY city',CITY,'weeks',wk.join(','),'avg',(wk.reduce((a,b)=>a+b,0)/wk.length).toFixed(1),'errors',errs.slice(0,5));
 await b.close();
})();
