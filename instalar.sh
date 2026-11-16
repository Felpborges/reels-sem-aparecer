#!/usr/bin/env bash
# REELS SEM APARECER · instalador (macOS e Windows).
#
#   bash instalar.sh                 instala tudo o que falta (pode rodar de novo quantas vezes quiser; não refaz o que já existe)
#   bash instalar.sh --com-whisper   (só Mac) também instala o transcritor que confere a narração (+ 0,6 GB)
#   bash instalar.sh --atualizar     baixa a versão mais nova da skill antes de instalar
#
# Direto da internet, sem baixar nada antes (ele mesmo baixa a skill para ~/.claude/skills/):
#   Mac (app Terminal):          curl -fsSL https://raw.githubusercontent.com/Felpborges/reels-sem-aparecer/main/instalar.sh | bash
#   Windows (app PowerShell):    irm https://raw.githubusercontent.com/Felpborges/reels-sem-aparecer/main/instalar.ps1 | iex
#
# O que ele põe no computador (cerca de 4 GB, 10 a 20 minutos na primeira vez):
#   · Mac: pelo Homebrew, ffmpeg, node, rubberband e uv (só os que faltarem)
#   · Windows: dentro da pasta da skill (ferramentas/bin), ffmpeg, node, rubberband e uv; nada é instalado no sistema
#   · dentro da pasta da skill: um Python próprio (.venv) e o HyperFrames na versão em que os motores foram validados
#   · modelos: alinhamento palavra a palavra em português, separação de áudio e recorte de fundo
#   · as três fontes do motor documentário, tiradas do próprio computador
if [ -n "$ZSH_VERSION" ]; then case "$0" in *instalar.sh) exec bash "$0" "$@" ;; *) emulate sh ;; esac; fi
set -e
REPO="${RSA_REPO:-https://github.com/Felpborges/reels-sem-aparecer.git}"   # RSA_REPO e RSA_RAMO: só para testes
RAMO="${RSA_RAMO:-main}"
DESTINO="$HOME/.claude/skills/reels-sem-aparecer"
COM_WHISPER=0; ATUALIZAR=0
for a in "$@"; do
  case "$a" in
    --com-whisper) COM_WHISPER=1 ;;
    --atualizar) ATUALIZAR=1 ;;
    *) echo "opção desconhecida: $a"; exit 2 ;;
  esac
done
case "$(uname -s)" in
  Darwin) OS=mac ;;
  MINGW*|MSYS*|CYGWIN*) OS=windows ;;
  *) echo "Este instalador cobre macOS e Windows. Neste sistema ($(uname -s)) a skill ainda não roda."; exit 1 ;;
esac
passo() { printf '\n▸ %s\n' "$1"; }

# 0 · onde está a skill? (rodando de dentro dela, ou vindo direto da internet)
AQUI=""; case "$0" in *instalar.sh) AQUI="$(cd "$(dirname "$0")" && pwd)" ;; esac
if [ -n "$AQUI" ] && [ -f "$AQUI/SKILL.md" ] && [ -d "$AQUI/motores" ]; then
  RSA="$AQUI"
  if [ "$ATUALIZAR" = 1 ] && [ -d "$RSA/.git" ]; then
    passo "Atualizando a skill"; git -C "$RSA" pull --ff-only
    if [ "$COM_WHISPER" = 1 ]; then exec bash "$RSA/instalar.sh" --com-whisper; else exec bash "$RSA/instalar.sh"; fi
  fi
else
  command -v git >/dev/null 2>&1 || { echo "Falta o git. No Mac: abra o Terminal, rode  xcode-select --install  , conclua e rode este comando de novo. No Windows: use o comando do PowerShell (instalar.ps1), que instala o Git."; exit 1; }
  if [ -d "$DESTINO/.git" ]; then passo "A skill já está em $DESTINO; atualizando"; git -C "$DESTINO" pull --ff-only
  elif [ -e "$DESTINO" ]; then echo "Já existe uma pasta em $DESTINO que não veio deste instalador. Renomeie ou apague essa pasta e rode de novo."; exit 1
  else passo "Baixando a skill para $DESTINO"; mkdir -p "$(dirname "$DESTINO")"; git -c core.autocrlf=false clone --depth 1 --branch "$RAMO" "$REPO" "$DESTINO"; fi
  exec bash "$DESTINO/instalar.sh" "$@"
fi
echo "Reels sem aparecer · instalando em $RSA"

