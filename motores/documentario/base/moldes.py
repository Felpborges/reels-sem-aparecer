"""MOTOR ESTILO D · os MOLDES: os tipos de plano medidos na referência (DESMONTE-D §2), com câmera, texto e som
já nos números medidos. cenas.py só escolhe o molde, a imagem e as palavras.

Convenção: `t` = início do plano (use CORTE(i) = 0,07 s antes da 1ª palavra que o plano ilustra); `idx` = índices das
palavras faladas (alinhamento). O plano vai até o começo do próximo. Coordenadas no palco 720x1280.
Famílias e onde aparecem no original:
  titulo_digitado   ESCURO-DIGITA     plano 1        caixa-alta digitada com queda, push-in, sai em chicote
  colagem           COLAGEM           planos 2-3     papel + recorte P&B + 1 elemento de cor + legenda serifada (+ seta, punch)
  documento         DOCUMENTO-DIGITA  plano 4        documento apagado + caixa-alta minúscula digitada com cursor, punch e seleção azul
  objeto_escuro     ESCURO-OBJETO     plano 5        petróleo + objeto branco que sobe + frase caixa-alta palavra a palavra + thump
  arquivo           ARQUIVO           6,7,10,17,18,20 filme/foto de arquivo cobrindo a tela (+ retícula, brilhos, legenda serifada digitada)
  palavras          PALAVRAS          planos 8, 15   uma palavra serifada por vez no centro
  diagrama          DIAGRAMA          plano 9        documento apagado afastando + desenho em traço + ondas de cor + título em bloco + boom
  cena_cor          CENA-COR          plano 11       degradê azul + objeto sobe + papel rasgado + anéis + consequência (fica vermelho e cai)
  descarte          DESCARTE          plano 12       o desenho amassado cai num cesto de cor numa sala P&B
  anos              ANOS              plano 13       contador de anos rolando
  foto              FOTO              plano 14       foto real com push-in (+ boom na virada de capítulo)
  rotulos           ESCURO-RÓTULOS    plano 16       anéis + rótulos azuis em cascata (thump em cada)
  quadro            QUADRO            plano 19       o arquivo vira um quadro dourado no papel + legenda de 2 linhas
  cta_icone         ESCURO-ÍCONE      plano 21       ícone + mãozinha que clica, zoom-out longo, boom
  cta_campo         TELA              plano 22       print borrado entra pela direita + campo com o texto digitado
"""
from build import *


def _desde(t, x):
    return max(x, t + PASSO)


_PLANOS_DE_PALAVRAS = [0]      # o clique da referência é mais forte no 1º plano de palavras e mais baixo nos seguintes


# ---------------------------------------------------------------- 1 · ESCURO-DIGITA
def titulo_digitado(t, txt, idx, size=60, y=640, cps=None, aproxima=(0.56, 1.0), tau=0.15):
    pl = plano(t, "preto", cam={"tipo": "aproxima", "de": aproxima[0], "ate": aproxima[1], "tau": tau},
               saida={"tipo": "chicote", "x": -27, "b": 3}, nome="titulo_digitado")
    s = cabe(txt, "caixa", size, 600)
    digita_queda(pl, txt, W / 2, y, s, "caixa", "#f2f2f2", tempos_letras(txt, idx, cps))
    return pl


