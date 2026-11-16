---
name: reels-sem-aparecer
description: Produz REELS / Shorts verticais SEM A PESSOA APARECER (motion graphics com narração de IA), do tema ao MP4 pronto, com Claude Code + Higgsfield, em QUATRO MOTORES de edição validados, cada um chamado pelo nome — motor EDITORIAL (a página branca que se escreve sozinha, palavra a palavra), motor DENTRO DO MUNDO (cada frase num cenário, com o texto escrito dentro da cena), motor QUADRO NEON (quadro-negro com neon amarelo que explica uma tese com exemplos de marcas) e motor DOCUMENTÁRIO (mini-documentário de arquivo em fita, colagens e narradora). Cuida de tudo — roteiro no esqueleto do motor, voz, imagens e trilha pelo Higgsfield, montagem em HyperFrames, conferências automáticas e render. Use SEMPRE que pedirem um reel sem aparecer, reel faceless, reel com voz de IA, "faz um reel no motor editorial / neon / documentário / dentro do mundo", "motor A, B, C ou D", "quero um reel estilo documentário sobre X", "3 vídeos sobre X com hooks diferentes nesse estilo", "instala a skill reels-sem-aparecer", ou pedirem os atalhos /reel-editorial, /reel-neon, /reel-documentario, /reel-dentro-do-mundo — mesmo sem citar a skill. NÃO use para editar uma gravação da pessoa falando, para vídeo longo horizontal, nem para carrossel de imagens.
---

# Reels sem aparecer

Quatro motores de edição, um por estilo. A pessoa diz o **nome do motor** e o **tema**; você conduz do roteiro ao MP4.
Quem usa esta skill quase sempre **não programa**: fale pelo efeito ("a voz", "as imagens", "o ritmo"), sem jargão, diga
quanto tempo e quantos créditos cada etapa leva antes de começar e só pergunte o que ela precisa decidir.

`S` = a pasta desta skill (normalmente `~/.claude/skills/reels-sem-aparecer`).

## 1 · Os motores: o nome escolhe o motor

| A pessoa diz | Motor (pasta em `S/motores/`) | O estilo em uma frase | Duração típica | Roteiro |
|---|---|---|---|---|
| **editorial**, "página que se escreve", motor A, `/reel-editorial` | `editorial` | página branca: cada palavra aparece quando é dita e a imagem que ela evoca já está lá; corte seco no fim da frase | ~70 s (~250 palavras) | texto corrido |
| **dentro do mundo**, "mundo", motor B, `/reel-dentro-do-mundo` | `dentro-do-mundo` | cada frase acontece num cenário (mesa vista de cima, lousa, tela de celular) e a palavra é escrita DENTRO dele; câmera sempre andando | ~35 s (~100 palavras) | texto corrido, `»` na frase-chave |
| **neon**, "quadro neon", "quadro-negro", motor C, `/reel-neon` | `quadro-neon` | fundo preto com malha e neon amarelo: uma tese contrária, provada por 4-5 marcas no mesmo molde, lista e chamada | ~42 s (~110 palavras) | marcado por ato: `[gancho] [ponte] [tese] [reframe] [prova] [sintese] [lista] [cta]` |
| **documentário**, "doc", "fita", motor D, `/reel-documentario` | `documentario` | mini-documentário em fita velha: arquivo de época, colagens em papel, palavras serifadas, corte a cada ~1,5 s | livre (30-60 s) | marcado por ato: `[gancho] [contexto] [feito] [rejeicao] [salto] [moral] [cta]` |

Regras do roteador:
- **O nome decide.** Veio um dos nomes (ou atalhos) acima: é esse motor, sem perguntar de novo.
- **Sem nome:** mostre os quatro em uma linha cada e peça para escolher. Se ajudar: notícia/explicação longa → editorial;
  frase de efeito curta e visual → dentro do mundo; tese de negócio com exemplos de marcas → neon; história de uma pessoa
  ou de um fato → documentário.
