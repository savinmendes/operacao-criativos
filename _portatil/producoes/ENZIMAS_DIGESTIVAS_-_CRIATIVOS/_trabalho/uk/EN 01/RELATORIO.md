# EN 01 - ENZIMAS-DUELO-DE-ENZIMAS → UK (08/10/2026)

Saída: `UK\EN 01 - ENZIMAS-DUELO-DE-ENZIMAS - UK.mp4` (720x1280, 30 fps, 97,01 s, igual ao original).

## Quem fala
- Duas pessoas: a creator à esquerda (roupão, adesivos dourados nos olhos) e o creator à direita.
- As duas frases trocadas são da **creator da esquerda**. A identificação foi feita pela abertura da boca (mediapipe) por frase (`falantes.txt`).
- A creator do EN 01 **não é a mesma** do EN 07, que tem outra mulher (de tiara) e o mesmo homem. Por isso foi clonada uma voz por vídeo, cada uma da creator que fala. A voz do homem não foi clonada porque ele não diz nenhuma frase trocada.

## Frases trocadas
| Trecho | Tempo (janela de áudio) | Original | Nova |
|---|---|---|---|
| A | 25,66–31,72 s (quadros 770–951) | "The food in America is just like super processed and hard to digest, which is why you're looking like six months pregnant after eating." | "The food we eat is just like super processed and hard to digest, which is why you're looking like six months pregnant after eating." |
| B | 85,74–90,40 s (quadros 2572–2711) | "They're doing like a big sale on here right now, too. So it's cheaper than you can even get it in the grocery store." | "They've got like a big sale on right now, too. So it's cheaper than you can even get it in the shops." |

- As emendas caem em pausa natural, medida no envelope da voz isolada:
  - A: há um respiro de cerca de 0,15 s entre "eat." e "The"; a frase termina numa pausa real até 32,1 s.
  - B: pausa entre "bloating." e "They're"; depois da frase há uma pausa até "OK, that's nuts".
- No trecho A a frase inteira foi refeita (até "after eating"), para a emenda cair numa pausa real. A segunda metade usa as mesmas palavras do original.
- Fica a repetição "...all the food we eat. The food we eat is...", que vem da troca aprovada no briefing.

## Voz / TTS
- Voz clonada: **"ENZIMAS UK EN 01 mulher" — voice_id `5qBMWyZj9vdMRyfDtJd6`**.
  - Fonte: 57 s de fala só dela, tirados da voz isolada pelo demucs (`amostra_voz_mulher.wav`).
- Caracteres de TTS: A 131 + B 101 = **232**.
- Ajustes:
  - A: sem atempo. A fala dura 5,87 s contra 5,94 s do original.
  - B: atempo 0,95, de 4,11 para 4,33 s, contra 4,40 s do original.
- Volume:
  - Ganho da voz: A +0,3 dB, B +3,4 dB, para igualar a voz isolada original em LUFS.
  - Mix final: A −30,1 contra −30,1 LUFS do original; B −26,7 contra −26,5.
- Áudio do trecho: fundo do demucs (`no_vocals`) + voz nova, com crossfade de 30 ms. Fora dos trechos, o áudio original está intocado.

## Rosto (HeyGen lipsync)
- `create_lipsync` em `mode speed`, cfr, sem duração dinâmica. Entrada recortada só no rosto da creator (360x640 → 720x1280), com o áudio ORIGINAL do trecho e a voz nova como `audio`.
- Jobs:
  - A `daf2ae58c502457299088509212f8ae3`: 6,07 s;
  - B `2b3c4e66db994c8d9b6a1d89f30034c0`: 4,67 s.
  - Os dois voltaram em cerca de 2 min, com o número exato de quadros (182 e 140).
- A colagem de volta usa elipse na boca e no queixo, com cor exata (`comum3`; desvio medido < 0,3 em BGR) e crossfade de 2 quadros nas 4 emendas, nenhuma delas em corte de câmera.
- Créditos: veja `..\heygen_log_en01_en07.txt`. A estimativa pela duração dos jobs é de cerca de 10,7 créditos (~1 crédito/s em speed).

## Índice de lipsync (`checar_lipsync.py` / `revisar_ad.py --lipsync`)
- A:
  - boca mudou em 100% dos quadros;
  - correlação boca × áudio novo 0,33, contra 0,18 com o original.
- B:
  - boca mudou em 100% dos quadros;
  - correlação 0,42, contra 0,27 com o original.
- **O índice de pausa não pôde ser calculado** porque as falas novas são contínuas, sem pausa ≥ 8 quadros. Por isso o revisor dá AVISO e não APROVADO. É o mesmo caso do s08 do AD 01.
- Conferência a olho, na folha de quadro a quadro das emendas e do meio (`cmp_A.jpg`, `cmp_B.jpg`):
  - boca natural, sem pulo nas emendas e cor igual;
  - no trecho B, ela vira de perfil (2580–2595) e o resultado continua bom.

## Tela (TikTok)
- A primeira captura de tela sobreposta (51,8–55,7 s, quadros 1556–1668) tinha um pedaço do selo **"Rewards" do TikTok** na borda esquerda.
  - Foi apagado com LaMa quadro a quadro (`ov_limpar.py` / `ov.json`); veja `ov_antes_depois_x.jpg`.
- A legenda da captura ("the part with the digestive enzyme is just like,") é conteúdo e ficou.
- Não há $, EUA, carrinho laranja nem @ na tela.
- A legenda do topo ("Seeing if these ACTUALLY work... (no cuts)") ficou.

## Revisão
- `revisar_ad.py --lipsync`, pelo PowerShell, com `proibidos.txt` (America, American, TikTok, tik tok, dollar, $, orange, grocery store, on here):
  - termos proibidos: nenhum;
  - silêncio, salto de pts e quadros soltos: nenhum;
  - resultado OK (só os avisos de lipsync acima).
  - Relatório em `rev\`.
- Whisper en no final: a fala bate com o roteiro novo e não sobra nada da frase antiga. Em 87,96 s: "They've got like a big sale on right now too. ...it's cheaper than you can even get it in the shops."
- Resolução, fps e duração iguais às do original: 720x1280, 30 fps, 97,01 s.

## Pendências
- O índice de pausa ficou sem número (fala contínua). A aprovação foi visual: vale um olhar rápido da pessoa nos trechos 25,7–31,7 s e 85,7–90,4 s.
- Créditos HeyGen: confirmar no log, porque a cobrança atrasa e há outros agentes usando o HeyGen em paralelo.
