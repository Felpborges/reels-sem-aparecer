#!/usr/bin/env python3
"""Mede a narração contra a do original (metas.json > voz): palavras/min, pausas, tom e extensão."""
import json, os, sys, numpy as np, librosa
AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(AQ, "medir", "metas.json")))["voz"]
A = json.load(open(os.path.join(AQ, "medir", "alinhamento.json")))
ini = np.array([a["ini"] for a in A]); fim = np.array([a["fim"] for a in A]); gaps = ini[1:] - fim[:-1]
ppm = len(A) / (fim[-1] - ini[0]) * 60; pz = gaps[gaps > 0.12]
y, sr = librosa.load(os.path.join(AQ, "assets", "narracao.wav"), sr=16000)
f0, v, _ = librosa.pyin(y, fmin=60, fmax=400, sr=sr, frame_length=1024); f0 = f0[v]
ext = 12 * np.log2(np.nanpercentile(f0, 95) / np.nanpercentile(f0, 5))
ok = M["ppm_total"][0] <= ppm <= M["ppm_total"][1] and (len(pz) == 0 or pz.max() <= M["pausa_max_s"]) and ext >= M["extensao_st_min"]
print(f"voz: {ppm:.0f} palavras/min (meta {M['ppm_total']}) · pausas {pz.mean() if len(pz) else 0:.2f} s média, máx {pz.max() if len(pz) else 0:.2f} "
      f"(meta ≤ {M['pausa_max_s']}) · tom mediano {np.nanmedian(f0):.0f} Hz · extensão {ext:.1f} st (meta ≥ {M['extensao_st_min']})")
print("VOZ:", "APROVADA" if ok else "FORA DA META (veja acima; a voz definitiva é escolhida pelo Felipe)")
