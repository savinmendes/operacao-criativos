# V12 → Lymphoria (Chile) — RUTINA 30 SEGUNDOS

- **Final:** `ADLIB-VITALY-CL\LYMPHORIA-ES-CL\V12 - LYMPHORIA-RUTINA-30-SEGUNDOS.mp4` (77,2 s, 720x1280, 23,9 MB).
- **Origem:** `VIDEOS\12 - Mi Camino al Bienestar - 1313049140654830.mp4` (720x1280, 70,4 s), narração em off, sem rosto falando. Sem upscale.
- **Estrutura:** parte 1 = original 0–64,47 s (corte depois de "…drenaste litros de líquido que sobraban") tratada + fim Lymphoria novo (12,6 s).

## Trocas (TROCAS)
| Início (s) | Fim (s) | Original | Novo | Tipo |
|---|---|---|---|---|
| 15,47 | 28,87 | Título "5 EXTRACTOS QUE DISUELVEN LOS BLOQUEOS" | "4 EXTRACTOS QUE DISUELVEN LOS BLOQUEOS" (caixa branca redesenhada, Poppins Bold) | Texto na tela |
| 15,60 | 17,12 | Fala "5 extractos naturales…" | "Cuatro extractos naturales…" (voz clonada, 0,85x p/ caber) | Voz em off |
| 15,67 | 18,37 | Legenda "cinco extractos naturales / entran a tu torrente" | "cuatro extractos naturales / entran a tu torrente" (caixa verde) | Texto na tela |
| 36,20 | 42,57 | Título "5 HIERBAS · 1 FÓRMULA · 20 GOTAS" | "4 HIERBAS · 1 FÓRMULA · 20 GOTAS" (dose mantida = a do vídeo) | Texto na tela |
| 36,36 | 39,08 | Fala "Vitaly tiene las 5 hierbas en una sola fórmula" | "Lymphoria tiene las cuatro hierbas en una sola fórmula" (voz clonada) | Voz em off |
| 36,27 | 39,17 | Legenda "Vitaly tiene las cinco / hierbas en una sola fórmula" | "Lymphoria tiene las cuatro / hierbas en una sola fórmula" | Texto na tela |
| 36,20 | 39,93 | Frasco IA "VITALY Drenaje Linfático" no boticário | Take Lymphoria conta-gotas + ervas (`lymphoria\_trabalho\ad13\flora\t4_edit.mp4`), legendas/título originais recolados | Take de frasco |
| 42,57 | 47,77 | Mulher pingando gotas, rótulo VITALY legível | Take Lymphoria frasco na mesa (`ad14\flora\t3_edit.mp4`, a 0,65x), título "EN TU CAFÉ…" e legendas originais recolados | Take de frasco |
| 64,47 | fim | "Envío gratis, garantía de 45 días. Si no funciona… Pruébalo hoy" + close do frasco VITALY (65–69 s) + título "GARANTÍA 45 DÍAS" | Cortado. Fim novo: take `P2_frasco_miel` + card de oferta (`_fim\oferta_card.jpg`: Compre 1, Reciba 2 $34.990 / 2→4 $59.990 / 3→6 $79.990, envío gratis, pagas al recibir, garantía 90 días), narração clonada "Lymphoria: compre uno y reciba dos. Envío gratis, pagas al recibir en tu casa y tienes noventa días de garantía. Si no funciona, te devolvemos tu plata. Toca el botón de abajo y pide el tuyo.", selo PAGO CONTRA ENTREGA, setas no "Toca" | Fim (voz em off) |

Áudio: voz e música separadas com demucs; trechos trocados só na voz, música original contínua por baixo; volume da fala nova casado por RMS com a original.

## Voz
- Clone ElevenLabs (IVC) da narradora do próprio V12 (amostra = vocals do demucs 0–64,4 s): **`HqqY0SS9swdkN4CjlQG4`** ("VITALY V12 narradora Mi Camino"). Marca da pessoa: clone permitido pelo briefing.
- TTS: 26 + 55 + 191 = 272 caracteres.

## Custo
- ElevenLabs TTS ≈ US$ 0,045 (clone sem custo). Takes do frasco reaproveitados (US$ 0). **Total ≈ US$ 0,05** (teto US$ 1,50).

## Revisão
- `revisar_ad.py --idioma es --proibidos proibidos.txt` → **RESULTADO: OK** (decodifica, sem salto de pts, sem quadro solto, setas no último quadro, nenhum termo proibido; Whisper ouve "linforia" = Lymphoria). Relatório: `rev\`.
- Folha nas emendas (36,20 / 39,93 / 42,57 / 47,77 / 64,47 s): `chk\emendas.jpg` — sem rótulo Vitaly, sem quadro solto.
- Pontos para revisão manual (não pedidos no briefing, mantidos): linguagem pseudo-médica ("sistema linfático bloqueado", "ganglios se limpian"), "semana 1 / semana 3", "tu abdomen se aplana". Silêncio final 0,87 s (cauda padrão do fim).

## Texto do anúncio (sugestão)
- Título: Compre 1, Reciba 2 · Pagas al recibir
- Texto: Mi rutina de 30 segundos para deshincharme 🌿 Lymphoria: 4 hierbas en una sola fórmula, unas gotas en tu café, té o agua caliente. Envío gratis, pagas al recibir y 90 días de garantía. Toca el botón de abajo 👇

## CTA v2 (10/10/2026)
- Fim refeito (sem card/preço, sem selo grande): corte em 64.47 s, parte 1 intacta, e fim novo com takes Lymphoria (ad19/t3_edit, ad11/t4_edit, P2_frasco_miel). Mesma voz do fim anterior (v12), encurtada e sem preço. Legenda palavra a palavra, selo amarelo pequeno "PAGO CONTRA ENTREGA" e setas vermelhas no CTA. Música contínua a -32 LUFS por baixo (exceto no V09, cujo original não tem música). Duração nova: 73.6 s. revisar_ad.py: RESULTADO OK. Antigo em `LYMPHORIA-ES-CL\_versao-cta-antigo\`. Scripts em `_cta_v2\`.
