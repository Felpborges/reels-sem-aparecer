#!/usr/bin/env bash
# MOTOR ESTILO D · pipeline na ordem certa. Independente dos motores A, B e C. Rodar de qualquer lugar: ./reel.sh <etapa> [arg]
#   texto                 -> medir/texto.json + atos.json (roteiro em narracao/fala.txt, marcado por ato)
#   voz narracao.mp3      -> tira o silêncio das pontas -> alinha -> põe as PAUSAS na cadência da referência -> realinha -> mede
#                            (gere a voz com o texto de narracao/fala-para-voz.txt; "voz arquivo.mp3 crua" pula o aperto de pausas)
#   indices               -> tabela palavra/índice/tempo (o mapa para escrever cenas.py)
#   conferir-fala         -> transcreve em trechos de 25 s (nenhuma frase sumiu)
#   checar                -> build + lint do HyperFrames
#   quadros t1 t2 ...     -> renderiza o limpo e tira PNGs em renders/q-<t>.png
#   montar                -> checar -> render 10 fps -> efeitos -> mixagem -> película (1080x1920) -> cópia leve -> movimento -> folha
#   rodar <comando…>     -> roda qualquer comando com o Python, o node e o ffmpeg da skill (ex.: ./reel.sh rodar python3 medir/x.py)
set -eo pipefail; cd "$(dirname "$0")"; EU="$(pwd)/$(basename "$0")"
RSA="${REELS_SEM_APARECER:-$(cat .rsa 2>/dev/null || true)}"; [ -f "$RSA/ferramentas/ambiente.sh" ] || RSA="$HOME/.claude/skills/reels-sem-aparecer"
source "$RSA/ferramentas/ambiente.sh" || exit 1   # python3, hyperframes, node, ffmpeg e rubberband da skill; RSA_CHROME, RSA_PERICIA, rsa_conferir_fala
SEP=python3; ALN=python3
NOME=$(python3 -c "import json;print(json.load(open('projeto.json'))['nome'])" | tr -d '\r')
REF=medir/movimento-referencia.json   # assinatura de movimento medida na referência (só números)
case "$1" in
  texto) python3 medir/texto.py narracao/fala.txt ;;
  voz)
    python3 medir/texto.py narracao/fala.txt >/dev/null
    ffmpeg -y -v error -i "$2" -ar 44100 -ac 1 narracao/bruta.wav
    ffmpeg -y -v error -i narracao/bruta.wav -af "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,adelay=60|60" assets/_voz.wav
    alinha() { ffmpeg -y -v error -i "$1" -ar 16000 -ac 1 -c:a pcm_s16le medir/voz16k.wav; $ALN -I medir/alinhar.py medir/voz16k.wav medir/texto.json medir/alinhamento.json 2>/dev/null | tail -1; }
    alinha assets/_voz.wav >/dev/null
    if [ "$3" != "crua" ]; then   # pausas na cadência da referência (2 passadas: a 2ª pega as pausas que o 1º alinhamento errou)
      for i in 1 2; do $SEP -I medir/aperta_pausas.py assets/_voz.wav medir/alinhamento.json assets/_voz_ap.wav; mv assets/_voz_ap.wav assets/_voz.wav; alinha assets/_voz.wav >/dev/null; done
    fi
    ffmpeg -y -v error -i assets/_voz.wav -af "apad=pad_dur=0.6" assets/narracao.wav; rm -f assets/_voz.wav
    alinha assets/narracao.wav
    python3 -c "import json;a=json.load(open('medir/alinhamento.json'));print(len(a),'palavras alinhadas, fala termina em',a[-1]['fim'],'s')"
    $SEP -I medir/voz_medir.py || true ;;
  indices) python3 medir/indices.py ;;
  conferir-fala) rsa_conferir_fala medir/voz16k.wav ;;
  checar)
    python3 build.py
    hyperframes lint . 2>&1 | grep -E "error|✗|◇" | tail -3 ;;
  quadros)
    shift; python3 build.py >/dev/null
    hyperframes render . -o renders/limpo.mp4 --fps 10 --quality high --crf 14 > renders/render.log 2>&1
    for t in "$@"; do ffmpeg -y -v error -ss $t -i renders/limpo.mp4 -frames:v 1 "renders/q-$t.png"; done; ls renders/q-*.png ;;
  montar)
    "$EU" checar
    [ -f assets/sfx/clique.wav ] || $SEP -I medir/sfx_d.py assets/sfx
    $SEP -I mix.py
    python3 build.py >/dev/null
    hyperframes render . -o renders/limpo.mp4 --fps 10 --quality high --crf 12 > renders/render.log 2>&1 || { tail -20 renders/render.log; exit 1; }
    $SEP -I pelicula.py renders/limpo.mp4 assets/mix.m4a "renders/$NOME.mp4" | tail -1
    ffmpeg -y -v error -i "renders/$NOME.mp4" -vf "setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv" -c:v libx264 -crf 23 -preset slow -x264-params colorprim=bt709:transfer=bt709:colormatrix=bt709 -c:a aac -b:a 160k -movflags +faststart "renders/$NOME-compartilhar.mp4"
    python3 "$RSA_PERICIA" "renders/$NOME.mp4" --contra "$REF" 2>&1 | grep -A8 "TESTE DE ACEITE" | tail -6 || true
    $SEP -I medir/folha_video.py "renders/$NOME.mp4" "renders/$NOME-folha" ;;
  rodar) shift; "$@" ;;
  *) sed -n '2,11p' "$EU" ;;
esac