# ---------------------------------------------------------------- 2-3 · COLAGEM
def colagem(t, imgs, legenda=None, seta_d=None, cam=None, punch_em=None, punch_escala=1.8, punch_origem="62% 34%",
            saida="borrao", fundo="papel"):
    """imgs: [dict(src, x, y, w, cinza, sombra, ent, d, de, t)] na ordem de baixo para cima.
    legenda: dict(txt, idx, x, y, size, cor, ritmo, no_corte) — corpo 41 px (medido). Por padrão já está inteira no 1º
    quadro do plano (medido: "her beauty" a 100 % desde o corte); no_corte=False revela palavra a palavra com a voz.
    punch_em: tempo do punch-in (início da palavra-chave)."""
    pl = plano(t, fundo, cam=cam or {"tipo": "pan", "x": 70, "tau": 0.35},
               saida={"tipo": "borrao", "d": 0.2, "b": 4} if saida == "borrao" else None, nome="colagem")
    for im in imgs:
        im = dict(im); src = im.pop("src"); x = im.pop("x"); y = im.pop("y"); w = im.pop("w")
        img(pl, src, x, y, w, **im)
    if legenda:
        L = legenda
        size = cabe(L["txt"].replace("\n", " "), "serifa", L.get("size", 41), L.get("maxw", 520))
        _, ids = texto(pl, L["txt"], L["x"], L["y"], size, "serifa", L.get("cor", TINTA), L.get("alinha", "centro"))
        if L.get("no_corte", True):
            for sid in ids:
                setar(sid, 0, {"opacity": 0}); setar(sid, g(t), {"opacity": 1})
        else:
            revela(ids, tempos_revela(L["idx"], t0=_desde(t, P(L["idx"][0]) - 0.1), ritmo=L.get("ritmo")))
        if L.get("some_no_punch") and punch_em:      # medido: cai a ~34 % um passo antes do punch, 30 % no punch, 50 %, inteira
            for sid in ids:
                setar(sid, g(punch_em) - PASSO, {"opacity": 0.34}); setar(sid, g(punch_em), {"opacity": 0.3})
                setar(sid, g(punch_em) + PASSO, {"opacity": 0.5}); setar(sid, g(punch_em) + 2 * PASSO, {"opacity": 1})
    if seta_d:
        seta(pl, seta_d, t)
    if punch_em:
        punch(pl, punch_em, punch_escala, punch_origem)
        SOM("ar-curto", g(punch_em))                  # o sopro agudo do punch-in
        if legenda:     # quadro seguro: onde a legenda vai parar depois do punch-in
            ox, oy = [float(v[:-1]) / 100 * (W if k == 0 else H) if v.endswith("%") else float(v[:-2]) for k, v in enumerate(punch_origem.split())]
            wl = largura(legenda["txt"].split("\n")[0], "serifa", size) * punch_escala
            cx = ox + punch_escala * (legenda["x"] - ox); cy = oy + punch_escala * (legenda["y"] - oy)
            if cx - wl / 2 < 24 or cx + wl / 2 > W - 24 or cy < 120 or cy > H - 260:
                print(f"AVISO quadro seguro: a legenda '{legenda['txt']}' sai do quadro depois do punch-in (centro {cx:.0f},{cy:.0f}, "
                      f"largura {wl:.0f}). Aproxime a legenda do ponto de origem do punch.")
    return pl


# ---------------------------------------------------------------- 4 · DOCUMENTO-DIGITA
def documento(t, doc_src, txt, idx, chave, x0=148, y=640, size=27, punch_escala=2.1, doc_opac=0.55, cps_chave=25, doc_borrao=0.0,
              doc_escala=1.25):
    """txt em caixa-alta; chave = (i0, i1) em PALAVRAS de txt (a palavra-chave, selecionada e com punch-in no início dela)."""
    pl = plano(t, "cor:#bab3a2", cam={"tipo": "pan", "x": 60, "x1": -40, "tau": 0.5}, saida={"tipo": "zoom", "d": 0.4, "s": 0.755},
               nome="documento")
    img(pl, doc_src, W / 2, H / 2, W * doc_escala, filtro=f"grayscale(.6) sepia(.35) contrast(.7) brightness(1.06) opacity({doc_opac}) blur({doc_borrao}px)")
    pals = txt.split(" ")
    i0, i1 = chave
    letras = tempos_letras(txt, idx)
    # a palavra-chave é digitada a ~25 c/s (medido: TECHNOLOGY em 0,3 s) começando NA palavra falada
    pos = sum(len(p) + 1 for p in pals[:i0])
    tk = P(idx[i0]) + 0.1
    nch = len(" ".join(pals[i0:i1 + 1]))
    for j in range(nch):
        letras[pos + j] = tk + j / cps_chave
    # punch-in com origem no começo da palavra-chave. O punch e a seleção acompanham os tempos FINAIS das letras: se a
    # frase não cabe no plano, a digitação é comprimida para a palavra-chave ficar inteira e nítida antes da saída.
    xk = x0 + largura(" ".join(pals[:i0]) + " ", "caixa", size)
    ox = (punch_escala * xk - 250) / (punch_escala - 1)
    _, ids = digita_cursor(pl, txt, x0, y, size, "caixa", "#141414", letras, sel=(pos, pos + nch), sel_antes=0.1,
                           depois=lambda L: punch(pl, L[pos] - 0.1, punch_escala, f"{ox:.0f}px {y}px", desfoque=0))
    return pl


