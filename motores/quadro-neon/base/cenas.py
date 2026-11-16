# MOTOR ESTILO C · configuração do reel (modelo). Manual: ~/.claude/skills/reels-sem-aparecer/motores/quadro-neon/MOTOR.md (exemplos em ~/.claude/skills/reels-sem-aparecer/motores/quadro-neon/referencia/). O roteiro (narracao/fala.txt) é marcado por ATO;
# moldes.py monta cada ato com as regras medidas no original. Aqui só entram as escolhas do reel:
#   imagens (Higgsfield, recorte com fundo transparente), ícone da tese (Lucide), as palavras-herói do reframe,
#   as marcas da prova (logo OFICIAL + print REAL: ./reel.sh marca <site> <slug>) e o texto da tarja.
IMG = "assets/img/"
CFG = {
    "gancho_img": IMG + "gancho.png",            # colagem: obra clássica/estátua "atualizada", P&B, recortada (entra pela direita)
    "gancho_img_pos": None,                      # None = medido (760 px de altura, borda direita em 556) ou (x, y, largura)
    "gancho_objeto": [(IMG + "objeto.png", 180, "compra")],   # objetos recortados do gancho, cada um na sua palavra:
                                                 #   o 1º sobe por baixo do título; os outros pipocam ao lado da linha da palavra
    "ponte_foto": None,                          # (src, largura): foto que pipoca embaixo da frase da ponte (punch no começo)
    "tese_icone": (["shield-check", "hand-helping"], [(0.10, -0.20, 0.52), (0, 0.16, 0.95)]),   # ícones Lucide em assets/icones/
    "tese_palavra": None,                        # palavra que vira "<manuscrita>" (padrão: a última da frase da tese)
    "reframe_a": "palavra",                      # herói amarelo de cima (uma palavra da frase do reframe)
    "reframe_b": "palavra",                      # herói branco de baixo (a consequência), ligado pelo arco tracejado
    "reframe_img": IMG + "produto.png",          # foto recortada do meio (pop)
    "reframe_img_palavra": None,                 # palavra em que a foto entra (padrão: 2 palavras depois do herói A)
    "marcas": [                                  # uma por frase da [prova], na ordem
        # {"nome": "Marca", "logo": IMG + "logo-marca.png", "print": IMG + "print-marca.jpg"},
    ],
    "tarja": "TÍTULO-SÍNTESE",                   # o adesivo amarelo (a frase da [sintese] resumida, ≤ 26 letras)
    "lista_prompt": 3,                           # quantas palavras da [lista] formam o ">prompt" antes dos itens
    "lista_imgs": None,                          # [foto recortada por item da lista] (opcional; dá dinâmica: entra/sai com o item)
}
reel_c(CFG)
