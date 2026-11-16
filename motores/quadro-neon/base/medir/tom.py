#!/usr/bin/env python3
"""ESTILO C (cópia independente da ferramenta do B) · ferramenta opcional: leva o TIMBRE da narração para o do narrador da referência (medido em
pericia/audio/sep/htdemucs/ref/vocals.wav, espectro médio em terços de oitava): mais grave (tom -SEMI semitons, formantes
preservados, duração intacta), mais peito em 100 Hz, menos "caixa" em 200-400 Hz, presença de locução em 1,6-5 kHz,
menos ar acima de 9 kHz e compressão de locução (fator de crista 20 -> 16 dB).
uso: tom.py entrada.wav saida.wav [semitons=-2]"""
import sys, subprocess, tempfile, numpy as np, soundfile as sf
from scipy.signal import lfilter
ent, sai = sys.argv[1:3]; SEMI = float(sys.argv[3]) if len(sys.argv) > 3 else -2.0
tmp = tempfile.mkdtemp()
subprocess.run(["rubberband", "-3", "-q", "-p", str(SEMI), "--formant", ent, f"{tmp}/p.wav"], check=True)
y, sr = sf.read(f"{tmp}/p.wav"); y = y.mean(1) if y.ndim > 1 else y
def bq(tipo, f0, g, q=0.707):                                # biquads do RBJ cookbook
    A = 10 ** (g / 40); w = 2 * np.pi * f0 / sr; c, s = np.cos(w), np.sin(w); al = s / (2 * q)
    if tipo == "pico":
        b = [1 + al * A, -2 * c, 1 - al * A]; a = [1 + al / A, -2 * c, 1 - al / A]
    else:
        r = 2 * np.sqrt(A) * al; sg = 1 if tipo == "grave" else -1
        b = [A * ((A + 1) - sg * (A - 1) * c + r), sg * 2 * A * ((A - 1) - sg * (A + 1) * c), A * ((A + 1) - sg * (A - 1) * c - r)]
        a = [(A + 1) + sg * (A - 1) * c + r, -sg * 2 * ((A - 1) + sg * (A + 1) * c), (A + 1) + sg * (A - 1) * c - r]
    return np.array(b) / a[0], np.array(a) / a[0]
for f in (("grave", 115, 4.5), ("pico", 260, -4.0, 0.9), ("pico", 1700, 5.0, 1.1), ("pico", 3200, 3.0, 0.9), ("agudo", 6500, -6.0)):
    b, a = bq(*f); y = lfilter(b, a, y)
# compressor de locução (RMS 10 ms, 2:1 acima do p95 - 4 dB relativo ao pico de fala, ataque 5 ms, soltura 90 ms)
y = y / np.abs(y).max() * 0.9
env = np.sqrt(np.convolve(y ** 2, np.ones(int(sr * .01)) / int(sr * .01), "same") + 1e-12); edb = 20 * np.log10(env)
thr = np.percentile(edb[edb > -50], 95) - 4; ganho = np.where(edb > thr, (thr - edb) * (1 - 1 / 1.4), 0.0)
at, rl = np.exp(-1 / (sr * .005)), np.exp(-1 / (sr * .09)); g = np.zeros_like(ganho); v = 0.0
for i, x in enumerate(ganho):
    v = at * v + (1 - at) * x if x < v else rl * v + (1 - rl) * x; g[i] = v
y = y * 10 ** (g / 20); y = y / np.abs(y).max() * 0.89
sf.write(sai, y, sr); print(f"tom {SEMI:+.1f} st · EQ de locução · compressão leve 1,4:1 -> {sai}")
