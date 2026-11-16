# Tabela de cenas da V2 do reel "Claude Code e a conversa parada" (34 cenas, moldes do original em rodízio). Executado por build.py.
# Espaço 720x1280. Tempos: P(i) = i-ésima palavra da narração (medir/alinhamento.json); P(i, d) = entrada em d quadros; INI = já na tela.
# Fontes: s = Poppins · b = manuscrita reforçada · o = manuscrita · d = serifada itálica · h = Helvetica (perguntas digitadas).
# Regras: nenhuma palavra cortada (margem de 40 px); logo oficial do Claude em toda menção; nada de interface redesenhada.

G = "#505050"      # cinza das palavras gigantes
GL = "#575757"
MARCA = "#d97757"  # laranja oficial do Claude (só no logo e em acentos mínimos)


def LOGO(w):
    return f'<img src="assets/img/claude.svg" style="width:{w}px;height:{w}px;display:block">'


def RELOGIO(p, w, hora=12, minuto=30):
    """Relógio de parede desenhado: ponteiros exatos (o gerador de imagem erra a hora)."""
    ah = (hora % 12) * 30 + minuto * 0.5; am = minuto * 6
    marcas = "".join(f'<line x1="100" y1="{16 if k % 3 == 0 else 20}" x2="100" y2="{30 if k % 3 == 0 else 27}" stroke="#333" stroke-width="{4 if k % 3 == 0 else 2}" transform="rotate({k * 30} 100 100)"/>' for k in range(12))
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 200 200" style="filter:drop-shadow(6px 9px 10px rgba(0,0,0,.25))"><circle cx="100" cy="100" r="92" fill="#fff" stroke="#2b2b2b" stroke-width="9"/>{marcas}'
            f'<line x1="100" y1="100" x2="100" y2="52" stroke="#222" stroke-width="8" stroke-linecap="round" transform="rotate({ah} 100 100)"/>'
            f'<g id="{p}min"><line x1="100" y1="100" x2="100" y2="30" stroke="#222" stroke-width="5" stroke-linecap="round" transform="rotate({am} 100 100)"/></g>'
            f'<circle cx="100" cy="100" r="7" fill="#222"/></svg>')


def BARRA(p, w=520, h=54, de=0.82):
    """Barra de limite: trilho claro + preenchimento escuro (id {p}f) que pode esvaziar."""
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="filter:drop-shadow(5px 7px 8px rgba(0,0,0,.22))"><rect x="0" y="0" width="{w}" height="{h}" rx="{h / 2}" fill="#e3e3e3"/>'
            f'<clipPath id="{p}c"><rect x="0" y="0" width="{w}" height="{h}" rx="{h / 2}"/></clipPath>'
            f'<rect id="{p}f" x="0" y="0" width="{w * de}" height="{h}" fill="#505050" clip-path="url(#{p}c)"/></svg>')


def CHAVE(p, w=220, ligada=True):
    """Chave liga/desliga genérica (não é a interface do Claude Code): trilho id {p}t, botão id {p}b."""
    h = w * 0.52; r = h / 2
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="filter:drop-shadow(6px 8px 9px rgba(0,0,0,.25))"><rect id="{p}t" x="0" y="0" width="{w}" height="{h}" rx="{r}" fill="{"#4d4d4d" if ligada else "#cfcfcf"}"/>'
            f'<circle id="{p}b" cx="{w - r if ligada else r}" cy="{r}" r="{r - 9}" fill="#fff"/></svg>')


def LINHAS(n, w, cor="#c9c9c9", h=9, vao=11, ult=0.6):
    return "".join(f'<div style="height:{h}px;margin-bottom:{vao}px;border-radius:5px;background:{cor};width:{(ult if k == n - 1 else 1) * w if k % 3 else w * 0.86}px"></div>' for k in range(n))