# ---------------------------------------------------------------- 5 · ESCURO-OBJETO
def objeto_escuro(t, obj_src, txt, idx, obj_w=470, obj_y=760, txt_y=490, size=53, cinza=True):
    pl = plano(t, "petroleo", cam={"tipo": "afasta", "de": 1.48, "ate": 1.0, "tau": 0.38, "origem": "50% 55%"}, nome="objeto_escuro")
    img(pl, obj_src, W / 2, obj_y, obj_w, t=t, ent="sobe", d=1.6, de=560, cinza=cinza,
        filtro="brightness(1.08) contrast(1.05)")
    s = cabe(txt, "caixa", size, 560)
    _, ids = texto(pl, txt, W / 2, txt_y, s, "caixa", "#f0f0ee")
    revela(ids, [_desde(t, P(i)) for i in idx])
    SOM("objeto", t)                                  # o grave com varreduras do objeto que sobe (começa antes do corte)
    return pl


# ---------------------------------------------------------------- 6/7/10/17/18/20 · ARQUIVO
def arquivo(t, src, inicio=0.0, cam=None, cinza=False, pontos=False, filtro="", legenda=None, brilho=None,
            desfoca_fim=None, saida=None, vel=1.0, ajuste="cover", enquadra=None):
    """src = .mp4 (filme) ou imagem. legenda = dict(txt, idx, x, y, size, cor) digitada com queda (serifada, corpo 66 px:
    a legenda de arquivo da referência ocupa 40 % da largura). Ponha a legenda sobre área ESCURA da imagem.
    brilho = dict(pontos=[(x,y),...], tam). desfoca_fim = segundos de desfoque antes do corte (vira o quadro).
    enquadra = (escala, fx, fy): a MESMA imagem num enquadramento mais fechado, centrado no ponto (fx, fy) da imagem
    (frações 0-1). É o recurso da referência para ter dois planos de um mesmo material (planos 17 e 18): serve para
    dividir um trecho longo sem imagem nova. A legenda não é ampliada junto."""
    sa = saida
    if desfoca_fim:
        sa = {"tipo": "borrao", "d": desfoca_fim, "b": 8}
    pl = plano(t, "preto", cam=cam or {"tipo": "afasta", "de": 1.35, "ate": 1.0, "tau": 0.3}, saida=sa, nome="arquivo")
    if src.lower().endswith((".mp4", ".mov", ".webm")):
        video(pl, src, inicio, cinza=cinza, pontos=pontos, filtro=filtro, vel=vel)
    else:
        e, fx, fy = enquadra or (1.0, 0.5, 0.5)
        ix = min(W * e / 2, max(W - W * e / 2, W / 2 + (0.5 - fx) * W * e))       # nunca mostra a borda da imagem
        iy = min(H * e / 2, max(H - H * e / 2, H / 2 + (0.5 - fy) * H * e))
        img(pl, src, ix, iy, W * e, H * e, cinza=cinza, pontos=pontos, filtro=filtro, ajuste=ajuste)
        anim(f'{pl["id"]}z', t, {"scale": 1.0}, {"scale": 1.10}, 4.0, "none")     # a foto respira como filme
    if legenda:
        L = legenda
        s = cabe(L["txt"], "serifa", L.get("size", 66), 600)
        digita_queda(pl, L["txt"], L.get("x", W / 2), L.get("y", 640), s, "serifa", L.get("cor", "#f4f2ee"),
                     tempos_letras(L["txt"], L["idx"], L.get("cps", 10)), queda=0.45)
    if brilho:
        brilhos(pl, brilho["pontos"], t, 99, brilho.get("tam", 34))
    return pl


