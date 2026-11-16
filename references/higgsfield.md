# Higgsfield: conexão, modelos, custos e arquivos

Voz, imagens, trilha e efeitos avulsos dos reels saem do Higgsfield, pelo conector (MCP) dele no Claude Code.
A conta e os créditos são da pessoa. **Nunca gere nada sem dizer antes quanto custa e receber o ok.**

## 1 · Está conectado?

Procure as ferramentas do Higgsfield nesta sessão (`generate_audio`, `generate_image`, `list_voices`, `balance`,
`jobs_wait`). Em algumas instalações elas aparecem com prefixo (`mcp__higgsfield__generate_audio`) ou ficam "adiadas" e
precisam ser carregadas pela busca de ferramentas. Achou: chame `balance` para confirmar a conta e o saldo.

Não achou: a pessoa ainda não conectou. Explique assim (é o passo 1 da aula):

1. Abrir **higgsfield.ai/mcp**, entrar na conta e copiar o endereço do conector.
2. No app do Claude: nas configurações, na parte de conectores, adicionar um conector personalizado, colar o endereço e autorizar.
   No Claude Code pelo terminal: `claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp` e depois
   `/mcp` para autorizar no navegador.
3. Abrir uma conversa nova e pedir: "qual é o meu saldo no Higgsfield?". Respondeu com o saldo: está conectado.

O login é sempre feito pela pessoa, no navegador. Não peça senha, código nem chave.

## 2 · O que cada motor pede

Os parâmetros exatos (voz sugerida, estabilidade, prompts) estão no `MOTOR.md` de cada motor. Resumo:

| Para quê | Ferramenta | Modelo | Observações |
|---|---|---|---|
| Narração | `generate_audio` | `elevenlabs_v4` | um único `dialogue` com a fala inteira; parágrafos separados por linha em branco. Os códigos de voz dos manuais são predefinições do Higgsfield: confirme com `list_voices`; se algum não existir na conta, escolha a mais próxima pela descrição (grave, contida, narrador) e avise |
| Fotos de pessoa e de cena | `generate_image` | `nano_banana_pro` | 9:16 para tela cheia; "no logos, no readable text" sempre |
| Objetos recortados | `generate_image` | `gpt_image_2_6` | 1:1, "isolated on a pure white seamless background" |
| Trilha | `generate_audio` | `elevenlabs_music_v2_5` | `force_instrumental: true`; peça a duração do reel + 10 s |
| Efeito avulso (opcional) | `generate_audio` | `mirelo_text_to_audio` | 1 a 1,5 s; descreva a FORMA do som. Os motores já trazem o kit de efeitos pronto |
| Luz de filme (só o neon; já vem pronta) | `generate_video` | `seedance_2_5` | não precisa gerar de novo |

Se um modelo mudou de nome, veja os disponíveis (`models_explore`) e use o equivalente mais novo da mesma família.

## 3 · Quanto custa (ordem de grandeza, em créditos)

| Item | Custo aproximado |
|---|---|
| Narração de um reel | ~2 |
| Imagem (`gpt_image_2_6`) | ~0,25 cada |
| Trilha de 40 a 70 s | ~6 |
| Efeito avulso | ~0,4 |
| **Reel editorial** (voz, ~12 imagens, trilha e testes) | 40 a 60 |
| **Reel documentário ou dentro do mundo** | 15 a 30 (estimativa) |
| **Reel neon** (poucas imagens; os prints das marcas são gratuitos) | 10 a 20 (estimativa) |

Os preços mudam: o valor real é o que a ferramenta informar na hora. Diga a estimativa, confira o saldo com `balance` e
só então gere. Gere em lotes pequenos (4 a 8 imagens por vez) para a pessoa poder parar no meio.

## 4 · Trazer os arquivos para a pasta do reel

A geração devolve um endereço (URL) ou um identificador de trabalho. Espere terminar (`jobs_wait`, com espera curta e
repetida), pegue o endereço do arquivo e baixe para dentro do projeto:

```bash
curl -fL -o narracao/voz-provisoria.mp3 "<endereço da narração>"
curl -fL -o brutos/pessoa.png "<endereço da imagem>"
curl -fL -o assets/trilha.mp3 "<endereço da trilha>"
```

Imagem bruta vai para `brutos/` e passa pelo recorte do motor antes de entrar em `assets/img/`. Confira cada imagem
olhando o arquivo: mão com dedo a mais, texto ilegível inventado, logo de terceiros (maçã na tampa do notebook) e
"cara de brinquedo" pedem nova geração.

## 5 · O que nunca fazer

- Gerar vídeo ou imagem de pessoa real, ou imitando a voz de alguém.
- Publicar, compartilhar ou enviar o que foi gerado: o reel fica na pasta da pessoa.
- Guardar no projeto qualquer chave, senha ou dado da conta dela.
