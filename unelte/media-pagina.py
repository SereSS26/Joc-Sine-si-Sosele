#!/usr/bin/env python3
# Sine si Sosele - face video-ul, GIF-ul si imaginile pentru pagina de prezentare (docs/)
# si capturile pentru Steam (store/screenshot_1..5.png).
#
#   python3 unelte/media-pagina.py            filmeaza jocul (Playwright) si face totul
#   python3 unelte/media-pagina.py --refolosesc   foloseste capturile deja facute
#
# Are nevoie de: Node.js + Playwright, ffmpeg, Python 3 cu Pillow.
import os, shutil, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = os.path.join(ROOT, 'unelte', 'capturi', 'media')
OUT = os.path.join(ROOT, 'docs', 'media')
FPS, K = 30, 30  # K cadre de trecere la capatul buclei (1 secunda)

if '--refolosesc' not in sys.argv:
    subprocess.run(['node', os.path.join(ROOT, 'unelte', 'media-captura.js')], check=True)
os.makedirs(OUT, exist_ok=True)

def ffmpeg(*args):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *args], check=True)

cadre = sorted(os.path.join(CAP, 'cadre', f) for f in os.listdir(os.path.join(CAP, 'cadre')))
# secventa: [amestec(sfarsit, inceput)] + cadrele din mijloc  -> se repeta perfect
tmp = os.path.join(CAP, 'bucla'); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
n = len(cadre); k = 0
for j in range(K):
    a = Image.open(cadre[n - K + j]).convert('RGB'); b = Image.open(cadre[j]).convert('RGB')
    Image.blend(a, b, j / K).save(os.path.join(tmp, '%04d.jpg' % k), quality=95); k += 1
for i in range(K, n - K):
    shutil.copy(cadre[i], os.path.join(tmp, '%04d.jpg' % k)); k += 1
print('bucla video:', k, 'cadre =', round(k / FPS, 1), 's')

# ---------------- video pentru pagina (H.264, merge peste tot)
ffmpeg('-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.jpg'), '-c:v', 'libx264', '-preset', 'slow', '-crf', '24',
       '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', os.path.join(OUT, 'gameplay.mp4'))
ffmpeg('-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.jpg'), '-vf', 'scale=1280:-2', '-c:v', 'libx264', '-preset', 'slow', '-crf', '25',
       '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', os.path.join(OUT, 'gameplay-720.mp4'))
# rezerva WebM (VP9) pentru browserele fara H.264
ffmpeg('-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.jpg'), '-vf', 'scale=1280:-2', '-c:v', 'libvpx-vp9', '-crf', '36', '-b:v', '0',
       '-row-mt', '1', '-deadline', 'good', '-cpu-used', '2', '-an', os.path.join(OUT, 'gameplay.webm'))
Image.open(os.path.join(tmp, '0000.jpg')).save(os.path.join(OUT, 'gameplay-poster.webp'), quality=80)
Image.open(os.path.join(tmp, '0000.jpg')).resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, 'gameplay-poster.jpg'), quality=84)

# ---------------- GIF pentru README (8 secunde, bucla separata)
g = os.path.join(CAP, 'gif'); shutil.rmtree(g, ignore_errors=True); os.makedirs(g)
m = 8 * FPS + K; k = 0
for j in range(K):
    a = Image.open(cadre[m - K + j]).convert('RGB'); b = Image.open(cadre[j]).convert('RGB')
    Image.blend(a, b, j / K).save(os.path.join(g, '%04d.jpg' % k), quality=95); k += 1
for i in range(K, m - K):
    shutil.copy(cadre[i], os.path.join(g, '%04d.jpg' % k)); k += 1
ffmpeg('-framerate', str(FPS), '-i', os.path.join(g, '%04d.jpg'), '-vf',
       'fps=15,scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96:stats_mode=full[p];[b][p]paletteuse=dither=none',
       '-loop', '0', os.path.join(OUT, 'gameplay.gif'))

# ---------------- imagini
def webp(src, dst, size=None, q=82):
    im = Image.open(os.path.join(CAP, src)).convert('RGB')
    if size: im = im.resize(size, Image.LANCZOS)
    im.save(os.path.join(OUT, dst), quality=q, method=6)

for name in ['prim-trecere', 'prim-pasaj', 'prim-giratoriu', 'prim-semafor', 'prim-depozit', 'prim-magazin']:
    webp(name + '.png', name + '.webp', (1200, 800))
for ci in range(5):
    webp('oras-%d.png' % ci, 'oras-%d.webp' % ci, (1200, 750), 80)
for k in range(1, 6):
    webp('captura-%d.png' % k, 'captura-%d.webp' % k, None, 84)
    webp('captura-%d.png' % k, 'captura-%d-mic.webp' % k, (800, 450), 82)
    shutil.copy(os.path.join(CAP, 'captura-%d.png' % k), os.path.join(ROOT, 'store', 'screenshot_%d.png' % k))
webp('telefon-vertical.png', 'telefon-vertical.webp', (585, 1266), 84)
webp('telefon-orizontal.png', 'telefon-orizontal.webp', (1266, 585), 84)
Image.open(os.path.join(CAP, 'og.png')).convert('RGB').save(os.path.join(OUT, 'og.jpg'), quality=88)

tot = 0
for f in sorted(os.listdir(OUT)):
    sz = os.path.getsize(os.path.join(OUT, f)); tot += sz
    print('%-28s %7.0f KB' % (f, sz / 1024))
print('total docs/media: %.1f MB' % (tot / 1048576))
