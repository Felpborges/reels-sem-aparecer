#!/usr/bin/env python3
"""Gera medir/texto.json ([palavra mostrada, pronúncia] por palavra falada) a partir da FALA do roteiro.
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
fala = open(sys.argv[1]).read()
pal = [w for w in fala.split() if re.search(r"[\wÀ-ÿ]", w)]
out = [[w, pron(w)] for w in pal]
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "texto.json"), "w"), ensure_ascii=False)
print(len(out), "palavras ·", f"~{len(out) / 212 * 60:.0f} s no ritmo do original (212/min)")
print("pronúncias trocadas:", sorted({(a, b) for a, b in out if re.sub(r'[^\wÀ-ÿ]', '', a).lower() != b}))
