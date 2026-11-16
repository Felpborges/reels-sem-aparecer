#!/usr/bin/env python3
"""ESTILO B · os efeitos de virada RECRIADOS a partir da referência (pericia/audio/sep/htdemucs/ref, drums+other):
  queda        cortes 8,07 e 20,23: um tom que despenca de ~2 kHz a ~50 Hz em 0,2 s (rápido no começo, devagar no fim),
               máximo em ~0,11 s, -5 dB em 0,15 s, -13 dB em 0,21 s. Começa NO corte, sem sopro antes.
  queda-grave  a mesma, partindo de 400 Hz (a que vem logo depois do riser)
  whoosh       movimentos rápidos de câmera (1,05 · 12,25 · 28,5-28,9): sopro de AR grave-médio (200 Hz-3 kHz, centro
               ~1,1 kHz), sobe 0,35 s, cai 0,5 s, com turbulência e um leve doppler; o instante marcado é o pico
  riser        19,4 → 20,23: sopro largo (200 Hz-6 kHz) que incha ~1 s e corta seco no corte
Na referência NÃO há efeito na maioria dos cortes: só a queda em ~1 de cada 6-7 cortes e o whoosh nos movimentos rápidos.
uso: sfx_ref.py [pasta]   (grava queda.wav, queda-grave.wav, whoosh.wav, riser.wav e atualiza pre.json)"""
import sys, os, json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR = 48000; rng = np.random.default_rng(23)
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "sfx")
def t(n): return np.arange(int(n * SR)) / SR
def norm(x, pk=0.9): return x / (np.abs(x).max() + 1e-9) * pk
def rosa(n):                                     # ruído rosa (o sopro da referência é grave-médio, não chiado)
    X = np.fft.rfft(rng.normal(0, 1, n)); f = np.fft.rfftfreq(n, 1 / SR); X[1:] /= np.sqrt(f[1:]); X[0] = 0
    return np.fft.irfft(X, n)
def bp_var(x, centro, q=0.9, blk=480):
    """passa-banda que anda: centro[i] em Hz por amostra (filtro por blocos com sobreposição)."""
    out = np.zeros_like(x); w = np.hanning(2 * blk)
    for i in range(0, len(x) - 2 * blk, blk):
        c = float(centro[i + blk]); lo, hi = max(40, c / (1 + q)), min(SR / 2 - 100, c * (1 + q))
        seg = sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), x[max(0, i - 4 * blk):i + 2 * blk])[-2 * blk:]
        out[i:i + 2 * blk] += seg * w
    return out
P = {}
def queda(f_alto, nome):
    tt = t(0.75)
    f = 45 + (f_alto - 295) * np.exp(-tt / 0.012) + 250 * np.exp(-tt / 0.06)      # 2000 @0 · 400 @0,023 · 100 @0,10 · 60 @0,145
    y = np.sin(2 * np.pi * np.cumsum(f) / SR)
    y *= (0.3 + 0.7 * (1 - np.exp(-tt / 0.045))) * np.where(tt < 0.11, 1.0, np.exp(-(tt - 0.11) / 0.065)) * (1 - np.exp(-tt / 0.002))
    y = np.tanh(y * 1.1) / np.tanh(1.1)                                             # pouco harmônico: a referência é quase um fio só
    y = sosfilt(butter(2, 30, "highpass", fs=SR, output="sos"), y)
    sf.write(f"{D}/{nome}.wav", norm(y), SR); P[nome] = 0.0
queda(2000, "queda"); queda(400, "queda-grave")
# whoosh: sobe 0,35 s, cai 0,5 s; centro do filtro 450 -> 1300 -> 500 Hz (doppler); turbulência 8-25 Hz; anda de um lado ao outro
sobe, cai = 0.35, 0.5; tt = t(sobe + cai + 0.15); n = len(tt)
env = np.where(tt < sobe, (tt / sobe) ** 2.0, np.exp(-((tt - sobe) / cai) * 3.2))
centro = np.where(tt < sobe, 450 + 850 * (tt / sobe) ** 1.5, 500 + 800 * np.exp(-(tt - sobe) / 0.18))
x = rosa(n + 4000)[:n]
corpo = bp_var(x, centro, q=1.4)
turb = 1 + 0.35 * sosfilt(butter(2, [8, 25], "bandpass", fs=SR, output="sos"), rng.normal(0, 1, n)) / 0.25
turb = np.clip(turb, 0.3, 1.8)
m = norm(corpo * env * turb); f = int(SR * 0.12); m[-f:] *= np.linspace(1, 0, f) ** 2
pan = np.clip(-0.6 + 1.2 * tt / (sobe + cai), -1, 1)                               # passa da esquerda pra direita
L = m * np.sqrt((1 - pan) / 2); R = m * np.sqrt((1 + pan) / 2)
sf.write(f"{D}/whoosh.wav", norm(np.stack([L, R], 1), 0.85), SR); P["whoosh"] = sobe
# riser: ruído rosa 200 Hz-6 kHz incha 1 s e corta seco; inclinação leve para o agudo no fim
tt = t(1.0); x = rosa(len(tt) + 4000)[:len(tt)]
base = sosfilt(butter(2, [200, 6000], "bandpass", fs=SR, output="sos"), x)          # uma banda só (sem buraco no meio)
agudo = sosfilt(butter(1, 1500, "highpass", fs=SR, output="sos"), base)
k = tt / 1.0; r = (base + agudo * 0.8 * k) * k ** 2.4
r[-int(SR * 0.01):] *= np.linspace(1, 0, int(SR * 0.01))
sf.write(f"{D}/riser.wav", norm(r, 0.7), SR); P["riser"] = 1.0
pre = json.load(open(f"{D}/pre.json")); pre.update(P); json.dump(pre, open(f"{D}/pre.json", "w"))
print("efeitos recriados em", D, P)
