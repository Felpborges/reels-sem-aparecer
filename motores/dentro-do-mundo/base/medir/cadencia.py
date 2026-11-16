#!/usr/bin/env python3
"""Cadência do ESTILO B, contra as metas medidas no original (medir/metas.json).
uso: cadencia.py [medir/elementos.json]   (gerado pelo build.py)
Regras: duração do mundo, respiro antes do corte, corte na 1ª palavra da frase, maior vazio sem novidade,
mundo longo com evento interno, fração em faixa quadrada, densidade."""
import json, os, sys, statistics as S
AQ = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(AQ, "metas.json")))["cenas"]
E = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQ, "elementos.json")))
W = json.load(open(os.path.join(AQ, "alinhamento.json")))
dur = E["duracao"]; mund = E["mundos"]; A = E["anims"]
ini = [m["t"] for m in mund]; fim = ini[1:] + [dur]
NOVO = {"in", "assenta", "digita", "risco", "conta"}
ev = sorted(a["t"] for a in A if a["k"] in NOVO or a.get("novo"))
dig = [(a["t"], a["t"] + (a.get("d") or 0)) for a in A if a["k"] in ("digita", "conta")]   # novidade contínua
mov = sorted([a["t"] for a in A if a["k"] in ("ft", "luz")] + [k[0] for c in E.get("cams", []) for k in c["k"][1:]])
falhas, linhas = [], []
for k, m in enumerate(mund):
    a, b = ini[k], fim[k]; d = b - a
    els = [t for t in ev if a - 0.05 <= t < b - 0.02]
    ult = max(els) if els else a
    dig_fim = False
    for t0, t1 in dig:                                  # digitação/contador contam como novidade contínua
        if a <= t0 < b and min(t1, b) > ult: ult = min(t1, b); dig_fim = True
    resp = b - ult
    # maior vazio sem novidade: tempo descoberto entre eventos (intervalos de digitação cobrem)
    pts = sorted(set([a, b] + els + [x for t0, t1 in dig for x in (t0, t1) if a <= x <= b]))
    vaz = 0; corrido = 0
    for x, y in zip(pts, pts[1:]):
        cobre = any(t0 <= x and t1 >= y for t0, t1 in dig)
        corrido = 0 if (cobre or x in els) else corrido
        if not cobre: corrido += y - x; vaz = max(vaz, corrido)
        if y in els: corrido = 0
    # corte na 1ª palavra: existe palavra começando entre 0 e 0,30 s depois do corte (o 1º mundo é livre)
    prox = [w["start"] - a for w in W if -0.06 <= w["start"] - a <= M["corte_antes_palavra_max_s"]]
    interno = [t for t in mov if a + 0.3 < t < b - 0.2]
    ok = {"dur": d >= M["mundo_min_s"] - 0.02, "resp": (k == len(mund) - 1) or resp >= (M["respiro_digitado_min_s"] if dig_fim else M["respiro_min_s"]),
          "vazio": vaz <= M["vazio_max_s"], "corte": k == 0 or m.get("entrada") in ("zoom", "flash") or bool(prox),
          "longo": d <= 3.0 or len(interno) >= max(1, int(d / M["evento_interno_cada_s"]))}
    linhas.append(f"{k + 1:2d} {m['nome'][:14]:14s} {a:6.2f}-{b:6.2f} {d:5.2f}s  {len(els):2d} elem  respiro {resp:4.2f}  vazio {vaz:4.2f}  "
                  f"{'faixa' if m['fmt'] == 'faixa' else '9:16 '}  " + " ".join(n.upper() for n, v in ok.items() if not v))
    falhas += [f"mundo {k + 1} ({m['nome']}): {n}" for n, v in ok.items() if not v]
print("\n".join(linhas))
ds = [f - i for i, f in zip(ini, fim)]
fx = sum(f - i for i, f, m in zip(ini, fim, mund) if m["fmt"] == "faixa") / dur
print(f"\nmundos {len(mund)} · mediana {S.median(ds):.2f} s (original {M['mundo_mediana_s']}) · em faixa {fx:.0%} (original {M['faixa_fracao']:.0%})")
if not (M["faixa_fracao_min"] <= fx <= M["faixa_fracao_max"]): falhas.append(f"fração em faixa {fx:.0%} fora de {M['faixa_fracao_min']:.0%}-{M['faixa_fracao_max']:.0%}")
if not (M["mundo_mediana_min_s"] <= S.median(ds) <= M["mundo_mediana_max_s"]): falhas.append(f"mediana dos mundos {S.median(ds):.2f} s fora da faixa")
print("CADÊNCIA:", "APROVADA" if not falhas else "REPROVADA\n  - " + "\n  - ".join(falhas))
sys.exit(1 if falhas else 0)
