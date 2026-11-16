#!/usr/bin/env python3
"""MIXAGEM DO ESTILO C: voz + trilha arranjada (medir/trilha_c.py) + efeitos, com os níveis medidos no original:
  voz -19,3 LUFS e trilha -24,5 LUFS no original = trilha ~5,2 LU abaixo da voz (cama PRESENTE, quase protagonista);
  efeitos: só o brilho dos flashes (o resto do "som" do C é a própria trilha); final -17,6 LUFS (o do original; ver metas)."""
import os, sys, json, subprocess, numpy as np, soundfile as sf, librosa
AQ = os.path.dirname(os.path.abspath(__file__)); SR = 48000
M = json.load(open(os.path.join(AQ, "medir", "metas.json")))["audio"]
PROJ = json.load(open(os.path.join(AQ, "projeto.json"))); ONS = json.load(open(os.path.join(AQ, "medir", "alinhamento.json")))
DUR = PROJ.get("duracao") or round(ONS[-1]["end"] + 0.5, 2); N = int(DUR * SR)
def lufs(p):
    o = subprocess.run(["ffmpeg", "-nostats", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float([l for l in o.splitlines() if l.strip().startswith("I:")][-1].split()[1])
voz, _ = librosa.load(os.path.join(AQ, "assets", "narracao.wav"), sr=SR, mono=True)
mix = np.zeros(N); mix[:min(N, len(voz))] += voz[:N]
tw = os.path.join(AQ, "assets", "trilha_arranjada.wav")
if os.path.exists(os.path.join(AQ, "assets", "trilha.mp3")):
    subprocess.run([sys.executable, os.path.join(AQ, "medir", "trilha_c.py"), str(DUR), tw], check=True)
    tr, _ = librosa.load(tw, sr=SR, mono=True); tr = np.pad(tr, (0, max(0, N - len(tr))))[:N]
    lv, lt = lufs(os.path.join(AQ, "assets", "narracao.wav")), lufs(tw)
    g = 10 ** ((lv - M["trilha_abaixo_da_voz_lu"] - lt) / 20); mix += tr * g
sf.write(os.path.join(AQ, "assets", "mix_sem_efeitos.wav"), mix, SR)
pre = json.load(open(os.path.join(AQ, "assets", "sfx", "pre.json"))) if os.path.exists(os.path.join(AQ, "assets", "sfx", "pre.json")) else {}
pk_voz = np.percentile(np.abs(voz[np.abs(voz) > 1e-4]), 99.5)
for s in json.load(open(os.path.join(AQ, "medir", "sons.json"))):
    x, _ = librosa.load(os.path.join(AQ, "assets", "sfx", s["tipo"] + ".wav"), sr=SR, mono=True)
    x = x / (np.abs(x).max() + 1e-9) * pk_voz * 10 ** ((M["efeitos_rel_voz_db"].get(s["tipo"], -10) + s.get("db", 0)) / 20)
    a = int((s["t"] - pre.get(s["tipo"], 0)) * SR)
    if a < 0: x = x[-a:]; a = 0
    b = min(N, a + len(x)); mix[a:b] += x[:b - a]
sf.write(os.path.join(AQ, "assets", "mix_bruto.wav"), mix, SR)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(AQ, "assets", "mix_bruto.wav"), "-af", f"loudnorm=I={M['lufs']}:TP=-1.0:LRA=7",
                "-ar", "48000", os.path.join(AQ, "assets", "mix.wav")], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(AQ, "assets", "mix.wav"), "-c:a", "aac", "-b:a", "192k", os.path.join(AQ, "assets", "mix.m4a")], check=True)
print(f"mix: trilha {'arranjada' if os.path.exists(tw) else 'AUSENTE (assets/trilha.mp3)'} · {M['lufs']} LUFS -> assets/mix.m4a")