def OLHO(p, w):
    """Olho com pálpebras que fecham numa curva (ids com prefixo p). Abertura e olhar são animados por ANIM lid/move."""
    h = round(w * 130 / 300)
    d = "M4 65 Q150 168 296 65 Q150 168 4 65Z"
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 300 130" style="overflow:visible"><defs>'
            f'<clipPath id="{p}c"><path id="{p}cp" d="{d}"/></clipPath>'
            f'<radialGradient id="{p}g" cx=".5" cy=".45" r=".62"><stop offset="0" stop-color="#fff"/><stop offset=".72" stop-color="#f4f4f6"/><stop offset="1" stop-color="#cfd0d6"/></radialGradient>'
            f'<linearGradient id="{p}i" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f4fc9"/><stop offset=".3" stop-color="#5a6fc0"/><stop offset=".5" stop-color="#dea066"/><stop offset="1" stop-color="#f2cda6"/></linearGradient>'
            f'<filter id="{p}s" x="-20%" y="-40%" width="140%" height="200%"><feDropShadow dx="4" dy="7" stdDeviation="5" flood-color="#000" flood-opacity=".22"/></filter></defs>'
            f'<g filter="url(#{p}s)"><path id="{p}f" d="{d}" fill="url(#{p}g)"/></g>'
            f'<g clip-path="url(#{p}c)"><g id="{p}iris"><circle cx="150" cy="65" r="60" fill="url(#{p}i)"/><circle cx="154" cy="63" r="26" fill="#1b1b1d"/></g></g>'
            f'<path id="{p}b" d="{d}" fill="none" stroke="#46528a" stroke-width="4.2" stroke-linejoin="round" stroke-linecap="round"/></svg>')


CARTAO = "background:#fff;border-radius:18px;box-shadow:12px 16px 30px rgba(0,0,0,.2);"

CINZA_FUNDO = '<div style="width:720px;height:{h}px;background:linear-gradient(to bottom,rgba(0,0,0,{a}),rgba(0,0,0,{b}) 70%,rgba(0,0,0,0))"></div>'
BR = "#fff"


def TELA(src, pos="center center", h=640, a=.55, b=.25):
    """Molde C: foto em tela cheia, sempre em corte seco, com escurecimento no topo para o texto branco."""
    I(src, 360, -4, 724, h=1290, cut=True, pos=pos, z=1)
    RAW(CINZA_FUNDO.format(h=h, a=a, b=b), 360, 0, cut=True, z=2, anc="tc")


# ============================== 1 · MANCHETE ==============================
# 1 — "O Claude Code agora mexe na sua conversa sozinho" (A: recorte P&B com base esfumada; abre com o impacto)
scene(0.0, cam=(0.95, 0, 14))
SOM("impacto", INI)
RAW(LOGO(104), 360, 186, cut=True, z=2)
L([("O", INI), ("Claude", P(1)), ("Code", P(2))], 360, 284, 66)
L([("agora", P(3)), ("mexe", P(4)), ("na", P(5)), ("sua", P(6))], 360, 356, 36, wt=500)
L(("conversa", P(7)), 360, 440, 100, col=G)
I("20-homem-cafe.png", 360, 520, 420, t=P(3, 9), mask=(68, 97), z=2)
L(("sozinho", P(8)), 360, 1096, 170, font="b", z=5)

# 2 — "enquanto você tá no almoço" (B: cartão de foto; palavra branca dentro, pretas fora; única dissolvência, como no original)
_f2 = round((ONS[9]["start"] - 0.10) * 30); DISS[_f2] = (_f2 + 8, _f2 + 14, "blur")
scene(9, cam=(1.0, 22, 0))
I("09-almoco-foto.jpg", 360, 330, 470, h=600, kind="card", cut=True, pos="center 30%")
L([("enquanto", INI), ("você", P(10)), ("tá", P(11)), ("no", P(12))], 360, 268, 42, wt=500)
L(("almoço", P(13)), 360, 840, 124, font="d", col=BR, z=5)
SOM("clique", P(10))

# 3 — "e isso tá economizando o seu limite" (E: objeto)
scene(14, cam=(0.95, 0, 0))
L([("e", INI), ("isso", P(15)), ("tá", P(16))], 232, 300, 40, wt=500)
L(("economizando", P(17)), 360, 384, 84, col=G)
L([("o", P(18)), ("seu", P(19))], 200, 476, 40, wt=500)
L(("limite", P(20)), 380, 520, 140, font="b")
I("40-ampulheta.png", 360, 640, 236, cut=True, shadow="drop-shadow(14px 18px 20px rgba(0,0,0,.24))")
SOM("pop", INI)

