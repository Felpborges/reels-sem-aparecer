# MOTOR ESTILO B · biblioteca de mundos (telas genéricas desenhadas por nós; nenhuma UI real de terceiros).
# Executado no mesmo namespace do build.py (usa bloco, texto, digita, anim, conta, risco, camada, _id, _n, ANIMS).
# Regras desta biblioteca (vieram da auditoria de 12/11/2026):
#   · QUADRO SEGURO — nada de texto que só cabe se a câmera não chegar perto; cada tela foi desenhada para caber em 9:16.
#   · Ícones de traço de verdade (nada de quadrado/círculo vazio "de wireframe"), sem desenho de marca real.
#   · Rótulos da interface no MESMO idioma da fala: defina IDIOMA = "pt" ou "en" no começo do cenas.py.
#   · Coluna direita (x > 620) e rodapé (y > 1100) do 9:16 são a zona dos botões e da legenda do Instagram: só decoração ali.

SANS = "'Inter'"
IDIOMA = "pt"
ROT = {
    "pt": {"volta": "Álbuns", "ok": "OK", "modos": ("CÂM. LENTA", "VÍDEO", "FOTO", "RETRATO", "QUADRADO"), "ranking": "Ranking",
           "melhor": "Melhor cliente", "fechar": "Fechar", "abas": ("Início", "Amigos"), "postar": "Publicar", "notas": "Notas",
           "msg": "Alex", "hoje": "Hoje, 19:30", "busca_abas": ("Tudo", "Imagens", "Vídeos", "Notícias")},
    "en": {"volta": "Albums", "ok": "Done", "modos": ("SLO-MO", "VIDEO", "PHOTO", "PORTRAIT", "SQUARE"), "ranking": "Ranking",
           "melhor": "Best customer", "fechar": "Close", "abas": ("Home", "Friends"), "postar": "Share", "notas": "Notes",
           "msg": "Alex", "hoje": "Today, 19:30", "busca_abas": ("All", "Images", "Videos", "News")},
}


def R(k):
    return ROT[IDIOMA][k]


# ---------------------------------------------------------------- ícones de traço (24x24)
ICO = {
    "casa": '<path d="M4 11l8-7 8 7v9h-5v-6H9v6H4z"/>',
    "lupa": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
    "sino": '<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
    "envelope": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 6.5L12 13l8.5-6.5"/>',
    "pessoa": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4.5 4.5-6.5 8-6.5s7 2 8 6.5"/>',
    "grupo": '<circle cx="9" cy="8.5" r="3.5"/><circle cx="17" cy="9.5" r="2.7"/><path d="M2.5 20c.8-3.8 3.6-5.6 6.5-5.6s5.7 1.8 6.5 5.6M16 14.5c2.6 0 4.6 1.6 5.3 4.6"/>',
    "lista": '<path d="M9 7h11M9 12h11M9 17h11"/><circle cx="4.5" cy="7" r="1.2"/><circle cx="4.5" cy="12" r="1.2"/><circle cx="4.5" cy="17" r="1.2"/>',
    "mais": '<circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/>',
    "imagem": '<rect x="3" y="4" width="18" height="16" rx="3"/><circle cx="9" cy="10" r="2"/><path d="M4 18l6-5 4 3 3-2 4 4"/>',
    "gif": '<rect x="2.5" y="5" width="19" height="14" rx="3"/><text x="12" y="15.4" text-anchor="middle" font-family="Inter" font-weight="800" font-size="7.6" fill="currentColor" stroke="none">GIF</text>',
    "enquete": '<path d="M5 20V12M10 20V6M15 20v-9M20 20V9"/>',
    "emoji": '<circle cx="12" cy="12" r="9"/><circle cx="9" cy="10" r=".8" fill="currentColor"/><circle cx="15" cy="10" r=".8" fill="currentColor"/><path d="M8 14.5c2 2.2 6 2.2 8 0"/>',
    "agenda": '<rect x="4" y="5" width="16" height="15" rx="3"/><path d="M4 10h16M9 3v4M15 3v4"/>',
    "local": '<path d="M12 21s-6-6-6-11a6 6 0 0 1 12 0c0 5-6 11-6 11z"/><circle cx="12" cy="10" r="2"/>',
    "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
    "globo": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
    "raio": '<path d="M13 2L5 14h6l-1 8 8-12h-6z"/>',
    "timer": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6"/>',
    "vivo": '<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="10.3" stroke-dasharray="3 3"/>',
    "filtros": '<circle cx="9" cy="10" r="5"/><circle cx="15" cy="10" r="5"/><circle cx="12" cy="15" r="5"/>',
    "girar": '<path d="M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3"/><path d="M18 3v4h-4M6 21v-4h4"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/>',
}


