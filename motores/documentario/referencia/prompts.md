# Prompts que funcionaram no teste (Higgsfield, 13/11/2026)

**Imagem: `gpt_image_2_6`** (0,25 crédito cada; o gerador limita ~8 pedidos simultâneos, mande em lotes de 4-8)

| Uso no D | Prompt (modelo) | Recorte |
|---|---|---|
| sujeito da COLAGEM (P&B) | "Black and white vintage photograph style full-body portrait of <pessoa/época>, three-quarter view, standing, isolated on a pure white seamless background, sharp focus, no text" (2:3) | `ia` + `cinza=True` |
| a UMA cor da colagem | "<objeto ligado à fala> in deep <cor>, photorealistic studio product photo, soft shadow, isolated on a pure white seamless background, no readable text" (1:1) | `ia` |
| multidão de costas | "Wide row of a large crowd of <época> people seen from behind, full bodies with feet visible, black and white vintage photograph, isolated on a pure white seamless background" (3:2) | `ia` |
| a personagem pequena em cor | "Full body <personagem> in an elegant <cor> <roupa da época>, facing the camera, photorealistic, isolated on a pure white seamless background" (2:3) | `ia` |
| documento do DOCUMENTO/DIAGRAMA | "Flat scan of an old <século> handwritten <tipo de documento> page ... faded ink on yellowed paper, full page" (2:3) | imagem cheia |
| objeto branco do ESCURO-OBJETO | "<objeto do dia a dia do espectador>, front three-quarter view, studio product photo, isolated on a pure white seamless background, no logos, no text" | `ia` + `cinza=True` |
| ARQUIVO (foto de época) | "Colorized vintage photograph of <cena>, slightly faded period colors, film grain, documentary archive look" (9:16) | imagem cheia (`pontos=True` se for "guerra/rua") |
| retrato "glamour" (brilhos) | "Oil portrait painting in the style of <época> ... jeweled necklace and diamond earrings ..." (9:16) | imagem cheia + pontos de brilho |
| traço do DIAGRAMA | "Technical black ink line drawing of <máquina/ideia>, patent drawing style, clean thin black lines only on a pure white background, no shading, no text" (2:3) | `traco` |
| objeto da CENA-COR (sobe, fica vermelho e cai) | "A tall vertical <objeto>, photorealistic, studio lighting, isolated on a pure white seamless background" (2:3) | `ia` |
| DESCARTE | sala P&B ("Black and white vintage photograph of a <época> committee room ... perspective down the table") + "A bright green plastic office trash bin ... isolated" + "A large loosely crumpled sheet of white paper forming a rough ball ... isolated" | `ia` |
| FOTO do salto | "A small wooden-framed school chalkboard hanging on a beige plaster wall, with <o conceito> drawn in white chalk, photograph, centered" (9:16) | imagem cheia |
| QUADRO | "An ornate antique gilded baroque picture frame, front view, empty with a plain flat white center, isolated on a pure white seamless background" (3:4) | `moldura` (imprime a janela) |
| CTA | "Cinematic photo of a person seen from behind ... at night working on a glowing laptop" + "Abstract pure black background with flowing silk-like 3D ribbons and thin white edge highlights" (9:16) | imagens cheias |

**Cama: `elevenlabs_music_v2_5`, 45 s, `force_instrumental`** (6,5 créditos):
"Slow emotional cinematic documentary underscore for a history voice-over. A minor, around 70 bpm, felt piano arpeggios over a
warm sustained string pad and soft cello, bass notes moving F, G, A. No drums, no percussion, no vocals. Intimate, mysterious,
nostalgic, steady texture with no big build-ups, sits quietly under narration."
(saiu em fá menor e com mais variação de nível que o original; o caráter — piano/cordas, sem bateria — bate.)

**Voz provisória: `elevenlabs_v4`, voz "Helena" (preset 3c2b83c0-…), stability 0,35** (~2 créditos). Só para os tempos.
