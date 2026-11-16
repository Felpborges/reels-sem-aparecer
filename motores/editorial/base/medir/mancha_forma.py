"""Gera o contorno liso da mancha (estrela de 5 braços com pontas arredondadas e junções côncavas), como na referência.
Desenha miolo + braços em raster, funde tudo com desfoque + limiar (as junções viram curvas contínuas) e exporta um caminho SVG
em unidades de um viewBox -300..300. -> mancha_forma.json {"d": caminho, "miolo": raio do maior círculo inscrito}"""
import cv2, numpy as np, json, os, math
AQUI = os.path.dirname(os.path.abspath(__file__))
K = 4                                           # px por unidade
S = 600 * K; img = np.zeros((S, S), np.float32); c = S / 2
def disco(x, y, r): cv2.circle(img, (int(round(c + x * K)), int(round(c + y * K))), int(round(r * K)), 1.0, -1, cv2.LINE_AA)
disco(0, 0, 44)
#        ângulo, comprimento, curvatura, cintura, ponta
BRACOS = [(-8, 206, 15, 19.5, 26.5), (63, 188, -13, 18.5, 25.5), (136, 214, 11, 20, 27.5), (207, 182, -15, 18.5, 25), (281, 200, 13, 19, 26)]
for ang, comp, curva, cint, ponta in BRACOS:
    th = math.radians(ang); ex, ey = comp * math.cos(th), comp * math.sin(th)
    mx, my = ex / 2 - curva * math.sin(th), ey / 2 + curva * math.cos(th)
    for i in range(0, 401):
        s = i / 400; x = 2 * (1 - s) * s * mx + s * s * ex; y = 2 * (1 - s) * s * my + s * s * ey
        base = 30 * (1 - s) ** 3                                   # alarga perto do miolo
        bulbo = (ponta - cint) * max(0.0, (s - 0.55) / 0.45) ** 1.6     # engrossa até a ponta
        disco(x, y, cint + base + bulbo)
b = cv2.GaussianBlur(img, (0, 0), 9 * K)        # funde: junções côncavas e contorno contínuo
m = (b > 0.5).astype(np.uint8)
cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); ct = max(cs, key=cv2.contourArea)[:, 0, :].astype(np.float32)
# suaviza o contorno (média circular) e reduz o número de pontos
n = len(ct); w = 9; ker = np.ones(2 * w + 1) / (2 * w + 1)
xs = np.convolve(np.r_[ct[-w:, 0], ct[:, 0], ct[:w, 0]], ker, "valid"); ys = np.convolve(np.r_[ct[-w:, 1], ct[:, 1], ct[:w, 1]], ker, "valid")
pts = np.stack([xs, ys], 1)[::max(1, n // 420)]
d = "M" + " L".join(f"{(x - c) / K:.1f} {(y - c) / K:.1f}" for x, y in pts) + "Z"
dt = cv2.distanceTransform(m, cv2.DIST_L2, 5); miolo = float(dt.max()) / K
alc = float(np.max(np.hypot(pts[:, 0] - c, pts[:, 1] - c))) / K
json.dump({"d": d, "miolo": round(miolo, 2), "alcance": round(alc, 1)}, open(os.path.join(AQUI, "mancha_forma.json"), "w"))
cv2.imwrite(os.path.join(AQUI, "vis", "mancha_forma.png") if os.path.isdir(os.path.join(AQUI, "vis")) else os.path.join(AQUI, "mancha_forma.png"), cv2.resize(255 - m * 160, (600, 600), interpolation=cv2.INTER_AREA))
print("pontos:", len(pts), " miolo:", round(miolo, 2), " alcance:", round(alc, 1), " alcance/miolo:", round(alc / miolo, 2))
