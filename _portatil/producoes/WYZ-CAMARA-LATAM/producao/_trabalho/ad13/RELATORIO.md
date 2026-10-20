# AD 13 — Wyze Solar Cam Pan, câmera na cerca (Grupo A)

- **Arquivo:** `producao\AD 13 - WYZE-SOLAR-CAM-PAN-CERCA-ES-LATAM.mp4` — 41,4 s, 720x1280, 25,5 MB, decodifica OK.
- **Voz:** "Juan Carlos - Confident and Upbeat" (`G4IAP30yc6c1gK0csDfu`), a mesma dos ADs 08/10 (`voz_08_10_13.txt`).
- **TTS:** 0 caracteres novos. Reaproveitei a narração do ad08 (`ad08\narr.mp3` + alinhamento), porque o roteiro é o mesmo (`roteiro_08_10_13.txt`).
- **Trocado:**
  - Áudio: voz em inglês substituída. O fundo é o `no_vocals` do demucs (rodou na CPU: o torch não tem CUDA).
  - Legenda em inglês coberta por uma caixa preta opaca (alpha 252, y 1068–1178). A legenda nova em espanhol fica dentro dela.
  - Saíram "sin sol / semanas sin sol", "back in stock / seis meses" e "linked down below".
  - Entraram "1 hora de sol directo al día" e o CTA "Pídela hoy. Toca el botón de abajo y pide la tuya."
  - Setas no "Toca" (38,5 s), acima da caixa.
  - Fim cortado 0,4 s depois da última palavra.
- **Selo:** não aplicado. Ficou pronto em `receita_com_selo.json`.
- **Revisão:**
  - Whisper es: o texto bate com o roteiro. Sem preço, país, TikTok, link ou datas comemorativas.
  - Whisper en: só traduz a fala em espanhol; não sobrou inglês.
  - Folha 1/s (`revisao2\`): nenhuma legenda em inglês vazando. Sem cortes internos, logo sem quadros soltos. Setas fora da legenda. Sem silêncio no fim.
- **Pendências:**
  - O relevo/logo WYZE fica, como o briefing permite.
  - Nada mais a fazer.