- **Um motor por reel. Nunca misture** arquivos, medidas, efeitos ou regras de um motor em outro: cada pasta é fechada.
- Depois de escolhido, **leia o `S/motores/<motor>/MOTOR.md` inteiro antes de escrever qualquer coisa** e o exemplo
  completo em `S/motores/<motor>/referencia/` (`cenas-exemplo-*.py` + `fala-exemplo-*.txt`). O manual manda; este arquivo
  só organiza. Os números do manual foram medidos: **não mude número sem medir de novo**.

## 2 · Antes do primeiro reel: a máquina

1. `zsh S/ferramentas/diagnostico.sh`. Saiu `PRONTO`: siga. Faltou algo: rode `zsh S/instalar.sh` (10 a 20 min na primeira
   vez, ~4 GB; pode rodar de novo à vontade). Se ele parar pedindo o **Homebrew**, é o único passo que a pessoa faz
   sozinha (pede a senha do Mac): mostre as três linhas que ele imprime e espere ela avisar que terminou.
2. **Higgsfield conectado.** Voz, imagens e trilha saem do Higgsfield pelo conector (MCP). Confira procurando as
   ferramentas dele (`generate_audio`, `generate_image`, `balance`). Não achou: explique em duas linhas como conectar
   (`references/higgsfield.md`) e pare até ela conectar. Sem o Higgsfield não há reel.
3. Só funciona em **macOS**. Em outro sistema, diga isso logo e não tente contornar.

## 3 · O fluxo (ordem fixa)

**0 · Tema.** Tem tema: siga. Não tem: pergunte o nicho, busque 3 a 5 notícias ou assuntos quentes dele e proponha.
Fato é fato: confira cada afirmação em fonte confiável antes de pôr no roteiro; nada de número inventado.

**1 · Roteiro, no esqueleto do motor.** Escreva pelo capítulo de roteiro do `MOTOR.md` (tamanho, atos, palavras de
virada, onde fica a palavra-chave). Mostre o texto e **espere o ok**: é a única aprovação obrigatória antes de gastar.
Se pedirem "3 vídeos com hooks diferentes", escreva os três roteiros (gancho e desenvolvimento diferentes, mesmo motor)
e aprove os três de uma vez.

**2 · Custo antes de gerar.** Veja o saldo (`balance`) e diga a estimativa do reel (o `MOTOR.md` e
`references/higgsfield.md` trazem os números; em geral de 15 a 60 créditos por reel). Só gere depois do ok. Se o saldo
não dá, diga quanto falta e pare.

**3 · Projeto.** Uma pasta por reel, em `reels/<nome-do-reel>/` dentro da pasta atual (nunca dentro da skill):
```bash
zsh S/ferramentas/novo-reel.sh <motor> reels/<nome-do-reel> <fala.txt> "Título do reel"
```
Daí em diante tudo roda de dentro dessa pasta com `./reel.sh <etapa>` (rode `./reel.sh` sem nada para ver as etapas).
O `reel.sh` já usa o Python, o HyperFrames e os modelos da skill; não instale nem troque nada na mão.

**4 · Voz.** Gere no Higgsfield como o capítulo de voz do motor manda (modelo, estabilidade, voz sugerida), baixe o
arquivo para `narracao/` e rode `./reel.sh voz <arquivo>` e depois `./reel.sh conferir-fala`. Nos motores neon e
documentário a voz é **provisória** até o fim: monte com ela e, com o reel pronto, ofereça 2 ou 3 vozes para a pessoa
escolher no ouvido; `./reel.sh voz <escolhida> && ./reel.sh montar` refaz todos os tempos sozinho.

**5 · Imagens e trilha.** Pelos prompts do capítulo de imagens do motor (sempre fotográfico, nunca 3D "de argila";
conferir logo de terceiros em tudo que for gerado). Trate cada imagem com a ferramenta de recorte do motor. Trilha pelo
prompt do capítulo de som, em `assets/trilha.mp3`.

**6 · Cenas.** Escreva o `cenas.py` do projeto seguindo os moldes do manual e o exemplo. Todo tempo sai da palavra
falada (`P(i)`), nunca de número fixo.

