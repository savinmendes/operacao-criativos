# AD 08 — Wyze Solar Cam Pan (EN → ES LATAM)

- **Arquivo:** producao$ARQ — 41,7 s, 720x1280, ~25 MB, decodifica OK.
- **Roteiro:** ad08\roteiro_es.txt (o mesmo de 08/10/13, em _trabalho\roteiro_08_10_13.txt).
- **Voz:** ElevenLabs catálogo "Juan Carlos - Confident and Upbeat" (latino, masc.), id G4IAP30yc6c1gK0csDfu, eleven_multilingual_v2. Mesma voz nos 08/10/13 (anotado em _trabalho\voz_08_10_13.txt).
- **TTS:** 608 caracteres (~US$0,10), gerado uma vez em ad08\narr.mp3 e reaproveitado no 10. Velocidade 1,0x (sem aceleração).
- **HeyGen:** não usado (grupo A).

## O que foi trocado / cortado
- Voz em inglês removida (demucs --two-stems=vocals, CPU porque o torch não tem CUDA); usado só o no_vocals.wav como fundo.
- Saiu da fala: "world's easiest", "100% solar", "no need sunlight", "multiple weeks without sunlight", "linked it down below", "back in stock for the first time in six months". "Smart home devices" (Alexa/Echo, fora das especificações oficiais) trocado por controle pelo celular.
- Entrou: "Con una hora de sol directo al día le basta, y la batería la mantiene funcionando de noche y en días nublados"; "no tienes que cargarla"; CTA "Pídela hoy. Toca el botón de abajo y pide la tuya." (setas no "Toca", 38,6 s).
- Fim cortado em 41,7 s (~0,6 s após a última palavra, fade de 0,3 s); o trecho final original (≈42–43,8 s) saiu.
- Tela do Echo Show com "Wyze Cam Outdoor v3" (16,5–19,5 s) mantida (marca permitida); a fala nesse trecho é "hacia arriba y hacia abajo, siguiendo a las personas".
- Faixa preta (alpha 252) em y 958–1102 cobre a caixa de legenda em inglês o vídeo todo; legenda nova dentro dela (y 1545 em 1080). Setas abaixo da faixa (cta.y 1680).
- Selo: NÃO colocado. Pronto em ad08\receita_com_selo.json ("PAGO CONTRA ENTREGA · ¡PAGAS AL RECIBIR!", a partir de 37,4 s).

## Revisão
- Whisper es: texto bate com o roteiro; nenhum preço, país, TikTok, link, Navidad/año nuevo, estoque, "sin sol" ou "100%". O nome sai como "Wise Solar Campaign" no Whisper (o mesmo acontecia no original em inglês) — é o "Wyze Solar Cam Pan" da voz.
- Whisper en: só devolve a tradução da fala em espanhol; nenhuma frase do original em inglês sobrou por baixo.
- Silêncio no fim (−45 dB, ≥0,7 s): nenhum.
- Folha 1 q/s (ad08\folha_final.jpg): nenhuma legenda em inglês visível, sem cortes internos (vídeo contínuo), setas fora da legenda.

## Pendências
- Confirmar com o fornecedor/loja as especificações faladas (360°, seguimento de pessoas, microSD, sem assinatura, 1 h de sol).
- Decidir se entra o selo de pagamento contra entrega (usar receita_com_selo.json com montar_ad.py).
- Texto do anúncio (.txt) não foi pedido neste lote.
