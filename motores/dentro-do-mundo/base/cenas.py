# MOTOR ESTILO B · tabela de MUNDOS do reel (modelo). Manual: ~/.claude/skills/reels-sem-aparecer/motores/dentro-do-mundo/MOTOR.md. Exemplos: ~/.claude/skills/reels-sem-aparecer/motores/dentro-do-mundo/referencia/ (catalogo-de-moldes.py e cenas-exemplo-conversa-parada.py)
#
# Uma frase = um mundo. Três famílias em rodízio (nunca a mesma duas vezes seguidas):
#   FOTO-MUNDO   foto(...) gerada no Higgsfield + texto posto NUMA SUPERFÍCIE do mundo (quad=..., digita, chip, risco)
#   TELA DE APP  fmt="faixa" (faixa quadrada 720x710 com barras pretas) + conversa/balao, composer, ranking, busca, pílulas
#   PAPEL        fundo liso "#e6e6e4" (ou preto) + assenta(...) pequeno; respiro entre mundos pesados e para o número
# Regras de tempo (checadas por ./reel.sh checar): o mundo abre 0-0,25 s ANTES da 1ª palavra da frase (use P(i, 0.1));
# mundo de 1,0 a ~5 s; mundo > 3 s tem câmera andando com um evento a cada ~2,5 s; respiro ≥ 0,45 s antes do corte
# (0,15 se terminar digitando); nunca mais de 1,15 s sem novidade; 20-50 % do tempo em faixa.
# P(i) = início da palavra i (medir/alinhamento.json, índice a partir de 0). F(i) = fim da palavra i.
# SOM(tipo, t): efeitos NÃO vão em todo corte (a referência deixa a maioria seco; som repetido em toda virada cansa).
#   Kit inicial (recriado da referência, MOTOR.md §7): "queda" nas viradas da história (~1 a cada 6 cortes), "whoosh" no
#   pico de um movimento rápido de câmera, "riser" + "queda-grave" no corte mais importante, "clique"/"pop"/"tecla" nas telas.
#   É ponto de partida, não regra: teste outros sons em cada parte com ./reel.sh provar <t> nada queda whoosh outro.wav
# TRILHA(t, -12) esvazia a trilha na virada antes do CTA; TRILHA(t2, 0) volta no CTA.
IMG = "assets/img/"

# 1 · gancho: foto-mundo com o texto escrito numa superfície ------------------------------------------------------
# mundo(0.0, nome="gancho", cam=[foco(0.0, 1.0, 360, 640), foco(P(5), 1.12, 360, 600, 0, "power1.in")])
# foto(IMG + "mesa.jpg")
# PAPEL = [(365, 405), (665, 545), (395, 915), (70, 735)]           # cantos da superfície na foto (TL, TR, BR, BL)
# texto("palavra", 0, 0, w=340, h=500, quad=PAPEL, font="mao", size=56, t=P(0), ent="blur")

# 2 · tela de app na faixa -------------------------------------------------------------------------------------------
# mundo(P(6, 0.1), fmt="faixa", fundo="#f3f3f3", nome="conversa", cam=[foco(P(6, 0.1), 1.05, 360, 640), foco(P(12), 1.0, 340, 660)])
# conversa("Mensagem", "Hoje, 19:30", y0=440)
# balao([("primeira", P(6)), ("frase", P(7))], 40, 650, "esq")

# 3 · papel cinético ---------------------------------------------------------------------------------------------------
# mundo(P(13, 0.1), fundo="#e6e6e4", nome="papel", cam=[(P(13, 0.1), 1.0, 0, 0, 0), (P(17), 1.3, 0, 0, 0)])
# borda_filme()
# assenta([("frase", P(13)), ("que", P(14)), ("assenta", P(15))], 0, 616, w=720, size=40, peso=600)
