#!/usr/bin/env bash
# MOTOR REEL EDITORIAL · pipeline na ordem certa. Rodar de qualquer lugar: ./reel.sh <etapa> [arg]
#   texto fala.txt        -> medir/texto.json (palavras + pronúncia para o alinhamento)
#   voz narracao.mp3      -> ritmo do original (pausas + 212 palavras/min) + alinhamento palavra a palavra + medição contra as metas
#   conferir-fala         -> transcreve em trechos de 25 s (a transcrição do arquivo inteiro pula frases; em trechos não)
#   checar                -> margens (nenhuma palavra cortada) -> build -> regras de cadência. Para no primeiro erro.
#   montar                -> checar + mixagem + render + cópia leve + teste de movimento contra o original + folha de quadros
set -eo pipefail; cd "$(dirname "$0")"; EU="$(pwd)/$(basename "$0")"
RSA="${REELS_SEM_APARECER:-$(cat .rsa 2>/dev/null || true)}"; [ -f "$RSA/ferramentas/ambiente.sh" ] || RSA="$HOME/.claude/skills/reels-sem-aparecer"
source "$RSA/ferramentas/ambiente.sh" || exit 1   # python3, hyperframes, node, ffmpeg e rubberband da skill; RSA_CHROME, RSA_PERICIA, rsa_conferir_fala
SEP=python3; ALN=python3
NOME=$(python3 -c "import json;print(json.load(open('projeto.json'))['nome'])" | tr -d '\r')
REF=medir/movimento-referencia.json   # assinatura de movimento medida na referência (só números)
case "$1" in
  texto) python3 medir/texto.py "$2" ;;
  voz)
    ffmpeg -y -v error -i "$2" -ar 48000 -ac 1 narracao/bruta.wav
    $SEP medir/ritmo_voz.py narracao/bruta.wav assets/narracao.wav auto
    ffmpeg -y -v error -i assets/narracao.wav -ar 16000 -ac 1 -c:a pcm_s16le medir/voz16k.wav
    $ALN medir/alinhar2.py medir/voz16k.wav medir/texto.json medir/alinhamento.json 2>&1 | grep -i "palavras"
    $SEP medir/voz_medir.py assets/narracao.wav ;;
  conferir-fala) rsa_conferir_fala medir/voz16k.wav ;;
  checar)
    python3 medir/margens.py          # PRIMEIRO: ela regrava o index.html sem câmera para medir; no fim devolve o normal
    python3 build.py
    python3 medir/cadencia.py medir/elementos.json | tail -6 ;;
  montar)
    "$EU" checar
    $SEP mix.py
    python3 build.py >/dev/null       # garante o index.html com a mixagem completa antes do render
    hyperframes render . -o "renders/$NOME.mp4" -q high 2>&1 | grep -iE " error|fail" || true
    ffmpeg -y -v error -i "renders/$NOME.mp4" -c:v libx264 -crf 24 -preset slow -c:a aac -b:a 160k -movflags +faststart "renders/$NOME-compartilhar.mp4"
    python3 "$RSA_PERICIA" "renders/$NOME.mp4" --contra "$REF" 2>&1 | grep -A8 "TESTE DE ACEITE" | tail -6
    $SEP medir/folha.py "renders/$NOME.mp4" "renders/$NOME-folha.jpg" ;;
  *) sed -n '2,8p' "$EU" ;;
esac
