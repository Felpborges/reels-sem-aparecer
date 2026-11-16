#!/usr/bin/env python3
"""MOTOR REEL EDITORIAL · gera index.html a partir da tabela de cenas (cenas.py). Manual: MOTOR.md do motor editorial, na skill.

Coordenadas em espaço 720x1280 (o palco é escalado 1.5x para 1080x1920).
Os tempos vêm do alinhamento forçado da narração (medir/alinhamento.json): P(i) = entrada na i-ésima palavra falada.
A geometria vem toda da tabela. A câmera de cada cena é um modelo simples (deriva lenta + assentamento rápido).
"""
import json, html, os, re, math

AQUI = os.path.dirname(os.path.abspath(__file__))
ONS = json.load(open(os.path.join(AQUI, "medir", "alinhamento.json")))     # [{text, start, end}] por palavra falada
PROJ = json.load(open(os.path.join(AQUI, "projeto.json")))
DUR = round(ONS[-1]["end"] + 0.2, 2)                   # o reel acaba na última palavra (como o original)
BG = "#fefefe"
MEDIR = os.environ.get("MEDIR") == "1"          # sem câmera, para conferir a composição parada
ADIANTA = 0.05                                  # a imagem entra um quadro e meio antes do som da palavra
AUDIO = "assets/mix.m4a" if os.path.exists(os.path.join(AQUI, "assets", "mix.m4a")) and os.environ.get("SO_VOZ") != "1" else "assets/narracao.wav"


def _load(nome, padrao):
    p = os.path.join(AQUI, "medir", nome)
    return json.load(open(p)) if os.path.exists(p) else padrao


LAY = {}                                         # (no motor de recriação vinha da medição contra a referência; aqui a tabela manda)
CAM = {}                                         # preenchido por cena a partir de scene(cam=...)
# Dissolvências (início da cena nova em quadros): (a antiga começa a sumir em, some de vez em, tipo). O resto é corte seco.
DISS = {}
QX = {}                                          # tempos fixados na tabela: mandam sobre a medição
TW = {}                                          # índice da palavra falada -> tempo medido na tela da referência
SCRIPT = []
NOFIT = []                                       # elementos cuja geometria não deve ser mexida pela medição
PASSO = 1
ELEMS = []
SONS = []                                        # efeitos sonoros amarrados às entradas visuais: (tipo, tempo)
FONTS = {"s": "Poppins", "b": "Grand Hotel", "o": "Grand Hotel", "d": "Playfair Display", "h": "Helvetica Neue", "t": "Sacramento"}


class _Q(float):
    d = 0.0


def Q(f, d=0):
    """Entra exatamente no quadro f da referência; d = quadros que a entrada leva (0 = aparece de uma vez)."""
    q = _Q((f - 1) / 30 if d else (f - 0.5) / 30)
    q.d = round((d + 1) / 30, 4) if d else 0.0
    return q


def P(i, d=0, antes=0.0):
    """Entra na i-ésima palavra falada (índice em medir/alinhamento.json); d = quadros que a entrada leva; antes = segundos a adiantar."""
    q = _Q(max(0.0, ONS[i]["start"] - ADIANTA - antes)); q.d = round((d + 1) / 30, 4) if d else 0.0
    return q


def S(seg, d=0):
    """Entra num tempo absoluto em segundos."""
    q = _Q(seg); q.d = round((d + 1) / 30, 4) if d else 0.0
    return q


INI = "INI"                                      # o elemento já está na tela no primeiro quadro da cena


def MED(eid):
    g = dict(LAY.get(eid, {}))
    if eid in QX:
        g.pop("ini", None); g.pop("d", None); g.update(QX[eid])
    return g


def auto(size):
    m = cur["cal"]
    if m == "none":
        return size
    if m == "hr":
        return size * (1.12 if size < 70 else 1.0)
    for lim, k in ((22, 1.7), (30, 1.6), (36, 1.42), (52, 1.3), (70, 1.2), (92, 1.08)):
        if size <= lim:
            return size * k
    return size


