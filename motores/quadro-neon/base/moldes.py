# MOTOR ESTILO C · MOLDES de alto nível. Cada ato do roteiro (marcado em fala.txt) vira um bloco montado com as regras
# MEDIDAS no original (pericia/DESMONTE-C.md + recriação validada). O cenas.py de um reel novo só passa a configuração
# (imagens, ícone, marcas, tarja) para reel_c(CFG). Tudo é amarrado à palavra falada (P/F): trocar a voz no fim
# (./reel.sh voz nova.mp3) refaz todos os tempos sozinho.
#
# Regras de tempo (medidas):
#   legenda de 1 palavra NA palavra (±1 quadro) · herói do reframe entra com o começo da frase, o 2º herói na palavra dele
#   título do gancho +0,12 s depois da palavra · digitação da prova acompanha a fala palavra a palavra (+0,12 s)
#   linha do payoff entra no começo da 2ª metade ("vende...") · item da lista entra na palavra e SOME na pausa
#   corte entre marcas na pausa, ~0,06 s antes do nome · flash de luz só entre ATOS (4 por reel) · nada de duas palavras encostadas
import json, os, re
from PIL import ImageFont

_M = os.path.join(AQUI, "medir")
FR = json.load(open(os.path.join(_M, "frases.json")))
_TTF = {"anton": "anton-latin-400-normal.ttf", "m400": "montserrat-latin-400-normal.ttf", "m500": "montserrat-latin-500-normal.ttf",
        "m600": "montserrat-latin-600-normal.ttf", "gochi": "gochi-hand-latin-400-normal.ttf"}


def larg(txt, fonte, size, sx=1.0):
    """largura real do texto em px do palco (fonte de verdade em medir/*.ttf)"""
    f = ImageFont.truetype(os.path.join(_M, _TTF[fonte]), int(size))
    return max(f.getlength(l) for l in txt.split("\n")) * sx


def cabe(txt, fonte, size, wmax, sx=1.0, minimo=10):
    """maior tamanho <= size em que o texto cabe em wmax (regra do quadro seguro: nunca cortar, reduzir o corpo)"""
    s = size
    while s > minimo and larg(txt, fonte, s, sx) > wmax: s -= 1
    return s


def limpa(w):
    return re.sub(r"[.,;:!?…]+$", "", w)


def atos(nome):
    return [f for f in FR if f["ato"] == nome]


def pal(i):
    return limpa(ONS_TXT[i])


ONS_TXT = [w[0] for w in json.load(open(os.path.join(_M, "texto.json")))]


def acha(fz, palavra):
    """índice da palavra (sem pontuação, sem caixa) dentro da frase fz"""
    for i in range(fz["ini"], fz["fim"] + 1):
        if limpa(ONS_TXT[i]).lower() == palavra.lower(): return i
    raise ValueError(f"'{palavra}' não está na frase: {' '.join(ONS_TXT[fz['ini']:fz['fim'] + 1])}")


def corte_antes(i):
    """corte na pausa antes da palavra i (medido: ~0,06 s antes da voz; nunca antes do fim da palavra anterior)"""
    t = P(i) - 0.06
    return round(max(t, F(i - 1) + 0.02) if i > 0 else 0.0, 3)


