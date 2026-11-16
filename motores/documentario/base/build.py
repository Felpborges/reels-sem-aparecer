#!/usr/bin/env python3
"""MOTOR ESTILO D ("o documentário de arquivo em fita") · gera index.html (HyperFrames + GSAP) a partir de cenas.py.

Independente dos motores A, B e C. Manual: MOTOR.md do motor documentario, na skill.
PALCO 720x1280 = o tamanho do reel de referência: todas as medidas da perícia valem 1:1.
O HTML é renderizado a 10 fps ("em três", como o original) e a pele da fita (linhas a 6 fps, RGB, grão, poeira,
tremulação) + a subida para 1080x1920 acontecem depois, em pelicula.py.

Tempos em segundos absolutos. P(i) = início da i-ésima palavra falada; F(i) = fim; CORTE(i) = corte do plano que
começa na palavra i (0,07 s antes, na grade de 10 fps). Cada plano dura até o começo do próximo.

Primitivas (usadas pelos moldes em moldes.py; cenas.py chama os moldes):
  plano(t, fundo, cam, saida)            um plano (corte seco). fundo: papel|preto|petroleo|azul|cor:#hex. cam: câmera
  img(pl, src, x, y, w, ...)             imagem/recorte (PNG com alfa) ou foto; cinza=True põe em P&B; pontos=True retícula
  video(pl, src, ...)                    filme de arquivo cobrindo a tela (data-media-start = ponto de entrada)
  serifa(pl, txt, x, y, size, ...)       Hoefler Text Italic (a voz escrita do D)
  caixa(pl, txt, x, y, size, ...)        Helvetica Neue Bold caixa-alta, tracking -0,06 em
  revela(...) pop(...) digita_queda(...) digita_cursor(...)   as 4 animações de texto medidas
  selecao, seta, aneis, ondas, rotulo, anos, rasgado, brilhos, mao, campo, punch, SOM
"""
import json, html, os, random, math
from PIL import ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
PROJ = json.load(open(os.path.join(AQUI, "projeto.json")))
ONS = json.load(open(os.path.join(AQUI, "medir", "alinhamento.json")))
CAUDA = 0.2                # o vídeo acaba ~0,2 s depois da última palavra (medido na referência: 0,17 s)
DUR = PROJ.get("duracao") or round(ONS[-1]["fim"] + CAUDA, 1)
W, H = 720, 1280
AUDIO = PROJ.get("audio") or ("assets/mix.m4a" if os.path.exists(os.path.join(AQUI, "assets", "mix.m4a")) else "assets/narracao.wav")

# ---- identidade medida (DESMONTE-D §5-§6)
PAPEL, PRETO, PETROLEO = "#c3c4c2", "#0a0a0a", "#061414"
TINTA = "#1d1c20"          # serifada no papel
AZUL_ROT, AZUL_ROT_SOMBRA, AZUL_ROT_BORDA = "#1e87b9", "#0d4f86", "#cfe8f5"
SELECAO, ALCA = "rgba(51,119,144,.42)", "#2a8fd0"
FONTES = {"serifa": os.path.join(AQUI, "assets/fonts/HoeflerText-Italic.ttf"),
          "caixa": os.path.join(AQUI, "assets/fonts/HelveticaNeue-Bold.ttf"),
          "ui": os.path.join(AQUI, "assets/fonts/HelveticaNeue.ttf")}
TRACK = {"serifa": -0.05, "caixa": -0.06, "ui": 0.0}
ANTES_DO_CORTE = 0.07      # o corte cai ~0,07 s antes da 1ª palavra (mediana medida)
PASSO = 0.1                # a grade do conteúdo (10 fps)

PLANOS, ANIMS, SONS = [], [], []
FILTROS_H = {}             # borrões só horizontais (chicote, saída em zoom): id -> desvio em px
_n = [0]
random.seed(PROJ.get("semente", 7))


def nid(p="e"):
    _n[0] += 1
    return f"{p}{_n[0]}"


def g(t):
    """Arredonda para a grade de 10 fps."""
    return round(round(t / PASSO) * PASSO, 3)


def P(i, antes=0.0):
    return round(max(0.0, ONS[i]["ini"] - antes), 3)


def F(i):
    return round(ONS[i]["fim"], 3)


def CORTE(i):
    return g(max(0.0, P(i) - ANTES_DO_CORTE))


def palavra(txt, n=1, desde=0):
    """Índice da n-ésima ocorrência da palavra (sem pontuação, sem caixa) a partir de `desde`."""
    lim = lambda s: "".join(c for c in s.lower() if c.isalnum())
    k = 0
    for i in range(desde, len(ONS)):
        if lim(ONS[i]["w"]) == lim(txt):
            k += 1
            if k == n:
                return i
    raise KeyError(f"palavra '{txt}' (#{n}) não está na fala")


def largura(txt, papel, size):
    f = ImageFont.truetype(FONTES[papel], 200)
    return f.getlength(txt) / 200 * size + TRACK[papel] * size * max(0, len(txt) - 1)


def cabe(txt, papel, size, maxw):
    """Corpo que faz o texto caber em maxw (nada cortado)."""
    w = largura(txt, papel, size)
    return round(size * min(1.0, maxw / w), 1) if w > 0 else size


# ------------------------------------------------------------------ planos e câmera
def plano(t, fundo="papel", cam=None, saida=None, nome="", entrada=None):
    """cam: {"tipo": "afasta"|"aproxima"|"pan"|"desliza"|"parado", "de": escala inicial, "ate": escala final,
             "x": deslocamento inicial em px (pan), "y": idem, "tau": constante de tempo (s), "ease": opcional,
             "origem": "50% 50%"}
       saida: aplicada no fim do plano, SEMPRE em passos de 10 fps gravados um a um (um tween curto não é amostrado):
              {"tipo": "borrao", "d": 0.2, "b": 4}   desfoca nos últimos d segundos; o ÚLTIMO quadro tem b px
              {"tipo": "chicote", "x": -27, "b": 3}  último quadro deslocado x px com borrão horizontal de b px
              {"tipo": "zoom", "d": 0.4, "s": 0.755} afasta acelerando até s; só o último quadro borra (b, horizontal)
       entrada: {"tipo": "borrao", "b": 3} -> o 1º quadro entra desfocado e o 2º já é nítido (a ponte de desfoque)."""
    pid = nid("p")
    pl = {"id": pid, "t": g(t), "fundo": fundo, "cam": cam or {"tipo": "parado"}, "saida": saida, "entrada": entrada, "els": [], "nome": nome, "z": 0}
    PLANOS.append(pl)
    return pl


