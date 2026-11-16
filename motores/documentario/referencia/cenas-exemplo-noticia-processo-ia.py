"""REEL "Processo para parar a IA" — motor D. As famílias do original (DESMONTE-D §2) na DINÂMICA do original: em média
um corte a cada 1,45 a 1,54 s. Com a voz Lucy na cadência da referência o reel tem ~44,6 s, então são 29 planos (o original
tem 22 em 32 s). Os planos a mais usam as famílias que a referência repete (ARQUIVO, PALAVRAS), a mesma imagem em dois
enquadramentos (planos 17/18 dela) e um segundo uso do título digitado e do objeto no escuro.
SEM MARCA NENHUMA (pedido do Felipe em 14/11/2026: o reel pode entrar numa campanha): nenhum nome de empresa, de produto
ou de pessoa na fala nem na tela, e nenhum logo. As empresas viraram "as cinco principais empresas de inteligência
artificial que você conhece hoje"; os três produtos viraram "texto, imagem e vídeo"; a foto do celular teve apagadas as
reações do feed, que lembravam uma rede social específica.
Fatos checados (13/11/2026): ação de 12/11 na Justiça estadual de São Francisco; 4 ONGs contra 5 empresas de IA; pedem
travar o desenvolvimento/lançamento de modelos mais avançados; o dono de uma delas falou em "civilization destruction"
(2023); nenhum juiz decidiu nada. Voz: Lucy (escolhida pelo Felipe em 13/11/2026). Todos os tempos saem de P(i)."""
import json
from build import *
from moldes import *

BR = json.load(open(os.path.join(AQUI, "medir", "brilhos.json")))


def brilhos_no_enquadre(pontos, e, fx, fy):
    """Os pontos de brilho medidos na imagem inteira, levados para o enquadramento fechado (a mesma conta do molde arquivo)."""
    ix = min(W * e / 2, max(W - W * e / 2, W / 2 + (0.5 - fx) * W * e)); iy = min(H * e / 2, max(H - H * e / 2, H / 2 + (0.5 - fy) * H * e))
    q = [(round(ix + (x - W / 2) * e), round(iy + (y - H / 2) * e)) for x, y in pontos]
    return [(x, y) for x, y in q if 30 < x < W - 30 and 30 < y < H - 30]


# ---------------- [gancho · 5 planos] "Pediram na Justiça pra parar a inteligência artificial mais avançada do mundo. Inclusive a que você usa no celular."
titulo_digitado(0, "PEDIRAM NA JUSTIÇA", [0, 1, 2])

colagem(CORTE(3), [dict(src="assets/img/robo.png", x=440, y=690, w=330, cinza=True, sombra=True),
                   dict(src="assets/img/botao.png", x=200, y=1060, w=230, sombra=True)],          # a ÚNICA cor da colagem
        legenda=dict(txt="pra parar", idx=[3, 4], x=215, y=812, size=41, some_no_punch=True),
        seta_d="M 262 838 C 300 850, 300 884, 246 896", punch_em=P(4) - 0.05, punch_escala=1.8, punch_origem="28% 83%")

pl = plano(CORTE(8), "papel", cam={"tipo": "pan", "x": 175, "x1": -175, "d": 1.9, "ease": "sine.inOut"}, entrada={"tipo": "borrao", "b": 3},
           nome="colagem")
img(pl, "assets/img/multidao.png", 360, 840, 1100, cinza=True, sombra=True)
img(pl, "assets/img/robo.png", 537, 585, 92)                                                    # ela (a IA), pequena, em cor
# medido na referência: 40 px, centros em 192 / 362 / 531 no fim do pan, linha de base 21 px acima da cabeça da figura
for k, (txt, i, x) in enumerate([("mais", 8, 352), ("avançada", 9, 537), ("do mundo", 10, 722)]):
    _, ids = texto(pl, txt, x, 448, 40, "serifa", partes="nada")
    revela([_], [min(P(i), CORTE(8) + .2 * k)])

