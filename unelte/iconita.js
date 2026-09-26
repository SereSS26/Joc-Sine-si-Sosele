// Sine si Sosele - genereaza iconita jocului build/icon.png din unelte/iconita.html
// Ruleaza din folderul proiectului: node unelte/iconita.js
const _path=require('path'),_fs=require('fs'),{pathToFileURL:_url}=require('url');
const ROOT=_path.resolve(__dirname,'..'), CAP=_path.join(__dirname,'capturi'); _fs.mkdirSync(CAP,{recursive:true});
const GAME=_url(_path.join(ROOT,'index.html')).href, GAME_DESKTOP=_url(_path.join(ROOT,'game','index.html')).href;
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1024,height:1024}});
await p.goto(_url(_path.join(__dirname,'iconita.html')).href);await p.screenshot({path:_path.join(ROOT,'build','icon.png'),omitBackground:true});await b.close();})();
