"""Alinhamento forçado por CTC (wav2vec2 PT-BR, offline). Serve para PT e, de forma aproximada, para o inglês da referência.
uso: alinhar.py <voz16k.wav> <texto.json> <saida.json>   (texto.json = [[mostrada, pronúncia], ...] gerado por texto.py)
Saída: [{"w": palavra, "ini": s, "fim": s}]. Início = 1º quadro do 1º caractere emitido; fim = último quadro do último."""
import sys, json, wave, re, os, unicodedata
import numpy as np, torch
os.environ['HF_HUB_OFFLINE'] = '1'
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
M = 'jonatasgrosman/wav2vec2-large-xlsr-53-portuguese'
wav, txt, out = sys.argv[1:4]
w = wave.open(wav); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
proc = Wav2Vec2Processor.from_pretrained(M); model = Wav2Vec2ForCTC.from_pretrained(M).eval()
with torch.inference_mode():
    em = torch.log_softmax(model(proc(x, sampling_rate=sr, return_tensors='pt').input_values).logits[0], -1).numpy()
T = em.shape[0]; dt = len(x) / sr / T
vocab = proc.tokenizer.get_vocab(); blank = vocab.get('<pad>', 0)
pares = json.load(open(txt))
palavras = [m for m, _ in pares]
toks, spans = [], []
for i, (_, p) in enumerate(pares):
    q = unicodedata.normalize('NFC', p.lower()); q = re.sub(r"[^a-záàâãéêíóôõúüç']", '', q)
    ch = [c for c in q if c in vocab] or ['a']
    if i: toks.append(vocab['|'])
    a = len(toks); toks += [vocab[c] for c in ch]; spans.append((a, len(toks)))
N = len(toks); S = 2 * N + 1
ext = np.full(S, blank); ext[1::2] = toks
pula = np.zeros(S, bool); pula[3::2] = ext[3::2] != ext[1:-2:2]
NEG = -1e18; dp = np.full(S, NEG); dp[0] = em[0, blank]; dp[1] = em[0, ext[1]]
bp = np.zeros((T, S), np.int8)
for t in range(1, T):
    a = dp; b = np.concatenate(([NEG], dp[:-1])); c = np.where(pula, np.concatenate(([NEG, NEG], dp[:-2])), NEG)
    m = np.stack([a, b, c]); k = m.argmax(0); dp = m[k, np.arange(S)] + em[t, ext]; bp[t] = k
s = S - 1 if dp[S - 1] >= dp[S - 2] else S - 2
est = np.zeros(T, int)
for t in range(T - 1, -1, -1):
    est[t] = s; s -= int(bp[t, s])
first, last = {}, {}
for t, s in enumerate(est):
    if s % 2:
        k = s // 2; first.setdefault(k, t); last[k] = t
res = []
for p, (a, b) in zip(palavras, spans):
    ks = [k for k in range(a, b) if k in first]
    res.append({'w': p, 'ini': round(first[ks[0]] * dt, 3), 'fim': round((last[ks[-1]] + 1) * dt, 3)})
json.dump(res, open(out, 'w'), ensure_ascii=False, indent=0)
for r in res: print(f"{r['ini']:6.2f}-{r['fim']:6.2f} {r['w']}")
