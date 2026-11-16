#!/usr/bin/env python3
"""ESTILO B · mede a narração contra o narrador do original (medir/metas.json -> voz).
uso: voz_medir.py narracao.wav [alinhamento.json]
Mede: palavras/min, pausas, % falando, entonação (semitons), ênfase (dB), f0, e o CONTORNO de cada frase
(o "% falando" é só informativo: a voz do original tem respiração e reverberação nas pausas, o TTS tem silêncio absoluto)
(ataque alto no começo, queda no fim: no original 90 % das frases começam acima da mediana e as com ponto final terminam abaixo)."""
import sys, os, json, numpy as np, soundfile as sf, librosa, warnings; warnings.filterwarnings("ignore")
AQ = os.path.dirname(os.path.abspath(__file__)); M = json.load(open(os.path.join(AQ, "metas.json")))["voz"]
p = sys.argv[1]; aln = sys.argv[2] if len(sys.argv) > 2 else os.path.join(AQ, "alinhamento.json")
y, sr = sf.read(p); y = y.mean(1) if y.ndim > 1 else y
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
f0, _, _ = librosa.pyin(y, fmin=55, fmax=400, sr=sr, hop_length=160); f = f0[~np.isnan(f0)]; med = np.median(f)
st = 12 * np.log2(f / med); st = st[abs(st) < 10]
seg = [db[k:k + 50][~sil[k:k + 50]].mean() for k in range(0, len(db) - 50, 50) if (~sil[k:k + 50]).sum() > 20]
A = json.load(open(aln)); n = len(A)
r = {"palavras_min": round(n / (A[-1]["end"] - A[0]["start"]) * 60), "pausa_max_s": round(float(ps.max()), 2) if len(ps) else 0,
     "pausa_media_s": round(float(ps.mean()), 2) if len(ps) else 0, "fala_ativa": round(float((~sil).mean()), 2), "entonacao_st": round(float(st.std()), 2), "enfase_db": round(float(np.std(seg)), 2), "f0_hz": round(float(med))}
# contorno por frase
fr_p = os.path.join(AQ, "frases.json"); sobe = desce = tot = totp = 0
if os.path.exists(fr_p):
    T = np.arange(len(f0)) * 0.01
    for fz in json.load(open(fr_p)):
        a, b = A[fz["ini"]]["start"], A[fz["fim"]]["end"]
        i0 = f0[(T >= a) & (T <= a + 0.4)]; i0 = i0[~np.isnan(i0)]; e0 = f0[(T >= b - 0.3) & (T <= b)]; e0 = e0[~np.isnan(e0)]
        if len(i0): tot += 1; sobe += np.median(i0) > med
        if len(e0) and fz["pont"] in ".!": totp += 1; desce += np.median(e0) < med
T_ = M["tolerancia"]
ok = {"palavras_min": T_["palavras_min"][0] <= r["palavras_min"] <= T_["palavras_min"][1], "pausa_max_s": T_["pausa_max_s"][0] <= r["pausa_max_s"] <= T_["pausa_max_s"][1],
      "pausa_media_s": T_["pausa_media_s"][0] <= r["pausa_media_s"] <= T_["pausa_media_s"][1], "entonacao_st": r["entonacao_st"] <= T_["entonacao_st_max"], "enfase_db": r["enfase_db"] >= T_["enfase_db_min"]}
for k, v in r.items(): print(f"{k:13s} {v:>7}   original {M[k]:>6}   {'' if k not in ok else ('ok' if ok[k] else 'FORA')}")
if tot: print(f"contorno: {sobe}/{tot} frases começam acima da mediana (original 90 %) · {desce}/{max(totp, 1)} com ponto terminam abaixo (original 100 %)")
print("VOZ:", "APROVADA" if all(ok.values()) else "fora da meta em " + ", ".join(k for k, v in ok.items() if not v))
