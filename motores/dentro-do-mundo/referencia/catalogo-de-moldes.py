# MOTOR DENTRO DO MUNDO · CATÁLOGO DE MOLDES: a chamada de cada um dos 14 mundos medidos na referência do estilo.
# NÃO é um reel pronto. O texto é só enfeite (tema inventado: criar o hábito de treinar) e os tempos são números fixos de
# exemplo; num reel de verdade cada tempo sai de P(i) (a palavra i da narração) e as imagens são as do seu tema.
# Use para copiar a estrutura de um mundo (câmera, superfície, entrada, som) e adaptar. Um reel inteiro e aprovado, com
# P(i) em tudo, está em cenas-exemplo-conversa-parada.py. Regras de quadro seguro: MOTOR.md §7.5.
IMG = "assets/img/"
IDIOMA = "pt"


def borrao(t0, dur, px=2.0):
    """Borrão de movimento na câmera do mundo atual durante um movimento rápido (sobe e desce em `dur`)."""
    c = MUNDOS[-1]["id"] + "c"
    anim(c, t0, {"filter": "blur(0px)"}, {"filter": f"blur({px}px)"}, dur / 2, "power1.in")
    anim(c, t0 + dur / 2, {"filter": f"blur({px}px)"}, {"filter": "blur(0px)"}, dur / 2, "power1.out")


SOMBRA = "text-shadow:0 2px 16px rgba(0,0,0,.5),0 1px 3px rgba(0,0,0,.35);"

# 1 · sala com lousa, dentro do visualizador de fotos -----------------------------------------------------------
mundo(0.0, nome="sala", cam=[(0.0, 1.0, 0, 0, 0), (0.95, 1.16, 0, -46, 0, "power1.inOut")])
foto(IMG + "sala.jpg", filtro="saturate(.92) contrast(1.05)")
luz(0.0, 1.0, x=470, y=520, tam=420, arco=True, forte=.35)
SALA_LOUSA = [(150, 446), (560, 446), (560, 684), (150, 684)]                       # a lousa da sala (o zoom "encontra" o texto)
gz = texto('<div style="padding:62px 0 0 40px;font-size:30px;line-height:1.3">Um estudo antigo<br>já avisava disso</div>', 0, 0, w=410, h=238,
           quad=SALA_LOUSA, font="giz", peso=400, cor="#f4f1e8", t="INI", ent="seco", extra=GIZ)
escreve(gz, 0.32, 0.55)
SOMBRA_FORTE = "text-shadow:0 2px 18px rgba(0,0,0,.75),0 1px 4px rgba(0,0,0,.6);"
assenta([("Um", 0.10, "color:#d6302b"), ("estudo", 0.42), ("\n", None), ("antigo", 0.62)], 96, 700, w=560, size=56, peso=800,
        alinh="left", cor="#ffffff", cinza="#f0f0f0", ls=-0.02, lh=1.06, extra=SOMBRA_FORTE, sai=(0.9, "fade", 0.08))
ui_galeria()

