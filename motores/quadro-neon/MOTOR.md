# Motor QUADRO NEON ("o quadro-negro neon que explica") — o estilo C

*Motor da skill `reels-sem-aparecer`. Criado em 13/11/2026 a partir de um reel de referência de 41,4 s, validado por uma
recriação fiel (passou no teste de movimento) e por um reel do zero ("Ninguém compra IA", 43,7 s). O vídeo de referência
não acompanha a skill; as medidas dele, sim. Neste manual, "C" é este motor.*

> **Como ler este manual.** “O Felipe” é o Felipe Borges, que criou e validou este motor; cada reprovação dele registrada
> aqui virou regra e vale para qualquer pessoa. O que é escolha de cada reel (tema, texto, voz, trilha, imagens) é de quem
> está fazendo o reel. Os comandos partem da pasta do projeto criado pelo `novo-reel.sh`; os arquivos de `referencia/`
> ficam em `~/.claude/skills/reels-sem-aparecer/motores/<motor>/referencia/`.

> **Motor independente.** Não usa, não lê e não altera nada dos motores A (editorial) e B
> (dentro do mundo). Scripts, metas, fontes, trilha e regras do C vivem só aqui. Nunca misturar estilos no mesmo reel.

**O estilo em uma frase:** fundo preto com malha fina e neon amarelo explicando UMA tese em 4 atos (frase contrária →
explicação com ícone → prova por repetição com 5 marcas reais no mesmo molde → síntese em lista → CTA palavra a palavra),
sobre uma trilha melódica de ~101 bpm que faz DROP no 1º exemplo e PARA na síntese. Sem câmera: tudo entra e fica.

> **Rodada 2 (13/11, depois do "ficou simplório" do Felipe):** a 1ª versão copiava os quadros parados mas não o que
> acontece ENTRE eles. Corrigido e medido: (1) a malha de linhas ROLA para baixo a 30 px/s em ponte, tese, reframe e
> síntese; (2) nos cartões e no CTA as cruzes do fundo piscam rápido e independentes (é o que deixa a tela viva);
> (3) o flash é LUZ DE FILME EM VÍDEO (`assets/luz.mp4`), não um degradê; (4) há DESENHO SONORO em quase toda entrada
> (whoosh em cada cartão e flash, brilho no ícone/objeto, impacto no drop, risco na seta/arco, sopro nos textos grandes);
> (5) o 2º herói sobe forte e o brilho "acende" depois; (6) a imagem do gancho deriva devagar; (7) imagens fotográficas.
> Total de tela 100 % parada: 65 % na v1 -> 35 % na v2 (original 29 %).

**Regra-mãe:** do original copiamos estrutura, ritmo, som, tipografia e física. Tema, frases e exemplos são de quem faz o reel.
Tudo aqui foi medido (folhas a 2/10/30 fps, demucs, legendas do original lidas quadro a quadro) e validado pela
recriação. Não mudar número sem medir de novo.

---

## 1 · Pipeline

```bash
zsh ~/.claude/skills/reels-sem-aparecer/ferramentas/novo-reel.sh quadro-neon <pasta-do-reel> fala.txt "Título do reel"   # cria o projeto (copia base/, lê o roteiro)
cd <pasta-do-reel>
./reel.sh marca ifood.com.br ifood                         # print REAL do site + logo OFICIAL (uma vez por marca)
# imagens do gancho e do reframe (Higgsfield, §5) em assets/img/ · trilha em assets/trilha.mp3 (§6) · preencher cenas.py
./reel.sh voz narracao-provisoria.mp3                      # voz PROVISÓRIA, só para os tempos (§4)
./reel.sh conferir-fala                                    # nenhuma frase sumiu
./reel.sh quadros 1.4 6 10 14 30 40                        # PNGs rápidos em renders/q-*.png, sem renderizar
./reel.sh montar                                           # auditoria -> trilha arranjada -> mixagem -> render -> movimento -> folha
# NO FIM: a pessoa escolhe a voz -> ./reel.sh voz escolhida.mp3 && ./reel.sh montar (todos os tempos se refazem)
```
Olhar `renders/<nome>-folha-0*.jpg` antes de entregar (print com banner/cookies, logo errado, localização aparecendo,
imagem com cara de brinquedo: o automático não pega).

