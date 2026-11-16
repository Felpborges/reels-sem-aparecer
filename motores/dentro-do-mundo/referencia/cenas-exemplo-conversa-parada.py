# REEL "Claude Code e a conversa parada" · MOTOR ESTILO B · voz Andre (PT-BR) com a cadência e o timbre do B
# 30 mundos em rodízio FOTO → APP (faixa) → PAPEL. Tempos presos à fala por P(i)/F(i) (medir/alinhamento.json).
# v3 (12/11): revisão quadro a quadro com 2 revisores independentes; telas no estilo do terminal do Claude Code;
# a linha REAL do changelog (2.1.299); sem números inventados; um laranja de ênfase, coral só na interface do Claude.
IMG = "assets/img/"
IDIOMA = "pt"


def W(i):
    """Abertura do mundo: até 0,25 s antes da 1ª palavra da frase (P já adianta 0,04)."""
    return P(i, 0.10)


def borrao(t0, dur, px=2.0):
    c = MUNDOS[-1]["id"] + "c"
    anim(c, t0, {"filter": "blur(0px)"}, {"filter": f"blur({px}px)"}, dur / 2, "power1.in")
    anim(c, t0 + dur / 2, {"filter": f"blur({px}px)"}, {"filter": "blur(0px)"}, dur / 2, "power1.out")


def fc(t, s, cx, cy, r=0, ease=None):
    """foco() com QUADRO SEGURO para mundos de foto: a foto 720x1280 sempre cobre o quadro.
    Com rotação r a escala mínima é cos r + 1,78 sen r; o centro é limitado ao que essa escala permite."""
    import math
    a = math.radians(abs(r)); k = math.cos(a) + 1.78 * math.sin(a)
    s = max(s, k * 1.02); se = s / k
    dx, dy = 360 * (1 - 1 / se) * 0.96, 640 * (1 - 1 / se) * 0.96
    cx = min(max(cx, 360 - dx), 360 + dx); cy = min(max(cy, 640 - dy), 640 + dy)
    return foco(t, s, round(cx, 1), round(cy, 1), r, ease) if ease else foco(t, s, round(cx, 1), round(cy, 1), r)


MONO = "font-family:'JetBrains Mono';"
FOLGA = "padding:0 24px 16px 0;"            # letra à mão/giz é inclinada: a máscara do escreve() não pode cortar o fim
LARANJA = "#e2531e"                         # a ÚNICA cor de ênfase do reel (palavra-chave, problema, perda)
VERMELHO = "#ff3d5a"                        # só o "60 / 1 hora" (onde o problema acontece)
CINZA = "#e6e6e4"
CC = "#d97757"                              # coral do Claude Code: só na interface (✻, ❯, cursor)
TXT = "#ecebe7"; DIM = "#8b8986"; VERDE = "#7fd88f"; AMBAR = "#e0b25a"


def barra(x, y, w, h=18, cor="#d9dde2", r=9):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{r}px;background:{cor}"></div>'


def janela(x, y, w, h, titulo="claude", fundo="#1d1c1a"):
    """Janela de terminal no estilo do Claude Code (genérica): cantos arredondados, 3 pontos cinza e título em mono.
    Entra JUNTO com o mundo (sem fade: o fade de um contêiner com filhos opacos piscava)."""
    pontos = "".join('<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#4a4844;margin-right:8px"></span>' for _ in range(3))
    return bloco(f'<div style="position:absolute;inset:0;border-radius:20px;background:{fundo};box-shadow:0 24px 50px rgba(0,0,0,.35),0 0 0 1px rgba(255,255,255,.06)"></div>'
                 f'<div style="position:absolute;left:22px;top:20px">{pontos}</div>'
                 f'<div style="position:absolute;left:0;right:0;top:15px;text-align:center;font:500 18px \'JetBrains Mono\';color:#6f6c68">{titulo}</div>'
                 f'<div style="position:absolute;left:0;right:0;top:52px;height:1px;background:rgba(255,255,255,.07)"></div>', x, y, w, h, z=2)


def linha_mono(txt, x, y, size=22, cor=DIM, t="INI", ent="fade", z=4, peso=500, **kw):
    return texto(txt, x, y, size=size, peso=peso, cor=cor, t=t, ent=ent, z=z, extra=MONO + "white-space:pre", **kw)


def foco_tela(y0):
    """Escurece e desfoca a parte de baixo da foto (teclado gerado por IA): a profundidade de campo fica na tela."""
    bloco('<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(8,6,4,.7) 35%,rgba(8,6,4,.9) 100%);'
          'backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(5px);-webkit-mask-image:linear-gradient(180deg,transparent,#000 22%);'
          'mask-image:linear-gradient(180deg,transparent,#000 22%)"></div>', -200, y0, 1120, 1600 - y0, z=1)


def chip_cc(palavras, x, y, size=22, eid=None):
    """Pílula de menção (@) chapada no laranja de ênfase, que nasce com a 1ª palavra e cresce com o texto."""
    eid = eid or _id("cc")
    inner = "".join(f'<span id="{eid}w{k}" style="opacity:0;display:none">{"" if k == 0 else " "}{p}</span>' for k, (p, tt) in enumerate(palavras))
    for k, (p, tt) in enumerate(palavras):
        ANIMS.append({"k": "ft", "id": f"{eid}w{k}", "t": round(tt, 3), "de": {"opacity": 0, "display": "none"},
                      "para": {"opacity": 1, "display": "inline"}, "d": 0.1, "e": "none", "novo": True})
    return bloco(f'<div style="display:inline-block;padding:9px 20px;border-radius:12px;background:{LARANJA};color:#fff;font:600 {size}px \'JetBrains Mono\';white-space:nowrap">{inner}</div>',
                 x, y, z=6, t=palavras[0][1], ent="pop", d=0.2, eid=eid, extra="transform-origin:0 50%")


MASC = ["..XXXXXXX..", "..X.XXX.X..", "XXXXXXXXXXX", "..XXXXXXX..", "..XXXXXXX..", "..X.X.X.X.."]
MASC_CANSADO = ["...........", "..XXXXXXX..", "..X..X..X..", ".XXXXXXXXX.", "..XXXXXXX..", ".X.X...X.X."]


def selecao(x, y, w=500, h=50, t="INI", ent="seco", eid=None):
    """Linha selecionada do terminal do Claude Code: fundo, barra coral de 5 px e o ❯ coral a 16 px; o texto vai em x + 44."""
    return bloco(f'<div style="position:absolute;inset:0;border-radius:10px;background:#2b2925"></div>'
                 f'<div style="position:absolute;left:0;top:0;width:5px;height:{h}px;border-radius:3px;background:{CC}"></div>'
                 f'<div style="position:absolute;left:16px;top:{h / 2 - 15:.0f}px;font:700 22px \'JetBrains Mono\';color:{CC}">❯</div>',
                 x, y, w, h, z=3, t=t, ent=ent, d=0.1, eid=eid)