# ------------------------------------------------------------------------------------------------- atos
def gancho(fz, img_src=None, img_pos=None, objeto=None, linhas=None):
    """Colagem + título neon gigante empilhado à esquerda, palavra a palavra (medido 0,33/0,47/0,86/1,02 s).
    Imagem: padrão medido = 760 px de altura, topo em 152, borda direita em 556 (ou img_pos=(x, y, largura)).
    Objeto: (src, largura) ou (src, x, y, largura); padrão encosta no fim do título, à esquerda (como a carteira)."""
    secao(0.0, nome="gancho")
    if img_src:
        if img_pos is None:
            from PIL import Image as _I
            iw, ih = _I.open(os.path.join(AQUI, img_src)).size; w = round(760 * iw / ih); img_pos = (max(150, 556 - w), 152, w)
        x, y, w = img_pos
        SOM("sopro", 0.16, -3)
        gid = img(img_src, x, y, w, t=0.06, ent="direita", de=320, d=0.32, sombra=False,     # some no preto embaixo (como no original)
            extra="-webkit-mask-image:linear-gradient(180deg,#000 62%,transparent 98%);mask-image:linear-gradient(180deg,#000 62%,transparent 98%);")
        anim(gid, 0.40, {"x": 0, "y": 0}, {"x": 3.4, "y": -3.4}, 1.6, "none")              # deriva lenta medida (~2 px/s)
    linhas = linhas or [(pal(i).upper(), i) for i in range(fz["ini"], fz["fim"] + 1)]
    n = len(linhas); size = min([177] + [cabe(l, "anton", 177, 480, ESTREITA["gancho"]) for l, _ in linhas])
    passo = size * 0.97; y0 = 118 + (4 - n) * passo / 2 if n < 4 else 118
    for k, (txt, i) in enumerate(linhas):
        display(txt, 44, round(y0 + k * passo), size=size, cor="amarelo", t=P(i) + 0.12, ent="esquerda", papel="gancho", alinh="left",
                lh=0.97, d=0.16, de=380)
        SOM("sopro", P(i) + 0.20, -4)
    # objetos: (src, largura) | (src, largura, "palavra") | {"src", "w", "palavra", "pos": (x, y)}
    # o 1º sobe por baixo do título (como a carteira do original); os outros pipocam ao lado da linha da palavra deles
    objs = objeto if isinstance(objeto, list) else ([objeto] if objeto else [])
    from PIL import Image as _I
    for k, o in enumerate(objs):
        if isinstance(o, tuple):
            o = {"src": o[0], "w": o[1], "palavra": o[2] if len(o) > 2 else None} if len(o) <= 3 else {"src": o[0], "pos": (o[1], o[2]), "w": o[3]}
        iw, ih = _I.open(os.path.join(AQUI, o["src"])).size; w = o["w"]; h = w * ih / iw
        li = next((j for j, (_, i) in enumerate(linhas) if o.get("palavra") and pal(i).lower() == o["palavra"].lower()), len(linhas) - 1)
        tt = P(linhas[li][1]) + (0.05 if k else -0.1)
        if o.get("pos"): x, y = o["pos"]
        elif k == 0: x, y = 70, round(y0 + n * passo - 0.25 * h)
        else:
            lx = 44 + larg(linhas[li][0], "anton", size, ESTREITA["gancho"])          # à direita da linha, sem encostar no 1º objeto
            x, y = round(min(max(lx + 30, 300), 556 - w)), round(y0 + li * passo + passo * 0.5 - h / 2)
        img(o["src"], x, y, w, t=tt, ent="baixo" if k == 0 else "pop", de=280 if k == 0 else None, d=0.26 if k == 0 else 0.22, rot=-4 if k == 0 else 6)
        SOM("brilho", tt + 0.15, -2)


def ponte(fz, foto=None):
    """Flash de luz; a frase em 2 linhas, letras chegam espaçadas e fecham (0,32 s).
    foto = (src, largura): foto recortada que pipoca embaixo da frase logo depois do flash (rodada 3: punch no começo)."""
    t = round(P(fz["ini"]) + 0.28, 3)
    secao(t, entrada="flash", nome="ponte", anda=30); SOM("whoosh", t)
    ws = [pal(i).upper() for i in range(fz["ini"], fz["fim"] + 1)]
    corte = max(1, round(len(ws) / 2 + 0.1)); l1, l2 = " ".join(ws[:corte]), " ".join(ws[corte:])
    size = min(116, cabe(l1, "anton", 116, 470, ESTREITA["ponte"]), cabe(l2 or "X", "anton", 116, 470, ESTREITA["ponte"]))
    display(l1, 288, 388 + (116 - size) * 0.6, size=size, cor="amarelo", t=t + 0.0, ent="tracking", papel="ponte", d=0.32)
    if l2: display(l2, 288, 388 + (116 - size) * 0.6 + size * 0.97, size=size, cor="amarelo", t=t + 0.05, ent="tracking", papel="ponte", d=0.32)
    if foto:
        from PIL import Image as _I
        src, w = foto; iw, ih = _I.open(os.path.join(AQUI, src)).size; h = w * ih / iw
        ytxt = 388 + (116 - size) * 0.6 + size * 0.97 * (2 if l2 else 1)
        img(src, 288 - w / 2, round(min(ytxt + 24, 900 - h)), w, t=t + 0.14, ent="pop", d=0.22); SOM("brilho", t + 0.18, -2)