# 4 — "sem você perceber" (E: o olho que pisca)
scene(21, cam=(1.0, 0, -16))
RAW(OLHO("oa", 320), 360, 560, cut=True)
ANIM(k="move", id="oairis", t=INI, x=40, y=-4, d=0.01)
ANIM(k="lid", id="oa", t=INI, a=0, b=1, d=0.2, e="sine.out")
ANIM(k="lid", id="oa", t=P(23), a=1, b=0, d=0.22, e="sine.inOut")
ANIM(k="lid", id="oa", t=P(23, antes=-0.30), a=0, b=1, d=0.24, e="sine.inOut")          # pisca: fecha e reabre
L([("sem", INI), ("você", P(22))], 290, 760, 42, wt=500)
L(("perceber", P(23)), 380, 846, 100, font="d", col=G)
SOM("clique-grave", INI)

# ============================== 2 · PROVA ==============================
# 5 — "Tá lá no registro oficial de atualizações" (o trecho real da linha do registro, em inglês como está lá)
scene(24, cam=(1.0, -20, 0))
L([("Tá", INI), ("lá", P(25))], 232, 300, 96, font="b")
L([("no", P(26)), ("registro", P(27))], 400, 388, 44, wt=500)
L(("oficial", P(28)), 360, 482, 118, col=G)
L([("de", P(29)), ("atualizações", P(30))], 360, 578, 44, wt=500)
RAW(f'<div style="{CARTAO}width:610px;padding:28px 32px 30px;white-space:normal">'
    f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">{LOGO(38)}<span style="font:600 28px Poppins;letter-spacing:-.02em;color:#1d1d1d">Claude Code</span>'
    '<span style="font:500 20px Poppins;color:#8d8d8d;margin-left:auto">changelog · 2.1.299</span></div>'
    '<div style="font:500 31px/1.5 \'Helvetica Neue\',Helvetica,Arial,sans-serif;color:#3a3a3a">…left idle for about '
    '<span style="position:relative;white-space:nowrap"><span id="s05gr" style="position:absolute;left:-2px;right:-2px;bottom:-3px;height:5px;background:#222;border-radius:3px;transform-origin:0 50%"></span><b style="position:relative;color:#111">54 minutes</b></span>'
    ' is compacted before its one-hour prompt cache expires…</div></div>', 360, 830, t=P(24, 6), z=3)
ANIM(k="ft", id="s05gr", t=P(30), d=0.3, de={"scaleX": 0}, para={"scaleX": 1}, e="power2.out")
SOM("clique", P(24))

# 6 — "desde outubro, quando uma conversa grande" (F: sanduíche — a torre de papel tapa a palavra gigante)
scene(31, cam=(0.95, 0, 0))
L(("desde", INI), 220, 296, 44, wt=500)
L(("outubro", P(32)), 360, 384, 110, font="d", col=G)
L([("quando", P(33)), ("uma", P(34))], 250, 482, 44, wt=500)
L(("conversa", P(35)), 330, 548, 64)
L(("grande", P(36)), 360, 900, 178, col=G, ls=-0.05, z=1)
I("23-torre-papel.png", 360, 610, 232, t=P(32, 7), sobe=30, ease="power1.out", z=3, shadow="drop-shadow(16px 18px 20px rgba(0,0,0,.22))")
SOM("pop", P(32))

# 7 — "fica uns 54 minutos parada"
scene(37, cam=(1.0, 0, -18))
L([("fica", INI), ("uns", P(38))], 232, 250, 44, wt=500)
L(("54", P(39)), 360, 440, 310, col=G, ls=-0.05)
L(("minutos", P(40)), 360, 640, 72)
L(("parada", P(41)), 330, 750, 112, font="d", col=GL)
I("00-mesa-vazia.png", 360, 860, 380, cut=True)
RAW('<svg width="64" height="76" viewBox="0 0 64 76"><rect x="4" y="4" width="20" height="68" rx="6" fill="#2b2b2b"/><rect x="40" y="4" width="20" height="68" rx="6" fill="#2b2b2b"/></svg>', 560, 754, t=P(41), fade=0.1)
SOM("clique", P(39))

