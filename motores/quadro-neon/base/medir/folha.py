#!/usr/bin/env python3
"""folha.py VIDEO SAIDA_PREFIXO fps largura cols linhas [ini fim]  -> folhas de quadros com carimbo de tempo"""
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
v,pre,fps,W,C,L=sys.argv[1],sys.argv[2],float(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6])
ini=float(sys.argv[7]) if len(sys.argv)>7 else 0; fim=float(sys.argv[8]) if len(sys.argv)>8 else 999
H=int(W*16/9)
raw=subprocess.run(["ffmpeg","-v","error","-ss",str(ini),"-to",str(fim),"-i",v,"-vf",f"fps={fps},scale={W}:{H}","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
fr=np.frombuffer(raw,np.uint8).reshape(-1,H,W,3); n=C*L
f=ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc",14)
for k in range(0,len(fr),n):
    im=Image.new("RGB",(C*W,L*H),(40,0,40)); d=ImageDraw.Draw(im)
    for j,a in enumerate(fr[k:k+n]):
        x,y=(j%C)*W,(j//C)*H; im.paste(Image.fromarray(a),(x,y))
        t=ini+(k+j)/fps; d.rectangle([x,y,x+46,y+16],fill=(0,0,0)); d.text((x+2,y+1),f"{t:.2f}",fill=(255,255,0),font=f)
    im.save(f"{pre}-{k//n+1:02d}.jpg",quality=85); print(f"{pre}-{k//n+1:02d}.jpg")
