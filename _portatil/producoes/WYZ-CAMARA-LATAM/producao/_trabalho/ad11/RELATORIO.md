# AD 11 — Paródia de documentário de natureza (ES LATAM)

- **Arquivo:** `producao\AD 11 - WYZE-SOLAR-CAM-PAN-DOCUMENTAL-ES-LATAM.mp4`. 41,2 s, 720x1280, 30 fps, 25,6 MB. Decodifica sem erro.
- **Voz:** Damián - Deep, Rich and Resonant (`BPwS5yO6aXvwg8auqNwS`).
  - Voz de catálogo do ElevenLabs, masculina, espanhol latino neutro, grave, no estilo de narrador de documentário. Não houve clonagem.
  - Velocidade 1,0, com as pausas dramáticas mantidas.
- **TTS:** 522 caracteres (~US$ 0,086).
- **HeyGen:** não se aplica (grupo A).
- **Roteiro:** `roteiro_es.txt`. O tom de documentário foi mantido: "Aquí, en su hábitat natural…", "fija a su presa", "su viejo enemigo, la escalera…".

## O que foi cortado ou trocado
- **Fala:**
  - Saiu "shop now at wyze.com". No lugar entrou o CTA "Toca el botón de abajo y pide la tuya", com as setas no "Toca" aos 38,1 s.
  - "The ladder has not been seen in months" virou "la escalera se quedó sin trabajo: a esta cámara no hay que cargarla", conforme a regra do briefing.
- **Gravações** (orig. 9,0–11,4 s e 15,6–18,3 s): a data/hora foi desfocada e o @perfil vertical no canto foi coberto com uma caixa preta sobre a tarja preta.
- **Legenda branca em inglês:** coberta por uma faixa preta opaca (alpha 253) em y 1052–1206, que também cobre a marca na legenda grande e o "Shop now at wyze.com". A legenda nova em espanhol fica dentro da faixa.
- **Ritmo:** as imagens estão em 0,86x para casar com a narração. O fundo (`no_vocals`) foi esticado para a mesma duração.
- **Selo:** não foi colocado. `receita_com_selo.json` está pronta.

## Revisão
- **Whisper es:** bate com o roteiro. Nenhum preço, país, TikTok, link, data comemorativa ou alegação proibida.
- **Whisper en:** só devolve a tradução. Idioma detectado: es (0,99). Não sobrou fala em inglês.
- **Folha 1 quadro/s** (`rev_folha.jpg`) e quadros em tamanho cheio das gravações:
  - nenhuma legenda em inglês, @perfil ou data legível;
  - não há quadro solto (o vídeo é contínuo, sem cortes novos);
  - o fim tem 0,7 s de cauda com música;
  - as setas ficam acima da faixa da legenda.

## Pendências (revisão manual)
- **Pessoas nas gravações:** o casal aparece com o rosto pequeno, mas reconhecível, no take olho de peixe (orig. ~16–18 s). Não foi desfocado. Se quiser zero rosto de terceiro, dá para desfocar.
- **Alegação de sol:** "una hora al día" de sol está nas specs oficiais ("1 hora de sol directo al día").
