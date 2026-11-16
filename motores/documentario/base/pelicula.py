#!/usr/bin/env python3
"""MOTOR ESTILO D · a "pele da fita" (DESMONTE-D §4 e §6). Roda DEPOIS do render limpo a 10 fps.

uso: pelicula.py <limpo_10fps.mp4> <audio.m4a|wav> <saida.mp4> [semente]

Cadências medidas: conteúdo a 10 fps (cada quadro 3x a 30 fps); textura a 6 fps (muda a cada 5 quadros).
Por cima de TUDO, nesta ordem:
  teto de branco : joelho em 190, teto em 197 (na referência nenhum branco passa do branco do papel: 99,9 % do vídeo
                   abaixo de 209; texto branco ~190). Sem isso os títulos "acendem" 50 níveis acima do papel.
  separação RGB  : vermelho -1,5 px, azul +1,5 px (horizontal, uniforme)
  maciez         : desfoque gaussiano 0,6 px
  poeira/manchas : só nos escuros (pontos brancos esparsos, manchas verticais suaves, às vezes um risco)
  varredura      : período 5,4 px, multiplica até 12,3 %, a fase PULA a cada 1/6 s
  tremulação     : brilho ±1,5 % a cada 1/6 s
  grão           : gaussiano fino (sigma ~2,2 níveis), novo a cada 1/6 s
Saída: 1080x1920, 30 fps, H.264 + AAC (a subida de 720p para 1080p é parte do look macio do original), convertida e
MARCADA em BT.709 (sem a marcação o ffmpeg grava em BT.601 e os players leem como 709: o vermelho e o verde mudam).
"""
import sys, subprocess, json, numpy as np, cv2

ent, aud, sai = sys.argv[1], sys.argv[2], sys.argv[3]
SEM = int(sys.argv[4]) if len(sys.argv) > 4 else 11
W, H = 720, 1280
M = {"rgb_px": 1.5, "maciez": 0.6, "linha_periodo": 5.4, "linha_prof": 0.123, "tremula": 0.015, "grao": 2.2,
     "grao_ganho": 1.25, "poeira_n": 14, "manchas": 2.5, "escuro_lim": 70.0, "branco_joelho": 190.0, "branco_teto": 197.0}
# conferido contra o original (recriação): linhas 23 níveis pico a pico no papel, grão de alta frequência ~1,4,
# preto com desvio ~2,1, papel com média ~193 (as linhas são normalizadas para não escurecer a média)

probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                        "stream=nb_read_packets,r_frame_rate", "-of", "json", ent], capture_output=True, text=True)
info = json.loads(probe.stdout)["streams"][0]
n10 = int(info["nb_read_packets"]); fr = info["r_frame_rate"]
num, den = map(int, fr.split("/")); fps_in = num / den
rep = max(1, round(30 / fps_in))          # 10 fps -> 3 (se vier a 30 fps, pega 1 a cada 3 adiante)
print(f"entrada {n10} quadros a {fps_in:g} fps -> saída 30 fps (cada quadro x{rep})")

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", ent, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-i", aud, "-map", "0:v", "-map", "1:a",
                        "-vf", "scale=1080:1920:flags=lanczos:out_color_matrix=bt709:out_range=tv,format=yuv420p,"
                               "setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv",
                        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                        "-x264-params", "colorprim=bt709:transfer=bt709:colormatrix=bt709",
                        "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy" if aud.lower().endswith((".m4a", ".aac", ".mp4")) else "aac", "-b:a", "192k",
                        "-t", f"{n10 * rep / 30:.3f}", "-movflags", "+faststart", sai], stdin=subprocess.PIPE)

yy = np.arange(H, dtype=np.float32)[:, None, None]
rng_g = np.random.default_rng(SEM)
cache = {}


