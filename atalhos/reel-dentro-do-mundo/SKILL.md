---
name: reel-dentro-do-mundo
description: Atalho da skill reels-sem-aparecer para o motor DENTRO DO MUNDO — produz um reel vertical sem a pessoa aparecer (cada frase num cenário, com o texto escrito dentro da cena), do tema ao MP4, com Claude Code + Higgsfield. Use quando a pessoa digitar /reel-dentro-do-mundo (com ou sem o tema) ou pedir um reel "no motor DENTRO DO MUNDO".
---

# /reel-dentro-do-mundo

Atalho. O motor já está escolhido: **DENTRO DO MUNDO** (pasta `dentro-do-mundo`).

1. Leia `~/.claude/skills/reels-sem-aparecer/SKILL.md` inteiro e siga o fluxo dele.
2. Onde ele manda escolher o motor, use `dentro-do-mundo` sem perguntar de novo.
3. O que a pessoa escreveu depois do atalho é o tema (ou o pedido). Sem tema: pergunte o tema ou o nicho.

Se `~/.claude/skills/reels-sem-aparecer/` não existir, diga que a skill principal não está instalada e mostre o comando de
instalação: `curl -fsSL https://raw.githubusercontent.com/Felpborges/reels-sem-aparecer/main/instalar.sh | bash`