SCENES = []
cur = None


def W(i):
    """Tempo em que a palavra de índice i aparece: medido na referência se houver, senão o da fala."""
    return TW.get(i, ONS[i][0] - 0.03)


def T(v, eid=None):
    """int = índice da palavra falada; float = tempo absoluto; Q/INI = verdade lida na referência."""
    if isinstance(v, int) and not isinstance(v, bool):
        v = P(v)
    if isinstance(v, str):
        if eid: QX[eid] = {"ini": True}
        return cur["start"]
    if isinstance(v, _Q):
        if eid: QX[eid] = {"d": v.d}
        return round(max(float(v), cur["start"]), 4)
    if eid and "t" in LAY.get(eid, {}):
        t = LAY[eid]["t"]
        if isinstance(v, int) and PASSO == 1:
            TW.setdefault(v, t)
    else:
        t = W(v) if isinstance(v, int) else float(v)
    return round(min(max(t, cur["start"]), DUR - 0.05), 4)


def reg(eid, kind, t, out=None):
    ELEMS.append({"id": eid, "n": len(SCENES), "k": kind, "t": t, "out": out})


def _id():
    return f"s{len(SCENES):02d}e{len(cur['els']) - cur.get('nfix', 0)}"


def _pos(x, y, anc, z, extra=""):
    tr = {"c": "translate(-50%,-50%)", "l": "translate(0,-50%)", "r": "translate(-100%,-50%)", "tl": "none", "tc": "translate(-50%,0)"}[anc]
    return f'left:{x}px;top:{y}px;transform:{tr};z-index:{z};{extra}'


def L(parts, x, y, size, font="s", wt=None, col="#111", anc="c", ls=None, z=4, out=None, typed=False, it=False, lh=1.0, c=None,
      fx=False, k=1, dxy=(0, 0), nofit=False, ws=None, liso=True, sombra=None, abre=0, fino=False):
    """Linha de palavras; cada palavra entra no seu próprio tempo. parts = [(texto, t), ...]
    fx = geometria da tabela vale (ignora a medida) · nofit = usa a medida, mas congela (com k e dxy por cima)."""
    if isinstance(parts, tuple):
        parts = [parts]
    eid = _id()
    fam = FONTS[font]
    if wt is None:
        wt = {"s": 600, "d": 500, "h": 400}.get(font, 400)
    size = round(size * c if c is not None else auto(size), 1)
    if ls is None or font in "bo":               # manuscrita ligada: espaçamento 0, senão as letras desencostam
        ls = -0.035 if font == "s" else 0
    man = font in "bo"                           # manuscrita (Grand Hotel inclinada): b = traço reforçado, o = traço normal
    claro = col.lower() in ("#fff", "#ffffff")

    def estilo(sz):
        st = f"font-family:'{fam}';font-weight:{wt};font-size:{sz}px;color:{col};letter-spacing:{ls}em;line-height:{lh};"
        if it or font == "d":
            st += "font-style:italic;"
        if font == "b" and not fino:             # pincel: o traço da mesma cor engrossa a letra
            st += f"-webkit-text-stroke:{sz / 70:.2f}px {col};"
        if font == "h":
            st += "font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;letter-spacing:-0.01em;"
        if ws:
            st += f"word-spacing:{ws}em;"
        if sombra or (claro and sombra is None):
            st += "text-shadow:0 2px 12px rgba(0,0,0,.42);"
        return st

    tx = (lambda s: f'<i class="sk">{html.escape(s)}</i>') if man else html.escape
    tout = T(out) if out is not None else None
    if font in "bo":                             # registro das palavras manuscritas (para conversão de fonte)
        g0 = MED(f"{eid}w0")
        solta = "cx" in g0 and not fx
        SCRIPT.append({"id": eid, "txt": " ".join(p[0] for p in parts), "font": font, "liso": liso, "anc": "c" if solta else anc, "ls": ls,
                       "x": round(g0["cx"] + dxy[0], 1) if solta else x, "y": round(g0["cy"] + dxy[1], 1) if solta else y,
                       "fs": round(g0.get("fs", size) * k, 1) if solta else size, "solta": solta, "n": len(SCENES)})
    spans, soltas = [], []
    for j, (txt, t) in enumerate(parts):
        wid = f"{eid}w{j}"
        t0 = T(t, wid)
        g = MED(wid)
        reg(wid, "t" if typed else "w", t0, tout)
        if fx or nofit:
            NOFIT.append(wid)
        if not g.get("ini"):
            cur["anims"].append({"k": "typed" if typed else "in", "id": wid, "t": t0, "col": col, "d": g.get("d", 0.27 if typed else 0), "y": 45})
        if "cx" in g and not fx:                # geometria medida: a palavra vira um elemento próprio
            soltas.append(f'<div class="pos" style="{_pos(round(g["cx"] + dxy[0] + (j - (len(parts) - 1) / 2) * abre, 1), round(g["cy"] + dxy[1], 1), "c", z)}"><span class="wd" id="{wid}" style="{estilo(round(g.get("fs", size) * k, 1))}">{tx(txt)}</span></div>')
            if tout is not None:
                cur["anims"].append({"k": "out", "id": wid, "t": tout})
        else:
            spans.append(f'<span class="wd" id="{wid}">{tx(txt)}</span>')
    if spans:
        cur["els"].append(f'<div class="pos" style="{_pos(x, y, anc, z)}"><div class="ln" id="{eid}" style="{estilo(size)}">{" ".join(spans)}</div></div>')
        if tout is not None:
            cur["anims"].append({"k": "out", "id": eid, "t": tout})
    else:
        cur["els"].append("")                    # mantém a numeração dos ids estável
    cur["els"] += soltas
    cur["nfix"] = cur.get("nfix", 0) + len(soltas)
    return eid


