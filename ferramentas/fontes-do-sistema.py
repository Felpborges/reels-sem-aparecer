#!/usr/bin/env python3
"""Motor DOCUMENTÁRIO · põe em motores/documentario/base/assets/fonts/ as três fontes que o estilo usa, tiradas do
próprio computador (não podem ser distribuídas junto com a skill).

  macOS:   Helvetica Neue, Helvetica Neue Bold e Hoefler Text Italic (as do estilo original).
  Windows: as equivalentes que todo Windows tem: Arial, Arial Bold e Palatino Linotype Italic (ou Georgia Italic).
           O desenho das letras muda um pouco em relação ao Mac; a diagramação é a mesma.

Rodado pelo instalar.sh; pode rodar de novo sem problema.
uso: python fontes-do-sistema.py            (grava as três; sai com 1 se alguma não foi encontrada)
"""
import os
import shutil
import sys

AQ = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(AQ, "..", "motores", "documentario", "base", "assets", "fonts")
QUERO = {  # nome PostScript no macOS -> arquivo que o motor espera
    "HelveticaNeue": "HelveticaNeue.ttf",
    "HelveticaNeue-Bold": "HelveticaNeue-Bold.ttf",
    "HoeflerText-Italic": "HoeflerText-Italic.ttf",
}
COLECOES = [
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Supplemental/Hoefler Text.ttc",
    "/Library/Fonts/Hoefler Text.ttc",
]
EQUIVALENTES = {  # arquivo que o motor espera -> candidatas, na ordem de preferência (Windows e Linux)
    "HelveticaNeue.ttf": ["arial.ttf", "LiberationSans-Regular.ttf", "DejaVuSans.ttf"],
    "HelveticaNeue-Bold.ttf": ["arialbd.ttf", "LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"],
    "HoeflerText-Italic.ttf": ["palai.ttf", "georgiai.ttf", "timesi.ttf", "LiberationSerif-Italic.ttf", "DejaVuSerif-Italic.ttf"],
}


def do_mac():
    from fontTools.ttLib import TTCollection
    achadas = {}
    for caminho in COLECOES:
        if not os.path.exists(caminho):
            continue
        for fonte in TTCollection(caminho).fonts:
            ps = fonte["name"].getDebugName(6)
            if ps in QUERO and QUERO[ps] not in achadas:
                fonte.save(os.path.join(DEST, QUERO[ps]))
                achadas[QUERO[ps]] = ps
    return achadas


def de_equivalentes():
    pastas = [os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
              os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"),
              "/usr/share/fonts", "/usr/local/share/fonts", os.path.expanduser("~/.fonts")]
    indice = {}
    for pasta in pastas:
        if not pasta or not os.path.isdir(pasta):
            continue
        for raiz, _, arquivos in os.walk(pasta):
            for a in arquivos:
                indice.setdefault(a.lower(), os.path.join(raiz, a))
    achadas = {}
    for alvo, candidatas in EQUIVALENTES.items():
        for c in candidatas:
            if c.lower() in indice:
                shutil.copyfile(indice[c.lower()], os.path.join(DEST, alvo))
                achadas[alvo] = c
                break
    return achadas


def main():
    os.makedirs(DEST, exist_ok=True)
    if sys.platform == "darwin":
        try:
            achadas = do_mac()
        except ImportError:
            sys.exit("fontes-do-sistema: falta o pacote fonttools (rode o instalar.sh da skill).")
    else:
        achadas = de_equivalentes()
    for alvo in sorted(achadas):
        print("  fonte do sistema pronta: %s (de %s)" % (alvo, achadas[alvo]))
    faltam = sorted(set(QUERO.values()) - set(achadas))
    if faltam:
        print("  NÃO ENCONTRADAS neste computador: %s" % ", ".join(faltam))
        print("  O motor documentário precisa delas. Os outros três motores funcionam sem elas.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
