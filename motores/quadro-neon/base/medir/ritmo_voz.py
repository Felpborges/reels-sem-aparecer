#!/usr/bin/env python3
"""ESTILO C · leva a narração à CADÊNCIA medida no narrador da referência (pericia/DESMONTE-C.md §10):
  - pausas CURTAS e IGUAIS (o metrônomo do C): ponto 0,27 s · depois do gancho 0,27 · pergunta do CTA -> ordem 0,17
  - vírgula: na PROVA pausa 0,26 s (antes do "vende..."), na LISTA 0,22 s entre itens; na tese/reframe/CTA a vírgula não pausa
  - velocidade por ATO (palavras/min dentro da frase; calibrado no teste de 13/11 para dar ~165/min no total, como o original):
      gancho 200 · ponte 200 · tese 218 · reframe 192 · prova 162 · sintese 210 · lista 158 · CTA pergunta 280 · CTA ordem 210
  - nenhum corte dentro de palavra: cada trecho é recortado pelo alinhamento e acelerado sem mudar o tom (rubberband R3).
uso: ritmo_voz.py bruta.wav alinhamento_bruto.json saida.wav     (usa medir/frases.json gerado pelo texto.py)"""
import sys, os, json, subprocess, tempfile, numpy as np, soundfile as sf
AQ = os.path.dirname(os.path.abspath(__file__))
ent, aln, sai = sys.argv[1:4]
A = json.load(open(aln)); F = json.load(open(os.path.join(AQ, "frases.json")))
WPM = {"gancho": 200, "ponte": 200, "tese": 218, "reframe": 192, "prova": 162, "sintese": 210, "lista": 158, "cta": 210, "cta?": 280}
PAUSA_VIRG = {"prova": 0.26, "lista": 0.22}
PAUSA = {".": 0.27, "!": 0.27, "?": 0.17}
y, sr = sf.read(ent); y = y.mean(1) if y.ndim > 1 else y
tmp = tempfile.mkdtemp(); out = [np.zeros(int(sr * 0.12))]; fade = int(sr * 0.008); k = 0
def trecho(i0, i1, wpm):
    """recorta as palavras i0..i1 (silêncio interno do TTS cai para 0,05 s) e leva à velocidade-alvo"""
    global k
    a = max(0.0, A[i0]["start"] - 0.03); b = A[i1]["end"] + 0.05
    partes, c0 = [], a
    for w in range(i0, i1):
        if A[w + 1]["start"] - A[w]["end"] > 0.09:
            partes += [y[int(c0 * sr):int((A[w]["end"] + 0.03) * sr)], np.zeros(int(sr * 0.05))]; c0 = A[w + 1]["start"] - 0.03
    partes.append(y[int(c0 * sr):int(b * sr)]); seg = np.concatenate(partes)
    seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    n = i1 - i0 + 1; alvo = n / wpm * 60 + 0.08
    fator = min(max((len(seg) / sr) / alvo, 0.80), 1.60)
    k += 1; p_in, p_out = f"{tmp}/{k}a.wav", f"{tmp}/{k}b.wav"; sf.write(p_in, seg, sr)
    subprocess.run(["rubberband", "-3", "-q", "-T", f"{fator:.4f}", "--formant", p_in, p_out], check=True)
    s2, _ = sf.read(p_out); return (s2 if s2.ndim == 1 else s2.mean(1)), fator
for j, f in enumerate(F):
    ato = f["ato"]; wpm = WPM["cta?" if (ato == "cta" and f["pont"] == "?") else ato]
    cortes = [v for v in f.get("virgulas", []) if ato in PAUSA_VIRG]
    ini = f["ini"]; fs = []
    for c in cortes + [f["fim"]]:
        s, fa = trecho(ini, c, wpm); out.append(s); fs.append(fa)
        if c != f["fim"]: out.append(np.zeros(int(sr * PAUSA_VIRG[ato])))
        ini = c + 1
    p = 0 if j == len(F) - 1 else PAUSA.get(f["pont"], 0.27)
    if j < len(F) - 1: out.append(np.zeros(int(sr * p)))
    print(f"{j + 1:2d} {ato:8s} {f['fim'] - f['ini'] + 1:2d} pal  {wpm}/min  x{np.mean(fs):.2f}  {len(cortes)} vírgula(s) com pausa  pausa depois {p:.2f}")
out.append(np.zeros(int(sr * 0.45))); r = np.concatenate(out); sf.write(sai, r, sr)
tot = sum(f["fim"] - f["ini"] + 1 for f in F); print(f"final {len(r) / sr:.2f} s · {tot / (len(r) / sr - 0.57) * 60:.0f} palavras/min (original 167)")