# 2 · lousa em close (zoom-através) --------------------------------------------------------------------------------
mundo(1.10, entrada=("zoom", 0.30), nome="lousa", cam=[foco(1.10, 1.1, 350, 628, 1.5), foco(2.1, 1.18, 360, 618, -2.5), foco(3.13, 1.22, 368, 612, -5)])
foto(IMG + "lousa.jpg", filtro="contrast(1.04) saturate(.95)")
luz(1.2, 1.9, x=600, y=250, tam=380, arco=True, forte=.3)
LOUSA = [(40, 372), (690, 500), (690, 712), (40, 650)]   # área de giz da lousa (segue a perspectiva)
lz = _id("lz")
bloco(f'''<div style="position:absolute;inset:0;font-family:Kalam;color:#f4f1e8;{GIZ}">
  <div id="{lz}a" style="position:absolute;left:70px;top:70px;font-size:46px;line-height:1.3">Um estudo antigo</div>
  <div id="{lz}b" style="position:absolute;left:70px;top:136px;font-size:46px;line-height:1.3">já avisava</div>
  <div id="{lz}c" style="position:absolute;left:374px;top:132px;font-size:50px;line-height:1.3;color:#ff7a6b">faz</div>
  <div id="{lz}d" style="position:absolute;left:494px;top:132px;font-size:50px;line-height:1.3;color:#ff7a6b">tempo</div>
</div>
<svg class="deco" style="position:absolute;left:0;top:0;overflow:visible;{GIZ}" width="650" height="260" fill="none" stroke="#ff7a6b" stroke-width="4.5" stroke-linecap="round">
  <path id="{lz}s" d="M72 200 C140 206 240 204 330 198" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>
  <path id="{lz}l" d="M368 152 C420 140 540 138 580 158 C606 176 552 204 470 206 C396 208 356 196 360 176 C364 162 392 152 428 148" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>
</svg>''', 0, 0, 650, 260, quad=LOUSA, z=4)
escreve(lz + "a", 1.14, 0.30); escreve(lz + "b", 1.30, 0.22); escreve(lz + "c", 1.68, 0.16); escreve(lz + "d", 1.94, 0.12)
anim(lz + "s", 1.46, {"strokeDashoffset": 1.1}, {"strokeDashoffset": 0}, 0.35, "power1.inOut", novo=True)
anim(lz + "l", 2.06, {"strokeDashoffset": 1.1}, {"strokeDashoffset": 0}, 0.42, "power1.inOut", novo=True)
ui_galeria()
SOM("boom", 1.32)

# 3 · visor da câmera sobre a mesa (quadro preto + exposição) ----------------------------------------------------
mundo(3.13, entrada=("preto", 0.42), nome="camera", cam=[foco(3.13, 1.22, 368, 600, -6), foco(4.3, 1.36, 374, 632, -4.5), foco(5.0, 1.48, 380, 655, -3.5), foco(5.93, 1.6, 386, 676, -2.5)])
foto(IMG + "mesa-contrato.jpg", filtro="contrast(1.08) saturate(1.05)")
texto("A FORÇA", 0, 286, w=748, alinh="center", size=58, peso=900, cor="#f4ecdf", t=3.45, ent="voa", de=[0, -40, 0, 1.2], rot=-10, ls=-0.01, sai=(4.7, "blur", 0.22),
      extra="word-spacing:.18em;text-shadow:0 2px 0 #c9b9a0,0 4px 0 #a8957a,0 6px 0 #857257,0 8px 0 #5e4c36,0 16px 22px rgba(40,20,0,.6)")
texto("DO HÁBITO", 0, 360, w=760, alinh="center", size=46, peso=900, cor="#e2483a", t=3.75, ent="voa", de=[0, -40, 0, 1.2], rot=-10, ls=-0.01, sai=(4.7, "blur", 0.22),
      extra="word-spacing:.18em;text-shadow:0 2px 0 #a22,0 4px 0 #811,0 6px 0 #600,0 14px 20px rgba(40,10,0,.6)")
PAPEL = [(365, 405), (665, 545), (395, 915), (70, 735)]
texto('<div style="font-size:54px;color:#7a5418;padding:44px 0 0 64px">Lista</div>', 0, 0, w=340, h=500, quad=PAPEL, font="mao", peso=700, t="INI")
l1 = texto('<div style="padding:150px 0 0 56px">1. Vai ser</div>', 0, 0, w=340, h=500, quad=PAPEL, font="mao", size=42, cor="#4a3622", t="INI", ent="seco")
l2 = texto('<div style="padding:212px 0 0 56px">2. Constância</div>', 0, 0, w=340, h=500, quad=PAPEL, font="mao", size=42, cor="#4a3622", t="INI", ent="seco")
l3 = texto('<div style="padding:286px 0 0 110px">diária</div>', 0, 0, w=340, h=500, quad=PAPEL, font="mao", size=42, cor="#4a3622", t="INI", ent="seco")
escreve(l1, 4.5, 0.32); escreve(l2, 4.84, 0.34); escreve(l3, 5.2, 0.22)
ui_camera(reticulo=(396, 760, 150, .7))
SOM("boom", 4.0)

