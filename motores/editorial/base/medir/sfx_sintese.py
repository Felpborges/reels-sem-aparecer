#!/usr/bin/env python3
"""Sintetiza os 4 efeitos do reel de referência a partir do perfil medido no original (faixa de bateria separada pelo demucs):
impacto = grave 20-60 Hz, pico em ~0,15 s · pop = tom ~850 Hz, some em ~25 ms · clique = tom ~2,5 kHz (ou ~1,45 kHz), some em 5-10 ms
painel = grave + sopro de ruído largo, pico em ~0,1 s. Saída: assets/sfx/*.wav (48 kHz, normalizados a pico 0,9)."""
import numpy as np, soundfile as sf, os
SR = 48000; rng = np.random.default_rng(7)
t = lambda d: np.arange(int(SR * d)) / SR
def norm(y): return 0.9 * y / np.abs(y).max()
def fase(f): return 2 * np.pi * np.cumsum(f) / SR
def lp(x, fc):                                   # passa-baixa de 1 polo, aplicado duas vezes
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0
    for _ in range(2):
        s = 0
        for i, v in enumerate(x): s = (1 - a) * v + a * s; y[i] = s
        x = y.copy()
    return y
def bp(x, f0, q):                                # passa-faixa biquad
    w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q); b0, b1, b2 = al, 0, -al; a0, a1, a2 = 1 + al, -2 * np.cos(w), 1 - al
    y = np.zeros_like(x); x1 = x2 = y1 = y2 = 0
    for i, v in enumerate(x):
        o = (b0 * v + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2) / a0; x2, x1, y2, y1 = x1, v, y1, o; y[i] = o
    return y
os.makedirs("assets/sfx", exist_ok=True)
# impacto: seno 62 -> 34 Hz, sobe em 0,13 s e cai rápido, cauda grave curta + estalo de ar 4-8 kHz no ataque
tt = t(0.75); f = 34 + 28 * np.exp(-tt / 0.18)
env = np.where(tt < 0.13, (tt / 0.13) ** 1.5, np.exp(-(tt - 0.13) / 0.11))
imp = np.sin(fase(f)) * env + 0.5 * np.sin(fase(2 * f)) * env * 0.25
ar = bp(rng.standard_normal(len(tt)), 6000, 0.8) * np.exp(-tt / 0.03) * 0.05
sf.write("assets/sfx/impacto.wav", norm(imp + ar), SR)
# pop: tom 1050 -> 820 Hz em 25 ms, ataque 3 ms, queda exponencial (-20 dB em ~25 ms)
tt = t(0.12); f = 820 + 230 * np.exp(-tt / 0.012)
env = np.minimum(tt / 0.003, 1) * np.exp(-tt / 0.011)
sf.write("assets/sfx/pop.wav", norm(np.sin(fase(f)) * env + 0.08 * np.sin(fase(2 * f)) * env), SR)
# pop longo (cartão de capítulo): mesmo tom, cauda mais longa
env = np.minimum(tt / 0.004, 1) * np.exp(-tt / 0.03); tt2 = t(0.25); f2 = 820 + 230 * np.exp(-tt2 / 0.012)
env2 = np.minimum(tt2 / 0.004, 1) * np.exp(-tt2 / 0.045)
sf.write("assets/sfx/pop-longo.wav", norm(np.sin(fase(f2)) * env2 + 0.08 * np.sin(fase(2 * f2)) * env2), SR)
# cliques: tom curto + um pouco de ruído na mesma faixa
for nome, f0, tau in (("clique", 2550, 0.0035), ("clique-grave", 1450, 0.005)):
    tt = t(0.05); env = np.minimum(tt / 0.0008, 1) * np.exp(-tt / tau)
    y = np.sin(2 * np.pi * f0 * tt) * env + 0.35 * bp(rng.standard_normal(len(tt)), f0, 2.0) * env
    sf.write(f"assets/sfx/{nome}.wav", norm(y), SR)
# painel: grave 45 Hz + sopro de ruído largo (subida 0,09 s, queda 0,12 s)
tt = t(0.45); env = np.where(tt < 0.09, (tt / 0.09) ** 2, np.exp(-(tt - 0.09) / 0.1))
som = lp(rng.standard_normal(len(tt)), 7000) * env * 0.55
grave = np.sin(fase(30 + 25 * np.exp(-tt / 0.1))) * np.where(tt < 0.07, tt / 0.07, np.exp(-(tt - 0.07) / 0.12))
sf.write("assets/sfx/painel.wav", norm(grave + som), SR)
print("ok")