ALERTA = (f'<svg width="22" height="20" viewBox="0 0 22 20" style="display:inline-block;vertical-align:-3px;margin-right:8px">'
          f'<path d="M11 1.5L21 18.5H1z" fill="{AMBAR}" stroke="{AMBAR}" stroke-width="2" stroke-linejoin="round"/>'
          f'<path d="M11 7.5v5" stroke="#1d1c1a" stroke-width="2.2" stroke-linecap="round"/><circle cx="11" cy="15.4" r="1.3" fill="#1d1c1a"/></svg>')


def mascote_svg(grade, px=8, cor="#1d2619"):
    """O mascote do Claude Code em pixel art (bloquinho com olhos e perninhas), na cor da tela LCD."""
    r = "".join(f'<rect x="{c * px}" y="{l * px}" width="{px}" height="{px}" fill="{cor}"/>'
                for l, linha in enumerate(grade) for c, ch in enumerate(linha) if ch == "X")
    return f'<svg width="{len(grade[0]) * px}" height="{len(grade) * px}" shape-rendering="crispEdges">{r}</svg>'


# 1 · FOTO · almoço: o terminal no notebook mexe na conversa sozinho --------------------------------------------------
LAP = [(240, 168), (655, 168), (640, 385), (242, 385)]
mundo(0.0, nome="almoco", cam=[fc(0.0, 1.04, 380, 600), fc(0.9, 1.16, 410, 540, -1, "power1.inOut"), fc(W(9), 1.32, 440, 490, -1.5, "sine.inOut")])
foto(IMG + "almoco.jpg", filtro="contrast(1.05) saturate(1.02)")
texto("✻ Claude Code", 0, 0, w=415, h=217, quad=LAP, size=24, peso=700, cor=CC, t="INI", extra=f"padding:22px 0 0 26px;{MONO}")
texto("sessão ativa · 12:30", 0, 0, w=415, h=217, quad=LAP, size=18, cor="#7d7a75", t=0.5, ent="fade", extra=f"padding:178px 0 0 26px;{MONO}")
digita("● mexe na sua conversa\n  sozinho", P(4), 0, 0, t1=P(8) + 0.2, w=415, h=217, quad=LAP, size=28, cor="#f2f2f2", cursor=CC,
       lh=1.3, extra=f"padding:74px 0 0 26px;{MONO}")

SOM("impacto", P(8))   # "sozinho" — fecho do gancho (ref: "years ago")
# 2 · PAPEL preto · "enquanto você tá no almoço" ----------------------------------------------------------------
mundo(W(9), fundo="#0b0b0b", nome="almoco-papel", cam=[(W(9), 1.0, 0, 0, 0), (W(14), 1.1, 0, 0, 0)])
texto("12:30", 0, 500, w=720, alinh="center", size=34, peso=500, cor="#a3a3a3", t=P(9) + 0.12, ent="fade", extra=MONO)
assenta([("enquanto", P(9)), ("você", P(10)), ("tá", P(11)), ("\n", None), ("no", P(12)), ("almoço", P(13), f"color:{LARANJA}")],
        0, 580, w=720, size=46, cor="#f4f4f4", cinza="#6d6d6d", peso=700, ls=-0.03)

# 3 · APP (faixa) · o limite para de cair: economia (sem número inventado) ----------------------------------------------
mundo(W(14), fmt="faixa", fundo="#101317", nome="limite", cam=[(W(14), 1.0, 0, 0, 0), (W(21), 1.05, 0, 0, -0.5)], mao=.6)
assenta([("e", P(14)), ("isso", P(15)), ("tá", P(16)), ("economizando", P(17), f"color:{VERDE}"), ("\n", None), ("o", P(18) - 0.1), ("seu", P(19) - 0.12), ("limite", P(20) - 0.2)],
        0, 360, w=720, size=34, cor="#f1f1f1", cinza="#5d6168", peso=700, ls=-0.03)
bloco(barra(0, 0, 560, 230, "#181b20", 22) + '<div style="position:absolute;inset:0;border-radius:22px;box-shadow:0 0 0 1px rgba(255,255,255,.06)"></div>', 80, 560, 560, 230, z=2)
linha_mono("limite de uso", 112, 590, size=22, cor=DIM)
bloco(f'<div style="width:496px;height:26px;border-radius:13px;background:#24262b;overflow:hidden"><div id="lim3" style="width:100%;height:100%;'
      f'border-radius:13px;background:#ecebe7;transform-origin:0 50%"></div></div>', 112, 640, z=3)
anim("lim3", W(14), {"scaleX": 1}, {"scaleX": .8}, P(17) - W(14), "power1.in")
anim("lim3", P(17), {"backgroundColor": "#ecebe7"}, {"backgroundColor": VERDE}, 0.25, "none")
bloco(f'<div style="padding:8px 18px;border-radius:12px;background:rgba(127,216,143,.14);color:{VERDE};font:600 22px \'JetBrains Mono\'">✓ parou de cair</div>',
      112, 700, z=3, t=P(17) + 0.05, ent="pop", d=0.2)

# 4 · PAPEL cinza · "sem você perceber" ----------------------------------------------------------------------------
mundo(W(21), fundo=CINZA, nome="perceber", cam=[(W(21), 1.0, 0, 0, 0), (W(24), 1.1, 0, 0, 0)])
assenta([("sem", P(21)), ("você", P(22)), ("perceber", P(23), "color:#6b6b6b")], 0, 616, w=720, size=42, peso=700, ls=-0.03)

# 5 · APP (faixa) · o registro oficial DE VERDADE: a linha da versão 2.1.299, grifada ------------------------------------
mundo(W(24), fmt="faixa", fundo="#efeeea", nome="registro",
      cam=[(W(24), 1.0, 0, 0, 0), (P(29), 1.0, 0, 0, 0), foco(W(31), 1.06, 360, 600, 0, "power2.inOut")], mao=.6)
assenta([("Tá", P(24)), ("lá", P(25)), ("no", P(26)), ("registro", P(27)), ("oficial", P(28), f"color:{LARANJA}"), ("de", P(29)), ("atualizações", P(30))],
        112, 330, w=560, alinh="left", size=28, peso=700, ls=-0.03, z=6)
bloco(barra(0, 0, 560, 390, "#fff", 22) + '<div style="position:absolute;inset:0;border-radius:22px;box-shadow:0 18px 40px rgba(0,0,0,.08),0 0 0 1px rgba(0,0,0,.06)"></div>',
      80, 404, 560, 390, z=2)
texto("Changelog", 112, 432, size=30, peso=800, cor="#1b1d20", t="INI", ls=-0.03)
linha_mono("2.1.299", 112, 482, size=22, cor=LARANJA, peso=600)
texto('• Added idle compaction in the terminal: a 200K+ token conversation <span id="grifo5" style="background-image:linear-gradient(#ffe34d,#ffe34d);'
      'background-repeat:no-repeat;background-position:0 88%;background-size:0% 62%;padding:0 2px">left idle for about 54 minutes</span> '
      'is compacted before its one-hour prompt cache expires, so your next message doesn’t reprocess it all',
      112, 528, w=460, size=25, peso=500, cor="#2b2b2b", t="INI", lh=1.45, extra="white-space:normal;padding-left:20px;text-indent:-20px")
