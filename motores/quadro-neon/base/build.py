#!/usr/bin/env python3
"""MOTOR ESTILO C ("o quadro-negro neon que explica") · gera index.html (HyperFrames + GSAP) a partir de cenas.py.

Independente dos motores A e B. Manual: MOTOR.md do motor quadro-neon, na skill.
PALCO 576x1024 = o tamanho do reel de referência (todas as medidas da perícia valem 1:1), escalado 1,875x para 1080x1920.
Tempos em segundos absolutos; P(i) = início da i-ésima palavra falada (medir/alinhamento.json).
Sem câmera: os elementos entram e FICAM (65 % do tempo a tela está parada, medido).

Primitivas (cenas.py):
  secao(t, entrada="corte"|"flash", fundo="grade"|"grade_larga", estrelas=True, nome="")
  display(txt, x, y, size, cor, t, ent, ...)     herói na display condensada (Anton estreitada) com brilho neon
  corpo(txt, x, y, size, cor, t, ent, ...)        Montserrat
  legenda([(palavra, t), ...], y, ...)            UMA palavra por vez, na palavra falada
  itens([(texto, t), ...], y, ...)                item amarelo que troca no lugar (lista do payoff)
  digita(txt, t0, x, y, w, cps, ...)              digitação centralizada, sem cursor (linha 1 do cartão)
  icone([nomes], x, y, tam, t, ...)               ícone de linha neon (Lucide, ISC) em assets/icones/
  manuscrito(txt, x, y, t)                        "<palavra>" em Gochi Hand, colchetes amarelos
  seta(path_d, t, d)                              traço branco à mão com ponta de seta
  arco(p0, p1, curva, t, d)                       arco tracejado que se desenha (causa -> efeito)
  img(src, x, y, w, t, ent, ...)                  foto recortada (PNG com alfa) ou print
  cartao(...)                                     o molde do cartão de marca (5x na referência)
  tarja(txt, x, y, w, h, t)                       adesivo amarelo do título-síntese
  prompt(txt, x, y, t)                            ">texto" com o ">" amarelo
  anim(id, t, de, para, d, ease)                  animação livre
  SOM(tipo, t, db) · MUSICA(evento, t)            efeitos e arranjo da trilha (lidos pelo mix.py)
"""
import json, html, os, random

AQUI = os.path.dirname(os.path.abspath(__file__))
PROJ = json.load(open(os.path.join(AQUI, "projeto.json")))
ONS = json.load(open(os.path.join(AQUI, "medir", "alinhamento.json")))
DUR = PROJ.get("duracao") or round(ONS[-1]["end"] + 0.5, 2)
FPS = 30
W, H, ESC = 576, 1024, 1.875
AUDIO = PROJ.get("audio") or ("assets/mix.m4a" if os.path.exists(os.path.join(AQUI, "assets", "mix.m4a")) else "assets/narracao.wav")

# ---- identidade medida na referência (pericia/DESMONTE-C.md §6-§7)
AMARELO = "#F9DB11"
BRANCO = "#FFFFFF"
NEON = {  # brilho externo (text-shadow) medido: miolo saturado + halo largo
    "amarelo": f"color:{AMARELO};text-shadow:0 0 3px rgba(255,226,60,.95),0 0 12px rgba(255,205,0,.75),0 0 30px rgba(255,190,0,.5),0 0 60px rgba(255,180,0,.25);",
    "branco": "color:#fff;text-shadow:0 0 4px rgba(255,255,255,.55),0 0 14px rgba(255,255,255,.28);",
    "branco_amarelo": "color:#fff;text-shadow:0 0 4px rgba(255,245,200,.95),0 0 14px rgba(255,214,40,.8),0 0 32px rgba(255,195,0,.55),0 0 64px rgba(255,180,0,.3);",
    "amarelo_suave": f"color:{AMARELO};text-shadow:0 0 6px rgba(255,210,0,.45);",
    "nenhum": "",
}
ESTREITA = {"gancho": 0.64, "ponte": 0.72, "heroi": 0.77, "marca": 0.82, "tarja": 0.66}   # scaleX medido por papel
ATRASO = 0.0      # a legenda entra NA palavra (medido ±1 quadro)

SECOES, ANIMS, SONS, MUSICA_EV = [], [], [], []
_n = [0]


def P(i, antes=0.0):
    """Início da i-ésima palavra falada (menos `antes`)."""
    return round(max(0.0, ONS[i]["start"] - antes), 3)


def F(i):
    return round(ONS[i]["end"], 3)


def _id(p="e"):
    _n[0] += 1
    return f"{p}{_n[0]}"


def SOM(tipo, t, ganho_db=0.0):
    SONS.append({"tipo": tipo, "t": round(float(t), 3), "db": ganho_db})


def MUSICA(evento, t):
    """Arranjo da trilha (mix.py): 'baixo_sai' (o grave some = tensão), 'drop' (bumbo + grave entram; riser antes),
    'break' (bumbo e grave somem), 'volta' (bumbo volta). Medido: drop no 1º exemplo, break no título-síntese."""
    MUSICA_EV.append({"ev": evento, "t": round(float(t), 3)})


# ---------------------------------------------------------------- seções
def secao(t, entrada="corte", fundo="grade", estrelas=True, nome="", seed=None, anda=0.0):
    """anda = px/s que a malha do fundo rola para BAIXO (medido: 27 px/s na tese e no reframe; parada no resto)."""
    s = {"id": _id("s"), "t": round(float(t), 3), "entrada": entrada, "fundo": fundo, "estrelas": estrelas,
         "nome": nome, "els": [], "seed": seed if seed is not None else len(SECOES) + 3, "anda": anda}
    SECOES.append(s)
    return s


