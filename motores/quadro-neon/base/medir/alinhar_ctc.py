"""Alinhamento forçado PT-BR com CTC completo (o caractere pode ocupar vários quadros, como o modelo emite).
uso: python alinhar2.py voz16k.wav texto.json saida.json   (texto.json = [[mostrado, pronúncia], ...])
Início da palavra = primeiro quadro do primeiro caractere; fim = último quadro do último caractere."""
import sys, json, wave, re, os, unicodedata
import numpy as np, torch
os.environ['HF_HUB_OFFLINE'] = '1'
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
M = 'jonatasgrosman/wav2vec2-large-xlsr-53-portuguese'
wav, txt, out = sys.argv[1:4]
w = wave.open(wav); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
proc = Wav2Vec2Processor.from_pretrained(M); model = Wav2Vec2ForCTC.from_pretrained(M).eval()
with torch.inference_mode():
    em = torch.log_softmax(model(proc(x, sampling_rate=sr, return_tensors='pt').input_values).logits[0], -1).numpy()
T = em.shape[0]; ratio = len(x) / sr / T
vocab = proc.tokenizer.get_vocab(); blank = vocab.get('<pad>', 0)
pal = json.load(open(txt)); toks = []; spans = []
for i, (shown, pron) in enumerate(pal):
    p = unicodedata.normalize('NFC', pron.lower()); p = re.sub(r"[^a-záàâãéêíóôõúüç' -]", '', p).replace(' ', '|')
    ch = [c for c in p if c in vocab]
    if i: toks.append(vocab['|'])
    a = len(toks); toks += [vocab[c] for c in ch]; spans.append((a, len(toks)))
N = len(toks); S = 2 * N + 1
ext = np.full(S, blank); ext[1::2] = toks
pula = np.zeros(S, bool); pula[3::2] = ext[3::2] != ext[1:-2:2]            # pode pular o branco entre caracteres diferentes
NEG = -1e18; dp = np.full(S, NEG); dp[0] = em[0, blank]; dp[1] = em[0, ext[1]]
bp = np.zeros((T, S), np.int8)
for t in range(1, T):
    a = dp; b = np.concatenate(([NEG], dp[:-1])); c = np.concatenate(([NEG, NEG], dp[:-2])); c = np.where(pula, c, NEG)
    m = np.stack([a, b, c]); k = m.argmax(0); dp = m[k, np.arange(S)] + em[t, ext]; bp[t] = k
s = S - 1 if dp[S - 1] >= dp[S - 2] else S - 2
est = np.zeros(T, int)
for t in range(T - 1, -1, -1):
    est[t] = s; s -= int(bp[t, s])
first = {}; last = {}
for t, s in enumerate(est):
    if s % 2:
        k = s // 2; first.setdefault(k, t); last[k] = t
res = []
for (shown, pron), (a, b) in zip(pal, spans):
    ks = [k for k in range(a, b) if k in first]
    if not ks: res.append({'text': shown, 'start': None, 'end': None}); continue
    res.append({'text': shown, 'start': round(first[ks[0]] * ratio, 3), 'end': round((last[ks[-1]] + 1) * ratio, 3)})
json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1)
print(len(res), 'palavras; sem tempo:', sum(1 for r in res if r['start'] is None), '| quadros', T, '| s por quadro', round(ratio, 4))
