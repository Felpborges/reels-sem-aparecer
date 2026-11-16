#!/usr/bin/env python3
"""MOTOR ESTILO B ("o texto mora dentro do mundo") · gera index.html (HyperFrames + GSAP) a partir de cenas.py.

Independente do motor A. Manual: MOTOR.md do motor dentro-do-mundo, na skill.
Palco 720x1280 (escalado 1,5x para 1080x1920). Tempos em segundos absolutos; P(i) = início da i-ésima palavra falada
(medir/alinhamento.json). Um MUNDO = um cenário (foto ou tela de app) com câmera própria; troca por corte seco
salvo quando a tabela pede outra transição.

Primitivas (usadas em cenas.py e em mundos.py):
  mundo(t, fmt="cheio"|"faixa", fundo, entrada=("corte"|"zoom"|"preto"|"dissolve"|"flash", dur), cam=[(t,s,x,y,r[,ease])])
  foto(src, ...)                      imagem de fundo (cobre o palco)
  img(src, x, y, w, ...)              imagem posicionada (recorte, objeto, primeiro plano desfocado)
  texto(html, x, y, ...)              texto solto; ent = "seco" | "blur" | "fade" | "assenta" | "voa" | "pop"
  assenta(palavras, x, y, ...)        linha que se monta palavra a palavra e se recentra (papel cinético)
  digita(txt, t0, x, y, ...)          texto digitado com cursor
  risco(pontos, t, d, ...)            traço que se desenha (sublinhado, linha que liga pílulas)
  bloco(html, x, y, w, h, ...)        bloco HTML livre (telas de app); filhos animados com anim()
  anim(id, t, de, para, d, ease)      animação genérica de qualquer elemento
  conta(id, t, de, ate, d, fmt)       contador numérico
  quad=[(x,y)x4]                      qualquer elemento pode ser posto numa superfície em perspectiva (TL,TR,BR,BL)
  SOM(tipo, t, ganho_db=0)            efeito sonoro (lido pelo mix.py)
"""
import json, html, os, math, random

AQUI = os.path.dirname(os.path.abspath(__file__))
PROJ = json.load(open(os.path.join(AQUI, "projeto.json")))
ONS = json.load(open(os.path.join(AQUI, "medir", "alinhamento.json")))
DUR = PROJ.get("duracao") or round(ONS[-1]["end"] + 0.35, 2)
FPS = 30
AUDIO = PROJ.get("audio") or ("assets/mix.m4a" if os.path.exists(os.path.join(AQUI, "assets", "mix.m4a")) else "assets/narracao.wav")
FAIXA = (285, 995)                      # faixa quadrada das telas de app (medida: barras de ~285 px)
ADIANTA = 0.04                          # o texto chega um quadro antes do som da palavra
LEVA = 0.22                             # duração padrão do "assentar" (medido: 6-8 quadros)

MUNDOS, ANIMS, SONS, CAMS = [], [], [], []
_n = [0]


def P(i, antes=0.0):
    """Início da i-ésima palavra falada menos ADIANTA (e menos `antes`)."""
    return round(max(0.0, ONS[i]["start"] - ADIANTA - antes), 3)


def F(i):
    """Fim da i-ésima palavra falada."""
    return round(ONS[i]["end"], 3)


def _id(p="e"):
    _n[0] += 1
    return f"{p}{_n[0]}"


TRILHA_PTS = []


def TRILHA(t, db, d=0.4):
    """Automação da trilha: em t, vai para `db` (relativo ao nível padrão, 11,5 dB abaixo da voz) em d segundos.
    Medido no original: a trilha ESVAZIA (~-12 dB) na virada antes do CTA e volta no CTA."""
    TRILHA_PTS.append({"t": round(float(t), 3), "db": db, "d": d})


def foco(t, s, cx, cy, r=0, ease=None):
    """Keyframe de câmera pelo ponto que deve ficar no centro da tela: (t, escala, x, y, rot[, ease])."""
    a = math.radians(r); px, py = cx - 360, cy - 640
    rx, ry = px * math.cos(a) - py * math.sin(a), px * math.sin(a) + py * math.cos(a)
    k = (t, s, round(-s * rx, 1), round(-s * ry, 1), r)
    return k + ((ease,) if ease else ())


def fc(t, s, cx, cy, r=0, ease=None):
    """foco() com QUADRO SEGURO para mundos de foto: a foto 720x1280 sempre cobre o quadro.
    Com rotação r a escala mínima é cos r + 1,78 sen r; o centro é limitado ao que essa escala permite."""
    a = math.radians(abs(r)); k = math.cos(a) + 1.78 * math.sin(a)
    s = max(s, k * 1.02); se = s / k
    dx, dy = 360 * (1 - 1 / se) * 0.96, 640 * (1 - 1 / se) * 0.96
    cx = min(max(cx, 360 - dx), 360 + dx); cy = min(max(cy, 640 - dy), 640 + dy)
    return foco(t, s, round(cx, 1), round(cy, 1), r, ease)


