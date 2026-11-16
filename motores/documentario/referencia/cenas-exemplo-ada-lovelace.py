"""TESTE DO MOTOR D — "A primeira programadora" (Ada Lovelace). Mesma sequência de famílias do original (DESMONTE-D §2),
tema 100 % novo. Índices = ./reel.sh indices. Voz PROVISÓRIA (Helena, ElevenLabs v4): todos os tempos saem de P(i)."""
import json
from build import *
from moldes import *

# pontos de brilho do retrato (específicos deste reel). Para rodar o exemplo, copie
# referencia/brilhos-retrato-exemplo-ada-lovelace.json para medir/brilhos-retrato.json do projeto.
BR = json.load(open(os.path.join(AQUI, "medir", "brilhos-retrato.json")))

# ---------------- [gancho] "Todo mundo lembra do pai dela. Quase ninguém sabe que ela escreveu o primeiro programa de computador da história."
titulo_digitado(0, "TODO MUNDO", [0, 1])

colagem(CORTE(2), [dict(src="assets/img/livros.png", x=250, y=1080, w=330, sombra=True),            # a ÚNICA cor da colagem
                   dict(src="assets/img/byron.png", x=430, y=720, w=300, cinza=True, sombra=True)],
        legenda=dict(txt="o pai dela", idx=[3, 4, 5], x=300, y=250, size=34, some_no_punch=True),
        seta_d="M 300 270 C 318 302, 368 320, 420 322", punch_em=P(4) - 0.1, punch_escala=1.8, punch_origem="60% 24%")

pl = plano(CORTE(6), "papel", cam={"tipo": "pan", "x": 175, "x1": -175, "d": 1.5, "ease": "sine.inOut"}, saida={"tipo": "borrao", "d": 0.1, "b": 7},
           nome="colagem")
img(pl, "assets/img/multidao.png", 360, 840, 1100, cinza=True, sombra=True)
img(pl, "assets/img/ada-azul.png", 360, 630, 96)                                                       # ela, pequena, em cor
for txt, i, x in [("quase", 6, 230), ("ninguém", 7, 360), ("sabe", 8, 490)]:
    _, ids = texto(pl, txt, x, 505, 24, "serifa")
    revela(ids, [max(CORTE(6) + .1, min(P(i), CORTE(6) + .1 + .25 * k)) for k in range(len(ids))])

documento(CORTE(10), "assets/img/manuscrito.jpg", "ELA ESCREVEU O PRIMEIRO PROGRAMA", [10, 11, 12, 13, 14], chave=(4, 4))

objeto_escuro(CORTE(15), "assets/img/computador.png", "DE COMPUTADOR DA HISTÓRIA.", [15, 16, 17, 18], obj_w=470, obj_y=800, txt_y=500)

# ---------------- [contexto] "No século dezenove, Ada Lovelace não estava só traduzindo um artigo."
arquivo(CORTE(19), "assets/img/londres.jpg", cam={"tipo": "afasta", "de": 2.1, "ate": 1.0, "tau": 0.25}, pontos=True,
        filtro="saturate(.75) sepia(.15)", legenda=dict(txt="Século XIX", idx=[20, 21], y=654, size=44))
arquivo(CORTE(22), "assets/img/ada-retrato.jpg", cinza=True, cam={"tipo": "afasta", "de": 1.12, "ate": 1.0, "tau": 0.8})
palavras(CORTE(24), [("não", 24), ("estava", 25), ("só", 26), ("traduzindo", 27), ("um", 28), ("artigo", 29)])

# ---------------- [feito] "Ela escreveu um algoritmo para uma máquina que ainda nem existia."
diagrama(CORTE(30), "assets/img/maquina-traco.png", "escreveu um", "Algoritmo", [31, 32, 33], doc_src="assets/img/manuscrito.jpg",
         desenho=(360, 830, 380), antena=(360, 560), ondas_cfg={"raio": 210, "ang": 30}, titulo_y=330)
arquivo(CORTE(34), "assets/img/pena.jpg", cam={"tipo": "deriva", "de": 1.0, "ate": 1.04}, filtro="saturate(.8)")
cena_cor(CORTE(37), "assets/img/engrenagens.png", "ainda nem existia", [38, 39, 40], t_consequencia=P(40) + 0.1, obj_w=150, obj_x=360,
         obj_y=760, rot_y=520)

# ---------------- [rejeicao] "A máquina nunca foi construída."
descarte(CORTE(41), "assets/img/escritorio.jpg", "assets/img/lixeira.png", "assets/img/bola.png", cesto=(360, 800, 330), bola_fim_w=130,
         desenho_src="assets/img/maquina-traco.png", desenho_w=560)

# ---------------- [salto] "Cem anos depois, a mesma ideia virou a base de computadores, aplicativos e inteligência artificial."
anos_rolando(CORTE(46), 1843, 1943)
foto(CORTE(49), "assets/img/lousa.jpg", boom=True)
palavras(CORTE(52), [("virou", 52), ("a", 53), ("base", 54), ("de", 55)])
rotulos(CORTE(56), [("Computadores", 56), ("Aplicativos", 57), ("IA", 59)], centro=(360, 640), pos=((217, 492), (222, 600), (277, 707)))

# ---------------- [moral] "O mundo lembrou dela como filha de um poeta, mas a história lembra dela como a primeira programadora."
arquivo(CORTE(61), "assets/img/ada-retrato.jpg", cam={"tipo": "afasta", "de": 1.06, "ate": 1.0, "tau": 0.6}, brilho=dict(pontos=BR[:14]))
arquivo(CORTE(65), "assets/img/ada-retrato.jpg", cam={"tipo": "afasta", "de": 1.62, "ate": 1.5, "tau": 0.6, "origem": "52% 34%"},
        brilho=dict(pontos=BR[:14]), desfoca_fim=0.3)
quadro(CORTE(70), "assets/img/ada-retrato.jpg", "assets/img/moldura.png", "a história lembra dela\ncomo a primeira programadora.",
       list(range(71, 79)), janela=(0.194, 0.188, 0.61, 0.627), mold=(360, 560, 400), leg_y=905)

# ---------------- [cta] "Se você quer criar programas com IA sem saber programar, comenta ADA aqui embaixo."
arquivo(CORTE(80), "assets/img/cta-broll.jpg", cam={"tipo": "afasta", "de": 1.41, "ate": 1.0, "tau": 0.2},
        legenda=dict(txt="Você", idx=[80], y=632, size=60))
cta_icone(CORTE(82), "assets/img/cta-fundo.jpg", "assets/img/icone-ia.png", t_clique=P(85), icone=(360, 640, 120), mao_de=(230, 1040))
palavras(CORTE(86), [("sem", 86), ("saber", 87), ("programar", 88)])
cta_campo(CORTE(89), "assets/img/cta-broll.jpg", "ADA", P(90), P(90) + 0.3, y=640, w=400, size=32)