anim("grifo5", P(29), {"backgroundSize": "0% 62%"}, {"backgroundSize": "100% 62%"}, 0.45, "power2.inOut", novo=True)

# 6 · FOTO · notebook à noite: a conversa grande fica parada (entrada de câmera: preto + exposição) ------------------
LN = [(65, 345), (650, 345), (650, 690), (65, 690)]
mundo(W(31), entrada=("preto", 0.42), nome="parada", cam=[fc(W(31), 1.02, 358, 560), fc(P(37), 1.06, 358, 545, -0.6, "sine.inOut"), fc(W(42), 1.1, 358, 530, -1.2)])
foto(IMG + "laptop-noite.jpg", filtro="contrast(1.06)")
foco_tela(700)
digita("✻ Claude Code · outubro", P(31), 0, 0, t1=P(32) + 0.3, w=585, h=345, quad=LN, size=22, peso=600, cor=DIM, cursor=CC,
       extra=f"padding:30px 0 0 34px;{MONO}", cursor_ate=P(33))
digita("❯ conversa grande", P(33), 0, 0, t1=P(36) + 0.2, w=585, h=345, quad=LN, size=30, cor="#f0eeea", cursor=CC,
       extra=f"padding:84px 0 0 34px;{MONO}", cursor_ate=P(37))
pts = _id("pt")
bloco("".join(f'<span id="{pts}{k}" style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{CC};margin-right:10px;opacity:.25"></span>' for k in range(3)),
      0, 0, 585, 345, quad=LN, z=5, t=P(37), ent="fade", extra="padding:162px 0 0 40px")
for k in range(9):
    anim(f"{pts}{k % 3}", P(37) + 0.12 + k * 0.16, {"opacity": .25}, {"opacity": 1}, 0.1, "none")
    anim(f"{pts}{k % 3}", P(37) + 0.26 + k * 0.16, {"opacity": 1}, {"opacity": .25}, 0.12, "none")
cp = texto("parada há 0 min", 0, 0, w=585, h=345, quad=LN, size=30, peso=700, cor=LARANJA, t=P(38), ent="fade", extra=f"padding:222px 0 0 34px;{MONO}")
conta(cp, P(38), 0, 54, P(41) - P(38) + 0.1, fmt="parada há {} min")

# 7 · FOTO · mesma tela, mais perto (corte seco): o Claude Code resume sozinho ------------------------------------------
mundo(W(42), nome="resumo", cam=[fc(W(42), 1.5, 360, 520), fc(P(47), 1.55, 360, 516, -1, "sine.inOut"), fc(W(52), 1.6, 362, 512, -2)])
foto(IMG + "laptop-noite.jpg", filtro="contrast(1.06)")
foco_tela(640)
texto("✻ Claude Code", 0, 0, w=585, h=345, quad=LN, size=24, peso=600, cor=DIM, t="INI", extra=f"padding:46px 0 0 118px;{MONO}")
digita("✻ fazendo um resumo…", P(45), 0, 0, t1=P(48) + 0.1, w=585, h=345, quad=LN, size=28, cor="#f0eeea", cursor=CC,
       extra=f"padding:110px 0 0 118px;{MONO}", cursor_ate=P(49))
digita("✓ por conta própria", P(49), 0, 0, t1=P(51) + 0.15, w=585, h=345, quad=LN, size=28, cor=VERDE, cursor=VERDE,
       extra=f"padding:170px 0 0 118px;{MONO}")

SOM("whoosh", W(42))   # corte que mergulha na mesma tela (zoom-através): whoosh com pico no corte
# 8 · APP (faixa) · cronômetro: 54 minutos, e não 60 --------------------------------------------------------------------
import math as _m
mundo(W(52), fmt="faixa", fundo="#121315", nome="54x60", cam=[(W(52), 1.0, 0, 0, 0), (P(57), 1.03, 0, 0, -0.6, "sine.inOut"), (W(61), 1.06, 0, 0, -1.2)], mao=.6)
assenta([("E", P(52)), ("por", P(53)), ("que", P(54))], 0, 352, w=720, size=30, cor="#f1f1f1", cinza="#5d6168", peso=600, ls=-0.03)
R8 = 158; C8 = 2 * _m.pi * R8; cx8, cy8 = 360, 646
def _p(a, r): return cx8 + r * _m.cos(_m.radians(a * 6 - 90)), cy8 + r * _m.sin(_m.radians(a * 6 - 90))
tiques = "".join('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%d"/>' % (*_p(a, R8 + 22), *_p(a, R8 + (32 if a % 5 == 0 else 27)),
                 "#5d6168" if a % 5 == 0 else "#33363c", 3 if a % 5 == 0 else 2) for a in range(60) if a not in (0,))
bloco(f'<svg width="720" height="1280" style="overflow:visible">{tiques}'
      f'<circle cx="{cx8}" cy="{cy8}" r="{R8}" fill="none" stroke="#24262b" stroke-width="20"/>'
      f'<circle id="arc54" cx="{cx8}" cy="{cy8}" r="{R8}" fill="none" stroke="#ecebe7" stroke-width="20" '
      f'stroke-dasharray="{C8:.1f}" stroke-dashoffset="{C8:.1f}" transform="rotate(-90 {cx8} {cy8})"/>'
      f'<circle id="arc60" cx="{cx8}" cy="{cy8}" r="{R8}" fill="none" stroke="{VERMELHO}" stroke-width="20" '
      f'stroke-dasharray="{C8 * .1:.1f} {C8:.1f}" stroke-dashoffset="{C8 * .1:.1f}" transform="rotate(234 {cx8} {cy8})"/>'
      f'<line id="tq60" x1="{cx8}" y1="{cy8 - R8 - 16}" x2="{cx8}" y2="{cy8 - R8 + 16}" stroke="{VERMELHO}" stroke-width="5" stroke-linecap="round" opacity="0"/></svg>',
      0, 0, 720, 1280, z=2)
anim("arc54", P(55), {"strokeDashoffset": C8}, {"strokeDashoffset": C8 * .1}, P(56) - P(55) + 0.25, "power2.out", novo=True)
anim("arc60", P(59), {"strokeDashoffset": C8 * .1}, {"strokeDashoffset": 0}, 0.35, "power2.out", novo=True)
anim("tq60", P(59), {"opacity": 0}, {"opacity": 1}, 0.1, "none")
n8 = texto("0", 0, 576, w=720, alinh="center", size=110, peso=800, cor="#f6f6f6", t=P(55), ent="fade", d=0.08, ls=-0.05, lh=1)
conta(n8, P(55), 0, 54, P(56) - P(55) + 0.25, fmt="{}")
texto("minutos", 0, 696, w=720, alinh="center", size=24, peso=600, cor="#8d9097", t=P(56), ent="fade")
assenta([("e", P(57)), ("não", P(58)), ("uma", P(59), f"color:{VERMELHO}"), ("hora?", P(60), f"color:{VERMELHO}")], 0, 878, w=720, size=34, cor="#f1f1f1",
        cinza="#5d6168", peso=700, ls=-0.03)
