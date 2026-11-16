#!/usr/bin/env python3
"""Lê o roteiro (narracao/fala.txt), marcado por ATO como no original (DESMONTE-D §1):
  [gancho] [contexto] [feito] [rejeicao] [salto] [moral] [cta]
Gera medir/texto.json ([[palavra mostrada, pronúncia], ...]), medir/atos.json e narracao/fala-para-voz.txt (o texto que
vai para o gerador de voz), e mostra palavras por ato x original.
Números: escreva por extenso na fala (o que a narradora diz).

PRONÚNCIA É DE CADA REEL, NUNCA DO MOTOR. O motor não guarda palavra nenhuma: cada tema tem as suas siglas e nomes.
Elas ficam em narracao/pronuncia.json do projeto, com duas listas (as chaves em minúsculas, sem pontuação):
  "alinhamento"  como a palavra SOA, em grafia fonética, só para o alinhador achar a palavra no áudio;
  "voz"          como ESCREVER a palavra para o gerador de voz ler certo (sigla que ele soletra ou lê errado).
O que não está nas listas vai como está no roteiro. O texto na TELA é sempre o do roteiro."""
import sys, json, re, os
AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_p = os.path.join(AQ, "narracao", "pronuncia.json")
_pr = json.load(open(_p)) if os.path.exists(_p) else {}
PRON = {k.lower(): v for k, v in _pr.get("alinhamento", {}).items()}
VOZ = {k.lower(): v for k, v in _pr.get("voz", {}).items()}
ORIG = {"gancho": 17, "contexto": 11, "feito": 13, "rejeicao": 5, "salto": 15, "moral": 15, "cta": 10}
fala = open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQ, "narracao", "fala.txt")).read()
ato, atos, pares, para_voz = "gancho", [], [], []
for tok in re.findall(r"\[[a-zçãé]+\]|\S+", fala):
    if tok.startswith("["):
        ato = tok.strip("[]"); continue
    limpo = re.sub(r"[^\wÀ-ÿ'-]", "", tok).lower()
    pares.append([tok, PRON.get(limpo, limpo)]); atos.append(ato)
    miolo = re.sub(r"^[^\wÀ-ÿ]+|[^\wÀ-ÿ]+$", "", tok)                       # a palavra sem a pontuação das pontas
    para_voz.append(tok.replace(miolo, VOZ[limpo]) if limpo in VOZ and miolo else tok)
json.dump(pares, open(os.path.join(AQ, "medir", "texto.json"), "w"), ensure_ascii=False, indent=0)
json.dump(atos, open(os.path.join(AQ, "medir", "atos.json"), "w"))
open(os.path.join(AQ, "narracao", "fala-para-voz.txt"), "w").write(" ".join(para_voz) + "\n")
trocas = sorted({f"{p} -> {v}" for (p, _), v in zip(pares, para_voz) if p != v})
if trocas:
    print("texto para a voz (narracao/fala-para-voz.txt): " + " · ".join(trocas))
print(f"{len(pares)} palavras (original: 85 em 32 s)")
for a in ORIG:
    n = atos.count(a)
    print(f"  {a:9} {n:3d} palavras (original {ORIG[a]})" + ("" if n else "  <- ato ausente"))