def _fundo_html(f):
    if f == "papel":
        return f'<div class="fd" style="background:{PAPEL}"></div>'
    if f == "preto":
        return (f'<div class="fd" style="background:{PRETO}"></div>'
                '<div class="fd" style="background-image:linear-gradient(rgba(255,255,255,.022) 1px,transparent 1px),'
                'linear-gradient(90deg,rgba(255,255,255,.022) 1px,transparent 1px);background-size:64px 64px"></div>')
    if f == "petroleo":
        return (f'<div class="fd" style="background:{PETROLEO}"></div>'
                '<div class="fd" style="background:repeating-radial-gradient(circle at 50% 108%,rgba(255,255,255,0) 0 150px,'
                'rgba(120,200,190,.035) 150px 300px)"></div>'
                '<div class="fd" style="background:radial-gradient(ellipse 80% 60% at 50% 70%,rgba(20,60,58,.35),rgba(0,0,0,0) 70%)"></div>')
    if f == "azul":
        riscos = "".join(f'<div class="ab" style="left:{x}px;top:0;width:{w}px;height:{H}px;background:linear-gradient(180deg,'
                         f'rgba(214,150,230,{o}),rgba(190,140,235,{o*0.4}) 60%,rgba(214,150,230,0));"></div>'
                         for x, w, o in [(118, 3, .45), (205, 2, .3), (318, 4, .25), (446, 2, .35), (520, 3, .5), (604, 2, .3), (690, 3, .25)])
        return ('<div class="fd" style="background:linear-gradient(180deg,#2c6e97 0%,#3b86b4 45%,#5aa5d3 100%)"></div>'
                + riscos + '<div class="fd pontos" style="opacity:.55"></div>')
    if f.startswith("cor:"):
        return f'<div class="fd" style="background:{f[4:]}"></div>'
    return f'<div class="fd" style="background:{PAPEL}"></div>'


def add(pl, h, z=None):
    pl["els"].append((pl["z"] if z is None else z, h))
    pl["z"] += 1


def anim(eid, t, de, para, d, e="expo.out"):
    ANIMS.append({"k": "ft", "id": eid, "t": round(t, 3), "d": round(d, 3), "de": de, "para": para, "e": e})


def setar(eid, t, props):
    ANIMS.append({"k": "set", "id": eid, "t": round(t, 3), "p": props})


def _hb(sigma):
    """Registra um borrão SÓ horizontal de `sigma` px e devolve o id do filtro SVG."""
    k = f"hb{int(round(sigma * 10))}"
    FILTROS_H[k] = round(sigma, 1)
    return k


def _px(origem):
    """'62% 34%' ou '310px 640px' -> (x, y) em px do palco."""
    return tuple(float(v[:-1]) / 100 * (W if k == 0 else H) if v.endswith("%") else float(v[:-2])
                 for k, v in enumerate(origem.split()))


def SOM(tipo, t, db=0.0):
    """Um efeito do kit (medir/sfx_d.py) no instante da IMAGEM: boom (t = o corte da virada de capítulo), thump/objeto/
    golpe (t = a entrada do elemento), clique (t = o quadro em que a palavra aparece), estalo (t = o corte), inchaco
    (t = o corte SEGUINTE), ar-ondas/ar-curto (t = o gesto). O mix.py põe o pico no lugar medido para cada tipo
    (metas.json › audio › pico_depois_s). A referência não tem efeito fora desses casos: não espalhe SOM pelo reel."""
    SONS.append({"tipo": tipo, "t": round(t, 3), "db": db})


# ------------------------------------------------------------------ elementos
def proporcao(src):
    from PIL import Image
    p = os.path.join(AQUI, src)
    if src.lower().endswith(".svg") and os.path.exists(p):
        import re as _re
        vb = _re.search(r'viewBox="([\d.\s-]+)"', open(p).read())
        if vb:
            _, _, vw, vh = map(float, vb.group(1).split())
            return vh / vw
        return 1.0
    if src.lower().endswith((".mp4", ".mov", ".webm")) or not os.path.exists(p):
        return 16 / 9 if not os.path.exists(p) else 1.0
    with Image.open(p) as im:
        return im.height / im.width


def img(pl, src, x, y, w, h=None, t=None, ent="seco", d=0.5, cinza=False, pontos=False, filtro="", sombra=False,
        origem="50% 50%", z=None, extra="", de=None, ajuste="cover", dentro=""):
    """Imagem/recorte posicionado pelo CENTRO (x, y), largura w (altura pela proporção do arquivo, ou h).
    ent: seco|fade|sobe|desliza_dir|cresce. cinza=True: P&B. pontos=True: retícula por cima. Retorna o id."""
    eid = nid("i")
    h = h or round(w * proporcao(src), 1)
    fil = ("grayscale(1) contrast(1.08) " if cinza else "") + filtro
    sh = "drop-shadow(0 16px 12px rgba(0,0,0,.26)) " if sombra else ""
    pts = '<div class="pontos" style="position:absolute;inset:0;opacity:.5;mix-blend-mode:multiply"></div>' if pontos else ""
    add(pl, f'<div id="{eid}" class="ab" style="left:{x - w / 2}px;top:{y - h / 2}px;width:{w}px;height:{h}px;transform-origin:{origem};{extra}">'
            f'<img src="{src}" style="display:block;width:100%;height:100%;object-fit:{ajuste};filter:{(sh + fil).strip() or "none"}">{pts}{dentro}</div>', z)
    if t is not None:
        entrar(eid, t, ent, d, de)
    return eid


def video(pl, src, inicio=0.0, cinza=False, pontos=False, filtro="", vel=1.0, z=None, x=0, y=0, w=W, h=H):
    """Filme de arquivo cobrindo o quadro. O trecho começa em `inicio` (s dentro do arquivo)."""
    eid = nid("v")
    fil = ("grayscale(1) contrast(1.06) " if cinza else "") + filtro
    pts = '<div class="pontos" style="position:absolute;inset:0;opacity:.55;mix-blend-mode:multiply"></div>' if pontos else ""
    pl.setdefault("videos", []).append({"id": eid, "src": src, "inicio": inicio, "vel": vel, "fil": fil, "x": x, "y": y, "w": w, "h": h})
    if pts:
        add(pl, f'<div class="ab" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{pts}</div>', z)
    return eid


def entrar(eid, t, ent, d=0.5, de=None):
    t = round(t, 3)
    if ent == "seco":
        setar(eid, 0, {"opacity": 0}); setar(eid, t, {"opacity": 1})
    elif ent == "fade":
        setar(eid, 0, {"opacity": 0}); anim(eid, t, {"opacity": 0}, {"opacity": 1}, d, "none")
    elif ent == "sobe":          # objeto que sobe de baixo (roteador, torpedo): impulso e desacelera
        setar(eid, 0, {"opacity": 0}); setar(eid, t, {"opacity": 1})
        anim(eid, t, {"y": de or 520}, {"y": 0}, d, "expo.out")
    elif ent == "desliza_dir":   # entra pela direita (torre, rótulos, print)
        setar(eid, 0, {"opacity": 0}); setar(eid, t, {"opacity": 1})
        anim(eid, t, {"x": de or 260}, {"x": 0}, d, "expo.out")
    elif ent == "cresce":
        setar(eid, 0, {"opacity": 0}); setar(eid, t, {"opacity": 1})
        anim(eid, t, {"scale": de or 0.3}, {"scale": 1}, d, "expo.out")


def _tx(papel, size, cor, extra=""):
    fam = {"serifa": "HoeflerD", "caixa": "HelvD", "ui": "HelvUI"}[papel]
    est = "italic" if papel == "serifa" else "normal"
    pes = 700 if papel == "caixa" else 400
    return (f"font-family:'{fam}';font-style:{est};font-weight:{pes};font-size:{size}px;color:{cor};"
            f"letter-spacing:{TRACK[papel]}em;line-height:1;white-space:nowrap;{extra}")