def ico(nome, tam=26, cor="#1d9bf0", esp=2):
    return (f'<svg width="{tam}" height="{tam}" viewBox="0 0 24 24" fill="none" stroke="{cor}" stroke-width="{esp}" stroke-linecap="round" '
            f'stroke-linejoin="round" style="color:{cor};display:block">{ICO[nome]}</svg>')


def icone(nome, x, y, tam=26, cor="#1d9bf0", t="INI", z=5, ent="fade"):
    """Ícone solto posicionado (ex.: à esquerda de um campo digitado)."""
    return bloco(ico(nome, tam, cor), x, y, tam, tam, z=z, t=t, ent=ent)


# ---------------------------------------------------------------- interfaces fixas (camada que não anda com a câmera)
def ui_galeria(cor="#f2b233"):
    """Cabeçalho de visualizador de fotos do celular: faixa escura com voltar / ⋯ / pronto."""
    camada("fixa")
    bloco(f'<div style="position:absolute;inset:0;background:linear-gradient(#050608,#0b0d10 80%,rgba(11,13,16,0));"></div>'
          f'<div style="position:absolute;left:40px;top:66px;font:500 23px {SANS};color:{cor}">‹ {R("volta")}</div>'
          f'<div style="position:absolute;left:510px;top:62px;width:30px;height:30px;border:2.5px solid {cor};border-radius:50%;'
          f'font:700 15px {SANS};color:{cor};text-align:center;line-height:22px">···</div>'
          f'<div style="position:absolute;left:574px;top:66px;font:600 23px {SANS};color:{cor}">{R("ok")}</div>', 0, 0, 720, 150, z=20)
    camada("cam")


def ui_camera(ativo=2, reticulo=(300, 690, 180, .45)):
    """Visor da câmera do celular: ícones de traço no topo, retículo de foco discreto, modos + disparador embaixo.
    reticulo = (x, y, tamanho, opacidade): ponha numa área SEM texto."""
    camada("fixa")
    ic = "".join(f'<div style="position:absolute;left:{x}px;top:18px">{ico(n, 30, "#e8e8e8", 1.8)}</div>' for x, n in ((96, "raio"), (300, "vivo"), (450, "timer"), (612, "filtros")))
    bloco(f'<div style="position:absolute;inset:0;background:#000"></div>{ic}', 0, 0, 720, 68, z=20)
    md = "".join(f'<span style="margin:0 15px;color:{"#f2a33a" if k == ativo else "#eee"}">{m}</span>' for k, m in enumerate(R("modos")))
    bloco(f'<div style="position:absolute;inset:0;background:#000"></div>'
          f'<div style="position:absolute;left:0;right:0;top:30px;text-align:center;font:600 19px {SANS};letter-spacing:.06em;white-space:nowrap">{md}</div>'
          f'<div style="position:absolute;left:304px;top:92px;width:112px;height:112px;border-radius:50%;border:7px solid #fff;padding:6px">'
          f'<div style="width:100%;height:100%;border-radius:50%;background:#fff"></div></div>'
          f'<div style="position:absolute;left:606px;top:124px">{ico("girar", 46, "#ddd", 1.6)}</div>'
          f'<div style="position:absolute;left:50px;top:116px;width:62px;height:62px;background:#222;border-radius:8px"></div>', 0, 1036, 720, 244, z=20)
    x, y, t_, o = reticulo
    fo = (f'<svg width="{t_}" height="{t_}" viewBox="0 0 240 240" fill="none" stroke="#f3f3f3" stroke-width="3">'
          '<path d="M0 40V0H40M200 0H240V40M240 200V240H200M40 240H0V200"/><path d="M120 108V132M108 120H132" stroke-width="2"/></svg>')
    bloco(fo, x, y, t_, t_, z=19, extra=f"opacity:{o}")
    camada("cam")


