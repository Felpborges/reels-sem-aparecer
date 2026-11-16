#!/usr/bin/env python3
"""Folha de conferência: o último quadro de cada cena (o estado mais cheio), 10 por linha. uso: folha.py video.mp4 saida.jpg"""
import sys, json, subprocess, os, tempfile
from PIL import Image, ImageDraw
v, out = sys.argv[1], sys.argv[2]; AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(os.path.join(AQ, "medir", "eventos.json")))["cenas"]; dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v], capture_output=True, text=True).stdout)
t = [x["t"] for x in c] + [dur]; W, H = 270, 480; cols = 10; rows = (len(c) + cols - 1) // cols
sh = Image.new("RGB", (W * cols, H * rows), "white"); d = ImageDraw.Draw(sh); tmp = tempfile.mkdtemp()
for i, (a, b) in enumerate(zip(t, t[1:])):
    tt = max(a, b - 0.12); p = f"{tmp}/{i}.png"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{tt:.2f}", "-i", v, "-frames:v", "1", "-vf", f"scale={W}:{H}", p])
    sh.paste(Image.open(p), ((i % cols) * W, (i // cols) * H)); d.text(((i % cols) * W + 6, (i // cols) * H + 6), f"{i + 1} · {a:.1f}s", fill="red")
sh.save(out, quality=82); print(out)
