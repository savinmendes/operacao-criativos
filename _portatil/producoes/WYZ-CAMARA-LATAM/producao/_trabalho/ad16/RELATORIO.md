# AD 16 — Wyze Solar Cam Pan · Beneficios · ES-LATAM (Grupo B)

- **Arquivo:** `producao\AD 16 - WYZE-SOLAR-CAM-PAN-BENEFICIOS-ES-LATAM.mp4`. 38,7 s, 720x1280, 25,9 MB. Original: 38,8 s.
- **Voz:** "Juan Carlos - Confident and Upbeat" (catálogo ElevenLabs, salva como "WYZE Juan Carlos"), id `G4IAP30yc6c1gK0csDfu`, 1,0x, `eleven_multilingual_v2`.
- **Caracteres de TTS:** 592 (≈US$0,098).
- **Avatar HeyGen:** "WYZE Review Latino 35" `430f346689b68545f1adbea9f186bd83`. Vídeo `6c17f2794834fa9e7df29c18360d5b10`.
- **Créditos HeyGen:** ~25. São 50 no total com o AD 14 (saldo de 9.071 para 9.021).
- **Estrutura** (apresentação de benefícios): avatar ≈ 61% e takes ≈ 39%:
  - 14,45–17,95 s: instalação na parede, emprestada do AD 14 (mesmo produto, sem rosto);
  - 17,95–22,55 s: gravações da câmera, também do 14, desfocadas e a 0,8x;
  - 22,55–29,3 s: closes do produto do próprio 16 (original 21,3–27,55 s), recortados à esquerda para tirar o rosto do criador e a legenda, a 0,93x.

## O que foi cortado ou trocado
- O criador não aparece em nenhum quadro.
- Saíram "dropped the price", "for that price", "orange shopping cart", "stock out / missed out" (escassez) e "you never have to charge" (virou "no tienes que cargarla", conforme o briefing).
- Os benefícios ficaram só com as especificações oficiais: 360°/70°, panel solar + 1 h de sol, IA de personas, alertas no celular, visão noturna a cor, reflector, áudio bidirecional, sirena 105 dB, 2K, lluvia/polvo e sem suscripción.
- **CTA:** "Pídela hoy. Toca el botón de abajo y pide la tuya." As setas entram no "Toca" (35,7 s).
- **Sem selo.** A versão com selo está em `receita_com_selo.json`.

## Revisão
- **Whisper es:** texto igual ao roteiro. Nenhum termo proibido.
- **Whisper en:** só reconhece o espanhol, sem nenhuma fala em inglês. O original não tinha música (no_vocals a −59 dB).
- **Folha 1 q/s:**
  - sem legenda em inglês, sem rosto do criador e sem quadros soltos;
  - setas abaixo da legenda;
  - o silêncio no fim caiu de 0,87 s para <0,5 s (cauda de 0,25 s).
- **finalizar.py:** decodificação OK.

## Pendências
- Os primeiros 14,4 s são só avatar. O 16 não tem outro take sem rosto: os closes de 0–1,4 s mostram o rosto atrás do painel.
- Dois takes vieram do AD 14 (instalação e gravações). Se quiser os ADs totalmente independentes, troque-os por takes de produto novos.
- Pronúncia de "Wyze" e avatar compartilhado com os ADs 01/12 com outra voz: mesmas observações do AD 14.
