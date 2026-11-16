"""cenas.py — a decupagem de UM reel do estilo D. Escreva este arquivo depois de `./reel.sh voz` e `./reel.sh indices`.

Esqueleto do original (22 planos em 32 s = um corte a cada ~1,45 s; DESMONTE-D §2) e o molde de cada um.
A DINÂMICA vale para qualquer duração: em média um corte a cada 1,45 a 1,54 s (a faixa do motor). Reel mais longo = MAIS
planos na mesma proporção (planos por ato ≈ duração falada do ato ÷ 1,5), dividindo os trechos longos com as mesmas
famílias. O build avisa (`AVISO ritmo: faltam ~N cortes`). Exemplo de reel mais longo que o original, com mais planos:
~/.claude/skills/reels-sem-aparecer/motores/documentario/referencia/cenas-exemplo-noticia-processo-ia.py.
O que é deste reel (pronúncia de siglas, posição de uma legenda, cor de um filtro) fica AQUI e em narracao/pronuncia.json,
nunca no motor.
Copie, troque imagens e índices:

  [gancho]   titulo_digitado(0, "TODO MUNDO", [0, 1])                                       ESCURO-DIGITA
             colagem(CORTE(i), [recorte P&B + UM objeto de cor], legenda=..., seta_d=..., punch_em=P(chave)-0.1)
             plano "papel" + multidão P&B com a personagem pequena EM COR + 3 palavras espaçadas (pan sine.inOut)
             documento(CORTE(i), doc, "FRASE EM CAIXA-ALTA", idx, chave=(k, k))                DOCUMENTO-DIGITA
             objeto_escuro(CORTE(i), objeto_branco, "PONTE COM O DIA A DIA.", idx)              + thump
  [contexto] arquivo(..., pontos=True, legenda=dict(txt="Época", idx=[...]))                   ARQUIVO + data digitada
             arquivo(retrato/filme P&B da personagem)
             palavras(CORTE(i), [("não", i), ...])                                              PALAVRAS
  [feito]    diagrama(CORTE(i), traço, "linha pequena", "Linha Grande", idx, doc_src=..., antena=...)   + boom
             arquivo(B-roll de época)
             cena_cor(CORTE(i), objeto, "rótulo rasgado", idx, t_consequencia=...)
  [rejeicao] descarte(CORTE(i), sala_PB, cesto_de_cor, bola_de_papel, desenho_src=traço)
  [salto]    anos_rolando(CORTE(i), ano0, ano1)
             foto(CORTE(i), foto_real, boom=True)
             palavras(...)
             rotulos(CORTE(i), [("Item 1", i1), ("Item 2", i2), ("Item 3", i3)])                + thump em cada
  [moral]    arquivo(retrato "glamour", brilho=dict(pontos=[...]))  x2 (o 2º mais fechado, desfoca_fim=0.3)
             quadro(CORTE(i), retrato, "assets/img/moldura.png", "linha 1\\nlinha 2", idx)
  [cta]      arquivo(B-roll, legenda=dict(txt="Vocativo", idx=[i]))
             cta_icone(CORTE(i), fundo_escuro, ícone, t_clique=P(j))                            + boom
             cta_campo(CORTE(i), fundo, "PALAVRA", P(k), P(k) + 0.3, size=32)

Exemplo completo e testado: ~/.claude/skills/reels-sem-aparecer/motores/documentario/referencia/cenas-exemplo-ada-lovelace.py (com fala-exemplo-ada-lovelace.txt).
"""
from build import *
from moldes import *

raise SystemExit("cenas.py ainda é o modelo: escreva a decupagem deste reel (ver o exemplo em ~/.claude/skills/reels-sem-aparecer/motores/documentario/referencia/cenas-exemplo-ada-lovelace.py)")
