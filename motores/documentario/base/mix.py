#!/usr/bin/env python3
"""MIXAGEM DO ESTILO D (DESMONTE-D §7): voz + cama musical + efeitos, em ESTÉREO, nos níveis medidos no original.
  voz   : no centro. Cama: estéreo. Efeitos: boom, inchaço e os "ares" são estéreo abertos; o resto vai no centro.
  kit   : assets/sfx (sintetizado por medir/sfx_d.py). Um reel pode trocar o kit inteiro com "sfx": "<pasta>" no
          projeto.json (a pasta precisa ter os mesmos nomes de arquivo e um pre.json).
  cama  : ~20 LU abaixo da voz (stem "other" do original -34 LUFS contra voz -14,3), contínua do 1º ao último quadro,
          em nível cheio até o fim (o fade-out embutido da faixa é descartado; fade final de 0,25 s)
  níveis e instantes de cada efeito: metas.json › audio › efeitos_rel_pico_voz_db e pico_depois_s (medidos na referência:
          boom -4 dB do pico da voz com o golpe 0,10 s depois do corte; thump -14,5 dB com pico 0,23 s depois da entrada;
          clique -3 dB no quadro em que a palavra aparece; ver ../pericia/audio/efeitos/CATALOGO.md)
  final : -14 LUFS integrado, true-peak -1 dB (o original: -14,2 LUFS), com GANHO FIXO + limitador (o loudnorm
          "linear" caía no modo dinâmico e mudava o nível dos efeitos ao longo do reel)"""
import os, json, subprocess, numpy as np, soundfile as sf, librosa
AQ = os.path.dirname(os.path.abspath(__file__)); SR = 48000
M = json.load(open(os.path.join(AQ, "medir", "metas.json")))["audio"]
PROJ = json.load(open(os.path.join(AQ, "projeto.json"))); ONS = json.load(open(os.path.join(AQ, "medir", "alinhamento.json")))
DUR = PROJ.get("duracao") or round(ONS[-1]["fim"] + 0.2, 1); N = int(DUR * SR)      # mesma cauda do build.py (CAUDA)
def lufs(p):
    o = subprocess.run(["ffmpeg", "-nostats", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float([l for l in o.splitlines() if l.strip().startswith("I:")][-1].split()[1])
nar0 = os.path.join(AQ, "assets", "narracao.wav"); nar = os.path.join(AQ, "assets", "_voz_comprimida.wav")
# voz compacta como a do original (LRA ~2): compressão suave, sem cortar nem acelerar nada
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", nar0, "-af", "acompressor=threshold=-24dB:ratio=3:attack=6:release=90:makeup=3,alimiter=limit=0.95:level=false",
                "-ar", str(SR), nar], check=True)
voz, _ = librosa.load(nar, sr=SR, mono=True)
def estereo(p):
    """Lê um arquivo como (amostras, 2): mono vai para o centro."""
    x, _ = librosa.load(p, sr=SR, mono=False); return x.T.copy() if x.ndim > 1 else np.stack([x, x], 1)
mix = np.zeros((N, 2)); nv = min(N, len(voz)); mix[:nv] += voz[:nv, None]
tmp_v = os.path.join(AQ, "assets", "_voz_centro.wav"); sf.write(tmp_v, mix, SR); lufs_voz = lufs(tmp_v); os.remove(tmp_v)
tr_p = next((os.path.join(AQ, "assets", f) for f in ("trilha.mp3", "trilha.wav", "trilha.m4a") if os.path.exists(os.path.join(AQ, "assets", f))), None)
if tr_p:
    tr = estereo(tr_p)
    ini = int(PROJ.get("trilha_inicio", 0.0) * SR); tr = tr[ini:]; trm = tr.mean(1)
    # só o trecho em NÍVEL CHEIO: o fade-out embutido da faixa é descartado (senão a cama some no fim do reel)
    h = SR // 2; nb = len(tr) // h
    db = np.array([20 * np.log10(np.sqrt(np.mean(trm[k * h:(k + 1) * h] ** 2)) + 1e-9) for k in range(nb)])
    cheio = np.where(db > np.median(db[db > db.max() - 20]) - 4)[0]
    if (cheio.max() + 1) * h < len(tr) - h:
        tr = tr[:(cheio.max() + 1) * h]
    if len(tr) < N:                          # faixa curta: laço para DENTRO do corpo da música, cruzamento de 2 s
        print(f"AVISO trilha: só {len(tr) / SR:.1f} s em nível cheio para {DUR} s de reel; emendada em laço (cruzamento de 2 s). "
              f"Prefira uma faixa com a duração do reel + 10 s, sem fade no fim.")
        x = int(2 * SR); corpo = tr.copy(); volta = int(min(len(corpo) * 0.25, 8 * SR))
        sai_, entra_ = np.cos(np.linspace(0, np.pi / 2, x))[:, None], np.sin(np.linspace(0, np.pi / 2, x))[:, None]
        while len(tr) < N:
            seg = corpo[volta:]; tr = np.concatenate([tr[:-x], tr[-x:] * sai_ + seg[:x] * entra_, seg[x:]])
    tr = tr[:N].copy(); f_ = int(0.3 * SR); tr[:f_] *= np.linspace(0, 1, f_)[:, None]; c_ = int(0.25 * SR); tr[-c_:] *= np.linspace(1, 0, c_)[:, None]
    tmp = os.path.join(AQ, "assets", "_trilha_corte.wav"); sf.write(tmp, tr, SR)
    g = 10 ** ((lufs_voz - M["cama_abaixo_da_voz_lu"] - lufs(tmp)) / 20); mix[:len(tr)] += tr * g; os.remove(tmp)