# 8 — "o Claude Code faz um resumo dela por conta própria" (a conversa longa encolhe num resumo)
scene(42, cam=(0.95, 0, 0))
RAW(LOGO(84), 122, 300, t=P(43), fade=0.1, z=2)
L([("o", INI), ("Claude", P(43)), ("Code", P(44))], 414, 300, 56)
L([("faz", P(45)), ("um", P(46))], 232, 398, 44, wt=500)
L(("resumo", P(47)), 400, 470, 170, font="b")
RAW(f'<div id="s08cx" style="{CARTAO}width:300px;height:330px;padding:26px 26px 0;overflow:hidden">{LINHAS(15, 248)}</div>', 360, 610, t=P(45, 5), z=3, anc="tc")
ANIM(k="ft", id="s08cx", t=P(47), d=0.5, de={"height": 330}, para={"height": 112}, e="power2.inOut")
L(("dela", P(48)), 560, 596, 40, wt=500)
L([("por", P(49)), ("conta", P(50))], 300, 820, 44, wt=500)
L(("própria", P(51)), 380, 900, 104, col=G)
SOM("clique", P(45))

# ============================== 3 · VIRADA ==============================
# 9 — "E por que 54 minutos, e não uma hora?" (C: tela cheia, corte seco)
scene(52, cam=(1.06, 0, 0))
TELA("24-relogio-pulso.jpg", h=700, a=.6, b=.3)
L([("E", INI), ("por", P(53)), ("que", P(54))], 360, 178, 46, col=BR, wt=500)
L(("54", P(55)), 196, 330, 176, col=BR, ls=-0.05)
L(("minutos", P(56)), 196, 444, 40, col=BR, wt=500)
L([("e", P(57)), ("não", P(58))], 360, 336, 38, col=BR, wt=500)
L(("60", P(59)), 528, 330, 176, col="#cfcfcf", ls=-0.05)
L(("uma hora?", P(60)), 528, 444, 40, col=BR, wt=500)
SOM("clique", INI)

# 10 — "Porque é justamente com uma hora que o problema acontece" (D: tipografia pura + manchas)
scene(61, blobs=True, cam=(1.0, -22, 0))
L([("Porque", INI), ("é", P(62))], 250, 330, 44, wt=500)
L(("justamente", P(63)), 360, 420, 128, font="b")
L(("com", P(64)), 190, 520, 44, wt=500)
L([("1", P(65)), ("hora", P(66))], 360, 630, 172, col=G, ls=-0.05)
L([("que", P(67)), ("o", P(68))], 220, 752, 44, wt=500)
L(("problema", P(69)), 360, 836, 104, wt=700)
L(("acontece", P(70)), 400, 940, 80, font="d", col=GL)
SOM("clique", P(63))

# ============================== 4 · MECANISMO ==============================
# 11 — "O Claude guarda a sua conversa pronta por uma hora"
scene(71, cam=(0.95, 0, 0))
RAW(LOGO(84), 232, 292, t=P(72), fade=0.1, z=2)
L([("O", INI), ("Claude", P(72))], 420, 292, 60)
L(("guarda", P(73)), 360, 404, 132, col=G)
L([("a", P(74)), ("sua", P(75)), ("conversa", P(76))], 360, 496, 44, wt=500)
I("03-caixa-arquivo.png", 360, 536, 330, t=P(73, 7), sobe=26, ease="power1.out", shadow="drop-shadow(18px 18px 22px rgba(0,0,0,.26))")
L(("pronta", P(77)), 236, 950, 118, font="b")
L(("por", P(78)), 396, 940, 44, wt=500)
L([("1", P(79)), ("hora", P(80))], 560, 946, 64)
SOM("pop", P(73))

# 12 — "e enquanto ela tá guardada, cada mensagem nova custa pouco" (B: cartão de foto; a oração inteira numa cena só)
scene(81, cam=(0.96, 0, 0))
L([("e", INI), ("enquanto", P(82)), ("ela", P(83)), ("tá", P(84))], 360, 196, 40, wt=500)
L(("guardada", P(85)), 300, 262, 96, col=G)
I("02-cronometro.png", 622, 200, 96, t=P(82, 5), sobe=18, ease="power1.out", shadow="drop-shadow(8px 10px 10px rgba(0,0,0,.22))", z=5)
I("25-maos-celular.jpg", 360, 392, 470, h=410, kind="card", t=P(83), fade=0.02)
L([("cada", P(86)), ("mensagem", P(87))], 360, 350, 40, wt=500)
L(("nova", P(88)), 360, 712, 126, font="b", col=BR, z=5)
L(("custa", P(89)), 186, 920, 58)
L(("pouco", P(90)), 414, 910, 146, font="b")
I("04-moeda.png", 628, 832, 100, t=P(90, 4), sobe=30, ease="power2.out", shadow="drop-shadow(8px 10px 10px rgba(0,0,0,.25))")
SOM("pop", P(82)); SOM("clique", P(83)); SOM("pop", P(90))