def _el(htm):
    SECOES[-1]["els"].append(htm)


def _entra(eid, t, ent, d=None, de=None):
    if t is None:
        return
    ANIMS.append({"k": "in", "id": eid, "t": round(float(t), 3), "ent": ent, "d": d, "de": de})


def _sai(eid, sai):
    if sai is not None:
        t, tipo, d = (list(sai) + [None, None])[:3] if isinstance(sai, (list, tuple)) else (sai, "seco", None)
        ANIMS.append({"k": "out", "id": eid, "t": round(float(t), 3), "tipo": tipo or "seco", "d": d or 0.12})


def _caixa(x, y, w=None, h=None, z=4, alinh="left", extra=""):
    """x,y = canto superior esquerdo (alinh left), centro horizontal (center) ou borda direita (right)."""
    s = f"top:{y}px;z-index:{z};"
    if alinh == "center":
        s += f"left:{x}px;transform:translateX(-50%);" if w is None else f"left:{x - w / 2}px;width:{w}px;"
    elif alinh == "right":
        s += f"right:{W - x}px;"
    else:
        s += f"left:{x}px;"
    if w is not None and alinh != "center": s += f"width:{w}px;"
    if h is not None: s += f"height:{h}px;"
    return s + f"text-align:{alinh};" + extra


# ---------------------------------------------------------------- tipografia
def display(txt, x, y, size=90, cor="amarelo", t=None, ent="cresce", papel="heroi", alinh="center", lh=0.92, z=5,
            sai=None, d=None, de=None, w=None, ls=0.0, extra=""):
    """Herói na display condensada. `papel` escolhe a estreiteza medida (ESTREITA). Quebra de linha com '\\n'."""
    eid = _id("dp")
    sx = ESTREITA.get(papel, papel if isinstance(papel, float) else 0.77)
    if ent == "tracking":      # letras separadas que deslizam (letterSpacing anima em pixels inteiros e "pula")
        linhas = "<br>".join("".join(f'<span class="lt">{html.escape(c) if c != " " else "&nbsp;"}</span>' for c in l) for l in txt.split("\n"))
    else:
        linhas = "<br>".join(html.escape(l) for l in txt.split("\n"))
    origem = {"center": "50%", "left": "0%", "right": "100%"}[alinh]
    st = _caixa(x, y, w, None, z, alinh, f"font-family:'Anton';font-size:{size}px;line-height:{lh};letter-spacing:{ls}em;white-space:nowrap;{NEON[cor]}{extra}")
    _el(f'<div id="{eid}" class="ab tx" style="{st}"><div class="sx" style="transform:scaleX({sx});transform-origin:{origem} 50%">{linhas}</div></div>')
    _entra(eid, t, ent, d, de); _sai(eid, sai)
    return eid


def corpo(txt, x, y, size=36, cor="branco", peso=500, t=None, ent="fade", alinh="center", lh=1.15, z=5, sai=None,
          d=None, de=None, w=None, caixa=False, extra=""):
    eid = _id("cp")
    st = _caixa(x, y, w, None, z, alinh, f"font-family:'Montserrat';font-weight:{peso};font-size:{size}px;line-height:{lh};"
               f"white-space:{'normal' if w else 'nowrap'};{'text-transform:uppercase;' if caixa else ''}{NEON.get(cor, 'color:' + cor + ';')}{extra}")
    _el(f'<div id="{eid}" class="ab tx" style="{st}">{txt}</div>')
    _entra(eid, t, ent, d, de); _sai(eid, sai)
    return eid


def legenda(palavras, y, x=W / 2, size=30, peso=600, cor="branco", caixa=False, fim=None, ent="flick", z=6):
    """UMA palavra por vez (medido: troca no lugar, na palavra falada, ±1 quadro). palavras = [(txt, t)].
    Cada palavra fica até a próxima; a última fica até `fim` (ou o fim da seção)."""
    ids = []
    for k, (p, t) in enumerate(palavras):
        nxt = palavras[k + 1][1] if k + 1 < len(palavras) else fim
        # palavra curta (ex.: "o" com 0,05 s na voz crua): a entrada nunca pode passar da saída, senão a palavra "religa"
        dd = None if nxt is None else max(0.01, min(0.07, nxt - (t + ATRASO) - 0.012))
        ids.append(corpo(html.escape(p), x, y, size=size, cor=cor, peso=peso, t=t + ATRASO, ent=ent, alinh="center", z=z,
                         caixa=caixa, sai=(nxt, "seco") if nxt else None, d=dd))
    return ids


def itens(lista, y, x=W / 2, size=34, peso=500, cor="amarelo_suave", fim=None, ent="sobe"):
    """Item que troca no lugar (lista do payoff): entra subindo e acendendo; some quando o próximo entra."""
    return [corpo(html.escape(p), x, y, size=size, cor=cor, peso=peso, t=t, ent=ent, alinh="center",
                  sai=((lista[k + 1][1] - 0.02, "seco") if k + 1 < len(lista) else ((fim, "seco") if fim else None)))
            for k, (p, t) in enumerate(lista)]