SOM("clique", P(59) + 0.05)

# 9 · FOTO · lousa em close: "Porque é justamente com uma hora" --------------------------------------------------------
mundo(W(61), nome="lousa", cam=[fc(W(61), 1.04, 360, 620), fc(P(64), 1.08, 360, 600, -1, "power1.inOut"), fc(W(67), 1.12, 362, 590, -2)])
foto(IMG + "lousa-close.jpg", filtro="contrast(1.04)")
g1 = texto("Porque é justamente", 92, 450, font="giz", size=50, peso=400, cor="#f4f1e8", t="INI", ent="seco", extra=GIZ + FOLGA)
escreve(g1, P(61), 0.55)
g2 = texto("com uma hora", 92, 540, font="giz", size=76, peso=700, cor="#ff7a6a", t="INI", ent="seco", extra=GIZ + FOLGA)
escreve(g2, P(64), 0.45)
bloco(f'<svg width="720" height="1280" style="overflow:visible;{GIZ}"><path id="sub9" d="M98 652 C200 660 330 648 520 656" fill="none" stroke="#ff7a6a" '
      f'stroke-width="6" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/></svg>', 0, 0, 720, 1280, z=5)
bloco(f'<svg width="720" height="1280" style="overflow:visible;{GIZ}"><circle id="rel9" cx="360" cy="900" r="118" fill="none" stroke="#f4f1e8" stroke-width="5" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" transform="rotate(-90 360 900)"/>'
      + '<g id="tq9g" opacity="0">' + "".join(f'<line x1="{360 + 100 * _m.cos(_m.radians(a * 30 - 90)):.0f}" y1="{900 + 100 * _m.sin(_m.radians(a * 30 - 90)):.0f}" x2="{360 + 112 * _m.cos(_m.radians(a * 30 - 90)):.0f}" y2="{900 + 112 * _m.sin(_m.radians(a * 30 - 90)):.0f}" stroke="#f4f1e8" stroke-width="4"/>' for a in range(12)) + '</g>'
      + '<path id="pt9" d="M360 900 L360 802 M360 900 L392 846" fill="none" stroke="#ff7a6a" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/></svg>', 0, 0, 720, 1280, z=5)
anim("rel9", P(62), {"strokeDashoffset": 1.1}, {"strokeDashoffset": 0}, 0.5, "power1.inOut", novo=True)
anim("tq9g", P(62) + 0.4, {"opacity": 0}, {"opacity": 1}, 0.2, "none")
anim("pt9", P(64) + 0.02, {"strokeDashoffset": 1.1}, {"strokeDashoffset": 0}, 0.3, "power1.inOut", novo=True)
bloco('<div style="width:720px;height:260px;background:linear-gradient(180deg,rgba(38,40,38,0),rgba(30,32,30,.92) 70%)"></div>', 0, 1060, z=1)
anim("sub9", P(64) + 0.15, {"strokeDashoffset": 1.1}, {"strokeDashoffset": 0}, 0.28, "power1.inOut", novo=True)

# 10 · PAPEL preto · "que o problema acontece" (escala variada: a palavra-problema gigante) ---------------------------
mundo(W(67), fundo=CINZA, nome="problema", cam=[(W(67), 1.0, 0, 0, 0), (W(71), 1.1, 0, 0, 0)])
assenta([("que", P(67)), ("o", P(68))], 0, 520, w=720, size=34, cor="#1b1d20", cinza="#9a9a9a", peso=600, ls=-0.03)
texto("problema", 0, 570, w=720, alinh="center", size=100, peso=800, cor=VERMELHO, t=P(69), ent="assenta", ls=-0.05, lh=1.05)
assenta([("acontece", P(70))], 0, 690, w=720, size=34, cor="#1b1d20", cinza="#9a9a9a", peso=600, ls=-0.03)

# 11 · APP (faixa) · terminal do Claude Code: a conversa guardada por uma hora ------------------------------------------
mundo(W(71), fmt="faixa", fundo="#e9e7e1", nome="guardada", cam=[(W(71), 1.0, 0, 0, 0), (P(77), 1.03, 0, 0, -0.5, "sine.inOut"), (W(81), 1.05, 0, 0, -0.8)], mao=.6)
janela(80, 372, 560, 556)
linha_mono("✻ Claude Code", 110, 446, size=22, cor=CC, peso=700)
for k, l in enumerate(("❯ refatora o módulo de pagamentos", "● Pronto: separei em 3 arquivos", "❯ agora escreve os testes", "● 14 testes passando ✓")):
    linha_mono(l, 110, 494 + k * 30, size=18, cor="#6f6c68")
digita("● O Claude guarda", P(71), 110, 636, t1=P(73) + 0.25, size=24, cor=TXT, cursor=CC, z=4, extra=MONO, cursor_ate=P(74))
digita("  a sua conversa pronta", P(74), 110, 672, t1=P(77) + 0.3, size=24, cor=TXT, cursor=CC, z=4, extra=MONO, cursor_ate=P(78))
bloco(barra(0, 0, 500, 64, "#262522", 14), 110, 832, z=3)
linha_mono("cache", 132, 851, size=20, cor=DIM, peso=600)
bloco(f'<div style="width:220px;height:10px;border-radius:5px;background:#3a3834;overflow:hidden"><div id="cbar" style="width:100%;height:100%;background:{CC};'
      f'transform-origin:0 50%;transform:scaleX(0)"></div></div>', 214, 859, z=4)
anim("cbar", P(78), {"scaleX": 0}, {"scaleX": 1}, P(80) - P(78) + 0.2, "power1.inOut", novo=True)
linha_mono("60 min", 456, 849, size=22, cor=CC, peso=700, t=P(79), ent="pop")

# 12 · FOTO · mãos no teclado: a mensagem nova custa pouco ---------------------------------------------------------------
MS = [(110, 248), (705, 252), (698, 588), (98, 584)]
mundo(W(81), nome="mensagem", cam=[fc(W(81), 1.02, 380, 520), fc(P(86), 1.1, 390, 470, -0.8, "sine.inOut"), fc(W(91), 1.16, 392, 450, -1.5)])
foto(IMG + "maos.jpg", filtro="contrast(1.05)")
digita("● conversa guardada ✓", P(82), 0, 0, t1=P(85) + 0.25, w=600, h=340, quad=MS, size=22, cor=DIM, cursor=DIM,
       extra=f"padding:30px 0 0 30px;{MONO}", cursor_ate=P(86))
digita("❯ mensagem nova", P(86), 0, 0, t1=P(88) + 0.2, w=600, h=340, quad=MS, size=30, cor=TXT, cursor=CC,
       extra=f"padding:100px 0 0 30px;{MONO}", cursor_ate=P(89))
