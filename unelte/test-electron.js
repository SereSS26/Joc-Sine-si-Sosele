// Sine si Sosele - verifica aplicatia desktop (Electron): porneste jocul, fonturile, erorile; captura in unelte/capturi
// Ruleaza din folderul proiectului: npx electron unelte/test-electron.js
const _path=require('path'),_fs=require('fs'),{pathToFileURL:_url}=require('url');
const ROOT=_path.resolve(__dirname,'..'), CAP=_path.join(__dirname,'capturi'); _fs.mkdirSync(CAP,{recursive:true});
const GAME=_url(_path.join(ROOT,'index.html')).href, GAME_DESKTOP=_url(_path.join(ROOT,'game','index.html')).href;
const { app, BrowserWindow } = require('electron'); const fs=require('fs');
app.whenReady().then(async()=>{
  const w=new BrowserWindow({width:1600,height:900,show:false,webPreferences:{contextIsolation:true,sandbox:true}});
  const errs=[]; w.webContents.on('console-message',(e,l,m)=>{ if(l>=3) errs.push(m); });
  await w.loadFile(_path.join(ROOT,'game','index.html'));
  await new Promise(r=>setTimeout(r,2500));
  const info=await w.webContents.executeJavaScript(`({quit:!document.getElementById('mQuit').hidden, font:document.fonts.check('900 20px "Big Shoulders Display"'), shops:window.__TJ.G.shops.length, cars:window.__TJ.G.cars.length})`);
  const img=await w.webContents.capturePage(); fs.writeFileSync(_path.join(CAP,'electron.png'),img.toPNG());
  console.log('SMOKE',JSON.stringify(info),'errors',JSON.stringify(errs)); app.quit();
});