def digita(txt, t0, x, y, w=520, cps=19.0, t1=None, size=36, peso=500, cor="branco", lh=1.12, z=5, sai=None, caixa=True, ritmo=None):
    """Digitação letra a letra, sem cursor, com o LAYOUT FINAL RESERVADO (medido: as letras surgem já no lugar da frase
    pronta, centralizada; a 2ª linha não "dança"). Ritmo: linear de t0 a t1 (ou cps), ou ritmo=[(t_ini, t_fim) por
    palavra] = a palavra k é digitada enquanto a voz a diz (medido: o texto acompanha a fala palavra a palavra)."""
    eid = _id("dg")
    st = _caixa(x, y, w, None, z, "center", f"font-family:'Montserrat';font-weight:{peso};font-size:{size}px;line-height:{lh};"
               f"white-space:normal;{'text-transform:uppercase;' if caixa else ''}{NEON[cor]}")
    pal = txt.split(" ")
    if ritmo and len(ritmo) == len(pal):
        marcas = []
        for p, (a, b) in zip(pal, ritmo):
            n = len(p); dd = max(0.05, b - a)
            marcas += [round(a + dd * k / max(1, n), 3) for k in range(n)] + [round(b, 3)]
        marcas = marcas[:-1]
    else:
        dur = (t1 - t0) if t1 else len(txt) / cps
        marcas = [round(t0 + dur * k / max(1, len(txt) - 1), 3) for k in range(len(txt))]
    spans, k = [], 0
    for j, p in enumerate(pal):
        letras = "".join(f'<span class="ch" data-t="{marcas[k + i]}">{html.escape(c)}</span>' for i, c in enumerate(p))
        k += len(p)
        spans.append(f'<span style="white-space:nowrap">{letras}</span>')
        if j < len(pal) - 1:
            spans.append(f'<span class="ch" data-t="{marcas[k] if k < len(marcas) else marcas[-1]}"> </span>'); k += 1
    _el(f'<div id="{eid}" class="ab tx" style="{st}">{"".join(spans)}</div>')
    ANIMS.append({"k": "digita", "id": eid, "t": marcas[0], "d": round(marcas[-1] - marcas[0], 3)})
    _sai(eid, sai)
    return eid


def manuscrito(txt, x, y, t, size=34, z=6, sai=None):
    """'<palavra>' em fonte manuscrita, colchetes angulares amarelos; entra de cinza desfocado para branco (0,3 s)."""
    eid = _id("ms")
    st = _caixa(x, y, None, None, z, "center", f"font-family:'Gochi Hand';font-size:{size}px;white-space:nowrap;{NEON['branco']}")
    _el(f'<div id="{eid}" class="ab tx" style="{st}"><span style="{NEON["amarelo"]}">&lt;</span>{html.escape(txt)}'
        f'<span style="{NEON["amarelo"]}">&gt;</span></div>')
    _entra(eid, t, "cinza", 0.3); _sai(eid, sai)
    return eid


# ---------------------------------------------------------------- gráficos
_ICONES = {}


def _icone_svg(nome):
    if nome not in _ICONES:
        s = open(os.path.join(AQUI, "assets", "icones", nome + ".svg")).read()
        _ICONES[nome] = s[s.index("<svg"):].split(">", 1)[1].rsplit("</svg>", 1)[0]
    return _ICONES[nome]


def icone(nomes, x, y, tam=140, t=None, ent="cresce", esp=1.5, z=5, sai=None, partes=None):
    """Ícone de linha neon amarelo (Lucide, 24x24). nomes = 'shield-check' ou lista de camadas;
    partes = [(dx, dy, escala)] por camada (fração do tamanho), para compor (ex.: escudo sobre a mão)."""
    eid = _id("ic")
    nomes = [nomes] if isinstance(nomes, str) else nomes
    partes = partes or [(0, 0, 1)] * len(nomes)
    g = "".join(f'<g transform="translate({12 + dx * 24},{12 + dy * 24}) scale({s}) translate(-12,-12)">{_icone_svg(n)}</g>'
                for n, (dx, dy, s) in zip(nomes, partes))
    _el(f'<div id="{eid}" class="ab" style="left:{x - tam / 2}px;top:{y - tam / 2}px;width:{tam}px;height:{tam}px;z-index:{z};'
        f'filter:drop-shadow(0 0 3px rgba(255,220,40,.9)) drop-shadow(0 0 12px rgba(255,200,0,.6)) drop-shadow(0 0 26px rgba(255,190,0,.35))">'
        f'<svg viewBox="0 0 24 24" width="{tam}" height="{tam}" fill="none" stroke="{AMARELO}" stroke-width="{esp}" '
        f'stroke-linecap="round" stroke-linejoin="round" style="overflow:visible">{g}</svg></div>')
    _entra(eid, t, ent); _sai(eid, sai)
    return eid


def seta(d, t, dur=0.55, esp=2.4, z=6, sai=None, cabeca=12):
    """Traço branco à mão (path SVG no palco 576x1024) que se desenha; a ponta de seta acende no fim."""
    eid = _id("st")
    _el(f'<svg id="{eid}" class="ab deco" style="left:0;top:0;z-index:{z};overflow:visible;filter:drop-shadow(0 0 4px rgba(255,255,255,.5))" '
        f'width="{W}" height="{H}"><path class="trc" d="{d}" pathLength="1" fill="none" stroke="#fff" stroke-width="{esp}" '
        f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>'
        f'<path class="pta" d="M0 0" fill="#fff"/></svg>')
    ANIMS.append({"k": "seta", "id": eid, "t": round(float(t), 3), "d": dur, "cab": cabeca})
    _sai(eid, sai)
    return eid


