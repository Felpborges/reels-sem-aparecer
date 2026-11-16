#!/usr/bin/env python3
"""ESTILO B · ferramenta opcional (quando a ênfase da voz fica abaixo da meta): aplica o contorno de força medido no narrador do original
(1ª palavra da frase é a mais forte, a frase termina caindo) e desacelera de leve o conjunto.
uso: acento.py narracao.wav alinhamento.json saida.wav saida-alinhamento.json [db_ini=2.5] [db_fim=-2.5] [tempo=0.97]"""
import sys, os, json, subprocess, tempfile, numpy as np, soundfile as sf
AQ = os.path.dirname(os.path.abspath(__file__))
ent, aln, sai, sai_aln = sys.argv[1:5]
DI = float(sys.argv[5]) if len(sys.argv) > 5 else 2.5; DF = float(sys.argv[6]) if len(sys.argv) > 6 else -2.5
TEMPO = float(sys.argv[7]) if len(sys.argv) > 7 else 0.97
A = json.load(open(aln)); F = json.load(open(os.path.join(AQ, "frases.json")))
y, sr = sf.read(ent); y = y.mean(1) if y.ndim > 1 else y
g = np.zeros(len(y))                                   # ganho em dB por amostra
for f in F:
    a, b = A[f["ini"]]["start"], A[f["fim"]]["end"]
    i0, i1 = int(a * sr), int(b * sr)
    if i1 <= i0: continue
    g[i0:i1] = np.linspace(DI, DF, i1 - i0)
k = int(sr * 0.03); g = np.convolve(g, np.ones(k) / k, mode="same")   # rampa suave, sem clique
z = y * 10 ** (g / 20); z *= 0.97 / max(1e-9, np.abs(z).max()) if np.abs(z).max() > 0.97 else 1
tmp = tempfile.mkdtemp(); sf.write(f"{tmp}/a.wav", z, sr)
subprocess.run(["rubberband", "-3", "-q", "-T", f"{TEMPO}", "--formant", f"{tmp}/a.wav", sai], check=True)
json.dump([dict(w, start=round(w["start"] / TEMPO, 3), end=round(w["end"] / TEMPO, 3)) for w in A], open(sai_aln, "w"), ensure_ascii=False, indent=1)
print(f"acento {DI:+.1f}→{DF:+.1f} dB por frase · tempo x{TEMPO} · {len(sf.read(sai)[0]) / sr:.2f} s")
