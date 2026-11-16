#!/usr/bin/env python3
"""Mede a narração contra as metas do reel de referência (../referencia/metas.json do motor, ou medir/metas.json).
uso: voz_medir.py narracao.wav [n_palavras]   -> velocidade, pausas, % falando, entonação (semitons) e ênfase (dB)."""
import sys, os, json, numpy as np, soundfile as sf, librosa, warnings; warnings.filterwarnings("ignore")
AQ = os.path.dirname(os.path.abspath(__file__)); M = json.load(open(os.path.join(AQ, "metas.json")))["voz"]
p = sys.argv[1]; y, sr = sf.read(p); y = y.mean(1) if y.ndim > 1 else y
y = librosa.resample(y.astype(np.float32), orig_sr=sr, target_sr=16000); sr = 16000
db = 20 * np.log10(librosa.feature.rms(y=y, frame_length=640, hop_length=160)[0] + 1e-9); sil = db < np.percentile(db, 95) - 30
ps = []; i = 0
while i < len(sil):
    if sil[i]:
        j = i
        while j < len(sil) and sil[j]: j += 1
        ps.append((j - i) * 0.01); i = j
    else: i += 1
ps = np.array(ps[1:-1]); ps = ps[ps > 0.15]
f0, _, _ = librosa.pyin(y, fmin=60, fmax=400, sr=sr, hop_length=320); f = f0[~np.isnan(f0)]; st = 12 * np.log2(f / np.median(f)); st = st[abs(st) < 10]
seg = [db[k:k + 50][~sil[k:k + 50]].mean() for k in range(0, len(db) - 50, 50) if (~sil[k:k + 50]).sum() > 20]
n = int(sys.argv[2]) if len(sys.argv) > 2 else len(json.load(open(os.path.join(AQ, "texto.json"))))
r = {"palavras_min": round(n / (len(y) / sr - 0.3) * 60), "pausa_max_s": round(float(ps.max()), 2) if len(ps) else 0, "fala_ativa": round(float((~sil).mean()), 2),
     "entonacao_st": round(float(st.std()), 2), "enfase_db": round(float(np.std(seg)), 2), "f0_hz": round(float(np.median(f)))}
T = M["tolerancia"]; ok = {"palavras_min": T["palavras_min"][0] <= r["palavras_min"] <= T["palavras_min"][1], "pausa_max_s": T["pausa_max_s"][0] <= r["pausa_max_s"] <= T["pausa_max_s"][1],
                           "fala_ativa": T["fala_ativa"][0] <= r["fala_ativa"] <= T["fala_ativa"][1], "entonacao_st": r["entonacao_st"] <= T["entonacao_st_max"], "enfase_db": r["enfase_db"] >= T["enfase_db_min"]}
for k, v in r.items(): print(f"{k:13s} {v:>7}   original {M[k]:>6}   {'' if k not in ok else ('ok' if ok[k] else 'FORA')}")
print("VOZ:", "APROVADA" if all(ok.values()) else "fora da meta em " + ", ".join(k for k, v in ok.items() if not v))
