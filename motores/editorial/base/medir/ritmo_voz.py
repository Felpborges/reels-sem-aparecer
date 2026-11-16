#!/usr/bin/env python3
"""Leva a narração ao ritmo do reel de referência: encurta as pausas internas para a distribuição do original
(média ~0,25 s, máx ~0,39 s) e depois acelera sem mudar o tom (rubberband R3) até a duração alvo.
uso: ritmo_voz.py entrada.wav saida.wav [duracao_alvo_s | auto]   (auto = nº de palavras de medir/texto.json a 212/min)"""
import sys, subprocess, numpy as np, soundfile as sf
ent, sai = sys.argv[1], sys.argv[2]
if len(sys.argv) < 4 or sys.argv[3] == "auto":            # 212 palavras/min, o ritmo do original (211), + respiro do começo/fim
    import json, os
    n = len(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "texto.json"))))
    alvo = round(n / 212 * 60 + 0.35, 2)
else:
    alvo = float(sys.argv[3])
y, sr = sf.read(ent); y = y.mean(1) if y.ndim > 1 else y
hop = int(sr * 0.01); n = len(y) // hop
db = np.array([20 * np.log10(np.sqrt(np.mean(y[i * hop:(i + 1) * hop] ** 2)) + 1e-9) for i in range(n)])
sil = db < np.percentile(db, 95) - 32
# silêncios (em quadros de 10 ms)
runs = []; i = 0
while i < n:
    if sil[i]:
        j = i
        while j < n and sil[j]: j += 1
        runs.append((i, j)); i = j
    else: i += 1
ini = runs[0][1] if runs and runs[0][0] == 0 else 0
fim = runs[-1][0] if runs and runs[-1][1] == n else n
pedacos = []; cur = ini * hop; fade = int(sr * 0.012)
for a, b in runs:
    if a <= ini or b >= fim: continue
    d = (b - a) * 0.01
    if d < 0.12: continue
    novo = min(0.40, 0.14 + (d - 0.12) * 0.8)             # aproxima da distribuição do original (média 0,25 s, máx 0,39 s, uma a cada ~3,6 s)
    corta = d - novo
    meio = (a + b) / 2 * hop
    c0 = int(meio - corta * sr / 2); c1 = int(meio + corta * sr / 2)
    pedacos.append(y[cur:c0]); cur = c1
pedacos.append(y[cur:fim * hop])
out = pedacos[0]
for p in pedacos[1:]:                                       # junta com cruzamento curto (no silêncio, inaudível)
    r = np.linspace(0, 1, fade)
    out = np.concatenate([out[:-fade], out[-fade:] * (1 - r) + p[:fade] * r, p[fade:]])
out = np.concatenate([np.zeros(int(sr * 0.08)), out, np.zeros(int(sr * 0.25))])
sf.write(sai + ".tmp.wav", out, sr)
fator = (len(out) / sr) / alvo
print(f"original {len(y)/sr:.2f}s -> pausas encurtadas {len(out)/sr:.2f}s -> tempo x{fator:.3f}")
subprocess.run(["rubberband", "-3", "-q", "-T", f"{fator:.4f}", "--formant", sai + ".tmp.wav", sai], check=True)
import os; os.remove(sai + ".tmp.wav")
print("final", sf.info(sai).duration)