def foto(t, src, de=1.0, ate=1.36, tau=0.33, boom=False, cinza=False, origem="50% 45%", legenda=None, enquadra=None):
    pl = arquivo(t, src, cam={"tipo": "aproxima", "de": de, "ate": ate, "tau": tau, "origem": origem}, cinza=cinza, legenda=legenda,
                 enquadra=enquadra)
    if boom:
        SOM("boom", t)
    return pl


# ---------------------------------------------------------------- 8/15 · PALAVRAS
def palavras(t, itens, size=64, y=640, fim=None, vazio=False):
    """itens = [(texto, idx)] ou [(texto, idx, (logo, altura_px))]. Cada palavra entra NO início falado (−0,05 s) e é
    trocada SECA pela próxima: fica na tela até a seguinte entrar (na referência não há quadro vazio entre as palavras
    do plano 8). vazio=True devolve o comportamento antigo (some 0,08 s depois de falada quando há pausa).
    Com logo: o logo OFICIAL + o nome."""
    pl = plano(t, "papel", nome="palavras")
    seq = []
    for k, it in enumerate(itens):
        txt, i = it[0], it[1]
        a = _desde(t, P(i) - 0.05) if k else max(t, P(i) - 0.05)
        if k + 1 < len(itens):
            prox = P(itens[k + 1][1]) - 0.05
            b = min(prox, F(i) + 0.08) if vazio and prox - F(i) >= 0.12 else prox
        else:
            b = fim or 999
        seq.append((txt, a, b) + ((it[2],) if len(it) > 2 else ()))
    _PLANOS_DE_PALAVRAS[0] += 1
    for _, a, _b, *_ in seq:                          # um clique seco no quadro em que cada palavra aparece
        SOM("clique", g(a), db=max(-10, -5 * (_PLANOS_DE_PALAVRAS[0] - 1)))
    pop(pl, seq, y=y, size=size)
    return pl


# ---------------------------------------------------------------- 9 · DIAGRAMA
def diagrama(t, desenho_src, pequeno, grande, idx, doc_src=None, desenho=(470, 900, 300), antena=None, ondas_cfg=None,
             titulo_y=320, boom=True, doc_opac=0.45, doc_borrao=0.0):
    """desenho = (cx, cy, w) do traço (entra pela direita e assenta no centro). antena = (x, y) de onde saem as ondas.
    pequeno/grande = as duas linhas do título em bloco ("designed a" / "Communication System")."""
    pl = plano(t, "papel", nome="diagrama")
    if doc_src:
        dz = img(pl, doc_src, W / 2, H / 2 + 120, W * 1.1, filtro=f"grayscale(1) contrast(.6) brightness(1.18) opacity({doc_opac}) blur({doc_borrao}px)")
        anim(dz, t, {"scale": 3.2}, {"scale": 1.0}, 6.93 * 0.55, "expo.out")
    cx, cy, w = desenho
    img(pl, desenho_src, cx, cy, w, t=t, ent="desliza_dir", d=1.6, de=180)
    if antena:
        o = dict(ondas_cfg or {}); t_ondas = o.pop("t", t + 0.2)
        ondas(pl, antena[0], antena[1], t_ondas, **o)
        SOM("ar-ondas", g(t_ondas))                   # os sopros agudos das ondas crescendo
    n_peq = len(pequeno.split(" "))
    s_gr = cabe(grande, "serifa", 63, 600); s_peq = cabe(pequeno, "serifa", round(s_gr * 0.55), 440)
    wg = largura(grande, "serifa", s_gr)
    # medido: a linha pequena começa ~50 px à direita do início da grande, colada em cima dela. Na referência as letras
    # debaixo dela são baixas; como a linha grande pode ter maiúsculas e ascendentes, a pequena sobe o bastante para o
    # descendente não encostar (0,82 do corpo em vez do 0,62 medido).
    _, ids1 = texto(pl, pequeno, W / 2 - wg / 2 + s_gr * 0.8, titulo_y - s_gr * 0.82, s_peq, "serifa", TINTA, "esquerda")
    _, ids2 = texto(pl, grande, W / 2, titulo_y, s_gr, "serifa", TINTA)
    tps = tempos_revela(idx, t0=_desde(t, P(idx[0])))
    revela(ids1 + ids2, tps)
    if boom:
        SOM("boom", t)
    return pl


