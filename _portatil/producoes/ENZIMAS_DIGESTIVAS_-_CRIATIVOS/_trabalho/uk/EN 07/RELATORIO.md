# EN 07 - ENZIMAS-DUELO-DE-ENZIMAS-V2 → UK (08/10/2026)

Saída: `UK\EN 07 - ENZIMAS-DUELO-DE-ENZIMAS-V2 - UK.mp4` (720x1280, 30 fps, 90,63 s, igual ao original).

## Quem fala
- Duas pessoas: a creator à esquerda (tiara branca, regata preta) e o creator à direita (o mesmo homem do EN 01).
- A frase trocada é da **creator da esquerda**. A identificação foi feita pela abertura da boca (mediapipe) por frase (`falantes.txt`).
- Ela **não é a mesma creator do EN 01**. Por isso a voz dela foi clonada à parte.

## Frase trocada
| Trecho | Tempo (janela de áudio) | Original | Nova |
|---|---|---|---|
| A | 20,10–24,22 s (quadros 603–726) | "So the food in America is super processed and just like really hard to digest." | "So the food we eat is super processed and just like really hard to digest." |

- As emendas caem em pausa natural: 19,72–20,10 s antes e 24,14–24,30 s depois.
- No EN 07 não há "on here", "grocery store", "$" nem "TikTok" falados. A frase do fim, "I will link where I get these in this video", ficou como está, porque "link" é permitido.

## Voz / TTS
- Voz clonada: **"ENZIMAS UK EN 07 mulher" — voice_id `lVyHshDR1NstCGJZhI0E`**.
  - Fonte: 62 s de fala só dela, tirados da voz isolada pelo demucs.
- Caracteres de TTS: **74**.
- Ajuste: atempo 1,02. A fala dura 4,00 s contra 3,98 s do original.
- Volume:
  - Ganho da voz: +3,1 dB.
  - Mix final: −24,7 contra −24,8 LUFS do original.
- Áudio do trecho: fundo do demucs + voz nova, com crossfade de 30 ms. Fora do trecho, o áudio original está intocado.

## Rosto (HeyGen lipsync)
- Job A `94dc51c6871946baba8b28092fed8ad8`, em `mode speed`, com a entrada recortada só no rosto dela e o áudio original.
  - Duração 4,13 s, cerca de 4,1 créditos estimados. Voltou em cerca de 2 min com 124 quadros exatos.
- A colagem usa elipse na boca e no queixo, com cor exata (desvio < 0,2 em BGR) e crossfade de 2 quadros nas 2 emendas.
- Créditos: veja `..\heygen_log_en01_en07.txt`.

## Índice de lipsync
- A boca mudou em 100% dos quadros.
- Correlação boca × áudio novo 0,27, contra −0,18 com o original.
- **O índice de pausa não pôde ser calculado** porque a fala nova é contínua, sem pausa ≥ 8 quadros. Por isso o revisor dá AVISO.
- Conferência visual quadro a quadro (`cmp_A.jpg`): boca natural, sem pulo nas emendas e cor igual.

## Tela (TikTok)
- As capturas de tela sobrepostas (45,9–49,6 s, quadros 1376–1487) mostravam a **interface do TikTok**. Tudo foi removido:
  - **Barra de status e abas** ("LIVE · Community · Local · Following · Shop · For You", hora, sinal, busca): a faixa do topo da 1ª captura (y 106–168) foi recortada e o fundo do próprio vídeo voltou no lugar. A captura agora começa abaixo das abas.
  - **Selo "Rewards"**, **coluna de ícones** da 1ª captura (avatar com +, coração, comentário, contagem), **ícones da 2ª captura** (avatar com +, coração, comentário, salvar) e uma faixa entre as capturas: apagados com LaMa quadro a quadro (`ov_limpar.py`, `ov.json` + `ov2.json`).
- Conferência quadro a quadro (`chk_ov_final2.jpg`, `z4.png`): sem sobra de interface.
  - Há uma pequena diferença de textura no canto direito da 2ª captura quando a 3ª entra (quadro 1415), quase imperceptível.
- A legenda da captura ("The part with the digestive enzyme is just like,") e a legenda do topo ficaram.

## Revisão
- `revisar_ad.py --lipsync`, pelo PowerShell, com `proibidos.txt`:
  - termos proibidos: nenhum;
  - silêncio, salto de pts e quadros soltos: nenhum;
  - resultado OK, com o aviso de lipsync acima.
- Whisper en no final: em 20,28 s, "So the food we eat is super processed..." e não sobra nada de "America".
- Resolução, fps e duração iguais às do original.

## Pendências
- O índice de pausa ficou sem número (fala contínua). A aprovação foi visual: vale um olhar rápido da pessoa em 20,1–24,2 s.
- Recorte da interface do TikTok nas capturas: a pessoa pode preferir tirar as capturas por inteiro. Hoje elas ficam sem a interface.
- Créditos HeyGen: confirmar no log.
