# AD 04 — LYMPHORIA MUJER-28 (origem: originais\04.mp4, 6:19, Maya Verra estilo Pixar)

## Entregas
- Longo: `producao\AD 04 - LYMPHORIA-MUJER-28-ES-LATAM.mp4`. Tem 373,0 s (6:13), 720x1280 e 44,6 MB. Passa de 30 MB: o kit não consegue colocar 6 min em 30 MB sem perder qualidade e escolheu 900 kbps.
- Curto: `producao\AD 04 CURTO - LYMPHORIA-MUJER-28-ES-LATAM.mp4`. Tem 86,9 s, 720x1280 e 23,3 MB.
  - Gancho de 0 a 17,4 s.
  - Mecanismo de 143,97 a 175,25 s: "La miré como una loca… lodo de menopausia… tienes que drenarlos".
  - Prova de 208,93 a 224,1 s: "Semana uno… el globo de mi vientre desapareció".
  - Mesmo fim COD.
- Receita: `_trabalho\r04.json`. Pipeline: `_trabalho\processar_ad04.py`, que é uma cópia do processar_ad.py com mais um passo, `legendas_caixa`.

## Corte e fim
- O corte está em 350,3 s, logo depois de "Fuerte. Despierta. Viva.". Com isso saem do vídeo:
  - "No dejes que te vendan Ozempic u hormonas";
  - "Mayaverra. Cuatro plantas";
  - "Garantía de 60 días";
  - "ya no la necesitarás".
- Usei o fim_A, porque a narração já cita as 4 ervas. Selo COD e setas.

## Rótulo Maya Verra (4 cenas)
- As 4 cenas foram trocadas pelo `band_fix04.py`, sem Kling. É uma versão ajustada do band_fix do ad25, com hue a partir de 18 para pegar a ponta iluminada da faixa e pintura das letras que sobram.
  - 2:00–2:03 (120,0 s, 89 quadros)
  - 2:04–2:07 (124,767 s, 90 quadros)
  - 3:16 (196,367 s, 42 quadros)
  - 5:04 (303,867 s, 48 quadros)
- Kling: 2 takes testados (2:00 e 2:04), US$ 1,412, **descartados**. No 1º o Kling trocou o rosto da mulher; no 2º apagou a personagem do fundo. Nenhum take do Kling está no vídeo, então o bug do encaixar_edit não afeta este AD.
- 2:55 (frasco na mão) e 2:57 (ervas): o rótulo não dá para ler, ficou o original.
- 5:08–5:10, tela do celular com a página MAYAVERRA: desfoquei a tela inteira (`desfocar_regioes`).

## Legenda queimada (caixa branca com texto preto)
O `trocar_texto_tela` do kit não serve para esse estilo, então fiz o `ad04\trocar_legenda_caixa.py`.
- "Levantó el frasco. Mayaverra." → "Levantó el frasco. Lymphoria."
- "el secreto de Brasil, Mayaverra." → "el secreto de Brasil: Lymphoria."
- "Semana cuatro. Seis kilos menos," → "Semana cuatro. La ropa más floja,"
- "Semana cinco. Nueve kilos menos." → "Semana cinco. Me sentía liviana."

## Voz (clone oC03u0lZtYoBEuEwq7B0)
- O narrador é o mesmo do AD 02 antigo: semelhança de 0,966 no resemblyzer. Reutilizei o clone, sem criar voz nova.
- Falas trocadas:
  - p1 "Levantó el frasco: Lymphoria. Cuatro plantas." (reaproveitada do ad02 antigo, 0 caracteres)
  - p2 "El secreto de Brasil: Lymphoria."
  - p3 "Semana cuatro. La ropa más floja, comiendo normal."
  - p4 "Semana cinco. Me sentía liviana."
- TTS: 426 caracteres (p2+p3+p4 = 116, narr_fim = 310), ~US$ 0,07.

## Revisão
- Whisper (es) nos dois vídeos: nenhum "Maya Verra", 60 días, hecho en EE.UU., Ozempic, TikTok, COFEPRIS, cáncer, preço ou link. A marca é ouvida como "linforia". Os únicos "kilos" que sobram são de peso ganho ("15 kilos en 18 meses", "gané 15 kilos"), sem promessa de perda.
- Folhas de contato a cada 2 s:
  - nenhum rótulo Maya Verra legível;
  - celular desfocado;
  - sem cena explícita: a cena da cama em 0:28 é só sugestiva, coberta pelo lençol;
  - sem antes/depois com kg.
- Cortes do curto em fim de frase e em troca de cena. Silêncio no fim: 0,6 s, igual ao padrão do lote.

## Pendente / revisão manual
- O longo tem 44,6 MB (acima de 30 MB).
- A faixa trocada pelo band_fix é lisa, sem o ícone de folha, e a borda fica um pouco serrilhada nas cenas em movimento (2:00 e 2:04). Vale conferir em tela cheia.
- Ficaram, por serem ângulo do criativo ou peso ganho: a médica que desdenha (1:24), "Semana cuatro" com a balança na tela (sem número legível) e "Seis semanas, no te reconocerás".
