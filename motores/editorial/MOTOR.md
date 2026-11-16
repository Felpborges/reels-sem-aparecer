# Motor EDITORIAL ("a página que se escreve sozinha") — o estilo A

*Motor da skill `reels-sem-aparecer`. Criado em 12/11/2026 a partir do reel aprovado "Claude Code e a conversa parada" (v2),
medido contra um reel de referência de 80,1 s. O vídeo de referência não acompanha a skill; as medidas dele, sim.*

> **Como ler este manual.** “O Felipe” é o Felipe Borges, que criou e validou este motor; cada reprovação dele registrada
> aqui virou regra e vale para qualquer pessoa. O que é escolha de cada reel (tema, texto, voz, trilha, imagens) é de quem
> está fazendo o reel. Os comandos partem da pasta do projeto criado pelo `novo-reel.sh`; os arquivos de `referencia/`
> ficam em `~/.claude/skills/reels-sem-aparecer/motores/<motor>/referencia/`.

**O estilo em uma frase:** cada palavra aparece na tela no instante em que é dita e a imagem que ela evoca já está lá,
numa página branca que se monta durante a frase e é trocada por corte seco quando a frase acaba.

**Regra-mãe:** do original copiamos método, ritmo, som e física; nunca o conteúdo (tema, frases, fotos, marcas).
Tudo o que está aqui foi **medido** no original (perícia de movimento, separação de áudio com demucs, recriação quadro a
quadro) e **validado** pelo Felipe na v2. Não mudar número sem medir de novo.

---

## 1 · Pipeline (a ordem importa)

```bash
zsh ~/.claude/skills/reels-sem-aparecer/ferramentas/novo-reel.sh editorial <pasta-do-reel> fala.txt "Título do reel"   # cria o projeto (copia base/, lê o roteiro)
# gerar a voz no Higgsfield (§3) e as imagens (§6); tratar com medir/recortar.py
cd <pasta-do-reel>
./reel.sh voz narracao.mp3      # ritmo do original + alinhamento palavra a palavra + medição contra as metas
./reel.sh conferir-fala         # transcrição por trechos: confirma que nenhuma frase sumiu
# escrever cenas.py (§4, §5); efeitos com SOM() dentro das cenas (§7); trilha em assets/trilha.mp3
./reel.sh checar                # margens -> build -> cadência; corrigir até passar
./reel.sh montar                # mixagem -> render -> cópia leve -> teste de movimento -> folha de quadros
```
Olhar `renders/<nome>-folha.jpg` (último quadro de cada cena) antes de entregar: é onde aparecem sobreposições,
texto branco sobre fundo claro e imagem com cara de brinquedo, que nenhuma checagem automática pega.

Ambiente: tudo vem do `instalar.sh` da skill (Python próprio com demucs, librosa, rembg e o alinhador em português; HyperFrames na versão validada; `ffmpeg` e `rubberband`). O `reel.sh` de cada projeto já usa esse ambiente sozinho. Para conferir a máquina: `zsh ~/.claude/skills/reels-sem-aparecer/ferramentas/diagnostico.sh`.

## 2 · Roteiro

- **Tamanho:** ~250 palavras = ~70 s no ritmo do original (212 palavras/min). `texto.py` informa a duração prevista.
- **Esqueleto do original:** gancho contrarian com o assunto na 1ª palavra (0-3 s) → autoridade/prova (3-6 s) → virada
  (pergunta ou contradição, com a 1ª foto em tela cheia) → mecanismo em blocos curtos → "sobe a aposta" → o outro lado →
  veredito (opinião) → **fecho em pergunta** que acaba na última palavra, sem "me segue".