**7 · Conferir e montar.** `./reel.sh checar` até passar; depois `./reel.sh montar` (1 a 5 min). Cada motor imprime os
seus portões (voz, margens ou auditoria de texto, cadência ou ritmo, movimento). Reprovou: conserte como o manual
ensina e rode de novo; não entregue reprovado nem afrouxe a meta.

**8 · Olhar antes de entregar.** Abra a folha de quadros (`renders/<nome>-folha*.jpg`) e olhe de verdade: texto
cortado ou encostado, palavra sobre fundo que some, imagem com cara de brinquedo, logo de terceiros. O automático não
pega isso. Corrija e monte de novo.

**9 · Entrega.** Diga onde está o vídeo: `renders/<nome>-compartilhar.mp4` (leve, para postar) e `renders/<nome>.mp4`
(alta qualidade). Conte em duas linhas o que foi conferido e o que ficou a critério dela (voz, trilha). **Nunca publique
nem envie o vídeo para lugar nenhum**: postar é com a pessoa.

**Ajustes.** Pedido de troca (voz, imagem, frase, ritmo) é uma rodada: mexa só no que foi pedido, `checar`, `montar`,
olhe a folha de novo. Mudou o texto: `./reel.sh texto` (ou o equivalente do motor), voz nova e `voz` de novo.

## 4 · Regras da casa (valem por cima de todo motor)

1. **Do reel de referência só vieram método, ritmo, som e física.** Tema, frases, imagens e exemplos são sempre de quem
   faz o reel. Não tente reproduzir o conteúdo de vídeo de outra pessoa.
2. **Nada de marca de terceiros** em imagem ou fala, a não ser a marca que é o assunto (aí: logo oficial, baixado do
   site da própria marca; print real quando o trecho for educativo). O motor neon vive de marcas reais: use o
   `./reel.sh marca` dele e confira cada print no olho.
3. **Crédito é dinheiro da pessoa.** Estimativa e ok antes de cada lote de geração; nada de gerar "para testar" sem avisar.
4. **Texto sempre legível e inteiro:** nenhuma palavra cortada, coberta ou colada na borda; nada na faixa dos botões
   da rede social (direita embaixo e rodapé).
5. **Cada reel na sua pasta.** Refinamento de um reel (pronúncia de uma sigla, posição de uma legenda, a voz) fica na
   pasta dele; nunca altere `S/motores/`.
6. **"O Felipe" nos manuais** é o Felipe Borges, que criou e validou os motores; as reprovações dele registradas lá são
   regra. O que é escolha de cada reel é da pessoa que está usando a skill.

## 5 · Quando algo falha

| Sintoma | O que fazer |
|---|---|
| "A skill ainda não terminou de ser instalada" | `zsh S/instalar.sh` |
| `conferir-fala` diz que foi pulada | o transcritor é opcional: `zsh S/instalar.sh --com-whisper`; enquanto isso, ouça a narração inteira |
| build do documentário reclama de fonte | `S/.venv/bin/python S/ferramentas/fontes-do-sistema.py` (tira as fontes do próprio macOS) |
| auditoria ou margens não abrem o navegador | falta o Google Chrome instalado |
| render falha | leia `renders/render.log`; quase sempre é imagem que o `cenas.py` cita e não está em `assets/img/` |
| a pasta do reel foi movida de computador | apague o arquivo `.rsa` dela (o `reel.sh` volta a achar a skill no lugar padrão) |

## 6 · Mapa

```
SKILL.md                      este arquivo (o roteador)
instalar.sh                   instala tudo o que os motores precisam (macOS)
ferramentas/                  diagnostico.sh · novo-reel.sh · ambiente.zsh · pericia-movimento.py · fontes-do-sistema.py
motores/<motor>/MOTOR.md      o manual do motor (ler inteiro antes de produzir)
motores/<motor>/base/         o projeto vazio que o novo-reel.sh copia (build, moldes, mixagem, reel.sh, medidores)
motores/<motor>/referencia/   exemplos completos (cenas + fala), prompts e medidas da referência (só números)
references/higgsfield.md      conectar o Higgsfield, modelos usados, custos e como baixar o que foi gerado
atalhos/                      /reel-editorial · /reel-dentro-do-mundo · /reel-neon · /reel-documentario
```
