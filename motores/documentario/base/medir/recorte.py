#!/usr/bin/env python3
"""Recortes para as colagens do estilo D. uso: recorte.py <entrada> <saida.png> <modo> [largura_max]
  ia      : remove o fundo (rembg isnet) — sujeitos e objetos fotográficos
  traco   : desenho de linha preta sobre branco -> só o traço (alfa pela escuridão)
  branco  : objeto sobre branco liso -> alfa pela distância do branco (bom para multidão/P&B)
  moldura : moldura sobre branco -> tira o fundo E vaza a janela do centro (o arquivo entra por trás)
Saída recortada na caixa do conteúdo."""
import sys, numpy as np, cv2
from PIL import Image
ent, sai, modo = sys.argv[1:4]; lmax = int(sys.argv[4]) if len(sys.argv) > 4 else 1400
im = Image.open(ent).convert("RGB")
if im.width > lmax: im = im.resize((lmax, round(im.height * lmax / im.width)), Image.LANCZOS)
a = np.asarray(im).astype(np.float32)
if modo == "ia":
    from rembg import remove, new_session
    out = np.asarray(remove(im, session=new_session("isnet-general-use")))
elif modo == "traco":
    lum = a.mean(2); al = np.clip((200 - lum) / 120, 0, 1)
    out = np.dstack([np.full_like(lum, 18), np.full_like(lum, 18), np.full_like(lum, 22), al * 255]).astype(np.uint8)
elif modo == "branco":
    d = 255 - a.min(2); al = np.clip((d - 14) / 40, 0, 1); al = cv2.GaussianBlur(al, (0, 0), 0.8)
    out = np.dstack([a, al * 255]).astype(np.uint8)
elif modo == "moldura":
    from rembg import remove, new_session
    out = np.asarray(remove(im, session=new_session("isnet-general-use"))).copy()
    # janela: maior região quase branca conectada ao centro
    branco = (a.min(2) > 225).astype(np.uint8)
    h, w = branco.shape; mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(branco, mask, (w // 2, h // 2), 2)
    jan = branco == 2
    ys, xs = np.where(jan); print("janela (fração):", round(xs.min() / w, 3), round(ys.min() / h, 3), round((xs.max() - xs.min()) / w, 3), round((ys.max() - ys.min()) / h, 3))
    out[..., 3][jan] = 0
else:
    sys.exit("modo: ia|traco|branco|moldura")
al = out[..., 3]; ys, xs = np.where(al > 20)
out = out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
Image.fromarray(out, "RGBA").save(sai); print(sai, out.shape[1], "x", out.shape[0])