Ambiente: tudo vem do `instalar.sh` da skill (Python próprio com demucs, librosa, rembg e o alinhador em português; HyperFrames na versão validada; `ffmpeg` e `rubberband`). O `reel.sh` de cada projeto já usa esse ambiente sozinho. Para conferir a máquina: `zsh ~/.claude/skills/reels-sem-aparecer/ferramentas/diagnostico.sh`. Este motor usa o Google Chrome para os prints das marcas e para a auditoria.

## 2 · Roteiro (esqueleto medido) — `fala.txt` marcado por ATO

```
[gancho] Ninguém compra IA.                                   ← 3-4 palavras, contra uma crença; vira o título gigante
[ponte] Deixa eu te explicar.                                 ← 3-5 palavras
[tese] IA não é o motivo de alguém te contratar, é só a ferramenta.     ← a ÚLTIMA palavra vira "<manuscrita>"
[reframe] O que faz alguém pagar é o resultado, e ele define quanto você cobra.   ← 2 palavras-herói (causa -> efeito)
[prova] O iFood não vende comida, vende tempo livre.          ← 4-5 linhas, TODAS "<Marca> não vende X, vende Y."
O Nubank não vende cartão, vende controle.
...
[sintese] É por isso que ninguém compra IA.                   ← vira a tarja amarela (texto da tarja no cenas.py)
[lista] Seu cliente compra uma tarde livre, um cliente a mais, menos retrabalho, uma noite de sono, um negócio que cresce.
[cta] Quer vender IA sem falar de IA? Me segue e comenta IA que eu te mostro como.   ← palavra-código = a do gancho
```
- **Tamanho:** ~105-120 palavras = ~40-45 s. `texto.py` mostra palavras por ato contra o original.
- **Prova:** a vírgula separa as metades; a 2ª metade começa com o verbo ("vende") e termina na palavra-payoff, que fica
  amarela. Mesma frase, mesma cadência nas 5 (é o refrão que prende). Marcas que o público do reel reconhece de olho.
- **Lista:** itens de 1-4 palavras separados por vírgula; as N primeiras palavras (padrão 3) viram o `>prompt`.
- **CTA:** a palavra depois de "comenta/comente/digita" ganha aspas na tela. Use a palavra do gancho (fecha o loop).
- Pronúncia de marca nova: dicionário `PRON` em `medir/texto.py` (só para o alinhamento).

## 3 · Os moldes (`base/moldes.py`) — o que cada ato vira, com os números medidos

| Ato | Tela | Tempo (amarrado à fala) |
|---|---|---|
| gancho | colagem P&B entra pela direita (760 px de altura, some no preto embaixo); título neon gigante empilhado à esquerda, 1 palavra por linha, Anton estreitada ×0,64; objeto colorido sobe no fim do título | palavra +0,12 s, entra deslizando da esquerda em 0,16 s |
| (fundo) | malha fina 30,5 px; **rola para baixo a 30 px/s** em ponte, tese, reframe e síntese; nos cartões e no CTA fica parada e as cruzes (a cada 61 px, ~55 %) **piscam rápido** (5-11 rad/s) | contínuo |
| ponte | **flash de luz**; frase em 2 linhas, letras chegam espaçadas e fecham (0,32 s) | flash 0,28 s depois do começo da ponte |
| tese | ícone de linha neon (Lucide, composto) no centro; legenda de 1 palavra (Montserrat 600, 30 px, y 735); no fim o ícone cresce ×1,4, a seta à mão com laço se desenha e a última palavra vira `<manuscrita>` (Gochi Hand, colchetes amarelos) | legenda NA palavra (±1 quadro); seta 0,49 s antes da última palavra |
| reframe | HERÓI A amarelo (y 205) cresce do apagado; foto recortada (pop); HERÓI B branco com brilho amarelo (y 680) sobe; arco tracejado A→B; depois a tela fica parada | A no começo da frase; legenda até o B; B na palavra −0,08; arco +0,13 |
| prova ×N | **cartão de marca**: logo oficial no círculo + nome (Anton) + régua; print real sobe com borrão (0,55 s); linha 1 digitada COM a fala (layout final reservado); linha 2 "VENDE **PAYOFF**" | 1º cartão com flash (= drop); os outros cortam na pausa 0,06 s antes do nome; linha 2 no começo da 2ª metade |
| sintese | **flash**; malha larga sem estrelas; tarja amarela sobe e acende | flash no começo da frase (= break da trilha) |
| lista | `>prompt` (o ">" amarelo, Montserrat 400); embaixo 1 item amarelo por vez | item entra NA palavra e SOME na pausa (tela vazia entre itens) |
| cta | **flash**; malha vazia; 1 palavra por vez em caixa alta (Montserrat 600, 36 px, centro) | na palavra; tela vazia nas pausas reais |

