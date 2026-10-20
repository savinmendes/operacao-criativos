# Relatório: vencedor A ("DEVOLVER"), Podadora COD Chile (08/10/2026)

**Origem:** `AD 04 - PODADORA-INALAMBRICA-DEVOLVER-ES-CL.mp4` (56,1 s, 720x1280), feito a partir de `original_04.mp4`.
**Voz:** clone do narrador do AD 04 (narrador B, o mesmo dos ADs 03/04), voice_id `BgvvJ0I0R4tg6uf8DolY`, `eleven_multilingual_v2`.

## Ponto de corte (regra: corpo e CTA intactos)
- No AD 04, o gancho original vai de 0 a 9,0 s. É a câmera da porta, sem fala, com a caixa "Bueno… creo que ya no la puedo devolver" de 0 a 6,1 s.
- A narração começa em 9,046 s com "Quien inventó esto merece un aumento.", que é a primeira frase do corpo.
- **Corte em 9,000 s.** Ele cai em fim de bloco (antes da 1ª palavra do corpo) e dentro da mesma tomada contínua da câmera da porta.
- Em cada variação, o AD 04 entra **de 9,0 s até o fim, sem nenhuma alteração** de imagem, legenda, selo, setas ou áudio. A única mudança é a recodificação final para caber em 30 MB.
- **Música do gancho:** é o próprio áudio do AD 04 nos Hd segundos anteriores a 9,0 s (ali só há música, o `no_vocals` do original). Por isso a trilha emenda sem pulo.
- **Fala do gancho:** o volume foi igualado ao LUFS da voz do corpo.
- **Visual do gancho:** tomadas do `original_04.mp4`, a faixa do aviso em espanhol do AD 04 (cobre o aviso em inglês) e uma caixa branca grande (Poppins Bold 46, cy 470). A caixa cobre a frase em inglês queimada na câmera da porta. A legenda é no mesmo estilo drop do corpo, com 1 palavra amarela.
- **Script:** `PODADORA-CL\_vencedores\A\montar_gancho.py`. Ele reproduz qualquer variação com `python montar_gancho.py A3`.

## Entregas (`PODADORA-CL\VENCEDORES\`)

| Arquivo | Gancho (narração / texto na tela) | Cenas do gancho (tempo no original_04) | Gancho | Total | MB |
|---|---|---|---|---|---|
| `A0 - DEVOLVER-1080.mp4` | AD 04 sem mudança. Real-ESRGAN 2x (GPU local), reduzido para 1080x1920, áudio copiado do AD 04 | — | — | 56,1 s | 27,3 |
| `A1 - DEVOLVER-ESPOSO-ES-CL.mp4` | "Mi esposo me dijo que la devolviera… ahora no me la quiere soltar." / ¿DEVOLVERLA? NI LOCA 😅 | Câmera da porta: caixa chegando (1,0–2,4) → máquina cortando o mato alto (6,27–9,0, emenda contínua no corpo) | 4,13 s | 51,2 s | 26,3 |
| `A2 - DEVOLVER-OTRA-COMPRA-ES-CL.mp4` | "Pensé que era otra compra de internet que iba a terminar guardada… me equivoqué." / OTRA COMPRA MÁS… 🙄 | Câmera da porta 0,3–5,23: caixa chegando e sendo aberta, zoom lento 1,0→1,2 | 4,93 s | 52,0 s | 26,4 |
| `A3 - DEVOLVER-UNA-PASADA-ES-CL.mp4` | "Una pasada… y el pasto que me llegaba a la rodilla desapareció." / UNA SOLA PASADA | Close do mato alto sumindo, só pernas (27,6–29,6) → câmera da porta cortando o mato (6,33–9,0, emenda contínua) | 4,67 s | 51,8 s | 26,0 |
| `A4 - DEVOLVER-INALAMBRICO-ES-CL.mp4` | "Nadie me creía… que esto era inalámbrico." / SIN CABLES. SIN BENCINA. | Mesa com as 2 baterías 21V e as rodas, só mão (35,85–37,25) → máquina com rodas cortando sem cabo, só pernas (24,6–26,6) | 3,40 s | 50,5 s | 26,3 |
| `A5 - DEVOLVER-JARDINERO-ES-CL.mp4` | "El jardinero me cobraba cada mes… ahora lo hago yo en diez minutos." / ADIÓS JARDINERO | Corte no caminho de pedra junto ao canteiro (21,35–23,85) → corte ao lado do canteiro de plantas (24,6–26,83), sem rosto | 4,73 s | 51,8 s | 26,1 |
| `A6 - DEVOLVER-LLEGO-AYER-ES-CL.mp4` | "Me llegó ayer… y ya limpié todo el patio." / LLEGÓ AYER 📦 | Câmera da porta: caixa chegando (1,0–2,4) → mesma câmera com o gramado já cortado (11,9–13,7) | 3,20 s | 50,3 s | 26,4 |