- **Frases curtas e orações fechadas.** A montagem corta entre frases; uma oração longa vira uma cena longa (até ~3,5 s está ok).
- **Palavras de virada** a cada 8-12 s ("Só que", "Tanto que", "Agora,", "Mas").
- **Marcas:** só as do próprio tema (nenhuma marca de terceiros na imagem nem na fala, a não ser que o tema peça).
- Pronúncia para o alinhamento: `medir/texto.py` já troca Claude/Code/Pro/Max e números; marca nova entra no dicionário `PRON`.

## 3 · Voz

- **Gerar:** Higgsfield `generate_audio`, modelo `elevenlabs_v4`, `stability: 0.75`, um único `dialogue` com a fala
  inteira (parágrafos separados por linha em branco). Voz padrão **Alden** (`fec5acae-d801-5761-8d2c-4c2c75db3e2a`);
  alternativa já testada e aprovada: **Andre** (`f1e8226e-2248-4d5f-b43c-0a79e9949dbf`).
- **Por que o Alden:** de 44 vozes masculinas medidas, é a que mais se aproxima do narrador do original em português:
  entonação contida (4,4 semitons; Andre 5,6; original 3,0) e ênfase por volume (3,5 dB; Andre 1,9; original 3,8).
  Em PT todas as vozes do ElevenLabs sobem o tom; não existe uma tão grave quanto o original (124 Hz).
- **Ritmo:** `./reel.sh voz` encurta as pausas para a distribuição do original e acelera sem mudar o tom
  (rubberband R3) até 212 palavras/min. A narração crua sai a ~180/min; o fator fica em ~1,17-1,20.
- **Metas** (`medir/metas.json`, checadas por `voz_medir.py`): 200-222 palavras/min · pausa máxima 0,25-0,45 s ·
  84-92 % do tempo falando · entonação ≤ 4,6 st · ênfase ≥ 3,0 dB.
- **Conferir a fala por trechos** (`./reel.sh conferir-fala`): a transcrição do arquivo inteiro "pula" frases que estão lá.

## 4 · Cenas: os moldes

Espaço 720×1280 (o palco é escalado ×1,5). Uma cena = uma frase ou oração; `scene(i)` corta 0,10 s antes da palavra i.
**Todas as trocas são corte seco**, menos a segunda cena do vídeo (dissolvência com desfoque, 6 quadros), como no original.
Câmera: deriva lenta por cena, `cam=(escala, dx, dy)` entre 0,95 e 1,07 e ±22 px; telas cheias usam 1,06-1,07.

| Molde | Quando | Receita (coordenadas da v2) | Quantas (70 s) |
|---|---|---|---|
| **A · recorte P&B** | pessoa: "você", quem pergunta, quem sofre | `I("pessoa.png", x, 430-520, 360-560, mask=(64-68, 95-97))` P&B, base some no branco; texto acima | 3-4 |
| **B · cartão de foto** | cena concreta ("almoço", "mensagem nova") | `I(src, 360, 320-390, 470-540, h=410-600, kind="card", cut=True)`; palavra branca DENTRO (embaixo, z=5), pretas FORA | 4-5 |
| **C · tela cheia** | virada/tensão; uma a cada ~12-18 s | `TELA(src, h=640-760, a=.45-.6, b=.2-.3)`, foto 9:16 P&B com topo escuro; texto branco no terço de cima | 4 |
| **C' · painéis** | comparação ("maior a conversa, maior o gasto") | dois `I(..., 196/524, 262, 304, h=660, kind="card", t=P(i), fade=0.02)`, um por palavra, som "painel" | 1 |
| **D · tipografia + manchas** | re-gancho e virada falada ("Só que", "Porque é justamente") | `scene(i, blobs=True)`; palavra-chave gigante (150-200) | 3-5 |
| **E · objeto** | coisa nomeada (ampulheta, caixa, sino, lupa, olho que pisca) | objeto **fotográfico** recortado, sombra `drop-shadow`, entra com a cena | 6-8 |
| **F · sanduíche** | palavra gigante atrás da figura ("grande" atrás da torre, "gente" atrás da multidão) | palavra `z=1` cinza, figura `z=3` na frente | 2 |
| **Selos + pílulas** | opções e listas ("1 continuar / 2 começar") | `BADGES([x], y, 64-76, [P(i)], nums=(n,))` + `PILL(...)` ao lado | 1-2 |
| **Prova** | o print/linha oficial ("Tá lá no registro") | cartão branco com o trecho real, sublinhado escuro animado (nunca marca-texto colorido) | 1 |
| **Fecho** | pergunta final | volta a figura da abertura, grande e ancorada na base; pergunta "digitada" (`typed=True`, fonte h); 2 cenas com a figura no mesmo lugar | 2 |

