#!/bin/zsh
# REELS SEM APARECER · diagnóstico: o que está pronto e o que falta neste computador.
# uso: zsh diagnostico.sh            -> lista com ✓ / ✗ e, no fim, PRONTO ou o que fazer
# Sai com 0 quando dá para produzir um reel; 1 quando falta algo essencial.
RSA="${0:a:h:h}"
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
FALTA=0; AVISO=0
ok()    { print -r -- "  ✓ $1"; }
falta() { print -r -- "  ✗ $1"; FALTA=$((FALTA + 1)); }
aviso() { print -r -- "  ! $1"; AVISO=$((AVISO + 1)); }

print "Reels sem aparecer · diagnóstico"
print -r -- "  pasta da skill: $RSA"

[ "$(uname)" = "Darwin" ] && ok "macOS $(sw_vers -productVersion 2>/dev/null) ($(uname -m))" || falta "este instalador só cobre macOS (aqui: $(uname))"

for t in ffmpeg ffprobe node rubberband; do
  command -v $t >/dev/null && ok "$t" || falta "$t não encontrado (o instalar.sh instala pelo Homebrew)"
done

PY="$RSA/.venv/bin/python"
if [ -x "$PY" ]; then
  ok "ambiente Python da skill ($("$PY" -V 2>&1))"
  "$PY" - <<'E' 2>/dev/null && ok "pacotes de áudio, imagem e alinhamento" || falta "pacotes Python incompletos (rode o instalar.sh de novo)"
import torch, torchaudio, demucs, transformers, librosa, soundfile, scipy, numpy, PIL, cv2, rembg, parselmouth, fontTools
E
  "$PY" - <<'E' 2>/dev/null && ok "modelo de alinhamento palavra a palavra (português)" || falta "modelo de alinhamento ainda não baixado (rode o instalar.sh de novo)"
import os
os.environ["HF_HUB_OFFLINE"] = "1"
from huggingface_hub import snapshot_download
snapshot_download("jonatasgrosman/wav2vec2-large-xlsr-53-portuguese", allow_patterns=["*.json", "*.txt", "*.bin", "*.safetensors"])
E
else
  falta "ambiente Python da skill ainda não foi criado (rode o instalar.sh)"
fi

HFB="$RSA/ferramentas/node_modules/.bin/hyperframes"
if [ -x "$HFB" ]; then
  ok "HyperFrames $("$HFB" --version 2>/dev/null | head -1)"
  "$HFB" browser path >/dev/null 2>&1 && ok "navegador de renderização do HyperFrames" || falta "navegador do HyperFrames não baixado (rode o instalar.sh de novo)"
else
  falta "HyperFrames não instalado na skill (rode o instalar.sh)"
fi

CH=""
for c in "/Applications/Google Chrome.app" "/Applications/Chromium.app" "/Applications/Microsoft Edge.app" "/Applications/Brave Browser.app"; do
  [ -d "$c" ] && { CH="$c"; break; }
done
[ -n "$CH" ] && ok "navegador para as conferências de texto (${CH:t:r})" \
  || aviso "sem Google Chrome: os motores editorial, dentro do mundo e quadro neon usam o Chrome para conferir se nenhum texto sai da tela. Instale o Google Chrome."

F="$RSA/motores/documentario/base/assets/fonts"
[ -f "$F/HelveticaNeue.ttf" ] && [ -f "$F/HelveticaNeue-Bold.ttf" ] && [ -f "$F/HoeflerText-Italic.ttf" ] \
  && ok "fontes do motor documentário (tiradas deste macOS)" \
  || aviso "fontes do motor documentário ainda não extraídas (rode o instalar.sh; os outros três motores não dependem delas)"

W=""; for w in "$RSA/modelos/ggml-large-v3-turbo-q5_0.bin" "$RSA/modelos/ggml-large-v3-turbo.bin" "$HOME/.cache/whisper-cpp/ggml-large-v3-turbo.bin"; do [ -f "$w" ] && { W="$w"; break; }; done
if command -v whisper-cli >/dev/null && [ -n "$W" ]; then ok "transcritor para conferir a narração (whisper)"
else aviso "transcritor (whisper) ausente: a etapa 'conferir-fala' é pulada. Para ligar: zsh \"$RSA/instalar.sh\" --com-whisper"; fi

LIVRE=$(df -g "$HOME" 2>/dev/null | awk 'NR==2 {print $4}')
[ -n "$LIVRE" ] && { (( LIVRE >= 3 )) && ok "espaço livre: ${LIVRE} GB" || aviso "pouco espaço livre (${LIVRE} GB): cada reel ocupa de 200 a 500 MB enquanto é produzido"; }

print
if (( FALTA == 0 )); then
  print "PRONTO: dá para produzir reels neste computador.$( (( AVISO > 0 )) && print " ($AVISO aviso(s) acima)")"
  print "Falta só conferir, dentro do Claude Code, se o Higgsfield está conectado (voz, imagens e trilha saem de lá)."
  exit 0
fi
print "FALTAM $FALTA item(ns) essencial(is). Rode:  zsh \"$RSA/instalar.sh\""
exit 1