def arco(p0, p1, curva=0.35, t=0, dur=0.6, esp=2.0, z=4, sai=None, traco="5 6"):
    """Arco tracejado branco com brilho de p0 a p1 (curva = desvio lateral como fração da distância, + = para a direita)."""
    eid = _id("ar")
    (a, b), (c, e) = p0, p1
    mx, my = (a + c) / 2, (b + e) / 2; dx, dy = c - a, e - b
    qx, qy = mx - dy * curva * -1, my + dx * curva * -1
    dd = f"M{a} {b} Q{qx:.1f} {qy:.1f} {c} {e}"
    _el(f'<svg id="{eid}" class="ab deco" style="left:0;top:0;z-index:{z};overflow:visible;filter:drop-shadow(0 0 3px rgba(255,255,255,.7))" '
        f'width="{W}" height="{H}"><defs><mask id="{eid}m"><path class="trc" d="{dd}" pathLength="1" fill="none" stroke="#fff" '
        f'stroke-width="{esp + 6}" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/></mask></defs>'
        f'<path d="{dd}" mask="url(#{eid}m)" fill="none" stroke="#fff" stroke-width="{esp}" stroke-dasharray="{traco}" stroke-linecap="round"/></svg>')
    ANIMS.append({"k": "arco", "id": eid, "t": round(float(t), 3), "d": dur})
    _sai(eid, sai)
    return eid


def img(src, x, y, w, h=None, t=None, ent="pop", d=None, de=None, z=4, sai=None, rot=0, filtro="", sombra=True, raio=0, extra=""):
    """Imagem posicionada pelo canto superior esquerdo. Recorte (PNG com alfa) com sombra; print com raio de canto."""
    eid = _id("im")
    f = ([filtro] if filtro else []) + (["drop-shadow(0 10px 18px rgba(0,0,0,.6))"] if sombra else [])
    hh = f"height:{h}px;object-fit:cover;" if h else ""
    _el(f'<div id="{eid}" class="ab" style="left:{x}px;top:{y}px;width:{w}px;z-index:{z};{"transform:rotate(%sdeg);" % rot if rot else ""}'
        f'{"filter:" + " ".join(f) + ";" if f else ""}{extra}"><img src="{src}" style="width:{w}px;{hh}display:block;border-radius:{raio}px"></div>')
    _entra(eid, t, ent, d, de); _sai(eid, sai)
    return eid


def tarja(txt, x, y, w=420, h=89, t=0, size=74, z=6, sai=None):
    """Adesivo amarelo (título-síntese): caixa amarela com brilho e texto display branco com contorno escuro; entra encolhendo."""
    eid = _id("tj")
    _el(f'<div id="{eid}" class="ab" style="left:{x - w / 2}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};background:{AMARELO};'
        f'box-shadow:0 0 10px rgba(255,214,0,.85),0 0 30px rgba(255,200,0,.5);display:flex;align-items:center;justify-content:center;overflow:hidden">'
        f'<div class="sx" style="font-family:\'Anton\';font-size:{size}px;line-height:1;color:#fff;white-space:nowrap;transform:scaleX({ESTREITA["tarja"]});'
        f'-webkit-text-stroke:1.2px rgba(120,90,0,.55);text-shadow:0 0 6px rgba(255,255,255,.6)">{html.escape(txt)}</div></div>')
    _entra(eid, t, "encolhe", 0.35); _sai(eid, sai)
    return eid


def prompt(txt, x, y, t, size=60, z=6, sai=None, ent="fade"):
    """'>texto' em Montserrat Regular branco, com o '>' amarelo (cara de prompt de terminal)."""
    eid = _id("pr")
    st = _caixa(x, y, None, None, z, "center", f"font-family:'Montserrat';font-weight:400;font-size:{size}px;white-space:nowrap;{NEON['branco']}")
    _el(f'<div id="{eid}" class="ab tx" style="{st}"><span style="{NEON["amarelo"]}">&gt;</span>{html.escape(txt)}</div>')
    _entra(eid, t, ent, 0.3); _sai(eid, sai)
    return eid