Tamanhos são calculados pela largura REAL do texto (`cabe()`): nada cortado, nada na coluna dos botões do Instagram.

## 4 · Voz — a VOZ é escolhida pela pessoa no FIM; o motor fixa só o TOM e a CADÊNCIA

**Regra (Felipe, 13/11):** o motor não escolhe voz. Monte com uma voz provisória qualquer (só para os tempos); no fim,
gere as candidatas que a pessoa quiser ouvir, ela escolhe, e `./reel.sh voz <escolhida>` + `./reel.sh montar` refazem
tudo (cada elemento é amarrado à palavra, nada é tempo fixo).

> **Decisão de 13/11 (Felipe): a voz entra CRUA.** O tratamento abaixo recortava a fala em pedaços, acelerava cada um
> num ritmo diferente e colava com silêncio absoluto: a voz ficou "picada, não fluida" (73 emendas bruscas contra 21 na
> crua). Agora `./reel.sh voz` só tira o silêncio das pontas e alinha. O tratamento ficou como opção (`TRATAR=1`), não
> recomendada; se um dia voltar, terá de ser sem recortar a fala (um ajuste de velocidade único e pausas encurtadas com
> transição suave) e passar num teste de fluidez (emendas bruscas da tratada ≤ da crua).

O que o tratamento opcional (`TRATAR=1 ./reel.sh voz ...`) aplica (medido no narrador do original):

| O quê | Original | Como aplicamos |
|---|---|---|
| Tom | f0 ~75 Hz, **plano** (entonação 1,9 semitom) | `tom_c.py`: Praat/PSOLA, melodia ×0,42 e −6 semitons, formantes intactos (`SEMI=-5 FATOR=0.5 ./reel.sh voz ...` para suavizar) |
| Velocidade | 167/min no total | `ritmo_voz.py` por ato: gancho 200 · ponte 200 · tese 218 · reframe 192 · **prova 162** · síntese 210 · **lista 158** · **pergunta do CTA 280** · ordem do CTA 210 |
| Pausas | **curtas e iguais** (~0,25 s): é o metrônomo do C | ponto 0,27 · vírgula da prova 0,26 · vírgula da lista 0,22 · pergunta→ordem 0,17 · vírgula na tese/reframe/CTA não pausa |
| Contorno | frase afirma e cai no fim; payoff na última posição | escrever a palavra-payoff no fim da frase |

Metas (`medir/metas.json`, `voz_medir.py`): 150-180 palavras/min · pausa média 0,18-0,34 s · máx. 0,25-0,50 s ·
entonação ≤ 2,8 st · ênfase ≥ 2,4 dB. Teste de 13/11 (voz provisória): 159/min, pausa 0,25 s, entonação 2,15 st, 89 Hz.

## 4.5 · Luz de filme (o flash)

