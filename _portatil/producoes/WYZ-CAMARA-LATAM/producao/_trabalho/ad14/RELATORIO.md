# AD 14 — Wyze Solar Cam Pan · Garaje · ES-LATAM (Grupo B)

- **Arquivo:** `producao\AD 14 - WYZE-SOLAR-CAM-PAN-GARAJE-ES-LATAM.mp4`. 52,7 s, 720x1280, 26,2 MB. Original: 62,8 s.
- **Voz:** "Gerardo - Cool Latin American voice" (catálogo ElevenLabs, salva na conta como "WYZE Gerardo"), id `NDcVpQJv7Naa7ZKrqtEk`, velocidade 1,05x, `eleven_multilingual_v2`.
- **Caracteres de TTS:** 755 no final (≈US$0,125). Houve também 880 de uma 1ª versão de 69 s, longa demais e descartada (≈US$0,145).
- **Avatar HeyGen:** "WYZE Review Latino 35" `430f346689b68545f1adbea9f186bd83`, criado pelo agente dos ADs 01/12, com lipsync do áudio do ElevenLabs. Vídeo `1a3b590921e9b0f606693f5c6a4c839e`.
- **Créditos HeyGen:** ~25. O saldo foi de 9.071 para 9.021 com os ADs 14 e 16 renderizados juntos, e outros agentes podem ter gastado no mesmo intervalo.
- **Estrutura:** avatar ≈ 66% e takes do original sem rosto ≈ 34%:
  - 5,3–13,0 s: gravações da câmera sobre as mãos;
  - 28,0–37,4 s: instalação na parede e gravações.

## O que foi cortado ou trocado
- O criador não aparece em nenhum quadro. A fala é toda do avatar e não há lipsync no criador real.
- Saíram "deals for the new year", "link" e "best selling".
- "Three foot cable" virou "cable de tres metros".
- "Una semana de batería con el panel cubierto de nieve" virou a frase-padrão: "la batería la mantiene funcionando de noche y en días nublados" (mais "1 hora de sol directo").
- **Assinatura:** "Graba en microSD y no necesita suscripción; la suscripción es opcional."
- **CTA:** "Pídela hoy. Toca el botón de abajo y pide la tuya." As setas entram no "Toca" (49,8 s).
- **Legenda em inglês:** eliminada por recorte dos takes, que cortam a faixa da legenda e o topo com o cabelo do criador. Não foi preciso usar faixa.
- **Rostos de terceiros:**
  - as gravações em 9,7–17,4 s e 34,95–38,6 s do original estão desfocadas (gblur σ5 no quadro inteiro da gravação);
  - o trecho 32,8–34,9 s foi **cortado**: um menor de idade aparece em tela cheia, de costas.
- **Takes:** os de instalação e gravação rodam a 0,85x para cobrir a fala.
- **Sem selo.** A versão com selo está pronta em `receita_com_selo.json` ("PAGO CONTRA ENTREGA").

## Revisão
- **Whisper es:** texto igual ao roteiro. Nenhum termo proibido (preço, país, TikTok, link, Navidad/año nuevo, descuento, stock, garantía, envío).
- **Whisper en:** só a tradução da fala em espanhol, sem nenhum resto de áudio em inglês. Não sobrou música nem fala original: o fundo do original era só voz, com no_vocals a −49 dB, então não usei trilha.
- **Folha de contato 1 q/s** (`revisao\folha_1s.jpg`): nenhuma legenda em inglês, nenhum quadro do criador, nenhum quadro solto nos cortes, setas abaixo da legenda e sem silêncio ≥0,5 s no fim.
- **finalizar.py:** decodificação OK.

## Pendências
- Whisper ouve "Wyze" como "Waze/Wise", ou seja, pronúncia "uaiz". Aceitável, mas vale ouvir.
- O avatar é o mesmo dos ADs 01/12, que usam outra voz ("Mario"). Segui a regra de uma voz por criador original. Se a mesma "pessoa" com 2 vozes incomodar nos anúncios, refaça o TTS com `tomkxGQGz4b1kE0EM722` (~US$0,13 mais ~25 créditos).
- Há 15 s seguidos de avatar (13–28 s): não há mais takes sem rosto no original.
- A marca d'água WYZE e o carimbo de data nas gravações ficaram desfocados junto com a gravação. A marca é permitida.
