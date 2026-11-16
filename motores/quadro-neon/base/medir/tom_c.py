#!/usr/bin/env python3
"""ESTILO C · leva o TOM da narração para o do narrador da referência: grave e PLANO.
Medido no original (pericia/audio/sep/htdemucs/ref/vocals.wav): f0 mediana ~75 Hz, entonação 1,9 semitom de desvio,
ênfase 3,2 dB. Uma voz de TTS em PT sai ~130 Hz com 3,6-4,3 st (fala "cantada").
O que faz (Praat/PSOLA, formantes intactos, duração intacta):
  1. achata a melodia: cada ponto de f0 fica a FATOR do desvio original em relação à mediana (0,5 = metade);
  2. desce SEMITONS (padrão -5; abaixo de -6 a voz começa a soar artificial);
  3. EQ de locução e compressão leve (mesma cadeia do tom.py).
uso: tom_c.py entrada.wav saida.wav [semitons=-5] [fator=0.5]"""
import sys, os, numpy as np, soundfile as sf, parselmouth, subprocess, tempfile
from parselmouth.praat import call
ent, sai = sys.argv[1:3]
SEMI = float(sys.argv[3]) if len(sys.argv) > 3 else -5.0
FATOR = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
snd = parselmouth.Sound(ent)
if snd.n_channels > 1: snd = snd.convert_to_mono()
man = call(snd, "To Manipulation", 0.01, 60, 400)
tier = call(man, "Extract pitch tier")
n = call(tier, "Get number of points")
ts = [call(tier, "Get time from index", i) for i in range(1, n + 1)]
fs = np.array([call(tier, "Get value at index", i) for i in range(1, n + 1)])
med = np.median(fs); k = 2 ** (SEMI / 12)
novo = med * (fs / med) ** FATOR * k
call(tier, "Remove points between", 0, snd.duration + 1)
for t, f in zip(ts, novo): call(tier, "Add point", t, float(f))
call([tier, man], "Replace pitch tier")
out = call(man, "Get resynthesis (overlap-add)")
tmp = tempfile.mkdtemp(); p = os.path.join(tmp, "p.wav"); out.save(p, "WAV")
tom = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tom.py")
subprocess.run([sys.executable, tom, p, sai, "0"], check=True, capture_output=True)   # só EQ + compressão (sem mudar o tom de novo)
print(f"tom_c: f0 {med:.0f} -> {med * k:.0f} Hz · melodia x{FATOR} · {sai}")
