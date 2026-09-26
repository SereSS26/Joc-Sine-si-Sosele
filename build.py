#!/usr/bin/env python3
# Sine si Sosele - construieste jocul din sursa.
#
#   python3 build.py
#
# Porneste de la src/game.html, pune fonturile inauntru si scrie:
#   index.html                 jocul gata de jucat (dublu-click)
#   game/index.html            acelasi joc, pentru aplicatia desktop (Electron / Steam)
#   mobile/                    versiunea de telefon, instalabila (PWA), merge fara internet
#   sine-si-sosele-web.zip     continutul lui mobile/, gata de urcat pe itch.io
#   docs/joaca/                aceeasi versiune, pentru pagina de prezentare (GitHub Pages)
#
# Are nevoie de Python 3 si Pillow (pip3 install pillow) pentru iconitele de telefon.
import base64, json, os, shutil, zipfile
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
def p(*a): return os.path.join(ROOT, *a)

# ---------------- fonturile (SIL Open Font License, vezi src/fonts/)
fonts = [('Big Shoulders Display', 800, 'big-shoulders-display-latin-800-normal.woff2'),
         ('Big Shoulders Display', 900, 'big-shoulders-display-latin-900-normal.woff2'),
         ('Barlow', 500, 'barlow-latin-500-normal.woff2'),
         ('Barlow', 600, 'barlow-latin-600-normal.woff2'),
         ('Barlow', 700, 'barlow-latin-700-normal.woff2')]
css = ''.join("@font-face{font-family:'%s';font-style:normal;font-weight:%d;font-display:block;src:url(data:font/woff2;base64,%s) format('woff2');}\n"
              % (n, w, base64.b64encode(open(p('src', 'fonts', f), 'rb').read()).decode()) for n, w, f in fonts)
src = open(p('src', 'game.html'), encoding='utf-8').read().replace('/*@FONTFACE@*/', css)

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f: f.write(text)

# ---------------- pagina de sine statatoare (calculator + Electron)
head = '<!doctype html>\n<html lang="ro">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">\n'
i = src.index('<div id="app">')
page = head + src[:i] + '</head>\n<body>\n' + src[i:] + '\n</body>\n</html>\n'
write(p('index.html'), page)
write(p('game', 'index.html'), page)
print('joc ok', len(src) // 1024, 'KB')

# ---------------- pachet mobil (PWA): instalabil pe telefon, merge si offline
M = p('mobile')
pwa_head = head + """<meta name="theme-color" content="#CFD4C8">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Sine si Sosele">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" href="icon-192.png">
"""
sw_reg = '<script>if("serviceWorker" in navigator&&(location.protocol==="https:"||location.hostname==="localhost")){addEventListener("load",function(){navigator.serviceWorker.register("sw.js").catch(function(){});});}</script>\n'
write(os.path.join(M, 'index.html'), pwa_head + src[:i] + '</head>\n<body>\n' + src[i:] + '\n' + sw_reg + '</body>\n</html>\n')
with open(os.path.join(M, 'manifest.webmanifest'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump({"name": "Sine si Sosele", "short_name": "Sine si Sosele", "description": "Drumuri, sine si orase care cresc.", "lang": "ro",
               "start_url": "./", "scope": "./", "display": "fullscreen", "orientation": "any", "background_color": "#CFD4C8", "theme_color": "#CFD4C8",
               "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                         {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
                         {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}, f, indent=1)
# Cand schimbi jocul, mareste numarul din CACHE ca telefoanele sa ia versiunea noua.
write(os.path.join(M, 'sw.js'), """// Sine si Sosele - pastreaza jocul pe telefon ca sa mearga si fara internet
const CACHE='sine-si-sosele-1.0.0';
const FILES=['./','./index.html','./manifest.webmanifest','./icon-180.png','./icon-192.png','./icon-512.png','./icon-maskable-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)));self.skipWaiting();});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)));});
""")
ico = Image.open(p('build', 'icon.png')).convert('RGBA')
for sz, name in [(180, 'icon-180.png'), (192, 'icon-192.png'), (512, 'icon-512.png')]:
    bg = Image.new('RGBA', (sz, sz), (226, 231, 219, 255)) if sz == 180 else Image.new('RGBA', (sz, sz), (0, 0, 0, 0))
    bg.alpha_composite(ico.resize((sz, sz), Image.LANCZOS)); bg.save(os.path.join(M, name))
mk = Image.new('RGBA', (512, 512), (226, 231, 219, 255))
mk.alpha_composite(ico.resize((440, 440), Image.LANCZOS), (36, 36)); mk.save(os.path.join(M, 'icon-maskable-512.png'))
with zipfile.ZipFile(p('sine-si-sosele-web.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir(M)): z.write(os.path.join(M, f), f)
print('telefon ok', sorted(os.listdir(M)))

# ---------------- pagina de prezentare (GitHub Pages din folderul docs/): jocul jucabil la /joaca/
J = p('docs', 'joaca')
os.makedirs(J, exist_ok=True)
for f in sorted(os.listdir(M)): shutil.copy(os.path.join(M, f), os.path.join(J, f))
print('pagina ok: docs/joaca/')