Todas as variações saem em 720x1280, 30 fps, H.264 high e AAC 48 kHz. O corpo não teve a resolução aumentada.

**Rostos:** nenhum gancho mostra rosto falando. A moça de macacão (49,9–56 s do original) **não** aparece em nenhum gancho; ela segue só no CTA do corpo original. Na câmera da porta aparece de longe o entregador, que é quem abre a caixa e corta o mato, sem falar.

## Custo de TTS (ElevenLabs, ~US$ 0,165 / 1.000 caracteres)
- **Ganchos finais:** 66 + 80 + 63 + 41 + 67 + 41 = 358 caracteres ≈ **US$ 0,059**.
- **Refeitos:** A4 e A6 foram refeitos uma vez (+80 caracteres ≈ US$ 0,013), porque a 1ª versão tinha só 2,4 e 2,6 s de fala, abaixo do mínimo de 3 s.
  - A 2ª versão tem pausa "…" no meio e velocidade 0,9, sem mudar nenhuma palavra.
  - As versões descartadas ficaram em `_vencedores\A\voz\v1\`.
- **Total gasto:** 438 caracteres ≈ **US$ 0,072**.
- HeyGen: US$ 0.

## Revisão
- **`revisar_ad.py`:** rodado pelo PowerShell nos 7 arquivos, com `--idioma es --idioma-residual en --passo 1`. Os termos proibidos ficam num .txt em UTF-8: `_vencedores\A\proibidos.txt`. Ele cobre preço/moeda, "gratis" fora de "despacho gratis", garantia além dos 90 días confirmados, TikTok e link/enlace.
  - **Resultado:** os 7 deram **OK, nenhum problema** (exit 0). Nenhum termo proibido, nenhum quadro solto, nenhum salto de áudio. As setas estão no fim e não ficam em cima da faixa.
  - O whisper transcreve o gancho certo em todas e emenda direto em "Quien inventó esto merece un aumento.": nenhuma frase cortada.
  - Relatórios: `_vencedores\A\revisao\*_revisao.txt/.jpg`.
- **Folha de 1 em 1 quadro na emenda gancho→corpo** (`_vencedores\A\revisao\A1..A6_emenda_1a1.jpg`, 24 quadros em volta do corte):
  - A emenda é limpa, sem quadro solto ou repetido.
  - Em A1 e A3 o gancho termina na mesma tomada da câmera da porta em que o corpo começa, então a imagem não pula.
  - A caixa do gancho some exatamente no corte, e a legenda do corpo entra 1–2 quadros depois, com "QUIEN".
- **A0:** comparado quadro a quadro com o AD 04 (1.681 quadros nos dois, SSIM 0,98 no trecho final). Está alinhado e sem nenhuma mudança de conteúdo.

## Pontos de atenção (revisão manual opcional)
- **A2:** a caixa é desenhada antes do zoom, então cresce junto com a cena. Isso foi necessário para continuar cobrindo a frase em inglês da câmera, que também se move com o zoom.
- **A6:** o "pátio limpo" é o fim da própria câmera da porta (gramado já em boa parte cortado). Logo depois, o corpo volta à mesma câmera em 9,0 s, ainda cortando. É uma volta no tempo dentro da mesma câmera, aceitável para AD, mas perceptível.
- **Cenas repetidas:** as tomadas do gancho vêm do próprio vencedor, então reaparecem mais adiante no corpo (A3 aos ~27 s, A4/A5 aos ~21–27 s). Isso não tem como evitar sem material novo.
- **Silêncio no fim:** os 0,8 s finais de silêncio já existem no AD 04 original e foram mantidos, pela regra do corpo intacto.
- **Marca SEESE:** continua visível nas baterias (A4) e na própria máquina, como no AD 04.
