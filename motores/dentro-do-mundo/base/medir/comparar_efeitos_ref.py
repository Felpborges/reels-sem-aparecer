#!/usr/bin/env python3
"""Mede os efeitos da NOSSA mixagem (separada no demucs: medir/sep/htdemucs/nosso) do mesmo jeito que os da referência:
pico de 10 ms na soma drums+other+bass, em dB vs p90 do stem de voz. uso: comparar_efeitos_ref.py"""
import os, json, numpy as np, soundfile as sf
AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RD = os.path.join(AQ, "..", "pericia", "audio", "sep", "htdemucs", "ref")
ND = os.path.join(AQ, "medir", "sep", "htdemucs", "nosso"); sr = 44100; h = int(sr * 0.01)
def carrega(D):
    st = {k: sf.read(f"{D}/{k}.wav")[0].mean(1) for k in ("bass", "other", "drums", "vocals")}
    env = lambda y: 20 * np.log10(np.array([np.sqrt(np.mean(y[i:i + h] ** 2)) for i in range(0, len(y) - h, h)]) + 1e-9)
    ev = env(st["vocals"]); return env(st["drums"] + st["other"] + st["bass"]), np.percentile(ev[ev > ev.max() - 35], 90)
R, rp = carrega(RD); N, np_ = carrega(ND)
pico = lambda E, p, t: E[int((t - 0.25) * 100):int((t + 0.35) * 100)].max() - p
REF = {"impacto": [1.75, 4.35, 10.47, 15.66, 22.17, 28.15], "soco": [6.43], "queda": [8.15, 20.26], "whoosh": [1.05, 12.15, 28.8]}
S = json.load(open(os.path.join(AQ, "medir", "sons.json")))
print("tipo        REF (mediana)   NOSSO (mediana)   diferença")
for tipo, ts in REF.items():
    r = np.median([pico(R, rp, t) for t in ts])
    nos = [pico(N, np_, s["t"] + (0.15 if tipo != "whoosh" else 0)) for s in S if s["tipo"].split("-")[0] == tipo]
    if nos: print(f"{tipo:10s} {r:+8.1f}        {np.median(nos):+8.1f}          {np.median(nos) - r:+5.1f}   ({len(nos)} no nosso)")