digita("custo: pouco ✓", P(89), 0, 0, t1=P(90) + 0.2, w=600, h=340, quad=MS, size=30, peso=700, cor=VERDE, cursor=VERDE,
       extra=f"padding:170px 0 0 30px;{MONO}")

# 13 · PAPEL preto · "Só que / passou de uma hora parada" --------------------------------------------------------------
mundo(W(91), fundo="#0b0b0b", nome="passou", cam=[(W(91), 1.0, 0, 0, 0), (W(98), 1.1, 0, 0, 0)])
assenta([("Só", P(91)), ("que", P(92)), ("\n", None), ("passou", P(93)), ("de", P(94)), ("uma", P(95), f"color:{VERMELHO}"), ("hora", P(96), f"color:{VERMELHO}"),
         ("parada", P(97))], 0, 580, w=720, size=44, cor="#f4f4f4", cinza="#6d6d6d", peso=700, ls=-0.03)

SOM("queda", W(91))   # virada da história: a "queda" da referência (só em ~1 de cada 6 cortes)
# 14 · APP (faixa) · relê a conversa inteira, até o começo ---------------------------------------------------------------
mundo(W(98), fmt="faixa", fundo="#f3f3f3", nome="releitura", cam=[(W(98), 1.0, 0, 0, 0), (W(109), 1.04, 0, 0, 0)], mao=.6)
linhas = []
for k in range(16):
    esq = k % 2 == 0; w_ = (300, 380, 260, 420, 330, 280)[k % 6]; x_ = 60 if esq else 660 - w_
    fundo_ = "#e2e4e8" if esq else "#cfe2fb"; tinta = "#c4c8cf" if esq else "#a9c6ef"
    nl = 2 if w_ > 330 else 1; h_ = 34 + 22 * nl
    linhas.append(barra(x_, k * 96, w_, h_, fundo_, 24) + "".join(barra(x_ + 22, k * 96 + 18 + 22 * j, (w_ - 60) if j == 0 else (w_ - 120), 9, tinta, 5) for j in range(nl)))
bloco('<div id="rlx" style="position:absolute;left:0;top:-640px;width:720px;height:1540px">' + "".join(linhas) + '</div>',
      0, 0, 720, 1280, z=2, extra="-webkit-mask-image:linear-gradient(180deg,transparent 470px,#000 530px,#000 800px,transparent 850px);"
                                    "mask-image:linear-gradient(180deg,transparent 470px,#000 530px,#000 800px,transparent 850px)")
anim("rlx", W(98), {"y": 0}, {"y": 50}, P(100) - W(98), "none")
anim("rlx", P(100), {"y": 50}, {"y": 1240}, P(106) - P(100), "power2.inOut")
anim("rlx", P(100), {"filter": "blur(0px)"}, {"filter": "blur(2px)"}, 0.5, "power1.in")
anim("rlx", P(105), {"filter": "blur(2px)"}, {"filter": "blur(0px)"}, 0.4, "power1.out")
texto("— início da conversa —", 0, 548, w=720, alinh="center", size=22, peso=600, cor="#8a8a8a", t=P(106), ent="fade", z=3)
bloco('<div style="width:720px;height:170px;background:linear-gradient(#f3f3f3 75%,rgba(243,243,243,0))"></div>', 0, 285, z=4)
assenta([("ele", P(98)), ("precisa", P(99)), ("ler", P(100)), ("a", P(101)), ("conversa", P(102)), ("inteira", P(103)), ("\n", None), ("de", P(104)), ("novo,", P(105)),
         ("desde", P(106), f"color:{LARANJA}"), ("o", P(107), f"color:{LARANJA}"), ("começo", P(108), f"color:{LARANJA}")],
        0, 330, w=720, size=32, peso=700, ls=-0.03, z=5)
bloco('<div style="padding:12px 24px;border-radius:26px;background:#1d1c1a;color:#ecebe7;font:600 22px JetBrains Mono;white-space:nowrap"><span id="rlc">relendo 0 mil tokens</span></div>',
      0, 0, z=6, t=P(100), ent="voa", de=[0, 20, 0, 1], d=0.25, extra="left:50%;top:872px;transform:translateX(-50%)")
conta("rlc", P(100), 0, 212, P(106) - P(100), fmt="relendo {} mil tokens")

# 15 · FOTO · aparelho: o mascote do Claude Code perde as forças enquanto a releitura consome o limite (frase-chave) ----
mundo(W(109), nome="console", cam=[fc(W(109), 1.12, 358, 600), fc(P(113), 1.3, 358, 600, -2, "sine.inOut"), fc(W(118), 1.42, 358, 600, -3.5, "sine.inOut")])
foto(IMG + "console.jpg", filtro="contrast(1.05) saturate(1.02)")
CO = [(180, 487), (535, 487), (535, 712), (180, 712)]
LCDC = "#1d2619"
bloco('<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%,rgba(255,255,255,.16),rgba(0,0,0,.06));'
      'box-shadow:inset 0 0 18px rgba(0,0,0,.22)"></div>', 0, 0, 355, 225, quad=CO, z=3)
seg = "".join(f'<div id="hp{k}" style="width:22px;height:14px;background:{LCDC};box-shadow:inset 0 0 0 2px {LCDC};margin-right:4px"></div>' for k in range(8))
texto("LIMITE", 0, 0, w=355, h=225, quad=CO, font="lcd", size=26, cor=LCDC, t="INI", z=5, extra="padding:14px 0 0 20px;" + LCD)
bloco(f'<div style="position:absolute;left:112px;top:20px;display:flex">{seg}</div>', 0, 0, 355, 225, quad=CO, z=5)
for k in range(8):                                                          # a barra de vida esvazia com "consome o seu limite"
    tk = P(114) + (7 - k) * (P(117) - P(114) + 0.1) / 8
    anim(f"hp{7 - k}", tk, {"backgroundColor": LCDC}, {"backgroundColor": "rgba(29,38,25,0.08)"}, 0.06, "none")
bloco(f'<div id="msc" style="position:absolute;left:22px;top:94px">{mascote_svg(MASC, 8, LCDC)}</div>'
      f'<div id="msc2" style="position:absolute;left:22px;top:100px;opacity:0">{mascote_svg(MASC_CANSADO, 8, LCDC)}</div>',
      0, 0, 355, 225, quad=CO, z=5, extra=LCD)
anim("msc", W(109) + 0.2, {"y": 0}, {"y": -4, "repeat": 5, "yoyo": True}, 0.28, "sine.inOut")                # pulando, cheio de energia
anim("msc", P(114) + 0.05, {"opacity": 1}, {"opacity": .2, "repeat": 5, "yoyo": True}, 0.08, "none")        # leva o golpe e pisca
anim("msc", P(116), {"opacity": 1}, {"opacity": 0}, 0.05, "none")
anim("msc2", P(116), {"opacity": 0, "y": 0}, {"opacity": 1, "y": 6}, 0.3, "power1.out", novo=True)          # cansado, afundando
digita("ESSA\nRELEITURA", P(110), 0, 0, t1=P(112) + 0.4, w=355, h=225, quad=CO, size=44, font="lcd", cor=LCDC, cursor=LCDC,
       lh=0.98, extra="padding:96px 0 0 132px;" + LCD, cursor_ate=P(113), sai=(P(114) - 0.02, "seco"))