def _aj(eid, x, y, fixo=False):
    g = {} if fixo else LAY.get(eid, {})
    return round(x + g.get("dx", 0), 1), round(y + g.get("dy", 0), 1), g.get("k", 1)


SOMBRAS = {"card": "14px 20px 34px rgba(0,0,0,.32)", "card2": "28px 32px 56px rgba(0,0,0,.30)", "circle": "10px 14px 24px rgba(0,0,0,.35)"}


def I(src, x, y, w, t=None, h=None, kind="", fade=0.3, z=2, mask=None, out=None, outd=0, cut=False, gray=None, grayd=13, pos="center top",
      filt="", shadow=None, anc="tc", extra="", sobe=0, ease="none"):
    """Imagem. x = centro, y = topo. kind: card | card2 (sombra larga) | flat (cartão sem sombra) | circle. Entra por opacidade simples."""
    eid = _id()
    t0 = T(t if t is not None else cur["start"], eid)
    x, y, k = _aj(eid, x, y)
    w = round(w * k, 1)
    h = round(h * k, 1) if h else h
    wrap = f"width:{w}px;" + (f"height:{h}px;overflow:hidden;" if h else "")
    if kind in SOMBRAS:
        wrap += f"box-shadow:{SOMBRAS[kind]};"
    if kind == "circle":
        wrap += "border-radius:50%;overflow:hidden;"
    if shadow:
        wrap += f"filter:{shadow};"
    if mask:
        g = f"linear-gradient(to bottom,#000 {mask[0]}%,transparent {mask[1]}%)"
        wrap += f"-webkit-mask-image:{g};mask-image:{g};"
    ist = "width:100%;display:block;" + (f"height:100%;object-fit:cover;object-position:{pos};" if h else "") + (f"filter:{filt};" if filt else "")
    cur["els"].append(f'<div class="pos" style="{_pos(x, y, anc, z)}"><div class="im" id="{eid}" style="{wrap}"><img id="{eid}i" src="assets/img/{src}" style="{ist}">{extra}</div></div>')
    tout = T(out) if out is not None else None
    if MED(eid).get("ini"):
        cut = True
    reg(eid, "i", cur["start"] if cut else t0, tout)
    if not cut:
        an = {"k": "some", "id": eid, "t": t0, "d": MED(eid).get("d") or fade, "y": sobe, "e": ease}
        if isinstance(sobe, (list, tuple)):      # [(quadro, px abaixo do lugar final), ...] lido na referência
            an["y"] = 0; an["pts"] = [[round(f / 30, 4), y_] for f, y_ in sobe]
        cur["anims"].append(an)
    if gray is not None:
        cur["anims"].append({"k": "gray", "id": eid + "i", "t": T(gray), "d": round(grayd / 30, 4)})
    if tout is not None:
        cur["anims"].append({"k": "outf", "id": eid, "t": tout, "d": round(outd / 30, 4)} if outd else {"k": "out", "id": eid, "t": tout})
    return eid