def cartao(t, logo, nome, print_, linha1, t_digita, payoff_pre, payoff, t_payoff, fim=None, logo_fundo="#fff",
           print_y=302, print_h=None, cps=19.0, logo_pad=8, t_fim_digita=None, w_linha=430, ritmo=None, size_l2=36,
           size_l1=36, nome_size=56, logo_desfoque=0, print_desfoque=0):
    """O MOLDE DO CARTÃO DE MARCA (medido 5x na referência, idêntico em todos):
      cabeçalho: círculo com o logo oficial (x 52-180, centro y 148) + nome na display (x 249, y 131) + régua y 227
      print real do site: x 40-536, sobe de baixo com borrão (0,5 s)
      linha 1 digitada (caixa alta, Montserrat 500 ~36 px, 2 linhas), y 615
      linha 2 'THEY SELL' + PAYOFF amarelo, entra inteira (cinza -> branco) na palavra-payoff, y 730
    Coreografia: logo cresce/acende e nome entra da direita no corte (0,2 s); print sobe em t+0,03; digitação em t_digita."""
    ids = {}
    ids["logo"] = _id("lg")
    _el(f'<div id="{ids["logo"]}" class="ab" style="left:52px;top:84px;width:128px;height:128px;z-index:5;border-radius:50%;'
        f'background:{logo_fundo};overflow:hidden;display:flex;align-items:center;justify-content:center;box-shadow:0 0 18px rgba(255,255,255,.18)">'
        f'<img src="{logo}" style="width:{128 - 2 * logo_pad}px;height:{128 - 2 * logo_pad}px;object-fit:contain;'
        f'{f"filter:blur({logo_desfoque}px);transform:scale(1.15);" if logo_desfoque else ""}"></div>')
    _entra(ids["logo"], t, "logo", 0.22)
    ids["nome"] = display(nome.upper(), 249, 128 + (56 - nome_size) * 0.55, size=nome_size, cor="branco", t=t, ent="direita", papel="marca", alinh="left", d=0.22)
    ids["regua"] = _id("rg")
    _el(f'<div id="{ids["regua"]}" class="ab" style="left:27px;top:226px;width:522px;height:2px;z-index:5;background:#fff;'
        f'box-shadow:0 0 6px rgba(255,255,255,.5);transform-origin:0 50%"></div>')
    _entra(ids["regua"], t, "regua", 0.25)
    ph = f"height:{print_h}px;object-fit:cover;object-position:top;" if print_h else ""
    ids["print"] = _id("pt")
    _el(f'<div id="{ids["print"]}" class="ab" style="left:40px;top:{print_y}px;width:496px;z-index:4;border-radius:7px;overflow:hidden;'
        f'box-shadow:0 0 0 1.5px rgba(255,255,255,.85),0 10px 30px rgba(0,0,0,.6)"><img src="{print_}" style="width:496px;{ph}display:block;'
        f'{f"filter:blur({print_desfoque}px);transform:scale(1.04);" if print_desfoque else ""}"></div>')
    _entra(ids["print"], t + 0.03, "sobe_borrao", 0.55)
    ids["l1"] = digita(linha1, t_digita, W / 2, 615, w=w_linha, cps=cps, t1=t_fim_digita, size=size_l1, ritmo=ritmo)
    ids["l2"] = corpo(f'{html.escape(payoff_pre)} <span style="{NEON["amarelo"]}">{html.escape(payoff)}</span>', W / 2, 730 + (36 - size_l2) * 0.5, size=size_l2,
                      peso=500, cor="branco", t=t_payoff, ent="cinza", d=0.22, caixa=True)
    if fim is not None:        # medido: a linha 1 some 1 quadro antes do resto
        _sai(ids["l1"], (fim - 1 / 30, "seco"))
    return ids


def anim(eid, t, de, para, d=0.3, ease="power2.out"):
    ANIMS.append({"k": "ft", "id": eid, "t": round(float(t), 3), "de": de, "para": para, "d": d, "e": ease})


# ---------------------------------------------------------------- fundo
def _fundo(s):
    """Fundo medido: preto #020202 + malha fina de 30,5 px (linhas #151515) + estrelas de 4 pontas nos cruzamentos a cada
    2 células (61 px), algumas acesas; 'grade_larga' (seção-síntese) = malha de 67 px mais clara, sem estrelas. Vinheta."""
    if s["fundo"] == "grade_larga":
        cel, cor, alf = 67, "#3a3a3a", 1
    else:
        cel, cor, alf = 30.5, "#1e1e1e", 1
    off = (W / 2) % cel
    g = (f"background-color:{'#080808' if s['fundo'] == 'grade_larga' else '#020202'};background-image:linear-gradient({cor} 1px,transparent 1px),linear-gradient(90deg,{cor} 1px,transparent 1px);"
         f"background-size:{cel}px {cel}px;background-position:{off}px {(H / 2) % cel}px;")
    out = [f'<div class="ab deco malha" id="{s["id"]}m" style="left:0;top:-420px;width:{W}px;height:{H + 420}px">'
           f'<div class="ab deco" style="inset:0;{g.replace(f"{(H / 2) % cel}px;", f"{(H / 2 + 420) % cel}px;")}"></div>']
    if s["estrelas"] and s["fundo"] != "grade_larga":
        rnd = random.Random(s["seed"]); est = []
        passo = cel * 2
        for gx in range(0, int(W / passo) + 2):
            for gy in range(0, int((H + 420) / passo) + 2):
                if rnd.random() < (0.24 if s.get("anda") else 0.55):
                    x = off + gx * passo; y = (H / 2) % cel + gy * passo
                    tam = rnd.choice([5, 7, 9]) if s.get("anda") else rnd.choice([8, 10, 12]); op = rnd.uniform(.3, .85); fase = rnd.uniform(0, 6.28)
                    est.append(f'<i class="est" data-f="{fase:.2f}" data-o="{op:.2f}" data-w="{rnd.uniform(5.0, 11.0) if not s.get("anda") else 1.7:.2f}" data-k="{0 if s.get("anda") else 1}" style="left:{x - tam / 2:.1f}px;top:{y - tam / 2 + 420:.1f}px;width:{tam}px;height:{tam}px;opacity:{op:.2f}"></i>')
                    if y + 420 > H: est.append(est[-1].replace(f"top:{y - tam / 2 + 420:.1f}px", f"top:{y - tam / 2:.1f}px"))
        out.append("".join(est))
    out.append("</div>")
    out.append('<div class="ab deco" style="inset:0;background:radial-gradient(ellipse 75% 60% at 50% 48%,rgba(0,0,0,0) 35%,rgba(0,0,0,.72) 100%)"></div>')
    return "".join(out)