digita("CONSOME\nSEU LIMITE", P(114), 0, 0, t1=P(117) + 0.25, w=355, h=225, quad=CO, size=44, font="lcd", cor=LCDC, cursor=LCDC,
       lh=0.98, extra="padding:96px 0 0 132px;" + LCD, cursor_ate=P(117) + 0.3)
tela_lcd(CO, 355, 225)

SOM("riser", W(109)); SOM("queda-grave", W(109))   # frase-chave: riser que corta seco + queda grave (como 19,4 → 20,23 na ref)
# 16 · PAPEL cinza · quanto maior a conversa, maior o gasto ------------------------------------------------------------
mundo(W(118), fundo=CINZA, nome="gasto", cam=[(W(118), 1.0, 0, 0, 0), (W(126), 1.1, 0, 0, 0)])
assenta([("quanto", P(119)), ("maior", P(120)), ("a", P(121)), ("conversa,", P(122))], 0, 430, w=720, size=36, peso=600, ls=-0.03)
for x_, eid_, t_, h_, cor_ in ((250, "g1b", P(120), 150, "#9aa3ad"), (400, "g2b", P(123), 270, LARANJA)):
    bloco(f'<div id="{eid_}" style="position:absolute;left:0;bottom:0;width:80px;height:{h_}px;border-radius:10px 10px 0 0;background:{cor_};'
          f'transform-origin:50% 100%;transform:scaleY(0)"></div>', x_, 800 - 280, 80, 280, z=3)
    anim(eid_, t_, {"scaleY": 0}, {"scaleY": 1}, 0.4, "power2.out", novo=True)
linha_mono("curta", 250, 808, size=20, cor="#6b6b6b", t=P(120), w=80, alinh="center")
linha_mono("longa", 400, 808, size=20, cor=LARANJA, peso=700, t=P(123), w=80, alinh="center")
assenta([("maior", P(123)), ("o", P(124)), ("gasto", P(125), f"color:{LARANJA}")], 0, 866, w=720, size=40, peso=700, ls=-0.03)

# 17 · APP (faixa) · planos Pro e Max ---------------------------------------------------------------------------------
mundo(W(126), fmt="faixa", fundo="#f3f3f3", nome="planos", cam=[(W(126), 1.0, 0, 0, 0), (W(133), 1.05, 0, 0, 0)], mao=.6)
assenta([("Tanto", P(126)), ("que,", P(127)), ("nos", P(128)), ("planos", P(129))], 0, 400, w=720, size=34, peso=600, ls=-0.03)
for x_, nome_, sub_, t_, cor_ in ((96, "Pro", "uso padrão", P(130), "#1b1d20"), (376, "Max", "5× ou 20× mais uso", P(132), LARANJA)):
    bloco(barra(0, 0, 248, 220, "#fff", 26) + '<div style="position:absolute;inset:0;border-radius:26px;box-shadow:0 14px 30px rgba(0,0,0,.06),0 0 0 1px rgba(0,0,0,.05)"></div>'
          f'<div style="position:absolute;left:30px;top:38px;font:800 64px Inter;letter-spacing:-.04em;color:{cor_}">{nome_}</div>'
          f'<div style="position:absolute;left:30px;top:142px;font:600 21px Inter;color:#6b6b6b;white-space:nowrap">{sub_}</div>',
          x_, 470, 248, 220, z=3, t=t_, ent="voa", de=[0, 40, 0, .96], d=0.3)

# 18 · FOTO · celular na mesa: chega o aviso -------------------------------------------------------------------------
mundo(W(133), nome="aviso", cam=[fc(W(133), 1.04, 360, 600), fc(P(136), 1.34, 361, 520, 0, "power2.inOut"), fc(W(139), 1.44, 361, 510, -1)])
foto(IMG + "celular.jpg", filtro="contrast(1.04)")
borrao(P(135), 0.4, 1.2)
texto("13:02", 0, 360, w=720, alinh="center", size=64, peso=300, cor="rgba(40,44,52,.55)", t="INI", ls=-0.02, extra="mix-blend-mode:multiply")
bloco(barra(0, 0, 262, 112, "rgba(250,248,244,.92)", 22) + '<div style="position:absolute;inset:0;border-radius:22px;box-shadow:0 8px 20px rgba(0,0,0,.12)"></div>'
      f'<div style="position:absolute;left:18px;top:18px;width:34px;height:34px;border-radius:9px;background:{CC};color:#fff;font:800 20px JetBrains Mono;text-align:center;line-height:34px">✻</div>'
      f'<div id="nbt" style="position:absolute;left:62px;top:24px;font:700 19px Inter;color:#1b1d20;opacity:0">Claude Code</div>'
      f'<div id="nbs" style="position:absolute;left:18px;top:66px;font:600 19px Inter;color:#3a3a3a;opacity:0">{ALERTA}avisa antes</div>',
      230, 470, 262, 112, z=5, t=P(133), ent="voa", de=[0, -50, 0, 1], d=0.35)
anim("nbt", P(134), {"opacity": 0}, {"opacity": 1}, 0.12, "none", novo=True)
anim("nbs", P(137), {"opacity": 0}, {"opacity": 1}, 0.12, "none", novo=True)
SOM("pop", P(133) + 0.1)

# 19 · APP (faixa) · /resume do Claude Code: voltar numa conversa antiga -----------------------------------------------
mundo(W(139), fmt="faixa", fundo="#151412", nome="antiga", cam=[(W(139), 1.0, 0, 0, 0), (W(144), 1.05, 0, 0, 0)], mao=.6)
janela(80, 400, 560, 470, titulo="claude · /resume")
linha_mono("Retomar sessão", 110, 474, size=22, cor=DIM, peso=600)
selecao(110, 524, eid="sel19")
anim("sel19", P(140), {"y": 0}, {"y": 56}, 0.14, "power2.out")
anim("sel19", P(141) + 0.12, {"y": 56}, {"y": 112}, 0.14, "power2.out")
for k, (l, d_) in enumerate((("refatorar pagamentos", "hoje"), ("testes do checkout", "ontem"))):
    linha_mono(l, 154, 537 + k * 56, size=22, cor=TXT if k == 0 else DIM)
    linha_mono(d_, 500, 536 + k * 56, size=20, cor="#6f6c68")
linha_mono("conversa antiga", 154, 649, size=22, cor=TXT, peso=700, t=P(141), ent="assenta")
linha_mono("há 3 dias", 470, 648, size=20, cor=CC, t=P(141) + 0.1, ent="fade")
linha_mono("enter pra retomar", 110, 800, size=18, cor="#5f5d59")
SOM("clique", P(140))

