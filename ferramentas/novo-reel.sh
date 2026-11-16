#!/usr/bin/env bash
# REELS SEM APARECER · cria a pasta de um reel novo a partir de um motor.
#   bash novo-reel.sh <motor> <pasta-do-reel> <fala.txt> "<título>" [nome-do-arquivo]
# <motor>: editorial · dentro-do-mundo · quadro-neon · documentario   (aceita também: neon, mundo, doc, A, B, C, D)
# A pasta não pode existir ainda. O roteiro (fala.txt) segue o formato do motor escolhido (seção de roteiro do MOTOR.md).
set -e
RSA="$(cd "$(dirname "$0")/.." && pwd)"
[ $# -ge 4 ] || { sed -n '2,5p' "$0"; exit 2; }
case "$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')" in
  editorial|a|motor-a) M=editorial ;;
  dentro-do-mundo|dentro|mundo|b|motor-b) M=dentro-do-mundo ;;
  quadro-neon|neon|quadro|c|motor-c) M=quadro-neon ;;
  documentario|documentário|doc|d|motor-d) M=documentario ;;
  *) echo "motor desconhecido: $1  (use editorial, dentro-do-mundo, quadro-neon ou documentario)"; exit 2 ;;
esac
PY="$RSA/.venv/bin/python"; [ -x "$PY" ] || PY="$RSA/.venv/Scripts/python.exe"
[ -x "$PY" ] || { echo "A skill ainda não foi instalada por completo. Rode:  bash \"$RSA/instalar.sh\""; exit 1; }
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
if [ "$M" = documentario ] && [ ! -f "$RSA/motores/documentario/base/assets/fonts/HoeflerText-Italic.ttf" ]; then
  "$PY" "$RSA/ferramentas/fontes-do-sistema.py" || { echo "Sem as fontes do sistema o motor documentário não roda neste computador."; exit 1; }
fi
shift
"$PY" "$RSA/motores/$M/novo_reel.py" "$@"
echo "motor: $M · manual: $RSA/motores/$M/MOTOR.md"
