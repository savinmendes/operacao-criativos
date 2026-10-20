# V19 → Lymphoria (Chile) — ANTES/DESPUÉS (SUAVIZADO)

- **Final:** `ADLIB-VITALY-CL\LYMPHORIA-ES-CL\V19 - LYMPHORIA-ANTES-DESPUES.mp4` (32,1 s, 720x1280, 18,7 MB).
- **Suavizados:** `LYMPHORIA-ES-CL\SUAVIZADOS\V19 - ORIGINAL.mp4` (cópia do original) e `V19 - SUAVIZADO.mp4` (= o final). Seção `## V19` escrita em `SUAVIZADOS\00-TROCAS.md`.
- **Origem:** `VIDEOS\19 - Vitaly - 881380110992207.mp4` (720x1280, 19,33 s, só música, sem fala). O corpo mantém a duração do original (19,33 s, 580 quadros); a música original segue sem mudança.

## Trocas (TROCAS)
| Início (s) | Fim (s) | Original | Novo | Tipo |
|---|---|---|---|---|
| 0,00 | 8,20 (q. 0–246) | Selo "114 KG" | "ANTES" (caixa branca no mesmo lugar, centro x 383, y 877–953) | Texto na tela |
| 8,23 | 19,33 (q. 247–579) | Selo "84 KG" | "DESPUÉS" | Texto na tela |
| 14,83 | 19,33 (q. 445–579) | "Todo gracias a las gotas herbales de Vitaly" | "Todo gracias a las gotas herbales de Lymphoria" (mesma caixa, um pouco mais larga) | Texto na tela |
| 19,33 | 32,10 | — | Fim Lymphoria (o mesmo do V12): take P2_frasco_miel + card de oferta (Compre 1, Reciba 2 $34.990 / 2→4 $59.990 / 3→6 $79.990, envío gratis, pagas al recibir, 90 días), narração (voz clonada da narradora do V12), selo PAGO CONTRA ENTREGA, setas no "Toca" | Fim (voz em off) |

Fonte das caixas novas: Poppins Medium, que fica próxima da fonte "Classic" original. Tempos tirados quadro a quadro do original.

## Custo
US$ 0 (o fim reaproveita a narração e o vídeo do V12).

## Revisão
- `revisar_ad.py --idioma es --proibidos proibidos.txt` → **RESULTADO: OK** (Whisper só ouve o fim; nenhum termo proibido; sem salto de pts; setas no último quadro). Folha 1 q/s conferida: nenhum "KG" nem "Vitaly" na tela.
- **Revisão manual:** o antes/depois visual do corpo continua (é o formato do vídeo) e é risco de reprovação na Meta. A música é uma canção em inglês com letra (direito autoral). "Haz clic abajo y aprende a drenar naturalmente tu cuerpo" foi mantido (é CTA).

## Texto do anúncio (sugestão)
- Título: Compre 1, Reciba 2 · Pagas al recibir
- Texto: Pensaba que era grasa, pero era retención de líquidos 💧 Lymphoria, gotas herbales de drenaje linfático. Envío gratis, pagas al recibir y 90 días de garantía. Toca el botón de abajo 👇

## CTA v2 (10/10/2026)
- Fim refeito (sem card/preço, sem selo grande): corte em 19.33 s, parte 1 intacta, e fim novo com takes Lymphoria (ad13/t5_edit, V1_gotero_hierbas, ad14/t4_edit). Mesma voz do fim anterior (v12), encurtada e sem preço. Legenda palavra a palavra, selo amarelo pequeno "PAGO CONTRA ENTREGA" e setas vermelhas no CTA. Música contínua a -32 LUFS por baixo (exceto no V09, cujo original não tem música). Duração nova: 28.5 s. revisar_ad.py: RESULTADO OK. Antigo em `LYMPHORIA-ES-CL\_versao-cta-antigo\`. Scripts em `_cta_v2\`.
