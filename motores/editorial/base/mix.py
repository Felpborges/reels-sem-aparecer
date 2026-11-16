#!/usr/bin/env python3
"""Mixagem da v2 com os níveis medidos no reel de referência (voz/trilha/efeitos separados com demucs):
- trilha melódica constante, sem ducking, ~24,6 dB abaixo da voz (RMS), equalizada para a faixa de 500 Hz-1 kHz do original;
- efeitos com o pico (janela de 10 ms) relativo ao p90 da voz: impacto +9,7 · pop -4,5 · pop-longo -9,2 · clique -8,7 ·
  clique-grave -11 · painel -11,5 dB; cada um começa no quadro da entrada visual (medir/sons_v2.json, gerado pelo build.py);
- saída na mesma loudness integrada do original."""
import json, os, subprocess, numpy as np, soundfile as sf
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
A_ = json.load(open("medir/alinhamento.json")); DUR = round(A_[-1]["end"] + 0.2, 2); SR = 48000
LUFS_REF = -15.5                                   # loudness integrada do reel de referência
REL = {"impacto": 9.7, "pop": -4.5, "pop-longo": -9.2, "clique": -8.7, "clique-grave": -11.0, "painel": -11.5}
def le(p):
    y, sr = sf.read(p, always_2d=True); y = y.mean(1)
    if sr != SR:
        tmp = "medir/_rs.wav"; subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", p, "-ar", str(SR), "-ac", "1", tmp], check=True); y, _ = sf.read(tmp); os.remove(tmp)
    return y
def quadros(y):
    h = int(SR * 0.01); n = len(y) // h
    return np.array([20 * np.log10(np.sqrt(np.mean(y[i * h:(i + 1) * h] ** 2)) + 1e-12) for i in range(n)])
rms = lambda y: 20 * np.log10(np.sqrt(np.mean(y ** 2)) + 1e-12)
N = int(DUR * SR)
voz = le("assets/narracao.wav")[:N]; voz = np.pad(voz, (0, N - len(voz)))
qv = quadros(voz); qa = qv[qv > np.percentile(qv, 95) - 30]; p90 = np.percentile(qa, 90); voz_rms = rms(voz[np.repeat(qv > np.percentile(qv, 95) - 30, int(SR * 0.01))[:N] if False else slice(None)])
# trilha: passa-alta 180 Hz + realce em 850 Hz, nível pelo RMS relativo do original
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "assets/trilha.mp3", "-af", "highpass=f=180,equalizer=f=850:t=o:w=1.2:g=6,equalizer=f=320:t=o:w=1:g=-4", "-ar", str(SR), "-ac", "1", "medir/_tr.wav"], check=True)
tr = le("medir/_tr.wav")[:N]; os.remove("medir/_tr.wav"); tr = np.pad(tr, (0, max(0, N - len(tr))))[:N]
alvo_tr = rms(voz) - 23.1; tr *= 10 ** ((alvo_tr - rms(tr)) / 20)
f = np.ones(N); fi = int(0.15 * SR); fo = int(1.2 * SR); f[:fi] = np.linspace(0, 1, fi); f[-fo:] = np.linspace(1, 0, fo); tr *= f
fx = np.zeros(N); sons = json.load(open("medir/sons_v2.json")); cache = {}
for tipo, t in sons:
    if tipo not in cache:
        s = le(f"assets/sfx/{tipo}.wav"); g = p90 + REL[tipo] - quadros(s).max(); cache[tipo] = s * 10 ** (g / 20)
    s = cache[tipo]; a = int(round(t * SR)); b = min(N, a + len(s)); fx[a:b] += s[:b - a]
mix = voz + tr + fx
sf.write("medir/_pre.wav", np.stack([mix, mix], 1), SR)
def lufs(p):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    L = [l.strip() for l in e.splitlines() if l.strip().startswith(("I:", "Peak:"))]
    return float(L[-2].split()[1]), L[-1]
ref_I = LUFS_REF
I, _ = lufs("medir/_pre.wav"); g = ref_I - I
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "medir/_pre.wav", "-af", f"volume={g:.2f}dB,alimiter=limit=0.89:attack=2:release=50:level=false", "-c:a", "aac", "-b:a", "256k", "assets/mix.m4a"], check=True)
os.remove("medir/_pre.wav")
fI, pk = lufs("assets/mix.m4a")
print(f"{len(sons)} efeitos | voz p90 {p90:.1f} dB, trilha {rms(tr):.1f} dB RMS (voz {rms(voz):.1f}) | loudness original {ref_I} LUFS -> nossa {fI} LUFS, {pk}")