if [ "$OS" = mac ]; then
  export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
  # 1 · Homebrew (é o único passo que pede a senha do computador; por isso não é feito sozinho)
  if ! command -v brew >/dev/null 2>&1; then
    echo
    echo "Falta o Homebrew, o instalador de programas do Mac. Ele pede a senha do computador, então precisa ser você:"
    echo "  1. Abra o app Terminal."
    echo '  2. Cole esta linha e aperte Enter:'
    echo '     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    echo "  3. Quando terminar, rode este instalador de novo."
    exit 3
  fi
  # 2 · programas
  passo "Programas (ffmpeg, node, rubberband, uv)"
  for par in ffmpeg:ffmpeg node:node rubberband:rubberband uv:uv; do
    cmd="${par%%:*}"; formula="${par##*:}"
    if command -v "$cmd" >/dev/null 2>&1; then echo "  já instalado: $cmd"; else echo "  instalando $formula…"; brew install "$formula"; fi
  done
  PY="$RSA/.venv/bin/python"
else
  # 1-2 · Windows: programas portáteis dentro da skill (não mexe no sistema, não pede senha)
  BIN="$RSA/ferramentas/bin"; TMPD="$BIN/_baixando"; mkdir -p "$BIN"
  ACHA=/usr/bin/find; [ -x "$ACHA" ] || ACHA=find      # o "find" do Windows é outro programa: usa sempre o do Git Bash
  export PATH="$BIN:$BIN/node:$PATH"
  baixa() { curl -fL --retry 3 --retry-delay 2 --progress-bar -o "$2" "$1"; }
  abre_zip() {
    rm -rf "$2"; mkdir -p "$2"
    if command -v unzip >/dev/null 2>&1; then unzip -qo "$1" -d "$2"
    else powershell.exe -NoProfile -Command "Expand-Archive -Force -LiteralPath '$(cygpath -w "$1")' -DestinationPath '$(cygpath -w "$2")'"; fi
  }
  passo "Programas (uv, ffmpeg, node, rubberband), dentro da pasta da skill"
  mkdir -p "$TMPD"
  if [ -f "$BIN/uv.exe" ]; then echo "  já instalado: uv"; else
    echo "  baixando uv…"; baixa "https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip" "$TMPD/uv.zip"
    abre_zip "$TMPD/uv.zip" "$TMPD/uv"; "$ACHA" "$TMPD/uv" -name "uv*.exe" -exec cp -f {} "$BIN/" \;
    [ -f "$BIN/uv.exe" ] || { echo "O pacote do uv veio sem o programa. Rode o instalador de novo."; exit 1; }
  fi
  if [ -f "$BIN/ffmpeg.exe" ] && [ -f "$BIN/ffprobe.exe" ]; then echo "  já instalado: ffmpeg"; else
    echo "  baixando ffmpeg (uns 100 MB)…"; baixa "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" "$TMPD/ffmpeg.zip"
    abre_zip "$TMPD/ffmpeg.zip" "$TMPD/ffmpeg"
    "$ACHA" "$TMPD/ffmpeg" \( -name "ffmpeg.exe" -o -name "ffprobe.exe" \) -exec cp -f {} "$BIN/" \;
    [ -f "$BIN/ffmpeg.exe" ] && [ -f "$BIN/ffprobe.exe" ] || { echo "O pacote do ffmpeg veio incompleto. Rode o instalador de novo."; exit 1; }
  fi
  if [ -f "$BIN/node/node.exe" ]; then echo "  já instalado: node"; else
    NODE_ZIP="$(curl -fsSL https://nodejs.org/dist/latest-v22.x/SHASUMS256.txt | grep -o 'node-v[0-9.]*-win-x64\.zip' | head -1)"
    [ -n "$NODE_ZIP" ] || { echo "Não consegui descobrir a versão do Node para baixar. Confira a internet e rode de novo."; exit 1; }
    echo "  baixando $NODE_ZIP…"; baixa "https://nodejs.org/dist/latest-v22.x/$NODE_ZIP" "$TMPD/node.zip"
    abre_zip "$TMPD/node.zip" "$TMPD/node"; rm -rf "$BIN/node"
    NODE_DIR="$(dirname "$("$ACHA" "$TMPD/node" -name "node.exe" | head -1)")"
    [ -f "$NODE_DIR/node.exe" ] || { echo "O pacote do Node veio sem o programa. Rode o instalador de novo."; exit 1; }
    mv "$NODE_DIR" "$BIN/node" 2>/dev/null || { rm -rf "$BIN/node"; cp -R "$NODE_DIR" "$BIN/node"; }
  fi
  if [ -f "$BIN/rubberband.exe" ]; then echo "  já instalado: rubberband"; else
    echo "  baixando rubberband…"; baixa "https://breakfastquay.com/files/releases/rubberband-4.0.0-gpl-executable-windows.zip" "$TMPD/rb.zip"
    abre_zip "$TMPD/rb.zip" "$TMPD/rb"
    RB_DIR="$(dirname "$("$ACHA" "$TMPD/rb" -name "rubberband.exe" | head -1)")"
    [ -f "$RB_DIR/rubberband.exe" ] || { echo "O pacote do rubberband veio sem o programa. Rode o instalador de novo."; exit 1; }
    "$ACHA" "$RB_DIR" -maxdepth 1 \( -name "*.exe" -o -name "*.dll" \) -exec cp -f {} "$BIN/" \;
  fi
  rm -rf "$TMPD" 2>/dev/null || true
  PY="$RSA/.venv/Scripts/python.exe"
  export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
