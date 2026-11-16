#!/usr/bin/env python3
"""Sintetiza os 6 efeitos do ESTILO B com o perfil medido no original (pericia/audio/eventos-sfx.json).
Cada arquivo começa em PRE segundos antes do instante do efeito (o mix.py desconta): o boom e o riser INCHAM
antes do corte e batem nele. uso: sfx_b.py [pasta]"""
import sys, os, json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR = 48000; D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "sfx")
os.makedirs(D, exist_ok=True); rng = np.random.default_rng(11)
def bp(x, a, b): return sosfilt(butter(2, [a, b], "bandpass", fs=SR, output="sos"), x)
def hp(x, a): return sosfilt(butter(2, a, "highpass", fs=SR, output="sos"), x)
def t(n): return np.arange(int(n * SR)) / SR
def norm(x, pk=0.9): return x / (np.abs(x).max() + 1e-9) * pk
PRE = {}
# boom: sopro 300-3000 Hz que incha 0,25 s + grave 62->48 Hz que bate no corte e cai em ~0,35 s
pre = 0.25; tt = t(pre + 0.6); n = len(tt); hit = int(pre * SR)
ar = np.zeros(n); ar[:hit] = (tt[:hit] / pre) ** 2.2; ar[hit:] = np.exp(-(tt[hit:] - pre) / 0.09)
sopro = bp(rng.normal(0, 1, n), 300, 3000) * ar * 0.35
f = 62 - 14 * np.clip((tt - pre) / 0.4, 0, 1); ph = 2 * np.pi * np.cumsum(f) / SR
sub = np.sin(ph) * np.where(tt < pre, (tt / pre) ** 3 * 0.3, np.exp(-(tt - pre) / 0.16)) * 1.0
boom = norm(sub + sopro); sf.write(f"{D}/boom.wav", boom, SR); PRE["boom"] = pre
# whoosh: sopro 1-3 kHz, 0,5 s, pico no meio (o instante marcado é o pico)
tt = t(0.55); env = np.sin(np.pi * tt / 0.55) ** 2
w = bp(rng.normal(0, 1, len(tt)), 900, 3200) * env; sf.write(f"{D}/whoosh.wav", norm(w, .8), SR); PRE["whoosh"] = 0.275
# riser: sopro que sobe de 0,8 para 8 kHz em 0,9 s e termina no corte
tt = t(0.95); x = rng.normal(0, 1, len(tt)); out = np.zeros(len(tt)); blk = 1200
for i in range(0, len(tt), blk):
    fr = 800 * (10 ** (i / len(tt))); seg = bp(x[max(0, i - 2400):i + blk], fr, min(fr * 1.8, 20000))[-len(x[i:i + blk]):]
    out[i:i + blk] = seg
r = out * (tt / 0.95) ** 2.5 * np.where(tt > 0.9, np.exp(-(tt - 0.9) / 0.02), 1); sf.write(f"{D}/riser.wav", norm(r, .7), SR); PRE["riser"] = 0.9
# clique: tom 3 kHz de 45 ms com ataque seco
tt = t(0.06); c = np.sin(2 * np.pi * 3000 * tt) * np.exp(-tt / 0.012) + hp(rng.normal(0, 1, len(tt)), 4000) * np.exp(-tt / 0.003) * 0.4
sf.write(f"{D}/clique.wav", norm(c, .8), SR); PRE["clique"] = 0.0
# pop: grave curto 180->110 Hz, 70 ms
tt = t(0.09); f = 180 - 70 * tt / 0.09; p = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.025)
sf.write(f"{D}/pop.wav", norm(p, .85), SR); PRE["pop"] = 0.0
# tecla: clique agudo ~5,6 kHz, 12 ms
tt = t(0.025); k = bp(rng.normal(0, 1, len(tt)), 4200, 7500) * np.exp(-tt / 0.004)
sf.write(f"{D}/tecla.wav", norm(k, .7), SR); PRE["tecla"] = 0.0
json.dump(PRE, open(f"{D}/pre.json", "w")); print("efeitos em", D, PRE)