ESCUDO_MAO = (["shield-check", "hand-helping"], [(0.10, -0.20, 0.52), (0, 0.16, 0.95)])
SETA = [(340, 410), (344, 372), (352, 346), (362, 330), (372, 312), (392, 296), (384, 280), (376, 262), (350, 272), (352, 296),
        (354, 322), (402, 330), (430, 298), (446, 280), (456, 252), (461, 222)]        # seta à mão com laço, medida (fim em 461,222)


def tese(fz, icone_nomes=ESCUDO_MAO, palavra_mao=None):
    """Ícone neon + legenda de 1 palavra; a última palavra (ou palavra_mao) vira '<palavra>' manuscrita, com a seta à mão."""
    t = corte_antes(fz["ini"]); secao(t, nome="tese", anda=30)
    nomes, partes = icone_nomes if isinstance(icone_nomes, tuple) else (icone_nomes, None)
    ic = icone(nomes, 288, 508, 165, t=t, ent="pop_leve", partes=partes); SOM("brilho", t + 0.2)
    im = acha(fz, palavra_mao) if palavra_mao else fz["fim"]
    legenda([(pal(i), P(i)) for i in range(fz["ini"], im)], 735, fim=P(im))
    ms = pal(im); size = cabe(f"<{ms}>", "gochi", 50, 300)
    cx = min(546 - larg(f"<{ms}>", "gochi", size) / 2, 445)
    anim(ic, P(im) - 0.52, {"scale": 1}, {"scale": 1.4}, 0.35)
    kx = (cx + 16 - 340) / (461 - 340)
    pts = [(round(340 + (x - 340) * kx, 1), y) for x, y in SETA]
    d = f"M{pts[0][0]} {pts[0][1]} " + " ".join(f"C{pts[j][0]} {pts[j][1]} {pts[j + 1][0]} {pts[j + 1][1]} {pts[j + 2][0]} {pts[j + 2][1]}" for j in range(1, len(pts) - 2, 3))
    seta(d, P(im) - 0.49, 0.55); SOM("risco", P(im) - 0.49)
    manuscrito(ms, cx, 128 + (50 - size) * 0.5, P(im), size=size); SOM("brilho", P(im) + 0.03, -3)
    for i in range(im + 1, fz["fim"] + 1):           # palavras depois da manuscrita (se houver) voltam como legenda
        legenda([(pal(i), P(i))], 735, fim=F(i) + 0.1)


def reframe(fz, heroi_a, heroi_b, img_src, img_palavra=None, img_w=330):
    """HERÓI A (amarelo, entra com a frase) -> foto recortada (pop) -> HERÓI B (branco com brilho, na palavra) + arco
    tracejado (causa -> efeito). Legenda de 1 palavra até o herói B; depois a tela fica parada (medido 1,9 s)."""
    t = corte_antes(fz["ini"]) - 0.04; secao(t, nome="reframe", anda=30)
    ia, ib = acha(fz, heroi_a), acha(fz, heroi_b)
    sa = cabe(heroi_a.upper(), "anton", 97, 420, ESTREITA["heroi"]); sb = cabe(heroi_b.upper(), "anton", 97, 420, ESTREITA["heroi"])
    display(heroi_a.upper(), 288, 205 + (97 - sa) * 0.5, size=sa, cor="amarelo", t=P(fz["ini"]), ent="cresce", d=0.40); SOM("sopro", P(fz["ini"]) + 0.1)
    legenda([(pal(i), P(i)) for i in range(fz["ini"], ib)], 735, fim=P(ib) - 0.1)
    ii = acha(fz, img_palavra) if img_palavra else min(ib - 1, ia + 2)
    img(img_src, 288 - img_w / 2, 318, img_w, t=P(ii), ent="pop", d=0.22); SOM("brilho", P(ii) + 0.03)
    display(heroi_b.upper(), 288, 680 + (97 - sb) * 0.5, size=sb, cor="branco_amarelo", t=P(ib) - 0.08, ent="sobe_forte", d=0.30); SOM("whoosh", P(ib) - 0.05, -4)
    xa = 288 + larg(heroi_a.upper(), "anton", sa, ESTREITA["heroi"]) / 2 + 12; xb = 288 + larg(heroi_b.upper(), "anton", sb, ESTREITA["heroi"]) / 2 + 4
    arco((min(xa, 530), 262), (min(xb, 530), 700), 0.32, t=P(ib) + 0.13, dur=0.60); SOM("risco", P(ib) + 0.13, 2)
    t_drop = P(atos("prova")[0]["ini"]) if atos("prova") else P(ib) + 2.8
    MUSICA("baixo_sai", max(t + 0.5, min(P(ib) - 0.1, t_drop - 2.6)))     # medido: o grave some ~2,8 s antes do drop


