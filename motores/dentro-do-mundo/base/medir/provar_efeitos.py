#!/usr/bin/env python3
"""ESTILO B · PROVA DE EFEITOS: toca o MESMO trecho do reel várias vezes, cada vez com um efeito diferente no mesmo
instante, para escolher no ouvido qual som cabe naquela parte. Os efeitos medidos na referência (queda, whoosh, riser…)
são só o ponto de partida: cada reel pode testar outros.
uso: provar_efeitos.py <t> <opção> [<opção> ...]
  t       instante do efeito no reel (o corte, ou o pico do whoosh), em segundos
  opção   'nada' | tipo de assets/sfx (queda, whoosh, …) | caminho de um .wav/.mp3 (gerado no Higgsfield, sintetizado…)
          sufixos opcionais: @db (ganho extra) e @pre (s antes de t em que o arquivo começa; tipos usam assets/sfx/pre.json)
          ex.: provar_efeitos.py 29.18 nada queda whoosh queda@-3 brutos/sfx/impacto.wav@0@0.05
Antes: ./reel.sh montar (ou mix.py) uma vez, para existir assets/mix_sem_efeitos.wav. Nível = metas.json (-6 dB se o tipo
for novo) em relação ao p90 da voz, a mesma régua do mix.py. Saída: renders/provar-<t>.m4a, na ordem das opções."""
import sys, os, json, subprocess, numpy as np, soundfile as sf, librosa
AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SR = 48000
if len(sys.argv) < 3: sys.exit(__doc__)
t0 = float(sys.argv[1]); ops = sys.argv[2:]
base_p = os.path.join(AQ, "assets", "mix_sem_efeitos.wav")
if not os.path.exists(base_p): sys.exit("falta assets/mix_sem_efeitos.wav: rode o mix.py antes")
base, _ = sf.read(base_p)
M = json.load(open(os.path.join(AQ, "medir", "metas.json")))["audio"]["efeitos_rel_voz_p90_db"]
PRE = json.load(open(os.path.join(AQ, "assets", "sfx", "pre.json")))
voz, sr = sf.read(os.path.join(AQ, "assets", "narracao.wav")); voz = voz.mean(1) if voz.ndim > 1 else voz
if sr != SR: voz = librosa.resample(voz, orig_sr=sr, target_sr=SR)
def env10(x): h = int(SR * 0.01); return np.array([np.sqrt(np.mean(x[i:i + h] ** 2)) for i in range(0, len(x) - h, h)])
ev = 20 * np.log10(env10(voz) + 1e-9); p90 = np.percentile(ev[ev > ev.max() - 35], 90)
A, D = 1.6, 1.6                                       # trecho: 1,6 s antes e depois do instante
a, b = max(0, int((t0 - A) * SR)), min(len(base), int((t0 + D) * SR))
pecas, pausa = [], np.zeros(int(SR * 0.6))
for op in ops:
    nome, *suf = op.split("@"); extra = float(suf[0]) if suf else 0.0
    y = base[a:b].copy()
    if nome != "nada":
        arq = nome if os.path.exists(nome) else os.path.join(AQ, "assets", "sfx", nome + ".wav")
        x, _ = librosa.load(arq, sr=SR, mono=True)
        tipo = os.path.splitext(os.path.basename(nome))[0]
        pre = float(suf[1]) if len(suf) > 1 else PRE.get(tipo, 0.0)
        alvo = p90 + M.get(tipo, -6.0) + extra; x = x * 10 ** ((alvo - 20 * np.log10(env10(x).max() + 1e-9)) / 20)
        s = int((t0 - pre) * SR) - a
        if s < 0: x = x[-s:]; s = 0
        n = min(len(y) - s, len(x)); y[s:s + n] += x[:n]
    pecas += [y, pausa]; print(f"{len(pecas) // 2}. {op}")
out = np.concatenate(pecas); tmp = os.path.join(AQ, "assets", "_provar.wav"); sf.write(tmp, out, SR)
os.makedirs(os.path.join(AQ, "renders"), exist_ok=True); dst = os.path.join(AQ, "renders", f"provar-{t0:.2f}.m4a")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-af", "loudnorm=I=-16:TP=-1.0", "-c:a", "aac", "-b:a", "192k", dst], check=True)
os.remove(tmp); print("->", dst)