# 14 — "Só que, passou de uma hora parada" (D: a virada, tipografia + manchas)
scene(91, blobs=True, cam=(1.04, 0, 0))
L([("Só", INI), ("que", P(92))], 300, 404, 150, wt=700)
L([("passou", P(93)), ("de", P(94))], 280, 528, 48, wt=500)
L([("1", P(95)), ("hora", P(96))], 360, 668, 190, col=G, ls=-0.05)
L(("parada", P(97)), 400, 826, 112, font="d", col=GL)
SOM("clique-grave", INI)

# 15 — "ele precisa ler a conversa inteira de novo, desde o começo" (C: tela cheia)
scene(98, cam=(1.07, 0, 0))
TELA("05-pilhas-papel.jpg", a=.5, b=.25)
L([("ele", INI), ("precisa", P(99))], 210, 200, 44, col=BR, wt=500)
L(("ler", P(100)), 172, 296, 150, col=BR)
L([("a", P(101)), ("conversa", P(102))], 420, 304, 52, col=BR, wt=500)
L(("inteira", P(103)), 380, 440, 170, font="b", col=BR)
L([("de", P(104)), ("novo", P(105))], 486, 566, 64, col=BR)
L([("desde", P(106)), ("o", P(107)), ("começo", P(108))], 360, 1176, 50, col=BR, wt=500)
SOM("clique", INI)

# 16 — "e é essa releitura que consome o seu limite" (a barra esvazia)
scene(109, cam=(0.95, 0, 0))
L([("e", INI), ("é", P(110)), ("essa", P(111))], 250, 340, 44, wt=500)
L(("releitura", P(112)), 370, 438, 160, font="b")
L(("que", P(113)), 190, 550, 44, wt=500)
L(("consome", P(114)), 360, 646, 132, col=G)
L([("o", P(115)), ("seu", P(116)), ("limite", P(117))], 360, 752, 50, wt=500)
RAW(BARRA("b16", 540, 58, 0.84), 360, 870, cut=True, z=3)
ANIM(k="attr", id="b16f", t=P(114), d=1.05, de={"width": 454}, para={"width": 92}, e="power2.inOut")

# ============================== 5 · SOBE A APOSTA ==============================
# 17 — "E quanto maior a conversa, maior o gasto" (C variante: dois painéis verticais, um por palavra, cada um com seu golpe)
scene(118, cam=(1.0, 0, 0))
L([("E", INI), ("quanto", P(119))], 360, 196, 48, wt=500)
I("27-papel-muito.jpg", 196, 262, 304, h=660, kind="card", t=P(120), fade=0.02, pos="center center")
I("30-frustrado.jpg", 524, 262, 304, h=660, kind="card", t=P(123), fade=0.02, pos="62% center")
L(("maior", P(120)), 196, 790, 78, col=BR, z=5)
L([("a", P(121)), ("conversa", P(122))], 196, 858, 36, col=BR, wt=500, z=5)
L(("maior", P(123)), 524, 790, 78, col=BR, z=5)
L([("o", P(124)), ("gasto", P(125))], 524, 858, 36, col=BR, wt=500, z=5)
SOM("painel", P(120)); SOM("painel", P(123))

# 18 — "Tanto que, nos planos Pro e Max" (pílulas que pipocam, manchas)
scene(126, blobs=True, cam=(0.97, 0, 0))
L([("Tanto", INI), ("que", P(127))], 360, 440, 112, wt=700)
L([("nos", P(128)), ("planos", P(129))], 360, 548, 48, wt=500)
PILL("Pro", 222, 690, P(130, 6), size=64, pad="12px 44px 14px", raio=22, sobe=22, ease="power2.out")
L(("e", P(131)), 360, 690, 44, wt=500)
PILL("Max", 498, 690, P(132, 6), size=64, pad="12px 44px 14px", raio=22, sobe=22, ease="power2.out")
SOM("pop", P(130)); SOM("pop", P(132))

