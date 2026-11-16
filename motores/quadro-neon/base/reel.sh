#!/bin/zsh
# MOTOR ESTILO C · pipeline na ordem certa. Independente dos motores A e B. Rodar de qualquer lugar: ./reel.sh <etapa> [arg]
#   texto fala.txt        -> medir/texto.json + medir/frases.json (roteiro marcado por ato: [gancho] [ponte] [tese] ...)
#   marca <site> <slug>   -> assets/img/print-<slug>.jpg (print real) + logo-<slug>.png (logo oficial)
#   voz narracao.mp3      -> voz CRUA (padrão) -> alinha -> mede (TRATAR=1: tom e cadência do C, reprovado por picotar). A VOZ É ESCOLHIDA NO FIM:
#                            rode com uma voz provisória para montar; quando o Felipe escolher a voz, rode de novo e "montar".
#   conferir-fala         -> transcreve em trechos de 25 s (nenhuma frase sumiu)
#   checar                -> build -> auditoria de cada palavra em cada quadro
#   quadros t1 t2 ...     -> PNGs rápidos do index.html (sem render) em renders/q-<t>.png
#   montar                -> checar + trilha arranjada + mixagem + render + cópia leve + teste de movimento + folha
set -e; setopt pipefail; EU="${0:a}"; cd "${0:a:h}"
RSA="${REELS_SEM_APARECER:-$(cat .rsa 2>/dev/null || true)}"; [ -f "$RSA/ferramentas/ambiente.zsh" ] || RSA="$HOME/.claude/skills/reels-sem-aparecer"
source "$RSA/ferramentas/ambiente.zsh" || exit 1   # python3, hyperframes e node da skill; RSA_CHROME, RSA_PERICIA, rsa_conferir_fala
SEP=python3; ALN=python3
NOME=$(python3 -c "import json;print(json.load(open('projeto.json'))['nome'])")
REF=medir/movimento-referencia.json   # assinatura de movimento medida na referência (só números)
case "$1" in
  texto) python3 medir/texto.py "$2" ;;
  marca) node medir/marca.mjs "$2" "$3" ;;
  voz)
    # PADRÃO (13/11): voz CRUA, como o TTS gerou — só tira o silêncio do começo/fim e alinha. O tratamento de tom e
    # cadência (TRATAR=1) recorta e acelera a fala por pedaços e foi reprovado pelo Felipe ("picada, não fluida").
    ffmpeg -y -v error -i "$2" -ar 44100 -ac 1 narracao/bruta.wav
    if [ "${TRATAR:-0}" = "1" ]; then
      $SEP medir/tom_c.py narracao/bruta.wav narracao/tom.wav ${SEMI:--6} ${FATOR:-0.42}
      ffmpeg -y -v error -i narracao/tom.wav -ar 16000 -ac 1 -c:a pcm_s16le medir/bruta16k.wav
      $ALN medir/alinhar_ctc.py medir/bruta16k.wav medir/texto.json medir/alinhamento_bruto.json 2>&1 | grep -i "palavras" || true
      $SEP medir/ritmo_voz.py narracao/tom.wav medir/alinhamento_bruto.json assets/narracao.wav 2>&1 | grep -v "Using time"
    else
      ffmpeg -y -v error -i narracao/bruta.wav -af "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,adelay=120|120,apad=pad_dur=0.45" assets/narracao.wav
    fi
    ffmpeg -y -v error -i assets/narracao.wav -ar 16000 -ac 1 -c:a pcm_s16le medir/voz16k.wav
    $ALN medir/alinhar_ctc.py medir/voz16k.wav medir/texto.json medir/alinhamento.json 2>&1 | grep -i "palavras" || true
    $SEP medir/voz_medir.py assets/narracao.wav medir/alinhamento.json || true ;;
  conferir-fala) rsa_conferir_fala medir/voz16k.wav ;;
  checar)
    python3 build.py
    node medir/auditoria.mjs 30 2>&1 | tail -1
    python3 medir/auditoria_relatorio.py > medir/auditoria-relatorio.txt || { tail -25 medir/auditoria-relatorio.txt; exit 1; }
    tail -1 medir/auditoria-relatorio.txt ;;
  quadros) shift; python3 build.py >/dev/null; node medir/quadros.mjs renders/q "$@" ;;
  montar)
    "$0" checar
    [ -f assets/sfx/brilho.wav ] || $SEP medir/sfx_c.py assets/sfx
    $SEP mix.py
    python3 build.py >/dev/null
    hyperframes render . -o "renders/$NOME.mp4" -q high > renders/render.log 2>&1 || { tail -20 renders/render.log; exit 1; }
    ffmpeg -y -v error -i "renders/$NOME.mp4" -c:v libx264 -crf 24 -preset slow -c:a aac -b:a 160k -movflags +faststart "renders/$NOME-compartilhar.mp4"
    python3 "$RSA_PERICIA" "renders/$NOME.mp4" --contra "$REF" 2>&1 | grep -A6 "TESTE DE ACEITE" | tail -5
    python3 medir/folha.py "renders/$NOME.mp4" "renders/$NOME-folha" 2 120 10 3 ;;
  *) sed -n '2,10p' "$EU" ;;
esac
