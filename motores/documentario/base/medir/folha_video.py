#!/usr/bin/env python3
"""Folhas de conferência no olho: um quadro a cada 0,5 s (24 por folha), com o tempo. uso: folha_video.py <video> <prefixo>"""
import sys, subprocess, io
from PIL import Image, ImageDraw
v, pre = sys.argv[1], sys.argv[2]
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout)
ts = [k * 0.5 + 0.25 for k in range(int(dur / 0.5))]
for f in range(0, len(ts), 24):
    lote = ts[f:f + 24]; sheet = Image.new('RGB', (8 * 180, 3 * 340), 'white'); d = ImageDraw.Draw(sheet)
    for k, t in enumerate(lote):
        b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', v, '-frames:v', '1', '-vf', 'scale=176:313', '-f', 'image2', '-c:v', 'png', '-'], capture_output=True).stdout
        x, y = (k % 8) * 180, (k // 8) * 340
        sheet.paste(Image.open(io.BytesIO(b)), (x + 2, y + 20)); d.text((x + 4, y + 4), f'{t:.2f}s', fill='black')
    sheet.save(f'{pre}-{f // 24 + 1:02d}.jpg', quality=85); print(f'{pre}-{f // 24 + 1:02d}.jpg')
