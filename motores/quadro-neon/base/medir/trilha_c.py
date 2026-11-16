#!/usr/bin/env python3
"""ESTILO C · ARRANJA a trilha pela estrutura do argumento (medido no original, DESMONTE-C.md §10):
  intro sem bumbo (teclas, pads, grave) -> 'baixo_sai' (o grave some: tensão) -> riser -> DROP no 1º exemplo
  -> groove cheio nas provas -> BREAK no título-síntese (bumbo e grave somem) -> 'volta' no 1º item da lista -> groove até o fim.
Como: a trilha gerada (assets/trilha.mp3, com intro sem bateria e um drop) é separada em stems com demucs (cache em
assets/trilha-stems/) e tocada CONTÍNUA com um deslocamento que põe o drop dela exatamente no 'drop' do reel; bateria e
grave são ligados/desligados pelos eventos de medir/musica.json (MUSICA() no cenas.py). 'volta' cai no tempo forte mais
próximo. Se a trilha acabar antes do reel, o groove é repetido em blocos de 4 tempos.
uso: trilha_c.py DURACAO saida.wav"""
import os, sys, json, subprocess, numpy as np, soundfile as sf, librosa, scipy.signal as ss
AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SR = 44100
DUR = float(sys.argv[1]); SAI = sys.argv[2]
TR = os.path.join(AQ, "assets", "trilha.mp3"); ST = os.path.join(AQ, "assets", "trilha-stems")
if not os.path.exists(os.path.join(ST, "drums.wav")):
    tmp = os.path.join(AQ, "assets", "_sep")
    subprocess.run([sys.executable, "-m", "demucs", "-n", "htdemucs", "-o", tmp, TR], check=True, capture_output=True)
    nome = os.path.splitext(os.path.basename(TR))[0]; os.makedirs(ST, exist_ok=True)
    for s in ("drums", "bass", "other", "vocals"): os.replace(os.path.join(tmp, "htdemucs", nome, s + ".wav"), os.path.join(ST, s + ".wav"))
S = {s: librosa.load(os.path.join(ST, s + ".wav"), sr=SR, mono=True)[0] for s in ("drums", "bass", "other", "vocals")}
S["other"] = S["other"] + S["vocals"]                       # restos tonais
dr = S["drums"]
# --- drop da trilha: maior salto de energia da bateria (janela de 50 ms) depois de um trecho sem bateria
h = int(SR * 0.05); e = np.array([np.sqrt(np.mean(dr[i:i + h] ** 2)) + 1e-9 for i in range(0, len(dr) - h, h)]); edb = 20 * np.log10(e)
pico = np.percentile(edb[int(len(edb) * 0.35):int(len(edb) * 0.7)], 90)     # nível dos ataques do groove (bumbo/caixa)
i_drop = int(np.argmax(edb > pico - 8)); SRC_DROP = i_drop * 0.05           # 1º ataque de groove = o drop (o riser não chega lá)
tempo, beats = librosa.beat.beat_track(y=(dr + S["bass"]).astype(np.float32), sr=SR, units="time")
PER = 60 / float(np.atleast_1d(tempo)[0])
ev = {x["ev"]: x["t"] for x in json.load(open(os.path.join(AQ, "medir", "musica.json")))}
t_drop = ev.get("drop", 11.0); OFF = SRC_DROP - t_drop
N = int(DUR * SR); tt = np.arange(N) / SR; src = tt + OFF
fim_groove = len(dr) / SR - 12.0                             # a trilha gerada tem ~10 s de saída: não usar
def pega(y, s):
    s = s.copy()
    alem = s > fim_groove
    if alem.any():                                           # repete o groove em blocos de 4 tempos
        bloco = 4 * PER * max(1, int((fim_groove - SRC_DROP) / (4 * PER)) // 2)
        s[alem] = fim_groove - bloco + ((s[alem] - fim_groove) % bloco)
    i = np.clip((s * SR).astype(int), 0, len(y) - 1); v = y[i]; v[s < 0] = 0; return v
def env(pts, n=N):
    """pts = [(t, valor)] em degraus com rampa de 60 ms"""
    g = np.ones(n); cur = 1.0
    for t, v in sorted(pts):
        a = int(t * SR); b = min(n, a + int(0.06 * SR))
        if a >= n: break
        g[a:b] = np.linspace(cur, v, max(1, b - a)); g[b:] = v; cur = v
    return g
beat = lambda t: t_drop + round((t - t_drop) / PER) * PER
gd = [(0, 0.0), (t_drop - 0.02, 1.0)]; gb = [(0, 1.0)]
if "baixo_sai" in ev: gb += [(ev["baixo_sai"], 0.0), (t_drop - 0.02, 1.0)]
if "break" in ev:
    gd += [(ev["break"] - 0.05, 0.0)]; gb += [(ev["break"] + 0.5, 0.25)]
    v = beat(ev.get("volta", ev["break"] + 2.5)); gd += [(v - 0.02, 1.0)]; gb += [(v - 0.02, 1.0)]
drums = pega(dr, src) * env(gd)
pre = (tt < t_drop)
drums[pre] = 0.0
# riser: o "build" da própria trilha nos 1,3 s antes do drop (o original tem ruído subindo + prato no fim do intro, 9,6-10,8 s)
jan = pre & (tt > t_drop - 1.3)
drums[jan] = pega(dr, src)[jan] * np.linspace(0.3, 1.0, jan.sum())
musica = drums + pega(S["bass"], src) * env(gb) + pega(S["other"], src)
fade = np.clip(np.minimum(tt / 0.25, (DUR - tt) / 0.6), 0, 1); musica *= fade
sf.write(SAI, musica, SR)
print(f"trilha: drop da fonte {SRC_DROP:.2f} s -> {t_drop:.2f} s no reel · {60 / PER:.1f} bpm · eventos {ev}")
