#!/usr/bin/env python3
"""Cadência de edição: quanto tempo cada cena e cada elemento ficam na tela.
uso: cadencia.py elementos.json [rótulo]   (elementos.json gerado pelo build.py: cenas + elementos com tempo de entrada)
Mede por cena: duração, tempo até o 1º visual, respiro final (do último elemento novo até o corte),
tempo de tela da imagem principal e a imagem (foto/objeto) que fica menos tempo visível."""
import json, sys, statistics as st
E = json.load(open(sys.argv[1])); rot = sys.argv[2] if len(sys.argv) > 2 else ""
C = {c["n"]: c for c in E["cenas"]}; por = {}
for e in E["elementos"]:
    por.setdefault(e["n"], []).append(e)
linhas = []
for n, c in sorted(C.items()):
    els = por.get(n, []); ini, fim = max(c["start"], 0), c["end"]; dur = fim - ini
    ts = sorted(max(e["t"], ini) for e in els)
    imgs = [e for e in els if e["k"] in "ir"]
    vis_img = [((e["out"] or fim) - max(e["t"], ini)) for e in imgs]
    novos = [t for t in ts if t > ini + 0.02]
    respiro = fim - (max(novos) if novos else ini)
    linhas.append(dict(n=n, ini=round(ini, 2), dur=round(dur, 2), n_el=len(els), respiro=round(respiro, 2),
                       img_max=round(max(vis_img), 2) if vis_img else None, img_min=round(min(vis_img), 2) if vis_img else None,
                       ate_img=round(min(max(e["t"], ini) for e in imgs) - ini, 2) if imgs else None))
if __name__ == "__main__":
    print(f"== {rot}: {len(linhas)} cenas")
    print(" n   início  dur   elem  respiro  img(maior)  img(menor)")
    for l in linhas:
        print(f"{l['n']:2d}  {l['ini']:6.2f}  {l['dur']:4.2f}  {l['n_el']:4d}   {l['respiro']:5.2f}    {str(l['img_max']):>6}     {str(l['img_min']):>6}")
    d = [l["dur"] for l in linhas]; r = [l["respiro"] for l in linhas]; im = [l["img_max"] for l in linhas if l["img_max"]]
    print(f"dur: mín {min(d):.2f} · p10 {sorted(d)[len(d)//10]:.2f} · mediana {st.median(d):.2f} | respiro: mín {min(r):.2f} · p10 {sorted(r)[len(r)//10]:.2f} · mediana {st.median(r):.2f} | imagem principal na tela: mín {min(im):.2f} · mediana {st.median(im):.2f}")

# ---------- regras de cadência, medidas no reel de referência (recriação fiel, 39 cenas) ----------
# duração da cena ≥ 1,2 s (o original só fica abaixo numa foto-soco de 3 elementos) · respiro final ≥ 0,30 s (p10 do
# original: 0,35) · imagem principal ≥ 0,9 s na tela · ≤ 6 elementos novos por segundo (máx. do original: 6,1) ·
# ≥ 70 % das cenas com imagem já abrem com ela no quadro do corte (original: 23 de 31); imagem atrasada só em cena ≥ 1,8 s.
REGRAS = {"dur": 1.2, "respiro": 0.30, "img": 0.9, "dens": 6.0, "abre_com_img": 0.70, "atraso_cena_min": 1.8}
def checa(linhas):
    ruins = []
    for l in linhas:
        if l["dur"] < REGRAS["dur"] and l["n_el"] > 3: ruins.append((l["n"], f"cena curta: {l['dur']} s com {l['n_el']} elementos"))
        if l["respiro"] < REGRAS["respiro"]: ruins.append((l["n"], f"respiro {l['respiro']} s antes do corte"))
        if l["img_max"] is not None and l["img_max"] < REGRAS["img"]: ruins.append((l["n"], f"imagem principal só {l['img_max']} s na tela"))
        if l["n_el"] / l["dur"] > REGRAS["dens"]: ruins.append((l["n"], f"{l['n_el'] / l['dur']:.1f} elementos/s"))
        if l["ate_img"] and l["ate_img"] > 0.05 and l["dur"] < REGRAS["atraso_cena_min"]: ruins.append((l["n"], f"imagem entra {l['ate_img']} s depois do corte numa cena de {l['dur']} s"))
    com = [l for l in linhas if l["ate_img"] is not None]; abre = sum(1 for l in com if l["ate_img"] <= 0.05) / max(1, len(com))
    if abre < REGRAS["abre_com_img"]: ruins.append((0, f"só {abre:.0%} das cenas com imagem abrem com ela na tela (meta ≥ 70 %)"))
    return ruins, abre
if __name__ == "__main__":
    ruins, abre = checa(linhas)
    print(f"cenas que abrem com a imagem: {abre:.0%}")
    print("REGRAS DE CADÊNCIA:", "APROVADO" if not ruins else f"{len(ruins)} problema(s)")
    for n, m in ruins: print(f"  cena {n}: {m}")
    sys.exit(1 if ruins else 0)
