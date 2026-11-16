# Motor DENTRO DO MUNDO ("o texto mora dentro do mundo") — o estilo B

*Motor da skill `reels-sem-aparecer`. Criado em 12/11/2026 a partir de um reel de referência de 37,0 s e validado por uma
recriação fiel. O vídeo de referência não acompanha a skill; as medidas dele, sim. Neste manual, "B" é este motor.*

> **Como ler este manual.** “O Felipe” é o Felipe Borges, que criou e validou este motor; cada reprovação dele registrada
> aqui virou regra e vale para qualquer pessoa. O que é escolha de cada reel (tema, texto, voz, trilha, imagens) é de quem
> está fazendo o reel. Os comandos partem da pasta do projeto criado pelo `novo-reel.sh`; os arquivos de `referencia/`
> ficam em `~/.claude/skills/reels-sem-aparecer/motores/<motor>/referencia/`.

> **Motor independente.** Não usa, não lê e não altera nada do motor A (o editorial, a "página que se
> escreve sozinha"). Scripts, metas, efeitos, fontes, voz e regras do B vivem só aqui. Se um número coincidir com o A, é
> coincidência medida. Nunca misturar os dois no mesmo reel.

**O estilo em uma frase:** cada frase acontece num MUNDO diferente (foto de mesa vista de cima, quadro-negro, celular
antigo, tela de app, papel cinza) e a palavra aparece DENTRO desse mundo (escrita, digitada, impressa num chip), com a
câmera sempre andando; o mundo troca por corte seco junto da 1ª palavra da frase seguinte. A maioria dos cortes é seca
(só a nota da trilha muda); efeito de virada só nas viradas da história e nos movimentos rápidos.

**Regra-mãe:** do original copiamos método, ritmo, som e física; nunca o conteúdo (tema, frases, fotos, marcas, UIs reais).
Tudo aqui foi **medido** (perícia de movimento, demucs, alinhamento forçado, leitura a 5 e 30 fps) e **validado** pela
recriação. Não mudar número sem medir de novo.

---

## 1 · Pipeline (a ordem importa)

```bash
bash ~/.claude/skills/reels-sem-aparecer/ferramentas/novo-reel.sh dentro-do-mundo <pasta-do-reel> fala.txt "Título do reel"   # cria o projeto (copia base/, lê o roteiro)
# gerar a voz em PT-BR (§3) e as imagens (§6)
cd <pasta-do-reel>
./reel.sh voz narracao.mp3    # alinha a voz crua -> tom e cadência do B frase a frase -> realinha -> mede
./reel.sh conferir-fala       # transcrição por trechos: nenhuma frase sumiu
# escrever cenas.py (§4, §5); SOM() e TRILHA() dentro das cenas (§7); trilha em assets/trilha.mp3
./reel.sh provar 12.3 nada queda whoosh outro.wav   # (depois do 1º montar) testa no ouvido os efeitos de cada parte
./reel.sh checar              # build -> cadência dos mundos; corrigir até APROVADA
./reel.sh montar              # mixagem -> render -> cópia leve -> teste de movimento -> folha de quadros
```
Olhar `renders/<nome>-folha.jpg` (meio e fim de cada mundo) antes de entregar: texto fora da superfície, palavra cortada,
logo de terceiros, imagem com cara de brinquedo — nada disso a checagem automática pega.

Ambiente: tudo vem do `instalar.sh` da skill (Python próprio com demucs, librosa, rembg e o alinhador em português; HyperFrames na versão validada; `ffmpeg` e `rubberband`). O `reel.sh` de cada projeto já usa esse ambiente sozinho. Para conferir a máquina: `bash ~/.claude/skills/reels-sem-aparecer/ferramentas/diagnostico.sh`.

## 2 · Roteiro (esqueleto medido)

- **Tamanho:** ~95-110 palavras = ~32-37 s (183 palavras/min no total). `texto.py` informa a duração prevista.
- **Esqueleto:** autoridade/previsão na 1ª palavra → a tese ("o futuro de X vai ser Y") → confirmação curta (soco de 1 s)
  → contraste ("não é A, é B") → consequência para você → dado surpreendente ("e aqui vai algo curioso: mais de N %…")
  → "não porque X, mas porque Y" → diagnóstico ("se você só…, está…") → virada/promessa ("mas se você…") → **CTA de
  comentário com palavra-código** ("comenta X que eu te mando"), digitado numa tela.
- **Uma ideia por frase**; frases de 3 a 12 palavras. Cada frase vira um mundo, então a pontuação É a montagem.
- **Marque com `»`** no começo a frase-chave (a tese e o fecho; 1 ou 2 por reel): ela é falada mais devagar.
- Linha em branco = fim de parágrafo = pausa maior.
- Marcas: só as do próprio tema (Claude, Claude Code). Pronúncia nova vai no dicionário `PRON` de `medir/texto.py`.

## 3 · Voz: o TOM e a CADÊNCIA do B (a voz em si é gerada depois, em PT-BR)

Medido no narrador do original, frase a frase:

| O quê | Original | Como aplicamos |
|---|---|---|
| Velocidade total | **183 palavras/min** (88 % do tempo falando) | resultado do ritmo abaixo |
| Velocidade DENTRO da frase | ~214/min (mediana 210) | `ritmo_voz.py`: 230/min em PT (palavra mais longa) |
| Frase-chave (tese, fecho) | ~160/min | marcada com `»`: 175/min em PT |
| Soco curto (≤ 4 palavras) | 265-320/min | 280/min |
| Pausa depois de ponto | média 0,39 s (0,10-0,92) | 0,34 s |
| Pausa depois de vírgula | média 0,31 s (0,08-0,60) | 0,20 s (vírgula após 1-2 palavras não pausa) |
| Pausa depois do gancho | 0,92 s (a maior do vídeo) | 0,62 s |
| Pausa de fim de parágrafo | 0,54-0,62 s | 0,50 s |
| Tom (f0) | **94 Hz**, grave | escolher voz grave (abaixo) |
| Entonação | 3,56 semitons (contida) | meta ≤ 4,6 |
| Ênfase | 3,29 dB | meta ≥ 2,8 |
| **Contorno** | toda frase **começa alta** (+4 a +11 st) e **termina caindo** (−2 a −7 st no ponto); a 1ª palavra é a mais forte | escrever frases afirmativas, começando pela palavra de peso ("Hoje,", "Mas", "Nenhum", número) e terminando em ponto |

**O mundo troca na pausa:** 7 dos 13 cortes caem dentro da pausa entre frases, e todos ficam 0-0,25 s antes da 1ª
palavra da frase nova. Por isso a pausa entre frases não pode sumir (é diferente do A, que corta todos os respiros).

**Gerar:** Higgsfield `generate_audio`, modelo `elevenlabs_v4`, `stability: 0.75`, um `dialogue` com a fala inteira
(parágrafos separados por linha em branco; o `»` sai do texto enviado à voz). Voz padrão do B: **Sterling**
(`dc382508-c8bd-443c-8cb2-46e57b8d2e6f`); alternativa: **Desmond** (`563f728c-e249-5a85-97ab-8461e8c09da6`).
Por quê: das 34 vozes masculinas medidas pela prévia, as mais próximas do narrador eram Fraser, Sterling, Brooks e
Desmond; testadas em PT, todas sobem o tom (117-129 Hz) e a Sterling ficou mais perto no conjunto
(117 Hz, entonação 4,34 st, ênfase 4,0 dB). Com a cadência do B aplicada ela passou nas metas
(177/min, pausa média 0,47 s, máx. 0,67 s, contorno 4/4).
**A voz é escolhida por reel** (pedido do Felipe, 12/11): testar as vozes do B e também as do A (Alden, Andre…), porque o
que é do B é a cadência e o tom, não a voz. No reel de exemplo (“Conversa parada”) venceu a **Andre**
(`f1e8226e-2248-4d5f-b43c-0a79e9949dbf`) com `stability: 0.5`, e depois do `./reel.sh voz` passou por
`medir/tom.py` (−2 semitons com formantes preservados + EQ e compressão de locução medidos no narrador) e
`medir/acento.py` (±1,5 dB do começo ao fim da frase, para a ênfase voltar acima de 2,8 dB). As duas são opcionais.

**Metas** (`medir/metas.json`, checadas por `voz_medir.py`): 172-194 palavras/min · pausa máx. 0,45-0,80 s · pausa
média 0,30-0,50 s · entonação ≤ 4,6 st · ênfase ≥ 2,8 dB. O "% falando" é só informativo (a voz do original tem
respiração nas pausas; o TTS tem silêncio absoluto).

## 4 · Mundos: as três famílias e os moldes

Espaço 720×1280 (palco ×1,5). Uma frase = um mundo. Rodízio de famílias, nunca a mesma duas vezes seguidas.

| Família | Formato | Quando | Como a palavra aparece | Primitivas |
|---|---|---|---|---|
| **Foto-mundo** | 9:16 cheio | gancho, tese, contraste, "jogo"/metáfora | numa SUPERFÍCIE da foto: papel, quadro, tela de aparelho, chip na mesa | `foto`, `texto(..., quad=)`, `digita(..., quad=)`, `chip`, `onda`, `risco`, `img` (objeto em 1º plano) |
| **Tela de app** | **faixa 1:1** (720×710, barras pretas de 285 px) | dado, conversa, lista, post, busca | conteúdo da interface: balão, linha da lista, campo digitado | `conversa`+`balao`+`digitando`, `ranking`, `composer`, `busca`, `pilula_progresso`, `pilula_no` |
| **Papel** | 9:16, liso `#e6e6e4` ou preto | respiro curto (1-1,5 s), número, conclusão | `assenta`: pequena (30-44 px), entra clara/abaixo e assenta; linha se recentra | `assenta`, `borda_filme`, `img` (globo, cone) |

Moldes medidos no original (`referencia/catalogo-de-moldes.py` mostra a chamada de cada um; `referencia/cenas-exemplo-conversa-parada.py` é um reel inteiro):
- **Visor da câmera** (`ui_camera`) sobre foto: entra com quadro preto + exposição subindo 0,42 s.
- **Visualizador de fotos** (`ui_galeria`) sobre foto 3D/sala: cabeçalho fixo.
- **Celular antigo / notas**: foto de aparelho + texto digitado no quad da tela + câmera que entra até 3× seguindo o cursor.
- **Composer**: o mundo anterior vira a IMAGEM ANEXADA do post (mundo dentro do mundo); câmera entra na linha digitada.
- **Flatlay com console**: texto digitado na tela do aparelho; giro de 360° com borrão; frase grande preta assenta por cima (camada fixa).
- **Lousa**: foto de ardósia ESCURA e limpa (régua dourada na diagonal, relógio acima, sombra suave; sem reflexo forte),
  texto num `quad` que segue a perspectiva da lousa, fonte Kalam com `GIZ` (traço tremido com falhas de pó), a palavra-chave
  em vermelho vivo `#ff6a58`, sublinhado e `laco()` que se desenham.
- **Atravessar a palavra** ("They aren't → wrong."): a câmera entra na frase até as letras virarem 1º plano gigante e
  desfocado nas BORDAS (um "y" escuro na esquerda, um "a" na direita) e o centro fica livre para a palavra seguinte.
  Origem do zoom = entre as duas letras, calculada com `_larg()` (ver o exemplo); escala ~15; as letras escurecem; o blur vai
  dividido pela escala (1,2 px vira ~18 px). Os objetos que voam junto são do vocabulário da frase (placa de aviso →
  `placa_aviso()`), nunca um objeto qualquer (os cones listrados foram reprovados).
- **Tela de aparelho**: aparelho HORIZONTAL de tela larga quando a frase tem 2 linhas (o portátil vertical quebrava
  "game" em "ame" e foi reprovado como "torto e estranho"); cantos da tela medidos com `medir/superficie.py`; fonte `lcd`
  (VT323) com o filtro `LCD`; o aparelho ocupa ~1/3 da largura do quadro, não o quadro inteiro.

**Tipografia:** Inter (500-800) pequena e discreta; Kalam + `GIZ` para lousa; Caveat para caneta no papel; VT323 (`lcd`)
ou Press Start 2P (`pixel`) + `LCD` para tela de aparelho; JetBrains Mono para interface técnica.
Uma cor de acento por mundo, vinda do próprio mundo. Nada de legenda de rodapé.

## 5 · Cadência, transição e permanência (checado por `medir/cadencia.py`)

| Regra | Original | Limite |
|---|---|---|
| Duração do mundo | mín. 1,00 · **mediana 2,24** · máx. 5,16 s | ≥ 1,0 s; mediana 1,8-3,0 s |
| Onde cai o corte | 0,00-0,25 s antes da 1ª palavra da frase (mediana +0,07) | palavra começando até 0,30 s depois do corte (zoom/flash são livres) |
| Respiro (último elemento → corte) | mín. 0,45 · mediana 0,77 s | ≥ 0,45 s (≥ 0,15 se o mundo termina digitando) |
| Maior vazio sem novidade | máx. 1,05-1,08 s | ≤ 1,15 s (digitação e contador cobrem) |
| Intervalo entre elementos | mediana 0,20 s | ~1 palavra |
| Mundo > 3 s | sempre tem câmera andando | 1 evento interno (câmera/rolagem/empurrão) a cada ≤ 2,5 s |
| Tempo em faixa 1:1 | 40 % | 20-50 % |
| Texto x voz | 1ª palavra junto da fala; a frase completa ~0,2-0,45 s antes da voz | `P(i)` já adianta 0,04 s; frases assentadas podem adiantar mais |

**Transições** (corte seco é o padrão; as outras uma vez cada, no máximo):
`("zoom", 0.30)` zoom-através com desfoque (o mundo continua mais perto) · `("preto", 0.42)` quadro preto + exposição
(entrada de câmera) · `("dissolve", 0.20)` dissolvência com desfoque · `("flash", 0.30)` vazamento de luz branco (entrada
do CTA) · objeto que passa na frente (`img` voando) + corte · mundo dentro do mundo (a foto anterior reaparece numa tela).

**Câmera:** nunca parada. Push lento 1,00→1,08-1,15 com rotação leve; use `foco(t, escala, x, y, rot)` (o ponto x,y fica
no centro). 1 movimento rápido a cada ~3 mundos: giro (com `anim(câmera, blur)` e escala ≤ 1,4 durante o giro), rolagem de
lista, empurrão lateral, entrada forte. Quando a câmera gira, o fundo do mundo precisa cobrir (grade/cor da base).

## 6 · Imagens (Higgsfield)

Modelo `nano_banana_pro` (fotos de mundo, 9:16) e `gpt_image_2_6` (objetos, 1:1). Sempre fotográfico, luz dura de
janela, grão de filme, **superfície em branco** onde a palavra vai morar. Prompts que funcionaram:
- **Mesa de cima:** "Top-down photo of [superfície] with [objetos do tema], a blank [papel/tela/cartão] in the center,
  hard diagonal sunlight beam with shadow, analog film look, grain, no logos, no readable text", 9:16.
- **Aparelho com tela em branco:** "Photorealistic close-up of [aparelho] … its screen shows a blank [app] page, no words
  on the screen, cinematic, no logos, no brand, no text", 9:16 (`nano_banana` falhou uma vez; `gpt_image_2_6` resolveu).
- **Objeto:** "Photorealistic [objeto], isolated on a pure white seamless background, soft studio light, no text, no logos"
  → recorte com `rembg` (já vem no Python da skill).
Gere 2 variantes (uma `nano_banana_pro`, uma `gpt_image_2_6`) e escolha no olho: na lousa e no flatlay a do `gpt_image_2_6`
venceu. Se sair em 752×1344, faça `upscale_image` (2k) antes de usar. Depois: redimensionar para 1440×2560 e achar os
cantos da superfície com `python medir/superficie.py foto.jpg x y` (x, y = um ponto dentro da superfície; grava
`foto-superficie.jpg` com o contorno para conferir) e usar no `quad=`. **Conferir desenho de produto reconhecível** (o smartphone saiu com cara de iPhone e o
console com cara de Game Boy na recriação; peça "generic, unbranded design" e confira).

## 7 · Som

**Os efeitos daqui são REFERÊNCIA, não regra** (Felipe, 12/11): o kit abaixo foi medido no original e é o ponto de
partida. Em cada reel, teste outros sons em cada parte e fique com o que soar melhor ali. O que vale sempre é só isto:
**nada de efeito em todo corte** (o mesmo som em toda virada ficou repetitivo e foi reprovado) e nada de sino, caixa
registradora ou glitch.
**Menos é mais (13/11):** com 34 efeitos de destaque em 80 s (impacto em quase toda palavra de fecho) o Felipe achou
"muito poluído, com efeitos muito repetidos" e mandou tirar na dúvida. Ficaram ~11 em 80 s: 2 impactos (fecho do gancho e
fecho final), 1 queda na virada principal, riser + queda-grave na frase-chave, 2 whooshes, poucos cliques de interface,
digitação só no CTA. Na dúvida, tire. Nunca o mesmo som duas vezes seguidas.

**O que o original faz de verdade** (medição evento por evento de 13/11 nos stems do demucs, com a palavra de cada um;
as leituras de 12/11 erraram duas vezes): o efeito principal é um **IMPACTO texturizado** que cai na **palavra de fecho da
frase** ("years ago", "would be", "Over 80 %", "short game"), não no corte: 6 em 31 s, mais denso no gancho. Mais um
**soco** curto ("wrong."), a **queda** em 2 cortes, o **riser** 1 vez e o **whoosh** nos 3 movimentos rápidos. A maioria
dos cortes é seca. Ao todo ~1 golpe a cada 3-5 s, alternando os tipos (nunca o mesmo som em sequência).

| Tipo (kit inicial) | Som (medido) | Onde no original | Nível (pico vs. p90 da voz) |
|---|---|---|---|
| impacto (+ impacto-2, impacto-3) | ataque seco, corpo 60-250 Hz com sub tonal descendo ~100→55 Hz, médios 20-25 dB abaixo, agudos 35-45 dB abaixo; sustenta ~0,4 s e solta em 0,1 s. Recriado pela curva média de 8 bandas dos 6 booms (`medir/molde-boom.json`; `medir/conferir_impacto.py` dá o erro, ~4 dB); as variações mudam ±1 semitom | palavra de fecho da frase (6 em 31 s) | ref +4,7 → no metas +7,8 a +8,3 (ver nota) |
| soco | o mesmo molde comprimido: bloco de 0,15 s, ataque e corte secos | palavra-soco curta ("wrong.") | ref +7,4 → no metas +9,5 |
| queda | tom que despenca de ~2 kHz a ~50 Hz em 0,2 s (rápido no começo), máximo em 0,11 s, some em 0,3 s; começa NO corte, sem sopro antes | 2 de 13 cortes (8,07 · 20,23) | +4 dB |
| queda-grave | a mesma, partindo de 400 Hz | logo depois do riser | +4,5 dB |
| whoosh | sopro de ar grave-médio (200 Hz-3 kHz, centro ~1,1 kHz), sobe 0,35 s, cai 0,5 s; marcar o PICO | movimentos rápidos: zoom-através, rolagem, giro | ref −0,8 → no metas +2 |
| riser | sopro largo (200 Hz-6 kHz) que incha 1 s e corta seco | 1 vez, no corte mais importante | −7,6 dB |
| clique | tom 3 kHz, 45 ms | pílula/selo que pipoca | +2,5 dB |
| pop | grave curto 180→110 Hz | objeto que pipoca | −6 dB |
| tecla | clique agudo ~5,6 kHz | digitação | −13 dB |
| boom | (antigo: sopro + grave em todo corte; **não usar como padrão**) | — | +5 dB |

Gerados por `medir/sfx_b.py` (clique, pop, tecla, boom), `medir/sfx_ref.py` (queda, queda-grave, whoosh, riser) e
`medir/impacto.py` (impacto, impacto-2, impacto-3, soco) em
`assets/sfx/`. Marque `SOM(tipo, t)` com t = o corte (queda) ou o pico (whoosh); o `pre.json` desconta o que começa antes.
Aplicação no reel de exemplo (“Conversa parada”) (80 s, 30 mundos, versão de 13/11): impactos e socos nas palavras de fecho
("sozinho", "economizando", "perceber.", "54", "problema", "gasto.", "considerável", "resumo,", "Mas,", "pausa."), queda
em 2 cortes, riser + queda-grave na frase-chave e whoosh em 4 movimentos rápidos; o resto dos cortes seco.

**Testar outros efeitos em cada parte:**
1. Fazer um `./reel.sh montar` (grava `assets/mix_sem_efeitos.wav`, só voz + trilha).
2. Juntar candidatos: os do kit, um `.wav` sintetizado, ou gerado no Higgsfield (`generate_audio`, modelo
   `mirelo_text_to_audio`, `duration` 1-1,5 s, ~0,38 crédito). Na 1ª tentativa os 6 gerados vieram como chiado constante ou
   com impacto no fim: descreva a FORMA do som (quando sobe, quando some, grave ou agudo) e meça antes de usar.
3. `./reel.sh provar <t> nada queda whoosh caminho/outro.wav@-3` → `renders/provar-<t>.m4a`: o mesmo trecho, uma vez com
   cada opção (sufixo `@db` = ganho extra, `@db@pre` = segundos antes de t). Escolher no ouvido, de preferência com a pessoa ouvindo junto.
4. Efeito novo que ficar: copiar para `assets/sfx/<nome>.wav`, pôr o nível em `metas.json` → `efeitos_rel_voz_p90_db`
   (sem nível, o `mix.py` usa −6 dB) e o `pre` em `assets/sfx/pre.json` se ele começar antes do instante marcado.

- **Trilha** (medida camada por camada em 13/11; também é referência, não regra). O original tem QUATRO camadas, não só
  um 808 (a descrição de 12/11 estava incompleta):
  - **Baixo:** seno limpo com a oitava (2º harmônico −2 a −14 dB), **sustentado**, notas longas de 3-4 s que descem em dó
    sustenido menor (C#2 → B1 → A1 → G#1) com **glide de 0,3-0,4 s**, sem ligação com os cortes; ~19 dB abaixo do p90 da
    voz. **Duas pausas longas** do baixo (na ref: 7,5-12,5 s e os 6,5 s antes do CTA).
  - **Pluck:** teclado suave quase senoidal com harmônicos de sino, ataque ~0,1 s, ~0,4 s de nota, **~2 notas/s em
    semicolcheias de 99 bpm**, notas do acorde na região C4-B4; ~21 dB abaixo da voz, sobe na 1ª pausa do baixo, cai na reta.
  - **Ronco grave** (40-125 Hz, ruído, não pad afinado) que enche a 1ª pausa do baixo; **brilho** agudo tonal e
    sustentado (2-8 kHz) bem baixo; **sub** de 25-55 Hz enquanto o baixo toca.
  - **CTA:** baixo distorcido em C#2 a ~12 dB abaixo da voz + bumbo 808 (queda de tom) em 0,10 · 0,35 · 2,10 · 2,50 ·
    2,90 · 3,30 s e chimbal irregular.
  **Como fazer a trilha (o que funcionou em 13/11):** sintetizar essas camadas do zero foi REPROVADO ("que merda de música
  é essa? não tem nada a ver"): o espectro e os níveis bateram com a ref, mas soou como MIDI barato. Medição não
  substitui ouvido. O caminho que funcionou:
  1. Gerar 4 trilhas PRODUZIDAS de 40 s no Higgsfield (`elevenlabs_music_v2_5`, `force_instrumental`, ~5,8 créditos cada),
     cada uma numa leitura do estilo (trap escuro com sino · piano e sino com 808 · phonk com caixinha de música ·
     documentário com arpejo). A pessoa escolhe NO OUVIDO. No reel de exemplo (“Conversa parada”) venceu a phonk: "Minimal dark
     phonk-style instrumental: distorted sliding 808 bass, a haunting music box melody, light vinyl crackle, sparse and
     spacious, lots of room for a voice-over. Drums only drop in during the last few seconds. No vocals."
  2. Separar a escolhida no demucs (bateria / baixo / melodia) e MONTAR na linha do tempo com a forma da ref: introdução,
     baixo entrando num corte, corpo sem bateria, pausas do baixo, reta quase em silêncio e a bateria entrando no CTA.
     Emendar em blocos de compassos (achar o ciclo pela semelhança de croma; lá era de 8) e ajustar o tempo em <1 % para
     os pontos-chave caírem em começo de compasso. Exemplo: `medir/trilha_montar_exemplo.py`.
  O que também não funcionou: pedir a trilha inteira ou só o pluck num prompt técnico (arranjo errado, 6 notas/s, outro
  tom) e usar um bloco de 808 gerado como sampler, uma nota por mundo (o bloco era lá, A1, e tudo saiu meio tom abaixo).
- **Master:** `loudnorm` de uma passada até −14,2 LUFS, sem tratar a voz antes. Em 13/11 tentei segurar a voz
  (compressor + limitador) e trocar o loudnorm por ganho fixo + limitador para os efeitos não perderem pico: o Felipe
  reprovou ("estragou e picotou o áudio"). O código ficou no `mix.py` desligado (`segurar_voz`), não religar sem pedido.
- **Nota sobre os níveis dos efeitos:** a coluna "ref" é medida no stem separado do original (depois do master dele). Os
  números do `metas.json` são maiores porque o nosso master e a separação ainda tiram ~2-3 dB dos picos. Confira sempre
  separando a NOSSA mixagem (`demucs -n htdemucs -o medir/sep medir/sep/nosso.wav` com `assets/mix.wav` copiado para lá) e
  rodando `medir/comparar_efeitos_ref.py`: impacto, soco e queda devem cair a ±2 dB da ref. O whoosh mede uns 3 dB abaixo
  porque parte dele vaza para o stem de voz (na mixagem bruta ele está no nível certo).

## 7.5 · QUADRO SEGURO (regra nº 1 desde a auditoria de 12/11)

O Felipe reprovou texto saindo da tela. Por isso, e mesmo quando o original faz diferente:
- **Nenhuma palavra cortada, coberta, vazando da superfície ou encostada em outra com a câmera parada.** Só se tolera
  corte de 1-4 quadros no meio de um movimento rápido (rolagem, empurrão, zoom), e mesmo assim borrado.
- **Calcule o enquadramento a partir da largura real do texto** (`_larg()`), nunca no olho: a linha mais longa × escala da
  câmera tem que caber em 720 − 2×36 px. Texto que não cabe ganha quebra de linha, não zoom menor "na sorte".
- **Câmera que anda num texto longo anda na VERTICAL** (linhas empilhadas), nunca seguindo o cursor para o lado.
- **O fundo sempre cobre o quadro**: rotação e deslocamento pedem escala (θ=5° → ≥1,15; θ=12° → ≥1,35). A `foto()` já põe
  atrás uma cópia ampliada e desfocada (rede de segurança), mas o auditor reprova canto descoberto com a câmera parada.
- **Uma palavra nunca aparece antes da hora** (nem fantasma) e o **"assentar" não recentra** a linha: o layout final é reservado.
- **Um cursor por vez** (some quando o próximo campo começa). Interface no **idioma da fala** (`IDIOMA = "pt"` no cenas.py).
- **Zona do Instagram**: coluna direita (x > 620 no palco) na metade de baixo e rodapé (y > 1100) só com decoração.
- **Transição nunca mostra dois textos nítidos juntos** (a dissolvência borra os dois mundos) nem quadro preto acidental.
- **Câmera de mão sutil** em todo mundo (±5 px, ±0,3°; `mundo(mao=0.6)` nas telas de app) e **borrão de movimento**
  (`borrao(t, dur, px)`) em todo movimento rápido de câmera.
- **Energia de câmera parecida com a do original** (o B é inquieto: 47 % de quase-parada). Medido na auditoria: mundo de
  leitura com câmera parada é o defeito nº 2 depois do texto cortado. Todo mundo tem push/rotação/pan CONTÍNUO; textos
  longos ganham aproximação por linha (close na linha que está sendo digitada, sem cortar); listas continuam rolando.
- **Escala mínima para cobrir o quadro**: com o ponto de foco a `d` px do centro na vertical, s ≥ 1/(1 − d/640);
  com rotação θ, s ≥ cos θ + 1,78·sen θ; giro de 360° exige s ≥ 2,04 durante o giro (vira um "mergulho girando").
- **Escrita à mão** com `escreve(id, t, d)` (máscara de borda suave), nunca recorte seco que decepa letra.
- **Apóstrofo tipográfico** (’) no texto que aparece; aspas “ ”.
- **Interface genérica de verdade**: nada que lembre X/iMessage/Google (cor de destaque própria, rótulos neutros, sem
  "AI Mode"), avatares com inicial no mesmo estilo.

## 8 · Checagens antes de entregar

| Checagem | Ferramenta | Passa quando |
|---|---|---|
| Voz | `./reel.sh voz` (`voz_medir.py`) | VOZ: APROVADA + contorno com ataque e queda |
| Fala completa | `./reel.sh conferir-fala` | todas as frases presentes |
| Cadência | `./reel.sh checar` (`cadencia.py`) | CADÊNCIA: APROVADA |
| Auditoria quadro a quadro | `./reel.sh checar` (`auditoria.mjs` + `auditoria_relatorio.py`) | AUDITORIA: APROVADA (relatório em `medir/auditoria-relatorio.txt`) |
| Movimento | `pericia-movimento.py --contra` (no `montar`) | amplitude ≥ 6,1× · quase-parada ≥ 37 % · ≥ 2 picos |
| Olho | `renders/<nome>-folha.jpg` | texto dentro da superfície, nada cortado, foto fotográfica, sem marca de terceiros |

## 9 · Armadilhas já vividas (na recriação)

- **Desfoque escala junto:** `blur` num elemento que cresce 10× vira 10× mais desfoque e o elemento some. Use blur/escala.
- **Giro sem cobertura** mostra cantos pretos: fundo do mundo com a cor/grade da base + escala adequada.
- **Giro forte demais** vira o único pico e reprova o teste de movimento: borrão durante o giro e escala ≤ 1,4.
- **`assenta` não anima tamanho de fonte** (o linter do HyperFrames reprova reflow): a palavra cresce por `scale` e a linha
  se recentra medindo no navegador.
- **Texto digitado sem largura** quebra na borda do palco: sem `w` ele fica numa linha só (`white-space: pre`).
- **Cursor** só aparece 0,3 s antes de a digitação começar.
- A trilha separada com demucs carrega restos de efeitos do original; para medir os nossos efeitos, meça na mixagem.
- **Antes de chamar um grave do original de "efeito" ou de "nota"**, olhe os stems lado a lado num espectrograma e ponha a
  palavra falada em cada evento: em 12/11 um detector de onset confundiu impactos com notas do baixo e a conclusão saiu errada.
- **Compare stem com stem**: separe a NOSSA mixagem no demucs também (`demucs -n htdemucs`) e meça as duas do mesmo jeito.
  Comparar a mixagem inteira esconde que uma camada inteira está faltando (foi o caso do pluck, 25 dB abaixo).
- **Letra à mão decepada** (Caveat/Kalam são inclinadas e passam da caixa; o `escreve()` cortava o fim): use `extra=FOLGA`.
- **Foto que descobre canto** com zoom/rotação: use `fc()` no lugar de `foco()` nos mundos de foto (limita escala e centro).
- **Duas pílulas de progresso** no mesmo reel: o id agora é único por padrão (antes as duas eram `pp` e a 2ª não contava).
- **Auditor parado em reel longo**: `auditoria.mjs` espera `load` (180 s), não `networkidle0`.

- **Imagem "quase boa" não serve** (rodada de 12/11, reprovada pelo Felipe): lousa com reflexo de sol em X, portátil
  vertical com texto quebrado e cones no lugar de placas de aviso. Antes de montar, olhe cada imagem já no quadro
  (a folha de quadros do `montar`) e troque a imagem quando o mundo não "lê" de primeira.
- **Lista que rola** tem que sair antes de a frase seguinte começar (`power2.inOut`, ~0,9 s), senão as linhas passam por cima.
- **Título longo digitado**: a câmera termina enquadrando o FIM do título (no original ela anda junto), senão ele corta.

## 10 · Arquivos

`base/`: `build.py` (motor HyperFrames + GSAP; filtros `GIZ` e `LCD`; câmera de mão; rede de segurança das fotos), `mundos.py`
(telas genéricas com rótulos PT/EN, ícones de traço, `tela_lcd`, `chip` que cresce, `onda` animada, `laco`, `placa_aviso`), `cenas.py` (modelo), `mix.py`, `reel.sh`,
`assets/` (fontes, grão, efeitos), `medir/` (texto, alinhar_ctc, ritmo_voz, voz_medir, tom, acento, cadencia, auditoria, folha, superficie, sfx_b, sfx_ref, provar_efeitos, metas.json,
Inter-Variable.ttf). `~/.claude/skills/reels-sem-aparecer/motores/dentro-do-mundo/referencia/`: `elementos-original.json` (os 14 mundos da referência e os tempos de cada
elemento, só medidas), `catalogo-de-moldes.py` (a chamada de cada molde, com texto de enfeite) e
`cenas-exemplo-conversa-parada.py` + `fala-exemplo-conversa-parada.txt` (um reel inteiro aprovado: o melhor exemplo de tabela de mundos).
