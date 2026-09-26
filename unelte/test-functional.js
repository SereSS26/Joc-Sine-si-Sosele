// Sine si Sosele - test functional: bonusurile +2 trenuri/camioane, atribuirea manuala pe depozite, pasajul de 10
// Ruleaza din folderul proiectului: node unelte/test-functional.js
const _path=require('path'),_fs=require('fs'),{pathToFileURL:_url}=require('url');
const ROOT=_path.resolve(__dirname,'..'), CAP=_path.join(__dirname,'capturi'); _fs.mkdirSync(CAP,{recursive:true});
const GAME=_url(_path.join(ROOT,'index.html')).href, GAME_DESKTOP=_url(_path.join(ROOT,'game','index.html')).href;
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto(GAME);await p.waitForTimeout(800);
await p.click('#mPlay'); await p.click('.cityCard'); await p.waitForTimeout(300);
// bonusuri: trenuri si camioane
for(const [i,k] of [[1,'loco'],[2,'truck']]){ const r0=await p.evaluate(k=>window.__TJ.G.res[k],k);
  await p.evaluate(()=>window.__TJ.endWeek()); await p.waitForTimeout(150);
  const card=await p.evaluate(i=>document.querySelector('#choices .choice:nth-child('+i+')').textContent,i);
  await p.click('#choices .choice:nth-child('+i+')'); await p.waitForTimeout(100);
  console.log('bonus',card,'-> +'+(await p.evaluate(k=>window.__TJ.G.res[k],k)-r0)); }
// pune toate vehiculele libere pe A
const A=await p.evaluate(()=>{const T=window.__TJ,d=T.G.depots[0];return T.t2s(d.x+1,d.y+1);});
await p.mouse.click(A[0],A[1]); await p.waitForTimeout(100);
for(let i=0;i<2;i++){ await p.click('#dpTp'); await p.click('#dpKp'); }
console.log('A dupa +:',await p.evaluate(()=>document.getElementById('dpTn').textContent+' trenuri, '+document.getElementById('dpKn').textContent+' camioane; libere '+window.__TJ.G.res.loco+'/'+window.__TJ.G.res.truck));
await p.click('#dpClose');
// depozit B
await p.evaluate(()=>{window.__TJ.endWeek();}); await p.waitForTimeout(100); await p.click('#choices .choice:nth-child(4)');
await p.evaluate(()=>{window.__TJ.endWeek();}); await p.waitForTimeout(100); await p.click('#choices .choice:nth-child(4)');
const B=await p.evaluate(()=>{const T=window.__TJ,d=T.G.depots[1];return d?T.t2s(d.x+1,d.y+1):null;});
await p.mouse.click(B[0],B[1]); await p.waitForTimeout(100);
console.log('B fara vehicule libere: +tren activ?',await p.evaluate(()=>!document.getElementById('dpTp').disabled),'| +camion activ?',await p.evaluate(()=>!document.getElementById('dpKp').disabled));
await p.click('#dpTp',{force:true}).catch(()=>{}); await p.waitForTimeout(50);
console.log('B dupa click pe + dezactivat:',await p.evaluate(()=>document.getElementById('dpTn').textContent),'trenuri');
// - pe A, apoi + pe B
await p.click('#dpClose'); await p.mouse.click(A[0],A[1]); await p.waitForTimeout(100); await p.click('#dpTm'); await p.waitForTimeout(50);
console.log('dupa - pe A: libere trenuri',await p.evaluate(()=>window.__TJ.G.res.loco));
await p.click('#dpClose'); await p.mouse.click(B[0],B[1]); await p.waitForTimeout(100);
console.log('B: +tren activ acum?',await p.evaluate(()=>!document.getElementById('dpTp').disabled)); await p.click('#dpTp'); await p.waitForTimeout(50);
console.log('B dupa +:',await p.evaluate(()=>document.getElementById('dpTn').textContent),'tren; A:',await p.evaluate(()=>{const G=window.__TJ.G;return G.trains.filter(t=>t.depot===G.depots[0]).length;}),'trenuri');
// pasaj: 10 patratele ok, 11 nu
console.log('pasaj peste 10:',await p.evaluate(()=>{const T=window.__TJ,G=T.G,W=T.W,b=G.bounds;for(let y=b.y0;y<=b.y1;y++)for(let x=b.x0;x+11<=b.x1;x++){const a=y*W+x;const r10=T.viaCheck(a,a+11),r11=T.viaCheck(a,a+12);if(r10.ok) return {peste10:r10.ok,peste11:r11.reason||r11.ok};}return 'fara loc';}));
console.log('errors',errs);await b.close();})();
