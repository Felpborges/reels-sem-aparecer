---
name: reel-editorial
description: Atalho da skill reels-sem-aparecer para o motor EDITORIAL — produz um reel vertical sem a pessoa aparecer (a página branca que se escreve sozinha, palavra a palavra), do tema ao MP4, com Claude Code + Higgsfield. Use quando a pessoa digitar /reel-editorial (com ou sem o tema) ou pedir um reel "no motor EDITORIAL".
---

# /reel-editorial

Atalho. O motor já está escolhido: **EDITORIAL** (pasta `editorial`).

1. Leia `~/.claude/skills/reels-sem-aparecer/SKILL.md` inteiro e siga o fluxo dele.
2. Onde ele manda escolher o motor, use `editorial` sem perguntar de novo.
3. O que a pessoa escreveu depois do atalho é o tema (ou o pedido). Sem tema: pergunte o tema ou o nicho.

Se `~/.claude/skills/reels-sem-aparecer/` não existir, diga que a skill principal não está instalada e mostre o comando de
instalação: `curl -fsSL https://raw.githubusercontent.com/Felpborges/reels-sem-aparecer/main/instalar.sh | bash`