# ---------------------------------------------------------------- telas de app (faixa 1:1)
def ranking(linhas, t0, passo=0.2, x=90, y=380, w=540, cor="#2fd16b", alto=150, t_rola=None, faixa=(285, 995), fade=64,
            av_fundo="#e8eef2", av_letra="#23313b"):
    """App escuro de ranking. linhas = [(inicial, nome, sub, selo)]. Devolve (id do cabeçalho, id da lista) para rolar.
    Tudo mora dentro de uma MÁSCARA FIXA na faixa: a linha some em degradê antes de tocar a borda (nunca fatiada seca).
    Só aparecem antes da rolagem as linhas que cabem inteiras; as outras entram com a rolagem (t_rola)."""
    hid, lid = _id("rh"), _id("rl")
    hd = (f'<div id="{hid}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:90px;opacity:0">'
          f'<div style="position:absolute;left:0;top:0;font:600 30px {SANS};color:#f2f2f2">{R("ranking")}</div>'
          f'<div style="position:absolute;left:0;top:44px;font:500 26px {SANS};color:{cor}">{R("melhor")}</div>'
          f'<div style="position:absolute;right:0;top:30px;font:500 24px {SANS};color:{cor}">{R("fechar")}</div></div>')
    rows, av = [], alto - 44
    for k, (ini, nome, sub, selo) in enumerate(linhas):
        yy = 120 + k * alto
        rows.append(f'<div id="rk{k}" style="position:absolute;left:0;top:{yy}px;width:{w}px;height:{alto - 14}px;opacity:0">'
                    f'<div style="position:absolute;left:0;top:0;width:{av}px;height:{av}px;border-radius:18px;background:{av_fundo};color:{av_letra};'
                    f'font:700 {av * .44:.0f}px {SANS};text-align:center;line-height:{av}px">{ini}</div>'
                    f'<div style="position:absolute;left:{av + 30}px;top:{av * .1:.0f}px;font:500 30px {SANS};color:{cor}">{nome}</div>'
                    f'<div style="position:absolute;left:{av + 30}px;top:{av * .1 + 44:.0f}px;font:400 27px {SANS};color:#b5c2c0">{sub}</div>'
                    f'<div style="position:absolute;left:{w - 52}px;top:{av / 2 - 25:.0f}px;width:50px;height:50px;border-radius:50%;background:#e8e8e8;color:#111;'
                    f'font:700 25px {SANS};text-align:center;line-height:50px">{k + 1}</div>' +
                    (f'<div style="position:absolute;left:{w - 176}px;top:{av / 2 - 16:.0f}px;font:700 25px {SANS};color:#7dff9f;text-shadow:0 0 14px #2fd16b,0 0 26px #2fd16b">{selo}</div>' if selo else '') +
                    '</div>')
    lista = f'<div id="{lid}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{120 + len(linhas) * alto}px">{"".join(rows)}</div>'
    a0, a1, b1, b0 = faixa[0], faixa[0] + fade, faixa[1] - fade, faixa[1]
    m = f"linear-gradient(180deg,transparent {a0 + 8}px,#000 {a1}px,#000 {b1}px,transparent {b0 - 8}px)"
    bloco(hd + lista, 0, 0, 720, 1280, z=3, extra=f"-webkit-mask-image:{m};mask-image:{m}")
    anim(hid, t0, {"opacity": 0, "filter": "blur(8px)"}, {"opacity": 1, "filter": "blur(0px)"}, 0.18, "power1.out", novo=True)
    for k in range(len(linhas)):
        cabe = y + 120 + k * alto + alto - 14 <= b1
        tk = t0 + 0.1 + k * passo if (cabe or t_rola is None) else t_rola
        anim(f"rk{k}", tk, {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0}, 0.25, "power2.out", novo=True)
    return hid, lid