def texto(pl, txt, x, y, size, papel="serifa", cor=TINTA, alinha="centro", z=None, extra="", partes="palavra"):
    """Bloco de texto ancorado: alinha=centro (x = centro) | esquerda (x = começo). Retorna (id, [ids das partes]).
    partes = palavra | letra | nada. Linhas separadas por '\\n' (sem <br>: cada linha é um bloco)."""
    eid = nid("t")
    linhas = txt.split("\n")
    ids, blocos = [], []
    lh = 0.84 if papel == "serifa" else 1.0
    for li, ln in enumerate(linhas):
        spans = []
        if partes == "palavra":
            for k, w_ in enumerate(ln.split(" ")):
                sid = f"{eid}w{li}_{k}"; ids.append(sid)
                spans.append(f'<span id="{sid}" class="pw">{html.escape(w_)}</span>')
            conteudo = " ".join(spans)
        elif partes == "letra":
            for k, c in enumerate(ln):
                sid = f"{eid}c{li}_{k}"; ids.append(sid)
                spans.append(f'<span id="{sid}" class="pc">{html.escape(c)}</span>')
            conteudo = "".join(spans)
        else:
            conteudo = html.escape(ln)
        ta = "center" if alinha == "centro" else "left"
        blocos.append(f'<div style="text-align:{ta};height:{size * lh}px;line-height:{size * lh}px">{conteudo}</div>')
    largura_box = 700
    left = x - largura_box / 2 if alinha == "centro" else x
    top = y - size * lh * len(linhas) / 2
    add(pl, f'<div id="{eid}" class="ab" style="left:{left}px;top:{top}px;width:{largura_box}px;transform-origin:'
            f'{"50%" if alinha == "centro" else "0"} 50%;{_tx(papel, size, cor, extra)}">{"".join(blocos)}</div>', z)
    return eid, ids


def revela(ids, tempos, t_fim=None):
    """Cada palavra entra apagada (35 %) e no passo seguinte fica inteira (DESMONTE §3/§5)."""
    for sid, t in zip(ids, tempos):
        setar(sid, 0, {"opacity": 0}); setar(sid, g(t), {"opacity": 0.35}); setar(sid, g(t) + PASSO, {"opacity": 1})
        if t_fim is not None:
            setar(sid, t_fim, {"opacity": 0})


def tempos_revela(idx_palavras, t0=None, ritmo=None, adianta=0.65):
    """A frase escrita ACOMPANHA a voz: a palavra k entra em min(início falado, t0 + ritmo × k), e nunca mais de
    `adianta` segundos antes de ser falada (na referência a escrita termina até 0,67 s antes da voz; com ritmo fixo e voz
    mais lenta ela chegava 1,4 s antes). Sem `ritmo`, ele sai da própria fala: 0,57 × o tempo falado ÷ nº de intervalos,
    entre 0,12 e 0,40 s."""
    a = P(idx_palavras[0]) if t0 is None else t0
    if ritmo is None:
        ritmo = min(0.40, max(0.12, 0.57 * (P(idx_palavras[-1]) - a) / max(1, len(idx_palavras) - 1)))
    return [max(min(P(i), a + ritmo * k), P(i) - adianta) for k, i in enumerate(idx_palavras)]


def pop(pl, palavras, y=640, size=64, cor=TINTA, papel="serifa", maxw=560, x=W / 2):
    """Uma palavra por vez no centro, trocada seca; nasce a 0,72x e assenta em 1,0 (ease-out, ~0,35 s).
    palavras = [(texto, t_entra, t_sai)]."""
    for item in palavras:
        txt, t, ts = item[:3]; logo = item[3] if len(item) > 3 else None
        s = cabe(txt, papel, size, maxw)
        if logo:      # logo oficial + nome: os dois nascem e assentam juntos
            lw, lh_ = logo
            eid = nid("t")
            # a PALAVRA fica onde a referência põe a palavra solta (centro em y, corpo inteiro); o logo vai acima dela
            nome = (f'<div style="margin-top:14px;{_tx(papel, s, cor)};text-align:center">{html.escape(txt)}</div>' if txt else "")
            add(pl, f'<div id="{eid}" class="ab" style="left:{x - 300}px;top:{(y - s / 2 - 14 - lh_) if txt else (y - lh_ / 2)}px;width:600px;'
                    f'display:flex;flex-direction:column;align-items:center;transform-origin:50% 50%">'
                    f'<img src="{lw}" style="height:{lh_}px;width:auto;max-width:440px;object-fit:contain">{nome}</div>')
        else:
            eid, _ = texto(pl, txt, x, y, s, papel, cor, partes="nada")
        setar(eid, 0, {"opacity": 0}); setar(eid, g(t), {"opacity": 0.92})
        anim(eid, g(t), {"scale": 0.72}, {"scale": 1}, 0.6, "expo.out")       # medido: 0,68-0,74 -> 0,85-0,94 -> 0,97 -> 1
        setar(eid, g(t) + PASSO, {"opacity": 1})
        if ts < 900:
            setar(eid, g(ts), {"opacity": 0})


def legivel_ate(pl, fim):
    """Último instante em que o plano ainda está nítido (antes dos quadros borrados da saída)."""
    sa = pl.get("saida")
    if not sa:
        return fim
    return round(fim - (max(PASSO, sa.get("d", 0.2)) if sa["tipo"] == "borrao" else PASSO), 3)


def cabe_no_plano(tempos, lim, rotulo=""):
    """Comprime os tempos de digitação para a ÚLTIMA letra entrar até `lim` (o texto fica completo e nítido antes do
    corte, como na referência: EVERYONE completa 0,2 s antes do corte; TECHNOLOGY, 0,4 s). Nunca atrasa nada."""
    a, b = min(tempos), max(tempos)
    lim = g(lim)
    if b <= lim + 1e-6:
        return list(tempos)
    if lim <= a + PASSO or len(tempos) / (lim - a) > 45:
        print(f"AVISO digitação cortada: '{rotulo}' não cabe no plano (começa em {a:.2f} s e o plano só fica nítido até "
              f"{lim:.2f} s). Encurte o texto, comece o plano antes ou divida em dois.")
        lim = max(lim, a + PASSO)
    else:
        print(f"ajuste de digitação: '{rotulo}' comprimida para terminar em {lim:.2f} s (era {b:.2f} s; "
              f"{len(tempos) / (lim - a):.0f} c/s)")
    return [a + (x - a) * (lim - a) / (b - a) for x in tempos]


def digita_queda(pl, txt, x, y, size, papel, cor, letras_t, queda=0.45, alinha="centro", folga=0.2):
    """Cada letra nova entra ~45 % da maiúscula ABAIXO e mais apagada; no passo seguinte sobe para a linha.
    folga: a última letra entra no máximo `folga` antes do fim nítido do plano (0,1 s para assentar + 0,1 s inteira)."""
    eid, ids = texto(pl, txt, x, y, size, papel, cor, alinha, partes="letra")
    for sid in ids:
        setar(sid, 0, {"display": "none"})

    def emite(fim):
        passos = [g(t) for t in cabe_no_plano(letras_t, legivel_ate(pl, fim) - folga, txt)]
        for k, (sid, t) in enumerate(zip(ids, passos)):
            ultima = k + 1 == len(passos) or passos[k + 1] > t
            if ultima and txt[k] != " ":
                setar(sid, t, {"display": "inline-block", "y": size * queda, "opacity": 0.55})
                setar(sid, t + PASSO, {"y": 0, "opacity": 1})
            else:
                setar(sid, t, {"display": "inline-block", "y": 0, "opacity": 1})
    pl.setdefault("tardios", []).append(emite)
    return eid, ids


