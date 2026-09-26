// Sine si Sosele - construieste automat un oras "jucat" cateva saptamani.
// Folosit de unelte/media-pagina.js pentru filmari si imagini. Jocul trebuie sa fie deja deschis in pagina.
async function construiesteOras(p, ci, weeks){
  return p.evaluate(({ci,weeks})=>{
    const T=window.__TJ;
    T.startCity(ci);
    const G=T.G; G.res.road=999;G.res.rail=999;G.res.bridge=99;G.res.barrier=99;G.res.overpass=0;G.res.loco=2;G.res.truck=2;G.res.lights=0;G.res.round=0;
    const linkedH=new Set(), linkedS=new Set(), linkedR=new Set();
    const bot=()=>{
      for(const s of G.shops){ if(linkedS.has(s.id))continue;
        let best=null,bd=1e9; for(const d of G.depots){const dd=Math.hypot(d.x-s.x,d.y-s.y);if(dd<bd){bd=dd;best=d;}}
        if(best&&T.autoConnect([...T.doorTiles(best,'rail')][0],T.doorTiles(s,'rail'),'rail',false)){linkedS.add(s.id);G.res.loco++;}
      }
      for(const d of G.depots){ if(d.__r) continue; const s=G.shops[0]; if(s&&T.autoConnect([...T.doorTiles(d,'road')][0],T.doorTiles(s,'road'),'road',false)){d.__r=1;G.res.truck++;} }
      for(const h of G.houses){ if(linkedH.has(h.id))continue;
        let best=null,bd=1e9; for(const s of G.shops) if(s.color===h.color){const dd=Math.hypot(s.x-h.x,s.y-h.y);if(dd<bd){bd=dd;best=s;}}
        const door=h.t+[1,T.W+1,T.W,T.W-1,-1,-T.W-1,-T.W,-T.W+1][h.dir];
        if(best&&T.autoConnect(door,T.doorTiles(best,'road'),'road',false)){ linkedH.add(h.id); linkedR.add(best.id); }
      }
      // fiecare magazin primeste drum de la cea mai apropiata casa de aceeasi culoare (niciun magazin izolat)
      for(const s of G.shops){ if(linkedR.has(s.id)) continue;
        let best=null,bd=1e9; for(const h of G.houses) if(h.color===s.color){const dd=Math.hypot(s.x-h.x,s.y-h.y);if(dd<bd){bd=dd;best=h;}}
        if(!best) continue; const door=best.t+[1,T.W+1,T.W,T.W-1,-1,-T.W-1,-T.W,-T.W+1][best.dir];
        if(T.autoConnect(door,T.doorTiles(s,'road'),'road',false)) linkedR.add(s.id);
      }
    };
    const assign=()=>{ let i=0; while(G.res.loco>0) T.addTrain(G.depots[(i++)%G.depots.length]); i=0; while(G.res.truck>0) T.addTruck(G.depots[(i++)%G.depots.length]); };
    const closeWeek=()=>{ if(G.modal){G.modal=false;document.getElementById('scrWeek').hidden=true;} };
    let n=0;
    while(G.week<weeks&&n<60*60*12){
      closeWeek();
      for(const s of G.shops) if(s.timer>.5) s.timer=.5;
      if(n%60===0){ bot(); assign(); }
      T.step(1/60); n++;
    }
    // intersectii: sensuri giratorii si semafoare
    const cand=[]; for(let t=0;t<T.N;t++) if(T.roadN[t]&&!T.railN[t]&&T.isInter(t)) cand.push([t,T.roadDeg(t)]); cand.sort((a,b)=>b[1]-a[1]);
    G.res.round=2; G.res.lights=3;
    const round=cand.slice(0,2).map(c=>c[0]), lights=cand.slice(2,5).map(c=>c[0]);
    for(const t of round) T.applySpecial(t,'round'); for(const t of lights) T.applySpecial(t,'lights');
    for(let i=0;i<600;i++){ closeWeek(); T.step(1/60); }
    // treceri la nivel: prima devine pasaj, restul primesc bariere
    const xings=[]; let over=-1;
    for(let t=0;t<T.N;t++) if(T.roadN[t]&&T.railN[t]){ if(over<0){T.xing[t]=2;over=t;} else {T.xing[t]=1;xings.push(t);} }
    for(let i=0;i<240;i++){ closeWeek(); T.step(1/60); }
    G.res={road:24,rail:12,bridge:2,loco:0,truck:1,barrier:2,overpass:1,lights:1,round:0};
    G.weekT=19; G.staticDirty=true; G.fx=[];
    document.getElementById('scrWeek').hidden=true;
    return {round,lights,xings,over};
  },{ci,weeks});
}
module.exports={construiesteOras};