**Tipografia:** Poppins 500-700 (letra de ligação 36-48, palavra-chave 100-310), Grand Hotel inclinada (`font="b"`) para a
palavra de desejo/ação, Playfair itálica (`font="d"`) para palavra abstrata. Cores só de tinta: preto `#111` nas pequenas,
cinza `#505050` nas gigantes, branco sobre foto. **Nenhuma cor de destaque no texto**; a cor vem das fotos e do logo.
Margem de 36 px: nenhuma palavra pode passar (checado). Texto branco tem que caber **dentro** do cartão.

## 5 · Cadência (o que faz "dar tempo de ler")

Medido nas 39 cenas da recriação fiel e checado por `medir/cadencia.py` (o `./reel.sh checar` para se falhar):

| Regra | Original | Limite |
|---|---|---|
| Duração da cena | p10 1,37 s, mediana 1,93 s | ≥ 1,2 s quando há mais de 3 elementos |
| Respiro (do último elemento novo até o corte) | p10 0,35 s, mediana 0,58 s | ≥ 0,30 s |
| Imagem principal na tela | mediana 1,83 s | ≥ 0,9 s |
| Densidade | máx. 6,1 elementos/s | ≤ 6 |
| Cena que já abre com a imagem | 23 de 31 | ≥ 70 % |

Como consertar quando falha: **junte a cena curta com a vizinha** (a figura fica e as palavras/opções entram ao lado:
o "uma palavra por vez" do original) e **faça a imagem entrar no corte** (`cut=True`), nunca no meio da frase.
Origem: o Felipe achou rápida demais a troca "ele pergunta se você quer" → opções 1 e 2 (1,03 s e 0,10 s de respiro).

## 6 · Imagens (Higgsfield)

Modelo: `nano_banana_pro` para pessoas e fotos, `gpt_image_2_6` para objetos. Modelos de prompt que funcionaram:
- **Recorte P&B (A):** "Black and white studio photograph of [pessoa genérica, idade, roupa], [gesto], framed from the waist
  up with empty margin around, isolated on a pure white seamless background, even soft light, no shadow on the background" → `recortar.py recorte x.png --pb`
- **Tela cheia (C):** "Vertical black and white cinematic photo of [cena], [luz], dark background/negative space in the upper
  third, film grain, no logos, no brand names, no readable text", 9:16, 2k → `recortar.py foto x.png`
- **Cartão (B):** foto colorida natural, 1:1 ou 3:4, "no logos, no readable text" → `recortar.py foto x.png --larg 800`
- **Objeto (E):** "Photorealistic studio photo of [objeto real], front/three-quarter view, isolated on a pure white seamless
  background, soft shadow underneath, no text, no logos" → `recortar.py recorte x.png --larg 700`

**Sempre fotográfico.** Render 3D "de argila" sai com cara de brinquedo (a bateria verde foi reprovada; virou ampulheta).
**Conferir logos de terceiros** em todo notebook/celular gerado (veio uma maçã na tampa): `recortar.py retoque`.
Logo da marca do tema: SVG oficial em `assets/img/`, em toda menção a ela (o do Claude, `assets/img/claude.svg`, já vem como exemplo).

## 7 · Som