def digita_cursor(pl, txt, x, y, size, papel, cor, letras_t, cursor_ate=None, alinha="esquerda", sel=None, t_sel=None,
                  sel_antes=0.0, folga=0.3, depois=None):
    """Digitação com barra '|' na ponta (2 caracteres por passo na caixa pequena). sel = (i0, i1) letras selecionadas.
    folga: a última letra entra no máximo `folga` antes do fim nítido do plano (o texto fica inteiro 3 quadros).
    sel_antes: a seleção aparece esse tanto antes da 1ª letra selecionada. depois(tempos): chamado com os tempos FINAIS
    das letras (é onde o molde agenda o punch-in, que depende deles)."""
    eid = nid("t")
    spans, ids = [], []
    for k, c in enumerate(txt):
        sid = f"{eid}c{k}"; ids.append(sid)
        ch = html.escape(c)
        if sel and k == sel[0]:
            spans.append(f'<span id="{eid}sel" class="sel">')
        spans.append(f'<span id="{sid}" class="pc">{ch}</span>')
        if sel and k == sel[1] - 1:
            spans.append(f'<i class="alca a1" style="--s:{size}px"></i><i class="alca a2" style="--s:{size}px"></i></span>')
    spans.append(f'<span id="{eid}cur" class="cur" style="height:{size * 0.95}px;width:{max(2, size * 0.11)}px"></span>')
    left = x if alinha == "esquerda" else x - 350
    ta = "left" if alinha == "esquerda" else "center"
    add(pl, f'<div id="{eid}" class="ab" style="left:{left}px;top:{y - size / 2}px;width:700px;text-align:{ta};'
            f'{_tx(papel, size, cor)};line-height:{size}px">{"".join(spans)}</div>')
    for sid in ids:
        setar(sid, 0, {"display": "none"})
    if sel:
        setar(f"{eid}sel", 0, {"opacity": 0})

    def emite(fim):
        tps = cabe_no_plano(letras_t, legivel_ate(pl, fim) - folga, txt)
        for sid, t in zip(ids, tps):
            setar(sid, g(t), {"display": "inline-block"})
        if sel:
            setar(f"{eid}sel", g(t_sel if t_sel is not None else tps[sel[0]] - sel_antes), {"opacity": 1})
        if depois:
            depois(tps)
    pl.setdefault("tardios", []).append(emite)
    if cursor_ate is not None:
        setar(f"{eid}cur", g(cursor_ate), {"opacity": 0})
    return eid, ids


def tempos_letras(txt, idx_palavras, cps=None, atraso=0.05, inicio=None):
    """Distribui os caracteres de cada palavra DURANTE a palavra falada (medido: atraso ~0,1 s)."""
    pals = txt.split(" ")
    assert len(pals) == len(idx_palavras), (txt, idx_palavras)
    out, fim_ant = [], -1.0
    for k, (p, i) in enumerate(zip(pals, idx_palavras)):
        a = max((P(i) if inicio is None or k else inicio) + atraso, fim_ant + (1 / cps if cps else 0.05))
        b = max(a + 0.05 * len(p), F(i))
        if cps:
            b = a + len(p) / cps
        fim_ant = b
        n = len(p)
        out += [a + (b - a) * j / max(1, n) for j in range(n)]
        if k < len(pals) - 1:
            out.append(b)          # o espaço
    return out


def selecao(eid):
    return f"{eid}sel"


def punch(pl, t, escala=1.9, origem="50% 40%", desfoque=6, d=0.2):
    """Corte para um enquadramento mais fechado NA palavra-chave: entra borrado e foca em 0,2 s."""
    pl.setdefault("punches", []).append({"t": g(t), "s": escala, "o": origem, "b": desfoque, "d": d})


def seta(pl, d_path, t, cor="#2a2a2a", larg=5, cab=16, z=None, desenha=0.3):
    eid = nid("s")
    add(pl, f'<svg id="{eid}" class="ab" style="left:0;top:0;overflow:visible" width="{W}" height="{H}">'
            f'<path class="trc" d="{d_path}" fill="none" stroke="{cor}" stroke-width="{larg}" stroke-linecap="round" pathLength="1" '
            f'stroke-dasharray="1 1"/><path class="pta" d="" fill="none" stroke="{cor}" stroke-width="{larg * 0.8}" stroke-linecap="round" stroke-linejoin="round"/></svg>', z)
    ANIMS.append({"k": "seta", "id": eid, "t": round(t, 3), "d": desenha, "cab": cab})
    return eid


def aneis(pl, cx, cy, raios=(55, 110, 165, 220, 275, 330), cor="255,255,255", t=None, pulso=True, z=None):
    eid = nid("r")
    cs = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="rgba({cor},{max(.08, .42 - k * .06):.2f})" '
                 f'stroke-width="1.6"/>' for k, r in enumerate(raios))
    pul = (f'<circle id="{eid}p" cx="{cx}" cy="{cy}" r="{raios[0] * .55}" fill="none" stroke="rgba({cor},.55)" stroke-width="1.6"/>'
           if pulso else "")
    add(pl, f'<svg id="{eid}" class="ab" style="left:0;top:0;overflow:visible;transform-origin:{cx}px {cy}px" width="{W}" height="{H}">'
            f'{cs}{pul}</svg>', z)
    if pulso:      # svgOrigin: o GSAP não usa o transform-origin do CSS num <circle> (o pulso saía andando na diagonal)
        ANIMS.append({"k": "pulso", "id": f"{eid}p", "pl": pl["id"], "per": 0.6, "o": f"{cx} {cy}"})
    if t is not None:
        entrar(eid, t, "fade", 0.2)
    return eid


def ondas(pl, cx, cy, t, raio=150, ang=34, n=6, cor1=(222, 64, 86), cor2=(250, 214, 220), cresce=0.55, z=None):
    """Leque de ondas em faixas (vermelho saturado -> rosa claro) dos dois lados de um ponto (a antena)."""
    eid = nid("o")
    def setor(r0, r1, a0, a1):
        p = lambda r, a: (cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a)))
        x0, y0 = p(r0, a0); x1, y1 = p(r1, a0); x2, y2 = p(r1, a1); x3, y3 = p(r0, a1)
        return f"M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f} A{r1} {r1} 0 0 0 {x2:.1f} {y2:.1f} L{x3:.1f} {y3:.1f} A{r0} {r0} 0 0 1 {x0:.1f} {y0:.1f}Z"
    paths = []
    for lado in (0, 180):
        for k in range(n):
            r0 = raio * (0.18 + 0.82 * k / n); r1 = raio * (0.18 + 0.82 * (k + 1) / n) - 2
            u = k / max(1, n - 1)
            c = tuple(int(a + (b - a) * (1 - u) * 0.85) for a, b in zip(cor1, cor2))
            a0, a1 = (lado - ang, lado + ang)
            paths.append(f'<path d="{setor(r0, r1, a0, a1)}" fill="rgb{c}" opacity=".93"/>')
    add(pl, f'<svg id="{eid}" class="ab" style="left:0;top:0;overflow:visible;transform-origin:{cx}px {cy}px" width="{W}" height="{H}">'
            + "".join(paths) + "</svg>", z)
    setar(eid, 0, {"opacity": 0}); setar(eid, g(t), {"opacity": 1})
    anim(eid, g(t), {"scale": 0.25}, {"scale": 1}, cresce * 4, "expo.out")
    return eid


