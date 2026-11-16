#!/bin/zsh
# REELS SEM APARECER · cria a pasta de um reel novo a partir de um motor.
#   zsh novo-reel.sh <motor> <pasta-do-reel> <fala.txt> "<título>" [nome-do-arquivo]
# <motor>: editorial · dentro-do-mundo · quadro-neon · documentario   (aceita também: neon, mundo, doc, A, B, C, D)
# A pasta não pode existir ainda. O roteiro (fala.txt) segue o formato do motor escolhido (seção de roteiro do MOTOR.md).
set -e
RSA="${0:a:h:h}"
[ $# -ge 4 ] || { sed -n '2,5p' "$0"; exit 2; }
case "${1:l}" in
  editorial|a|motor-a) M=editorial ;;
  dentro-do-mundo|dentro|mundo|b|motor-b) M=dentro-do-mundo ;;
  quadro-neon|neon|quadro|c|motor-c) M=quadro-neon ;;
  documentario|documentário|doc|d|motor-d) M=documentario ;;
  *) print "motor desconhecido: $1  (use editorial, dentro-do-mundo, quadro-neon ou documentario)"; exit 2 ;;
esac
[ -x "$RSA/.venv/bin/python" ] || { print "A skill ainda não foi instalada por completo. Rode:  zsh \"$RSA/instalar.sh\""; exit 1; }
if [ "$M" = documentario ] && [ ! -f "$RSA/motores/documentario/base/assets/fonts/HoeflerText-Italic.ttf" ]; then
  "$RSA/.venv/bin/python" "$RSA/ferramentas/fontes-do-sistema.py" || { print "Sem as fontes do sistema o motor documentário não roda neste computador."; exit 1; }
fi
shift
"$RSA/.venv/bin/python" "$RSA/motores/$M/novo_reel.py" "$@"
print "motor: $M · manual: $RSA/motores/$M/MOTOR.md"
