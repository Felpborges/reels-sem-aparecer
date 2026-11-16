#!/bin/zsh
# REELS SEM APARECER · instalador (macOS).
#
#   zsh instalar.sh                 instala tudo o que falta (pode rodar de novo quantas vezes quiser; não refaz o que já existe)
#   zsh instalar.sh --com-whisper   também instala o transcritor que confere a narração (+ 0,6 GB)
#   zsh instalar.sh --atualizar     baixa a versão mais nova da skill antes de instalar
#
# Também funciona direto da internet, sem baixar nada antes (ele mesmo baixa a skill para ~/.claude/skills/):
#   curl -fsSL https://raw.githubusercontent.com/Felpborges/reels-sem-aparecer/main/instalar.sh | zsh
#
# O que ele põe no computador (cerca de 4 GB, 10 a 20 minutos na primeira vez):
#   · pelo Homebrew: ffmpeg, node, rubberband e uv (só os que faltarem)
#   · dentro da pasta da skill: um Python próprio (.venv) e o HyperFrames na versão em que os motores foram validados
#   · modelos: alinhamento palavra a palavra em português, separação de áudio e recorte de fundo
#   · as três fontes do motor documentário, tiradas do próprio macOS
# Nada é instalado fora da pasta da skill além dos programas do Homebrew e dos caches normais dessas ferramentas.

set -e
REPO="https://github.com/Felpborges/reels-sem-aparecer.git"
DESTINO="$HOME/.claude/skills/reels-sem-aparecer"
COM_WHISPER=0; ATUALIZAR=0
for a in "$@"; do
  case "$a" in
    --com-whisper) COM_WHISPER=1 ;;
    --atualizar) ATUALIZAR=1 ;;
    *) print "opção desconhecida: $a"; exit 2 ;;
  esac
done
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
passo() { print; print -r -- "▸ $1"; }

[ "$(uname)" = "Darwin" ] || { print "Este instalador é para macOS. No Windows a skill ainda não roda."; exit 1; }

# 0 · onde está a skill? (rodando de dentro dela, ou vindo direto da internet)
AQUI="${0:a:h}"
if [ -f "$AQUI/SKILL.md" ] && [ -d "$AQUI/motores" ]; then
  RSA="$AQUI"
  if (( ATUALIZAR )) && [ -d "$RSA/.git" ]; then passo "Atualizando a skill"; git -C "$RSA" pull --ff-only; fi
else
  command -v git >/dev/null || { print "Falta o git. Abra o Terminal, rode  xcode-select --install  , conclua a instalação e rode este comando de novo."; exit 1; }
  if [ -d "$DESTINO/.git" ]; then passo "A skill já está em $DESTINO; atualizando"; git -C "$DESTINO" pull --ff-only
  elif [ -e "$DESTINO" ]; then print "Já existe uma pasta em $DESTINO que não veio deste instalador. Renomeie ou apague essa pasta e rode de novo."; exit 1
  else passo "Baixando a skill para $DESTINO"; mkdir -p "${DESTINO:h}"; git clone --depth 1 "$REPO" "$DESTINO"; fi
  exec zsh "$DESTINO/instalar.sh" "$@"
fi
print "Reels sem aparecer · instalando em $RSA"

# 1 · Homebrew (é o único passo que pede a senha do computador; por isso não é feito sozinho)
if ! command -v brew >/dev/null; then
  print
  print "Falta o Homebrew, o instalador de programas do Mac. Ele pede a senha do computador, então precisa ser você:"
  print "  1. Abra o app Terminal."
  print '  2. Cole esta linha e aperte Enter:'
  print '     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  print "  3. Quando terminar, rode este instalador de novo."
  exit 3
fi

# 2 · programas
passo "Programas (ffmpeg, node, rubberband, uv)"
for par in ffmpeg:ffmpeg node:node rubberband:rubberband uv:uv; do
  cmd="${par%%:*}"; formula="${par##*:}"
  if command -v "$cmd" >/dev/null; then print "  já instalado: $cmd"; else print "  instalando $formula…"; brew install "$formula"; fi
done

# 3 · Python da skill
passo "Python da skill e pacotes (a parte mais demorada na primeira vez)"
[ -x "$RSA/.venv/bin/python" ] || uv venv --python 3.11 "$RSA/.venv"
uv pip install --python "$RSA/.venv/bin/python" -r "$RSA/ferramentas/requirements.txt"

# 4 · HyperFrames (versão fixa) e o navegador dele
passo "HyperFrames (renderizador) na versão dos motores"
if [ ! -x "$RSA/ferramentas/node_modules/.bin/hyperframes" ]; then
  npm install --prefix "$RSA/ferramentas" --no-audit --no-fund --loglevel=error
else print "  já instalado"; fi
"$RSA/ferramentas/node_modules/.bin/hyperframes" browser ensure >/dev/null 2>&1 || "$RSA/ferramentas/node_modules/.bin/hyperframes" browser ensure

# 5 · modelos
passo "Modelos (alinhamento em português ~1,2 GB, separação de áudio, recorte de fundo)"
"$RSA/.venv/bin/python" - <<'E'
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

# 6 · fontes do motor documentário (do próprio macOS)
passo "Fontes do motor documentário"
"$RSA/.venv/bin/python" "$RSA/ferramentas/fontes-do-sistema.py" || true

# 7 · transcritor (opcional)
if (( COM_WHISPER )); then
  passo "Transcritor para conferir a narração (whisper, 0,6 GB)"
  command -v whisper-cli >/dev/null || brew install whisper-cpp
  mkdir -p "$RSA/modelos"
  [ -f "$RSA/modelos/ggml-large-v3-turbo-q5_0.bin" ] || curl -fL --progress-bar -o "$RSA/modelos/ggml-large-v3-turbo-q5_0.bin" \
    "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin"
fi

# 8 · atalhos por nome de motor (/reel-editorial, /reel-neon, /reel-documentario, /reel-dentro-do-mundo)
if [ "${RSA:h}" = "$HOME/.claude/skills" ]; then
  passo "Atalhos dos motores"
  for d in "$RSA"/atalhos/*(/N); do
    n="${d:t}"; alvo="$HOME/.claude/skills/$n"
    if [ -e "$alvo" ] && ! grep -q "reels-sem-aparecer" "$alvo/SKILL.md" 2>/dev/null; then print "  /$n: já existe outra skill com esse nome; mantive a sua"
    else mkdir -p "$alvo"; cp "$d/SKILL.md" "$alvo/SKILL.md"; print "  /$n"; fi
  done
fi

print
zsh "$RSA/ferramentas/diagnostico.sh"