# ---------------------------------------------------------------- montagem do HTML
def montar():
    SECOES.sort(key=lambda s: s["t"])
    body, flashes = [], []
    for k, s in enumerate(SECOES):
        fim = SECOES[k + 1]["t"] if k + 1 < len(SECOES) else DUR
        if s.get("anda"):
            px = s["anda"] * (fim - s["t"]); cel = 67 if s["fundo"] == "grade_larga" else 30.5
            if px > 400: px = px % (2 * cel) + 2 * cel * int(380 / (2 * cel))      # a malha é periódica: nunca passa do invólucro
            ANIMS.append({"k": "rola", "id": s["id"] + "m", "t": s["t"], "d": round(fim - s["t"], 3), "px": round(px, 1)})
        if s["entrada"] == "flash" and k > 0:
            flashes.append(s["t"])
        body.append(f'<div id="{s["id"]}" class="clip secao" data-start="{s["t"]}" data-duration="{round(fim - s["t"], 4)}" '
                    f'data-track-index="{1 + k % 2}" style="z-index:{k + 1}">{_fundo(s)}' + "\n".join(s["els"]) + "</div>")
    # luz de filme EM VÍDEO (assets/luz.mp4, gerado no Higgsfield): um trecho de ~0,4 s centrado no estouro de branco,
    # em "screen" por cima de tudo; sem o vídeo, cai no vazamento desenhado em CSS (reserva).
    LUZ = PROJ.get("luz") or (json.load(open(os.path.join(AQUI, "assets", "luz.json"))) if os.path.exists(os.path.join(AQUI, "assets", "luz.json")) else None)
    luzes = []
    if LUZ and os.path.exists(os.path.join(AQUI, LUZ["arquivo"])):
        for k, t in enumerate(flashes):
            a = round(t - LUZ["antes"], 3); ms = round(LUZ["pico"] - LUZ["antes"], 3)
            luzes.append(f'<video id="lz{k}" src="{LUZ["arquivo"]}" muted playsinline data-start="{a}" data-duration="{LUZ["dur"]}" '
                         f'data-media-start="{ms}" data-track-index="{5 + k % 2}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;'
                         f'object-fit:cover;mix-blend-mode:screen;filter:brightness(1.35) contrast(1.08);z-index:902;pointer-events:none"></video>')
        flashes_css = []
    else:
        flashes_css = flashes
    LUZ_HTML = "".join(luzes)
    fonts = """
@font-face{font-family:'Anton';src:url('assets/fonts/anton-latin-400-normal.woff2') format('woff2')}
@font-face{font-family:'Anton';src:url('assets/fonts/anton-latin-ext-400-normal.woff2') format('woff2');unicode-range:U+0100-024F,U+1E00-1EFF}
@font-face{font-family:'Montserrat';src:url('assets/fonts/montserrat-latin-wght-normal.woff2') format('woff2');font-weight:100 900}
@font-face{font-family:'Montserrat';src:url('assets/fonts/montserrat-latin-ext-wght-normal.woff2') format('woff2');font-weight:100 900;unicode-range:U+0100-024F,U+1E00-1EFF}
@font-face{font-family:'Gochi Hand';src:url('assets/fonts/gochi-hand-latin-400-normal.woff2') format('woff2')}"""
    H_ = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{html.escape(PROJ.get("titulo", "Reel estilo C"))}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{fonts}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#020202}}
#stage{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform:scale({ESC});transform-origin:0 0;overflow:hidden;background:#020202}}
.secao{{position:absolute;inset:0;overflow:hidden;background:#020202}}
.ab{{position:absolute}}
.deco,.est,#vaz{{pointer-events:none}}
.tx{{white-space:nowrap}}
.est{{position:absolute;background:#e6e6e6;clip-path:polygon(50% 0,60% 40%,100% 50%,60% 60%,50% 100%,40% 60%,0 50%,40% 40%);transform:rotate(12deg)}}
.lt{{display:inline-block}}
#vaz{{position:absolute;inset:0;z-index:900;opacity:0;mix-blend-mode:screen;overflow:hidden}}
#vaz .v1{{position:absolute;left:-40%;top:-10%;width:180%;height:120%;filter:blur(14px);
  background:linear-gradient(90deg,rgba(60,25,0,0) 0%,rgba(150,80,20,.75) 12%,rgba(255,200,130,.95) 24%,rgba(255,246,228,1) 36%,rgba(255,252,244,1) 52%,
  rgba(255,236,200,1) 62%,rgba(240,170,90,.85) 76%,rgba(110,55,10,.6) 88%,rgba(40,15,0,0) 100%)}}
#vaz .v2{{position:absolute;left:-60%;top:-30%;width:220%;height:160%;opacity:0;filter:blur(16px);
  background:linear-gradient(150deg,rgba(0,0,0,0) 22%,rgba(255,70,50,.7) 27%,rgba(255,170,40,.8) 30%,rgba(255,240,90,.75) 33%,
  rgba(110,255,130,.65) 36%,rgba(60,190,255,.6) 39%,rgba(150,90,255,.5) 42%,rgba(0,0,0,0) 47%),
  radial-gradient(ellipse 60% 40% at 30% 95%,rgba(200,110,30,.7),rgba(0,0,0,0) 70%)}}
