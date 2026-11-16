#!/usr/bin/env python3
"""Efeitos do estilo D, SINTETIZADOS na forma medida no reel de referência — sem amostra de terceiros.
Catálogo e medidas: ../../pericia/audio/efeitos/CATALOGO.md. A referência usa pouco efeito e sempre preso a uma mudança
da imagem; cada som abaixo existe nela:
  boom      virada de capítulo: ruído largo de 10-90 Hz, ESTÉREO com L e R independentes; incha ~0,5 s ANTES do corte,
            golpe logo depois, platô de 0,5 s, -20 dB em ~0,95 s (largura de ~1,1 s a -12 dB)
  thump     cada rótulo que entra: tom FIXO de ~49 Hz, sobe 0,25 s, ~0,5 s de largura
  objeto    objeto branco que sobe no escuro: grave de ~52 Hz com varreduras descendentes de 100 a 40 Hz, ~1,1 s
  inchaco   sob o plano de colagem com pan: ruído de 10-70 Hz que cresce e some ANTES do corte seguinte
  golpe     objeto que entra na cena de cor: 43 Hz, 80 ms
  clique    cada palavra solta que aparece: estalo seco de ~4 ms, 2-8 kHz
  estalo    no corte para o CTA: rajada de ~60 ms, 0,5-12 kHz
  ar-ondas  ondas do diagrama: três sopros agudos (5-12 kHz) em ~0,9 s, só nos lados do estéreo
  ar-curto  punch-in e clique da mãozinha: um sopro agudo de ~0,25 s, só nos lados
uso: sfx_d.py <pasta>   -> <pasta>/*.wav e pre.json (segundos entre o começo do arquivo e o PICO do efeito; o mix põe
esse pico em t + metas.audio.pico_depois_s[tipo])."""
import sys, os, json, numpy as np, soundfile as sf, scipy.signal as sg
SR = 48000; out = sys.argv[1] if len(sys.argv) > 1 else "assets/sfx"; os.makedirs(out, exist_ok=True); rng = np.random.default_rng(7)
def filtro(x, fc, tipo, ordem=2): return sg.sosfilt(sg.butter(ordem, fc, tipo, fs=SR, output="sos"), x, axis=0)
def grava(nome, y, pico=0.9): sf.write(os.path.join(out, nome), (y / np.abs(y).max() * pico).astype(np.float32), SR)
def corpo_grave(n, lo=12, hi=40):
    r = rng.normal(0, 1, n + SR); r = filtro(filtro(r, hi, "low"), lo, "high")[SR:]; return r / np.sqrt(np.mean(r ** 2))
PRE = {}

PRE["boom"] = 0.65; n = int(2.4 * SR); t = np.arange(n) / SR; env = np.zeros(n)
a = t < 0.15; env[a] = 10 ** (-11 / 20) * (t[a] / 0.15) ** 2
b = (t >= 0.15) & (t < 0.65); env[b] = 10 ** ((-11 + 11 * (t[b] - 0.15) / 0.50) / 20)
u = t[t >= 0.65] - 0.65
db = np.where(u < 0.10, -5.5 * u / 0.10, np.where(u < 0.50, -5.5 - 2.0 * (u - 0.10) / 0.40, np.where(u < 0.95, -7.5 - 12.5 * (u - 0.50) / 0.45, -20 - 18 * (u - 0.95))))
env[t >= 0.65] = 10 ** (db / 20)
boom = np.vstack([corpo_grave(n) * env, corpo_grave(n) * env]).T; boom[-int(0.15 * SR):] *= np.linspace(1, 0, int(0.15 * SR))[:, None]; grava("boom.wav", boom)

PRE["thump"] = 0.25; n = int(1.0 * SR); t = np.arange(n) / SR
f = 47 + 4 * np.exp(-((t - 0.25) / 0.15) ** 2)
e = np.where(t < 0.25, (t / 0.25) ** 1.5, 0.5 * np.exp(-(t - 0.25) / 0.06) + 0.5 * np.exp(-(t - 0.25) / 0.33))
th = np.tanh(1.15 * np.sin(2 * np.pi * np.cumsum(f) / SR) * e) / np.tanh(1.15); th *= np.minimum(1, (1.0 - t) / 0.1); grava("thump.wav", th)

