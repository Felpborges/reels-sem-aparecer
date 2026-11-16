#!/usr/bin/env python3
"""ESTILO B · EXEMPLO (do reel-noticia-claude-code; troque o arquivo, os nomes de mundo e a batida do drop). Trilha a partir da OPÇÃO 3 escolhida pelo Felipe (13/11): "phonk escuro com caixinha de música",
gerada no Higgsfield (elevenlabs_music_v2_5, 40 s, brutos/trilhas/opcao-3.mp3) e separada no demucs em bateria / baixo /
melodia (medir/sep-trilha/htdemucs/opcao3). Montada na linha do tempo do reel com a forma da referência:
  0 → 13,4 s     a introdução original (só a caixinha de música)
  13,4 s         o 808 entra no corte do "resumo" (mundo 7)
  corpo          baixo + melodia, SEM bateria (a ref não tem bateria no corpo)
  1ª pausa       só a melodia, de "Só que…" (mundo 13) até a volta em "E quanto maior…" (mundo 16)
  reta           melodia baixa a partir de "Mas, na minha opinião" e quase silêncio em "na pausa"
  CTA            a bateria entra no corte, com o começo do drop original
A parte principal tem um ciclo de 8 compassos (fá x4, dó x4) que se repete; o áudio é levemente acelerado (~0,6 %) para que
o 808 em 13,42 s e o CTA em 74,93 s caiam os dois em começo de compasso (37 compassos entre eles).
Nível: corpo (baixo + melodia) ~18 dB abaixo do p90 da voz (a ref fica em -17,4); CTA ~4 dB acima do corpo.
uso: trilha_opcao3.py   (grava assets/trilha.mp3; metas.json -> audio.trilha_absoluta = true)"""
import os, json, subprocess, tempfile, numpy as np, soundfile as sf, librosa
AQ = os.path.dirname(os.path.abspath(os.path.join(__file__, ".."))); SR = 44100
E = json.load(open(os.path.join(AQ, "medir", "elementos.json"))); DUR = E["duracao"]; M = {m["nome"]: m["t"] for m in E["mundos"]}
ST = os.path.join(AQ, "medir", "sep-trilha", "htdemucs", "opcao3")
ENTRA_808, CTA = M["resumo"], M["cta"]
PAUSA1 = (M["passou"], M["gasto"]); RETA, SILENCIO = M["opiniao"], M["pausa"]

# ---- grade da fonte: batidas medidas -> período e compasso 0 do drop (batida 31, ~13,02 s)
y0, _ = librosa.load(os.path.join(AQ, "brutos", "trilhas", "opcao-3.mp3"), sr=SR, mono=True)
_, bt = librosa.beat.beat_track(y=y0, sr=SR, units="time")
k = np.arange(len(bt)); per, fase = np.polyfit(k, bt, 1)            # batida k = fase + k*per
D0 = fase + 31 * per                                                # 1º tempo do drop
BAR_ALVO = (CTA - ENTRA_808) / 37                                   # 37 compassos entre o 808 e o CTA
R = BAR_ALVO / (4 * per)                                            # fator de tempo (duração nova / antiga)
tmp = tempfile.mkdtemp(); S = {}
for nome in ("drums", "bass", "other"):
    subprocess.run(["rubberband", "-3", "-q", "-t", f"{R:.6f}", os.path.join(ST, nome + ".wav"), f"{tmp}/{nome}.wav"], check=True)
    x, sr = sf.read(f"{tmp}/{nome}.wav"); x = x if x.ndim > 1 else np.stack([x, x], 1)
    S[nome] = librosa.resample(x.T, orig_sr=sr, target_sr=SR).T if sr != SR else x
D0s, BAR = D0 * R, BAR_ALVO
N = int(DUR * SR); out = {n: np.zeros((N, 2)) for n in S}

