#!/usr/bin/env python3
"""ESTILO C · agrupa medir/auditoria.json em problemas (seção, elemento, tipo) -> intervalos e palavras.
Reprova: corte/coberta/encosta/zona-ig por 2+ quadros PARADOS, rente por > 0,3 s. Movimento (entrada deslizando) é tolerado."""
import json, os, sys, collections
AQ = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(AQ, "auditoria.json"))); S = json.load(open(os.path.join(AQ, "elementos.json")))["secoes"]
def sec(t):
    m = [x for x in S if x["t"] <= t + 1e-6]; return m[-1]["nome"] if m else "?"
G = collections.defaultdict(lambda: {"ts": [], "w": collections.Counter()}); ant = {}
for f in A:
    pos = {}
    for p in f["palavras"]:
        key = (p["id"], p["w"]); pos[key] = (p["x"], p["y"]); o = ant.get(key)
        anda = o is None or abs(o[0] - p["x"]) + abs(o[1] - p["y"]) > 3
        for i in p["iss"]:
            tipo = i.split(":")[0]
            if anda and tipo in ("corte", "fora", "encosta", "coberta", "rente"): tipo += "(movendo)"
            if tipo.startswith("fora"): continue
            k = (sec(f["t"]), p["id"], tipo); G[k]["ts"].append(f["t"]); G[k]["w"][p["w"]] += 1
    ant = pos
graves = [(k, v) for k, v in G.items() if k[2] in ("corte", "coberta", "encosta", "zona-ig") and len(set(v["ts"])) >= 2]
rentes = [(k, v) for k, v in G.items() if k[2] == "rente" and len(set(v["ts"])) / 30 > 0.3]
for k, v in sorted(G.items(), key=lambda kv: kv[1]["ts"][0]):
    ts = sorted(set(v["ts"]))
    print(f"{k[0]:10s} {k[1]:8s} {k[2]:18s} {len(ts) / 30:5.2f}s  {ts[0]:.2f}-{ts[-1]:.2f}  palavras: {', '.join(w for w, _ in v['w'].most_common(6))}")
print(f"\nquadros auditados: {len(A)}")
print("AUDITORIA:", "APROVADA (nenhuma palavra cortada, coberta, encostada ou na zona do Instagram com a tela parada)" if not graves and not rentes
      else f"REPROVADA: {len(graves)} problema(s) grave(s) e {len(rentes)} rente(s) à borda")
sys.exit(1 if graves or rentes else 0)
