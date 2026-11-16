#!/usr/bin/env python3
"""MOTOR ESTILO D · põe as PAUSAS de uma narração na cadência da referência, sem mexer na fala.

uso: aperta_pausas.py <voz.wav> <alinhamento.json> <saida.wav> [fim_de_frase=0.14] [virgula=0.09] [resto=0.07]

Medido na narradora da referência (trechos de 60 ms ou mais com a voz 25 dB abaixo da fala forte): 18 pausas somando
1,6 s em 32 s (5 % do tempo), a maior com 0,17 s; o normal é 0,06-0,12 s. As vozes sintéticas fazem 40-50 pausas somando
9-12 s (21-25 %), com 0,5-0,7 s entre frases — é isso que deixa o reel lento, não a velocidade da fala.

Aqui cada pausa (o maior trecho contínuo abaixo de -25 dB dentro do intervalo entre duas palavras do alinhamento) é
encurtada para o alvo do tipo dela: fim de frase, vírgula/dois-pontos, ou o resto. Sai o MIOLO da pausa; ficam 35 % do
alvo depois da palavra anterior e 65 % antes da seguinte (o ataque da palavra nunca é tocado), com 15 ms de cruzamento.
Nenhuma sílaba é cortada nem acelerada. Pausa que já é menor que o alvo fica como está."""
import sys, json, numpy as np, soundfile as sf
ent, alin, sai = sys.argv[1:4]
ALVO = {"frase": float(sys.argv[4]) if len(sys.argv) > 4 else 0.14, "virg": float(sys.argv[5]) if len(sys.argv) > 5 else 0.09,
        "resto": float(sys.argv[6]) if len(sys.argv) > 6 else 0.07}
LIMIAR_DB = -25.0
x, sr = sf.read(ent); x = x.mean(1) if x.ndim > 1 else x
al = json.load(open(alin))
h = int(sr * 0.005); n = len(x) // h
rms = np.sqrt(np.array([np.mean(x[k * h:(k + 1) * h] ** 2) for k in range(n)]) + 1e-12)
quieto = 20 * np.log10(rms / np.percentile(rms, 95)) < LIMIAR_DB
cortes = []                                   # (início, fim) em amostras a REMOVER
for a, b in zip(al, al[1:]):
    g0, g1 = max(0, int((a["fim"] - 0.08) * sr / h)), min(n, int((b["ini"] + 0.08) * sr / h))
    if g1 - g0 < 4:
        continue
    q = quieto[g0:g1]; melhor = (0, 0); i = 0          # o maior trecho contínuo de pausa dentro do intervalo
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if j - i > melhor[1] - melhor[0]: melhor = (i, j)
            i = j
        else:
            i += 1
    s0, s1 = (g0 + melhor[0]) * h, (g0 + melhor[1]) * h
    dur = (s1 - s0) / sr
    tipo = "frase" if a["w"].rstrip()[-1:] in ".?!" else "virg" if a["w"].rstrip()[-1:] in ",:;" else "resto"
    if dur > ALVO[tipo] + 0.03:
        c0 = s0 + int(ALVO[tipo] * 0.35 * sr); c1 = s1 - int(ALVO[tipo] * 0.65 * sr)
        if c1 - c0 > int(0.02 * sr):
            cortes.append((c0, c1))
xf = int(sr * 0.015); partes = []; pos = 0
for c0, c1 in cortes:
    partes.append(x[pos:c0].copy()); pos = c1
partes.append(x[pos:].copy())
y = partes[0]
for seg in partes[1:]:
    k = min(xf, len(y), len(seg))
    r = np.linspace(0, 1, k)
    y = np.concatenate([y[:-k], y[-k:] * (1 - r) + seg[:k] * r, seg[k:]])
sf.write(sai, y, sr, subtype="PCM_16")
print(f"pausas: {len(cortes)} encurtadas · {len(x) / sr:.2f} s -> {len(y) / sr:.2f} s (tirou {(len(x) - len(y)) / sr:.2f} s)")