# 19 — "o Claude Code agora avisa antes"
scene(133, cam=(1.0, -20, 0))
RAW(LOGO(84), 122, 300, t=P(134), fade=0.1, z=2)
L([("o", INI), ("Claude", P(134)), ("Code", P(135))], 414, 300, 56)
L(("agora", P(136)), 200, 404, 44, wt=500)
L(("avisa", P(137)), 262, 520, 164, col=G, ls=-0.04)
I("07-sino.png", 590, 390, 180, t=P(137, 4), sobe=24, ease="power2.out", shadow="drop-shadow(12px 14px 16px rgba(0,0,0,.26))")
L(("antes", P(138)), 360, 720, 190, font="b")
SOM("pop-longo", P(137))

# 20 — "se voltar naquela conversa antiga"
scene(139, cam=(0.95, 0, 0))
I("06-pastas-antigas.png", 360, 300, 440, cut=True, shadow="drop-shadow(16px 18px 22px rgba(0,0,0,.26))")
L([("se", INI), ("voltar", P(140)), ("naquela", P(141))], 360, 760, 44, wt=500)
L(("conversa", P(142)), 360, 836, 70)
L(("antiga", P(143)), 360, 950, 140, font="d", col=G)
SOM("clique", INI)

# 21 — "for consumir uma parte considerável do seu limite de cinco horas"
scene(144, cam=(1.0, 0, -16))
L([("for", INI), ("consumir", P(145))], 280, 300, 44, wt=500)
L([("uma", P(146)), ("parte", P(147))], 300, 376, 62)
L(("considerável", P(148)), 360, 490, 130, font="b")
RAW(BARRA("b21", 560, 62, 1.0), 360, 640, t=INI, z=3)
RAW('<svg width="560" height="62" viewBox="0 0 560 62"><clipPath id="b21k"><rect x="0" y="0" width="560" height="62" rx="31"/></clipPath><rect id="b21p" x="316" y="0" width="0" height="62" fill="#a9a9a9" clip-path="url(#b21k)"/></svg>', 360, 640, t=P(145), fade=0.05, z=4)
ANIM(k="attr", id="b21p", t=P(145), d=0.9, de={"x": 560, "width": 0}, para={"x": 316, "width": 244}, e="power2.out")
L([("do", P(149)), ("seu", P(150)), ("limite", P(151)), ("de", P(152))], 360, 770, 44, wt=500)
L([("5", P(153)), ("horas", P(154))], 360, 900, 170, col=G, ls=-0.05)
SOM("clique", P(148))

# 22 — "ele pergunta se você quer continuar mesmo assim ou começar uma nova"
# A: o recorte P&B entra com a 1ª palavra e FICA; as duas opções entram ao lado, com selos (a pergunta inteira numa cena só)
scene(155, cam=(1.0, 0, 12))
L(("?", P(156)), 600, 470, 300, col="#e6e6e6", z=1, wt=700)
I("28-mulher-pensando.png", 230, 470, 360, t=P(155, 6), mask=(64, 95), z=2)
L([("ele", INI), ("pergunta", P(156))], 360, 250, 66)
L([("se", P(157)), ("você", P(158)), ("quer", P(159))], 360, 336, 44, wt=500)
BADGES([420], 620, 64, [P(160)], nums=(1,))
PILL("continuar<br>mesmo assim", 536, 712, P(160, 6), size=34, pad="14px 24px 16px", raio=18, sobe=22, ease="power2.out")
L(("ou", P(163)), 536, 812, 42, wt=500)
BADGES([420], 880, 64, [P(164)], nums=(2,))
PILL("começar<br>uma nova", 536, 972, P(164, 6), size=34, pad="14px 24px 16px", raio=18, sobe=22, ease="power2.out")
SOM("clique-grave", INI); SOM("pop", P(160)); SOM("pop", P(164))