def rotulo(pl, txt, x, y, t, w=285, h=80, size=55, z=None, de=440, logo=None, logo_filtro=""):
    """Rótulo azul de interface: retícula, borda clara, sombra deslocada (DESMONTE §5). Entra pela direita.
    logo: arquivo do logo OFICIAL (entra à esquerda do nome, num disco branco)."""
    eid = nid("l")
    lg = h * 0.5
    s = cabe(txt, "caixa", size, w - 30 - (lg + 10 if logo else 0))
    marca = (f'<span style="display:inline-flex;align-items:center;justify-content:center;width:{lg}px;height:{lg}px;border-radius:50%;'
             f'background:#dfe6ea;margin-right:10px;flex:none"><img src="{logo}" style="width:{lg * 0.68}px;height:{lg * 0.68}px;'
             f'object-fit:contain;filter:{logo_filtro or "none"}"></span>') if logo else ""
    add(pl, f'<div id="{eid}" class="ab rot" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<div class="rotc">{marca}<span style="{_tx("caixa", s, "#cfd9e0", "letter-spacing:-0.02em;text-shadow:2px 2px 0 rgba(8,50,95,.55)")}">'
            f'{html.escape(txt)}</span></div></div>', z)
    entrar(eid, t, "desliza_dir", 1.4, de)
    return eid


def anos(pl, a0, a1, t0, t1, y=640, size=67, passo_ano=5, z=None, itens=None):
    """Contador de anos que rola de baixo para cima: segura o primeiro, acelera, assenta no último.
    itens = lista de rótulos no lugar dos anos (ex.: ["hoje", "amanhã"])."""
    eid = nid("a")
    if itens:
        lista = [html.escape(i) for i in itens]
    else:
        lista = list(range(a0, a1 + 1, passo_ano))
        if lista[-1] != a1:
            lista.append(a1)
    alt = size * 1.05
    itens = "".join(f'<div class="ano" style="height:{alt}px;line-height:{alt}px">{a}</div>' for a in lista)
    add(pl, f'<div class="ab" style="left:0;top:{y - alt * 0.95}px;width:{W}px;height:{alt * 1.9}px;overflow:hidden;text-align:center;{_tx("serifa", size, TINTA)}">'
            f'<div id="{eid}" style="position:relative;top:{alt * 0.45}px">{itens}</div></div>', z)     # janela: o vizinho só aparece cortado, rolando
    ANIMS.append({"k": "anos", "id": eid, "t": g(t0), "d": round(t1 - t0, 3), "n": len(lista), "alt": alt})
    return eid


def rasgado(pl, txt, x, y, t, size=60, d=0.45, z=None):
    """Faixa de papel rasgado que cresce da esquerda; as letras acendem salteadas."""
    eid = nid("g")
    larg = largura(txt, "serifa", size) + size * 1.1
    pts, k = [], 0
    for i in range(0, 41):                                   # borda de cima
        pts.append(f"{i * 2.5:.1f}% {random.uniform(0, 20):.1f}%")
    for i in range(1, 8):                                    # lado direito rasgado
        pts.append(f"{100 - random.uniform(0, 4):.1f}% {i * 12.5:.1f}%")
    for i in range(40, -1, -1):                              # borda de baixo
        pts.append(f"{i * 2.5:.1f}% {100 - random.uniform(0, 20):.1f}%")
    for i in range(7, 0, -1):                                # lado esquerdo rasgado
        pts.append(f"{random.uniform(0, 4):.1f}% {i * 12.5:.1f}%")
    spans, ids = [], []
    for c in txt:
        sid = f"{eid}c{k}"; k += 1; ids.append(sid)
        spans.append(f'<span id="{sid}">{html.escape(c)}</span>')
    alt = size * 1.15                 # faixa pouco mais alta que o corpo: ascendentes e descendentes passam da borda, como na referência
    add(pl, f'<div id="{eid}" class="ab" style="white-space:pre;left:{x - larg / 2}px;top:{y - alt / 2}px;width:{larg}px;height:{alt}px">'
            f'<div id="{eid}f" style="position:absolute;inset:-10px">'          # só o invólucro recebe o inset() animado
            f'<div style="position:absolute;inset:0;filter:blur(.6px) drop-shadow(0 2px 2px rgba(0,0,0,.25))">'
            f'<div style="position:absolute;inset:10px;background:#f4f2ee;clip-path:polygon({",".join(pts)})"></div></div></div>'
            f'<div style="position:absolute;inset:0;text-align:center;{_tx("serifa", size, TINTA)};line-height:{alt * 0.94}px;white-space:pre">{"".join(spans)}</div></div>', z)
    setar(f"{eid}f", 0, {"clipPath": "inset(0 100% 0 0)"})          # a faixa só existe depois que começa a rasgar
    anim(f"{eid}f", g(t), {"clipPath": f"inset(0 100% 0 0)"}, {"clipPath": "inset(0 0% 0 0)"}, d, "power2.out")
    ordem = list(range(len(ids))); random.shuffle(ordem)
    for j, k in enumerate(ordem):
        setar(ids[k], 0, {"opacity": 0})
        setar(ids[k], g(t + d * (j + 1) / len(ids)), {"opacity": 1})
    return eid


def brilhos(pl, pontos, t0, t1, tam=34, z=None):
    """Estrelinhas de 4 pontas piscando (joias, brilho do arquivo 'glamour'). pontos = [(x, y), ...]."""
    for k, (x, y) in enumerate(pontos):
        eid = nid("b")
        s = tam * random.uniform(0.6, 1.2)
        add(pl, f'<div id="{eid}" class="ab est" style="left:{x - s / 2}px;top:{y - s / 2}px;width:{s}px;height:{s}px"></div>', z)
        ANIMS.append({"k": "brilha", "id": eid, "pl": pl["id"], "t0": t0, "t1": t1, "per": random.uniform(0.35, 0.7), "fase": random.uniform(0, 1)})


def mao(pl, x0, y0, x1, y1, t, d=0.9, t_clique=None, alvo=None, size=58, z=None):
    """Mãozinha do cursor que vem até o alvo e clica (o alvo encolhe 6 % no clique)."""
    eid = nid("h")
    add(pl, f'<svg id="{eid}" class="ab" style="left:{x1 - size * .3}px;top:{y1 - size * .05}px;overflow:visible" width="{size}" height="{size * 1.15}" '
            f'viewBox="0 0 24 28"><path d="M9 1.5c1.1 0 2 .9 2 2v8.2l.6-.1c1-.2 2 .4 2.3 1.4l.1.3.6-.1c1-.1 1.9.5 2.1 1.5l.1.3.5-.1c1.1-.1 2 .8 2 1.9V22c0 '
            f'3-2.4 5.5-5.5 5.5h-2.6c-1.9 0-3.6-1-4.6-2.6L2.5 18.6c-.6-.9-.3-2.1.6-2.6.8-.5 1.8-.3 2.4.4L7 18.2V3.5c0-1.1.9-2 2-2z" '
            f'fill="#fff" stroke="#111" stroke-width="1.3" stroke-linejoin="round"/></svg>', z)
    setar(eid, 0, {"opacity": 0}); setar(eid, g(t), {"opacity": 1})
    anim(eid, g(t), {"x": x0 - x1, "y": y0 - y1}, {"x": 0, "y": 0}, d, "power3.out")
    if t_clique:
        anim(eid, g(t_clique), {"scale": 0.86}, {"scale": 1}, 0.25, "power2.out")
        if alvo:
            anim(alvo, g(t_clique), {"scale": 0.94}, {"scale": 1}, 0.3, "power2.out")
    return eid