FOLGA = "padding:0 24px 16px 0;"   # extra= de texto à mão/giz (Caveat, Kalam): a letra inclinada passa da caixa e o escreve() a decepava


def SOM(tipo, t, ganho_db=0.0):
    SONS.append({"tipo": tipo, "t": round(float(t), 3), "db": ganho_db})


# ---------------------------------------------------------------- perspectiva
def _homog(w, h, q):
    """matrix3d que leva a caixa w x h (origem 0 0) para o quadrilátero q = [TL, TR, BR, BL]."""
    src = [(0, 0), (w, 0), (w, h), (0, h)]
    A, B = [], []
    for (x, y), (u, v) in zip(src, q):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    n = 8
    M = [row[:] + [b] for row, b in zip(A, B)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    h_ = [M[i][n] / M[i][i] for i in range(n)]
    a, b, c, d, e, f, g, hh = h_
    m = [a, d, 0, g, b, e, 0, hh, 0, 0, 1, 0, c, f, 0, 1]
    return "matrix3d(" + ",".join(f"{v:.8f}" for v in m) + ")"


def _pos(x, y, w=None, h=None, z=2, quad=None, rot=0, extra=""):
    s = f"left:{x}px;top:{y}px;z-index:{z};"
    if w is not None: s += f"width:{w}px;"
    if h is not None: s += f"height:{h}px;"
    if quad:
        s = f"left:0;top:0;z-index:{z};width:{w}px;height:{h}px;transform-origin:0 0;transform:{_homog(w, h, quad)};"
    elif rot:
        s += f"transform:rotate({rot}deg);transform-origin:50% 50%;"
    return s + extra


# ---------------------------------------------------------------- mundos
def mundo(t, fmt="cheio", fundo="#000", entrada=("corte", 0), cam=None, nome="", mao=1.0):
    """Abre um mundo novo em t. cam = [(t_abs, escala, dx, dy, rot_graus[, ease])]."""
    m = {"id": _id("m"), "t": round(float(t), 3), "fmt": fmt, "fundo": fundo, "entrada": entrada, "els": [], "fixos": [], "nome": nome, "mao": mao, "cam": cam or []}
    CAMADA[0] = "cam"
    if cam:
        CAMS.append({"id": m["id"] + "c", "k": [list(k) for k in cam]})
    MUNDOS.append(m)
    return m


CAMADA = ["cam"]


def camada(qual):
    """'cam' = o que anda com a câmera (padrão); 'fixa' = interface por cima que não se mexe (visor, cabeçalho, texto que fica reto)."""
    CAMADA[0] = qual


def _el(htm):
    MUNDOS[-1]["fixos" if CAMADA[0] == "fixa" else "els"].append(htm)


def _entra(eid, t, ent, d=None, de=None):
    if t is None or t == "INI":
        return
    ANIMS.append({"k": "in", "id": eid, "t": round(float(t), 3), "ent": ent, "d": d, "de": de})


def _sai(eid, sai):
    if sai:
        t, tipo, d = (list(sai) + [None, None])[:3]
        ANIMS.append({"k": "out", "id": eid, "t": round(float(t), 3), "tipo": tipo or "seco", "d": d or 0.15, "de": None})


def foto(src, x=0, y=0, w=720, h=1280, z=0, filtro="", t="INI", ent="seco", d=None, sai=None, pos="50% 50%"):
    eid = _id("f")
    st = _pos(x, y, w, h, z) + f"background:url('{src}') {pos}/cover no-repeat;" + (f"filter:{filtro};" if filtro else "")
    # rede de segurança: a mesma foto ampliada e desfocada atrás (se a câmera girar/aproximar demais, o canto não fica vazio)
    _el(f'<div class="ab" style="left:{x - w * .45}px;top:{y - h * .45}px;width:{w * 1.9}px;height:{h * 1.9}px;z-index:{z - 1};'
        f'background:url(\'{src}\') {pos}/cover no-repeat;filter:blur(26px) brightness(.92);"></div>')
    _el(f'<div id="{eid}" class="ab cobre" style="{st}">{_cantos(True, w, h)}</div>')
    _entra(eid, t, ent, d); _sai(eid, sai)
    return eid


def img(src, x, y, w, h=None, z=3, t="INI", ent="seco", d=None, de=None, sai=None, rot=0, blur=0, sombra=False, quad=None, extra=""):
    eid = _id("i")
    f = []
    if blur: f.append(f"blur({blur}px)")
    if sombra: f.append("drop-shadow(8px 14px 14px rgba(0,0,0,.35))")
    st = _pos(x, y, w, h, z, quad, rot, (f"filter:{' '.join(f)};" if f else "") + extra)
    hh = f'height:{h}px;object-fit:cover;' if h else ''
    _el(f'<div id="{eid}" class="ab"  style="{st}"><img src="{src}" style="width:{w}px;{hh}display:block"></div>')
    _entra(eid, t, ent, d, de); _sai(eid, sai)
    return eid


FONTES = {"sans": "'Inter'", "mao": "'Caveat'", "giz": "'Kalam'", "mono": "'JetBrains Mono'", "lcd": "'VT323'", "pixel": "'Press Start 2P'"}
GIZ = "filter:url(#giz);"            # traço de giz: borda tremida + falhas de pó (use em extra= de texto/assenta)
LCD = "filter:url(#lcd);"            # texto de tela de aparelho: leve borrão + sombra interna de pixel


def _fonte(font, size, peso, cor, extra=""):
    return f"font-family:{FONTES.get(font, font)};font-size:{size}px;font-weight:{peso};color:{cor};{extra}"


def texto(htm, x, y, size=26, cor="#1a1a1a", peso=500, font="sans", w=None, h=None, alinh="left", z=4, t="INI",
          ent="blur", d=None, de=None, sai=None, rot=0, quad=None, ls=-0.01, lh=1.12, extra=""):
    eid = _id("t")
    st = _pos(x, y, w, h, z, quad, rot, _fonte(font, size, peso, cor) + f"text-align:{alinh};letter-spacing:{ls}em;line-height:{lh};" + extra)
    _el(f'<div id="{eid}" class="ab tx{" sup" if quad else ""}" style="{st}">{htm}{_cantos(quad, w, h)}</div>')
    _entra(eid, t, ent, d, de); _sai(eid, sai)
    return eid


_FONTES_TTF = {"sans": os.path.join(AQUI, "medir", "Inter-Variable.ttf")}


def _larg(txt, size, peso, font="sans", ls=0.0):
    """Largura do texto em px (mede com a fonte real; sem a fonte, estima 0,56 em por caractere)."""
    try:
        from PIL import ImageFont
        f = ImageFont.truetype(_FONTES_TTF[font], size)
        f.set_variation_by_axes([min(32, max(14, size)), peso])
        return f.getlength(txt) + ls * size * len(txt)
    except Exception:
        return 0.56 * size * len(txt) + ls * size * len(txt)


def assenta(palavras, x, y, w=680, size=24, cor="#1a1a1a", cinza="#8a8a8a", peso=500, font="sans", alinh="center",
            z=4, lh=1.15, sai=None, quad=None, rot=0, h=None, ls=-0.01, recentra=False, extra=""):
    """Linha que se monta palavra a palavra (medido: a palavra nasce menor, mais clara, abaixo e à direita, e assenta em
    6-8 quadros); a linha se RECENTRA a cada palavra nova (translação suave medida no navegador, sem reflow).
    palavras = [(texto, t[, css extra])]; ("\\n", None) quebra a linha."""
    eid = _id("a")
    st = _pos(x, y, w, h, z, quad, rot, _fonte(font, size, peso, cor) + f"line-height:{lh};letter-spacing:{ls}em;" + extra)
    linhas, cur = [], []
    for p in palavras:
        if p[0] == "\n":
            linhas.append(cur); cur = []
        else:
            cur.append(p)
    linhas.append(cur)
    htm = []
    for li, lin in enumerate(linhas):
        lid = f"{eid}l{li}"
        spans = []
        for k, p in enumerate(lin):
            sid = f"{lid}w{k}"
            css = p[2] if len(p) > 2 else ""
            spans.append(f'<span id="{sid}" class="wd" style="transform-origin:0 100%;margin-right:.26em;{css}">{p[0]}</span>')
            ANIMS.append({"k": "assenta", "id": sid, "t": round(float(p[1]), 3), "d": LEVA, "cor": cor, "cinza": cinza, "de": None,
                          "css_cor": ("color" in css)})
        ANIMS.append({"k": "linha", "id": lid, "t": round(float(lin[0][1]), 3) if lin else 0, "ts": [round(float(p[1]), 3) for p in lin],
                      "w": w, "al": alinh, "d": LEVA, "de": None, "re": recentra})
        htm.append(f'<div id="{lid}" style="position:absolute;left:0;top:{li * size * lh:.1f}px;display:flex;white-space:nowrap">{"".join(spans)}</div>')
    _el(f'<div id="{eid}" class="ab as{" sup" if quad else ""}" style="{st}">{"".join(htm)}{_cantos(quad, w, h)}</div>')
    _sai(eid, sai)
    return eid


def digita(txt, t0, x, y, cps=16.0, t1=None, size=26, cor="#1a1a1a", peso=500, font="sans", w=None, h=None, cursor="#1a1a1a",
           z=4, quad=None, rot=0, lh=1.2, sai=None, extra="", fixa=False, cursor_ate=None):
    """Digitação caractere a caractere a partir de t0 (cps caracteres/s, ou até t1). '\\n' quebra linha.
    O cursor pisca antes e depois (a cada 0,5 s). fixa=True: texto já completo (só o cursor)."""
    eid = _id("d")
    dur = (t1 - t0) if t1 else len(txt) / cps
    st = _pos(x, y, w, h, z, quad, rot, _fonte(font, size, peso, cor) + f"line-height:{lh};white-space:{'pre-wrap' if w else 'pre'};" + extra)
    _el(f'<div id="{eid}" class="ab{" sup" if quad else ""}" style="{st}"><span class="dg"></span><span class="cur" style="background:{cursor}"></span>{_cantos(quad, w, h)}</div>')
    ANIMS.append({"k": "digita", "id": eid, "t": round(float(t0), 3), "d": round(dur, 3), "txt": txt, "de": None, "fixa": fixa,
                  "cursor_ate": cursor_ate})
    _sai(eid, sai)
    return eid


def risco(pontos, t, d=0.35, cor="#d23", esp=3, z=5, curva=False, sai=None, ease="power1.inOut"):
    """Traço SVG que se desenha de pontos[0] a pontos[-1] (coordenadas do palco)."""
    eid = _id("r")
    if curva and len(pontos) == 3:
        (a, b), (c, d_), (e, f) = pontos; dd = f"M{a} {b} Q{c} {d_} {e} {f}"
    else:
        dd = "M" + " L".join(f"{a} {b}" for a, b in pontos)
    _el(f'<svg id="{eid}" class="ab deco" style="left:0;top:0;z-index:{z};overflow:visible" width="720" height="1280">'
        f'<path d="{dd}" pathLength="1" fill="none" stroke="{cor}" stroke-width="{esp}" stroke-linecap="round" '
        f'stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/></svg>')
    ANIMS.append({"k": "risco", "id": eid, "t": round(float(t), 3), "d": d, "de": None, "e": ease})
    _sai(eid, sai)
    return eid


def _cantos(quad, w, h):
    """Superfície em perspectiva: 4 marcadores nos cantos da caixa, lidos pelo auditor (medir/auditoria.mjs)."""
    if not quad: return ""
    return "".join(f'<i class="canto" style="left:{a}px;top:{b}px"></i>' for a, b in ((0, 0), (w, 0), (w, h), (0, h)))


def bloco(htm, x, y, w=None, h=None, z=3, t="INI", ent="seco", d=None, de=None, sai=None, rot=0, quad=None, extra="", eid=None):
    eid = eid or _id("b")
    st = _pos(x, y, w, h, z, quad, rot, extra)
    _el(f'<div id="{eid}" class="ab{" sup" if quad else ""}" style="{st}">{htm}{_cantos(quad, w, h)}</div>')
    _entra(eid, t, ent, d, de); _sai(eid, sai)
    return eid


def escreve(eid, t, d=0.3, suave=8):
    """Revela um texto da esquerda para a direita com borda SUAVE (como traço sendo escrito), sem letra decepada."""
    ANIMS.append({"k": "escreve", "id": eid, "t": round(float(t), 3), "d": d, "s": suave, "de": None, "novo": True})


def anim(eid, t, de, para, d=0.3, ease="power2.out", novo=False):
    """novo=True quando a animação é a ENTRADA de algo (conta como elemento novo na cadência)."""
    ANIMS.append({"k": "ft", "id": eid, "t": round(float(t), 3), "de": de, "para": para, "d": d, "e": ease, "novo": novo})


def conta(eid, t, de, ate, d=0.6, fmt="{}%", ease="power1.out"):
    ANIMS.append({"k": "conta", "id": eid, "t": round(float(t), 3), "a": de, "b": ate, "d": d, "fmt": fmt, "e": ease, "de": None})


def borda_filme(z=8, cor="#c98a3a", texto_="FILM 400", lado="ambos"):
    """Marcas de borda de filme na vertical (as do original citam uma marca; aqui é genérico)."""
    s = f"font-family:'JetBrains Mono';font-size:11px;letter-spacing:.32em;color:{cor};opacity:.75;"
    for x, r in (((26, 90),) if lado == "esq" else ((26, 90), (694, 90))):
        _el(f'<div class="ab deco" style="left:{x}px;top:640px;z-index:{z};{s}transform:translate(-50%,-50%) rotate({r}deg);white-space:nowrap">'
            f'{texto_} ▸ 24A &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {texto_} ▸ 25 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {texto_} ▸ 25A</div>')


def luz(t, d=0.5, x=360, y=500, tam=700, z=9, forte=0.85, arco=False):
    """Vazamento de luz: mancha quente (ou arco-íris) que acende e apaga em d segundos."""
    eid = _id("l")
    g = ("conic-gradient(from 200deg, rgba(255,80,80,.0), rgba(255,170,60,.55), rgba(255,240,120,.5), rgba(120,255,170,.45), "
         "rgba(90,170,255,.5), rgba(200,120,255,.4), rgba(255,80,80,0))") if arco else \
        "radial-gradient(circle, rgba(255,255,255,1) 0%, rgba(255,246,230,.85) 35%, rgba(255,230,200,0) 70%)"
    _el(f'<div id="{eid}" class="ab deco" style="left:{x - tam / 2}px;top:{y - tam / 2}px;width:{tam}px;height:{tam}px;z-index:{z};'
        f'border-radius:50%;background:{g};mix-blend-mode:screen;filter:blur({60 if arco else 30}px);opacity:0"></div>')
    ANIMS.append({"k": "luz", "id": eid, "t": round(float(t), 3), "d": d, "f": forte, "de": None})
    return eid


# ---------------------------------------------------------------- montagem do HTML
def montar():
    MUNDOS.sort(key=lambda m: m["t"])
    # cursor único: cada digitação apaga o cursor quando a próxima do mesmo mundo começa
    lim = [m["t"] for m in MUNDOS] + [DUR]
    digs = sorted([a for a in ANIMS if a["k"] == "digita"], key=lambda a: a["t"])
    for a in digs:
        fimm = min(x for x in lim if x > a["t"] + 1e-6)
        prox = [b["t"] for b in digs if a["t"] < b["t"] < fimm]
        a["ate"] = a.get("cursor_ate") or (prox[0] if prox else None)
    body, tr = [], []
    for k, m in enumerate(MUNDOS):
        fim = MUNDOS[k + 1]["t"] if k + 1 < len(MUNDOS) else DUR
        nxt = MUNDOS[k + 1] if k + 1 < len(MUNDOS) else None
        ini = m["t"]
        tipo, td = (list(m["entrada"]) + [0])[:2] if isinstance(m["entrada"], (list, tuple)) else (m["entrada"], 0)
        if tipo in ("zoom", "dissolve") and td:
            ini = max(0, ini - td / 2)                  # o mundo novo começa a aparecer antes do corte
        ntipo, ntd = ((list(nxt["entrada"]) + [0])[:2] if isinstance(nxt["entrada"], (list, tuple)) else (nxt["entrada"], 0)) if nxt else ("corte", 0)
        if ntipo in ("zoom", "dissolve") and ntd:
            fim = fim + ntd / 2                          # o antigo fica até a dissolvência terminar
        clip = ""
        if m["fmt"] == "faixa":
            a, b = FAIXA
            clip = f"clip-path:inset({a}px 0 {1280 - b}px 0);"
        bg = "#000" if m["fmt"] == "faixa" else m["fundo"]
        inner_bg = f"background:{m['fundo']};" if m["fmt"] == "faixa" else ""
        body.append(
            f'<div id="{m["id"]}" class="clip mundo" data-start="{round(ini, 4)}" data-duration="{round(fim - ini, 4)}" '
            f'data-track-index="{1 + k % 2}" style="z-index:{k + 1};background:{bg}">'
            f'<div class="fx" style="{clip}"><div class="tr"><div class="mao" data-mao="{m.get("mao", 1.0)}">'
            f'<div id="{m["id"]}c" class="cam" style="{inner_bg}">' + "\n".join(m["els"]) +
            '</div></div></div>' + "\n".join(m["fixos"]) + '</div></div>')
        tr.append({"id": m["id"], "t": m["t"], "tipo": tipo, "d": td, "ini": ini})
    # grão: deslocamentos pseudo-aleatórios a cada 2 quadros (determinístico)
    rnd = random.Random(7)
    grao = [[round(i * 2 / FPS, 4), rnd.randint(0, 255), rnd.randint(0, 255)] for i in range(int(DUR * FPS / 2) + 1)]
    fonts = f"""
@font-face{{font-family:'Inter';src:url('assets/fonts/Inter-var.woff2') format('woff2');font-weight:100 900}}
@font-face{{font-family:'Caveat';src:url('assets/fonts/Caveat-700-latin.woff2') format('woff2');font-weight:700}}
@font-face{{font-family:'Caveat';src:url('assets/fonts/Caveat-400-latin.woff2') format('woff2');font-weight:400}}
@font-face{{font-family:'JetBrains Mono';src:url('assets/fonts/JetBrainsMono-Regular.woff2') format('woff2')}}
@font-face{{font-family:'Kalam';src:url('assets/fonts/Kalam-400-latin.woff2') format('woff2');font-weight:400}}
@font-face{{font-family:'Kalam';src:url('assets/fonts/Kalam-400-latin-ext.woff2') format('woff2');font-weight:400;unicode-range:U+0100-024F,U+1E00-1EFF}}
@font-face{{font-family:'Kalam';src:url('assets/fonts/Kalam-700-latin.woff2') format('woff2');font-weight:700}}
@font-face{{font-family:'VT323';src:url('assets/fonts/vt323-latin-400-normal.woff2') format('woff2')}}
@font-face{{font-family:'Press Start 2P';src:url('assets/fonts/press-start-2p-latin-400-normal.woff2') format('woff2')}}"""
    H = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{html.escape(PROJ.get("titulo", "Reel estilo B"))}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{fonts}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#stage{{position:absolute;left:0;top:0;width:720px;height:1280px;transform:scale(1.5);transform-origin:0 0;overflow:hidden}}
.mundo{{position:absolute;inset:0;overflow:hidden}}
.fx{{position:absolute;inset:0;overflow:hidden}}
.tr,.mao{{position:absolute;inset:0;transform-origin:50% 50%}}
.cam{{position:absolute;inset:0;transform-origin:50% 50%;will-change:transform}}
.ab{{position:absolute}}
.deco,#grao,#branco,.canto{{pointer-events:none}}
.canto{{position:absolute;width:1px;height:1px;margin:-.5px 0 0 -.5px;opacity:0}}
.tx{{white-space:nowrap}}
.as .asl{{display:flex;flex-wrap:wrap;align-items:baseline;column-gap:.26em}}
.as .br{{flex-basis:100%;height:0}}
.wd{{display:inline-block;opacity:0;white-space:nowrap}}
.cur{{display:inline-block;width:.08em;height:1.05em;margin-left:.04em;vertical-align:-.14em}}
#grao{{position:absolute;inset:-20px;z-index:900;pointer-events:none;background:url('assets/grao.png');background-size:256px 256px;mix-blend-mode:overlay;opacity:.38}}
#branco{{position:absolute;inset:0;z-index:901;background:#fff;opacity:0}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920" data-fps="30">
<audio id="audio" class="clip" src="{AUDIO}" data-start="0" data-duration="{DUR}" data-track-index="0" data-volume="1"></audio>
<div id="stage">
{chr(10).join(body)}
<svg width="0" height="0" style="position:absolute"><defs>
<filter id="giz" x="-5%" y="-20%" width="110%" height="140%"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="4" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="2.4" result="d"/><feTurbulence type="fractalNoise" baseFrequency="0.55" numOctaves="3" seed="9" result="m"/>
<feColorMatrix in="m" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.7 1.55" result="ma"/>
<feComposite in="d" in2="ma" operator="in" result="g"/><feGaussianBlur in="g" stdDeviation=".35"/></filter>
<filter id="lcd"><feGaussianBlur stdDeviation=".45" result="b"/><feOffset in="b" dx=".8" dy=".8" result="o"/>
<feColorMatrix in="o" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .25 0" result="s"/><feMerge><feMergeNode in="s"/><feMergeNode in="b"/></feMerge></filter>
</defs></svg>
<div id="grao"></div><div id="branco"></div>
</div>
</div>
<script>
const A = {json.dumps(ANIMS)};
const TR = {json.dumps(tr)};
const CAMS = {json.dumps(CAMS)};
const GRAO = {json.dumps(grao)};
const tl = gsap.timeline({{ paused: true }});
const $ = (i) => document.getElementById(i);
// ---- entradas e saídas de elementos
for (const a of A) {{
  const el = $(a.id); if (!el) continue;
  const d = a.d || 0;
  if (a.k === "in") {{
    const D = d || ({{seco: 0, blur: 0.15, fade: 0.25, assenta: 0.22, voa: 0.45, pop: 0.3, entra: 0.4}})[a.ent] || 0;
    if (a.ent === "seco" || !D) tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.001 }}, a.t);
    else if (a.ent === "blur") tl.fromTo(el, {{ opacity: 0, filter: "blur(10px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: D, ease: "power1.out" }}, a.t);
    else if (a.ent === "fade") tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: D, ease: "none" }}, a.t);
    else if (a.ent === "assenta") tl.fromTo(el, {{ opacity: 0, x: 8, y: 8, scale: .82 }}, {{ opacity: 1, x: 0, y: 0, scale: 1, duration: D, ease: "power2.out" }}, a.t);
    else if (a.ent === "pop") tl.fromTo(el, {{ opacity: 0, scale: .55 }}, {{ opacity: 1, scale: 1, duration: D, ease: "back.out(2)" }}, a.t);
    else if (a.ent === "entra") {{ const f = a.de || [300, 0, 0, 1];
      tl.fromTo(el, {{ opacity: 1, x: f[0], y: f[1], rotation: f[2], scale: f[3] }}, {{ opacity: 1, x: 0, y: 0, rotation: 0, scale: 1, duration: D || 0.4, ease: "power2.out", immediateRender: false }}, a.t);
      tl.set(el, {{ opacity: 0 }}, 0); tl.set(el, {{ opacity: 1 }}, a.t); }}
    else if (a.ent === "voa") {{ const f = a.de || [0, 120, 0, 1];
      tl.fromTo(el, {{ opacity: 0, x: f[0], y: f[1], rotation: f[2], scale: f[3] }}, {{ opacity: 1, x: 0, y: 0, rotation: 0, scale: 1, duration: D, ease: "expo.out" }}, a.t); }}
  }}
  else if (a.k === "out") {{
    if (a.tipo === "seco") tl.to(el, {{ opacity: 0, duration: 0.001 }}, a.t);
    else if (a.tipo === "fade") tl.to(el, {{ opacity: 0, duration: d, ease: "none" }}, a.t);
    else if (a.tipo === "blur") tl.to(el, {{ opacity: 0, filter: "blur(10px)", duration: d, ease: "power1.in" }}, a.t);
  }}
  else if (a.k === "assenta") {{
    const de = {{ opacity: .7, y: 6, x: 5, scale: .86 }}, pa = {{ opacity: 1, y: 0, x: 0, scale: 1, duration: d, ease: "power2.out" }};
    if (!a.css_cor) {{ de.color = a.cinza; pa.color = a.cor; }}
    gsap.set(el, {{ opacity: 0 }}); tl.set(el, {{ opacity: 0 }}, 0);                       // invisível até a hora dela
    pa.immediateRender = false; tl.fromTo(el, de, pa, a.t);
  }}
  else if (a.k === "linha") {{
    // recentra a linha a cada palavra: posição calculada no navegador (com a fonte já carregada) na hora do 1º render
    const sp = Array.from(el.children), W = a.w;
    const vis = (k) => {{ const s = sp[k]; return s.offsetLeft + s.offsetWidth; }};
    const off = (k) => a.al === "center" ? (W - vis(k)) / 2 : (a.al === "right" ? W - vis(k) : 0);
    if (!a.re) tl.set(el, {{ x: () => off(sp.length - 1) }}, 0);          // layout final reservado: a palavra nasce no lugar
    else {{ tl.set(el, {{ x: () => off(0) }}, Math.max(0, a.ts[0] - 0.01));
      for (let k = 1; k < sp.length; k++) tl.to(el, {{ x: () => off(k), duration: d, ease: "power2.out" }}, a.ts[k]); }}
  }}
  else if (a.k === "digita") {{
    const tx = el.querySelector(".dg"), cur = el.querySelector(".cur"), s = a.txt, st = {{ n: a.fixa ? s.length : 0 }};
    const put = () => {{ tx.textContent = s.slice(0, Math.round(st.n)); }};
    put();
    if (!a.fixa) tl.fromTo(st, {{ n: 0 }}, {{ n: s.length, duration: d, ease: "none", onUpdate: put, immediateRender: false }}, a.t);
    // cursor: aceso enquanto digita, pisca 0,5 s antes e depois
    gsap.set(cur, {{ opacity: 0 }}); tl.set(cur, {{ opacity: 1 }}, a.t);
    for (let k = 0; k < 40; k++) {{ const tt = a.t + d + 0.25 + k * 0.5; if (a.ate && tt >= a.ate) break; tl.set(cur, {{ opacity: k % 2 ? 1 : 0 }}, tt); }}
    if (a.ate) tl.set(cur, {{ opacity: 0 }}, a.ate);
  }}
  else if (a.k === "escreve") {{
    const mk = (p) => `linear-gradient(90deg,#000 ${{p - a.s}}%,transparent ${{p}}%)`, st = {{ p: 0 }};
    const put = () => {{ el.style.webkitMaskImage = mk(st.p); el.style.maskImage = mk(st.p); }};
    put(); tl.fromTo(st, {{ p: 0 }}, {{ p: 100 + a.s, duration: d, ease: "none", onUpdate: put, immediateRender: false }}, a.t);
  }}
  else if (a.k === "risco") tl.fromTo(el.querySelector("path"), {{ strokeDashoffset: 1.1 }}, {{ strokeDashoffset: 0, duration: d, ease: a.e }}, a.t);
  else if (a.k === "ft") tl.fromTo(el, a.de, Object.assign({{ duration: d, ease: a.e, immediateRender: false }}, a.para), a.t);
  else if (a.k === "conta") {{
    const st = {{ v: a.a }}; const put = () => {{ el.textContent = a.fmt.replace("{{}}", Math.round(st.v)); }}; put();
    tl.fromTo(st, {{ v: a.a }}, {{ v: a.b, duration: d, ease: a.e, onUpdate: put, immediateRender: false }}, a.t);
  }}
  else if (a.k === "luz") {{
    tl.fromTo(el, {{ opacity: 0, scale: .7 }}, {{ opacity: a.f, scale: 1.15, duration: d * .45, ease: "power2.out" }}, a.t);
    tl.to(el, {{ opacity: 0, scale: 1.35, duration: d * .55, ease: "power1.in" }}, a.t + d * .45);
  }}
}}
// ---- transições entre mundos
for (let k = 0; k < TR.length; k++) {{
  const m = TR[k], el = $(m.id), prev = k ? $(TR[k - 1].id) : null, d = m.d || 0;
  if (m.tipo === "zoom" && prev) {{
    tl.to(prev.querySelector(".tr"), {{ scale: 3.0, filter: "blur(9px) brightness(1.6)", duration: d, ease: "power2.in" }}, m.t - d / 2);
    tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: d, ease: "power1.out" }}, m.t - d / 2);
    tl.fromTo(el.querySelector(".tr"), {{ filter: "blur(9px)" }}, {{ filter: "blur(0px)", duration: d, ease: "power1.out" }}, m.t - d / 2);
  }} else if (m.tipo === "dissolve" && prev) {{
    // sobreposição curta (20 % da duração) com os dois mundos borrados: sem quadro preto e sem dois textos nítidos juntos
    tl.to(prev.querySelector(".tr"), {{ filter: "blur(10px)", duration: d / 2, ease: "power1.in" }}, m.t - d / 2);
    tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: d * .7, ease: "power1.inOut", immediateRender: false }}, m.t - d * .35);
    tl.fromTo(el.querySelector(".tr"), {{ filter: "blur(10px)" }}, {{ filter: "blur(0px)", duration: d * .7, ease: "power1.out", immediateRender: false }}, m.t - d * .35);
    tl.set(el, {{ opacity: 0 }}, 0);
  }} else if (m.tipo === "preto") {{
    tl.fromTo(el.querySelector(".tr"), {{ filter: "brightness(.22)" }}, {{ filter: "brightness(1)", duration: d, ease: "power1.out" }}, m.t + 1 / 30);
  }} else if (m.tipo === "flash") {{
    tl.fromTo("#branco", {{ opacity: 0 }}, {{ opacity: 1, duration: d * .5, ease: "power2.in" }}, m.t - d * .5);
    tl.to("#branco", {{ opacity: 0, duration: d * .8, ease: "power2.out" }}, m.t);
  }}
}}
// ---- câmeras: keyframes (t, escala, dx, dy, rot[, ease]) por mundo
for (const c of CAMS) {{
  const el = $(c.id), K = c.k;
  gsap.set(el, {{ scale: K[0][1], x: K[0][2], y: K[0][3], rotation: K[0][4] }});
  tl.set(el, {{ scale: K[0][1], x: K[0][2], y: K[0][3], rotation: K[0][4] }}, Math.max(0, K[0][0] - 0.001));
  for (let i = 1; i < K.length; i++) {{
    tl.to(el, {{ scale: K[i][1], x: K[i][2], y: K[i][3], rotation: K[i][4], duration: Math.max(0.001, K[i][0] - K[i - 1][0]), ease: K[i][5] || "none" }}, K[i - 1][0]);
  }}
}}
// ---- câmera de mão
const MAOS = [...document.querySelectorAll(".mao")], st_mao = {{ t: 0 }};
const mao = () => {{ const t = st_mao.t; MAOS.forEach((m, i) => {{ const k = +m.dataset.mao, f = i * 1.7;
  gsap.set(m, {{ x: k * (3.4 * Math.sin(1.9 * t + f) + 1.8 * Math.sin(4.7 * t + 2 * f)), y: k * (3.0 * Math.sin(1.5 * t + f + 1) + 1.6 * Math.sin(5.1 * t + f)),
                 rotation: k * 0.32 * Math.sin(1.3 * t + f), scale: 1 + k * 0.02 }}); }}); }};