`assets/luz.mp4` (+ `luz.json`): luz de filme gerada no Higgsfield (`seedance_2_5`, 9:16, 4 s, prompt em
`referencia/prompt-luz.txt`), retemporizada com ffmpeg em 3 velocidades para caber em 0,23 s como no original
(âmbar entra → branco no corte → recua com reflexo). Entra em `screen` por cima de tudo, 0,12 s antes do corte, com
brilho ×1,35. Sem o arquivo, o build cai no vazamento desenhado em CSS (pior; só reserva).

## 5 · Imagens

- **Gancho:** obra clássica ou estátua "atualizada" (óculos escuros, fone, celular), P&B, sobre fundo preto liso —
  `gpt_image_2_6`, 3:4. Recorte: rembg + chave de luminância, convertida para P&B.
  Nunca a mesma obra do reel de referência (lá era a Mona Lisa).
- **Objeto do gancho e foto do reframe:** objeto FOTOGRÁFICO isolado em branco (`gpt_image_2_6`, 1:1), recortado com rembg,
  ligado ao verbo do gancho (comprar → cartão dourado) e ao herói do reframe (resultado → troféu). Nada de 3D "de argila"
  nem de robô de brinquedo (reprovado na rodada 1) e nada escuro sobre o fundo preto (some).
- **Punch no começo (rodada 3):** o gancho aceita vários objetos, cada um amarrado a uma palavra do título
  (`gancho_objeto: [(src, largura, "compra"), (src, largura, "ia")]`): o 1º sobe por baixo do título, os outros pipocam
  à direita da linha da palavra (com brilho). A ponte aceita uma foto (`ponte_foto: (src, largura)`) que pipoca embaixo
  da frase logo depois do flash. Exemplo: cartão dourado em "compra", chip em "IA", lâmpada acesa em "deixa eu te explicar".
- **Fotos da lista (`lista_imgs`, pedido do Felipe na rodada 2 — "dá mais dinâmica"):** uma foto recortada por item da
  [lista], no estilo dos relógios do original (produto fotográfico, colorido, ângulo dinâmico, sombra suave). Entra com o
  item (pop + brilho) embaixo do texto (y 600, 300 px) e sai com ele. Prompt que funcionou (`gpt_image_2_6`, 1:1, em lote):
  "Photorealistic <objeto que materializa o item>, dynamic three-quarter angle, crisp studio product photography, soft
  shadow, isolated on a pure white seamless background, no text, no logos" -> rembg. Exemplo: tarde livre = espreguiçadeira,
  cliente a mais = aperto de mão, menos retrabalho = papel amassado, noite de sono = travesseiro com máscara, negócio que
  cresce = planta nascendo de moedas.
- **Marcas:** `./reel.sh marca <site> <slug>` (print real 1440×810 + logo oficial do próprio site). Conferir no olho:
  verificação anti-robô (não contornar: usar a página institucional), "navegador não suportado" (usar o site "about"),
  banner de cookies (o script clica em "somente o necessário"; se sobrar, refazer) e **a localização de quem está rodando** (Uber e
  Airbnb mostram a cidade da conexão: tapar/recortar antes de usar).

## 6 · Trilha e som

- **Trilha:** gerar no Higgsfield `elevenlabs_music_v2_5`, 70 s, `force_instrumental`, com o prompt de
  `referencia/prompt-trilha.txt` (melodic future bass ~101 bpm, F# menor, teclas/sinos, 808, sidechain, intro sem
  bateria e drop). Salvar como `assets/trilha.mp3`. O `trilha_c.py` separa em stems (cache `assets/trilha-stems/`),
  acha o drop da faixa (1º ataque no nível do groove) e a toca contínua com deslocamento que põe esse drop no 1º exemplo.
  Arranjo pelos eventos dos moldes: **intro sem bumbo → grave some 2,6 s antes do drop → riser (o build da própria
  faixa, 1,3 s) → DROP no 1º exemplo → BREAK na síntese (bumbo sai, grave a 25 %) → VOLTA no 1º item da lista, no
  tempo forte → groove até o fim** (repete em blocos se faltar).
- **Nível:** trilha **5,2 LU abaixo da voz** (cama presente; o A fica a 23 dB, o B a 11,5). Final −17,6 LUFS (o do
  original; para o Instagram pode ir a −14 em `metas.json` sem mudar o resto).