pk_voz = np.percentile(np.abs(voz[np.abs(voz) > 1e-4]), 99.5)
KIT = os.path.join(AQ, PROJ.get("sfx", os.path.join("assets", "sfx")))
pre = json.load(open(os.path.join(KIT, "pre.json"))); depois = M.get("pico_depois_s") or M.get("pico_depois_db", {}); faltam = set()
for s in json.load(open(os.path.join(AQ, "medir", "sons.json"))):
    arq = os.path.join(KIT, s["tipo"] + ".wav")
    if not os.path.exists(arq) or s["tipo"] not in M["efeitos_rel_pico_voz_db"]:
        faltam.add(s["tipo"]); continue
    x = estereo(arq)
    # O nível medido na referência é o do pico no CENTRO (L+R)/2. Num efeito estéreo aberto (boom, inchaço) o centro fica
    # ~4 dB abaixo de cada canal; normalizando pelo canal o boom saía 4,5 dB fraco. Efeito que só existe nos lados (os
    # "ares") não tem centro: aí vale o pico do canal.
    centro = np.abs(x.mean(1)).max(); canal = np.abs(x).max()
    x = x / ((centro if centro > 0.5 * canal else canal) + 1e-9) * pk_voz * 10 ** ((M["efeitos_rel_pico_voz_db"][s["tipo"]] + s.get("db", 0)) / 20)
    a = int((s["t"] + depois.get(s["tipo"], 0) - pre.get(s["tipo"], 0)) * SR)
    if a < 0: x = x[-a:]; a = 0
    b = min(N, a + len(x))
    if b > a: mix[a:b] += x[:b - a]
if faltam:
    print("AVISO efeitos: sem arquivo ou sem nível em metas.json para " + ", ".join(sorted(faltam)) + f" (kit: {KIT})")
sf.write(os.path.join(AQ, "assets", "mix_bruto.wav"), mix, SR)
# normalização com GANHO FIXO e limitador DEPOIS do ganho (o limitador só pega os picos da voz; os efeitos entram e
# saem com o mesmo nível relativo). O ganho é repetido até o integrado ficar a 0,15 LU da meta; o teto do limitador
# desce até o pico VERDADEIRO do AAC final ficar em -1 dBTP (a codificação passa ~1 dB do pico do WAV).
bruto = os.path.join(AQ, "assets", "mix_bruto.wav"); final = os.path.join(AQ, "assets", "mix.wav"); m4a = os.path.join(AQ, "assets", "mix.m4a")
def pico_verdadeiro(p):
    o = subprocess.run(["ffmpeg", "-nostats", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float([l for l in o.splitlines() if l.strip().startswith("Peak:")][-1].split()[1])
ganho = M["lufs"] - lufs(bruto); teto_db = -1.8
for _ in range(4):
    for _ in range(4):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", bruto, "-af",
                        f"volume={ganho:.2f}dB,alimiter=limit={10 ** (teto_db / 20):.4f}:attack=5:release=50:level=false:latency=true",
                        "-ar", "48000", final], check=True)
        erro = M["lufs"] - lufs(final)
        if abs(erro) <= 0.15:
            break
        ganho += erro
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", final, "-c:a", "aac", "-b:a", "192k", m4a], check=True)
    tp = pico_verdadeiro(m4a)
    if tp <= -0.95:
        break
    teto_db -= tp + 1.0 + 0.1
print(f"mix: ganho fixo {ganho:+.2f} dB · limitador {teto_db:.1f} dBFS -> {lufs(m4a):.1f} LUFS, pico verdadeiro {tp:.1f} dBTP")
os.remove(nar)
print(f"mix: cama {'ok' if tr_p else 'AUSENTE (assets/trilha.mp3)'} · {len(json.load(open(os.path.join(AQ, 'medir', 'sons.json'))))} efeitos · {M['lufs']} LUFS -> assets/mix.m4a")
