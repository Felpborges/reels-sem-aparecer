#!/usr/bin/env python3
"""ESTILO C · mede a narração (já com tom e cadência) contra o narrador do original (medir/metas.json -> voz).
uso: voz_medir.py narracao.wav alinhamento.json"""
import sys, os, json, numpy as np, librosa, warnings; warnings.filterwarnings("ignore")
AQ = os.path.dirname(os.path.abspath(__file__)); M = json.load(open(os.path.join(AQ, "metas.json")))["voz"]; T_ = M["tolerancia"]
y, sr = librosa.load(sys.argv[1], sr=16000, mono=True); A = json.load(open(sys.argv[2]))
db = 20 * np.log10(librosa.feature.rms(y=y, frame_length=640, hop_length=160)[0] + 1e-9); sil = db < np.percentile(db, 95) - 30
ps, i = [], 0
while i < len(sil):
    if sil[i]:
        j = i
        while j < len(sil) and sil[j]: j += 1
        ps.append((j - i) * 0.01); i = j
    else: i += 1
ps = np.array(ps[1:-1]); ps = ps[ps > 0.12]
f0, _, _ = librosa.pyin(y, fmin=50, fmax=300, sr=sr, hop_length=320); g = f0[~np.isnan(f0)]; st = 12 * np.log2(g / np.median(g)); st = st[abs(st) < 10]
seg = [db[k:k + 50][~sil[k:k + 50]].mean() for k in range(0, len(db) - 50, 50) if (~sil[k:k + 50]).sum() > 20]
r = {"palavras_min": round(len(A) / (A[-1]["end"] - A[0]["start"]) * 60), "pausa_media_s": round(float(ps.mean()), 2), "pausa_max_s": round(float(ps.max()), 2),
     "fala_ativa": round(float((~sil).mean()), 2), "entonacao_st": round(float(st.std()), 2), "enfase_db": round(float(np.std(seg)), 2), "f0_hz": round(float(np.median(g)))}
ok = {"palavras_min": T_["palavras_min"][0] <= r["palavras_min"] <= T_["palavras_min"][1], "pausa_media_s": T_["pausa_media_s"][0] <= r["pausa_media_s"] <= T_["pausa_media_s"][1],
      "pausa_max_s": T_["pausa_max_s"][0] <= r["pausa_max_s"] <= T_["pausa_max_s"][1], "entonacao_st": r["entonacao_st"] <= T_["entonacao_st_max"], "enfase_db": r["enfase_db"] >= T_["enfase_db_min"]}
for k, v in r.items(): print(f"{k:13s} {v:>7}   original {M[k]:>6}   {'' if k not in ok else ('ok' if ok[k] else 'FORA')}")
print("VOZ:", "APROVADA" if all(ok.values()) else "fora da meta em " + ", ".join(k for k, v in ok.items() if not v))
