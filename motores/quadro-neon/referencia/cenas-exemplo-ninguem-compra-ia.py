# TESTE DO MOTOR C · "Ninguém compra IA" (roteiro em narracao/fala.txt). Voz PROVISÓRIA (Sterling) só para os tempos:
# a voz definitiva é escolhida pelo Felipe no fim (./reel.sh voz <escolhida> && ./reel.sh montar).
IMG = "assets/img/"
CFG = {
    "gancho_img": IMG + "gancho.png",
    "gancho_objeto": [(IMG + "cartao.png", 230, "compra"), (IMG + "chip.png", 175, "ia")],
    "ponte_foto": (IMG + "lampada.png", 230),
    "tese_icone": (["bot", "hand-helping"], [(0.10, -0.22, 0.50), (0, 0.16, 0.95)]),
    "reframe_a": "resultado", "reframe_b": "cobra", "reframe_img": IMG + "trofeu.png", "reframe_img_palavra": "define",
    "marcas": [
        {"nome": "iFood", "logo": IMG + "logo-ifood.png", "print": IMG + "print-ifood.jpg", "logo_pad": 4},
        {"nome": "Nubank", "logo": IMG + "logo-nubank.png", "print": IMG + "print-nubank.jpg", "logo_pad": 0},
        {"nome": "Uber", "logo": IMG + "logo-uber.png", "print": IMG + "print-uber.jpg", "logo_pad": 0},
        {"nome": "Netflix", "logo": IMG + "logo-netflix.png", "print": IMG + "print-netflix.jpg", "logo_pad": 22},
        {"nome": "Airbnb", "logo": IMG + "logo-airbnb.png", "print": IMG + "print-airbnb.jpg", "logo_pad": 0},
    ],
    "tarja": "POR QUE NINGUÉM COMPRA IA",
    "lista_prompt": 3,
    "lista_imgs": [IMG + "item1-espreguicadeira.png", IMG + "item2-aperto.png", IMG + "item3-papel.png",
                   IMG + "item4-travesseiro.png", IMG + "item5-planta.png"],
}
reel_c(CFG)