#branco{{position:absolute;inset:0;z-index:901;background:#fff8ec;opacity:0;pointer-events:none}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920" data-fps="30">
<audio id="audio" class="clip" src="{AUDIO}" data-start="0" data-duration="{DUR}" data-track-index="0" data-volume="1"></audio>
<div id="stage">
{chr(10).join(body)}
{LUZ_HTML}<div id="vaz"><div class="v1"></div><div class="v2"></div></div><div id="branco"></div>
</div>
</div>
<script>
const A = {json.dumps(ANIMS)};
const FL = {json.dumps(flashes_css)};
const tl = gsap.timeline({{ paused: true }});
const $ = (i) => document.getElementById(i);
for (const a of A) {{
  const el = $(a.id); if (!el) continue;
  const d = a.d || 0;
  if (a.k === "in") {{
    const D = d || ({{seco: 0, flick: 0.07, pop_leve: 0.12, sobe_forte: 0.3, fade: 0.25, cresce: 0.4, sobe: 0.22, pop: 0.22, esquerda: 0.16, direita: 0.22, baixo: 0.3, tracking: 0.32,
                     sobe_borrao: 0.5, cinza: 0.22, logo: 0.22, regua: 0.25, encolhe: 0.35}})[a.ent] || 0;
    gsap.set(el, {{ opacity: 0 }}); tl.set(el, {{ opacity: 0 }}, 0);
    const T = (de, pa) => tl.fromTo(el, de, Object.assign({{ duration: D, immediateRender: false }}, pa), a.t);
    if (a.ent === "seco" || !D) tl.set(el, {{ opacity: 1 }}, a.t);
    else if (a.ent === "flick") T({{ opacity: .55, filter: "blur(3px)" }}, {{ opacity: 1, filter: "blur(0px)", ease: "none" }});
    else if (a.ent === "pop_leve") T({{ opacity: 0, scale: 1.18 }}, {{ opacity: 1, scale: 1, ease: "power2.out" }});
    else if (a.ent === "sobe_forte") {{
      tl.fromTo(el, {{ opacity: 0, y: (a.de || 70), filter: "blur(8px) brightness(.55)" }}, {{ opacity: 1, y: 0, filter: "blur(0px) brightness(.8)", duration: D, ease: "power3.out", immediateRender: false }}, a.t);
      tl.to(el, {{ filter: "blur(0px) brightness(1.25)", duration: .22, ease: "power1.out" }}, a.t + D);
      tl.to(el, {{ filter: "blur(0px) brightness(1)", duration: .3, ease: "power1.inOut" }}, a.t + D + .22); }}
    else if (a.ent === "fade") T({{ opacity: 0 }}, {{ opacity: 1, ease: "none" }});
    else if (a.ent === "cresce") T({{ opacity: 0, scale: .55, y: (a.de === null ? -55 : a.de), filter: "brightness(.35) blur(2px)" }}, {{ opacity: 1, scale: 1, y: 0, filter: "brightness(1) blur(0px)", ease: "power2.out" }});
    else if (a.ent === "sobe") T({{ opacity: 0, y: 18, filter: "blur(5px) grayscale(1) brightness(.6)" }}, {{ opacity: 1, y: 0, filter: "blur(0px) grayscale(0) brightness(1)", ease: "power2.out" }});
    else if (a.ent === "pop") T({{ opacity: 0, scale: 1.32 }}, {{ opacity: 1, scale: 1, ease: "power2.out" }});
    else if (a.ent === "esquerda") T({{ opacity: 1, x: -(a.de || 340) }}, {{ opacity: 1, x: 0, ease: "power2.out" }});
    else if (a.ent === "direita") T({{ opacity: 0, x: (a.de || 120) }}, {{ opacity: 1, x: 0, ease: "power2.out" }});
    else if (a.ent === "baixo") T({{ opacity: 1, y: (a.de || 260) }}, {{ opacity: 1, y: 0, ease: "power3.out" }});
    else if (a.ent === "cinza") T({{ opacity: .35, filter: "grayscale(1) blur(2px)" }}, {{ opacity: 1, filter: "grayscale(0) blur(0px)", ease: "power1.out" }});
    else if (a.ent === "logo") T({{ opacity: .5, scale: 1.3, filter: "grayscale(1)" }}, {{ opacity: 1, scale: 1, filter: "grayscale(0)", ease: "power2.out" }});
    else if (a.ent === "regua") T({{ opacity: 1, scaleX: 0 }}, {{ opacity: 1, scaleX: 1, ease: "power2.out" }});
    else if (a.ent === "encolhe") T({{ opacity: 0, y: 45 }}, {{ opacity: 1, y: 0, ease: "power2.out" }});
    else if (a.ent === "sobe_borrao") T({{ opacity: 1, y: (a.de || 420), filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", ease: "power3.out" }});
    else if (a.ent === "tracking") {{
      const L = [...el.querySelectorAll(".lt")], fs = parseFloat(getComputedStyle(el).fontSize), n = L.length;
      tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: .04, ease: "none", immediateRender: false }}, a.t);
      L.forEach((c, k) => tl.fromTo(c, {{ x: (k - (n - 1) / 2) * fs * 1.1 }}, {{ x: 0, duration: D, ease: "power2.inOut", immediateRender: false }}, a.t)); }}
  }}
  else if (a.k === "out") {{
    if (a.tipo === "seco") tl.set(el, {{ opacity: 0 }}, a.t);
    else tl.to(el, {{ opacity: 0, duration: d, ease: "none" }}, a.t);
  }}
  else if (a.k === "digita") {{
    for (const c of el.querySelectorAll(".ch")) {{ gsap.set(c, {{ opacity: 0 }}); tl.set(c, {{ opacity: 0 }}, 0); tl.set(c, {{ opacity: 1 }}, +c.dataset.t); }}
  }}
  else if (a.k === "seta") {{
    const p = el.querySelector(".trc"), pt = el.querySelector(".pta"); gsap.set(el, {{ opacity: 0 }}); tl.set(el, {{ opacity: 1 }}, a.t);
    tl.fromTo(p, {{ strokeDashoffset: 1.1 }}, {{ strokeDashoffset: 0, duration: d, ease: "power1.inOut", immediateRender: false }}, a.t);
    const L = p.getTotalLength(), e = p.getPointAtLength(L), b = p.getPointAtLength(Math.max(0, L - 10));
    const ang = Math.atan2(e.y - b.y, e.x - b.x), c = a.cab, w = c * .55;
    const P = (r, s) => [e.x + Math.cos(ang + s) * r, e.y + Math.sin(ang + s) * r];
    const q1 = P(-c, -Math.atan(w / c)), q2 = P(-c, Math.atan(w / c));
    pt.setAttribute("d", `M${{e.x}} ${{e.y}} L${{q1[0]}} ${{q1[1]}} L${{q2[0]}} ${{q2[1]}} Z`);
    gsap.set(pt, {{ opacity: 0 }}); tl.set(pt, {{ opacity: 1 }}, a.t + d * .92);
  }}
  else if (a.k === "arco") {{
    const p = el.querySelector(".trc"); gsap.set(el, {{ opacity: 0 }}); tl.set(el, {{ opacity: 1 }}, a.t);
    tl.fromTo(p, {{ strokeDashoffset: 1.1 }}, {{ strokeDashoffset: 0, duration: d, ease: "power1.inOut", immediateRender: false }}, a.t);
  }}
  else if (a.k === "rola") tl.fromTo(el, {{ y: 0 }}, {{ y: a.px, duration: d, ease: "none", immediateRender: false }}, a.t);
  else if (a.k === "ft") tl.fromTo(el, a.de, Object.assign({{ duration: d, ease: a.e, immediateRender: false }}, a.para), a.t);
}}
// ---- vazamento de luz (medido a 30 fps: 0,23 s; âmbar entra, estoura em creme no corte, recua com arco-íris fraco)
const v1 = document.querySelector("#vaz .v1"), v2 = document.querySelector("#vaz .v2"), vz = $("vaz"), br = $("branco");
const ss = (a, b, x) => {{ const u = Math.min(1, Math.max(0, (x - a) / (b - a))); return u * u * (3 - 2 * u); }};
const luz = (p) => {{
  const o1 = p <= 0 || p >= 1 ? 0 : ss(0, .25, p) * (1 - ss(.55, .7, p));
  const ob = ss(.2, .34, p) * (1 - ss(.52, .6, p)) * .92;
  const o2 = ss(.5, .6, p) * (1 - ss(.66, .94, p)) * .38;
  vz.style.opacity = (o1 > 0 || o2 > 0) ? 1 : 0; v1.style.opacity = o1.toFixed(3); v2.style.opacity = o2.toFixed(3);
  v1.style.transform = `translateX(${{(-14 + 24 * p).toFixed(2)}}%)`; v2.style.transform = `translateX(${{(-8 + 14 * p).toFixed(2)}}%)`;
  br.style.opacity = ob.toFixed(3); }};
