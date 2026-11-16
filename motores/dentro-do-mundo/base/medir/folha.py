#!/usr/bin/env python3
"""ESTILO B · folha de conferência: para cada MUNDO, o quadro do meio e o último (o estado mais cheio). uso: folha.py video.mp4 saida.jpg"""
import sys, json, subprocess, os, tempfile
from PIL import Image, ImageDraw
v, out = sys.argv[1], sys.argv[2]; AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = json.load(open(os.path.join(AQ, "medir", "elementos.json"))); m = E["mundos"]
t = [x["t"] for x in m] + [E["duracao"]]; W, H = 216, 384; cols = 8; n = len(m) * 2; rows = (n + cols - 1) // cols
sh = Image.new("RGB", (W * cols, H * rows), "white"); d = ImageDraw.Draw(sh); tmp = tempfile.mkdtemp(); k = 0
for i, (a, b) in enumerate(zip(t, t[1:])):
    for tt, rot in (((a + b) / 2, "meio"), (max(a, b - 0.1), "fim")):
        p = f"{tmp}/{k}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{tt:.2f}", "-i", v, "-frames:v", "1", "-vf", f"scale={W}:{H}", p])
        x, y = (k % cols) * W, (k // cols) * H; sh.paste(Image.open(p), (x, y))
        d.rectangle([x, y, x + W, y + 18], fill="black"); d.text((x + 4, y + 3), f"{i + 1} {m[i]['nome'][:12]} · {rot} {tt:.1f}s", fill="yellow"); k += 1
sh.save(out, quality=82); print(out)
