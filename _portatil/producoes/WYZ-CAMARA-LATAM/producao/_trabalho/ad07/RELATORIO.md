# AD 07 — Montagem de gravações (ES LATAM)

- **Arquivo:** `producao\AD 07 - WYZE-SOLAR-CAM-PAN-GRABACIONES-ES-LATAM.mp4`. 41,6 s, 720x1280, 30 fps, 15 MB. Decodifica sem erro.
- **Voz:** Eduardo - Persuasive and Neutral (`JjHBC66wF58p4ogebCNA`). Voz de catálogo do ElevenLabs, masculina, espanhol latino neutro, com energia de anúncio. Não houve clonagem. Speed 1,08 no ElevenLabs. Pausas acima de 0,38 s foram encurtadas para 0,28 s, sem atempo.
- **TTS:** 1.123 caracteres (~US$ 0,185):
  - 576 caracteres na v1, descartada porque "I A" ficou arrastado e o texto ficou longo;
  - 547 caracteres na versão final.
- **HeyGen:** não se aplica (grupo A).
- **Roteiro:** `roteiro_es.txt`.

## O que foi cortado ou trocado
- **Fala:**
  - Saíram "best-selling camera on TikTok", "stocking stuffer", "get them before they sell out", "shopping cart bottom left" e "no more false alerts".
  - O CTA novo é "Pídela ahora. Toca el botón de abajo y pide la tuya." As setas entram no "Toca", aos 37,7 s.
- **Takes cortados:**
  - Halloween com pessoas fantasiadas (orig. 6,0–10,6 s).
  - Close nítido do rosto de um homem à noite (orig. 21,9–22,8 s).
  - FedEx inteiro (orig. 35,2–39,4 s).
- **Desfoque:**
  - Data/hora em todas as gravações.
  - Logo e telefone do caminhão CWD, com caixa que acompanha o caminhão.
- **Legenda em inglês:** coberta por uma faixa preta opaca (alpha 253) em y 952–1102. A legenda nova em espanhol fica dentro da faixa, com Wyze, 360 e 2K escritos corretamente.
- **Ritmo:** as imagens estão em 0,84x (câmera lenta leve) para casar com a narração. O fundo é o `no_vocals` do demucs.
- **Selo:** não foi colocado. `receita_com_selo.json` está pronta com "PAGO CONTRA ENTREGA".

## Revisão
- **Whisper es:** bate com o roteiro. Nenhum preço, país, TikTok, link, Natal/ano novo ou alegação proibida. ("Wwise Solar Campan" é só como o Whisper escreveu a marca.)
- **Whisper en:** só devolve a tradução da fala em espanhol. Idioma detectado: es (1,00). Não sobrou fala em inglês.
- **Folha 1 quadro/s** (`rev_folha.jpg`) e bordas dos cortes (`bordas.jpg`):
  - nenhuma legenda em inglês nem borda roxa aparecendo;
  - nenhum quadro solto nos cortes;
  - o fim tem 0,6 s de cauda com música (sem silêncio);
  - as setas ficam abaixo da faixa da legenda.

## Pendências (revisão manual)
- **Halloween de fundo:** as abóboras vermelhas no gramado e a decoração de "fantasma" no tronco (borda direita) continuam nos takes de dia e no carro com luz vermelha. São menos evidentes e foram mantidas para não ficar sem imagem. Se incomodar, dá para cortar o take do carro vermelho (orig. 12,1–14,6 s) ou desfocar a borda direita.
- **Van da Amazon:** aparece pequena ao fundo no take de dia (orig. ~15 s).
- **Pessoas:** as das gravações são pequenas ou de costas. Não há rosto nítido.
