#!/usr/bin/env python3
"""Trata imagens geradas para o motor. Saída em assets/img/.
  recortar.py recorte brutos/x.png [--pb] [--larg 900]        recorte com fundo transparente (pessoa/objeto em fundo branco)
  recortar.py foto brutos/x.png [--pb] [--larg 1080]          foto (tela cheia, cartão, painel) reduzida, em jpg
  recortar.py retoque brutos/x.png CX CY R                     apaga um logo de terceiros (CX, CY, R em fração da largura/altura)
--pb = preto e branco (todo recorte de PESSOA no molde A é P&B; objetos ficam coloridos)."""
import sys, os
from PIL import Image
a = sys.argv; modo, ent = a[1], a[2]; pb = "--pb" in a
larg = int(a[a.index("--larg") + 1]) if "--larg" in a else (900 if modo == "recorte" else 1080)
nome = os.path.splitext(os.path.basename(ent))[0]
if modo == "retoque":
    import cv2, numpy as np
    im = cv2.imread(ent); h, w = im.shape[:2]; m = np.zeros((h, w), np.uint8)
    cv2.circle(m, (int(float(a[3]) * w), int(float(a[4]) * h)), int(float(a[5]) * w), 255, -1)
    cv2.imwrite(ent, cv2.inpaint(im, m, 9, cv2.INPAINT_TELEA)); print("retocado:", ent); sys.exit()
im = Image.open(ent).convert("RGB")
if pb: im = im.convert("L").convert("RGB")
if modo == "recorte":
    from rembg import remove, new_session
    out = remove(im, session=new_session("isnet-general-use"))
    out = out.crop(out.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()); out.thumbnail((larg, larg * 2))
    out.save(f"assets/img/{nome}.png"); print(f"assets/img/{nome}.png", out.size)
else:
    im.thumbnail((larg, larg * 2)); im.save(f"assets/img/{nome}.jpg", quality=90); print(f"assets/img/{nome}.jpg", im.size)
