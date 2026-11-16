#!/usr/bin/env python3
"""Mostra cada palavra falada com o índice, o tempo e o ato — é o mapa para escrever cenas.py (P(i), CORTE(i))."""
import json, os
AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(os.path.join(AQ, "medir", "alinhamento.json")))
atos = json.load(open(os.path.join(AQ, "medir", "atos.json"))) if os.path.exists(os.path.join(AQ, "medir", "atos.json")) else [""] * len(A)
ult = None
for i, (a, ato) in enumerate(zip(A, atos)):
    if ato != ult:
        print(f"\n[{ato}]"); ult = ato
    print(f"  {i:3d} {a['ini']:6.2f}-{a['fim']:6.2f}  {a['w']}")
