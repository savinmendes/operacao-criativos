# Produção noturna 03→04/10/2026 — relatório final

Escopo aprovado: Lymphoria Lotes 2+3 (ES neutro LATAM — Chile, Guatemala, Equador; 720p) + 5 Linfarele (IT, Itália). Orçamento aprovado ≈ US$51.

## Entregas — Lymphoria (pasta `lymphoria/`, atalho `entregas-lymphoria/`)
| AD | Arquivo | O que foi feito |
|---|---|---|
| 01 | AD 01 - LYMPHORIA-ESPOSA-ES-LATAM.mp4 | Kling nos frascos, tela do celular coberta, fim com voz clonada |
| 02 | AD 02 - LYMPHORIA-28-ANOS-ES-LATAM.mp4 | 3 takes Kling, 2 legendas e 2 falas trocadas, celular desfocado, fim B |
| 03 | AD 03 - LYMPHORIA-ESQUELETO-30DIAS-ES-LATAM.mp4 | Kling + fim |
| 05 | AD 05 - LYMPHORIA-HIGADO-ES-LATAM.mp4 | já era Lymphoria; corte + fim C |
| 07 | AD 07 - LYMPHORIA-RINON-ES-LATAM.mp4 | corte 2:04 + fim do médico com voz clonada |
| 09 | AD 09 - LYMPHORIA-SESENTA-ES-LATAM.mp4 | 2 takes Kling, legenda + fala trocadas, fim B |
| 10 | AD 10 - LYMPHORIA-MATRIMONIO-ES-LATAM.mp4 | Kling + falas + fim |
| 11 | AD 11 - LYMPHORIA-GIMNASIO-ES-LATAM.mp4 | 5 takes Kling, legenda + fala, celular desfocado, fim B |
| 12 | AD 12 - LYMPHORIA-BANO-RESERVA-ES-LATAM.mp4 | 2 takes Kling, celular coberto, fala trocada, fim B |
| 13 | AD 13 - LYMPHORIA-HERMANO-ES-LATAM.mp4 | 5 takes Kling, 3 legendas + 3 falas, celular desfocado, fim B |
| 14 | AD 14 - LYMPHORIA-VIAJE-ES-LATAM.mp4 | 5 takes Kling, 2 legendas + 2 falas, celular desfocado, fim B |
| 16 | AD 16 - LYMPHORIA-VESTIDO-ES-LATAM.mp4 | 3 takes Kling, legenda + fala, celular desfocado, fim B |
| 19 | AD 19 - LYMPHORIA-CELULITIS-ES-LATAM.mp4 | 4 takes Kling (Herbalia→Lymphoria; 1 com rosto, conferido), fim próprio |
| 22 | AD 22 - LYMPHORIA-22-ANOS-ES-LATAM.mp4 | 2 takes Kling, 2 legendas + 2 falas, celular desfocado, fim A |

Lote 1 (04, 06, 21, 23, 24) já tinha sido entregue. Textos dos anúncios: `lymphoria/TEXTOS-ANUNCIOS-LOTE1/2/3.txt`.

## Entregas — Linfarele IT (pasta `linfarele/`, atalho `entregas-linfarele/`)
| AD | Arquivo | O que foi feito |
|---|---|---|
| 03 | AD 03 - LINFARELE-SCHELETRO-30GIORNI-IT.mp4 | dublagem IT (voz clonada), legenda IT, 2 takes Kling → Linfarele, fim IT |
| 04 | AD 04 - LINFARELE-SCHELETRO-BIRRA-IT.mp4 | idem, 7 takes Kling |
| 05 | AD 05 - LINFARELE-FEGATO-IT.mp4 | idem; mascote-frasco sem marca legível (sem Kling) |
| 06 | AD 06 - LINFARELE-PETTO-IT.mp4 | idem; sem frasco antes do corte |
| 10 | AD 10 - LINFARELE-MATRIMONIO-IT.mp4 | legenda ES removida localmente (Vmake sem crédito), 3 takes Kling, 2 falas "Linfarele" |

Textos: `linfarele/TESTI-ANNUNCI-IT.txt`.

## Custos (aprox.)
- Kling O1 Edit (Flora): ~60 takes cobrados × US$0,706 ≈ **US$42** (takes recusados por duração curta não foram cobrados).
- Flora imagens (recorte/fotos): ≈ US$0,14.
- ElevenLabs falas/fins: ≈ US$2,1. Dublagem IT e clonagem de voz: créditos do plano.
- **Total ≈ US$44** (dentro dos US$51).

## Correções feitas na revisão final
- AD 10 (Lymphoria, já entregue no lote 2) tinha um frasco Mayaverra em 4:45–4:47 → refeito com Kling e reenviado (mesmo nome de arquivo). Mesmo frasco corrigido no AD 10 IT.
- AD 14: frasco do conta-gotas em 6:22 ainda mostrava MAYAVERRA → take extra no Kling.
- AD 10 IT: legenda dividia "L'INFARELE" → o kit agora junta elisões italianas e corrige o nome da marca (`legenda_hook.corrigir`).

## Limitações / revisão manual
- AD 01: pausa curta na frase trocada (fala esticada a 0,85×).
- AD 02: "De Lymphoria y el secreto de Brasil" ficou mais curta que o trecho original → completada com silêncio.
- AD 11 5:10 (0,7 s): o Kling trocou o fundo do close do frasco por um fundo liso — passa como inserto de produto, mas dá para notar.
- Frascos muito pequenos/ilegíveis ao fundo foram mantidos (ex.: AD 11 6:24, AD 13 3:54/4:41, AD 14 6:55).
- AD 19: tomadas da mulher em 0:00–0:02 e 0:08–0:09 mantêm o frasco Herbalia pequeno (só 0:25 foi trocado, para não arriscar o rosto). O vídeo tem antes/depois de celulite → risco de reprovação.
- AD 07 (médico/insuficiência renal) e AD 19: risco de compliance no Meta.
- Linfarele: confirmar no site se frete grátis e garantia de 90 dias valem para a Itália (o fim IT promete os dois).
- Legendas IT geradas por transcrição automática — revisar a grafia de "Linfarele" no AD 10.
- Vídeos longos passam de 30 MB (até ~110 MB) — Meta aceita; reduzir só se a plataforma reclamar.
- Pendente decisão: apagar "PREVIA - AD 04 ... ES-CL.mp4"?