def pilula_progresso(x, y, t, de, ate, dur, rotulo, w=520, h=174, eid=None, ent=("voa", [0, 40, 0, .96], 0.4)):
    """Pílula escura com anel verde e porcentagem contando. eid único por padrão (o anel é f"{eid}a", o número f"{eid}n")."""
    eid = eid or _id("pp")
    r = 50; c = 2 * 3.14159 * r
    htm = (f'<div style="position:absolute;inset:0;border-radius:{h / 2}px;background:linear-gradient(#3a3a3a,#262626);'
           f'box-shadow:0 22px 34px rgba(0,0,0,.35),inset 0 2px 2px rgba(255,255,255,.12)"></div>'
           f'<svg style="position:absolute;left:36px;top:{h / 2 - 60}px" width="120" height="120"><circle cx="60" cy="60" r="{r}" fill="none" stroke="#1d1d1d" stroke-width="9"/>'
           f'<circle id="{eid}a" cx="60" cy="60" r="{r}" fill="none" stroke="#33e06a" stroke-width="9" stroke-linecap="round" '
           f'stroke-dasharray="{c:.1f}" stroke-dashoffset="{c * (1 - de / 100):.1f}" transform="rotate(-90 60 60)"/></svg>'
           f'<div id="{eid}n" style="position:absolute;left:180px;top:{h / 2 - 54}px;font:700 52px {SANS};color:#fff">{de}%</div>'
           f'<div style="position:absolute;left:182px;top:{h / 2 + 12}px;font:500 25px {SANS};color:#d0d0d0">{rotulo}</div>')
    pid = bloco(htm, x, y, w, h, z=5, t=t, ent=ent[0], de=ent[1], d=ent[2], eid=eid)
    conta(f"{eid}n", t, de, ate, dur)
    anim(f"{eid}a", t, {"strokeDashoffset": c * (1 - de / 100)}, {"strokeDashoffset": c * (1 - ate / 100)}, dur, "power1.out")
    return pid


def pilula_no(txt, x, y, t, cor="verde", size=30, eid=None):
    """Pílula com brilho (nó de um diagrama). Entra por escala no PRÓPRIO lugar, para a linha que chega nela não ficar solta."""
    c = {"verde": ("#3cc35a", "#22913c", "rgba(60,220,100,.55)"), "vermelho": ("#ef4b4b", "#c42a2a", "rgba(255,70,70,.5)"),
         "azul": ("#3b8cff", "#1f62d6", "rgba(70,140,255,.5)")}[cor]
    htm = (f'<div style="position:absolute;left:-14px;top:50%;width:22px;height:22px;margin-top:-11px;border-radius:50%;background:#ddd;border:3px solid #bbb"></div>'
           f'<div style="padding:16px 36px;border-radius:40px;background:linear-gradient({c[0]},{c[1]});color:#fff;font:500 {size}px {SANS};'
           f'white-space:nowrap;box-shadow:0 0 30px {c[2]},0 10px 18px rgba(0,0,0,.18),inset 0 2px 1px rgba(255,255,255,.35)">{txt}</div>')
    return bloco(htm, x, y, None, None, z=5, t=t, ent="pop", d=0.3, eid=eid, extra="transform-origin:0 50%")


def conversa(y0=430):
    """Cabeçalho de conversa genérico: avatar com inicial + nome do contato + data."""
    texto(f'<div style="width:46px;height:46px;margin:0 auto 6px;border-radius:50%;background:#d7dde3;color:#3a4650;font:700 21px {SANS};line-height:46px">{R("msg")[0]}</div>'
          f'<div style="font:600 20px {SANS};color:#333">{R("msg")}</div><div style="font:400 20px {SANS};color:#7a7a7a;margin-top:4px">{R("hoje")}</div>',
          0, y0, w=720, alinh="center", t="INI", size=20)