# ---------------------------------------------------------------- 11 · CENA-COR
def cena_cor(t, obj_src, rotulo_txt, idx_rotulo, t_consequencia, obj_w=150, obj_x=380, obj_y=760, rot_y=None,
             fundo="azul", aneis_topo=True):
    pl = plano(t, fundo, cam={"tipo": "afasta", "de": 1.75, "ate": 1.0, "tau": 0.3, "origem": "50% 40%"}, nome="cena_cor")
    if aneis_topo:
        ar = aneis(pl, W / 2, -40, raios=tuple(range(120, 1300, 95)), t=_desde(t, P(idx_rotulo[0]) + 0.15), pulso=False)
        anim(ar, _desde(t, P(idx_rotulo[0]) + 0.15), {"scale": 0.6}, {"scale": 1.0}, 2.0, "expo.out")
    o = img(pl, obj_src, obj_x, obj_y, obj_w, t=t, ent="sobe", d=1.4, de=760)
    vermelho = img(pl, obj_src, obj_x, obj_y, obj_w, filtro="sepia(1) saturate(9) hue-rotate(-38deg) brightness(.85)")
    entrar(vermelho, g(t_consequencia), "seco")
    anim(vermelho, g(t), {"y": 760}, {"y": 0}, 1.4, "expo.out")
    for e in (o, vermelho):
        anim(e, g(t_consequencia) + 0.3, {"rotation": 0, "x": 0}, {"rotation": 58, "x": 170}, 0.7, "power2.in")
        anim(e + "", g(t_consequencia) + 0.3, {"yPercent": 0}, {"yPercent": 60}, 0.7, "power2.in")
    SOM("golpe", t); SOM("golpe", g(t_consequencia) + 0.3)       # golpe curto na entrada do objeto e outro na virada
    rasgado(pl, rotulo_txt, W / 2 - 10, rot_y or obj_y - 70, _desde(t, P(idx_rotulo[0]) + 0.25),
            size=cabe(rotulo_txt, "serifa", 60, 600))
    return pl


