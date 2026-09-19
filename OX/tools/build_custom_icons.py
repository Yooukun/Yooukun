#!/usr/bin/env python3
"""Deterministic resizing/compositing requested by user; no AI logo redraw."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
from manage import ROOT, BASE

OUT=ROOT/'icons/custom'
SIZE=432
records=[]

def save(name, canvas, source, operation):
    mask=Image.new('L',(SIZE,SIZE),0)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,SIZE-1,SIZE-1),radius=86,fill=255)
    canvas.putalpha(mask)
    canvas.resize((108,108),Image.Resampling.LANCZOS).save(OUT/(name+'.png'))
    data=(OUT/(name+'.png')).read_bytes()
    records.append({'path':'custom/'+name+'.png','source_url':source,'operation':operation,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})

def framed(name, path, bg, source, margin=40):
    original=Image.open(path).convert('RGBA')
    box=original.getbbox()
    if box: original=original.crop(box)
    image=ImageOps.contain(original,(SIZE-margin*2,SIZE-margin*2),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(SIZE,SIZE),bg)
    canvas.alpha_composite(image,((SIZE-image.width)//2,(SIZE-image.height)//2))
    save(name,canvas,source,'Preserve mark; alpha crop, proportional fit, rounded square; 108x108 RGBA PNG')

def main():
    framed('claude-v1',OUT/'sources/claude-vector.png','#faf7f2','https://claude.com/ (official inline wordmark SVG, isolated mark path)',60)
    framed('riot-v1',OUT/'sources/riot-original.png','#080808','https://www.riotgames.com/assets/img/meta/87021767499a895b42bbe1e6a9edaf27/apple-touch-icon-precomposed-180x180.png',0)
    framed('netease-v1',ROOT/'icons/mini/Color/neteasemusic--dfb008e11754.png','#ff3036','../mini/Color/neteasemusic--dfb008e11754.png',0)
    framed('pornhub-v1',ROOT/'icons/qure/Color/Pornhub_2--45a52609fa30.png','#121212','../qure/Color/Pornhub_2--45a52609fa30.png',40)
    framed('india-v1',ROOT/'icons/qure/Color/India--3630dde4f0ca.png','#f5f5f5','../qure/Color/India--3630dde4f0ca.png',15)
    swiss=Image.new('RGBA',(SIZE,SIZE),'#da291c')
    draw=ImageDraw.Draw(swiss)
    draw.rectangle((180,100,251,331),fill='white')
    draw.rectangle((100,180,331,251),fill='white')
    save('switzerland-v1',swiss,'Geometric national flag motif: red field, centered white cross','Original geometric UI rendering, not an official flag specification')
    dutch=Image.new('RGBA',(SIZE,SIZE),'white')
    draw=ImageDraw.Draw(dutch)
    draw.rectangle((0,0,SIZE,143),fill='#ae1c28')
    draw.rectangle((0,288,SIZE,431),fill='#21468b')
    save('netherlands-v1',dutch,'Geometric national flag motif: red white blue horizontal bands','Original geometric UI rendering, rounded square adaptation')
    (OUT/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    override={'Claude':'claude-v1','Riot游戏':'riot-v1','网易云音乐':'netease-v1','Pornhub':'pornhub-v1','印度':'india-v1','瑞士':'switzerland-v1','荷兰':'netherlands-v1'}
    (ROOT/'icons/overrides.json').write_text(json.dumps({k:BASE+'/icons/custom/'+v+'.png' for k,v in override.items()},ensure_ascii=False,indent=2)+'\n')
    for source in (OUT/'sources').glob('*.png'):
        print(source.name,hashlib.sha256(source.read_bytes()).hexdigest())
    print('Built 7 deterministic 108x108 RGBA icons; original sources retained.')

if __name__=='__main__': main()