# 4 · papel cinza: a câmera ATRAVESSA as duas primeiras palavras (as letras viram 1º plano) e a palavra-soco fica no centro livre ------
mundo(5.93, fundo="radial-gradient(circle at 50% 48%, #efeeec 0%, #e2e0de 55%, #d3d1cf 100%)", nome="papel-soco",
      cam=[(5.93, 1.0, 0, 0, 0), (7.07, 1.06, 0, 0, 0)])
borda_filme()
TAM = 58; w1 = _larg("Eles", TAM, 600, ls=-0.03); w2 = _larg("sabiam", TAM, 600, ls=-0.03); gap = 0.26 * TAM
ox = (720 - (w1 + gap + w2)) / 2 + w1 + gap / 2; oy = TAM * 1.15 * 0.8 - 0.27 * TAM     # entre as duas palavras, no meio da altura-x
ta = assenta([("Eles", 6.0), ("sabiam", 6.16, "color:#8a8a8a")], 0, 580, w=720, size=TAM, peso=600, ls=-0.03)
anim(ta + "l0w1", 6.24, {"color": "#8a8a8a"}, {"color": "#1b1d20"}, 0.12, "none")
anim(ta, 6.22, {"scale": 1, "filter": "blur(0.5px)", "transformOrigin": f"{ox:.0f}px {oy:.0f}px"},
     {"scale": 15, "filter": "blur(1.5px)", "transformOrigin": f"{ox:.0f}px {oy:.0f}px"}, 0.2, "power2.in")
anim(ta, 6.44, {"scale": 15}, {"scale": 16.2}, 0.63, "none")                                  # as letras gigantes seguem derivando
p1 = img(IMG + "placa.png", 450, -120, 380, z=7, t=6.26, ent="voa", de=[220, -220, 30, 1.2], d=0.4, blur=8, rot=18)
p2 = img(IMG + "placa.png", -80, 466, 190, z=7, t=6.30, ent="voa", de=[-200, 40, -30, 1.2], d=0.4, blur=4, rot=-22)
anim(p1, 6.66, {"x": 0, "y": 0}, {"x": 26, "y": -18}, 0.41, "none"); anim(p2, 6.7, {"x": 0, "y": 0}, {"x": -18, "y": 10}, 0.37, "none")
tw = texto("disso.", 0, 636, w=720, alinh="center", size=64, peso=700, cor="#e2531e", t=6.58, ent="assenta", z=8, ls=-0.03)
anim(tw, 6.82, {"scale": 1}, {"scale": 1.04}, 0.25, "none")
img(IMG + "placa.png", 472, 690, 62, z=9, t=6.62, ent="pop", rot=-24, sombra=True)
SOM("boom", 6.30)

# 5 · preto com globo ------------------------------------------------------------------------------------------------
mundo(7.07, fundo="#0b0b0b", nome="preto-globo", cam=[(7.07, 1.0, 0, 0, 0), (8.07, 1.09, 0, 0, 0)])
wa, wb, G_ = _larg("Hoje em", 52, 700, ls=-0.04) * 1.06, _larg("dia,", 52, 700, ls=-0.04) * 1.06, 150   # grupo centralizado (folga de 6 %)
x0g = (720 - (wa + 26 + G_ + 26 + wb)) / 2
texto("Hoje em", x0g, 612, size=52, peso=700, cor="#fff", t=7.22, ent="assenta", ls=-0.04)
img(IMG + "globo.png", x0g + wa + 26, 566, G_, t=7.52, ent="pop", d=0.3)
texto("dia,", x0g + wa + 26 + G_ + 26, 612, size=52, peso=700, cor="#fff", t=7.62, ent="assenta", ls=-0.04)
SOM("pop", 7.55)