# ---------------------------------------------------------------- 12 · DESCARTE
def descarte(t, sala_src, cesto_src, bola_src, cesto=(360, 780, 300), bola_w=1150, bola_fim_w=150, desenho_src=None, desenho_w=700):
    """sala P&B + cesto colorido + a bola de papel (o desenho amassado) que encolhe até a boca do cesto e afunda.
    desenho_src: o desenho chapado em papel branco que aparece 0,1 s antes de amassar (o "close" da ideia)."""
    if desenho_src:
        f = plano(t, "cor:#cac9c5", nome="descarte_close")
        img(f, desenho_src, W / 2, H / 2 + 160, desenho_w, filtro="contrast(1.15)")
        t = t + PASSO
    cx, cy, cw = cesto
    pl = plano(t, "preto", cam={"tipo": "afasta", "de": 2.6, "ate": 1.0, "tau": 0.5, "origem": f"{cx}px {cy - 60}px"}, nome="descarte")
    img(pl, sala_src, W / 2, H / 2, W * 1.02, H * 1.02, cinza=True, ajuste="cover", filtro="brightness(1.1)")
    img(pl, cesto_src, cx, cy, cw, sombra=True)
    boca = cy - cw * proporcao(cesto_src) * 0.42
    impresso = (f'<div style="position:absolute;inset:0;-webkit-mask-image:url({bola_src});-webkit-mask-size:100% 100%;mask-image:url({bola_src});'
                f'mask-size:100% 100%"><img src="{desenho_src}" style="position:absolute;left:50%;top:6%;height:88%;width:auto;'
                f'transform:translateX(-50%) rotate(-6deg) skewX(4deg);mix-blend-mode:multiply;opacity:.88;filter:contrast(1.1)"></div>') if desenho_src else ""
    b = img(pl, bola_src, cx, boca, bola_fim_w, sombra=True, dentro=impresso)
    k = bola_w / bola_fim_w / 2.6
    y0 = (H / 2 - boca) * 0.85
    setar(b, 0, {"scale": k, "y": y0})

    def cai(fim):
        """Medido na referência: a bola encolhe em ~0,4 s, PAIRA sobre a boca do cesto e só afunda 0,1-0,2 s antes do
        corte. Com tempos fixos ela sumia cedo e o cesto ficava vazio até 1,2 s; agora a queda acompanha o fim do plano."""
        anim(b, t + 0.2, {"scale": k, "y": y0}, {"scale": 1, "y": -14}, 0.4, "power2.inOut")
        t_af = max(round(t + 0.8, 3), round(fim - 0.2, 3))
        anim(b, round(t + 0.6, 3), {"y": -14}, {"y": -4}, max(0.2, round(t_af - (t + 0.6), 3)), "sine.inOut")       # paira
        setar(b, t_af, {"y": 8, "opacity": 1}); setar(b, round(t_af + PASSO, 3), {"y": 26, "opacity": 0.5})       # afunda em 2 quadros
    pl.setdefault("tardios", []).append(cai)
    return pl


# ---------------------------------------------------------------- 13 · ANOS
def anos_rolando(t, a0=None, a1=None, d=1.0, size=67, itens=None):
    pl = plano(t, "papel", nome="anos")
    anos(pl, a0, a1, t + 0.2, t + 0.8, size=size, itens=itens)
    return pl


# ---------------------------------------------------------------- 16 · ESCURO-RÓTULOS
def rotulos(t, itens, centro=(300, 640), pos=((127, 492), (132, 600), (187, 707)), deslize=30, saida=True):
    """itens = [(texto, idx)] ou [(texto, idx, logo, filtro_css)] (até 4). Os rótulos entram pela direita no início
    falado; o grupo anda à esquerda. Marca citada = logo oficial dentro do rótulo."""
    passos = [[round(_desde(t, P(it[1]) - 0.25), 3), deslize, 0, 1] for it in itens]
    pl = plano(t, "preto", cam={"tipo": "degraus", "passos": passos, "tau": 0.33},
               saida={"tipo": "borrao", "d": 0.2, "b": 5} if saida else None, nome="rotulos")
    aneis(pl, centro[0], centro[1])
    tem_logo = any(len(it) > 2 and it[2] for it in itens)
    larg_rot = max(285, max(round(ImageFont.truetype(FONTES["caixa"], 200).getlength(it[0]) / 200 * 55 - 0.02 * 55 * (len(it[0]) - 1))
                            for it in itens) + 34 + (50 if tem_logo else 0))        # 285 px na referência ("Bluetooth" a 55 px)
    for k, it in enumerate(itens):
        txt, i = it[0], it[1]
        x, y = pos[k] if k < len(pos) else (pos[-1][0] + 55 * (k - len(pos) + 1), pos[-1][1] + 108 * (k - len(pos) + 1))
        rotulo(pl, txt, x - (larg_rot - 285) / 2, y, _desde(t, P(i) - 0.25), w=larg_rot, logo=it[2] if len(it) > 2 else None,
               logo_filtro=it[3] if len(it) > 3 else "")
        SOM("thump", _desde(t, P(i) - 0.25))
    return pl