def BADGES(xs, y, d, times, nums=(1, 2, 3), z=5, sobe=None, vem=None):
    """Selos numerados. Molde lido na referência: nascem abaixo e à esquerda (proporcional ao tamanho) e assentam
    desacelerando em 28 quadros, enquanto a opacidade entra em 15."""
    sobe = round(0.455 * d, 1) if sobe is None else sobe
    vem = round(-0.14 * d, 1) if vem is None else vem
    for x, t, n in zip(xs, times, nums):
        eid = _id()
        t0 = T(t, eid)
        xx, yy, k = _aj(eid, x, y)
        dd = round(d * k, 1)
        cur["els"].append(f'<div class="pos" style="{_pos(xx, yy, "c", z)}"><div class="badge" id="{eid}" style="width:{dd}px;height:{dd}px;font-size:{round(dd * .66)}px">{n}</div></div>')
        if not MED(eid).get("ini"):
            cur["anims"].append({"k": "selo", "id": eid, "t": t0, "d": round(14 / 30, 4), "y": sobe, "x": vem})
        reg(eid, "b", t0)


def PILL(inner, x, y, t, size=22, pad="10px 20px", z=5, out=None, fam="s", w=None, cor="#fff", raio=10, fixo=False, sombra=None, sobe=0, ease="power1.out"):
    eid = _id()
    t0 = T(t, eid)
    x, y, k = _aj(eid, x, y, fixo)
    cls = "pill ph" if fam == "h" else "pill"
    st = f"font-size:{round(size * k, 1)}px;padding:{pad};color:{cor};border-radius:{raio}px;" + (f"width:{w}px;" if w else "") + (f"box-shadow:{sombra};" if sombra else "")
    cur["els"].append(f'<div class="pos" style="{_pos(x, y, "c", z)}"><div class="{cls}" id="{eid}" style="{st}">{inner}</div></div>')
    if fixo:
        NOFIT.append(eid)
    if not MED(eid).get("ini"):
        cur["anims"].append({"k": "in", "id": eid, "t": t0, "d": MED(eid).get("d") or 0.2, "y": sobe, "e": ease})
    tout = T(out) if out is not None else None
    reg(eid, "p", t0, tout)
    if tout is not None:
        cur["anims"].append({"k": "out", "id": eid, "t": tout})
    return eid


def RAW(markup, x, y, t=None, z=3, anc="c", fade=0.3, out=None, cut=False, kind=None):
    """Desenho em SVG/HTML. Entra por opacidade simples."""
    eid = _id()
    t0 = T(t if t is not None else cur["start"], eid)
    x, y, k = _aj(eid, x, y)
    sc = f' style="transform:scale({k});transform-origin:50% 50%"' if k != 1 else ""
    cur["els"].append(f'<div class="pos" style="{_pos(x, y, anc, z)}"><div id="{eid}"><div{sc}>{markup}</div></div></div>')
    tout = T(out) if out is not None else None
    if MED(eid).get("ini"):
        cut = True
    if not cut:
        d = MED(eid).get("d")
        cur["anims"].append({"k": "some", "id": eid, "t": t0, "d": fade if d is None else d, "y": 0})
    reg(eid, "r", t0, tout)
    if tout is not None:
        cur["anims"].append({"k": "out", "id": eid, "t": tout})
    return eid