def balao(palavras, x, y, lado="esq", size=30, maxw=520):
    """Balão de conversa que cresce palavra a palavra. palavras = [(txt, t)]. lado: esq (cinza) | dir (azul).
    x é a borda do balão do lado dele (esq: borda esquerda; dir: borda DIREITA)."""
    bg, cor = ("#e9e9eb", "#111") if lado == "esq" else ("#0075de", "#fff")
    eid = _id("bl")
    spans = "".join(f'<span id="{eid}w{k}" style="opacity:0;display:none">{"" if k == 0 else " "}{p}</span>' for k, (p, t) in enumerate(palavras))
    rabo = (f'<div style="position:absolute;{"left:-7px" if lado == "esq" else "right:-7px"};bottom:0;width:22px;height:22px;background:{bg};'
            f'border-radius:{"0 0 0 16px" if lado == "esq" else "0 0 16px 0"};transform:skewX({"20" if lado == "esq" else "-20"}deg)"></div>')
    htm = (f'<div style="display:flex;justify-content:{"flex-start" if lado == "esq" else "flex-end"};width:{maxw}px">'
           f'<div style="position:relative;padding:14px 26px;border-radius:30px;background:{bg};color:{cor};font:400 {size}px {SANS};'
           f'max-width:{maxw}px">{rabo}<span style="position:relative">{spans}</span></div></div>')
    bx = x if lado == "esq" else x - maxw
    bid = bloco(htm, bx, y, maxw, None, z=4, t=palavras[0][1], ent="pop", d=0.22, eid=eid,
                extra=f"transform-origin:{'0' if lado == 'esq' else '100%'} 100%")
    for k, (p, t) in enumerate(palavras):
        ANIMS.append({"k": "ft", "id": f"{eid}w{k}", "t": round(t, 3), "de": {"opacity": 0, "display": "none"},
                      "para": {"opacity": 1, "display": "inline"}, "d": 0.01, "e": "none", "novo": True})
    return bid


def digitando(x_dir, y, t, ate, cor="#dfe9fb"):
    """Bolinhas de 'digitando…' no lado de quem vai responder (x_dir = borda direita); somem quando o balão nasce no lugar."""
    eid = _id("dt")
    b = "".join(f'<div id="{eid}p{k}" style="width:13px;height:13px;border-radius:50%;background:#7a8fb3;margin:0 4px"></div>' for k in range(3))
    bloco(f'<div style="display:flex;padding:20px 22px;border-radius:26px;background:{cor}">{b}</div>', x_dir - 110, y, z=4, t=t, ent="pop", sai=(ate, "fade", 0.08), eid=eid)
    k = 0; tt = t + 0.1
    while tt < ate:
        anim(f"{eid}p{k % 3}", tt, {"y": 0, "opacity": .5}, {"y": -6, "opacity": 1}, 0.12, "sine.out")
        anim(f"{eid}p{k % 3}", tt + 0.12, {"y": -6, "opacity": 1}, {"y": 0, "opacity": .5}, 0.12, "sine.in")
        k += 1; tt += 0.11
    return eid


def chip(palavras, x, y, estilo="laranja", size=28, eid=None):
    """Pílula de interface pousada num mundo fotográfico. Nasce com a 1ª palavra e CRESCE com o texto (nunca vazia)."""
    bg = {"laranja": "linear-gradient(90deg,#e8452c,#f2741f 60%,#f08a1c)", "branco": "rgba(245,245,245,.94)",
          "verde": "linear-gradient(#b9df8d,#9fcd6f)"}[estilo]
    cor = "#fff" if estilo == "laranja" else "#555"
    eid = eid or _id("ch")
    inner = "".join(f'<span id="{eid}w{k}" style="opacity:0;display:none">{"" if k == 0 else " "}{p}</span>' for k, (p, tt) in enumerate(palavras))
    for k, (p, tt) in enumerate(palavras):
        ANIMS.append({"k": "ft", "id": f"{eid}w{k}", "t": round(tt, 3), "de": {"opacity": 0, "display": "none"},
                      "para": {"opacity": 1, "display": "inline"}, "d": 0.1, "e": "none", "novo": True})
    htm = (f'<div style="display:inline-block;padding:12px 30px;border-radius:34px;background:{bg};color:{cor};font:500 {size}px {SANS};white-space:nowrap;'
           f'box-shadow:0 10px 20px rgba(0,0,0,.28),inset 0 1px 1px rgba(255,255,255,.4)">{inner}</div>')
    return bloco(htm, x, y, z=6, t=palavras[0][1], ent="pop", d=0.22, eid=eid, extra="transform-origin:0 50%")