# 6 · celular antigo: 5 linhas curtas (letra grande que cabe na tela), câmera mostra a tela inteira ---------------------
TELA = [(192, 212), (526, 212), (526, 548), (192, 548)]
LINHAS_NOTA = ["Ninguém fica", "em forma", "NUM DIA!!", "Fica em", "forma aos poucos."]
TAM_NOTA = 60
while max(_larg(l, TAM_NOTA, 700) for l in LINHAS_NOTA) * 1.06 + 10 > 334 - 2 * 26 or len(LINHAS_NOTA) * TAM_NOTA * 1.18 > 336 - 34: TAM_NOTA -= 1
mundo(8.07, fundo="#050505", nome="celular", cam=[foco(8.07, 1.06, 360, 640), foco(8.35, 1.35, 359, 560, 0, "power1.in"), foco(8.6, 1.66, 359, 405, 0, "power1.out"),
      foco(9.4, 1.74, 359, 420, -1, "sine.inOut"), foco(10.15, 1.82, 359, 470, -2, "sine.inOut"), foco(10.5, 1.86, 361, 476, -2.5)])
foto(IMG + "celular.jpg", filtro="contrast(1.05) saturate(.9)")
borrao(8.12, 0.42, 1.6)
texto(f'<div style="position:absolute;left:0;right:0;top:-31px;text-align:center;font:700 21px Inter;color:#1b3a7a">{R("notas")}</div>', 192, 212, w=334, t="INI", z=5)
digita("\n".join(LINHAS_NOTA), 8.1, 0, 0, t1=10.15, w=334, h=336, quad=TELA, size=TAM_NOTA, peso=700,
       cor="#1a1a1a", cursor="#1a1a1a", lh=1.18, extra="padding:14px 26px;white-space:pre;font-family:Inter")
tela_lcd(TELA, 334, 336)
img(IMG + "smartphone.png", 470, 600, 150, z=8, t=9.15, ent="entra", de=[300, 60, 30, 1], d=0.55, rot=-70, blur=0.5, sombra=True)   # passa sobre o teclado
anim("i" + str(_n[0]), 9.75, {"x": 0, "y": 0, "rotation": 0}, {"x": -260, "y": 14, "rotation": 16}, 0.75, "sine.inOut")
SOM("boom", 8.07)

# 7 · ranking escuro (faixa): rola rápido, para com as 2 últimas linhas no alto e a frase mora logo abaixo -------------
mundo(10.50, fmt="faixa", fundo="#0f1b22", nome="ranking", cam=[(10.5, 1.0, 0, 0, 0), (14.17, 1.04, 0, -8, 0)], mao=.6)
bloco('<div style="position:absolute;inset:0;background:linear-gradient(#123a2c,#101a22 60%)"></div>', 0, 0, 720, 1280, z=0)
hid, lid = ranking([("C", "Clube da Manhã", "Seu melhor hábito", ""), ("A", "Ana Braga", "Treina toda semana", "+200 dias"),
                    ("L", "Leo Castro", "Sequência firme", "+100 dias"), ("M", "Mia Lopes", "Sequência firme", "+90 dias"),
                    ("N", "Nei Kato", "Voltou a treinar", "+70 dias"), ("Z", "Zoe Paz", "Pegou gosto", "+60 dias"),
                    ("E", "Edu Cole", "Começou agora", "+40 dias")], 10.5, passo=0.22, t_rola=11.4)
for e in (hid, lid):
    anim(e, 11.4, {"y": 0}, {"y": -900}, 0.7, "power2.inOut")
    anim(e, 12.1, {"y": -900}, {"y": -990}, 2.07, "none")                                        # segue rolando; as linhas somem na máscara
anim("rk5", 12.85, {"opacity": 1}, {"opacity": 0}, 0.45, "power1.in")                                # some antes de chegar à borda
anim(lid, 11.4, {"filter": "blur(0px)"}, {"filter": "blur(1.5px)"}, 0.35, "power1.in")
anim(lid, 11.75, {"filter": "blur(1.5px)"}, {"filter": "blur(0px)"}, 0.35, "power1.out")
assenta([("Quem", 12.12), ("chega", 12.3), ("lá", 12.42), ("é", 12.6), ("\n", None), ("quem", 12.8), ("não", 12.98), ("falta", 13.4), ("nunca", 13.62)],
        0, 660, w=720, size=36, cor="#e8edf2", cinza="#7d8b98", peso=500, lh=1.25)
SOM("boom", 10.30); SOM("whoosh", 11.75)

