#!/usr/bin/env python3
"""Confere um efeito contra o molde da referência (bandas a cada 10 ms). uso: conferir_impacto.py arquivo.wav [molde.json]"""
import sys, os, json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
AQ = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(AQ, "molde-boom.json"))); T = np.array(M["db"]); BANDAS = M["bandas"]
y, sr = sf.read(sys.argv[1]); y = y.mean(1) if y.ndim > 1 else y; h = int(sr * 0.01)
B = np.array([[20 * np.log10(np.sqrt(np.mean(z[i:i + h] ** 2)) + 1e-9) for i in range(0, len(z) - h, h)][:T.shape[1]]
              for z in [sosfilt(butter(4, [a, b], "bandpass", fs=sr, output="sos"), y) for a, b in BANDAS]])
n = min(B.shape[1], T.shape[1]); B, T = B[:, :n], T[:, :n]
B += T.max() - B.max()                                   # mesma referência de nível (o pico do molde)
print("tempo  " + " ".join(f"{a}-{b}".rjust(11) for a, b in BANDAS) + "   (nosso/referência)")
for i in range(0, min(n, 60), 5): print(f"{-0.05 + i * 0.01:5.2f}  " + " ".join(f"{B[b, i]:5.0f}/{T[b, i]:<5.0f}" for b in range(len(BANDAS))))
ok = T > -45
print("ERRO MÉDIO onde o molde > -45 dB: %.1f dB" % np.mean(np.abs(B[ok] - T[ok])))