def campo(pl, txt, x, y, t0, t1, w=442, h=60, size=38, z=None, lupa=True):
    h = max(h, size * 1.58)
    """Barra vazada (busca/comentário) com o texto digitado e cursor."""
    eid = nid("c")
    lp = ('<svg style="position:absolute;right:16px;top:50%;margin-top:-17px" width="34" height="34" viewBox="0 0 24 24"><circle cx="10" cy="10" r="7" '
          'fill="none" stroke="#fff" stroke-width="2.4"/><path d="M15.5 15.5L21 21" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/></svg>' if lupa else "")
    add(pl, f'<div id="{eid}" class="ab" style="left:{x - w / 2}px;top:{y - h / 2}px;width:{w}px;height:{h}px;border:2.4px solid #f2f2f2;'
            f'border-radius:{h}px;background:rgba(10,10,10,.25)">{lp}</div>', z)
    tid, ids = digita_cursor(pl, txt, x - w / 2 + 24, y, size, "ui", "#f5f5f5",
                             [t0 + (t1 - t0) * k / max(1, len(txt)) for k in range(len(txt))])
    for k in range(8):                # depois de digitar o cursor PISCA: 0,3 s aceso, 0,2 s apagado (medido)
        setar(f"{tid}cur", g(t1) + 0.4 + 0.5 * k, {"opacity": 0}); setar(f"{tid}cur", g(t1) + 0.6 + 0.5 * k, {"opacity": 1})
    return eid


# ------------------------------------------------------------------ montagem do HTML
CSS = f"""
@font-face{{font-family:'HoeflerD';src:url('assets/fonts/HoeflerText-Italic.ttf') format('truetype');font-style:italic;font-weight:400}}
@font-face{{font-family:'HelvD';src:url('assets/fonts/HelveticaNeue-Bold.ttf') format('truetype');font-weight:700}}
@font-face{{font-family:'HelvUI';src:url('assets/fonts/HelveticaNeue.ttf') format('truetype');font-weight:400}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#000}}
#root{{position:relative;width:100%;height:100%;overflow:hidden;background:{PRETO}}}
.plano{{position:absolute;inset:0;overflow:hidden}}
.cam,.pz,.fx{{position:absolute;inset:0}}
.fd{{position:absolute;inset:-40%}}
.ab{{position:absolute}}
.pw,.pc{{display:inline-block}}
.pc{{white-space:pre}}
.pontos{{background-image:radial-gradient(circle,rgba(0,0,0,.42) 1.15px,rgba(0,0,0,0) 1.7px);background-size:6px 6px}}
.sel{{position:relative;display:inline-block;background:{SELECAO};padding:0 .04em}}
.cur{{display:inline-block;background:currentColor;vertical-align:middle;margin-left:.04em}}
.sel .cur{{position:absolute;right:-.07em;top:.03em}}
.alca{{position:absolute;width:3px;background:{ALCA}}}
.alca::after{{content:"";position:absolute;left:50%;width:calc(var(--s)*.41);height:calc(var(--s)*.41);margin-left:calc(var(--s)*-.205);border-radius:50%;background:{ALCA}}}
.alca.a1{{left:-1.5px;top:-.35em;height:1.6em}} .alca.a1::after{{top:calc(var(--s)*-.3)}}
.alca.a2{{right:-1.5px;top:-.05em;height:1.6em}} .alca.a2::after{{bottom:calc(var(--s)*-.3)}}
.rot .rotc{{position:absolute;inset:0;background:{AZUL_ROT};border:2px solid {AZUL_ROT_BORDA};box-shadow:6px 7px 0 {AZUL_ROT_SOMBRA};
  display:flex;align-items:center;justify-content:center;
  background-image:radial-gradient(circle,rgba(6,58,104,.42) 1.7px,rgba(6,58,104,0) 2.4px),radial-gradient(circle,rgba(6,58,104,.42) 1.7px,rgba(6,58,104,0) 2.4px);
  background-size:7px 7px;background-position:0 0,3.5px 3.5px}}
.est{{background:radial-gradient(circle,#fff 0 18%,rgba(255,252,235,.95) 30%,rgba(255,250,230,.75) 100%);clip-path:polygon(50% 0,56% 44%,100% 50%,56% 56%,50% 100%,44% 56%,0 50%,44% 44%);filter:drop-shadow(0 0 4px rgba(255,255,255,1)) drop-shadow(0 0 2px rgba(120,100,60,.6))}}
.ano{{text-align:center}}
"""


def _confere_ritmo():
    """A DINÂMICA vale para qualquer duração: em média um corte a cada 1,45 a 1,54 s (1,45 = a referência, 22 planos em
    32 s; 1,54 = o teto aprovado pelo Felipe em 13/11/2026). Reel mais longo = MAIS planos, na mesma proporção; nunca os
    mesmos planos esticados nem roteiro encurtado para caber. A faixa mora em medir/metas.json."""
    try:
        m = json.load(open(os.path.join(AQUI, "medir", "metas.json"))).get("ritmo", {})
    except Exception:
        m = {}
    faixa = m.get("plano_medio_s", [1.45, 1.54]); teto = m.get("plano_max_s", 2.9)
    lo, hi = (faixa, faixa) if isinstance(faixa, (int, float)) else (min(faixa), max(faixa))
    planos = []                                   # um "flash" de 1-2 quadros (o close do descarte) conta junto com o seguinte
    for p in PLANOS:
        if planos and planos[-1]["fim"] - planos[-1]["t"] < 0.3:
            planos[-1] = {"t": planos[-1]["t"], "fim": p["fim"], "nome": p["nome"]}
        else:
            planos.append({"t": p["t"], "fim": p["fim"], "nome": p["nome"]})
    n = len(planos); media = round(DUR / n, 2)
    n_min, n_max = math.ceil(DUR / (hi + 0.005)), math.floor(DUR / (lo - 0.005))     # nº de planos que cai na faixa
    faixa_txt = f"{lo:.2f} a {hi:.2f} s".replace(".", ",")
    alvo_txt = f"{n_min}" if n_min >= n_max else f"{n_min} a {n_max}"
    print(f"ritmo: {n} planos em {DUR} s = um corte a cada {media:.2f} s (faixa do motor: {faixa_txt} -> {alvo_txt} planos para esta duração)")
    if media > hi:
        print(f"AVISO ritmo: faltam ~{n_min - n} cortes para manter a dinâmica. Divida os planos mais longos:")
        for p in sorted(planos, key=lambda p: p["t"] - p["fim"])[:max(3, n_min - n)]:
            print(f"    {p['nome']:<16} {p['t']:>5.1f}-{p['fim']:<5.1f} ({p['fim'] - p['t']:.1f} s)")
    elif media < lo:
        print(f"AVISO ritmo: {n - n_max} cortes a mais que a dinâmica da referência (planos curtos demais).")
    else:
        for p in planos:
            if p["fim"] - p["t"] > teto + 1e-6:
                print(f"AVISO plano longo: {p['nome']} {p['t']:.1f}-{p['fim']:.1f} ({p['fim'] - p['t']:.1f} s; teto {teto} s)")