fi

# 3 · Python da skill
passo "Python da skill e pacotes (a parte mais demorada na primeira vez)"
[ -f "$PY" ] || uv venv --python 3.11 "$RSA/.venv"
uv pip install --python "$PY" -r "$RSA/ferramentas/requirements.txt"
if [ "$OS" = windows ]; then
  # bibliotecas da Microsoft de que o torch precisa e que um Windows recém-instalado pode não ter (se não der, segue)
  uv pip install --python "$PY" msvc-runtime >/dev/null 2>&1 || true
  if ! "$PY" -c "import torch" >/dev/null 2>&1; then
    echo
    echo "O Windows está sem o 'Microsoft Visual C++ Redistributable', de que os motores precisam. É rápido:"
    echo "  1. Baixe e instale: https://aka.ms/vs/17/release/vc_redist.x64.exe"
    echo "  2. Rode este instalador de novo."
    exit 4
  fi
fi

# 4 · HyperFrames (versão fixa) e o navegador dele
passo "HyperFrames (renderizador) na versão dos motores"
HFB="$RSA/ferramentas/node_modules/.bin/hyperframes"
if [ ! -e "$HFB" ]; then
  npm install --prefix "$RSA/ferramentas" --no-audit --no-fund --loglevel=error
else echo "  já instalado"; fi
"$HFB" browser ensure >/dev/null 2>&1 || "$HFB" browser ensure

# 5 · modelos
passo "Modelos (alinhamento em português ~1,2 GB, separação de áudio, recorte de fundo)"
"$PY" - <<'E'
import os, sys
from huggingface_hub import snapshot_download
snapshot_download("jonatasgrosman/wav2vec2-large-xlsr-53-portuguese",
                  allow_patterns=["*.json", "*.txt", "pytorch_model.bin", "model.safetensors"])
os.environ["HF_HUB_OFFLINE"] = "1"
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
M = "jonatasgrosman/wav2vec2-large-xlsr-53-portuguese"
Wav2Vec2Processor.from_pretrained(M); Wav2Vec2ForCTC.from_pretrained(M)
print("  alinhamento: pronto")
from demucs.pretrained import get_model
get_model("htdemucs"); print("  separação de áudio: pronta")
from rembg import new_session
new_session("isnet-general-use"); print("  recorte de fundo: pronto")
E

# 6 · fontes do motor documentário (do próprio computador)
passo "Fontes do motor documentário"
"$PY" "$RSA/ferramentas/fontes-do-sistema.py" || true

# 7 · transcritor (opcional, só Mac)
if [ "$COM_WHISPER" = 1 ]; then
  if [ "$OS" = mac ]; then
    passo "Transcritor para conferir a narração (whisper, 0,6 GB)"
    command -v whisper-cli >/dev/null 2>&1 || brew install whisper-cpp
    mkdir -p "$RSA/modelos"
    [ -f "$RSA/modelos/ggml-large-v3-turbo-q5_0.bin" ] || curl -fL --progress-bar -o "$RSA/modelos/ggml-large-v3-turbo-q5_0.bin" \
      "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin"
  else
    echo; echo "O transcritor (--com-whisper) ainda só é instalado no Mac. No Windows a etapa 'conferir-fala' fica pulada: ouça a narração inteira antes de montar."
  fi
fi

# 8 · atalhos por nome de motor (/reel-editorial, /reel-neon, /reel-documentario, /reel-dentro-do-mundo)
if [ "$(dirname "$RSA")" = "$HOME/.claude/skills" ]; then
  passo "Atalhos dos motores"
  for d in "$RSA"/atalhos/*/; do
    [ -d "$d" ] || continue
    n="$(basename "$d")"; alvo="$HOME/.claude/skills/$n"
    if [ -e "$alvo" ] && ! grep -q "reels-sem-aparecer" "$alvo/SKILL.md" 2>/dev/null; then echo "  /$n: já existe outra skill com esse nome; mantive a sua"
    else mkdir -p "$alvo"; cp "$d/SKILL.md" "$alvo/SKILL.md"; echo "  /$n"; fi
  done
fi

echo
bash "$RSA/ferramentas/diagnostico.sh"