documento(CORTE(12), "assets/img/processo.jpg", "INCLUSIVE A QUE VOCÊ USA", [12, 13, 14, 15, 16], chave=(3, 4), doc_opac=0.24, doc_borrao=1.6, doc_escala=1.0)

objeto_escuro(CORTE(17), "assets/img/celular.png", "NO CELULAR.", [17, 18], obj_w=250, obj_y=800, txt_y=470)

# ---------------- [contexto · 7 planos] "Quatro ONGs processaram as cinco principais empresas de inteligência artificial que você conhece hoje. Sim, justamente essa que você deve ter aberto agora no seu computador."
arquivo(CORTE(19), "assets/img/ativistas.jpg", cam={"tipo": "afasta", "de": 2.1, "ate": 1.0, "tau": 0.25}, pontos=True,
        filtro="saturate(.8) sepia(.12) brightness(.74) contrast(1.06)",       # escuro como o arquivo da referência: a legenda branca precisa disso
        legenda=dict(txt="4 ONGs", idx=[19, 20], y=860, size=66))
palavras(CORTE(22), [("As Cinco", 22), ("Principais", 24), ("Empresas", 25)])
# o complemento escrito sobre a sala do tribunal (legenda de arquivo, como "During WW2")
arquivo(CORTE(26), "assets/img/tribunal-sala.jpg", cinza=True, filtro="brightness(.62) contrast(1.1)", enquadra=(1.5, 0.5, 0.36),
        cam={"tipo": "afasta", "de": 1.3, "ate": 1.0, "tau": 0.3}, legenda=dict(txt="inteligência artificial", idx=[26, 28], y=640, cps=24))
# quem conhece: o público, em P&B, fechado numa pessoa (a legenda cai sobre a blusa escura)
arquivo(CORTE(30), "assets/img/celulares.jpg", cinza=True, filtro="brightness(.72) contrast(1.08)", enquadra=(1.9, 0.50, 0.80),
        cam={"tipo": "afasta", "de": 1.25, "ate": 1.0, "tau": 0.3}, legenda=dict(txt="que você conhece", idx=[29, 30, 31], y=950, cps=16))
palavras(CORTE(33), [("Sim,", 33), ("Justamente", 34), ("Essa", 35)])
# o corte espera "deve" para o "Essa" ficar 0,6 s na tela (cortando em "que" ele durava 2 quadros)
arquivo(CORTE(38), "assets/img/cta-broll.jpg", enquadra=(1.7, 0.62, 0.50), cam={"tipo": "afasta", "de": 1.15, "ate": 1.0, "tau": 0.3},
        filtro="saturate(.85)")                                                # "deve ter aberto": a pessoa no notebook
objeto_escuro(CORTE(41), "assets/img/laptop.png", "NO SEU COMPUTADOR.", [42, 43, 44], obj_w=430, obj_y=830, txt_y=470)

# ---------------- [feito · 6 planos] "O pedido: travar modelos mais poderosos. O argumento? Um dos próprios donos dessas empresas já disse que a IA pode destruir a civilização."
diagrama(CORTE(45), "assets/img/supercomputador-traco.png", "o pedido:", "Travar Modelos", [45, 46, 47, 48],
         doc_src="assets/img/processo.jpg", desenho=(360, 840, 330), antena=(360, 575), ondas_cfg={"raio": 210, "ang": 30}, titulo_y=330,
         doc_opac=0.12, doc_borrao=2.0)
objeto_escuro(CORTE(49), "assets/img/robo.png", "MAIS PODEROSOS.", [49, 50], obj_w=250, obj_y=830, txt_y=440)
titulo_digitado(CORTE(51), "O ARGUMENTO?", [51, 52])
arquivo(CORTE(53), "assets/img/palco.jpg", cam={"tipo": "afasta", "de": 1.4, "ate": 1.0, "tau": 0.3}, filtro="saturate(.85)",
        legenda=dict(txt="um dos donos", idx=[53, 54, 56], y=955, size=66, cps=20))