# 20 · PAPEL cinza · consumir uma parte considerável do limite de 5 horas ------------------------------------------------
mundo(W(144), fundo=CINZA, nome="consumir", cam=[(W(144), 1.0, 0, 0, 0), (W(155), 1.1, 0, 0, 0)])
assenta([("for", P(144) + 0.06), ("consumir", P(144) + 0.1)], 0, 420, w=720, size=38, peso=700, ls=-0.03)
pilula_progresso(110, 520, P(146), 0, 40, 0.9, "uma parte considerável", w=500, eid="pp2")
anim("pp2a", W(144), {"stroke": LARANJA}, {"stroke": LARANJA}, 0.01, "none")
assenta([("do", P(149)), ("seu", P(150)), ("limite", P(151)), ("de", P(152)), ("5", P(153), f"color:{LARANJA}"), ("horas", P(154), f"color:{LARANJA}")],
        0, 760, w=720, size=36, peso=600, ls=-0.03)

# 21 · APP (faixa) · terminal do Claude Code: a pergunta antes de voltar ----------------------------------------------
mundo(W(155), fmt="faixa", fundo="#151412", nome="pergunta", cam=[(W(155), 1.0, 0, 0, 0), (P(160), 1.03, 0, 0, 0, "sine.inOut"), (W(167), 1.06, 0, 0, -0.5)], mao=.6)
janela(80, 400, 560, 500)
linha_mono(ALERTA + "retomar consome parte do limite", 110, 474, size=21, cor=AMBAR, peso=600, t=P(155), ent="fade")
digita("Continuar mesmo assim?", P(158), 110, 530, t1=P(162) + 0.2, size=28, peso=700, cor=TXT, cursor=CC, z=4, extra=MONO, cursor_ate=P(162) + 0.25)
selecao(110, 606, t=P(162) + 0.28, ent="fade")
linha_mono("1. Continuar", 154, 619, size=24, cor=TXT, peso=700, t=P(162) + 0.28, ent="assenta")
linha_mono("2. Começar uma nova", 154, 682, size=24, cor=DIM, t=P(164), ent="assenta")
linha_mono("↑↓ escolher · enter confirmar", 110, 830, size=18, cor="#5f5d59")

# 22 · FOTO · caderno novo consulta o antigo -----------------------------------------------------------------------------
mundo(W(167), nome="cadernos", cam=[fc(W(167), 1.12, 360, 860), fc(P(172), 1.1, 380, 640, -1, "power2.inOut"), fc(W(176), 1.12, 360, 540, -2, "sine.inOut")])
foto(IMG + "cadernos.jpg", filtro="contrast(1.05)")
borrao(P(172) - 0.1, 0.5, 1.2)
nv = texto("na nova", 120, 776, size=60, font="mao", peso=700, cor="#1f3a8a", t="INI", ent="seco", extra=FOLGA)
escreve(nv, P(168), 0.4)
risco([(122, 858), (220, 864), (330, 860)], P(170), d=0.25, cor="#1f3a8a", esp=3.5, curva=True)
ct = texto("consulta", 432, 752, size=40, font="mao", peso=700, cor="#1f3a8a", t="INI", ent="seco", rot=-6, extra=FOLGA)
escreve(ct, P(172) - 0.02, 0.3)
risco([(560, 744), (612, 560), (512, 380)], P(172) + 0.2, d=0.35, cor="#1f3a8a", esp=3.5, curva=True)
risco([(490, 396), (512, 380), (522, 406)], P(172) + 0.53, d=0.1, cor="#1f3a8a", esp=3.5)
an = texto("a antiga", 410, 300, size=52, font="mao", peso=700, cor="#6b3d16", t="INI", ent="seco", rot=-2, extra=FOLGA)
escreve(an, P(172) + 0.53, 0.35)
SOM("whoosh", (W(167) + P(172)) / 2)        # pico no meio do movimento de câmera

# 23 · APP (faixa) · na conversa nova, citar a antiga (campo do Claude Code) ----------------------------------------
mundo(W(176), fmt="faixa", fundo="#151412", nome="citar", cam=[foco(W(176), 1.06, 360, 690), foco(W(180), 1.1, 360, 696)], mao=.6)
linha_mono("✻ nova conversa", 0, 560, size=22, cor=DIM, peso=600, w=720, alinh="center")
bloco('<div style="position:absolute;inset:0;border-radius:16px;border:2px solid #4a4743;background:#1d1c1a"></div>', 110, 660, 500, 88, z=3)
linha_mono("❯", 132, 684, size=26, cor=CC, peso=700)
digita("se você citar", P(176), 168, 686, t1=P(178) + 0.02, size=24, cor=TXT, cursor=CC, z=4, extra=MONO, cursor_ate=P(178) + 0.06)
chip_cc([("@conversa", P(178)), ("antiga", P(179))], 372, 682, size=19)
SOM("clique", P(178))

# 24 · PAPEL cinza · "Agora, resumo é resumo" (o segundo "resumo" sai espremido: perdeu algo) -----------------------------
mundo(W(180), fundo=CINZA, entrada=("dissolve", 0.2), nome="resumo-e-resumo", cam=[(W(180), 1.0, 0, 0, 0), (W(184), 1.1, 0, 0, 0)])
assenta([("Agora,", P(180))], 0, 540, w=720, size=30, peso=600, cor="#6b6b6b", cinza="#a0a0a0", ls=-0.02)
assenta([("resumo", P(181)), ("é", P(182)), ("r<span style=\"opacity:.28\">e</span>sum<span style=\"opacity:.28\">o</span>", P(183, 0.05), "color:#6b6b6b")], 0, 596, w=720, size=56, peso=800, ls=-0.04)

# 25 · FOTO · quebra-cabeça (girado: a peça de fora fica no alto, longe da legenda do Instagram) ----------------------
mundo(W(184), nome="quebra", cam=[fc(W(184), 1.04, 360, 640, 0), fc(P(189), 1.1, 340, 560, -1.5, "sine.inOut"), fc(W(193), 1.14, 362, 540, -2)])
foto(IMG + "quebra-180.jpg", filtro="contrast(1.05)")
assenta([("algum", P(185)), ("detalhe", P(186)), ("\n", None), ("da", P(187)), ("conversa", P(188))], 0, 630, w=720, size=50, peso=800,
        cor="#1b1d20", cinza="#9a9a9a", ls=-0.04, extra="mix-blend-mode:multiply")
assenta([("pode", P(189)), ("ficar", P(190)), ("de", P(191)), ("fora", P(192, 0.08), f"color:{LARANJA}")], 0, 820, w=720, size=50, peso=800,
        cor="#1b1d20", cinza="#9a9a9a", ls=-0.04, extra="mix-blend-mode:multiply")
laco(250, 412, 92, 84, P(190), cor=LARANJA, esp=4)

# 26 · APP (faixa) · /config do Claude Code: dá pra desligar o resumo automático ----------------------------------------
mundo(W(193), fmt="faixa", fundo="#151412", nome="config", cam=[(W(193), 1.0, 0, 0, 0), (P(198), 1.03, 0, 0, 0, "sine.inOut"), (W(203), 1.06, 0, 0, -0.5)], mao=.6)
assenta([("dá", P(196)), ("pra", P(197)), ("desligar", P(198), f"color:{LARANJA}"), ("essa", P(199)), ("função", P(200)), ("\n", None),
         ("nas", P(201)), ("configurações", P(202))], 0, 330, w=720, size=30, cor="#f1f1f1", cinza="#5d6168", peso=700, ls=-0.03, z=6)
