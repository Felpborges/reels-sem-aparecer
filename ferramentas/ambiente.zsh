# Ambiente compartilhado dos quatro motores. É carregado pelo reel.sh de cada projeto (source), nunca rodado sozinho.
# Entra com RSA = pasta da skill. Sai com: python3/hyperframes/node no PATH certos e as variáveis RSA_* exportadas.
if [ ! -x "$RSA/.venv/bin/python" ] || [ ! -x "$RSA/ferramentas/node_modules/.bin/hyperframes" ]; then
  echo "A skill reels-sem-aparecer ainda não terminou de ser instalada neste computador."
  echo "Rode:  zsh \"$RSA/instalar.sh\"     (ou peça ao Claude: \"instala a skill reels-sem-aparecer\")"
  return 1
fi
export RSA
export PATH="$RSA/.venv/bin:$RSA/ferramentas/node_modules/.bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
export RSA_NODE_MODULES="$RSA/ferramentas/node_modules/"
export RSA_PERICIA="$RSA/ferramentas/pericia-movimento.py"
export TOKENIZERS_PARALLELISM=false
if [ -z "$RSA_CHROME" ]; then
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "/Applications/Chromium.app/Contents/MacOS/Chromium" \
           "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"; do
    [ -x "$c" ] && { export RSA_CHROME="$c"; break; }
  done
fi
if [ -z "$RSA_WHISPER_MODEL" ]; then
  for w in "$RSA/modelos/ggml-large-v3-turbo-q5_0.bin" "$RSA/modelos/ggml-large-v3-turbo.bin" "$HOME/.cache/whisper-cpp/ggml-large-v3-turbo.bin"; do
    [ -f "$w" ] && { export RSA_WHISPER_MODEL="$w"; break; }
  done
fi
# transcrição por trechos de 25 s (a transcrição do arquivo inteiro pula frases). uso: rsa_conferir_fala medir/voz16k.wav
rsa_conferir_fala() {
  if ! command -v whisper-cli >/dev/null || [ -z "$RSA_WHISPER_MODEL" ]; then
    echo "conferir-fala: o transcritor (whisper) não está instalado; esta conferência foi PULADA."
    echo "Para ligar: zsh \"$RSA/instalar.sh\" --com-whisper    (enquanto isso, ouça a narração inteira antes de montar)"
    return 0
  fi
  local D T=0 TR; TR=$(mktemp -t rsa_trecho).wav
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$1")
  while (( T < D )); do
    ffmpeg -y -v error -ss $T -t 26 -i "$1" "$TR"
    echo "[$T s] $(whisper-cli -m "$RSA_WHISPER_MODEL" -l pt -nt -np -f "$TR" 2>/dev/null | tr '\n' ' ')"; T=$((T + 25))
  done; rm -f "$TR"
}