arquivo(CORTE(59), "assets/img/palco.jpg", enquadra=(1.75, 0.5, 0.56), cam={"tipo": "afasta", "de": 1.18, "ate": 1.0, "tau": 0.35},
        filtro="saturate(.85) brightness(.9)", legenda=dict(txt="a IA pode", idx=[62, 63, 64], y=730, cps=14))          # sobre o painel escuro do púlpito
cena_cor(CORTE(65), "assets/img/globo.png", "destruir a civilização", [65, 66, 67], t_consequencia=P(67) + 0.1, obj_w=270, obj_x=360,
         obj_y=760, rot_y=610)

# ---------------- [rejeicao · 1 plano, como na referência] "Mas calma: ninguém mandou parar nada."
descarte(CORTE(68), "assets/img/tribunal-sala.jpg", "assets/img/lixeira.png", "assets/img/bola.png", cesto=(360, 800, 330), bola_fim_w=130,
         desenho_src="assets/img/botao.png", desenho_w=420)

# ---------------- [salto · 4 planos] "O juiz ainda não decidiu. Ou seja, amanhã, tudo abre normal: texto, imagem e vídeo."
foto(CORTE(74), "assets/img/martelo.jpg", boom=True, legenda=dict(txt="não decidiu", idx=[77, 78], y=930, cps=16))
anos_rolando(CORTE(79), itens=["hoje", "amanhã"])
palavras(CORTE(82), [("Tudo", 82), ("Abre", 83), ("Normal", 84)])
# os três usos, só em palavras (como "Bluetooth / WiFi / GPS" na referência): sem logo e sem nome de produto
rotulos(CORTE(85), [("Texto", 85), ("Imagem", 86), ("Vídeo", 88)], centro=(360, 640), pos=((217, 492), (222, 600), (277, 707)))

# ---------------- [moral · 3 planos] "Antes, essa briga era na internet. Agora, ela também está no tribunal."
# a mesma foto em dois enquadramentos, o segundo mais fechado (planos 17 e 18 da referência)
arquivo(CORTE(89), "assets/img/maos-celular.jpg", cam={"tipo": "afasta", "de": 1.08, "ate": 1.0, "tau": 0.6}, brilho=dict(pontos=BR["maos"]))
arquivo(CORTE(92), "assets/img/maos-celular.jpg", enquadra=(1.5, 0.5, 0.40), cam={"tipo": "afasta", "de": 1.12, "ate": 1.04, "tau": 0.6},
        brilho=dict(pontos=brilhos_no_enquadre(BR["maos"], 1.5, 0.5, 0.40)), desfoca_fim=0.3)
quadro(CORTE(95), "assets/img/tribunal-pintura.jpg", "assets/img/moldura.png", "agora, ela também\nestá no tribunal.", [95, 96, 97, 98, 99, 100],
       janela=(0.194, 0.188, 0.61, 0.627), mold=(360, 540, 400), leg_y=884)

# ---------------- [cta · 3 planos] "E você, acha que deviam parar? Comenta SIM ou NÃO aqui embaixo."
arquivo(CORTE(101), "assets/img/cta-broll.jpg", cam={"tipo": "afasta", "de": 1.41, "ate": 1.0, "tau": 0.2},
        legenda=dict(txt="E você?", idx=[101, 102], y=800, size=67, cps=16))
cta_icone(CORTE(103), "assets/img/cta-fundo.jpg", "assets/img/icone-parar.png", t_clique=P(106), icone=(360, 640, 120), mao_de=(230, 1040))
cta_campo(CORTE(107), "assets/img/cta-broll.jpg", "SIM ou NÃO", P(108) - 0.1, P(110) + 0.15, y=640)
