#!/usr/bin/env python3
"""ESTILO B · acha os 4 cantos de uma superfície lisa numa foto (tela de aparelho, papel, lousa, chip) para o quad=.
uso: superficie.py foto.jpg x y [tolerância=18]     (x, y = um ponto DENTRO da superfície, em coordenadas do palco 720x1280)
Faz flood-fill pela cor a partir do ponto, pega o contorno e aproxima um quadrilátero. Imprime [(TL), (TR), (BR), (BL)]
e grava foto-superficie.jpg com o contorno desenhado para conferir no olho."""
import sys, numpy as np, cv2
img = cv2.imread(sys.argv[1]); H, W = img.shape[:2]; k = W / 720
x, y = int(float(sys.argv[2]) * k), int(float(sys.argv[3]) * k); tol = int(sys.argv[4]) if len(sys.argv) > 4 else 18
blur = cv2.GaussianBlur(img, (9, 9), 0); mask = np.zeros((H + 2, W + 2), np.uint8)
cv2.floodFill(blur, mask, (x, y), (0, 0, 255), (tol,) * 3, (tol,) * 3, cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE | (255 << 8) | 8)
m = mask[1:-1, 1:-1]; m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); c = max(cs, key=cv2.contourArea)
hull = cv2.convexHull(c); per = cv2.arcLength(hull, True); q = None
for e in np.linspace(0.01, 0.1, 40):
    a = cv2.approxPolyDP(hull, e * per, True)
    if len(a) == 4: q = a.reshape(4, 2); break
if q is None: q = cv2.boxPoints(cv2.minAreaRect(c)).astype(int)
s = q.sum(1); d = np.diff(q, axis=1).ravel()
tl, br, tr, bl = q[np.argmin(s)], q[np.argmax(s)], q[np.argmin(d)], q[np.argmax(d)]
out = [tuple(int(round(v / k)) for v in p) for p in (tl, tr, br, bl)]
print(out)
dbg = img.copy(); cv2.polylines(dbg, [np.array([tl, tr, br, bl])], True, (255, 0, 255), max(2, int(3 * k)))
cv2.imwrite(sys.argv[1].rsplit(".", 1)[0] + "-superficie.jpg", cv2.resize(dbg, (720, 1280)))
