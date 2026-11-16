#!/usr/bin/env python3
"""ESTILO B · Gera medir/texto.json ([palavra mostrada, pronúncia] por palavra falada) a partir da FALA do roteiro.
uso: texto.py fala.txt      (só o texto que será narrado; parágrafos à vontade)
A pronúncia serve ao alinhamento forçado em PT-BR: nomes em inglês e números viram como se falam.
Acrescente termos novos em PRON quando o roteiro trouxer outras marcas/palavras estrangeiras."""
import json, re, sys, os
PRON = {"claude": "clód", "code": "côud", "pro": "pró", "max": "macs", "higgsfield": "higsfild", "chatgpt": "tchat gê pê tê",
        "gpt": "gê pê tê", "openai": "open ei ai", "ai": "ei ai", "app": "ép", "apps": "éps", "prompt": "prompt", "online": "onlaine",
        "site": "saite", "sites": "saites", "design": "dizaine", "fable": "fêibol", "opus": "ópus", "sonnet": "sonet", "haiku": "raicu"}
U = "zero um dois três quatro cinco seis sete oito nove dez onze doze treze catorze quinze dezesseis dezessete dezoito dezenove".split()
D = "_ _ vinte trinta quarenta cinquenta sessenta setenta oitenta noventa".split()
C = "_ cento duzentos trezentos quatrocentos quinhentos seiscentos setecentos oitocentos novecentos".split()
def num(n):
    if n < 20: return U[n]
    if n < 100: return D[n // 10] + ("" if n % 10 == 0 else " e " + U[n % 10])
    if n == 100: return "cem"
    if n < 1000: return C[n // 100] + ("" if n % 100 == 0 else " e " + num(n % 100))
    if n < 1000000:
        m, r = divmod(n, 1000); p = "mil" if m == 1 else num(m) + " mil"
        return p + ("" if r == 0 else (" e " if r < 100 or r % 100 == 0 else " ") + num(r))
    return str(n)
def pron(w):
    b = re.sub(r"[^\wÀ-ÿ%$]", "", w).lower()
    if re.fullmatch(r"\d+", b): return num(int(b))
    if re.fullmatch(r"\d+%", b): return num(int(b[:-1])) + " por cento"
    return PRON.get(b, b)
# ESTILO B: o roteiro marca a FRASE-CHAVE (tese, fecho) com » no começo; ela é falada mais devagar (~160/min, medido).
# Linha em branco = fim de parágrafo (pausa maior). Grava também medir/frases.json para o ritmo_voz.py.
fala = open(sys.argv[1]).read()
out, frases, cur, chave = [], [], None, False
for par in re.split(r"\n\s*\n", fala.strip()):
    toks = par.split()
    for j, w in enumerate(toks):
        if w.startswith("»"): chave = True; w = w[1:]
        if not re.search(r"[\wÀ-ÿ]", w): continue
        if cur is None: cur = {"ini": len(out), "chave": chave}
        out.append([w, pron(w)])
        fimpar = j == len(toks) - 1
        if w[-1] in ".,;:!?…" or fimpar:
            cur.update({"fim": len(out) - 1, "pont": w[-1] if w[-1] in ".,;:!?…" else ".", "paragrafo": fimpar}); frases.append(cur); cur = None; chave = False
AQ = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(AQ, "texto.json"), "w"), ensure_ascii=False)
json.dump(frases, open(os.path.join(AQ, "frases.json"), "w"), ensure_ascii=False, indent=0)
print(len(frases), "frases ·", sum(f["chave"] for f in frases), "frase(s)-chave marcadas com »")
print(len(out), "palavras ·", f"~{len(out) / 183 * 60 + 0.6:.0f} s no ritmo do original do estilo B (183/min)")
print("pronúncias trocadas:", sorted({(a, b) for a, b in out if re.sub(r'[^\wÀ-ÿ]', '', a).lower() != b}))
