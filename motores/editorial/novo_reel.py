#!/usr/bin/env python3
"""Cria um projeto de reel a partir do motor.
uso: python3 novo_reel.py <pasta-destino> <fala.txt> "<título>" [nome-do-arquivo]
Copia base/ para a pasta, grava projeto.json, gera medir/texto.json e deixa cenas.py como modelo para preencher."""
import sys, os, shutil, json, subprocess, re
AQ = os.path.dirname(os.path.abspath(__file__)); dst, fala, tit = sys.argv[1], sys.argv[2], sys.argv[3]
nome = sys.argv[4] if len(sys.argv) > 4 else re.sub(r"[^a-z0-9]+", "-", tit.lower().encode("ascii", "ignore").decode()).strip("-")
if os.path.exists(dst): sys.exit(f"{dst} já existe")
shutil.copytree(os.path.join(AQ, "base"), dst)
for _p in ("narracao", "renders", "brutos", os.path.join("assets", "img")):   # o git não guarda pasta vazia: garante as do projeto
    os.makedirs(os.path.join(dst, _p), exist_ok=True)
shutil.copy(fala, os.path.join(dst, "narracao", "fala.txt"))
json.dump({"titulo": tit, "nome": nome}, open(os.path.join(dst, "projeto.json"), "w"), ensure_ascii=False, indent=1)
open(os.path.join(dst, ".rsa"), "w").write(os.path.abspath(os.path.join(AQ, "..", "..")).replace("\\", "/"))   # onde está a skill (o reel.sh lê)
subprocess.run([sys.executable, os.path.join(dst, "medir", "texto.py"), os.path.join(dst, "narracao", "fala.txt")], check=True)
print(f"projeto criado em {dst}. Próximo: gerar a voz (MOTOR.md §3) e rodar ./reel.sh voz <arquivo>")
