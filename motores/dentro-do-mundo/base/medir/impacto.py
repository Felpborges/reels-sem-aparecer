#!/usr/bin/env python3
"""ESTILO B · o IMPACTO (boom texturizado) da referência, recriado pela curva média de cada banda.
Medido em pericia/audio/sep/htdemucs/ref/drums.wav nos 6 booms (1,69 · 4,22 · 10,42 · 15,62 · 22,09 · 27,96): ataque
seco (sem sopro antes), corpo 60-250 Hz com sub tonal descendo ~100 -> 55 Hz, médios 20-25 dB abaixo, agudos 35-45 dB
abaixo, sustenta até ~0,4 s e solta em ~0,1 s. Molde: medir/molde-boom.json (bandas em dB a cada 10 ms).
Fonte = sub tonal + ruído rosa saturados; depois cada banda recebe o envelope do molde (5 passadas para acertar a
sobreposição dos filtros). Variações ('impacto-2', 'impacto-3') mudam o ruído e o sub em ±1 semitom: o mesmo som repetido
cansa. 'soco' = o golpe curto de 6,43 s ("wrong"): bloco de 0,15 s, ataque e corte secos.
uso: impacto.py [pasta]"""
import sys, os, json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt
SR = 48000; AQ = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQ, "..", "assets", "sfx")
M = json.load(open(os.path.join(AQ, "molde-boom.json"))); BANDAS = M["bandas"]; T = np.array(M["db"])   # [banda, quadro 10 ms]
H = int(SR * 0.01)
def filtro(a, b): return butter(4, [a, b], "bandpass", fs=SR, output="sos")
FIL = [filtro(a, b) for a, b in BANDAS]
def env(z): return np.array([np.sqrt(np.mean(z[i:i + H] ** 2)) + 1e-9 for i in range(0, len(z) - H + 1, H)])
def rosa(n, rng):
    X = np.fft.rfft(rng.normal(0, 1, n)); f = np.fft.rfftfreq(n, 1 / SR); X[1:] /= np.sqrt(f[1:]); X[0] = 0
    return np.fft.irfft(X, n)
def impacto(nome, semi=0.0, seed=5, molde=T, dur=0.9):
    rng = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR
    k = 2 ** (semi / 12)
    f = k * (55 + 50 * np.exp(-t / 0.09))                                 # sub ~105 -> 55 Hz
    ph = 2 * np.pi * np.cumsum(f) / SR
    fonte = np.sin(ph) + 0.35 * np.sin(2 * ph + 0.3) + 0.6 * rosa(n, rng) / 0.05
    fonte = np.tanh(fonte * 1.5)
    alvo = 10 ** (molde[:, :n // H] / 20)                                   # envelope linear por banda
    ib = np.arange(n) / H                                                   # índice fracionário do quadro
    y = fonte.copy()
    for passada in range(5):
        partes = []
        for b, sos in enumerate(FIL):
            z = sosfiltfilt(sos, y); e = env(z)[:alvo.shape[1]]
            g = alvo[b, :len(e)] / e                                            # quadro a quadro (o ataque é seco)
            partes.append(z * np.interp(ib, np.arange(len(g)) + 0.5, g))
        y = np.sum(partes, 0)
    y[:int(SR * 0.002)] *= np.linspace(0, 1, int(SR * 0.002))
    y[-int(SR * 0.05):] *= np.linspace(1, 0, int(SR * 0.05))
    sf.write(os.path.join(D, nome + ".wav"), y / np.abs(y).max() * 0.9, SR)
    return y
impacto("impacto", 0, 5); impacto("impacto-2", -1, 9); impacto("impacto-3", 1, 13)
# soco: o molde comprimido no tempo (0,15 s de corpo) e cortado seco
c = T.copy(); idx = np.clip((np.arange(T.shape[1]) * 2.6).astype(int), 0, T.shape[1] - 1); c = c[:, idx]
c[:, 22:] = -90
impacto("soco", 0, 21, molde=c, dur=0.3)
pre = json.load(open(os.path.join(D, "pre.json"))); pre.update({"impacto": 0.05, "impacto-2": 0.05, "impacto-3": 0.05, "soco": 0.05})
json.dump(pre, open(os.path.join(D, "pre.json"), "w")); print("impacto, impacto-2, impacto-3, soco ->", D)
