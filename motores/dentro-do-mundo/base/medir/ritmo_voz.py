#!/usr/bin/env python3
"""ESTILO B · leva a narração ao TOM E CADÊNCIA medidos no narrador do original (estilo-b/pericia/audio/voz-frases.json):
  - dentro da frase: original 214 palavras/min (frase-chave 162, frase de até 4 palavras 265); em PT +7-10 %: 230 / 175 / 280
  - pausa ENTRE frases pela pontuação (medidas no original, gaps de 0,08 a 0,92 s, soma 6,1 s em 37 s):
    ponto 0,34 s · vírgula 0,20 · dois-pontos 0,40 · fim de parágrafo 0,50
    · depois da 1ª frase (o gancho) 0,75  -> total ~183 palavras/min, 88 % do tempo falando
  - nenhum corte dentro de palavra: cada frase é recortada pelo alinhamento e acelerada sem mudar o tom (rubberband R3).
uso: ritmo_voz.py bruta.wav alinhamento_bruto.json saida.wav     (usa medir/frases.json gerado pelo texto.py)"""
import sys, os, json, subprocess, tempfile, numpy as np, soundfile as sf
AQ = os.path.dirname(os.path.abspath(__file__))
ent, aln, sai = sys.argv[1:4]
A = json.load(open(aln)); F0 = json.load(open(os.path.join(AQ, "frases.json")))
# vírgula depois de 1-2 palavras ("Hoje,") não é frase: junta com a seguinte (no original não há pausa ali)
F = []
for f in F0:
    if F and F[-1].get("_junta"):
        g = F.pop(); f = dict(f, ini=g["ini"], chave=g.get("chave") or f.get("chave"))
    if f["pont"] == "," and f["fim"] - f["ini"] + 1 <= 2 and not f.get("paragrafo"): f = dict(f, _junta=True)
    F.append(f)
WPM = {"normal": 230, "chave": 175, "curta": 280}     # em PT as palavras são mais longas: +10 % sobre o original (214 / 162 / 265)
PAUSA = {".": 0.34, "!": 0.34, "?": 0.40, "…": 0.42, ",": 0.20, ";": 0.28, ":": 0.40}
y, sr = sf.read(ent); y = y.mean(1) if y.ndim > 1 else y
tmp = tempfile.mkdtemp(); out = [np.zeros(int(sr * 0.10))]; fade = int(sr * 0.008)
for k, f in enumerate(F):
    a = max(0.0, A[f["ini"]]["start"] - 0.03); b = A[f["fim"]]["end"] + 0.06
    n = f["fim"] - f["ini"] + 1
    tipo = "chave" if f.get("chave") else ("curta" if n <= 4 else "normal")
    alvo = n / WPM[tipo] * 60 + 0.09                      # duração-alvo da frase (com as bordas)
    # silêncio interno do TTS (entre palavras da mesma frase) cai para no máximo 0,06 s
    partes, c0 = [], a
    for w in range(f["ini"], f["fim"]):
        gap = A[w + 1]["start"] - A[w]["end"]
        if gap > 0.10:
            partes.append(y[int(c0 * sr):int((A[w]["end"] + 0.03) * sr)]); partes.append(np.zeros(int(sr * 0.06))); c0 = A[w + 1]["start"] - 0.03
    partes.append(y[int(c0 * sr):int(b * sr)]); seg = np.concatenate(partes)
    seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    fator = (len(seg) / sr) / alvo
    fator = min(max(fator, 0.80), 1.60)                  # nunca deforma demais
    p_in, p_out = f"{tmp}/{k}a.wav", f"{tmp}/{k}b.wav"; sf.write(p_in, seg, sr)
    subprocess.run(["rubberband", "-3", "-q", "-T", f"{fator:.4f}", "--formant", p_in, p_out], check=True)
    s2, _ = sf.read(p_out); out.append(s2 if s2.ndim == 1 else s2.mean(1))
    if k < len(F) - 1:
        p = 0.62 if k == 0 else (0.50 if f.get("paragrafo") else PAUSA.get(f["pont"], 0.38))
        out.append(np.zeros(int(sr * p)))
    print(f"{k + 1:2d} {tipo:6s} {n:2d} pal  x{fator:.2f}  pausa depois {0 if k == len(F) - 1 else p:.2f}")
out.append(np.zeros(int(sr * 0.25))); r = np.concatenate(out); sf.write(sai, r, sr)
tot = sum(f["fim"] - f["ini"] + 1 for f in F); print(f"final {len(r) / sr:.2f} s · {tot / (len(r) / sr - 0.35) * 60:.0f} palavras/min (alvo 183)")