# 8 · papel cinza com widgets (faixa) ----------------------------------------------------------------------------------
mundo(14.17, fmt="faixa", fundo="#e6e6e6", nome="widgets", cam=[(14.17, 1.0, 0, 0, 0), (18.0, 1.07, 0, 0, 0)], mao=.6)
a1 = assenta([("Olha", 14.17), ("que", 14.24), ("curioso", 14.46)], 0, 616, w=720, size=40, peso=600)
anim(a1, 15.22, {"y": 0, "scale": 1}, {"y": -150, "scale": .85}, 0.36, "power2.inOut")
pid = pilula_progresso(110, 560, 15.42, 1, 80, 0.66, "sono e alimentação", w=500, ent=("voa", [0, 46, 0, .96], 0.38))
for e in (pid, a1):                                    # empurrão: some (borrado) ANTES de tocar a borda; nunca fica fatiado legível
    anim(e, 16.40, {"x": 0, "filter": "blur(0px)", "scaleX": 1}, {"x": -760, "filter": "blur(12px)", "scaleX": 1.18}, 0.22, "power2.in")
    anim(e, 16.40, {"opacity": 1}, {"opacity": 0}, 0.09, "none")
pv = pilula_no("Sono", 164, 598, 16.5, "verde", size=40, eid="pv")
anim("pv", 16.5, {"x": 340}, {"x": 0}, 0.42, "power3.out")
r1 = risco([(-10, 638), (150, 638)], 16.86, d=0.2, cor="#a9a9a9", esp=2.5)
anim("pv", 17.0, {"y": 0}, {"y": -150}, 0.4, "power2.inOut")
anim(r1, 17.0, {"y": 0}, {"y": -150}, 0.4, "power2.inOut")
risco([(40, 488), (40, 710), (150, 710)], 17.3, d=0.2, cor="#a9a9a9", esp=2.5)      # tronco em L ligando as duas pílulas
pilula_no("Alimentação", 164, 670, 17.36, "vermelho", size=40, eid="pr")
SOM("boom", 15.4); SOM("whoosh", 16.45); SOM("clique", 16.9); SOM("clique", 17.38)

# 9 · conversa (faixa; dissolvência em sequência: o mundo anterior some antes de este aparecer) ---------------------
mundo(18.17, fmt="faixa", fundo="#f3f3f3", entrada=("dissolve", 0.24), nome="conversa",
      cam=[foco(18.05, 1.06, 360, 640), foco(20.23, 1.0, 360, 640)], mao=.6)
conversa(y0=440)
balao([("vem", 18.2), ("do", 18.36), ("descanso", 18.55)], 64, 650, "esq")
digitando(590, 778, 18.3, 18.82)
balao([("que", 18.84), ("você", 18.95), ("faz", 19.1), ("toda", 19.22), ("noite", 19.45)], 590, 790, "dir")
SOM("riser", 19.30)

# 10 · mesa com fita cassete e pílulas que crescem com o texto -------------------------------------------------------
mundo(20.23, nome="mesa-fita", cam=[foco(20.23, 1.04, 360, 640), foco(21.0, 1.13, 380, 600, -1, "power1.inOut"), foco(22.07, 1.22, 390, 590, -2)])
foto(IMG + "mesa-fita.jpg", filtro="contrast(1.06) saturate(.95)")
chip([("Não", 20.24), ("porque", 20.45), ("você", 20.84)], 214, 330, "laranja", eid="c1")
chip([("Treina", 20.98), ("mais", 21.12), ("que", 21.24), ("todos", 21.5)], 224, 425, "branco", eid="c2")
onda(385, 880, 20.6, 22.07, 300)
SOM("boom", 20.10)

# 11 · composer de rede social (faixa; o mundo 10 vira a imagem do post) -----------------------------------------
mundo(22.07, fmt="faixa", fundo="#000", nome="composer", mao=.6,
      cam=[foco(22.07, 1.28, 356, 520), foco(23.0, 1.38, 350, 500, 0, "none"),
           foco(23.27, 2.0, 330, 522, 0, "power2.inOut"), foco(23.5, 2.04, 330, 526, 0, "none"),
           foco(23.78, 2.3, 300, 742, 0, "power2.inOut"), foco(24.06, 2.3, 300, 744, 0, "none"),
           foco(24.36, 2.3, 306, 772, 0, "power2.inOut"), foco(25.16, 2.36, 318, 778, 0, "none"),
           foco(25.46, 1.86, 342, 800, 0, "power2.inOut"), foco(26.4, 1.9, 352, 806, 0, "sine.inOut"), foco(27.23, 1.88, 346, 812, 0, "sine.inOut")])