PRE["objeto"] = 0.43; n = int(1.5 * SR); t = np.arange(n) / SR      # começa 0,17 s ANTES do corte; pico 0,26 s depois dele
base = np.sin(2 * np.pi * 52 * t) * np.where(t < 0.43, (t / 0.43) ** 1.3, np.exp(-(t - 0.43) / 0.45))
var = np.zeros(n)
for t0 in (0.38, 0.68, 0.98):
    m = (t >= t0) & (t < t0 + 0.45); uu = (t[m] - t0) / 0.45; fq = 100 * 0.4 ** uu
    var[m] += 0.55 * np.sin(2 * np.pi * np.cumsum(fq) / SR) * np.sin(np.pi * uu) ** 0.8
ob = base + var; ob *= np.minimum(1, (1.5 - t) / 0.15); grava("objeto.wav", ob)

PRE["inchaco"] = 0.75; n = int(1.05 * SR); t = np.arange(n) / SR      # pico 0,65 s antes do corte SEGUINTE; some 0,35 s antes
ei = np.where(t < 0.75, (t / 0.75) ** 2, np.exp(-(t - 0.75) / 0.07)); ei *= np.minimum(1, (1.05 - t) / 0.05)
grava("inchaco.wav", np.vstack([corpo_grave(n, 10, 70) * ei, corpo_grave(n, 10, 70) * ei]).T, 0.7)

PRE["golpe"] = 0.02; n = int(0.12 * SR); t = np.arange(n) / SR
grava("golpe.wav", np.sin(2 * np.pi * 43 * t) * np.where(t < 0.02, t / 0.02, np.exp(-(t - 0.02) / 0.03)) * np.minimum(1, (0.12 - t) / 0.02))

n = int(0.02 * SR); k = np.arange(n); i0 = 48; c = np.zeros(n); PRE["clique"] = i0 / SR
for dt, amp in ((0.0, -1.0), (0.0001, 0.57), (0.00054, 1.0), (0.00065, -0.62), (0.0033, 0.62)): c[i0 + int(round(dt * SR))] += amp
c += rng.normal(0, 0.12, n) * np.exp(-np.maximum(0, (k - i0) / SR) / 0.0025) * (k >= i0)
c = filtro(filtro(c, 1700, "high"), 10000, "low"); c *= np.minimum(1, (n - k) / 96); grava("clique.wav", c)

n = int(0.09 * SR); t = np.arange(n) / SR; PRE["estalo"] = 0.004; r = rng.normal(0, 1, n)
es = sum(g * sg.sosfilt(sg.butter(2, [fc * 0.94, fc * 1.06], "band", fs=SR, output="sos"), r) for fc, g in ((1500, 0.9), (4000, 1.0), (6500, 0.8), (9000, 0.6)))
es += 0.25 * filtro(filtro(r, 500, "high"), 12000, "low")
ee = np.where(t < 0.004, t / 0.004, np.where(t < 0.045, 1 - 0.35 * (t - 0.004) / 0.041, 0.65 * np.exp(-(t - 0.045) / 0.008))); grava("estalo.wav", es * ee, 0.8)

def ar(dur, pulsos):
    n = int(dur * SR); t = np.arange(n) / SR; e = np.zeros(n)
    for c0, larg, g in pulsos: e += g * np.exp(-0.5 * ((t - c0) / larg) ** 2)
    l = filtro(filtro(rng.normal(0, 1, n), 5000, "high"), 12000, "low") * e; r_ = filtro(filtro(rng.normal(0, 1, n), 5000, "high"), 12000, "low") * e
    y = np.vstack([l, -r_ * 0.9 + l * 0.1]).T; y[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))[:, None]; return y
PRE["ar-ondas"] = 0.05; grava("ar-ondas.wav", ar(1.1, ((0.08, 0.05, 0.55), (0.40, 0.045, 1.0), (0.78, 0.09, 0.5))), 0.5)
PRE["ar-curto"] = 0.15; grava("ar-curto.wav", ar(0.36, ((0.17, 0.035, 1.0), (0.25, 0.03, 0.4))), 0.5)
json.dump(PRE, open(os.path.join(out, "pre.json"), "w"), indent=1)
print("sfx:", ", ".join(sorted(f[:-4] for f in os.listdir(out) if f.endswith(".wav"))))
