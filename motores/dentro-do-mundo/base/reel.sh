#!/usr/bin/env bash
# MOTOR ESTILO B · pipeline na ordem certa. Independente do motor A. Rodar de qualquer lugar: ./reel.sh <etapa> [arg]
#   texto fala.txt        -> medir/texto.json + medir/frases.json (frase-chave marcada com » no roteiro)
#   voz narracao.mp3      -> alinha a voz crua -> tom e cadência do B frase a frase -> realinha -> mede contra o original
#   conferir-fala         -> transcreve em trechos de 25 s (confirma que nenhuma frase sumiu)
#   checar                -> build -> cadência dos mundos -> AUDITORIA de cada palavra em cada quadro. Para no primeiro erro.
#   montar                -> checar + mixagem + render + cópia leve + teste de movimento contra o original + folha de quadros
#   provar <t> <opções…>  -> toca o mesmo trecho com cada efeito candidato (medir/provar_efeitos.py) -> renders/provar-<t>.m4a
#   rodar <comando…>     -> roda qualquer comando com o Python, o node e o ffmpeg da skill (ex.: ./reel.sh rodar python3 medir/x.py)
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
    ffmpeg -y -v error -i "$2" -ar 16000 -ac 1 -c:a pcm_s16le medir/bruta16k.wav
    $ALN medir/alinhar_ctc.py medir/bruta16k.wav medir/texto.json medir/alinhamento_bruto.json 2>&1 | grep -i "palavras"
    $SEP medir/ritmo_voz.py narracao/bruta.wav medir/alinhamento_bruto.json assets/narracao.wav 2>&1 | grep -v "Using time"
    ffmpeg -y -v error -i assets/narracao.wav -ar 16000 -ac 1 -c:a pcm_s16le medir/voz16k.wav
    $ALN medir/alinhar_ctc.py medir/voz16k.wav medir/texto.json medir/alinhamento.json 2>&1 | grep -i "palavras"
    $SEP medir/voz_medir.py assets/narracao.wav medir/alinhamento.json ;;
  conferir-fala) rsa_conferir_fala medir/voz16k.wav ;;
  checar)
    python3 build.py
    python3 medir/cadencia.py medir/elementos.json | tail -22
    node medir/auditoria.mjs 30 2>&1 | tail -1
    python3 medir/auditoria_relatorio.py > medir/auditoria-relatorio.txt || { grep -vE "fora" medir/auditoria-relatorio.txt | tail -40; exit 1; }
    tail -1 medir/auditoria-relatorio.txt ;;
  montar)
    "$EU" checar
    [ -f assets/sfx/clique.wav ] || $SEP medir/sfx_b.py assets/sfx
    [ -f assets/sfx/queda.wav ] || $SEP medir/sfx_ref.py assets/sfx     # kit inicial recriado da referência (refaz whoosh e riser)
    $SEP mix.py
    python3 build.py >/dev/null       # garante o index.html apontando para a mixagem
    hyperframes render . -o "renders/$NOME.mp4" -q high > renders/render.log 2>&1 || { tail -20 renders/render.log; exit 1; }
    ffmpeg -y -v error -i "renders/$NOME.mp4" -c:v libx264 -crf 24 -preset slow -c:a aac -b:a 160k -movflags +faststart "renders/$NOME-compartilhar.mp4"
    python3 "$RSA_PERICIA" "renders/$NOME.mp4" --contra "$REF" 2>&1 | grep -A6 "TESTE DE ACEITE" | tail -5
    $SEP medir/folha.py "renders/$NOME.mp4" "renders/$NOME-folha.jpg" ;;
  provar) shift; $SEP medir/provar_efeitos.py "$@" ;;
  rodar) shift; "$@" ;;
  *) sed -n '2,9p' "$EU" ;;
esac