borrao(23.0, 0.27, 1.6); borrao(23.5, 0.3, 2.2); borrao(24.06, 0.3, 1.2); borrao(25.16, 0.3, 1.2)
C = composer(IMG + "mesa-fita.jpg")
bloco('<div style="padding:10px 26px;border-radius:30px;background:linear-gradient(90deg,#e8452c,#f08a1c);font:500 20px Inter;color:#fff">Não porque você</div>'
      '<div style="margin-top:12px;padding:10px 26px;border-radius:30px;background:#f1f1f1;font:500 20px Inter;color:#666;display:inline-block">Treina mais que todos</div>',
      C["img"][0] + 36, C["img"][1] + 8, z=4)
digita("Mas porque você não para.", 22.15, C["linha"][0], C["linha"][1], t1=23.4, size=22, cor="#ededed", cursor=ACENTO, z=5)
for (cx, cy), nome_ico, t_ in zip(C["campos"], ("pessoa", "doc", "globo"), (23.6, 24.08, 25.18)):
    icone(nome_ico, cx, cy + 2, 20, "#9aa4ad" if nome_ico != "globo" else ACENTO, t=t_)
digita("Então, se você", 23.66, C["campos"][0][0] + 30, C["campos"][0][1], t1=23.98, size=18, cor="#d4d4d4", cursor=ACENTO, z=5)
digita("Só treina quando dá vontade", 24.1, C["campos"][1][0] + 30, C["campos"][1][1], t1=25.1, size=18, cor="#d4d4d4", cursor=ACENTO, z=5)
digita("Em vez de criar uma rotina.", 25.2, C["campos"][2][0] + 30, C["campos"][2][1], t1=26.45, size=17, cor="#9d93ff", cursor=ACENTO, z=5)
anim(C["img_id"], 23.5, {"filter": "sepia(0) saturate(1) brightness(1)"}, {"filter": "sepia(.6) saturate(.6) brightness(.68) contrast(1.05)"}, 0.28, "none")
SOM("boom", 22.0)

# 12 · flatlay com portátil horizontal (gira 360°) -----------------------------------------------------------------
# giro de 360°: para a foto 9:16 cobrir o quadro 9:16 em QUALQUER ângulo a escala tem que ser >= 2,04 (pior caso ~61°);
# a escala só volta ao normal depois que a rotação já está perto de 0°
mundo(27.23, fundo="#eceeeb", nome="flatlay", cam=[foco(27.23, 1.18, 360, 620, -2), foco(28.2, 1.4, 362, 628, -11, "sine.in"),
      (28.38, 2.06, 0, 0, 30, "power1.in"), (28.62, 2.1, 0, 0, 200, "none"), (28.8, 2.06, 0, 0, 340, "none"),
      foco(29.02, 1.2, 364, 575, 354, "power2.out"), foco(30.5, 1.3, 364, 585, 362, "sine.inOut")])
bloco('<div style="width:100%;height:100%;background:#eceeeb repeating-linear-gradient(0deg,transparent 0 28px,#8fc4c0 28px 29.5px),'
      'repeating-linear-gradient(90deg,transparent 0 28px,#8fc4c0 28px 29.5px)"></div>', -1000, -1000, 2720, 3280, z=-2)
foto(IMG + "flatlay2.jpg", filtro="contrast(1.05) saturate(1.04)")
c_ = MUNDOS[-1]["id"] + "c"                                               # borrão do giro: alto enquanto o canto da foto aparece
anim(c_, 28.22, {"filter": "blur(0px)"}, {"filter": "blur(3px)"}, 0.16, "power1.out")
anim(c_, 28.82, {"filter": "blur(3px)"}, {"filter": "blur(0px)"}, 0.2, "power1.in")
CONS = [(267, 531), (486, 586), (450, 727), (233, 670)]          # medido com medir/superficie.py
bloco('<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%,rgba(255,255,255,.18),rgba(0,0,0,.06));'
      'box-shadow:inset 0 0 18px rgba(0,0,0,.22)"></div>', 0, 0, 320, 200, quad=CONS, z=3)