def cola(dst, nome, t_ini, t_fim, src_ini, fade=0.02):
    """copia a fonte [src_ini, src_ini + (t_fim - t_ini)] para o reel [t_ini, t_fim], com fades curtos."""
    a, b = int(t_ini * SR), min(N, int(t_fim * SR)); s = int(src_ini * SR); n = min(b - a, len(S[nome]) - s)
    if n <= 0: return
    seg = S[nome][s:s + n].copy(); f = min(int(fade * SR), n // 2)
    seg[:f] *= np.linspace(0, 1, f)[:, None]; seg[n - f:] *= np.linspace(1, 0, f)[:, None]
    dst[nome][a:a + n] += seg

# introdução: termina exatamente onde o drop começa
cola(out, "other", max(0, ENTRA_808 - D0s), ENTRA_808 + 0.02, max(0, D0s - ENTRA_808), fade=0.05)
# parte principal em blocos de 8 compassos: A = compassos 0-7, B = 8-14 + o 7 de novo (o 15 da fonte é o fim que some)
def blocos(t0, t1):
    t, i = t0, 0
    while t < t1:
        ordem = range(8) if i % 2 == 0 else list(range(8, 15)) + [7]
        for c in ordem:
            if t >= t1: return
            yield t, min(t + BAR, t1), D0s + c * BAR
            t += BAR
        i += 1
for t_a, t_b, s in blocos(ENTRA_808, CTA):
    cola(out, "other", t_a, t_b + 0.01, s)
    if not (PAUSA1[0] <= t_a < PAUSA1[1]) and t_a < RETA:
        fim = min(t_b, PAUSA1[0]) if t_a < PAUSA1[0] < t_b else t_b
        cola(out, "bass", t_a, fim + 0.01, s, fade=0.06 if fim < t_b else 0.02)
# CTA: o drop do começo, com bateria
for nome in ("drums", "bass", "other"):
    cola(out, nome, CTA, DUR, D0s, fade=0.01)

# ---- dinâmica por trecho (dB)
t = np.arange(N) / SR
def curva(pts): ts, ds = zip(*pts); return 10 ** (np.interp(t, ts, ds) / 20)
# (na ref a melodia SOBE quando o baixo sai: a 1ª pausa fica no nível do corpo, a reta ~13 dB abaixo)
melodia = curva([(0, 8), (ENTRA_808 - 0.1, 8), (ENTRA_808, 0), (PAUSA1[0], 0), (PAUSA1[0] + 0.3, 9), (PAUSA1[1] - 0.3, 9), (PAUSA1[1], 0),
                 (RETA, 0), (RETA + 0.6, 3), (SILENCIO, 3), (SILENCIO + 0.8, -8), (CTA - 0.05, -8), (CTA, 0), (DUR, 0)])
mix = out["other"] * melodia[:, None] + out["bass"] + out["drums"]
cta = t >= CTA; mix[cta] *= 10 ** (4 / 20)
mix[-int(0.4 * SR):] *= np.linspace(1, 0, int(0.4 * SR))[:, None]

# ---- nível do corpo contra o p90 da voz (régua da perícia)
voz, sv = sf.read(os.path.join(AQ, "assets", "narracao.wav")); voz = voz.mean(1) if voz.ndim > 1 else voz
voz = librosa.resample(voz, orig_sr=sv, target_sr=SR) if sv != SR else voz
def env10(x): h = int(SR * 0.01); return np.array([np.sqrt(np.mean(x[i:i + h] ** 2)) for i in range(0, len(x) - h, h)])
ev = 20 * np.log10(env10(voz) + 1e-9); P90 = np.percentile(ev[ev > ev.max() - 35], 90)
corpo = mix[int(PAUSA1[1] * SR):int(RETA * SR)].mean(1); ec = 20 * np.log10(env10(corpo) + 1e-9)
mix *= 10 ** ((P90 - 18.0 - ec.mean()) / 20)
sf.write(f"{tmp}/t.wav", mix, SR)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{tmp}/t.wav", "-b:a", "320k", os.path.join(AQ, "assets", "trilha.mp3")], check=True)
print(f"opção 3 montada: {60 / per:.1f} -> {60 / (BAR / 4):.1f} bpm (fator {R:.4f}) · 808 em {ENTRA_808:.2f} s · CTA em {CTA:.2f} s · pico {np.abs(mix).max():.2f}")