# ---------------------------------------------------------------- 19 · QUADRO
def quadro(t, conteudo_src, moldura_src, linhas, idx, inicio=0.0, janela=(0.205, 0.17, 0.59, 0.66), mold=(360, 560, 400),
           leg_y=880, size=53, maxw=600):
    """O arquivo vira um quadro dourado no papel: entra gigante e desfocado, afasta e foca. janela = (x, y, w, h) da
    abertura da moldura em fração da moldura. linhas = "linha 1\\nlinha 2" (revelada palavra a palavra)."""
    mx, my, mw = mold
    mh = mw * proporcao(moldura_src)
    pl = plano(t, "papel", cam={"tipo": "afasta", "salto": 3.3, "de": 1.29, "ate": 1.0, "tau": 0.6, "origem": f"{mx}px {my}px"}, nome="quadro")
    jx, jy, jw, jh = janela
    x0, y0 = mx - mw / 2 + jw * mw / 2 + jx * mw, my - mh / 2 + jh * mh / 2 + jy * mh
    if conteudo_src.lower().endswith((".mp4", ".mov", ".webm")):
        video(pl, conteudo_src, inicio, x=mx - mw / 2 + jx * mw, y=my - mh / 2 + jy * mh, w=jw * mw, h=jh * mh)
    else:
        img(pl, conteudo_src, x0, y0, jw * mw, jh * mh, ajuste="cover")
    img(pl, moldura_src, mx, my, mw, sombra=True)
    anim(f'{PLANOS[-1]["id"]}z', t, {"filter": "blur(9px)"}, {"filter": "blur(0px)"}, 0.5, "power2.out")
    s = cabe(max(linhas.split("\n"), key=len), "serifa", size, maxw)
    _, ids = texto(pl, linhas, W / 2, leg_y, s, "serifa", TINTA)
    tps = tempos_revela(idx, t0=_desde(t + 0.2, P(idx[0])))
    revela(ids, tps)
    for tq in tps[:2]:                                # dois cliques baixos nas primeiras palavras da legenda
        SOM("clique", g(tq), db=-8)
    return pl


# ---------------------------------------------------------------- 21-22 · CTA
def cta_icone(t, fundo_src, icone_src, t_clique, icone=(360, 640, 120), mao_de=(250, 1000), boom=True):
    ix, iy, iw = icone
    pl = plano(t, "preto", cam={"tipo": "afasta", "de": 2.5, "ate": 1.0, "tau": 0.5, "origem": f"{ix}px {iy}px"}, nome="cta_icone")
    img(pl, fundo_src, W / 2, H / 2, W * 1.05, H * 1.05, ajuste="cover", filtro="brightness(.8)")
    ic = img(pl, icone_src, ix, iy, iw)
    mao(pl, mao_de[0], mao_de[1], ix + iw * 0.1, iy + iw * 0.25, t + 0.1, d=1.3, t_clique=t_clique, alvo=ic, size=40)
    if t_clique:
        SOM("ar-curto", g(t_clique))                  # o sopro agudo do clique da mãozinha
    if boom:
        SOM("boom", t)
    return pl


def cta_campo(t, print_src, txt, t0, t1, y=640, w=442, borrado=6.0, size=38, brilho=0.6):
    pl = plano(t, "preto", cam={"tipo": "pan", "x": 330, "tau": 0.35}, nome="cta_campo")
    img(pl, print_src, W / 2, H / 2, W, H, ajuste="cover", filtro=f"blur({borrado}px) brightness({brilho})")
    campo(pl, txt, W / 2 + 40, y, t0, t1, w=w, size=size)
    return pl