# 24 — "e na nova ele ainda consegue consultar a antiga se você citar ela"
scene(167, cam=(1.0, 18, 0))
L([("e", INI), ("na", P(168)), ("nova", P(169))], 360, 280, 44, wt=500)
L([("ele", P(170)), ("ainda", P(171)), ("consegue", P(172))], 360, 340, 44, wt=500)
L(("consultar", P(173)), 360, 440, 118, col=G)
RAW(f'<div style="{CARTAO}width:216px;height:270px;padding:24px 22px">{LINHAS(7, 170)}</div>', 196, 690, cut=True, z=3)
RAW(f'<div style="background:#ece8e0;border-radius:18px;box-shadow:12px 16px 30px rgba(0,0,0,.2);width:216px;height:270px;padding:24px 22px">{LINHAS(9, 170, cor="#bdb6a8")}</div>', 524, 690, t=P(175, 5), z=3)
RAW('<svg width="150" height="120" viewBox="0 0 150 120"><defs><mask id="s24mk" maskUnits="userSpaceOnUse" x="0" y="0" width="150" height="120"><path id="s24fm" d="M6 78 C40 10 104 10 140 70" fill="none" stroke="#fff" stroke-width="16" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/></mask></defs>'
    '<path d="M6 78 C40 10 104 10 140 70" fill="none" stroke="#5c5c5c" stroke-width="3" stroke-dasharray="7 6" mask="url(#s24mk)"/><path id="s24pt" d="M128 52 L141 72 L118 74" fill="none" stroke="#5c5c5c" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity="0"/></svg>', 360, 620, cut=True, z=4)
ANIM(k="attr", id="s24fm", t=P(173), d=0.4, de={"stroke-dashoffset": 100}, para={"stroke-dashoffset": 0})
ANIM(k="ft", id="s24pt", t=P(173, antes=-0.36), d=0.06, de={"opacity": 0}, para={"opacity": 1}, e="none")
L(("nova", P(169)), 196, 874, 70, font="b")
L(("antiga", P(175)), 524, 872, 56, font="d", col=GL)
L([("se", P(176)), ("você", P(177)), ("citar", P(178)), ("ela", P(179))], 360, 1000, 46, wt=500)
SOM("pop", P(175))


# ============================== 6 · O OUTRO LADO ==============================
# 26 — "Agora, resumo é resumo" (C: tela cheia)
scene(180, cam=(1.06, 0, 0))
TELA("29-bilhete.jpg", h=720, a=.55, b=.3)
L(("Agora", INI), 220, 210, 60, col=BR)
L(("resumo", P(181)), 380, 340, 160, font="b", col=BR)
L(("é", P(182)), 360, 456, 46, col=BR, wt=500)
L(("resumo", P(183)), 360, 556, 124, col=BR)
SOM("clique", INI)

# 27 — "então algum detalhe da conversa pode ficar de fora"
scene(184, cam=(1.0, -18, 0))
I("11-lupa.png", 196, 330, 300, cut=True)  
L([("então", INI), ("algum", P(185))], 510, 372, 44, wt=500)
L(("detalhe", P(186)), 440, 480, 104, col=G)
L([("da", P(187)), ("conversa", P(188))], 470, 572, 44, wt=500)
L([("pode", P(189)), ("ficar", P(190))], 300, 800, 56)
L([("de", P(191)), ("fora", P(192))], 420, 920, 170, font="b")

# 28 — "e por isso dá pra desligar essa função nas configurações" (a chave real do settings.json)
scene(193, cam=(0.95, 0, 0))
L([("e", INI), ("por", P(194)), ("isso", P(195)), ("dá", P(196)), ("pra", P(197))], 360, 300, 42, wt=500)
L(("desligar", P(198)), 360, 404, 138, col=G)
RAW(CHAVE("c28", 230, True), 360, 560, t=INI, z=3)
ANIM(k="attr", id="c28b", t=P(198), d=0.28, de={"cx": 170.2}, para={"cx": 59.8}, e="power2.inOut")
ANIM(k="attr", id="c28t", t=P(198), d=0.28, de={"fill": "#4d4d4d"}, para={"fill": "#cfcfcf"}, e="power2.inOut")
L([("essa", P(199)), ("função", P(200))], 360, 700, 50, wt=500)
RAW('<div style="background:#1f1f1f;border-radius:16px;box-shadow:10px 12px 22px rgba(0,0,0,.28);padding:16px 30px 20px;font:500 34px/1.35 Menlo,Monaco,Consolas,monospace;color:#f2f2f2;white-space:nowrap">'
    '<div style="font-size:22px;color:#8f8f8f">settings.json</div>"idleCompaction": <span style="color:#d6d6d6">false</span></div>', 360, 842, t=P(201, 6), z=3)
L([("nas", P(201)), ("configurações", P(202))], 360, 984, 62, font="d", col=GL)
SOM("clique", P(198))