- **Efeitos:** só os 4 tipos do original, sintetizados com o perfil medido nele (`medir/sfx_sintese.py`, já em `assets/sfx/`).
  Marcar na própria cena com `SOM(tipo, P(i))` ou `SOM(tipo, INI)`:

| Tipo | Som | Onde | Nível (pico 10 ms vs. p90 da voz) |
|---|---|---|---|
| impacto | grave 20-60 Hz | só no 1º quadro | +9,7 dB |
| pop / pop-longo | tom ~850 Hz, ~25 ms | selos, objetos, pílulas, logo, opção | -4,5 / -9,2 dB |
| clique / clique-grave | tom ~2,5 kHz / ~1,45 kHz, 5-10 ms | cartão, tela cheia, palavra-chave, abertura de cena | -8,7 / -11 dB |
| painel | grave + sopro | cada painel vertical | -11,5 dB |

  Densidade do original: ~0,47 por segundo (≈33 num reel de 70 s). Nada de digitação, sino, caixa registradora ou riser.
- **Trilha:** Higgsfield `elevenlabs_music_v2_5`, ~75 s, `force_instrumental: true`, prompt: "Soft minimal background bed for
  a fast documentary-style explainer short: gentle plucked pizzicato strings and felt piano playing a light, curious,
  repeating melodic figure in the mid register, airy and editorial, steady around 100 bpm, no drums, no percussion, no bass,
  no claps, no risers, no drops, consistent texture from start to end" → `assets/trilha.mp3`. O `mix.py` equaliza
  para a faixa do original (500 Hz-1 kHz), deixa constante (sem ducking) a 23 dB abaixo da voz e fecha em -15,5 LUFS.

## 8 · Checagens antes de entregar

| Checagem | Ferramenta | Passa quando |
|---|---|---|
| Voz | `voz_medir.py` (no `./reel.sh voz`) | VOZ: APROVADA |
| Fala completa | `./reel.sh conferir-fala` | todas as frases presentes |
| Margens | `margens.py` | 0 fora da margem de 36 px |
| Cadência | `cadencia.py` | APROVADO |
| Movimento | `pericia-movimento.py --contra` (no `montar`) | APROVADO (amplitude ≥ 11,5×, quase-parada ≥ 64 %, ≥ 4 picos) |
| Olho | `renders/<nome>-folha.jpg` | sem sobreposição, texto legível, imagem fotográfica, sem logo de terceiros |

## 9 · Armadilhas já vividas

- `margens.py` regrava o `index.html` sem câmera para medir. O `reel.sh` já roda na ordem certa; à mão, sempre `margens → build → render`.
- A transcrição do arquivo inteiro pula frases; confira por trechos antes de achar que a voz engoliu texto.
- Pílula com texto longo passa da margem: quebre com `<br>` e recue o x.
- Separar o áudio final com demucs **não** serve para medir os nossos efeitos (são tons limpos e ele espalha entre faixas); meça direto na mixagem.
- Duração do vídeo = última palavra + 0,2 s (automático no `build.py` e no `mix.py`).
- Custo de um reel completo no Higgsfield: ~40-60 créditos (voz, 12 imagens, trilha e testes).

## 10 · Arquivos

`base/` é o projeto vazio que o `novo_reel.py` copia: `build.py` (motor HyperFrames + GSAP), `cenas.py` (modelo),
`mix.py`, `reel.sh`, `assets/` (fontes, efeitos, logo do Claude), `medir/` (ritmo_voz, alinhar2, texto, voz_medir,
cadencia, margens, recortar, folha, sfx_sintese, metas.json). `~/.claude/skills/reels-sem-aparecer/motores/editorial/referencia/` guarda os tempos da referência quadro a quadro
(`elementos-original.json`, só números) e a tabela de cenas aprovada (`cenas-exemplo-conversa-parada.py`), que é o melhor
exemplo de como escrever as cenas. As metas medidas estão em `medir/metas.json` de cada projeto.