def SOM(tipo, t):
    """Efeito sonoro no instante visual t (P(i), S(seg) ou INI = início da cena). Tipos medidos no original:
    impacto · pop · pop-longo · clique · clique-grave · painel."""
    SONS.append((tipo, round(cur["start"] + 0.0002 if t == INI else float(T(t)), 4)))


def ANIM(**kw):
    if "t" in kw:
        kw["t"] = T(kw["t"])
    cur["anims"].append(kw)


def scene(start, blobs=False, bg=None, cal="none", cam=None):
    """start = índice da palavra que abre a cena (corta 0,10 s antes dela) ou tempo em segundos.
    cam = (escala inicial, dx inicial, dy inicial): a câmera vai disso até (1, 0, 0) ao longo da cena."""
    global cur
    if isinstance(start, int) and not isinstance(start, bool):
        start = max(0.0, ONS[start]["start"] - 0.10)
    f = round(start * 30)
    # um fio antes do quadro: a cena nova já vale no quadro do corte e a anterior acaba nele (sem quadro em branco)
    cur = {"start": round(f / 30 - 0.0002, 5), "f": f, "corte": f not in DISS, "blobs": blobs, "bg": bg, "cal": cal, "cam": cam, "els": [], "anims": []}
    SCENES.append(cur)
    return cur


CENAS_SRC = open(os.path.join(AQUI, "cenas.py")).read()
for PASSO in (1, 2):                             # passo 1 descobre os tempos medidos; o 2 monta com eles
    SCENES.clear(); ELEMS.clear(); SONS.clear(); NOFIT.clear(); QX.clear(); SCRIPT.clear(); cur = None
    exec(CENAS_SRC)


# ---------- montagem ----------
def _estrela():
    """Mancha dos cantos: contorno único e liso (5 braços de ponta arredondada, junções côncavas), gerado por medir/mancha_forma.py."""
    forma = json.load(open(os.path.join(AQUI, "medir", "mancha_forma.json")))
    return f'<path d="{forma["d"]}" fill="#5e5e5e"/>'


# Manchas dos cantos: no original são uma animação própria, igual em toda cena e independente da câmera. O miolo sai do
# quadro em linha reta enquanto a mancha cresce (lido quadro a quadro). MANCHA_T0 = em que quadro desse "clipe" a cena começa
# (a cena 1808 continua a de 1754; a última entra com o clipe já adiantado).

def mancha(q):
    """Quadro q do clipe -> centro da mancha de cima/direita, centro da de baixo/esquerda, tamanho (px)."""
    return (636 + 0.65 * q, 84 - 1.6 * q), (89 - 0.85 * q, 1200 + 1.65 * q), 505 * (1 + 0.004 * q)


BLOB = '<svg viewBox="-300 -300 600 600" width="{s}" height="{s}">' + _estrela() + '</svg>'