def onda(cx, y, t0, t1, w=300, semente=3, dur_txt="0:04"):
    """Chip de mensagem de voz pousado no mundo: play + onda que se MEXE com a voz + duração. cx = centro."""
    import random as _r
    rnd = _r.Random(semente); n = int((w - 120) / 8); eid = _id("on")
    barras = "".join(f'<div id="{eid}b{k}" style="width:3px;height:30px;background:#f4fbe9;margin:0 1.5px;border-radius:2px;transform:scaleY(.25)"></div>' for k in range(n))
    bloco(f'<div style="display:flex;align-items:center;gap:10px;height:58px;width:{w}px;padding:0 16px;border-radius:29px;'
          f'background:linear-gradient(#5fa83a,#3f8a26);box-shadow:0 10px 20px rgba(0,0,0,.3),inset 0 1px 1px rgba(255,255,255,.35)">'
          f'<svg width="22" height="22" viewBox="0 0 24 24"><path d="M7 4l13 8-13 8z" fill="#f4fbe9"/></svg>'
          f'<div style="display:flex;align-items:center;flex:1">{barras}</div>'
          f'<div style="font:600 18px {SANS};color:#f4fbe9">{dur_txt}</div></div>', cx - w / 2, y, z=6, t=t0, ent="voa", de=[0, 20, 0, 1], eid=eid)
    for k in range(n):
        dd = rnd.uniform(.08, .15); amp = rnd.uniform(.35, 1.0) * (1 - abs(k - n / 2) / (n * .75))
        rep_ = max(1, int((t1 - t0) / dd))
        anim(f"{eid}b{k}", t0 + rnd.uniform(0, .1), {"scaleY": .2}, {"scaleY": max(.25, amp), "repeat": rep_, "yoyo": True}, dd, "sine.inOut")
    return eid


ICONES_BARRA = ["imagem", "gif", "emoji", "local"]
ACENTO = "#7b6cf6"


def composer(foto_src, x=100, y=310, w=520, campos=3):
    """Rede social genérica, tema escuro: abas, linha com avatar, imagem anexada, até 3 CAMPOS em linhas próprias (cabem
    inteiros num close de 2,2x), barra de ícones de traço. Devolve coordenadas e o id da imagem anexada."""
    iid = _id("ci")
    yc = 420; yd = yc + campos * 30 + 8; yi = yd + 14
    lat = "".join(f'<div style="position:absolute;left:4px;top:{58 + k * 50}px">{ico(n, 26, "#d8d8d8", 1.8)}</div>'
                  for k, n in enumerate(["casa", "lupa", "sino", "envelope", "lista", "grupo", "pessoa", "mais"]))
    ab = R("abas")
    bloco(f'<div style="position:absolute;left:-40px;top:0;width:44px;height:520px">{lat}</div>'
          f'<div style="position:absolute;left:70px;top:6px;font:600 17px {SANS};color:#eee">{ab[0]}</div>'
          f'<div style="position:absolute;left:70px;top:34px;width:56px;height:4px;border-radius:2px;background:{ACENTO}"></div>'
          f'<div style="position:absolute;left:300px;top:6px;font:500 17px {SANS};color:#777">{ab[1]}</div>'
          f'<div style="position:absolute;left:20px;top:46px;width:{w - 20}px;height:1px;background:#2a2a2a"></div>'
          f'<div style="position:absolute;left:24px;top:66px;width:38px;height:38px;border-radius:50%;background:#2d2850;color:#d9d4ff;font:700 17px {SANS};text-align:center;line-height:38px">J</div>'
          f'<div id="{iid}" style="position:absolute;left:76px;top:120px;width:{w - 96}px;height:290px;border-radius:16px;overflow:hidden;'
          f'background:url(\'{foto_src}\') 50% 45%/cover"></div>'
          f'<div style="position:absolute;left:24px;top:{yd}px;width:{w - 30}px;height:1px;background:#2a2a2a"></div>'
          + "".join(f'<div style="position:absolute;left:{76 + k * 40}px;top:{yi}px">{ico(n, 28, ACENTO, 2)}</div>' for k, n in enumerate(ICONES_BARRA)) +
          f'<div style="position:absolute;left:{w - 86}px;top:{yi - 4}px;width:76px;height:36px;border-radius:18px;background:{ACENTO};font:700 16px {SANS};color:#fff;text-align:center;line-height:36px">{R("postar")}</div>'
          f'<div style="position:absolute;left:24px;top:{yi + 48}px;width:{w - 30}px;height:1px;background:#2a2a2a"></div>',
          x, y, w, yi + 60, z=3)
    return {"img_id": iid, "linha": (x + 76, y + 70), "img": (x + 76, y + 120, w - 96, 290),
            "campos": [(x + 76, y + yc + k * 30) for k in range(campos)], "icones_y": y + yi}


