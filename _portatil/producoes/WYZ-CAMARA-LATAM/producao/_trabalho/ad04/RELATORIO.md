# AD 04 — Wyze Solar Cam Pan (câmera em poste) — EN → ES LATAM

- **Arquivo:** `producao\AD 04 - WYZE-SOLAR-CAM-PAN-SIN-CARGAR-ES-LATAM.mp4` — 38,70 s, 720x1280, 23,4 MB, decodifica OK.
- **Voz:** Eduardo - Persuasive and Neutral (catálogo, espanhol latino, masculina) — `JjHBC66wF58p4ogebCNA`. Sem clonagem.
- **TTS:** 527 caracteres (~US$ 0,09). Narração com atempo 1,06 (abaixo do teto de 1,1).
- **HeyGen:** não se aplica (Grupo A).

## O que foi cortado ou trocado
- Fala nova (roteiro em `roteiro_es.txt`). **Saíram:** "#1 best-selling… in America", "sold out eight times", "nearly six months / never charged it once", "before they sell out again" e a marca falada.
- "Never needs to be charged" virou "no tienes que cargar". "Hour of sunlight = 100% charge" virou "una hora de sol directo al día, funciona continuo, y la batería la mantiene funcionando de noche y en días nublados" (texto do briefing).
- Entrou o "video dos K" (spec oficial). CTA: "Pídela hoy. Toca el botón de abajo y pide la tuya." Setas no "Toca" (34,96 s até o fim).
- Legenda em inglês (e o "SD" gráfico de ~25 s) cobertos por faixa preta 100% opaca no rodapé (y ≥ 1080 de 1280). Legenda nova pelo alinhamento do ElevenLabs.
- Últimos 1,3 s: quadro final congelado para a fala caber sem acelerar.
- **Sem fundo musical:** o `no_vocals` do demucs (htdemucs e htdemucs_ft) ainda tinha a voz em inglês inteligível para o Whisper ("number one… in America", "sold out eight times"). Para não sobrar inglês por baixo, o fundo original foi retirado: o áudio final é só a narração.
- Sem selo. A receita com selo está pronta em `receita_com_selo.json` (não renderizada).

## Revisão
- Whisper es: bate com o roteiro. Sem preço, país, TikTok, "link", Navidad/año nuevo ou alegação proibida. ("dos K" sai como "2 kappa" no Whisper; a tradução EN o lê como "2K".)
- Whisper en: só a tradução da fala em espanhol; nenhuma fala em inglês original.
- Folha 1/s (`rev\folha.jpg`): nenhuma legenda em inglês visível (faixa medida: brilho máximo 0), setas entre a legenda e a faixa, sem quadro solto. Silêncio no fim: 0,46 s.

## Pendências
- Se quiser música, inserir uma trilha livre (o fundo original não pôde ser usado).
- Relevo WYZE na câmera mantido (permitido).
- Selo "PAGO CONTRA ENTREGA" só depois da confirmação.
