# TABELA DE CENAS · motor reel editorial. Executada por build.py (que fornece scene, L, I, RAW, PILL, BADGES, ANIM, SOM, P, S, INI, ONS, DISS).
# Preencha seguindo ~/.claude/skills/reels-sem-aparecer/motores/editorial/MOTOR.md §4 (moldes) e §5 (cadência). Exemplo completo e aprovado: ~/.claude/skills/reels-sem-aparecer/motores/editorial/referencia/cenas-exemplo-conversa-parada.py
# P(i) = entra na i-ésima palavra falada (índices: python3 -c "import json;[print(i,w['text']) for i,w in enumerate(json.load(open('medir/alinhamento.json')))]")
# Espaço 720x1280. Tempos: P(i) = i-ésima palavra da narração (medir/alinhamento.json); P(i, d) = entrada em d quadros; INI = já na tela.
# Fontes: s = Poppins · b = manuscrita reforçada · o = manuscrita · d = serifada itálica · h = Helvetica (perguntas digitadas).
# Regras: nenhuma palavra cortada (margem de 40 px); logo oficial do Claude em toda menção; nada de interface redesenhada.

G = "#505050"      # cinza das palavras gigantes
GL = "#575757"
MARCA = "#d97757"  # laranja oficial do Claude (só no logo e em acentos mínimos)


def LOGO(w):
    return f'<img src="assets/img/claude.svg" style="width:{w}px;height:{w}px;display:block">'


def RELOGIO(p, w, hora=12, minuto=30):
    """Relógio de parede desenhado: ponteiros exatos (o gerador de imagem erra a hora)."""
    ah = (hora % 12) * 30 + minuto * 0.5; am = minuto * 6
    marcas = "".join(f'<line x1="100" y1="{16 if k % 3 == 0 else 20}" x2="100" y2="{30 if k % 3 == 0 else 27}" stroke="#333" stroke-width="{4 if k % 3 == 0 else 2}" transform="rotate({k * 30} 100 100)"/>' for k in range(12))
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 200 200" style="filter:drop-shadow(6px 9px 10px rgba(0,0,0,.25))"><circle cx="100" cy="100" r="92" fill="#fff" stroke="#2b2b2b" stroke-width="9"/>{marcas}'
            f'<line x1="100" y1="100" x2="100" y2="52" stroke="#222" stroke-width="8" stroke-linecap="round" transform="rotate({ah} 100 100)"/>'
            f'<g id="{p}min"><line x1="100" y1="100" x2="100" y2="30" stroke="#222" stroke-width="5" stroke-linecap="round" transform="rotate({am} 100 100)"/></g>'
            f'<circle cx="100" cy="100" r="7" fill="#222"/></svg>')


def BARRA(p, w=520, h=54, de=0.82):
    """Barra de limite: trilho claro + preenchimento escuro (id {p}f) que pode esvaziar."""
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="filter:drop-shadow(5px 7px 8px rgba(0,0,0,.22))"><rect x="0" y="0" width="{w}" height="{h}" rx="{h / 2}" fill="#e3e3e3"/>'
            f'<clipPath id="{p}c"><rect x="0" y="0" width="{w}" height="{h}" rx="{h / 2}"/></clipPath>'
            f'<rect id="{p}f" x="0" y="0" width="{w * de}" height="{h}" fill="#505050" clip-path="url(#{p}c)"/></svg>')


def CHAVE(p, w=220, ligada=True):
    """Chave liga/desliga genérica (não é a interface do Claude Code): trilho id {p}t, botão id {p}b."""
    h = w * 0.52; r = h / 2
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="filter:drop-shadow(6px 8px 9px rgba(0,0,0,.25))"><rect id="{p}t" x="0" y="0" width="{w}" height="{h}" rx="{r}" fill="{"#4d4d4d" if ligada else "#cfcfcf"}"/>'
            f'<circle id="{p}b" cx="{w - r if ligada else r}" cy="{r}" r="{r - 9}" fill="#fff"/></svg>')


def LINHAS(n, w, cor="#c9c9c9", h=9, vao=11, ult=0.6):
    return "".join(f'<div style="height:{h}px;margin-bottom:{vao}px;border-radius:5px;background:{cor};width:{(ult if k == n - 1 else 1) * w if k % 3 else w * 0.86}px"></div>' for k in range(n))


def OLHO(p, w):
    """Olho com pálpebras que fecham numa curva (ids com prefixo p). Abertura e olhar são animados por ANIM lid/move."""
    h = round(w * 130 / 300)
    d = "M4 65 Q150 168 296 65 Q150 168 4 65Z"
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 300 130" style="overflow:visible"><defs>'
            f'<clipPath id="{p}c"><path id="{p}cp" d="{d}"/></clipPath>'
            f'<radialGradient id="{p}g" cx=".5" cy=".45" r=".62"><stop offset="0" stop-color="#fff"/><stop offset=".72" stop-color="#f4f4f6"/><stop offset="1" stop-color="#cfd0d6"/></radialGradient>'
            f'<linearGradient id="{p}i" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f4fc9"/><stop offset=".3" stop-color="#5a6fc0"/><stop offset=".5" stop-color="#dea066"/><stop offset="1" stop-color="#f2cda6"/></linearGradient>'
            f'<filter id="{p}s" x="-20%" y="-40%" width="140%" height="200%"><feDropShadow dx="4" dy="7" stdDeviation="5" flood-color="#000" flood-opacity=".22"/></filter></defs>'
            f'<g filter="url(#{p}s)"><path id="{p}f" d="{d}" fill="url(#{p}g)"/></g>'
            f'<g clip-path="url(#{p}c)"><g id="{p}iris"><circle cx="150" cy="65" r="60" fill="url(#{p}i)"/><circle cx="154" cy="63" r="26" fill="#1b1b1d"/></g></g>'
            f'<path id="{p}b" d="{d}" fill="none" stroke="#46528a" stroke-width="4.2" stroke-linejoin="round" stroke-linecap="round"/></svg>')


CARTAO = "background:#fff;border-radius:18px;box-shadow:12px 16px 30px rgba(0,0,0,.2);"

CINZA_FUNDO = '<div style="width:720px;height:{h}px;background:linear-gradient(to bottom,rgba(0,0,0,{a}),rgba(0,0,0,{b}) 70%,rgba(0,0,0,0))"></div>'
BR = "#fff"


def TELA(src, pos="center center", h=640, a=.55, b=.25):
    """Molde C: foto em tela cheia, sempre em corte seco, com escurecimento no topo para o texto branco."""
    I(src, 360, -4, 724, h=1290, cut=True, pos=pos, z=1)
    RAW(CINZA_FUNDO.format(h=h, a=a, b=b), 360, 0, cut=True, z=2, anc="tc")




# ============================== MODELO (apague e escreva as cenas do roteiro) ==============================
# 1 — primeira frase: abre com o impacto e com a imagem já na tela (molde A: recorte P&B com base esfumada)
scene(0.0, cam=(0.95, 0, 14))
SOM("impacto", INI)
RAW(LOGO(104), 360, 186, cut=True, z=2)
L([("O", INI), ("Claude", P(1)), ("Code", P(2))], 360, 284, 66)
# I("pessoa.png", 360, 520, 420, t=P(3, 9), mask=(68, 97), z=2)

# A segunda troca de cena é a única dissolvência do vídeo (as outras são corte seco):
# _f2 = round((ONS[i]["start"] - 0.10) * 30); DISS[_f2] = (_f2 + 8, _f2 + 14, "blur")   # antes de scene(i)