def prova(frases, marcas):
    """O molde do cartão de marca, um por frase. marcas = [{"nome", "logo", "print", ["logo_pad"], ["logo_fundo"]}].
    Frase: '<Marca> não vende X, vende Y.' -> linha 1 = até a vírgula (digitada com a fala), linha 2 = '<1ª palavra> <PAYOFF>'."""
    for k, (fz, m) in enumerate(zip(frases, marcas)):
        v = (fz["virgulas"] or [fz["fim"] - 2])[0]
        t = round(P(fz["ini"]) - 0.02, 3) if k == 0 else corte_antes(fz["ini"])
        fim = (corte_antes(frases[k + 1]["ini"]) if k + 1 < len(frases) else None)
        secao(t, entrada="flash" if k == 0 else "corte", nome=f"prova{k + 1}")
        if k == 0: SOM("impacto", t); SOM("whoosh", t, -2); MUSICA("drop", t)
        else: SOM("whoosh", t)                                               # medido: whoosh em TODA troca de cartão
        l1 = " ".join(pal(i).upper() for i in range(fz["ini"], v + 1))
        ritmo = [(P(i) + 0.12, F(i) + 0.12) for i in range(fz["ini"], v + 1)]
        pre_ = pal(v + 1).upper(); pay = " ".join(pal(i).upper() for i in range(v + 2, fz["fim"] + 1))
        # linha 1 cabe em no máximo 2 linhas (acima da linha 2): alarga a caixa e, se precisar, reduz o corpo
        def n_linhas(txt, size, w):
            k, cur = 1, ""
            for p_ in txt.split():
                tent = (cur + " " + p_).strip()
                if larg(tent, "m500", size) > w and cur: k += 1; cur = p_
                else: cur = tent
            return k
        s1, w1 = 36, 430
        if n_linhas(l1, s1, w1) > 2: w1 = 500
        while n_linhas(l1, s1, w1) > 2 and s1 > 26: s1 -= 1
        ids = cartao(t, m["logo"], m["nome"], m["print"], l1, ritmo[0][0], pre_, pay, P(v + 1), fim=fim,
                     size_l1=s1, w_linha=w1, nome_size=cabe(m["nome"].upper(), "anton", 56, 300, ESTREITA["marca"]),
                     logo_desfoque=m.get("logo_desfoque", 0), print_desfoque=m.get("print_desfoque", 0),
                     logo_pad=m.get("logo_pad", 14), logo_fundo=m.get("logo_fundo", "#fff"), ritmo=ritmo,
                     size_l2=cabe(f"{pre_} {pay}", "m500", 36, 430))           # quadro seguro: fora da coluna do Instagram
        if fim: _sai(ids["l2"], (fim - 1 / 30, "seco"))