mao(); tl.fromTo(st_mao, {{ t: 0 }}, {{ t: {DUR}, duration: {DUR}, ease: "none", onUpdate: mao, immediateRender: false }}, 0);
// ---- grão do filme
const g = $("grao");
for (const [t, x, y] of GRAO) tl.set(g, {{ backgroundPosition: x + "px " + y + "px" }}, t);
tl.set({{}}, {{}}, {DUR});
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
    open(os.path.join(AQUI, "index.html"), "w").write(H)
    json.dump(SONS, open(os.path.join(AQUI, "medir", "sons.json"), "w"), indent=0)
    json.dump(TRILHA_PTS, open(os.path.join(AQUI, "medir", "trilha.json"), "w"), indent=0)
    els = [{"mundo": m["id"], "nome": m["nome"], "t": m["t"], "fmt": m["fmt"],
            "entrada": (m["entrada"][0] if isinstance(m["entrada"], (list, tuple)) else m["entrada"])} for m in MUNDOS]
    json.dump({"duracao": DUR, "mundos": els, "anims": ANIMS, "cams": CAMS}, open(os.path.join(AQUI, "medir", "elementos.json"), "w"), indent=0)
    print(f"{len(MUNDOS)} mundos · {len(ANIMS)} animações · {len(CAMS)} câmeras · {len(SONS)} sons · {DUR} s")


if __name__ == "__main__":
    ns = {k: v for k, v in globals().items() if not k.startswith("__")}
    exec(open(os.path.join(AQUI, "mundos.py")).read(), ns)
    exec(open(os.path.join(AQUI, "cenas.py")).read(), ns)
    montar()
