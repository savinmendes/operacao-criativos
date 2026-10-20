# AD 18 — Lymphoria "Gotitas día a día" (origem: vídeo 18, Herbalia 3D, 1:30)

## Entregas
- Longo: `producao\AD 18 - LYMPHORIA-GOTITAS-DIA-A-DIA-ES-LATAM.mp4` — 96,1 s, 720x1280, 25,1 MB
- Curto: `producao\AD 18 CURTO - LYMPHORIA-GOTITAS-DIA-A-DIA-ES-LATAM.mp4` — 58,4 s, 720x1280, 23,9 MB

## O que foi feito
- Corte em 81,25 s (depois de "...y su cuerpo drena", antes de "Comprá dos y llévate dos gratis"). Saiu: oferta 2+2, "Garantía de 90 días" com selo, escassez ("se agotan", "este lote") e "link".
- Fim universal (voz clonada do narrador): "Se llama Lymphoria, y sabe a miel. Pides ahora, te llega con envío gratis y pagas al recibir en tu casa. Y tienes noventa días de garantía o te devolvemos tu dinero. Toca el botón de abajo y pide el tuyo." (variante do fim_C sem repetir "gotas bajo la lengua", que o narrador já tinha dito).
- 2 falas trocadas: "Herbalia, cuatro hierbas" → "Lymphoria, cuatro hierbas" (58,6–60,4 s) e "tomando herbalia" → "tomando Lymphoria" (76,95–77,97 s).
- 2 legendas queimadas "herbalia" → "lymphoria" (59 s e 77,6 s).
- Kling O1 Edit (Flora, nós n154/n158/n157): t1 frasco na mão no gancho (0–2,1 s), t2 packshot com ervas (58,9–60,5 s), t3 frasco pequeno à esquerda (63,9–64,9 s; só os 28 primeiros quadros, porque depois o Kling apagou o brilho da cena).
- Curto: 0–31,1 s (gancho + Día 1/2/5) + 46,2–58,5 s ("Esto es lo que nadie te dice… se nota") + o mesmo fim.
- Voz: clone novo "DRENAGEM AD18 narrador" `K30xlzBx7r8q6rKkLEyi` (nenhum clone antigo bateu: semelhança máx. 0,77).

## Custos
- Kling: 3 takes × US$0,706 = US$2,118
- TTS: 204 + 26 + 17 = 247 caracteres (≈ US$0,04)

## Revisão
- Whisper (es) no longo e no curto: nenhum termo proibido (Herbalia, 60 días, link, preço, TikTok etc.).
- Folha de contato 1 quadro/2 s: rótulo Lymphoria nos 3 takes; sem quadro solto (corrigido 1 quadro de "Semana 2" na junção do curto); fim com selo e setas até o último quadro.

## Para revisão manual
- 1:16–1:18 (multidão comemorando): frasco erguido pequeno com o rótulo original; a marca não é legível nesse tamanho, então ficou.
- Mantidos do original: "Semana 2… bajaste de peso", "Miles de personas ya están tomando…", "se absorbe en menos de 60 segundos" e o mascote de jaleco (risco Meta médio, apontado na análise G3).

## Correção 05/10 (bug do encaixar_edit.py: branco copiado fora da faixa da legenda)
- Afetados t1, t2 e t3:
  - t2 tinha letras fantasma no "LYMPHORIA" e uma mancha branca na bolha;
  - t3 tinha uma faixa branca no jato de mel;
  - t1 tinha marcas brancas no rótulo e no contorno.
- Refeito com `encaixar_edit_faixa.py`, depois `processar_ad.py r18.json` e o curto (mesmo trim do parte1 + montar).
- Revisão: decodificação OK; duração igual (96,10 s e 58,40 s); áudio idêntico. Versões antigas em `ad18/_antes_fix_faixa/`.