- **Efeitos (corrigido na rodada 2 — a 1ª perícia errou ao dizer "quase não há"):** medidos no resíduo do original
  (trilha subtraída compasso a compasso) e sintetizados no mesmo formato por `medir/sfx_c.py`:

  | Efeito | Onde (os moldes já marcam) | Forma | Nível |
  |---|---|---|---|
  | whoosh | toda troca de cartão, os 4 flashes, o 2º herói | médios (~600 Hz), incha 0,30 s, pico 0,07 s depois do corte | −3 dB |
  | brilho | ícone da tese, objeto do gancho, foto do reframe, palavra manuscrita | cintilação 3-9 kHz, 0,45 s | −7 dB |
  | impacto | o drop (1º cartão) | sub que despenca + prato | −1 dB |
  | risco | seta e arco se desenhando | caneta granulada 2-6 kHz | −13 dB |
  | sopro | título do gancho, herói A, tarja, prompt, itens | whoosh curto e agudo | −9 dB |

  Conferido: na faixa de cada um, sobem 3-13 dB sobre a trilha (original 2,6-9 dB). Candidatos gerados no Mirelo ficam em
  `referencia/sfx-mirelo-candidatos/` para teste no ouvido.

## 7 · Checagens

| Checagem | Ferramenta | Passa quando |
|---|---|---|
| Voz | `./reel.sh voz` | VOZ: APROVADA |
| Fala completa | `./reel.sh conferir-fala` | todas as frases presentes |
| Quadro seguro | `./reel.sh checar` (`auditoria.mjs` a 30 fps) | AUDITORIA: APROVADA (nada cortado, coberto, encostado, rente ou na coluna do Instagram com a tela parada) |
| Movimento | `pericia-movimento.py --contra` (no montar) | amplitude ≥ 67,5× · quase-parada ≥ 73 % · ≥ 2 picos |
| Olho | `renders/<nome>-folha-0*.jpg` | prints limpos, logos certos, nenhuma localização, imagens fotográficas |

## 8 · Armadilhas já vividas

- **Whisper adianta as palavras** ~0,3-0,5 s no inglês da referência: os tempos da recriação vieram das legendas do
  original, lidas quadro a quadro. No PT o motor usa o alinhamento forçado (wav2vec2), que é exato.
- **A legenda e o herói não podem encostar**: o original deixa "drives" por cima de PURCHASES; aqui a legenda some antes.
- **Payoff longo** ("VENDE PERTENCIMENTO") invadia a coluna do Instagram: a linha 2 encolhe até 430 px.
- **Gancho com 3 palavras** deixava imagem pequena e objeto solto: imagem com 760 px de altura e objeto colado no título.
- **Drop da trilha**: a maior subida de energia caía num fill no meio do groove; o certo é o 1º ataque no nível do groove.
- **Prints de sites**: verificação anti-robô (iFood), navegador não suportado (Netflix) e cidade do usuário (Uber, Airbnb).

## 9 · Arquivos

`base/`: `build.py` (palco 576×1024 = o do original, HTML + GSAP para HyperFrames; fundo de malha com estrelas,
vazamento de luz, primitivas), `moldes.py` (os atos), `cenas.py` (modelo de configuração), `mix.py`, `reel.sh`,
`assets/` (fontes Anton, Montserrat, Gochi Hand; ícones Lucide, licença ISC; efeito), `medir/` (texto, alinhar_ctc,
tom_c, tom, ritmo_voz, voz_medir, trilha_c, sfx_c, marca, quadros, pares, auditoria, folha, metas.json e as fontes TTF de
medida). `~/.claude/skills/reels-sem-aparecer/motores/quadro-neon/referencia/`: `cenas-exemplo-ninguem-compra-ia.py` + `fala-exemplo-…txt`
(um reel completo do motor), a versão `-sem-marcas` do mesmo reel, `prompt-trilha.txt`, `prompt-luz.txt` e os candidatos de efeito.