def textura(s):
    """Tudo o que muda a 6 fps, sorteado de forma determinística pelo passo s."""
    if s in cache:
        return cache[s]
    r = np.random.default_rng(SEM * 1000 + s)
    fase = r.uniform(0, M["linha_periodo"])
    linhas = 1 - M["linha_prof"] * (0.5 + 0.5 * np.cos(2 * np.pi * (yy + fase) / M["linha_periodo"]))
    linhas = linhas / linhas.mean()          # a média do quadro não escurece
    trem = 1 + r.uniform(-M["tremula"], M["tremula"])
    grao = r.normal(0, M["grao"], (H, W, 1)).astype(np.float32)
    grao = cv2.GaussianBlur(grao, (0, 0), 0.55)[..., None] * M["grao_ganho"]
    # poeira: pontos e fios brancos (aparecem só onde a imagem é escura)
    po = np.zeros((H, W), np.float32)
    for _ in range(r.integers(M["poeira_n"] // 2, M["poeira_n"])):
        x, y = int(r.uniform(0, W)), int(r.uniform(0, H)); rr = r.choice([1, 1, 1, 2, 2, 3])
        cv2.circle(po, (x, y), int(rr), float(r.uniform(60, 170)), -1)
    if r.uniform() < 0.35:   # um fio/risco curto às vezes
        x, y = int(r.uniform(0, W)), int(r.uniform(0, H)); a = r.uniform(0, np.pi)
        L = r.uniform(20, 90)
        cv2.line(po, (x, y), (int(x + L * np.cos(a)), int(y + L * np.sin(a))), float(r.uniform(40, 90)), 1)
    po = cv2.GaussianBlur(po, (0, 0), 0.7)
    # manchas verticais suaves (a "película" do preto)
    baixa = r.normal(0, 1, (40, 24)).astype(np.float32)
    man = cv2.resize(baixa, (W, H), interpolation=cv2.INTER_CUBIC)
    man = cv2.GaussianBlur(man, (0, 0), sigmaX=6, sigmaY=40) * M["manchas"]
    cache.clear()
    cache[s] = (linhas.astype(np.float32), trem, grao, po[..., None], man[..., None])
    return cache[s]


def processa(fr, s):
    img = fr.astype(np.float32)
    # teto de branco (joelho suave): acima do joelho os valores se comprimem até o teto; o papel quase não muda
    k, t = M["branco_joelho"], M["branco_teto"]
    img = np.where(img > k, k + (t - k) * (1 - np.exp(-(img - k) / (t - k))), img)
    # separação RGB (sub-pixel: média de dois deslocamentos inteiros)
    d = M["rgb_px"]; a, b = int(np.floor(d)), int(np.ceil(d)); w = d - a
    R = img[..., 0]; B = img[..., 2]
    Rl = (1 - w) * np.roll(R, -a, 1) + w * np.roll(R, -b, 1)
    Br = (1 - w) * np.roll(B, a, 1) + w * np.roll(B, b, 1)
    img = np.stack([Rl, img[..., 1], Br], -1)
    img = cv2.GaussianBlur(img, (0, 0), M["maciez"])
    linhas, trem, grao, po, man = textura(s)
    lum = img.mean(2, keepdims=True)
    escuro = np.clip((M["escuro_lim"] - lum) / M["escuro_lim"], 0, 1)
    img = img + escuro * (po + man)
    img = img * linhas * trem + grao
    return np.clip(img, 0, 255).astype(np.uint8)


n_out = 0; idx = 0; tam = W * H * 3
while True:
    buf = dec.stdout.read(tam)
    if len(buf) < tam:
        break
    fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    if rep == 1 and fps_in > 20:          # veio a 30 fps: posteriza aqui (segura 1 a cada 3)
        if idx % 3 == 0:
            hold = fr.copy()
        reps = [hold]
    else:
        reps = [fr] * rep
    for f in reps:
        enc.stdin.write(processa(f, n_out // 5).tobytes()); n_out += 1
    idx += 1
enc.stdin.close(); enc.wait(); dec.wait()
print(f"película: {n_out} quadros a 30 fps -> {sai}")
