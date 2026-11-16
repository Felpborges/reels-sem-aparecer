# Motor DOCUMENTÁRIO ("o documentário de arquivo em fita") — o estilo D

*Motor da skill `reels-sem-aparecer`. Criado em 13/11/2026 a partir de um reel de referência de 32,0 s, validado por uma
recriação (passou no teste de movimento) e por um reel do zero num tema novo ("A primeira programadora", Ada Lovelace,
38,8 s). O vídeo de referência não acompanha a skill; as medidas dele, sim. Neste manual, "D" é este motor.
Revisado em 13/11/2026 depois da auditoria quadro a quadro contra a referência:
defeitos de saída, digitação, branco, cor e mixagem corrigidos (§9) e regra de ritmo proporcional (§3).*

> **Como ler este manual.** “O Felipe” é o Felipe Borges, que criou e validou este motor; cada reprovação dele registrada
> aqui virou regra e vale para qualquer pessoa. O que é escolha de cada reel (tema, texto, voz, trilha, imagens) é de quem
> está fazendo o reel. Os comandos partem da pasta do projeto criado pelo `novo-reel.sh`; os arquivos de `referencia/`
> ficam em `~/.claude/skills/reels-sem-aparecer/motores/<motor>/referencia/`.

> **Motor independente.** Não usa, não lê e não altera nada dos motores A (editorial), B
> (dentro do mundo) e C (quadro neon). Scripts, metas, fontes, efeitos, trilha e regras do D vivem só aqui.
> Nunca misturar estilos no mesmo reel.

**O estilo em uma frase:** um mini-documentário de arquivo em fita velha — uma narradora conta uma história esquecida em
7 atos, cortando a cada ~1,45 s entre arquivo de época, colagens recortadas sobre papel cinza (sujeito em P&B + UMA cor),
palavras serifadas itálicas que aparecem uma a uma e cenas escuras com caixa-alta digitada; tudo animado "em três"
(10 fps), com linhas de varredura que tremem a 6 fps, separação RGB, câmera que entra com impulso e desacelera em todo
plano, e som quase só de voz + cama de piano/cordas, com um boom sub nas viradas de capítulo.

**Regra-mãe:** do original copiamos estrutura, ritmo, física, tipografia, pós e som. Tema, frases, imagens e termos são de
quem faz o reel. Tudo aqui foi medido e validado pela recriação. **Não mudar número sem medir de novo.**

**O que é do motor × o que é de cada reel (regra do Felipe, 14/11/2026).** O motor serve para qualquer tema, então só
guarda o que vem da REFERÊNCIA e vale para todo reel: ritmo, moldes, tamanhos de texto, pele, regras de som. Tudo que é
refinamento de UM reel fica na pasta daquele reel e nunca entra em `base/` nem neste manual: a pronúncia de uma sigla
(`narracao/pronuncia.json`), a posição de uma legenda, o filtro de uma imagem, a escolha da voz, o texto. Antes de mexer
em `base/`, a pergunta é: "isso valeria para um reel de outro assunto?". Se não, é do reel.

---

## 1 · Pipeline

```bash
bash ~/.claude/skills/reels-sem-aparecer/ferramentas/novo-reel.sh documentario <pasta-do-reel> fala.txt "Título do reel"   # cria o projeto (copia base/, lê o roteiro)
cd <pasta-do-reel>
# imagens (§5) em assets/img/ (recortes: medir/recorte.py) · cama em assets/trilha.mp3 (§6)
./reel.sh voz narracao-provisoria.mp3                        # voz gerada com narracao/fala-para-voz.txt; aperta as pausas (§4)
./reel.sh indices                                            # palavra · índice · tempo · ato -> o mapa para cenas.py
# escrever cenas.py (um molde por plano, §3; exemplo em referencia/cenas-exemplo-ada-lovelace.py)
./reel.sh conferir-fala                                      # nenhuma frase sumiu
./reel.sh quadros 1.6 4.2 14.5                               # PNGs rápidos do conteúdo limpo
./reel.sh montar                                             # build -> render 10 fps -> efeitos -> mix -> película -> teste de movimento -> folhas
# NO FIM: a pessoa escolhe a voz -> ./reel.sh voz escolhida.mp3 && ./reel.sh montar (todos os tempos se refazem)
```
Saídas: `renders/<nome>.mp4` (1080×1920, 30 fps), `renders/<nome>-compartilhar.mp4`, `renders/<nome>-folha-0*.jpg`.
**Olhar as folhas antes de entregar** (o automático não pega imagem com cara de IA, texto que encosta, recorte sujo).

