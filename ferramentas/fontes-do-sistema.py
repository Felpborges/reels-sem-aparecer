#!/usr/bin/env python3
"""Motor DOCUMENTÁRIO · tira do próprio macOS as três fontes que o estilo usa (Helvetica Neue, Helvetica Neue Bold e
Hoefler Text Italic) e grava em motores/documentario/base/assets/fonts/.

Essas fontes são da Apple e vêm instaladas em todo Mac, mas não podem ser distribuídas junto com a skill. Por isso a
skill não as carrega: cada computador extrai as suas. Rodado pelo instalar.sh; pode rodar de novo sem problema.

uso: python fontes-do-sistema.py            (grava as três; sai com 1 se alguma não foi encontrada)
"""
import os
import sys

AQ = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(AQ, "..", "motores", "documentario", "base", "assets", "fonts")
QUERO = {  # nome PostScript -> arquivo que o motor espera
    "HelveticaNeue": "HelveticaNeue.ttf",
    "HelveticaNeue-Bold": "HelveticaNeue-Bold.ttf",
    "HoeflerText-Italic": "HoeflerText-Italic.ttf",
}
COLECOES = [
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Supplemental/Hoefler Text.ttc",
    "/Library/Fonts/Hoefler Text.ttc",
]


def main():
    try:
        from fontTools.ttLib import TTCollection
    except ImportError:
        sys.exit("fontes-do-sistema: falta o pacote fonttools (rode o instalar.sh da skill).")
    os.makedirs(DEST, exist_ok=True)
    achadas = set()
    for caminho in COLECOES:
        if not os.path.exists(caminho):
            continue
        for fonte in TTCollection(caminho).fonts:
            ps = fonte["name"].getDebugName(6)
            if ps in QUERO and ps not in achadas:
                fonte.save(os.path.join(DEST, QUERO[ps]))
                achadas.add(ps)
    faltam = sorted(set(QUERO) - achadas)
    for ps in sorted(achadas):
        print("  fonte do sistema pronta: %s" % QUERO[ps])
    if faltam:
        print("  NÃO ENCONTRADAS neste computador: %s" % ", ".join(faltam))
        print("  O motor documentário precisa delas (vêm com o macOS). Os outros três motores funcionam sem elas.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