digita("Você tá\njogando o\njogo curto", 27.4, 0, 0, t1=28.15, w=320, h=200, quad=CONS, size=52, font="lcd", cor="#111511", cursor="#111511",
       lh=0.96, extra="padding:24px 0 0;text-align:center;" + LCD, cursor_ate=28.2)
tela_lcd(CONS, 320, 200)
assenta([("Mas", 28.98), ("se", 29.03), ("você", 29.1), ("põe", 29.2)], 142, 330, w=440, size=46, peso=800, alinh="left", cor="#1e1e1e",
        ls=-0.05, extra="mix-blend-mode:multiply", rot=4)
assenta([("rotina", 29.34), ("antes", 29.58)], 256, 380, w=480, size=66, peso=800, alinh="left", cor="#1e1e1e", ls=-0.05, extra="mix-blend-mode:multiply", rot=4)
SOM("boom", 27.70); SOM("whoosh", 28.45)

# 13 · papel cinza: frase pequena ------------------------------------------------------------------------------------
mundo(30.50, fundo="#ececec", nome="papel-final", cam=[(30.5, 1.0, 0, 0, 0), (31.95, 1.18, 0, 0, 0)])
assenta([("o", 30.55), ("resultado", 30.62), ("vem", 30.78), ("sozinho", 30.97, "color:#555")], 0, 566, w=720, size=40, peso=700, ls=-0.04)
SOM("boom", 31.62)

# 14 · busca (vazamento de luz) · layout vertical: tudo cabe; cada enquadramento mostra o texto inteiro ----------------
mundo(31.95, fundo="#f5f6fa", entrada=("flash", 0.3), nome="busca",
      cam=[foco(31.95, 1.45, 300, 600), foco(32.2, 1.45, 300, 600), foco(33.4, 1.45, 345, 600, 0, "none"), foco(33.85, 1.0, 360, 600, 0, "power2.inOut"),
           foco(34.6, 1.08, 360, 800, 0, "power2.inOut"), foco(35.4, 1.12, 360, 830), foco(36.95, 1.16, 360, 880, 0, "sine.inOut")])
borrao(33.35, 0.5, 1.4); borrao(34.0, 0.6, 1.2)
m, bar, (qx, qy) = busca('<span style="color:#1f1f1f">busca</span><span style="color:#0075de">.</span>', y=440)
digita("Plano de treino simples", 32.2, qx, qy, t1=33.4, size=30, peso=400, cor="#222", cursor="#0075de", z=5, cursor_ate=33.9)
ABAS = R("busca_abas")
texto("".join(f'<span style="margin-right:28px;color:{"#1f1f1f;font-weight:600" if k == 0 else "#6b6b6b"}">{a}</span>' for k, a in enumerate(ABAS)),
      100, 662, size=22, peso=400, cor="#222", t=33.95, ent="fade")
bloco('<div style="width:52px;height:52px;border-radius:50%;background:#e9efe9;color:#2fa84f;font:700 26px Inter;text-align:center;line-height:52px">E</div>',
      100, 734, z=4, t=34.35, ent="voa", de=[0, 10, 0, 1], d=0.3)
texto("Exemplo.com", 168, 732, size=30, peso=500, cor="#1a1a1a", t=34.38, ent="voa", de=[0, 10, 0, 1], d=0.3)
texto("exemplo.com", 168, 770, size=21, peso=400, cor="#5f6368", t=34.5, ent="voa", de=[0, 10, 0, 1], d=0.3)
digita('Comenta “PLANO” que\neu te mando', 35.6, 100, 818, t1=36.5, size=44, peso=700, cor="#222", cursor="#222", lh=1.15, z=5)
texto("Um passo a passo simples.<br>Para começar ainda esta semana.", 100, 935, size=23, peso=400, cor="#555", t=36.55, ent="fade", lh=1.4)
