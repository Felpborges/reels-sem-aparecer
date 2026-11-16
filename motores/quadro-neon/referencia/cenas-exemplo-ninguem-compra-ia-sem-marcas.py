# TESTE DO MOTOR C · "Ninguém compra IA" (roteiro em narracao/fala.txt; a versão com marcas está em fala-com-marcas.txt). Voz PROVISÓRIA (Sterling) só para os tempos:
# a voz definitiva é escolhida pelo Felipe no fim (./reel.sh voz <escolhida> && ./reel.sh montar).
IMG = "assets/img/"
CFG = {
    "gancho_img": IMG + "gancho.png",
    "gancho_objeto": [(IMG + "cartao.png", 230, "compra"), (IMG + "chip.png", 175, "ia")],
    "ponte_foto": (IMG + "lampada.png", 230),
    "tese_icone": (["bot", "hand-helping"], [(0.10, -0.22, 0.50), (0, 0.16, 0.95)]),
    "reframe_a": "resultado", "reframe_b": "cobra", "reframe_img": IMG + "trofeu.png", "reframe_img_palavra": "define",
    # ESTE REEL NÃO PODE MOSTRAR MARCAS (pedido do Felipe, 13/11; só aqui, não no motor): a fala cita o SETOR,
    # o nome no cartão vira o setor e o logo e o print entram embaçados.
    "marcas": [
        {"nome": "Delivery", "logo": IMG + "logo-ifood.png", "print": IMG + "print-ifood.jpg", "logo_pad": 4, "logo_desfoque": 16, "print_desfoque": 12},
        {"nome": "Banco digital", "logo": IMG + "logo-nubank.png", "print": IMG + "print-nubank.jpg", "logo_pad": 0, "logo_desfoque": 16, "print_desfoque": 12},
        {"nome": "App de corrida", "logo": IMG + "logo-uber.png", "print": IMG + "print-uber.jpg", "logo_pad": 0, "logo_desfoque": 16, "print_desfoque": 12},
        {"nome": "Streaming", "logo": IMG + "logo-netflix.png", "print": IMG + "print-netflix.jpg", "logo_pad": 22, "logo_desfoque": 16, "print_desfoque": 12},
        {"nome": "Aluguel", "logo": IMG + "logo-airbnb.png", "print": IMG + "print-airbnb.jpg", "logo_pad": 0, "logo_desfoque": 16, "print_desfoque": 12},
    ],
    "tarja": "POR QUE NINGUÉM COMPRA IA",
    "lista_prompt": 3,
    "lista_imgs": [IMG + "item1-espreguicadeira.png", IMG + "item2-aperto.png", IMG + "item3-papel.png",
                   IMG + "item4-travesseiro.png", IMG + "item5-planta.png"],
}
reel_c(CFG)