body, anims, cams, info = [], [], {}, []
for n, sc in enumerate(SCENES, 1):
    sid = f"s{n:02d}"
    ult = n == len(SCENES)
    nxt = DUR if ult else SCENES[n]["start"]
    nf = round(DUR * 30) if ult else SCENES[n]["f"]
    dz = None if (ult or SCENES[n]["corte"]) else DISS[nf]
    end = nxt if dz is None else round((dz[1] + 1) / 30 - 0.0002, 5)
    els = "\n      ".join(e for e in sc["els"] if e)
    manchas = ""
    if sc["blobs"]:
        manchas = (f'<div class="inner" id="{sid}bc"><div class="pos" style="left:664px;top:44px;transform:translate(-50%,-50%);z-index:1"><div class="msb" id="{sid}da"><div class="blob" id="{sid}ba">{BLOB.format(s=570)}</div></div></div>'
                   f'<div class="pos" style="left:60px;top:1236px;transform:translate(-50%,-50%);z-index:1"><div class="msb" id="{sid}db"><div class="blob" id="{sid}bb">{BLOB.format(s=570)}</div></div></div></div>\n    ')
        dur = end - sc["start"]
        q0 = sc["blobs"] if not isinstance(sc["blobs"], bool) else 0; q1 = q0 + dur * 30; kk = 1
        (a_0, b_0, s_0), (a_1, b_1, s_1) = mancha(q0), mancha(q1)
        for suf, a0, p0, p1, base in (("a", 0, a_0, a_1, (664, 44)), ("b", 140, b_0, b_1, (60, 1236))):
            anims.append({"k": "rot", "id": sid + "b" + suf, "t": sc["start"], "d": dur, "a0": a0 + 34 * sc["start"], "a1": a0 + 34 * end})
            anims.append({"k": "vai", "id": sid + "d" + suf, "t": sc["start"], "d": dur, "de": [round(p0[0] - base[0], 1), round(p0[1] - base[1], 1), round(kk * s_0 / 570, 4)],
                          "para": [round(p1[0] - base[0], 1), round(p1[1] - base[1], 1), round(kk * s_1 / 570, 4)]})
    bg = f"background:{sc['bg']};" if sc["bg"] else ""
    body.append(f'''  <div id="{sid}" class="clip scene" data-start="{sc["start"]}" data-duration="{round(end - sc["start"], 5)}" data-track-index="{1 + n % 2}" data-track-kind="graphics" style="z-index:{n};{bg}">
    {manchas}<div class="inner" id="{sid}in">
      {els}
    </div>
  </div>''')
    if sc.get("cam") and not MEDIR:               # deriva linear até (1, 0, 0) + assentamento rápido no começo
        s0, dx0, dy0 = sc["cam"]; Tc = end - sc["start"]; pts = []
        for kq in range(int(Tc * 30) + 2):
            u = kq / 30; lin = max(0.0, 1 - u / Tc); ass = math.exp(-u / 0.16)
            pts.append([round(u, 4), round(1 + (s0 - 1) * (0.62 * lin + 0.38 * ass), 4), round(dx0 * (0.62 * lin + 0.38 * ass), 1), round(dy0 * (0.62 * lin + 0.38 * ass), 1)])
        cams[sid + "in"] = {"t0": sc["start"], "d": round(Tc, 5), "p": pts}
    if dz:
        anims.append({"k": "exit" if dz[2] == "blur" else "exitf", "id": sid + "in", "t": round((dz[0] - 0.5) / 30, 4), "d": round((dz[1] - dz[0] + 1) / 30, 4)})
    anims += sc["anims"]
    info.append({"n": n, "start": sc["start"], "f": sc["f"], "end": round(nxt, 5), "nf": nf, "seco": dz is None, "corte": sc["corte"], "fin": nf - 1 if dz is None else dz[0] - 1})

os.makedirs(os.path.join(AQUI, "medir"), exist_ok=True)
json.dump({"cenas": [{"n": i["n"], "t": i["start"], "f": i["f"]} for i in info], "anims": [{"k": a["k"], "id": a["id"], "t": a.get("t"), "d": a.get("d")} for a in anims if a.get("t") is not None]},
          open(os.path.join(AQUI, "medir", "eventos.json"), "w"), indent=0)
json.dump(sorted(SONS, key=lambda x: x[1]), open(os.path.join(AQUI, "medir", "sons_v2.json"), "w"))
json.dump({"cenas": info, "elementos": ELEMS, "nofit": NOFIT}, open(os.path.join(AQUI, "medir", "elementos.json"), "w"), indent=0)