Ambiente: tudo vem do `instalar.sh` da skill (Python próprio com demucs, librosa, rembg e o alinhador em português; HyperFrames na versão validada; `ffmpeg` e `rubberband`). O `reel.sh` de cada projeto já usa esse ambiente sozinho. Para conferir a máquina: `bash ~/.claude/skills/reels-sem-aparecer/ferramentas/diagnostico.sh`. As três fontes deste motor (Hoefler Text Italic, Helvetica Neue e Helvetica Neue Bold) são tiradas do próprio macOS pelo instalador (`~/.claude/skills/reels-sem-aparecer/ferramentas/fontes-do-sistema.py`); se o build reclamar de fonte faltando, rode o instalador de novo.

## 2 · Roteiro — `fala.txt` marcado por ATO

```
[gancho] Todo mundo lembra do pai dela. Quase ninguém sabe que ela escreveu o primeiro programa de computador da história.
[contexto] No século dezenove, Ada Lovelace não estava só traduzindo um artigo.
[feito] Ela escreveu um algoritmo para uma máquina que ainda nem existia.
[rejeicao] A máquina nunca foi construída.
[salto] Cem anos depois, a mesma ideia virou a base de computadores, aplicativos e inteligência artificial.
[moral] O mundo lembrou dela como filha de um poeta, mas a história lembra dela como a primeira programadora.
[cta] Se você quer criar programas com IA sem saber programar, comenta ADA aqui embaixo.
```
| Ato | Regra (medida) | Palavras no original |
|---|---|---|
| gancho | contraste fama × feito escondido; a 2ª frase liga ao dia a dia de quem assiste | 17 |
| contexto | "Em/Durante <época>, <personagem> não estava só <o óbvio>." | 11 |
| feito | concreto e visual (dá para desenhar) | 13 |
| rejeicao | frase curta e seca (4-6 palavras) | 5 |
| salto | "<N> anos depois, a mesma ideia virou a base de <A>, <B> e <C>." — 3 itens que o público usa | 15 |
| moral | quiasmo que repete a palavra-tema do gancho: "O mundo lembrou dela como X, mas a história lembra dela como Y." | 15 |
| cta | vocativo/condição + ação + destino; a palavra-código vira o texto digitado no campo | 10 |

- **Tamanho: livre.** O roteiro pode ser maior ou menor que o do original; o que não muda é a DINÂMICA (§3, "Sequência e
  ritmo"): roteiro maior = mais planos. Para estimar: em português cada palavra ocupa ~0,43 s de tela (93 palavras deram
  38,8 s; 101 deram 45,2 s). `./reel.sh texto` conta por ato contra o original.
- **Números por extenso** (é o que a narradora fala); a data abreviada vai para a TELA ("Século XIX", "WW2").
- **Fatos:** checar cada afirmação (é conteúdo educativo). Nada de "ninguém deu bola" se a história não for essa.
- Pronúncia de nome estrangeiro/sigla: `narracao/pronuncia.json` de cada reel, com duas listas: `"alinhamento"` (como soa,
  só para o alinhador) e `"voz"` (como escrever para o gerador de voz ler certo; ver §4). O motor não guarda palavra
  nenhuma. Exemplos dos dois reels feitos: `referencia/pronuncia-exemplo-*.json`.

## 3 · Os moldes (`base/moldes.py`) — o que cada plano vira

Convenção: `t = CORTE(i)` (o corte cai 0,07 s antes da 1ª palavra que o plano ilustra, na grade de 10 fps); o plano vai
até o próximo. `P(i)` / `F(i)` = início / fim da palavra i. Palco 720×1280 (as medidas do original valem 1:1).