def sintese(fz, tarja_txt):
    """Flash; malha larga sem estrelas; a TARJA amarela (título-síntese) sobe e acende."""
    t = round(P(fz["ini"]) - 0.02, 3)
    secao(t, entrada="flash", fundo="grade_larga", nome="sintese", anda=30); SOM("whoosh", t); MUSICA("break", t)
    s = cabe(tarja_txt.upper(), "anton", 70, 470, ESTREITA["tarja"])
    w = min(520, larg(tarja_txt.upper(), "anton", s, ESTREITA["tarja"]) + 44)
    tarja(tarja_txt.upper(), 288, 173, w, 89, t=t + 0.1, size=s); SOM("sopro", t + 0.2)


def lista(fz, n_prompt=3, imgs=None, img_w=300):
    """'>prompt' (o '>' amarelo) na fala dele; embaixo UM item por vez: entra na palavra, some na pausa (medido).
    imgs = [foto recortada por item] (opcional, pedido do Felipe na rodada 2: dá dinâmica): a foto entra com o item
    (pop + brilho, como os relógios do original) embaixo do texto e sai com ele."""
    pr = " ".join(pal(i) for i in range(fz["ini"], fz["ini"] + n_prompt))
    prompt(pr, 288, 412, P(fz["ini"]), size=cabe(">" + pr, "m400", 60, 500)); SOM("sopro", P(fz["ini"]) + 0.1, -3)
    segs, a = [], fz["ini"] + n_prompt
    for v in fz["virgulas"] + [fz["fim"]]:
        if v >= a: segs.append((a, v)); a = v + 1
    MUSICA("volta", P(segs[0][0]))
    for k, (a, b) in enumerate(segs):
        tx = " ".join(pal(i) for i in range(a, b + 1))
        if imgs and k < len(imgs) and imgs[k]:
            img(imgs[k], 288 - img_w / 2, 600, img_w, t=P(a) + 0.02, ent="pop", d=0.22, sai=(F(b) + 0.03, "seco"))
            SOM("brilho", P(a) + 0.05, -2)
        corpo(tx, 288, 522, size=cabe(tx, "m500", 46, 480), peso=500, cor="amarelo_suave", t=P(a), ent="sobe", sai=(F(b) + 0.03, "seco"))
        SOM("sopro", P(a) + 0.06, -6)


def cta(frases, gatilhos=("comenta", "comente", "digita", "digite", "escreve", "escreva")):
    """Flash; fundo vazio; UMA palavra por vez em caixa alta no centro; a palavra-código (depois de 'comenta') entre aspas."""
    t = corte_antes(frases[0]["ini"]) - 0.04
    secao(t, entrada="flash", nome="cta"); SOM("whoosh", t)
    idx = [i for fz in frases for i in range(fz["ini"], fz["fim"] + 1)]
    for k, i in enumerate(idx):
        w = pal(i).upper()
        if k and pal(idx[k - 1]).lower() in gatilhos: w = f"“{w}”"
        nxt = P(idx[k + 1]) if k + 1 < len(idx) else F(i) + 0.4
        fim = nxt if nxt - F(i) < 0.15 else F(i) + 0.05            # pausa real -> tela vazia (medido 37,50-37,67)
        legenda([(w, P(i))], 494, size=cabe(w, "m600", 36, 480), fim=fim)


def reel_c(CFG):
    """Monta o reel inteiro a partir de fala.txt (atos) + CFG. Ver o modelo em cenas.py."""
    g = atos("gancho")[0]; gancho(g, CFG.get("gancho_img"), CFG.get("gancho_img_pos", (200, 152, 356)), CFG.get("gancho_objeto"))
    ponte(atos("ponte")[0], CFG.get("ponte_foto"))
    tese(atos("tese")[0], CFG.get("tese_icone", ESCUDO_MAO), CFG.get("tese_palavra"))
    reframe(atos("reframe")[0], CFG["reframe_a"], CFG["reframe_b"], CFG["reframe_img"], CFG.get("reframe_img_palavra"))
    prova(atos("prova"), CFG["marcas"])
    sintese(atos("sintese")[0], CFG["tarja"])
    lista(atos("lista")[0], CFG.get("lista_prompt", 3), CFG.get("lista_imgs"))
    cta(atos("cta"))