CSS = open(os.path.join(AQUI, "assets/fonts/fonts.css")).read()
HTML = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(PROJ.get("titulo", "Reel"))}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
{CSS}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:{BG}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:{BG}}}
#stage{{position:absolute;left:0;top:0;width:720px;height:1280px;transform:scale(1.5);transform-origin:0 0}}
.scene{{position:absolute;inset:0;overflow:hidden}}
.inner{{position:absolute;inset:0;transform-origin:50% 50%}}
.pos{{position:absolute;white-space:nowrap}}
.ln{{white-space:nowrap}}
.wd{{display:inline-block;will-change:transform,opacity}}
.sk{{display:inline-block;transform:skewX(-11deg);font-style:normal}}
.im{{position:relative}}
.im img{{display:block}}
.badge{{border-radius:50%;background:radial-gradient(circle at 36% 28%,#757575,#4d4d4d 62%,#3f3f3f);color:#fff;font-family:'Poppins';font-weight:700;display:flex;align-items:center;justify-content:center;box-shadow:7px 9px 14px rgba(0,0,0,.38),inset 0 2px 3px rgba(255,255,255,.18),inset 0 -3px 5px rgba(0,0,0,.22);line-height:1;text-shadow:0 2px 3px rgba(0,0,0,.35)}}
.pill{{background:#595959;color:#fff;font-family:'Poppins';font-weight:500;box-shadow:6px 8px 12px rgba(0,0,0,.36);line-height:1.05;text-align:center;letter-spacing:-.02em}}
.pill.ph{{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-weight:400;letter-spacing:0;background:#5c5c5c}}
.pill i{{font-family:'Sacramento';font-style:normal;font-weight:400;display:block;font-size:1.22em;line-height:.67;margin-bottom:-.02em;transform:skewX(-9deg)}}
.blob{{filter:blur(.6px)}}
.msb{{filter:drop-shadow(3px 4px 3px rgba(0,0,0,.3))}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920" data-fps="30">
<audio id="narracao" class="clip" src="{AUDIO}" data-start="0" data-duration="{DUR}" data-track-index="0" data-volume="1"></audio>
<div id="stage">
{chr(10).join(body)}
</div>
</div>
<script>
const A = {json.dumps(anims)};
const tl = gsap.timeline({{ paused: true }});
const LIDS = {{}};
for (const a of A) {{
  const el = "#" + a.id, d = a.d || 0;
  // palavra/pílula: de uma vez (d = 0) ou subindo de baixo enquanto a opacidade entra
  if (a.k === "in") {{
    if (d < 0.04) tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.001 }}, a.t);
    else tl.fromTo(el, {{ opacity: 0, y: a.y || 0 }}, {{ opacity: 1, y: 0, duration: a.y && !a.e ? d * 1.2 : d, ease: a.e || (a.y ? "power1.out" : "none") }}, a.t);
  }}
  // pergunta "digitada": nasce clara, abaixo e à direita, e sobe em diagonal até a linha
  else if (a.k === "typed") tl.fromTo(el, {{ opacity: 0, x: 14, y: a.y || 45, color: "#d2d2d2" }}, {{ opacity: 1, x: 0, y: 0, color: a.col, duration: Math.max(d * 1.2, 0.24), ease: "power1.out" }}, a.t);
  else if (a.k === "some" && a.pts) {{
    const P = a.pts, q = document.querySelector(el), st = {{ u: P[0][0] }};
    const yy = (u) => {{ let i = 0; while (i < P.length - 2 && P[i + 1][0] < u) i++; const A_ = P[i], B_ = P[i + 1], f = Math.min(1, Math.max(0, (u - A_[0]) / (B_[0] - A_[0]))); return A_[1] + (B_[1] - A_[1]) * f; }};
    gsap.set(q, {{ y: P[0][1] }});
    tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: Math.max(d, 0.001), ease: a.e || "none" }}, a.t);
    tl.to(st, {{ u: P[P.length - 1][0], duration: P[P.length - 1][0] - P[0][0], ease: "none", onUpdate: () => gsap.set(q, {{ y: yy(st.u) }}) }}, P[0][0]);
  }}
  else if (a.k === "some") tl.fromTo(el, {{ opacity: 0, y: a.y || 0 }}, {{ opacity: 1, y: 0, duration: Math.max(d, 0.001), ease: a.e || "none" }}, a.t);
  else if (a.k === "selo") {{
    tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: d || 0.5, ease: "power2.out" }}, a.t);
    tl.fromTo(el, {{ y: a.y || 0, x: a.x || 0 }}, {{ y: 0, x: 0, duration: 28 / 30, ease: "expo.out" }}, a.t);
  }}
  else if (a.k === "out") tl.to(el, {{ opacity: 0, duration: 0.001 }}, a.t);
  else if (a.k === "outf") tl.to(el, {{ opacity: 0, duration: d, ease: "none" }}, a.t);
  else if (a.k === "exit") {{
    // lido na referência: o desfoque (leve) fecha em ~1,5 quadro e a cena some por opacidade linear logo depois
    tl.fromTo(el, {{ filter: "blur(0px)" }}, {{ filter: "blur(3px)", duration: 1.5 / 30, ease: "none" }}, a.t - 1 / 30);
    tl.to(el, {{ opacity: 0, duration: d, ease: "none" }}, a.t + 0.5 / 30);
  }}
  else if (a.k === "exitf") tl.to(el, {{ opacity: 0, duration: d, ease: "none" }}, a.t);
  else if (a.k === "gray") tl.fromTo(el, {{ filter: "grayscale(0)" }}, {{ filter: "grayscale(1)", duration: d || 0.43, ease: "none" }}, a.t);
  else if (a.k === "vai") tl.fromTo(el, {{ x: a.de[0], y: a.de[1], scale: a.de[2] }}, {{ x: a.para[0], y: a.para[1], scale: a.para[2], duration: a.d, ease: "none" }}, a.t);
  else if (a.k === "rot") tl.fromTo(el, {{ rotation: a.a0 }}, {{ rotation: a.a1, duration: a.d, ease: "none" }}, a.t);
  else if (a.k === "attr") tl.fromTo(el, {{ attr: a.de }}, {{ attr: a.para, duration: a.d, ease: a.e || "none" }}, a.t);
  else if (a.k === "ft") tl.fromTo(el, a.de, Object.assign({{ duration: a.d, ease: a.e || "power2.out" }}, a.para), a.t);
  else if (a.k === "lid") {{
    const st = {{ o: a.a }}, ids = [a.id + "cp", a.id + "f", a.id + "b"].map((i) => document.getElementById(i));
    const poe = () => {{ const dd = `M4 65 Q150 ${{(168 - st.o * 206).toFixed(1)}} 296 65 Q150 168 4 65Z`; ids.forEach((n) => n.setAttribute("d", dd)); }};
    if (!LIDS[a.id]) {{ LIDS[a.id] = 1; poe(); }}
    tl.fromTo(st, {{ o: a.a }}, {{ o: a.b, duration: a.d, ease: a.e || "power1.inOut", onUpdate: poe, immediateRender: false }}, a.t);
  }}
  else if (a.k === "move") tl.to(el, {{ x: a.x || 0, y: a.y || 0, duration: a.d || 0.4, ease: "power2.inOut" }}, a.t);
}}
// câmera: caminho medido na referência (escala + deslocamento), reproduzido ponto a ponto
const CAMS = {json.dumps(cams)};
for (const [id, c] of Object.entries(CAMS)) {{
  const el = document.getElementById(id), P = c.p, st = {{ u: 0 }};
  const pose = (u) => {{
    let i = 0; while (i < P.length - 2 && P[i + 1][0] < u) i++;
    const a = P[i], b = P[i + 1] || a, f = b[0] > a[0] ? Math.min(1, Math.max(0, (u - a[0]) / (b[0] - a[0]))) : 0;
    gsap.set(el, {{ scale: a[1] + (b[1] - a[1]) * f, x: a[2] + (b[2] - a[2]) * f, y: a[3] + (b[3] - a[3]) * f }});
  }};
  pose(0);
  tl.to(st, {{ u: c.d, duration: c.d, ease: "none", onUpdate: () => pose(st.u) }}, c.t0);
}}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
open(os.path.join(AQUI, "index.html"), "w").write(HTML)
print(f"{len(SCENES)} cenas, {len(anims)} animações, {sum(1 for s in SCENES for e in s['els'] if e)} elementos")
