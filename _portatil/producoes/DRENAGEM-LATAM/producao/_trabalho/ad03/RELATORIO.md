# AD 03 — LYMPHORIA MEJOR-AMIGA (ES-LATAM)

**Arquivos**
- Longo: `producao/AD 03 - LYMPHORIA-MEJOR-AMIGA-ES-LATAM.mp4`: 7:24 (444,3 s), 720x1280, 53,9 MB. Passa do teto de 30 MB por causa da duração; o finalizar usou 900 kbps.
- Curto: `producao/AD 03 CURTO - LYMPHORIA-MEJOR-AMIGA-ES-LATAM.mp4`: 1:29 (89,4 s), 23,9 MB.

**Encurtamento (13:37 → 7:24)**
- São 17 trechos do original, cortados em fim de frase. A lista está em `cortes_longo.json` e é gerada por `cortes.py`.
- Saíram estes blocos:
  - "me decía que era normal…";
  - madrinha da filha;
  - "volvería bronceada…";
  - "¿te operaste ahí abajo?";
  - vinho/risadas na festa;
  - "no me tocó ni una vez / la tocó tres veces";
  - o vestido de US$150 no banheiro;
  - o monólogo no espelho (49 anos, "había dejado de luchar…");
  - a confissão longa (Amazon, médica);
  - **o Ozempic e as injeções** (383–392 s);
  - a previsão das 6 semanas;
  - o celular com "COMPRAR";
  - semana 4 e semana 5 (**14 e 19 libras**, as promessas de kg saem junto);
  - o fim inteiro do original: recapitulação, Facebook, Ozempic de novo, escassez, "botón naranja" e **garantia de 60/600 días**.
- A narrativa termina em "…ella me guiñó el ojo" e emenda no fim_A ("La marca que te da esas cuatro hierbas… se llama Lymphoria…").

**Curto**
- Gancho (0–21,5 s).
- Mecanismo: "tú no tienes peso de menopausia… cada toxina… se queda ahí… no es grasa, es desecho… los tienes que drenar".
- Prova: "Miguel me tocó la parte baja de la espalda… no lo había hecho en dos años".
- Fecha com o fim_B, já que no curto as ervas não são citadas antes.

**Rótulo Maya Verra: 0 takes no Kling (US$0)**
- Quatro cenas foram tratadas com `band_fix2.py`. É uma variante do `band_fix` do ad25: detecta a faixa escura por linha, preenche com a cor da própria faixa e escreve LYMPHORIA, com ROI interpolada quando o frasco se move.
- As cenas são 407,1 s (frasco com ervas), 419,0 s (Emilia tira o frasco da bolsa), 420,7 s (close do MAYAVERRA) e 482,9 s (frasco no chão).
- Comandos em `bf/LEIAME.txt`. Conferido quadro a quadro com zoom.
- Mantidos como no original, porque a marca não é legível:
  - frasco pequeno no gancho (~19,8 s);
  - 487–491 s (rótulo "lymphatic drainage", faixa coberta pela legenda);
  - 532 s ("me pasó la botellita", faixa minúscula);
  - 543 s (conta-gotas);
  - 424 s (frasco brilhando na mão).

**Legenda queimada nas emendas**
- A legenda original tem atraso e mostrava frases cortadas no começo de alguns trechos, como "te operaste allá abajo", "de vino tres veces" e "pensando".
- Correção, conforme o caso:
  - caixa da legenda certa colada por cima (`patch_legenda.py`, 12 emendas);
  - ou o primeiro quadro com a legenda certa congelado por 0,3–0,9 s (5 emendas, via `concat_cortes.py`);
  - quadros soltos de troca de cena nas bordas também foram congelados.

**Voz**
- Clone reaproveitado: `XgKboIFsmuyzrgubdI8J`, do AD 16 antigo (mesmo roteiro e mesmo narrador; semelhança com o original de 03 = 0,87 entre os originais).
- TTS: 305 + 282 = 587 caracteres (≈ US$0,10). Nenhuma fala do meio foi trocada: tudo saiu por corte.

**Revisão**
- Whisper (es) nos dois vídeos finais: nenhum "Maya Verra", 60 días, hecho en EE.UU., Ozempic, TikTok, COFEPRIS, câncer, preço ou link. A única garantia é "noventa días".
- Folha de contato a cada 2 s, mais 1 s no miolo dos frascos: rótulo legível só LYMPHORIA, sem cena sexual, sem antes/depois com kg, fim sem silêncio (−20 dB médio nos últimos 3 s).
- O decode do finalizar deu OK.

**Pendências / revisão manual**
- O longo tem 53,9 MB: acima de 30 MB, mas aceito pelo kit para vídeo longo.
- Ficou "Me dijo, mi hermana María me enseñó algo allá" logo depois de "Emilia no dijo nada por un minuto entero" (corte do Ozempic). Funciona, mas é uma emenda seca.
- Ver com áudio as emendas congeladas (1:08, 1:59, 3:41, 6:26).
- O fundo de 2 "patches" de legenda pode ser notado por 0,3 s se alguém procurar.
