#!/usr/bin/env python3
"""MIXAGEM DO ESTILO B: voz + trilha + efeitos, com os níveis medidos no original (medir/metas.json -> audio).
- efeitos: pico de 10 ms de cada tipo no nível medido em relação ao p90 da voz; o arquivo começa `pre` s antes do instante
- trilha: 11,5 dB abaixo da voz (RMS com fala), automação de medir/trilha.json (TRILHA() em cenas.py), fades de 0,3 s
- final: -14,2 LUFS integrado. Saída: assets/mix.m4a (e assets/mix.wav)"""
import os, json, subprocess, numpy as np, soundfile as sf, librosa
AQ = os.path.dirname(os.path.abspath(__file__)); SR = 48000
M = json.load(open(os.path.join(AQ, "medir", "metas.json")))["audio"]
voz, sr = sf.read(os.path.join(AQ, "assets", "narracao.wav")); voz = voz.mean(1) if voz.ndim > 1 else voz
if sr != SR: voz = librosa.resample(voz, orig_sr=sr, target_sr=SR)
# LOCUÇÃO segurada antes de somar (medido no stem de voz da ref: pico de amostra até ~12 dB e pico de 10 ms até ~5,5 dB
# acima do p90 da voz; a narração crua chegava a 17,5 e 8,7). Sem isto o limitador final esmaga os efeitos junto com a voz.
def _segura(x, sr_):
    h = int(sr_ * 0.01); e = 20 * np.log10(np.array([np.sqrt(np.mean(x[i:i + h] ** 2)) for i in range(0, len(x) - h, h)]) + 1e-9)
    p = np.percentile(e[e > e.max() - 35], 90)
    red = np.maximum(0, e - (p + 3.0)) * (1 - 1 / 3.0)                           # compressor 3:1 acima de p90 + 3 dB
    for i in range(1, len(red)): red[i] = max(red[i], red[i - 1] * np.exp(-0.01 / 0.08))   # solta em 80 ms
    g = np.interp(np.arange(len(x)) / h, np.arange(len(red)) + 0.5, -red)
    x = x * 10 ** (g / 20)
    teto = 10 ** ((p + 11.5) / 20); gl = np.minimum(1, teto / (np.abs(x) + 1e-12))   # limitador de amostra: p90 + 11,5 dB
    w = int(sr_ * 0.002); gl = -np.convolve(-np.pad(gl, (w, w), constant_values=1), np.ones(1), "same")[w:-w]
    from scipy.ndimage import minimum_filter1d
    gl = minimum_filter1d(gl, 2 * w + 1); k = np.exp(-1 / (sr_ * 0.03))
    for i in range(1, len(gl)): gl[i] = min(gl[i], 1 - (1 - gl[i - 1]) * k)          # solta em 30 ms
    return x * gl
if M.get("segurar_voz", False): voz = _segura(voz, SR)   # DESLIGADO: o Felipe reprovou (13/11, "estragou e picotou o áudio")
ONS = json.load(open(os.path.join(AQ, "medir", "alinhamento.json")))
PROJ = json.load(open(os.path.join(AQ, "projeto.json")))
DUR = PROJ.get("duracao") or round(ONS[-1]["end"] + 0.35, 2)
N = int(DUR * SR); mix = np.zeros(N); mix[:min(N, len(voz))] += voz[:N]
def env10(x): h = int(SR * 0.01); return np.array([np.sqrt(np.mean(x[i:i + h] ** 2)) for i in range(0, len(x) - h, h)])
ev = 20 * np.log10(env10(voz) + 1e-9); fala = ev > ev.max() - 35
p90 = np.percentile(ev[fala], 90); rms_fala = 20 * np.log10(np.sqrt(np.mean(np.repeat(10 ** (ev[fala] / 10), 1))) + 1e-9)
# trilha
tp = os.path.join(AQ, "assets", "trilha.mp3")
if os.path.exists(tp):
    tr, _ = librosa.load(tp, sr=SR, mono=True); tr = np.resize(tr, N) if len(tr) < N else tr[:N]
    et = 20 * np.log10(np.sqrt(np.mean(tr ** 2)) + 1e-9); mk = np.zeros(len(voz), bool); rp = np.repeat(fala, int(SR * 0.01))[:len(voz)]; mk[:len(rp)] = rp
    voz_rms = 20 * np.log10(np.sqrt(np.mean(voz[mk] ** 2)) + 1e-9)
    g = 10 ** ((voz_rms - M["trilha_abaixo_da_voz_db"] - et) / 20)
    if M.get("trilha_absoluta"): g = 1.0          # a trilha já veio calibrada contra o p90 da voz (ex.: trilha_b2.py)
    auto = np.zeros(N); pts = json.load(open(os.path.join(AQ, "medir", "trilha.json"))) if os.path.exists(os.path.join(AQ, "medir", "trilha.json")) else []
    cur = 0.0; tt = np.arange(N) / SR; db = np.zeros(N)
    for p in sorted(pts, key=lambda p: p["t"]):
        a = int(p["t"] * SR); b = int((p["t"] + p["d"]) * SR)
        db[a:b] = np.linspace(cur, p["db"], max(1, b - a)); db[b:] = p["db"]; cur = p["db"]
    fade = np.minimum(1, np.minimum(tt / 0.3, (DUR - tt) / 0.5))
    mix += tr * g * 10 ** (db / 20) * np.clip(fade, 0, 1)
sf.write(os.path.join(AQ, "assets", "mix_sem_efeitos.wav"), mix, SR)   # voz + trilha: base do medir/provar_efeitos.py
# efeitos
pre = json.load(open(os.path.join(AQ, "assets", "sfx", "pre.json")))
for s in json.load(open(os.path.join(AQ, "medir", "sons.json"))):
    x, _ = librosa.load(os.path.join(AQ, "assets", "sfx", s["tipo"] + ".wav"), sr=SR, mono=True)
    pk = 20 * np.log10(env10(x).max() + 1e-9); alvo = p90 + M["efeitos_rel_voz_p90_db"].get(s["tipo"], -6) + s.get("db", 0)
    x = x * 10 ** ((alvo - pk) / 20); a = int((s["t"] - pre.get(s["tipo"], 0)) * SR)
    if a < 0: x = x[-a:]; a = 0
    b = min(N, a + len(x)); mix[a:b] += x[:b - a]
sf.write(os.path.join(AQ, "assets", "mix_bruto.wav"), mix, SR)
alvo = M["lufs"]
# volume final: loudnorm de uma passada (a cadeia que o Felipe aprovou para a voz). Tentar ganho fixo + limitador e voz
# comprimida (13/11) foi reprovado: "estragou e picotou o áudio".
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(AQ, "assets", "mix_bruto.wav"), "-af", f"loudnorm=I={alvo}:TP=-1.0:LRA=7",
                "-ar", "48000", os.path.join(AQ, "assets", "mix.wav")], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(AQ, "assets", "mix.wav"), "-c:a", "aac", "-b:a", "192k", os.path.join(AQ, "assets", "mix.m4a")], check=True)
print(f"mix: {len(json.load(open(os.path.join(AQ, 'medir', 'sons.json'))))} efeitos · trilha {'sim' if os.path.exists(tp) else 'NÃO (falta assets/trilha.mp3)'} · {alvo} LUFS -> assets/mix.m4a")
