# Reels sem aparecer

Skill para o **Claude Code** que produz reels verticais **sem você aparecer**: você dá o tema, escolhe o estilo pelo
nome e o Claude faz o resto (roteiro, voz, imagens, trilha, montagem e conferência), usando o **Higgsfield** para gerar
a mídia. São quatro motores de edição, cada um medido e validado num estilo:

| Motor | Como chamar | O estilo |
|---|---|---|
| **Editorial** | `/reel-editorial` ou "no motor editorial" | página branca que se escreve sozinha: cada palavra aparece quando é dita |
| **Dentro do mundo** | `/reel-dentro-do-mundo` ou "no motor dentro do mundo" | cada frase num cenário, com o texto escrito dentro da cena |
| **Quadro neon** | `/reel-neon` ou "no motor neon" | quadro-negro com neon amarelo: uma tese provada por exemplos de marcas |
| **Documentário** | `/reel-documentario` ou "no motor documentário" | mini-documentário de arquivo em fita, com colagens e narradora |

## O que você precisa ter

- Um **Mac** (testado em Mac com chip Apple, M1 ou mais novo). No Windows ainda não roda.
- O **Claude Code** (o app do Claude, aba Code, ou o `claude` no terminal).
- Uma conta no **Higgsfield** com créditos, conectada ao Claude (é o passo 1 da aula; a skill te guia se faltar).
- Uns **4 GB livres** e de 10 a 20 minutos para a primeira instalação.
- O **Google Chrome** instalado (a skill usa para conferir se nenhum texto sai da tela).

## Instalar

**Jeito 1 (o mais fácil): peça ao Claude.** Abra o Claude Code e cole:

> Instale a skill deste repositório seguindo o README: https://github.com/Felpborges/reels-sem-aparecer

**Jeito 2: uma linha no Terminal.** Abra o app Terminal, cole e aperte Enter:

```bash
curl -fsSL https://raw.githubusercontent.com/Felpborges/reels-sem-aparecer/main/instalar.sh | zsh
```

Nos dois jeitos o instalador baixa a skill para `~/.claude/skills/reels-sem-aparecer`, instala o que falta e termina
com um diagnóstico. Quando aparecer `PRONTO`, feche e abra o Claude Code de novo.

Se ele parar dizendo que falta o **Homebrew**, é o único passo que precisa da senha do seu Mac: ele mostra a linha para
colar no Terminal; cole, espere terminar e rode o instalador de novo.

<details>
<summary>Para o Claude: como instalar (jeito 1)</summary>

1. Rode `curl -fsSL https://raw.githubusercontent.com/Felpborges/reels-sem-aparecer/main/instalar.sh | zsh` (leva de 10
   a 20 minutos; rode em segundo plano e avise a pessoa do tempo).
2. Se sair com código 3, falta o Homebrew: mostre à pessoa as linhas que o instalador imprimiu, espere ela concluir e
   rode de novo. Não tente instalar o Homebrew você mesmo (pede a senha dela).
3. No fim, rode `zsh ~/.claude/skills/reels-sem-aparecer/ferramentas/diagnostico.sh` e conte o resultado em linguagem
   simples. Confira também se o Higgsfield está conectado (`references/higgsfield.md`).
4. Peça para a pessoa reiniciar o Claude Code para os atalhos aparecerem.
</details>

## Usar

Dentro de uma pasta sua (por exemplo, uma pasta "Reels" na Área de Trabalho), abra o Claude Code e peça:

```
/reel-documentario a história de quem inventou o Wi-Fi
```
```
Faz um reel no motor neon sobre por que ninguém compra "site", compra cliente novo.
```
```
Faça 3 vídeos sobre [tema] com hooks diferentes e desenvolvimentos diferentes, no motor editorial.
```

O Claude mostra o roteiro para você aprovar, diz quantos créditos do Higgsfield vai gastar e só então gera. O vídeo
pronto fica em `reels/<nome-do-reel>/renders/`, em duas versões: `...-compartilhar.mp4` (leve, para postar) e o `.mp4`
em alta qualidade. Nada é publicado sozinho: postar é com você.

Quer trocar a voz, uma imagem ou uma frase? É só pedir na mesma conversa.

## Atualizar ou remover

```bash
zsh ~/.claude/skills/reels-sem-aparecer/instalar.sh --atualizar
```

Para remover, apague a pasta `~/.claude/skills/reels-sem-aparecer` e as quatro pastas `~/.claude/skills/reel-*` dos atalhos.

## O que tem aqui

`SKILL.md` (as instruções que o Claude segue), `motores/` (os quatro motores, cada um com manual, projeto-base e
exemplos), `ferramentas/` (instalador, diagnóstico e utilitários) e `references/` (guia do Higgsfield). Os vídeos de
referência que serviram de medida não acompanham a skill: dos estilos ficaram só método, ritmo e medidas; tema, texto e
imagens são sempre seus. Fontes e ícones de terceiros: `LICENCAS-DE-TERCEIROS.md`.

Feito por Felipe Borges ([@FelipeBorgesFalaIA](https://www.youtube.com/@FelipeBorgesFalaIA)).
