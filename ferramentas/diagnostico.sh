#!/usr/bin/env bash
# REELS SEM APARECER · diagnóstico: o que está pronto e o que falta neste computador (macOS e Windows).
# uso: bash diagnostico.sh            -> lista com ✓ / ✗ e, no fim, PRONTO ou o que fazer
# Sai com 0 quando dá para produzir um reel; 1 quando falta algo essencial.
RSA="$(cd "$(dirname "$0")/.." && pwd)"
case "$(uname -s)" in
  Darwin) OS=mac ;;
  MINGW*|MSYS*|CYGWIN*) OS=windows ;;
  *) OS=outro ;;
esac
if [ "$OS" = windows ]; then
  export PATH="$RSA/ferramentas/bin:$RSA/ferramentas/bin/node:$PATH"; PY="$RSA/.venv/Scripts/python.exe"
else
  export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"; PY="$RSA/.venv/bin/python"
fi
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
FALTA=0; AVISO=0
ok()    { printf '  ✓ %s\n' "$1"; }
falta() { printf '  ✗ %s\n' "$1"; FALTA=$((FALTA + 1)); }
aviso() { printf '  ! %s\n' "$1"; AVISO=$((AVISO + 1)); }

echo "Reels sem aparecer · diagnóstico"
echo "  pasta da skill: $RSA"

case "$OS" in
  mac) ok "macOS $(sw_vers -productVersion 2>/dev/null) ($(uname -m))" ;;
  windows) ok "Windows ($(uname -m)), pelo Git Bash" ;;
  *) falta "a skill só cobre macOS e Windows (aqui: $(uname -s))" ;;
esac

for t in ffmpeg ffprobe node rubberband; do
  if command -v $t >/dev/null 2>&1; then ok "$t"; else falta "$t não encontrado (o instalar.sh instala)"; fi
done

if [ -f "$PY" ]; then
  ok "ambiente Python da skill ($("$PY" -V 2>&1 | tr -d '\r'))"
  if "$PY" - <<'E' 2>/dev/null
import torch, torchaudio, demucs, transformers, librosa, soundfile, scipy, numpy, PIL, cv2, rembg, parselmouth, fontTools
E
  then ok "pacotes de áudio, imagem e alinhamento"; else falta "pacotes Python incompletos (rode o instalar.sh de novo)"; fi
  if "$PY" - <<'E' 2>/dev/null
import os
os.environ["HF_HUB_OFFLINE"] = "1"
from huggingface_hub import snapshot_download
snapshot_download("jonatasgrosman/wav2vec2-large-xlsr-53-portuguese", allow_patterns=["*.json", "*.txt", "*.bin", "*.safetensors"])
E
  then ok "modelo de alinhamento palavra a palavra (português)"; else falta "modelo de alinhamento ainda não baixado (rode o instalar.sh de novo)"; fi
else
  falta "ambiente Python da skill ainda não foi criado (rode o instalar.sh)"
fi

HFB="$RSA/ferramentas/node_modules/.bin/hyperframes"
if [ -e "$HFB" ]; then
  ok "HyperFrames $("$HFB" --version 2>/dev/null | head -1 | tr -d '\r')"
  if "$HFB" browser path >/dev/null 2>&1; then ok "navegador de renderização do HyperFrames"; else falta "navegador do HyperFrames não baixado (rode o instalar.sh de novo)"; fi
else
  falta "HyperFrames não instalado na skill (rode o instalar.sh)"
fi

CH=""
if [ "$OS" = windows ]; then
  PF="$(cygpath -m "${PROGRAMFILES:-C:/Program Files}")"; PF86="$(cygpath -m "${PROGRAMFILES_X86:-C:/Program Files (x86)}")"; LA="$(cygpath -m "${LOCALAPPDATA:-$HOME/AppData/Local}")"
  for c in "$PF/Google/Chrome/Application/chrome.exe" "$PF86/Google/Chrome/Application/chrome.exe" "$LA/Google/Chrome/Application/chrome.exe" \
           "$PF86/Microsoft/Edge/Application/msedge.exe" "$PF/Microsoft/Edge/Application/msedge.exe"; do
    [ -f "$c" ] && { CH="$(basename "$c" .exe)"; break; }
  done
else
  for c in "/Applications/Google Chrome.app" "/Applications/Chromium.app" "/Applications/Microsoft Edge.app" "/Applications/Brave Browser.app"; do
    [ -d "$c" ] && { CH="$(basename "$c" .app)"; break; }
  done
fi
if [ -n "$CH" ]; then ok "navegador para as conferências de texto ($CH)"
else aviso "sem Google Chrome ou Edge: os motores editorial, dentro do mundo e quadro neon usam o navegador para conferir se nenhum texto sai da tela. Instale o Google Chrome."; fi

F="$RSA/motores/documentario/base/assets/fonts"
if [ -f "$F/HelveticaNeue.ttf" ] && [ -f "$F/HelveticaNeue-Bold.ttf" ] && [ -f "$F/HoeflerText-Italic.ttf" ]; then ok "fontes do motor documentário (tiradas deste computador)"
else aviso "fontes do motor documentário ainda não extraídas (rode o instalar.sh; os outros três motores não dependem delas)"; fi

W=""; for w in "$RSA/modelos/ggml-large-v3-turbo-q5_0.bin" "$RSA/modelos/ggml-large-v3-turbo.bin" "$HOME/.cache/whisper-cpp/ggml-large-v3-turbo.bin"; do [ -f "$w" ] && { W="$w"; break; }; done
if command -v whisper-cli >/dev/null 2>&1 && [ -n "$W" ]; then ok "transcritor para conferir a narração (whisper)"
elif [ "$OS" = mac ]; then aviso "transcritor (whisper) ausente: a etapa 'conferir-fala' é pulada. Para ligar: bash \"$RSA/instalar.sh\" --com-whisper"
else aviso "transcritor (whisper) não disponível no Windows: a etapa 'conferir-fala' é pulada (ouça a narração inteira antes de montar)"; fi

LIVRE=$(df -k "$HOME" 2>/dev/null | awk 'NR==2 {print int($4/1048576)}')
if [ -n "$LIVRE" ]; then
  if [ "$LIVRE" -ge 3 ]; then ok "espaço livre: ${LIVRE} GB"; else aviso "pouco espaço livre (${LIVRE} GB): cada reel ocupa de 200 a 500 MB enquanto é produzido"; fi
fi

echo
if [ "$FALTA" -eq 0 ]; then
  if [ "$AVISO" -gt 0 ]; then echo "PRONTO: dá para produzir reels neste computador. ($AVISO aviso(s) acima)"; else echo "PRONTO: dá para produzir reels neste computador."; fi
  echo "Falta só conferir, dentro do Claude Code, se o Higgsfield está conectado (voz, imagens e trilha saem de lá)."
  exit 0
fi
echo "FALTAM $FALTA item(ns) essencial(is). Rode:  bash \"$RSA/instalar.sh\""
exit 1
