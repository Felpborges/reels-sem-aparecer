#!/usr/bin/env python3
"""Agrupa medir/auditoria.json em problemas: (mundo, elemento, tipo) -> intervalos de tempo e palavras.
uso: auditoria_relatorio.py [--tudo]   (sem --tudo ignora 'pequena' e os 'fora' de elementos que estão saindo de cena)"""
import json, os, sys, collections
AQ = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(AQ, "auditoria.json"))); E = json.load(open(os.path.join(AQ, "elementos.json")))
mundos = E["mundos"]
def mundo(t):
    m = [x for x in mundos if x["t"] <= t + 1e-6]; return m[-1]["nome"] if m else "?"
G = collections.defaultdict(lambda: {"ts": [], "w": collections.Counter()})
tot = collections.Counter(); ant = {}
for f in A:
    pos = {}
    for p in f["palavras"]:
        key = (p["id"], p["k"], p["w"][:3]); pos[key] = (p["x"], p["y"])
        o = ant.get(key); anda = o is not None and abs(o[0] - p["x"]) + abs(o[1] - p["y"]) > 10
        for i in p["iss"]:
            tipo = i.split(":")[0]
            if tipo in ("corte", "fora", "vaza") and anda: tipo = tipo + "(movendo)"; i = tipo
            if tipo == "pequena" and "--tudo" not in sys.argv: continue
            k = (mundo(f["t"]), p["id"], i if tipo.startswith("coberta") else tipo)
            G[k]["ts"].append(f["t"]); G[k]["w"][p["w"]] += 1; tot[tipo] += 1
    ant = pos
def faixas(ts, passo=0.07):
    out = []; a = b = ts[0]
    for t in ts[1:]:
        if t - b > passo: out.append((a, b)); a = t
        b = t
    out.append((a, b)); return out
print(f"quadros auditados: {len(A)} · ocorrências por tipo: {dict(tot)}\n")
# veredito: corte/vaza/coberta/encosta PARADOS reprovam; rente parado por mais de 0,3 s reprova; o resto é transitório
graves = [(k, v) for k, v in G.items() if k[2].split(":")[0] in ("corte", "vaza", "coberta", "encosta", "borda")
          and len(set(v["ts"])) >= 2]          # 1 quadro isolado = o primeiro quadro de um movimento (ainda sem "anterior" p/ medir)
rentes = [(k, v) for k, v in G.items() if k[2] == "rente" and len(set(v["ts"])) / 30 > 0.3]
for k, v in sorted(G.items(), key=lambda kv: kv[1]["ts"][0]):
    ts = sorted(set(v["ts"])); fx = faixas(ts); dur = len(ts) / 30
    print(f"{k[0]:12s} {k[1]:10s} {k[2]:22s} {dur:5.2f}s  em {', '.join(f'{a:.2f}-{b:.2f}' for a, b in fx[:4])}{' …' if len(fx) > 4 else ''}")
    print(f"{'':12s} palavras: {', '.join(w for w, _ in v['w'].most_common(8))}")

print("\nAUDITORIA:", "APROVADA (nenhuma palavra cortada, vazando, coberta ou encostada com a câmera parada)" if not graves and not rentes else
      f"REPROVADA: {len(graves)} problema(s) grave(s) e {len(rentes)} palavra(s) rente(s) à borda por mais de 0,3 s")
sys.exit(1 if graves or rentes else 0)