for (const t of FL) {{ const st = {{ p: 0 }};
  tl.fromTo(st, {{ p: 0 }}, {{ p: 1, duration: .25, ease: "none", immediateRender: false, onUpdate: () => luz(st.p), onComplete: () => luz(1) }}, t - .14); }}
// ---- estrelas do fundo: cintilação lenta
const EST = [...document.querySelectorAll(".est")], st_e = {{ t: 0 }};
const brilha = () => EST.forEach((e) => {{ const w = +e.dataset.w, sn = Math.sin(w * st_e.t + +e.dataset.f);
  e.style.opacity = (+e.dataset.k ? Math.min(1, (+e.dataset.o + .3)) * (.06 + .94 * Math.pow(Math.max(0, sn), 2.2)) : +e.dataset.o * (.62 + .38 * sn)).toFixed(3); }});
brilha(); tl.fromTo(st_e, {{ t: 0 }}, {{ t: {DUR}, duration: {DUR}, ease: "none", onUpdate: brilha, immediateRender: false }}, 0);
tl.set({{}}, {{}}, {DUR});
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
    open(os.path.join(AQUI, "index.html"), "w").write(H_)
    json.dump(SONS, open(os.path.join(AQUI, "medir", "sons.json"), "w"), indent=0)
    json.dump(MUSICA_EV, open(os.path.join(AQUI, "medir", "musica.json"), "w"), indent=0)
    json.dump({"duracao": DUR, "secoes": [{"id": s["id"], "nome": s["nome"], "t": s["t"], "entrada": s["entrada"]} for s in SECOES],
               "anims": ANIMS}, open(os.path.join(AQUI, "medir", "elementos.json"), "w"), indent=0)
    print(f"{len(SECOES)} seções · {len(ANIMS)} animações · {len(flashes)} flashes · {len(SONS)} sons · {len(MUSICA_EV)} marcas de música · {DUR} s")


if __name__ == "__main__":
    ns = {k: v for k, v in globals().items() if not k.startswith("__")}
    if os.path.exists(os.path.join(AQUI, "moldes.py")) and os.path.exists(os.path.join(AQUI, "medir", "frases.json")):
        exec(open(os.path.join(AQUI, "moldes.py")).read(), ns)
    exec(open(os.path.join(AQUI, "cenas.py")).read(), ns)
    montar()
