// Sine si Sosele - test pentru versiunea de telefon instalabila (manifest, service worker, merge fara internet)
// Ruleaza din folderul proiectului: intai porneste un server: python3 -m http.server 8765 -d mobile   apoi: node unelte/test-pwa-offline.js
const _path=require('path'),_fs=require('fs'),{pathToFileURL:_url}=require('url');
const ROOT=_path.resolve(__dirname,'..'), CAP=_path.join(__dirname,'capturi'); _fs.mkdirSync(CAP,{recursive:true});
const GAME=_url(_path.join(ROOT,'index.html')).href, GAME_DESKTOP=_url(_path.join(ROOT,'game','index.html')).href;
const { chromium, devices } = require('playwright');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({...devices['Pixel 7']});const p=await ctx.newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/');await p.waitForTimeout(1500);
const m=await p.evaluate(async()=>{const r=await fetch('manifest.webmanifest');const j=await r.json();return j.name+' / '+j.display+' / icons '+j.icons.length;});
console.log('manifest',m);
const sw=await p.evaluate(async()=>{const reg=await navigator.serviceWorker.ready;return !!reg.active;});
console.log('service worker active',sw);
await p.waitForTimeout(800);
await ctx.setOffline(true);
await p.reload(); await p.waitForTimeout(1500);
console.log('offline reload -> game loaded:',await p.evaluate(()=>!!window.__TJ&&document.title));
await p.tap('#mPlay'); await p.tap('.cityCard'); await p.waitForTimeout(500);
console.log('offline play ok:',await p.evaluate(()=>window.__TJ.G.mode));
console.log('errors',errs);await b.close();})();