| Molde | Família (planos no original) | O que faz (números medidos) |
|---|---|---|
| `titulo_digitado(t, txt, idx)` | ESCURO-DIGITA (1) | preto com grade/poeira; Helvetica Neue Bold caixa-alta, cada letra entra 45 % ABAIXO e apagada e sobe no passo seguinte (só a última do passo cai); centralizado crescendo; push-in 0,56→1,0 (τ 0,15 s); sai em chicote horizontal |
| `colagem(t, imgs, legenda, seta_d, punch_em)` | COLAGEM (2-3) | papel #c3c4c2; recortes (o sujeito `cinza=True` + UM objeto de cor); legenda serifada de 41 px, inteira desde o corte; seta à mão em gancho (traço de 5 px, ponta aberta); **punch-in ×1,8 na palavra-chave** (entra borrado 6 px, foca em 0,2 s); sai borrando. Avisa se a legenda sair do quadro depois do punch |
| (multidão) | COLAGEM (3) | `plano("papel", cam pan ±175 px sine.inOut 1,5 s)` + multidão P&B larga + a personagem pequena EM COR + 3 palavras pequenas espaçadas (ver o exemplo) |
| `documento(t, doc, TXT, idx, chave)` | DOCUMENTO-DIGITA (4) | documento bege apagado; caixa-alta 27 px digitada com cursor durante cada palavra; **punch-in ×2,1** no começo da palavra-chave (ela fica em x≈250); a palavra-chave entra numa SELEÇÃO azul com alças, a ~25 c/s; sai com zoom-out + borrão direcional |
| `objeto_escuro(t, obj, TXT, idx)` | ESCURO-OBJETO (5) | petróleo #061414 com arcos; objeto branco SOBE de baixo (expo 1,6 s); caixa-alta 53 px palavra a palavra (apagada→branca) acima; zoom-out 1,48→1,0; **thump** |
| `arquivo(t, src, ...)` | ARQUIVO (6,7,10,17,18,20) | foto/filme cobrindo a tela; zoom-out padrão 1,35→1,0 (guerra: 2,1, τ 0,25); foto "respira" +10 % em 4 s; `pontos=True` retícula; `legenda=` serifada digitada com queda (a data/o vocativo); `brilho=` estrelas de 4 pontas piscando (joias); `desfoca_fim=0.3` para virar o quadro |
| `palavras(t, [(txt, i), ...])` | PALAVRAS (8, 15) | UMA palavra Hoefler Italic por vez no centro (64 px, cabe em 560); nasce a 0,72× e assenta em 0,3-0,4 s; trocada SECA (fica até a próxima entrar; `vazio=True` devolve o papel vazio na pausa) |
| `diagrama(t, traço, pequeno, grande, idx, doc_src, antena)` | DIAGRAMA (9) | documento apagado afastando 3,2→1,0; o traço entra pela direita e assenta; ondas de cor em leque saindo da "antena"; título em bloco (linha pequena 23 px + grande 60 px) revelado a 0,25 s/palavra; **boom** |
| `cena_cor(t, objeto, rótulo, idx, t_consequencia)` | CENA-COR (11) | degradê azul com retícula e riscos de luz; objeto SOBE; faixa de papel rasgado cresce e as letras acendem salteadas; anéis brancos descem do topo; na consequência o objeto fica VERMELHO, gira 58° e cai |
| `descarte(t, sala, cesto, bola, desenho_src)` | DESCARTE (12) | 0,1 s do desenho chapado no papel; depois sala P&B + cesto de cor; a bola de papel (com o desenho impresso) segura grande e cai rápido no cesto (0,25 s power2.in) e afunda; zoom-out 2,6→1,0 (τ 0,5) |
| `anos_rolando(t, a0, a1)` | ANOS (13) | segura 0,2 s, rola em 0,6 s (sine.inOut); o próximo vem de baixo borrado e apagado, o anterior some rápido |
| `foto(t, src, boom=True)` | FOTO (14) | foto real com push-in 1,0→1,36 (τ 0,33); **boom** na virada do salto |
| `rotulos(t, [(txt, i)])` | ESCURO-RÓTULOS (16) | preto + 6 anéis com pulso; rótulos 285×80 azuis (#1e87b9, retícula, borda clara, sombra deslocada) entram pela direita 0,25 s antes da palavra, em cascata (0/+5/+60 px, degrau 108 px); o grupo anda 30 px à esquerda a cada um; **thump** em cada |
| `quadro(t, conteúdo, moldura, "l1\nl2", idx)` | QUADRO (19) | o retrato vira um quadro dourado no papel: 1º quadro a 3,3× e desfocado, depois 1,29→1,0 (τ 0,6) focando; legenda de 2 linhas embaixo, 0,13 s/palavra |
| `cta_icone(t, fundo, ícone, t_clique)` | ESCURO-ÍCONE (21) | fundo escuro de fitas; ícone + mãozinha que vem e clica (o ícone encolhe 6 %); zoom-out 2,5→1,0 (τ 0,5); **boom** |
| `cta_campo(t, fundo, PALAVRA, t0, t1)` | TELA (22) | fundo borrado entra deslizando da direita; campo vazado (pílula branca 2,4 px) com a palavra digitada e cursor |

**Texto na tela — tamanhos medidos na referência (palco de 720 px). Não diminuir (regra do Felipe, 13/11/2026: mesmo
tamanho e mesma legibilidade da referência).** O texto que acompanha a voz é o mais importante do estilo; se não dá
para ler, é como se não existisse.

| Texto | Corpo | Onde fica |
|---|---|---|
| título digitado em caixa-alta | 60-62 px (maiúscula de 44 px) | centro; cabe em 600 px |
| legenda da colagem | **41 px** (74 px depois do punch ×1,8) | no papel LIMPO ao lado do sujeito, perto da origem do punch; inteira desde o 1º quadro |
| três palavras da multidão | **40 px**, passo de ~170-185 px | linha de base ~21 px acima da cabeça da figura; entram uma a uma |
| caixa-alta do documento | 27 px (maiúscula de 41 px depois do punch ×2,1) | — |
| frase do objeto escuro | 53 px | acima do objeto |
| legenda de arquivo (data, vocativo) | **66-67 px** (~40 % da largura) | sobre área ESCURA da imagem; y até 930 |
| palavra solta | 64 px | centro (360, 640); com logo, o logo vai ACIMA e a palavra continua no centro, no corpo inteiro |
| título em bloco do diagrama | grande **63 px**; pequena **35 px** (0,55 da grande) | pequena colada em cima da grande, ~50 px à direita do início dela |
| papel rasgado | **60 px** numa faixa de ~69 px | a faixa cruza o objeto |
| contador (anos/itens) | **67 px** | centro; em repouso só um item visível |
| rótulo azul | **55 px** (maiúscula de 39 px) | caixa de 285 × 80 (mais larga só se o nome com logo não couber) |
| legenda de 2 linhas do quadro | **53 px**, entrelinha 0,84 | topo do texto ~12 px abaixo da moldura |
| texto do campo do CTA | **38 px** num campo de 442 × 60 | sobre fundo escuro |

- **Nada abaixo de 35 px.** A serifada vai apertada (`TRACK["serifa"] = -0.05`; na referência as letras quase se tocam).
- **A escrita acompanha a voz** (`tempos_revela`): a palavra entra em min(início falado, ritmo proporcional à fala) e nunca
  mais de 0,65 s antes de ser falada. Exceção medida: a legenda da colagem já está inteira no 1º quadro do plano.
- **Nunca mais de ~2,5 s de fala sem nada escrito** (na referência o maior trecho é 2,0 s): num plano de arquivo longo,
  use `legenda=` (o molde `foto` também aceita).
- **Legenda branca precisa de fundo escuro:** com o teto de branco (§7) ela mede ~200 de luminância; sobre cartaz, céu ou
  tela acesa some. Mude o `y` ou escureça a imagem (`filtro="brightness(.75)"`).

**Notícia (não só história):** o mesmo esqueleto serve para notícia — gancho com o fato, contexto (quem processou quem),
feito (o pedido + o argumento), rejeição ("mas calma"), salto (o que muda pra você, com 3 itens nos rótulos), moral
("antes… agora…") e CTA. Exemplo completo: `referencia/cenas-exemplo-noticia-processo-ia.py`.

**Marcas citadas (regra da casa: logo oficial):** `palavras(t, [("Marca", i, ("assets/img/logos/marca.svg", 96)), ...])`
faz o logo + o nome pularem juntos (texto vazio = só o logo, para wordmark); `rotulos(t, [("Marca", i, "logos/marca.svg"), ...])`
põe o logo num disco branco dentro do rótulo azul. Logos: baixe o SVG oficial do site da própria marca para
`assets/img/logos/` (SVG funciona direto). `anos_rolando(t, itens=["hoje", "amanhã"])` rola rótulos
em vez de anos. `documento(..., doc_opac, doc_borrao, doc_escala)` e `diagrama(..., doc_opac, doc_borrao)` deixam o documento
de fundo tão apagado quanto a patente do original (um documento só de texto fica legível demais depois do punch ×2,1).
Citar marca é opcional e é decisão de cada reel: quando o reel não pode ter marca (campanha, publicidade), os mesmos moldes
rodam só com texto, como na referência ("Bluetooth / WiFi / GPS" sem logo). O exemplo de notícia está nessa versão.

Primitivas livres (em `build.py`): `plano`, `img`, `video`, `texto`, `revela`, `pop`, `digita_queda`, `digita_cursor`,
`punch`, `seta`, `aneis`, `ondas`, `rotulo`, `anos`, `rasgado`, `brilhos`, `mao`, `campo`, `anim`, `setar`, `SOM`.
Câmeras: `afasta` / `aproxima` (escala, expo.out com duração 6,93·τ), `pan` (x/y), `degraus` (impulsos somados), `deriva`
(linear), `salto` (1º quadro mais fechado). Saídas: `borrao`, `chicote`, `zoom`.

**Sequência e ritmo — a dinâmica vale para QUALQUER duração (regra do Felipe, 13/11/2026).** A referência tem 22 planos
em 32 s: um corte a cada 1,45 s (mín. 0,67 · mediana 1,45 · máx. 2,70). **Faixa do motor: em média um corte a cada
1,45 a 1,54 s** (1,45 é a referência; 1,54 é o teto aprovado pelo Felipe em 13/11/2026).
Um reel mais longo tem MAIS planos, na mesma proporção (nº de planos entre duração ÷ 1,54 e duração ÷ 1,45: 21 a 22 para
32 s, 29 a 31 para 45 s, 39 a 41 para 60 s); nunca os mesmos 22 planos esticados, e nunca um roteiro encurtado só para
caber em 32 s.
- **Por ato:** planos ≈ duração falada do ato ÷ 1,5 (na referência: gancho 5 · contexto 3 · feito 3 · rejeição 1 · salto 4 ·
  moral 3 · CTA 3).
- **De onde vêm os planos a mais:** a ordem de famílias do original é o esqueleto; os trechos longos são divididos com as
  famílias que a referência repete e sem imagem nova: um ARQUIVO com legenda digitada, uma PALAVRAS de uma ou duas
  palavras, a MESMA imagem em enquadramento mais fechado (`arquivo(..., enquadra=(escala, fx, fy))`, como os planos 17 e
  18 dela), um segundo `titulo_digitado` ou `objeto_escuro`. Duas PALAVRAS seguidas não contam como corte (papel sobre
  papel): intercale outra família. Exemplo de 29 planos em 44,6 s: `referencia/cenas-exemplo-noticia-processo-ia.py`.
- **Continuam valendo:** nunca mais de 2 planos seguidos da mesma família; claro/escuro trocando a cada 1-3 planos.
- **O build confere:** imprime `ritmo: N planos em T s = um corte a cada X s (faixa do motor: 1,45 a 1,54 s -> A a B
  planos)` e, fora da faixa, `AVISO ritmo: faltam ~N cortes` com os planos mais longos. Dentro da faixa, avisa só de
  plano acima de 2,9 s (`AVISO plano longo`). A faixa mora em `medir/metas.json › ritmo › plano_medio_s`.

## 4 · Voz — a VOZ é escolhida pela pessoa no FIM; o motor fixa só ritmo e alinhamento

- Monte com uma voz provisória. Quando a pessoa escolher, `./reel.sh voz <escolhida>` e `./reel.sh montar` refazem todos
  os tempos (cada elemento é amarrado à palavra).
- **Gere a voz com o texto de `narracao/fala-para-voz.txt`**, não com o roteiro cru. `medir/texto.py` escreve esse arquivo
  trocando as siglas e nomes que o gerador lê errado pelo jeito de falar. **As trocas são de cada reel:** ficam em
  `narracao/pronuncia.json` do projeto (lista `"voz"`), nunca no motor, porque cada tema tem as suas. Saiu errada numa
  tomada? Acrescente ali e gere de novo. Na tela continua o texto do roteiro.
- **`./reel.sh voz` põe as pausas na cadência da referência** (`medir/aperta_pausas.py`): os geradores entregam 0,5-0,7 s
  entre frases (21-25 % do tempo em pausa) e a narradora da referência quase não para (5 % do tempo; a maior pausa tem
  0,17 s; média 0,09 s). O passo encurta só o MIOLO de cada pausa (0,14 s em fim de frase, 0,09 s em vírgula, 0,07 s no
  resto); nenhuma sílaba é cortada nem acelerada. `./reel.sh voz arquivo.mp3 crua` pula esse passo.
- **Como escolher a voz:** medir os presets (altura, extensão, agudos) contra a narradora e gerar o roteiro com os mais
  próximos; conferir a fala por transcrição em trechos de ~20 s (a transcrição do arquivo inteiro perde frases) e
  descartar tomada com pronúncia errada.
- **A voz mais curta pede menos planos:** com as pausas apertadas o mesmo roteiro cai uns 5 s; confira a linha `ritmo:`
  do build e ajuste a decupagem para a faixa de 1,45 a 1,54 s.
- O original: **narradora** (f0 ~194 Hz, 10 semitons de extensão — expressiva, de contadora de história), **160
  palavras/min**, pausas curtas (0,14-0,18 s dentro do período, 0,22-0,34 s entre frases). `medir/voz_medir.py` compara.
  A provisória do teste ficou mais lenta (146/min, pausa máx. 0,70 s): o reel durou 38,8 s em vez de ~33.
- Na mixagem a voz recebe compressão suave (o original é bem compacto: LRA 1,9) — nada de corte nem aceleração.

## 5 · Imagens e recortes

- **Arquivo real em domínio público sempre que houver** (o original usa filme real da personagem). Imagem gerada só onde o
  original também usa ilustração (a colagem) — prompts testados em `referencia/prompts.md`.
- **Uma cor por colagem:** sujeito em P&B (`cinza=True`) + um único objeto saturado (livros vermelhos, vestido azul,
  lixeira verde, moldura dourada). Nada de 3D "de argila".
- **Logos oficiais** quando uma marca for citada na fala (regra da casa); print real quando o trecho for educativo.
- Recortes: `medir/recorte.py <entrada> <saída.png> ia|traco|branco|moldura` (moldura vaza a janela e imprime a fração para
  `quadro(janela=...)`).
- Brilhos: passe pontos sobre joias em áreas de meio-tom (branco sobre branco some). No exemplo: reflexos achados por
  top-hat e filtrados por luminância local.
- Reutilizáveis já na base: `moldura.png`, `bola.png`, `lixeira.png`, `icone-ia.png`, `cta-fundo.jpg`.

## 6 · Som

- **Cama:** piano/cordas sustentados, menor, sem bateria, contínua (`referencia/prompts.md`, ElevenLabs Music 45 s).
  Salvar como `assets/trilha.mp3`; o mix corta, faz fade e põe **20 LU abaixo da voz** (`trilha_inicio` no projeto.json
  escolhe o ponto de entrada).
- **Efeitos: só os que a referência tem, presos ao TIPO de plano**. Quem põe o som é o molde, não o `cenas.py`: um reel de qualquer assunto sai com
  os efeitos certos sem ninguém escolher. Fora dos casos da tabela, silêncio de efeito.

  | Efeito | Quando (quem chama) | Como é | Nível × pico da voz |
  |---|---|---|---|
  | `boom` | virada de capítulo: `diagrama`, `foto(boom=True)`, `cta_icone` — três por reel | ruído largo de 10-90 Hz, estéreo aberto; incha 0,5 s ANTES do corte, golpe 0,1 s depois | −4 dB |
  | `thump` | cada rótulo que entra (`rotulos`) | tom fixo de ~49 Hz; pico 0,23 s depois da entrada | −14,5 dB |
  | `objeto` | objeto branco que sobe (`objeto_escuro`) | grave de ~52 Hz com varreduras de 100 a 40 Hz; começa 0,17 s antes do corte | −10,5 dB |
  | `clique` | cada palavra solta que aparece (`palavras`); 2 nas primeiras palavras da legenda do `quadro` | estalo seco de ~4 ms, 2-8 kHz, no quadro exato | −3 dB no 1º plano de palavras, −8 no 2º, −13 no 3º; −11 no quadro |
  | `estalo` | uma vez, no corte que abre o ato `[cta]` (o build acha sozinho) | rajada de ~60 ms | −11,5 dB |
  | `inchaco` | colagem que atravessa em pan (o build acha pelo `cam` com `x1`) | ruído grave que cresce e some 0,35 s antes do corte | −13 dB |
  | `golpe` | entrada e virada do objeto na `cena_cor` | 43 Hz, 80 ms | −16,5 dB |
  | `ar-ondas`, `ar-curto` | ondas do `diagrama`; punch-in da `colagem` e clique da mão no `cta_icone` | sopro agudo só nos lados do estéreo | −26 dB |

  O kit é sintetizado por `medir/sfx_d.py` (sem amostra de terceiros) na forma medida; níveis e instantes ficam em
  `medir/metas.json › audio`. **A referência não tem** som de digitação, whoosh em corte comum nem efeito em plano de arquivo.
- **Mixagem em estéreo:** voz no centro, cama e boom abertos, como na referência. O nível de um efeito estéreo é medido no
  centro (L+R)/2.
- **Trocar o kit é decisão de cada reel**, não do motor: `"sfx": "<pasta>"` no `projeto.json` do reel aponta outra pasta
  com os mesmos nomes de arquivo e um `pre.json`.
- **Final −14 LUFS, LRA ~2, true-peak −1 dB** (ganho FIXO + limitador depois do ganho, conferindo o LUFS e o pico
  verdadeiro do AAC final). O original: −14,2 LUFS, LRA 1,9.
- **A cama vai em nível cheio até o último quadro:** o mix descarta o fade-out embutido da faixa e avisa quando ela é mais
  curta que o reel (aí emenda em laço para dentro do corpo da música). Prefira faixa com a duração do reel + 10 s, sem fade.

## 7 · A pele da fita (`pelicula.py`)

Conteúdo renderizado a **10 fps** (cada quadro 3× a 30 fps). Por cima, a cada **1/6 s**: linhas de varredura (período
5,4 px, 12,3 % de profundidade, normalizadas para não escurecer a média) com a fase pulando; tremulação de brilho ±1,5 %;
grão fino; poeira e manchas verticais só nos escuros. Sempre: separação RGB (vermelho −1,5 px, azul +1,5 px) e maciez
0,6 px. Sobe para 1080×1920. Conferido contra o original: linhas 24,7 × 23,2 níveis pico a pico, grão 1,36 × 1,40, papel
189 × 193.

**Teto de branco:** na referência nenhum branco passa do branco do papel (99,9 % do vídeo abaixo de 209; texto branco
~190-200). A película comprime tudo acima de 190 até o teto 197 antes das linhas (medido depois: p99,9 = 214 contra 213 do
original). Consequência: legenda branca precisa de fundo escuro — sobre cartaz ou tela acesa ela some.
**Cor:** a saída é convertida e MARCADA em BT.709 (matriz, primárias e curva). Sem isso o ffmpeg grava em BT.601 sem
etiqueta e os players leem como 709: o vermelho e o verde mudam.

## 8 · Checagens

| Checagem | Ferramenta | Passa quando |
|---|---|---|
| Fala completa | `./reel.sh conferir-fala` | todas as frases presentes |
| Lint | `./reel.sh checar` | 0 erros |
| Quadro seguro | aviso no build (`AVISO quadro seguro`) + folhas | nenhum aviso; nada cortado/encostado nas folhas |
| Ritmo | aviso no build (`AVISO ritmo`, `AVISO plano longo`) | em média um corte a cada 1,45 a 1,54 s, em qualquer duração; nenhum plano acima de 2,9 s |
| Digitação | aviso no build (`AVISO digitação cortada`) | nenhum aviso: todo texto digitado termina e fica nítido antes do corte |
| Movimento | `pericia-movimento.py --contra` (no `montar`) | amplitude ≥ 3,0× · quase-parada ≥ 25 % · ≥ 8 picos. **Só tem piso:** um reel parado demais (58 % de quase-parada contra 29 %) também passa; quem pega isso é o portão de ritmo |
| Áudio | `mix.py` | −14 LUFS, LRA ~2 |
| Olho | `renders/<nome>-folha-0*.jpg` | recortes limpos, uma cor por colagem, imagens com cara de arquivo, brilhos visíveis |

Resultados: **recriação** 4,4× / 31 % / 8 picos (original 4,3× / 29 % / 12) — APROVADA. **Teste Ada Lovelace** 9,6× /
49 % / 9 — APROVADO (mais parado que o original por causa da voz provisória lenta e de fotos no lugar de filme; com a voz
definitiva e arquivo em vídeo `arquivo(src=".mp4")` fica mais perto).

## 9 · Armadilhas já vividas

- **Tween longo com `onUpdate` começando em 0 não é chamado no render** (brilhos e pulso sumiram): o build expande esses
  efeitos em tweens explícitos dentro da janela do plano. Animação nova: use `anim`/`setar`, não `onUpdate` de 0 a DUR.
- **Vídeo dentro de elemento com `data-start` é proibido** no HyperFrames: os planos NÃO são `.clip`; a visibilidade é
  `display` no timeline.
- **O fundo encolhia com o zoom-out** (bordas pretas): o fundo do plano fica FORA da câmera.
- **Legenda saindo do quadro depois do punch-in:** ponha a legenda perto do ponto de origem do punch (o build avisa).
- **Duas letras caindo juntas** na digitação: só a última letra de cada passo de 10 fps cai.
- **Letras fora de ordem** quando a digitação a c/s fixo atravessava a palavra seguinte: as palavras entram em sequência.
- **Corpo do documento:** a altura medida (12 px) estava errada por causa do borrão; o certo saiu da LARGURA (27 px).
- **Grão e poeira demais deixavam o filme "mexendo" parado** (quase-parada caía): grão 1,25× e manchas 2,5 (medidos).
- **A multiplicação das linhas escurecia o papel 6 %:** as linhas são normalizadas pela média.
- **Mix a −15 LUFS** com voz dinâmica: compressão suave na voz + normalização em duas passadas.
- **A faixa de papel rasgado aparecia inteira antes da hora** (o recorte só valia depois do tween começar): agora nasce
  recortada no tempo 0.
- **Digitação cortada pelo corte seguinte** (o título parava duas letras antes do fim): o motor agora comprime a
  digitação para a última letra entrar antes do fim nítido do plano (0,2 s na digitação com queda, 0,3 s na com cursor; o
  punch e a seleção do `documento` acompanham) e imprime `AVISO digitação cortada` quando não cabe.
- **Saída curta não aparece no vídeo:** um tween de 0,1-0,2 s a 10 fps só é amostrado no começo (valor zero) — o "sair
  borrando" nunca renderizava. As saídas (`borrao`, `chicote`, `zoom`) e a entrada desfocada (`plano(entrada=...)`) são
  gravadas quadro a quadro com `setar`. Regra: animação menor que 0,3 s = um `setar` por passo, nunca tween.
- **Filtro dentro de punch-in:** `blur()` vale em px locais; depois de um punch ×1,8 aparece 1,8× maior. O build divide
  pela escala do punch.
- **Chicote forte demais** (14 px e −70 px viravam uma barra ilegível): o medido é ~3 px só na horizontal e −27 px.
- **`clip-path` animado sobrescreve o `clip-path` do desenho** (o papel rasgado saía como retângulo reto): o recorte
  animado vai num invólucro e a borda rasgada fica no miolo.
- **`transform-origin` do CSS não vale para `<circle>` no GSAP** (o pulso dos anéis saía andando na diagonal): `svgOrigin`.
- **`&nbsp;` no Hoefler tem metade da largura do espaço** (as legendas digitadas saíam coladas): as letras usam espaço comum
  com `white-space:pre`.
- **`palavras()` deixava o papel vazio a pausa inteira** (1,3 s de buracos num plano): troca seca por padrão.
- **`loudnorm linear=true` cai no modo dinâmico** quando o pico passaria do teto (os booms saíam com níveis diferentes):
  ganho fixo + limitador.
- **Trilha com fade-out embutido:** a cama sumia no CTA e o laço colava o começo da música no último segundo.
- **Cauda final de 0,6 s:** a referência acaba 0,17 s depois da última palavra; agora `CAUDA = 0.2` (`build.py` e `mix.py`).
- **`-shortest` com áudio copiado cortava o último quadro:** a película fecha pela duração do vídeo (`-t`).

## 10 · Arquivos

`base/`: `build.py` (primitivas + HTML), `moldes.py` (os 15 moldes), `cenas.py` (modelo), `pelicula.py` (a pele da fita),
`mix.py`, `reel.sh`, `assets/` (fontes, efeitos, recortes reutilizáveis), `medir/` (texto, alinhar, indices, voz_medir,
sfx_d, recorte, folha_video, metas.json). `~/.claude/skills/reels-sem-aparecer/motores/documentario/referencia/`: `cenas-exemplo-ada-lovelace.py` + `fala-exemplo-…txt` (um reel
completo do motor), `camera-original.json` (o movimento de câmera da referência, plano a plano, só números),
`pronuncia-exemplo-*.json` e `prompts.md`.
