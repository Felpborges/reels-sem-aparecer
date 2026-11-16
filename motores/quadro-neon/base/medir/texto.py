#!/usr/bin/env python3
"""ESTILO C · lê o roteiro marcado por ATO e gera medir/texto.json ([mostrada, pronúncia] por palavra falada) e
medir/frases.json (frase a frase, com o ato, para o ritmo da voz e para os moldes do cenas.py).
uso: texto.py fala.txt
Formato do roteiro (uma linha por frase; o ato vale até o próximo marcador):
  [gancho] Ninguém compra IA.
  [ponte] Deixa eu te explicar.
  [tese] ...   [reframe] ...   [prova] (uma linha por exemplo)   [sintese] ...   [lista] ...   [cta] ...
Acrescente pronúncias novas em PRON (marcas e siglas viram como se falam)."""
import json, re, sys, os
PRON = {"ia": "i a", "ias": "i as", "claude": "clód", "code": "côud", "chatgpt": "tchat gê pê tê", "gpt": "gê pê tê", "ifood": "ai fud",
        "nubank": "nubanc", "uber": "uber", "netflix": "nétflics", "airbnb": "érbi en bi", "app": "ép", "apps": "éps", "online": "onlaine",
        "site": "saite", "sites": "saites", "design": "dizaine", "canva": "canva", "notion": "nôuchon", "google": "gugol", "instagram": "instagram",
        "whatsapp": "uatsap", "spotify": "spotifai", "apple": "épol", "iphone": "aifone", "amazon": "amazon", "shopee": "xopi", "delivery": "delíveri", "streaming": "estríming", "streamings": "estrímings", "pro": "pró", "max": "macs"}
U = "zero um dois três quatro cinco seis sete oito nove dez onze doze treze catorze quinze dezesseis dezessete dezoito dezenove".split()
D = "_ _ vinte trinta quarenta cinquenta sessenta setenta oitenta noventa".split()
def num(n):
    if n < 20: return U[n]
    if n < 100: return D[n // 10] + ("" if n % 10 == 0 else " e " + U[n % 10])
    return str(n)
def pron(w):
    b = re.sub(r"[^\wÀ-ÿ%]", "", w).lower()
    if re.fullmatch(r"\d+", b): return num(int(b))
    if re.fullmatch(r"\d+%", b): return num(int(b[:-1])) + " por cento"
    return PRON.get(b, b)
ATOS = ("gancho", "ponte", "tese", "reframe", "prova", "sintese", "lista", "cta")
out, frases, ato = [], [], None
for linha in open(sys.argv[1]).read().splitlines():
    linha = linha.strip()
    if not linha: continue
    m = re.match(r"\[(\w+)\]\s*(.*)", linha)
    if m:
        ato = m.group(1).lower(); linha = m.group(2)
        assert ato in ATOS, f"ato desconhecido: {ato}"
    if not linha: continue
    toks = [w for w in linha.split() if re.search(r"[\wÀ-ÿ]", w)]
    ini = len(out); cur = ini
    for j, w in enumerate(toks):
        out.append([w, pron(w)])
        if w[-1] in ".?!" or j == len(toks) - 1:                       # frase = até o ponto (uma linha pode ter 2)
            frases.append({"ini": cur, "fim": len(out) - 1, "ato": ato, "pont": w[-1] if w[-1] in ".?!," else ".",
                           "virgulas": [k for k in range(cur, len(out) - 1) if out[k][0][-1] == ","]}); cur = len(out)
AQ = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(AQ, "texto.json"), "w"), ensure_ascii=False)
json.dump(frases, open(os.path.join(AQ, "frases.json"), "w"), ensure_ascii=False, indent=0)
n = {a: sum(f["fim"] - f["ini"] + 1 for f in frases if f["ato"] == a) for a in ATOS}
print(len(frases), "frases ·", len(out), "palavras ·", f"~{len(out) / 160 * 60 + 1:.0f} s no ritmo do original (167/min, PT ~160)")
print("palavras por ato:", n, "(original: gancho 4 · ponte 4 · tese 11 · reframe 13 · prova 5x7-9 · sintese 6 · lista 17 · cta 21)")
print("pronúncias trocadas:", sorted({(a, b) for a, b in out if re.sub(r'[^\wÀ-ÿ]', '', a).lower() != b}))
