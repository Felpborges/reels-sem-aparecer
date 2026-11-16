---
name: reel-neon
description: Atalho da skill reels-sem-aparecer para o motor QUADRO NEON — produz um reel vertical sem a pessoa aparecer (quadro-negro com neon amarelo que explica uma tese com exemplos de marcas), do tema ao MP4, com Claude Code + Higgsfield. Use quando a pessoa digitar /reel-neon (com ou sem o tema) ou pedir um reel "no motor QUADRO NEON".
---

# /reel-neon

Atalho. O motor já está escolhido: **QUADRO NEON** (pasta `quadro-neon`).

1. Leia `~/.claude/skills/reels-sem-aparecer/SKILL.md` inteiro e siga o fluxo dele.
2. Onde ele manda escolher o motor, use `quadro-neon` sem perguntar de novo.
3. O que a pessoa escreveu depois do atalho é o tema (ou o pedido). Sem tema: pergunte o tema ou o nicho.

Se `~/.claude/skills/reels-sem-aparecer/` não existir, diga que a skill principal não está instalada e mostre o comando de
instalação: `curl -fsSL https://raw.githubusercontent.com/Felpborges/reels-sem-aparecer/main/instalar.sh | zsh`
