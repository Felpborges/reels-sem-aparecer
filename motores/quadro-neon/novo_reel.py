#!/usr/bin/env python3
"""MOTOR ESTILO C · cria um projeto de reel a partir de base/. Independente dos motores A e B.
uso: python3 novo_reel.py <pasta-destino> <fala.txt> "<título>" [nome-do-arquivo]
Copia base/, grava projeto.json, gera medir/texto.json + medir/frases.json (roteiro marcado por ato)."""
import sys, os, shutil, json, subprocess, re
AQ = os.path.dirname(os.path.abspath(__file__)); dst, fala, tit = sys.argv[1], sys.argv[2], sys.argv[3]
nome = sys.argv[4] if len(sys.argv) > 4 else re.sub(r"[^a-z0-9]+", "-", tit.lower().encode("ascii", "ignore").decode()).strip("-")
if os.path.exists(dst): sys.exit(f"{dst} já existe")
shutil.copytree(os.path.join(AQ, "base"), dst, ignore=shutil.ignore_patterns("index.html", "renders/*", "*.pyc"))
shutil.copy(fala, os.path.join(dst, "narracao", "fala.txt"))
json.dump({"titulo": tit, "nome": nome, "estilo": "C"}, open(os.path.join(dst, "projeto.json"), "w"), ensure_ascii=False, indent=1)
open(os.path.join(dst, ".rsa"), "w").write(os.path.abspath(os.path.join(AQ, "..", "..")))   # onde está a skill (o reel.sh lê)
os.makedirs(os.path.join(dst, "renders"), exist_ok=True)
subprocess.run([sys.executable, os.path.join(dst, "medir", "texto.py"), os.path.join(dst, "narracao", "fala.txt")], check=True)
print(f"projeto estilo C criado em {dst}.\nPróximos: imagens + ./reel.sh marca <site> <slug> + cenas.py; voz PROVISÓRIA -> ./reel.sh voz; trilha em assets/trilha.mp3; ./reel.sh montar.\n"
      "A voz definitiva é escolhida pela pessoa no FIM: ./reel.sh voz <escolhida> && ./reel.sh montar (todos os tempos se refazem).")