def busca(marca_html, y=470, x=80, w=560, marca_size=64):
    """Página de busca genérica em layout VERTICAL (cabe no 9:16): marca centralizada em cima e barra com lupa embaixo.
    Devolve (id da marca, id da barra, (x, y) onde a consulta começa)."""
    m = texto(marca_html, 0, y, w=720, alinh="center", size=marca_size, peso=700, t="INI", ent="seco", ls=-0.045)
    yb = y + marca_size + 40
    bid = bloco(f'<div style="width:{w}px;height:84px;border-radius:42px;background:#fff;'
                f'box-shadow:0 0 0 2px #cfe0fb, 0 10px 30px rgba(0,117,222,.14)"></div>'
                f'<div style="position:absolute;left:26px;top:28px">{ico("lupa", 28, "#7a7a7a", 2.2)}</div>'
                f'<div style="position:absolute;left:{w - 56}px;top:28px">{ico("mic", 28, "#9a9a9a", 1.8)}</div>',
                x, yb, w, 84, z=3)
    return m, bid, (x + 72, yb + 23)


def tela_lcd(quad, w, h, z=6):
    """Acabamento de tela de aparelho por cima do texto: vinheta, reflexo diagonal sutil e grade de pixel (~6 %)."""
    return bloco('<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(255,255,255,0) 62%,rgba(20,30,60,.16) 100%)"></div>'
                 '<div style="position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,0) 30%,rgba(255,255,255,.16) 42%,rgba(255,255,255,0) 52%)"></div>'
                 '<div style="position:absolute;inset:0;opacity:.07;background:repeating-linear-gradient(0deg,#000 0 1px,transparent 1px 3px),'
                 'repeating-linear-gradient(90deg,#000 0 1px,transparent 1px 3px)"></div>', 0, 0, w, h, quad=quad, z=z, extra="pointer-events:none")


def laco(cx, cy, rx, ry, t, d=0.45, rot=-6, cor="#d9483b", esp=3.2, voltas=1.12, z=5):
    """Laço desenhado à mão em volta de uma palavra (elipse que passa um pouco do ponto de partida e não fecha)."""
    import math
    pts = []
    n = 46
    for k in range(n + 1):
        a = math.radians(200) + 2 * math.pi * voltas * k / n
        r = 1 + 0.06 * math.sin(3 * a) + 0.04 * (k / n)
        x, y = rx * r * math.cos(a), ry * r * math.sin(a)
        c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pts.append((round(cx + x * c - y * s_, 1), round(cy + x * s_ + y * c, 1)))
    return risco(pts, t, d=d, cor=cor, esp=esp, z=z, ease="power1.inOut")


def placa_aviso(x, y, w, t, de=(160, -160, 25, 1.3), d=0.35, blur=0, rot=0, z=7):
    """Placa triangular de aviso desenhada em SVG (alternativa à foto recortada assets/img/placa.png)."""
    svg = (f'<svg width="{w}" height="{w * .9:.0f}" viewBox="0 0 100 90"><defs><linearGradient id="pa{_n[0]}" x1="0" y1="0" x2="1" y2="1">'
           f'<stop offset="0" stop-color="#ffd23f"/><stop offset=".55" stop-color="#f7a21b"/><stop offset="1" stop-color="#d9730f"/></linearGradient></defs>'
           f'<path d="M50 4 Q54 4 56 8 L96 78 Q98 84 92 85 L8 85 Q2 84 4 78 L44 8 Q46 4 50 4Z" fill="url(#pa{_n[0]})" stroke="#1a1a1a" stroke-width="6" stroke-linejoin="round"/>'
           f'<path d="M50 30 L50 58" stroke="#1a1a1a" stroke-width="9" stroke-linecap="round"/><circle cx="50" cy="71" r="5" fill="#1a1a1a"/></svg>')
    return bloco(f'<div class="occ">{svg}</div>', x, y, z=z, t=t, ent="voa", de=list(de), d=d, rot=rot,
                 extra=(f"filter:blur({blur}px) drop-shadow(6px 10px 10px rgba(0,0,0,.25));" if blur else "filter:drop-shadow(4px 6px 6px rgba(0,0,0,.3));"))