janela(80, 450, 560, 450, titulo="claude · /config")
linha_mono("Tema", 154, 530, size=22, cor=DIM); linha_mono("escuro", 470, 530, size=22, cor=DIM)
selecao(110, 576)
linha_mono("Resumo automático", 154, 589, size=22, cor=TXT, peso=700)
linha_mono("ligado", 470, 589, size=22, cor=VERDE, peso=700, sai=(P(198), "seco"))
linha_mono("desligado", 470, 589, size=22, cor="#a3a09b", peso=700, t=P(198), ent="pop")
linha_mono("Idioma", 154, 650, size=22, cor=DIM); linha_mono("português", 470, 650, size=22, cor=DIM)
linha_mono("✓ salvo", 110, 820, size=20, cor=VERDE, peso=600, t=P(202) + 0.3, ent="pop")
SOM("clique", P(198))

# 27 · PAPEL preto · "Mas, na minha opinião, vale deixar ligado" ----------------------------------------------------
mundo(W(203), fundo="#0b0b0b", nome="opiniao", cam=[(W(203), 1.0, 0, 0, 0), (W(210), 1.1, 0, 0, 0)])
assenta([("Mas,", P(203)), ("na", P(204)), ("minha", P(205)), ("opinião,", P(206)), ("\n", None), ("vale", P(207)), ("deixar", P(208)),
         ("ligado", P(209), f"color:{VERDE}")], 0, 540, w=720, size=44, cor="#f4f4f4", cinza="#6d6d6d", peso=700, ls=-0.03)
bloco(f'<div style="padding:12px 26px;border-radius:14px;background:#161a16;box-shadow:0 0 0 1px #2c3a2e;font:600 22px \'JetBrains Mono\';color:{VERDE};white-space:nowrap">'
      '✓ resumo automático · ligado</div>', 0, 0, z=4, t=P(209) - 0.05, ent="pop", d=0.22, extra="left:50%;top:700px;transform:translateX(-50%)")

# 28 · FOTO · caderno: o que muita gente acha (riscado com traço fino, depois de ler) -----------------------------------
mundo(W(210), nome="caderno", cam=[fc(W(210), 1.04, 360, 620, 0), fc(P(215), 1.05, 362, 612, -0.8, "sine.inOut"), fc(W(224), 1.07, 364, 604, -1.2, "sine.inOut")])
foto(IMG + "caderno.jpg", filtro="contrast(1.05)")
MAO = "#26306a"
for txt_, x_, y_, t_, sz in (("muita gente", 88, 440, P(211), 44), ("acha:", 88, 500, P(213), 44), ("o limite acaba", 425, 440, P(215) - 0.15, 38),
                             ("por causa do", 425, 500, P(218) - 0.2, 38), ("tamanho", 425, 560, P(221) - 0.33, 38), ("do pedido", 425, 620, P(221) + 0.06, 38)):
    e_ = texto(txt_, x_, y_, size=sz, font="mao", peso=700, cor=MAO, t="INI", ent="seco", extra=FOLGA + "mix-blend-mode:multiply")
    escreve(e_, t_, 0.3)
risco([(418, 584), (482, 581), (552, 585)], P(222) + 0.11, d=0.14, cor="#c8402f", esp=3, curva=True)
risco([(418, 644), (500, 641), (580, 645)], P(222) + 0.17, d=0.14, cor="#c8402f", esp=3, curva=True)

# 29 · PAPEL cinza · "quando uma parte dele tava indo embora na pausa" (frase-chave) -----------------------------------
mundo(W(224), fundo=CINZA, nome="pausa", cam=[(W(224), 1.0, 0, 0, 0), (W(233), 1.14, 0, 0, 0, "sine.inOut")])
assenta([("quando", P(224)), ("uma", P(225)), ("parte", P(226)), ("dele", P(227)), ("\n", None), ("tava", P(228)), ("indo", P(229)), ("embora", P(230))],
        0, 440, w=720, size=38, peso=600, ls=-0.03)
hl = _id("hl")
bloco(f'<div id="{hl}" style="width:330px;height:34px;background:#ffd84d;border-radius:4px;transform-origin:0 50%;transform:scaleX(0)"></div>', 195, 664, z=3)
anim(hl, P(232), {"scaleX": 0}, {"scaleX": 1}, 0.3, "power2.out", novo=True)
texto("na pausa", 0, 610, w=720, alinh="center", size=76, peso=800, cor="#1b1d20", t=P(231), ent="assenta", ls=-0.04, z=4)
bloco('<div style="display:flex;gap:12px"><div style="width:16px;height:52px;border-radius:4px;background:#1b1d20"></div>'
      '<div style="width:16px;height:52px;border-radius:4px;background:#1b1d20"></div></div>', 340, 780, z=4, t=P(232) + 0.08, ent="pop", d=0.2)
SOM("impacto-3", P(232))   # "pausa." — o soco final antes do quase-silêncio, como "short game" na ref

# 30 · CTA · comentário digitado palavra a palavra (vazamento de luz) -------------------------------------------------
mundo(W(233), fundo="#f5f6fa", entrada=("flash", 0.3), nome="cta",
      cam=[foco(W(233), 1.18, 360, 580), foco(P(239), 1.18, 360, 590), foco(P(240), 1.14, 360, 630, 0, "power2.inOut"),
           foco(P(245), 1.14, 360, 640), foco(P(246), 1.1, 360, 650, 0, "power2.inOut"), foco(DUR, 1.12, 360, 650)])
texto("Comentários", 100, 400, size=26, peso=700, cor="#1b1d20", t="INI")
bloco('<div style="width:52px;height:52px;border-radius:50%;background:#e9eef7;color:#0075de;font:700 24px Inter;text-align:center;line-height:52px">V</div>',
      100, 460, z=4)
texto("você", 168, 474, size=22, peso=600, cor="#5f6368", t="INI")
bloco('<div style="position:absolute;inset:0;border-radius:24px;background:#fff;box-shadow:0 0 0 2px #d9dde5,0 12px 30px rgba(20,30,60,.06)"></div>', 80, 528, 560, 236, z=3)
CTA = "E você, já voltou\ndo almoço e viu\no seu limite sumir\nsem entender o motivo? "
digita(CTA, P(233), 108, 552, t1=F(248) - 0.05, size=38, peso=700, cor="#1b1d20", cursor="#0075de", lh=1.2, z=5, cursor_ate=F(248) + 0.6)
bloco('<div style="padding:12px 30px;border-radius:24px;background:#0075de;color:#fff;font:700 22px Inter">Publicar</div>', 452, 790, z=4)
tt = P(233) + 0.05
while tt < F(248) - 0.1:
    SOM("tecla", tt); tt += 0.17