def gerar():
    import importlib.util, sys
    sys.modules["build"] = sys.modules[__name__]
    spec = importlib.util.spec_from_file_location("cenas", os.path.join(AQUI, "cenas.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    PLANOS.sort(key=lambda p: p["t"])
    corpo = []
    for k, pl in enumerate(PLANOS):
        fim = PLANOS[k + 1]["t"] if k + 1 < len(PLANOS) else DUR
        dur = round(fim - pl["t"], 3)
        pl["fim"] = fim
        els = "".join(h for _, h in sorted(pl["els"], key=lambda e: e[0]))
        vids = ""
        for v in pl.get("videos", []):
            vids += (f'<video id="{v["id"]}" src="{v["src"]}" muted playsinline data-start="{pl["t"]}" data-duration="{dur}" '
                     f'data-media-start="{v["inicio"]}" data-track-index="{20 + k}" style="position:absolute;left:{v["x"]}px;top:{v["y"]}px;'
                     f'width:{v["w"]}px;height:{v["h"]}px;object-fit:cover;filter:{v["fil"] or "none"}"></video>')
        setar(pl["id"], 0, {"display": "none"}); setar(pl["id"], pl["t"], {"display": "block"})
        if k + 1 < len(PLANOS):
            setar(pl["id"], fim, {"display": "none"})
        corpo.append(f'<div id="{pl["id"]}" class="plano" style="z-index:{k + 1}">{_fundo_html(pl["fundo"])}<div id="{pl["id"]}c" class="cam"><div id="{pl["id"]}z" class="pz"><div id="{pl["id"]}x" class="fx">'
                     f'{vids}{els}</div></div></div></div>')
        # câmera: impulso no corte que decai exponencialmente (expo.out com duração 6,93*tau)
        c = pl["cam"]; tau = c.get("tau", 0.4); D = round(6.93 * tau, 3)
        tipo = c.get("tipo", "parado")
        o = c.get("origem", "50% 50%")
        setar(f'{pl["id"]}c', 0, {"transformOrigin": o})
        if tipo in ("afasta", "aproxima"):
            de = c.get("de", 1.5 if tipo == "afasta" else 1.0); ate = c.get("ate", 1.0 if tipo == "afasta" else 1.36)
            t_mov = pl["t"]
            if c.get("salto"):        # 1º quadro num enquadramento bem mais fechado (o quadro dourado "gigante")
                setar(f'{pl["id"]}c', pl["t"], {"scale": c["salto"]}); t_mov = round(pl["t"] + PASSO, 3)
            anim(f'{pl["id"]}c', t_mov, {"scale": de, "x": c.get("x", 0), "y": c.get("y", 0)}, {"scale": ate, "x": 0, "y": 0}, D, c.get("ease", "expo.out"))
        elif tipo in ("pan", "desliza"):
            anim(f'{pl["id"]}c', pl["t"], {"x": c.get("x", 0), "y": c.get("y", 0), "scale": c.get("de", 1)},
                 {"x": c.get("x1", 0), "y": c.get("y1", 0), "scale": c.get("ate", c.get("de", 1))},
                 c.get("d", D), c.get("ease", "expo.out"))
        elif tipo == "degraus":
            ANIMS.append({"k": "degraus", "id": f'{pl["id"]}c', "t": pl["t"], "D": D, "passos": c["passos"], "fim": fim})
        elif tipo == "deriva":
            anim(f'{pl["id"]}c', pl["t"], {"scale": c.get("de", 1.0)}, {"scale": c.get("ate", 1.04)}, dur, "none")
        for tardio in pl.get("tardios", []):      # digitações: só agora se sabe onde o plano acaba (podem agendar punch)
            tardio(fim)
        # som da referência que depende do corte: o inchaço grave sob a colagem que atravessa em pan morre antes do corte
        if pl["nome"] == "colagem" and pl["cam"].get("tipo") == "pan" and "x1" in pl["cam"] and k + 1 < len(PLANOS):
            SOM("inchaco", fim)
        fx = f'{pl["id"]}x'
        en = pl.get("entrada")
        if en:                                     # 1º quadro desfocado, 2º nítido (medido no corte 2->3 da referência)
            setar(fx, pl["t"], {"filter": f'blur({en.get("b", 3)}px)'}); setar(fx, round(pl["t"] + PASSO, 3), {"filter": "blur(0px)"})
        for pu in pl.get("punches", []):
            if pu["b"] > 0 and pu["t"] - PASSO > pl["t"]:      # o quadro ANTES do punch já vem desfocado (medido: ~3 px)
                setar(f'{pl["id"]}z', round(pu["t"] - PASSO, 3), {"filter": f'blur({min(3, pu["b"] / 2):.1f}px)'})
            setar(f'{pl["id"]}z', pu["t"], {"transformOrigin": pu["o"], "scale": pu["s"]})
            anim(f'{pl["id"]}z', pu["t"], {"filter": f'blur({pu["b"]}px)'}, {"filter": "blur(0px)"}, pu["d"], "power1.out")
        sa = pl.get("saida")
        if sa and k + 1 < len(PLANOS):
            # Saídas gravadas PASSO A PASSO: um tween de 0,1-0,2 s a 10 fps só é amostrado no começo (valor zero), e a
            # saída não aparecia no vídeo. Os filtros valem em px locais: divide pela escala do punch-in, se houver.
            pu = pl["punches"][-1] if pl.get("punches") else None
            esc = pu["s"] if pu else 1.0
            if sa["tipo"] == "borrao":
                n = max(1, round(sa.get("d", 0.2) / PASSO)); b = sa.get("b", 4)
                for j in range(1, n + 1):          # medido na saída da colagem: ~1,5 px e depois 4 px
                    setar(fx, round(fim - (n - j + 1) * PASSO, 3), {"filter": f'blur({b * (j / n) ** 1.5 / esc:.2f}px)'})
            elif sa["tipo"] == "chicote":          # medido: desloca ~-27 px, borrão só horizontal ~3 px, texto legível
                setar(fx, round(fim - PASSO, 3), {"filter": f'url(#{_hb(sa.get("b", 3) / esc)})', "x": round(sa.get("x", -27) / esc, 1)})
            elif sa["tipo"] == "zoom":             # medido: x0,990 · 0,979 · 0,946 · 0,823 (= x0,755); só o último quadro borra
                n = max(1, round(sa.get("d", 0.4) / PASSO)); s_fim = sa.get("s", 0.755)
                perfil = (0.036, 0.112, 0.308, 1.0) if n == 4 else [(j / n) ** 3 for j in range(1, n + 1)]
                cx, cy = W / 2, H / 2              # afasta em torno do centro da TELA (em coordenadas locais, se houve punch)
                if pu:
                    ox, oy = _px(pu["o"]); cx, cy = ox + (cx - ox) / esc, oy + (cy - oy) / esc
                setar(fx, round(fim - n * PASSO, 3), {"transformOrigin": f"{cx:.1f}px {cy:.1f}px"})
                for j, u in enumerate(perfil, 1):
                    p_ = {"scale": round(s_fim ** u, 4)}
                    if j == n:
                        p_["filter"] = f'url(#{_hb(sa.get("b", 2.5) / esc)})'
                    setar(fx, round(fim - (n - j + 1) * PASSO, 3), p_)
    _confere_ritmo()
    try:                                           # o estalo da referência: uma vez, no corte que abre o CTA
        atos = json.load(open(os.path.join(AQUI, "medir", "atos.json")))
        if "cta" in atos:
            t_cta = CORTE(atos.index("cta")); perto = min(PLANOS, key=lambda p: abs(p["t"] - t_cta))
            if abs(perto["t"] - t_cta) <= 0.25 and perto["t"] > 0:
                SOM("estalo", perto["t"])
    except Exception:
        pass
    janelas = {p["id"]: (p["t"], p["fim"]) for p in PLANOS}
    extra = []
    for a in [a for a in ANIMS if a["k"] in ("brilha", "pulso")]:
        a0, a1 = janelas[a["pl"]]
        if a["k"] == "brilha":
            a0 = max(a0, a["t0"]); a1 = min(a1, a["t1"]); per = a["per"]; t = a0 + a["fase"] * per; ang = random.uniform(0, 45)
            extra.append({"k": "set", "id": a["id"], "t": 0, "p": {"scale": 0, "opacity": 0}})
            while t < a1:
                extra.append({"k": "ft", "id": a["id"], "t": round(t, 3), "d": round(per / 2, 3), "de": {"scale": 0, "opacity": 0, "rotation": ang},
                              "para": {"scale": 1, "opacity": 1, "rotation": ang + 25}, "e": "sine.out"})
                extra.append({"k": "ft", "id": a["id"], "t": round(t + per / 2, 3), "d": round(per / 2, 3), "de": {"scale": 1, "opacity": 1, "rotation": ang + 25},
                              "para": {"scale": 0, "opacity": 0, "rotation": ang + 50}, "e": "sine.in"})
                t += per * random.uniform(1.4, 2.6); ang += 50
        else:
            t = a0
            while t < a1:
                extra.append({"k": "ft", "id": a["id"], "t": round(t, 3), "d": a["per"], "de": {"scale": 0.15, "opacity": 1, "svgOrigin": a["o"]},
                              "para": {"scale": 1.25, "opacity": 0, "svgOrigin": a["o"]}, "e": "none"})
                t += a["per"]
    ANIMS[:] = [a for a in ANIMS if a["k"] not in ("brilha", "pulso")] + extra
    sons_path = os.path.join(AQUI, "medir", "sons.json")
    json.dump(sorted(SONS, key=lambda s: s["t"]), open(sons_path, "w"), indent=1)
    json.dump([{"id": p["id"], "t": p["t"], "fim": p["fim"], "nome": p["nome"], "fundo": p["fundo"]} for p in PLANOS],
              open(os.path.join(AQUI, "medir", "planos.json"), "w"), indent=1, ensure_ascii=False)
    js = r"""
const A = __ANIMS__;
const tl = gsap.timeline({ paused: true });
const $ = (i) => document.getElementById(i);
for (const a of A) {
  const el = $(a.id); if (!el) continue;
  if (a.k === "set") { if (a.t <= 0) gsap.set(el, a.p); tl.set(el, a.p, a.t); }
  else if (a.k === "ft") tl.fromTo(el, a.de, Object.assign({ duration: a.d, ease: a.e, immediateRender: false }, a.para), a.t);
  else if (a.k === "seta") {
    const p = el.querySelector(".trc"), pt = el.querySelector(".pta");
    gsap.set(el, { opacity: 0 }); tl.set(el, { opacity: 1 }, a.t);
    tl.fromTo(p, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: a.d, ease: "power1.inOut", immediateRender: false }, a.t);
    const L = p.getTotalLength(), e = p.getPointAtLength(L), b = p.getPointAtLength(Math.max(0, L - 8));
    const ang = Math.atan2(e.y - b.y, e.x - b.x), c = a.cab, w = c * .7;
    const Q = (r, s) => [e.x + Math.cos(ang + s) * r, e.y + Math.sin(ang + s) * r];
    const q1 = Q(-c, -Math.atan(w / c)), q2 = Q(-c, Math.atan(w / c));
    pt.setAttribute("d", `M${q1[0]} ${q1[1]} L${e.x} ${e.y} L${q2[0]} ${q2[1]}`);
    gsap.set(pt, { opacity: 0 }); tl.set(pt, { opacity: 1 }, a.t + a.d * .9);
  }
  else if (a.k === "anos") {
    const it = [...el.children], st = { p: 0 };
    const upd = () => { const pos = st.p * (a.n - 1);
      el.style.transform = `translateY(${(-pos * a.alt).toFixed(2)}px)`;
      it.forEach((c, k) => { const s = k - pos, dd = Math.abs(s);
        c.style.opacity = Math.max(0, 1 - dd * 1.05).toFixed(3);
        c.style.filter = `blur(${Math.min(3.5, dd * 2.6).toFixed(2)}px)`; }); };
    upd(); tl.fromTo(st, { p: 0 }, { p: 1, duration: a.d, ease: "sine.inOut", immediateRender: false, onUpdate: upd }, a.t);
  }
  else if (a.k === "degraus") {
    const st = { t: 0 }, eo = (p) => p >= 1 ? 1 : 1 - Math.pow(2, -10 * p);
    const f = () => { let x = 0, y = 0, s = 1;
      for (const [t0, dx, dy, ds] of a.passos) { if (st.t < t0) { x += dx; y += dy; s *= ds; continue; }
        const u = 1 - eo((st.t - t0) / a.D); x += dx * u; y += dy * u; s *= Math.pow(ds, u); }
      el.style.transform = `translate(${x.toFixed(2)}px,${y.toFixed(2)}px) scale(${s.toFixed(4)})`; };
    f(); tl.fromTo(st, { t: a.t }, { t: a.fim, duration: a.fim - a.t, ease: "none", onUpdate: f, immediateRender: false }, a.t);
  }
}
tl.set({}, {}, __DUR__);
window.__timelines["main"] = tl;
"""
    js = js.replace("__ANIMS__", json.dumps(ANIMS)).replace("__DUR__", str(DUR))
    filtros = "".join(f'<filter id="{k_}" x="-20%" y="-5%" width="140%" height="110%"><feGaussianBlur stdDeviation="{v} 0"/></filter>'
                      for k_, v in sorted(FILTROS_H.items()))
    doc = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{html.escape(PROJ.get("titulo", "Reel estilo D"))}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}" data-fps="10">
<svg width="0" height="0" style="position:absolute">{filtros}</svg>
{chr(10).join(corpo)}
</div>
<script>{js}</script>
</body>
</html>
'''
    open(os.path.join(AQUI, "index.html"), "w").write(doc)
    print(f"index.html: {len(PLANOS)} planos, {len(ANIMS)} animações, {len(SONS)} efeitos, {DUR} s")


if __name__ == "__main__":
    gerar()