# ============================== 7 · VEREDITO ==============================
# 29 — "Mas, na minha opinião, vale deixar ligado"
scene(203, cam=(1.04, 0, 0))
L(("Mas", INI), 250, 380, 180, wt=700)
L([("na", P(204)), ("minha", P(205))], 300, 500, 44, wt=500)
L(("opinião", P(206)), 400, 590, 150, font="b")
L([("vale", P(207)), ("deixar", P(208))], 300, 740, 50, wt=500)
L(("ligado", P(209)), 262, 850, 126, col=G)
RAW(CHAVE("c29", 160, False), 590, 858, t=P(207), fade=0.1, z=3)
ANIM(k="attr", id="c29b", t=P(209), d=0.26, de={"cx": 41.6}, para={"cx": 118.4}, e="power2.inOut")
ANIM(k="attr", id="c29t", t=P(209), d=0.26, de={"fill": "#cfcfcf"}, para={"fill": "#4d4d4d"}, e="power2.inOut")
SOM("clique", P(209))

# 30 — "porque muita gente acha que o limite acaba" (F: silhuetas ancoradas na base, palavra gigante atrás)
scene(210, cam=(1.0, 20, 0))
L(("porque", INI), 210, 300, 44, wt=500)
L(("muita", P(211)), 300, 400, 92, col=G)
L(("gente", P(212)), 380, 800, 196, col="#6a6a6a", ls=-0.05, z=1)
I("10-multidao.png", 360, 880, 760, cut=True, z=3)
L([("acha", P(213)), ("que", P(214)), ("o", P(215)), ("limite", P(216)), ("acaba", P(217))], 360, 540, 46, wt=500)
SOM("clique", P(212))

# 31 — "por causa do tamanho do pedido" (B: cartão que perde a cor durante a frase)
scene(218, cam=(0.96, 0, 0))
L([("por", INI), ("causa", P(219)), ("do", P(220))], 360, 268, 44, wt=500)
I("30-frustrado.jpg", 360, 320, 540, h=600, kind="card", cut=True, gray=P(221), grayd=16, pos="center center")
L([("tamanho", P(221)), ("do", P(222)), ("pedido", P(223))], 360, 846, 50, col=BR, z=5)
SOM("clique", INI)

# 32 — "quando uma parte dele tava indo embora na pausa" (C: tela cheia)
scene(224, cam=(1.06, 0, 0))
TELA("31-mesa-almoco.jpg", h=760, a=.45, b=.2)
L([("quando", INI), ("uma", P(225)), ("parte", P(226)), ("dele", P(227))], 360, 196, 42, col=BR, wt=500)
L([("tava", P(228)), ("indo", P(229)), ("embora", P(230))], 360, 268, 58, col=BR)
L(("na", P(231)), 150, 372, 50, col=BR, wt=500)
L(("pausa", P(232)), 380, 470, 176, col=BR, wt=700)
SOM("clique", INI)

# ============================== 8 · FECHO ==============================
# 33 — volta a figura da abertura, grande e ancorada na base; a pergunta "digitada" palavra a palavra
scene(233, cam=(1.0, 0, 0))
I("20-homem-cafe.png", 360, 500, 560, cut=True, mask=(66, 95), z=2)
L([("E", P(233, 7)), ("você,", P(234, 7)), ("já", P(235, 7)), ("voltou", P(236, 7))], 360, 290, 50, font="h", col="#555", typed=True, ws=0.06)
L([("do", P(237, 7)), ("almoço?", P(238, 7))], 360, 356, 50, font="h", col="#555", typed=True, ws=0.06)

# 34 — mesma figura no mesmo lugar; a segunda pergunta; termina na última palavra
scene(239, cam=(1.0, 0, 0))
I("20-homem-cafe.png", 360, 500, 560, cut=True, mask=(66, 95), z=2)
L([("e", P(239, 7)), ("viu", P(240, 7)), ("o", P(241, 7)), ("seu", P(242, 7)), ("limite", P(243, 7)), ("sumir", P(244, 7))], 360, 290, 50, font="h", col="#555", typed=True, ws=0.06)
L([("sem", P(245, 7)), ("entender", P(246, 7)), ("o", P(247, 7)), ("motivo?", P(248, 7))], 360, 356, 50, font="h", col="#555", typed=True, ws=0.06)
