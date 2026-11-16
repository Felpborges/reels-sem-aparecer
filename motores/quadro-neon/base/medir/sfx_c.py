#!/usr/bin/env python3
"""ESTILO C · kit de efeitos sintetizado no FORMATO medido no original (pericia: resíduo depois de tirar a trilha, que se
repete por compasso; correção de 13/11 — a 1ª perícia disse "quase não há efeitos" e estava errada).
  whoosh   troca de cartão / flash: sopro de médios (pico ~600 Hz, 300-1500), incha 0,30 s, pico 0,07 s DEPOIS do corte,
           some em 0,12 s                                                    nível -3 dB vs p90 da voz
  sopro    entrada de texto grande (título, herói, tarja, prompt): versão curta e mais aguda do whoosh      -9 dB
  brilho   ícone/objeto que aparece: cintilação aguda (parciais 3-9 kHz que piscam), pico ~0,05 s, some em 0,45 s  -7 dB
  impacto  o DROP: sub que despenca 90->38 Hz + estalo + prato (ruído agudo que decai 1,4 s)              -1 dB
  risco    seta/arco que se desenham: ruído de caneta 2-6 kHz com granulação, 0,5 s                        -13 dB
uso: sfx_c.py pasta   (grava <tipo>.wav e pre.json = quanto do som vem ANTES do instante marcado)"""
import sys, os, json, numpy as np, soundfile as sf, scipy.signal as ss
D = sys.argv[1]; os.makedirs(D, exist_ok=True); SR = 48000; R = np.random.default_rng(7)
def bp(x, a, b, o=2): bb, aa = ss.butter(o, [a / (SR / 2), b / (SR / 2)], "band"); return ss.lfilter(bb, aa, x)
def norm(x): return x / (np.abs(x).max() + 1e-9) * 0.9
def t_(d): return np.arange(int(d * SR)) / SR
# whoosh: ruído com filtro que varre 350->900 Hz enquanto incha (0,30 s), corte rápido depois do pico
t = t_(0.50); n = R.standard_normal(len(t)); out = np.zeros_like(n); blk = 480
for i in range(0, len(t), blk):
    fc = 350 + 550 * min(1, t[i] / 0.37); out[i:i + blk] = bp(n[max(0, i - 2048):i + blk], fc * 0.55, fc * 1.9)[-len(t[i:i + blk]):]
env = np.where(t < 0.37, (t / 0.37) ** 2.2, np.exp(-(t - 0.37) / 0.045)); w = norm(out * env)
sf.write(os.path.join(D, "whoosh.wav"), w, SR)
# sopro: mais curto e agudo
t = t_(0.30); n = bp(R.standard_normal(len(t)), 700, 3200); env = np.where(t < 0.17, (t / 0.17) ** 2, np.exp(-(t - 0.17) / 0.04))
sf.write(os.path.join(D, "sopro.wav"), norm(n * env), SR)
# brilho: parciais agudos que piscam + ar
t = t_(0.55); x = np.zeros_like(t)
for f in (3150, 4200, 5300, 6650, 7900, 9100):
    a0 = R.uniform(0, 0.08); x += np.where(t > a0, np.sin(2 * np.pi * f * (t - a0)) * np.exp(-(t - a0) / R.uniform(0.08, 0.22)), 0) * (1 + 0.6 * np.sin(2 * np.pi * 23 * t))
x += 0.25 * bp(R.standard_normal(len(t)), 5000, 11000) * np.exp(-t / 0.12)
sf.write(os.path.join(D, "brilho.wav"), norm(x * np.minimum(1, t / 0.004)), SR)
# impacto: sub que despenca + estalo + prato longo
t = t_(1.6); f = 38 + 52 * np.exp(-t / 0.09); sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.35)
est = bp(R.standard_normal(len(t)), 1500, 6000) * np.exp(-t / 0.012)
prato = bp(R.standard_normal(len(t)), 4500, 15000, 1) * (np.exp(-t / 0.45) * 0.8 + 0.2 * np.exp(-t / 1.2)) * np.minimum(1, t / 0.003)
sf.write(os.path.join(D, "impacto.wav"), norm(1.0 * sub + 0.5 * est + 0.35 * prato), SR)
# risco: caneta (granulado agudo)
t = t_(0.5); g = (R.random(len(t)) < 0.02).astype(float); g = np.convolve(g, np.hanning(60), "same")
x = bp(R.standard_normal(len(t)), 2000, 6000) * (0.4 + g) * np.sin(np.pi * np.minimum(1, t / 0.5))
sf.write(os.path.join(D, "risco.wav"), norm(x), SR)
json.dump({"whoosh": 0.30, "sopro": 0.12, "brilho": 0.0, "impacto": 0.0, "risco": 0.0}, open(os.path.join(D, "pre.json"), "w"))
print("whoosh sopro brilho impacto risco")
