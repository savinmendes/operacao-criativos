# EN 02: ENZIMAS-TRUQUE-6-MESES-GRAVIDA, versão Reino Unido (piloto, 08/10/2026)

**Entrega:** `UK\EN 02 - ENZIMAS-TRUQUE-6-MESES-GRAVIDA - UK.mp4`
- 720x1280, 30 fps, 120,00 s: igual ao original (3600 quadros).
- Áudio AAC 128k a 44,1 kHz, 35,1 MB. O original tem 17 MB; a diferença vem da re-codificação em crf 18.

## Frases trocadas
| # | Janela trocada (s / quadros) | Antes | Depois |
|---|---|---|---|
| A | 53,70–56,73 (q 1611–1701) | "It's actually just **the American** food system, freaking ruined our food." | "It's actually just **our modern** food system, freaking ruined our food." |
| B | 111,37–120,00 (q 3341–3599) | "They have thousands of reviews you can look at and I just saw **their by far cheapest on TikTok** right now, like cheaper than **you can get them in the grocery store**. So I'll put the link **in this video** if they still have some in stock." | "They have thousands of reviews you can look at, and I just saw **they're on offer** right now, like cheaper than **in the shops**. So I'll put the link **below** if they still have some in stock." |

**Emendas em pausa natural da voz (medidas na voz isolada pelo demucs):**
- 53,70 s, entre "fault" e "It's";
- 56,73 s, numa pausa de 0,49 s antes de "And now";
- 111,37 s, entre "this is the stuff" e "They have".

**Encaixe no tempo:**
- A: a fala nova dura 2,88 s (TTS + atempo 1,04), contra 2,73 s no original.
- B: a fala nova dura 8,42 s (TTS + atempo 1,05), contra 8,45 s no original.
- "They have thousands of reviews you can look at" foi regerado com o texto idêntico, para a emenda de B cair numa fronteira de frase.

**Correção feita durante o trabalho:** na 1ª versão do trecho A, a emenda caiu em 53,37 s e cortava o "fault" de "it's not your fault". Refiz o trecho:
- emenda nova em 53,70 s;
- novo job de lipsync;
- o whisper confirma "it's not your fault. It's actually just our modern food system".

## Voz
- Clone ElevenLabs "ENZIMAS UK EN 02 creator", **voice_id `rnyHtBhQLcSaNXnn1yy9`**. Base: a voz isolada (demucs) de 0 a 111 s.
- TTS com eleven_multilingual_v2, velocidade 1,1. **Caracteres: 251** (A = 68, B = 183), dentro do limite de 600.
- **Áudio dos trechos:** fundo do demucs (no_vocals) + voz nova.
- **Fora dos trechos:** áudio original intocado, com crossfade de 30 ms nas emendas.
- **Volume:** voz nova A −23,2 LUFS contra −23,3 do original; B −23,7 contra −23,5.

## Rosto / lipsync (HeyGen)
- **Lipsync foi necessário:** a boca da creator aparece nos dois trechos.
- **Parâmetros:** `create_lipsync` com `mode speed`, sem dynamic duration, cfr e keepTheSameFormat.
- **Entrada:** recorte 9:16 (360x640 → 720x1280) que segue o rosto quadro a quadro, com o áudio ORIGINAL do trecho; a voz nova foi enviada como `audio`.
- **Colagem:** elipse na boca e no queixo, com cor exata (`comum3.py`). O desvio de cor medido foi de ≤ 0,2 nível.
- **Emendas:** crossfade de 2 quadros.
- **Jobs:**

  | Trecho | Job | Situação |
  |---|---|---|
  | A v1 (3,33 s) | 09711d26… | descartado (emenda errada) |
  | B (8,63 s) | eab5daf6… | usado |
  | A v2 (3,03 s) | e04052e8… | usado |

  Total de 15,0 s em speed. Todos voltaram em menos de 2 min, com o número exato de quadros.
- **Créditos HeyGen:**
  - saldo antes: 8797;
  - saldo logo após o último job: 8797 (a cobrança atrasa);
  - estimativa: ~15 créditos, a ~1/s em speed. Teto: 40.
  - **Pendente: reconferir o saldo cerca de 1 h depois.**
- **Índice de pausa:** não calculável. A fala nova é contínua, sem pausa ≥ 8 quadros nos dois trechos.
  - Critério alternativo do `checar_lipsync`:
    - A: a boca mudou em 99% dos quadros; correlação boca × áudio novo de 0,40 contra 0,45 com o original.
    - B: a boca mudou em 94% dos quadros; correlação boca × áudio novo de 0,34 contra 0,12 com o original.
    - Resultado: AVISO nos dois, pelo motivo "sem pausa".
  - Conferência a olho, na folha de 1 em 1 quadro e com zoom na boca:
    - a boca articula de forma natural;
    - não há pulo de imagem nem de cor nas emendas;
    - as mãos que passam na frente do rosto em B (111,7–113,5 s) ficaram intactas.

## Tela
- **111,43–113,47 s, print de avaliações** (layout de loja do TikTok Shop, sem logo): apagado o país **"United States"** ao lado de cada autor.
  - Método: o script `painel.py` acha a linha do autor pelo avatar e deixa branco o texto cinza depois do nome.
  - Foram junto as datas e o "Verified purchase" das mesmas linhas.
  - Restam pequenos restos de pixels claros na borda inferior do painel, ilegíveis.
- **0–6 s:** não há carrinho, @, marca d'água, $ ou "TikTok" escrito em nenhum quadro.

## Revisão
`revisar_ad.py --lipsync`, rodado pelo PowerShell com o modelo whisper medium em en:
- decodificação OK e 720x1280 a 30 fps;
- pts do áudio sem saltos;
- sem silêncios longos e sem quadro solto;
- termos proibidos: **nenhum** (America, American, TikTok, dollar, "$", orange, grocery store, on here);
- a transcrição final bate com o roteiro novo, sem sobra da frase antiga;
- resultado: **OK, nenhum problema**. Os 2 avisos são de lipsync "sem pausa", conferidos a olho.
- O aviso "setas (vermelho)" é falso positivo: é o rótulo do frasco.

## Pendências / precisa de revisão manual
1. **Saldo HeyGen:** reconferir com `get_current_user` cerca de 1 h depois. O consumo esperado é de ~15 créditos (~9 do trecho B e ~3 de cada job do A, contando o A descartado).
2. **"Reply to Allison's comment":** o adesivo de resposta a comentário (0–6 s) foi mantido. É um estilo de UI do TikTok, mas não tem logo e o Instagram tem um equivalente. A pessoa decide se cobre.
3. **Print de avaliações:** o layout de loja do TikTok Shop foi mantido (botões "fast delivery", "Reset filters" em rosa, "Reply from seller"); só o país foi apagado. Se for preciso tirar qualquer UI de TikTok Shop, a saída é substituir o print por outro de avaliações.
4. **Preço:** o EN 02 não fala preço, então não há "under twenty pounds" a confirmar neste vídeo.
5. **Legenda queimada:** não há legenda da fala no vídeo, só o título "Seeing if these ACTUALLY work (no cuts)". Nada a trocar.
6. **Tamanho do arquivo:** 35 MB contra 17 MB do original. Se precisar, dá para re-codificar em crf 21–22.
