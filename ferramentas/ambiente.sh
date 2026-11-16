# Ambiente compartilhado dos quatro motores (macOS e Windows com Git Bash). É carregado pelo reel.sh de cada projeto
# (source), nunca rodado sozinho. Entra com RSA = pasta da skill. Sai com python3/hyperframes/node/ffmpeg/rubberband
# certos no PATH e as variáveis RSA_* exportadas. Escrito para funcionar em bash 3.2+ e em zsh.
case "$(uname -s)" in
  Darwin) RSA_OS=mac ;;
  MINGW*|MSYS*|CYGWIN*) RSA_OS=windows ;;
  *) RSA_OS=linux ;;
esac
if [ "$RSA_OS" = windows ]; then
  RSA="$(cygpath -m "$RSA")"                      # C:/Users/... : serve para o bash e para os programas do Windows
  _rsa_u="$(cygpath -u "$RSA")"                    # /c/Users/... : só para o PATH
  _rsa_vbin="$_rsa_u/.venv/Scripts"; RSA_PY="$RSA/.venv/Scripts/python.exe"
  _rsa_extra="$_rsa_u/ferramentas/bin:$_rsa_u/ferramentas/bin/node:"
else
  _rsa_u="$RSA"; _rsa_vbin="$RSA/.venv/bin"; RSA_PY="$RSA/.venv/bin/python"
  _rsa_extra="/opt/homebrew/bin:/usr/local/bin:"
fi
if [ ! -x "$RSA_PY" ] || [ ! -e "$RSA/ferramentas/node_modules/.bin/hyperframes" ]; then
  echo "A skill reels-sem-aparecer ainda não terminou de ser instalada neste computador."
  echo "Rode:  bash \"$RSA/instalar.sh\"     (ou peça ao Claude: \"instala a skill reels-sem-aparecer\")"
  return 1
fi
export RSA RSA_OS RSA_PY
export PATH="$_rsa_vbin:$_rsa_u/ferramentas/node_modules/.bin:$_rsa_extra$PATH"
export RSA_NODE_MODULES="$RSA/ferramentas/node_modules/"
export RSA_PERICIA="$RSA/ferramentas/pericia-movimento.py"
export TOKENIZERS_PARALLELISM=false
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8       # no Windows o Python abriria os textos em cp1252 e quebraria os acentos
# No Windows o ambiente tem python.exe (não python3) e o "python3" do sistema abre a loja da Microsoft: fixa o da skill.
if [ "$RSA_OS" = windows ]; then python3() { "$RSA_PY" "$@"; }; fi
if [ -z "$RSA_CHROME" ]; then
  if [ "$RSA_OS" = windows ]; then
    _rsa_pf="$(cygpath -m "${PROGRAMFILES:-C:/Program Files}")"; _rsa_pf86="$(cygpath -m "${PROGRAMFILES_X86:-C:/Program Files (x86)}")"
    _rsa_la="$(cygpath -m "${LOCALAPPDATA:-$HOME/AppData/Local}")"
    for c in "$_rsa_pf/Google/Chrome/Application/chrome.exe" "$_rsa_pf86/Google/Chrome/Application/chrome.exe" \
             "$_rsa_la/Google/Chrome/Application/chrome.exe" "$_rsa_pf86/Microsoft/Edge/Application/msedge.exe" \
             "$_rsa_pf/Microsoft/Edge/Application/msedge.exe" "$_rsa_pf/BraveSoftware/Brave-Browser/Application/brave.exe"; do
      [ -f "$c" ] && { export RSA_CHROME="$c"; break; }
    done
  elif [ "$RSA_OS" = mac ]; then
    for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "/Applications/Chromium.app/Contents/MacOS/Chromium" \
             "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"; do
      [ -x "$c" ] && { export RSA_CHROME="$c"; break; }
    done
  else
    for c in google-chrome google-chrome-stable chromium chromium-browser microsoft-edge; do
      command -v "$c" >/dev/null 2>&1 && { export RSA_CHROME="$(command -v "$c")"; break; }
    done
  fi
fi
if [ -z "$RSA_WHISPER_MODEL" ]; then
  for w in "$RSA/modelos/ggml-large-v3-turbo-q5_0.bin" "$RSA/modelos/ggml-large-v3-turbo.bin" "$HOME/.cache/whisper-cpp/ggml-large-v3-turbo.bin"; do
    [ -f "$w" ] && { export RSA_WHISPER_MODEL="$w"; break; }
  done
fi
# transcrição por trechos de 25 s (a transcrição do arquivo inteiro pula frases). uso: rsa_conferir_fala medir/voz16k.wav
rsa_conferir_fala() {
  if ! command -v whisper-cli >/dev/null 2>&1 || [ -z "$RSA_WHISPER_MODEL" ]; then
    echo "conferir-fala: o transcritor (whisper) não está instalado; esta conferência foi PULADA."
    echo "Para ligar (só no Mac): bash \"$RSA/instalar.sh\" --com-whisper    (enquanto isso, ouça a narração inteira antes de montar)"
    return 0
  fi
  _rsa_t=0; _rsa_tr="medir/_trecho_conferir.wav"
  _rsa_d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$1" | tr -d '\r'); _rsa_d=${_rsa_d%.*}
  while [ "$_rsa_t" -le "${_rsa_d:-0}" ]; do
    ffmpeg -y -v error -ss "$_rsa_t" -t 26 -i "$1" "$_rsa_tr"
    echo "[$_rsa_t s] $(whisper-cli -m "$RSA_WHISPER_MODEL" -l pt -nt -np -f "$_rsa_tr" 2>/dev/null | tr '\n' ' ')"; _rsa_t=$((_rsa_t + 25))
  done; rm -f "$_rsa_tr"
}
