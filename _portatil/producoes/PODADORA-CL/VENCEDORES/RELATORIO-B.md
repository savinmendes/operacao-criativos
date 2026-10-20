# Relatório — Vencedor B "ORILLA" (Podadora COD Chile) — 08/10/2026

**Origem:** `_vencedores/vencedor1.mp4`, 37,0 s, 576x1024, 30 fps. É um vídeo da própria operação, com narração feminina em espanhol de tom mexicano.
**Estrutura do original (transcrição por palavra):** a narração inteira (0–15,0 s, "Ya ni se veía la orilla, sigue viendo… Pícale aquí abajo") **se repete** sobre outras cenas de 16,4 s a 31,5 s. De 32,7 s até o fim (4,25 s) não há som nenhum (−74 dB), só a moça sorrindo. O original **não tem trilha**: o `no_vocals` do demucs fica em −50 a −60 dB, com dois efeitos curtos em 15 s e 31,5 s.
**Corte gancho→corpo:** 2,100 s. A frase "…sigue viendo." termina em 1,92 s e "Mira," começa em 2,26 s. O corpo e o CTA vão de 2,100 s até o fim, **sem nenhuma alteração** (também não há legenda, selo nem setas, porque o original não tem).

## Entregas

| Arquivo | Gancho (narração / texto na tela) | Cenas do gancho (s do original) | Gancho | Total | MB |
|---|---|---|---|---|---|
| `B0 - ORILLA-1080.mp4` | — (original sem mudança) | — | — | 36,97 s | 25,2 |
| `B1 - ORILLA-YA-NI-SE-VEIA-ES-CL.mp4` | "Ya ni se veía la orilla… mira cómo quedó." / YA NI SE VEÍA 😳 | corredor tomado de mato 0,00–1,20 → faixa sendo aberta no gramado alto 19,50–20,60 → POV da faixa listrada aberta 22,40–23,13 | 3,03 s | 37,90 s | 25,4 |
| `B2 - ORILLA-VECINOS-ES-CL.mp4` | "Mis vecinos pensaron que contraté a alguien." / ¿CONTRATASTE A ALGUIEN? | faixas listradas no gramado alto 18,40–20,10 → POV da faixa 22,40–23,13 → close das rodas/disco na beira 21,60–22,20 | 3,03 s | 37,90 s | 25,3 |
| `B3 - ORILLA-SOLA-ES-CL.mp4` | "Esto lo hice en una tarde, y sola." / SOLA. EN UNA TARDE. | visão do cabo cortando mato alto 16,45–18,12 → quintal já cortado 32,60–33,83 | 2,90 s | 37,77 s | 25,0 |
| `B4 - ORILLA-TU-PATIO-ES-CL.mp4` | "Si tu patio se ve así… sigue viendo." / ¿TU PATIO SE VE ASÍ? | pior quadro do mato (corredor, 0,00) **congelado 1,0 s** → corredor 0,00–2,10, que emenda sem corte no corpo | 3,10 s | 37,97 s | 26,0 |
| `B5 - ORILLA-ORILLA-PERFECTA-ES-CL.mp4` | "La parte más difícil era la orilla… hasta ahora." / LA ORILLA PERFECTA | beira do gramado junto à rua 11,40–12,80 → máquina vindo rente à beira da calçada até o close do disco 20,00–22,20 | 3,60 s | 38,47 s | 25,4 |
| `B6 - ORILLA-VALIO-LA-PENA-ES-CL.mp4` | "Dos baterías, ruedas y **cuatro cuchillas**… por eso valió la pena." / VALIÓ LA PENA ✅ | foto do kit (`produto_kit.webp`, zoom lento 1,00→1,08, fundo ampliado e desfocado) 2,87 s → cortes rápidos: POV no mato alto 16,45–17,25, disco na beira 21,45–22,18, rodas no gramado 6,25–6,78 | 4,93 s | 39,80 s | 26,0 |

Todos os vídeos: H.264 high, yuv420p, 30 fps, AAC 48 kHz estéreo, abaixo de 30 MB e decodificando sem erro. Texto na tela: caixa branca do kit (Poppins Bold 64 px, centro y=240 em 1280) durante todo o gancho. Nenhum gancho tem rosto falando: a moça aparece só de corpo ou de longe, cortando.

## Decisões e desvios (para revisar)
- **Resolução das variações:** o `gerar_variacao.py` só gera em 720x1280 ou 1080x1920. Por isso o vídeo inteiro (gancho + corpo) foi **escalado proporcionalmente de 576x1024 para 720x1280, sem corte e sem barra**: as duas resoluções são 9:16 exatos, então o `crop` do script não remove nenhum pixel. Não houve upscale por IA nas variações.
- **B0:** upscale Real-ESRGAN 2x (`realesr-animevideov3`) gera 1152x2048, reduzido depois para 1080x1920 com lanczos. O áudio original foi mantido. A 1ª passada do `upscale_video.py` saiu com **1105 de 1109 quadros**: o Real-ESRGAN pulou 4 PNGs em silêncio, provavelmente com a GPU dividida com o outro lote. Refiz rodando o Real-ESRGAN direto e conferindo os **1109/1109 quadros**.
- **B6, "cuatro cabezales":** não bate com a foto. O kit tem 2 discos de serra + 2 lâminas de 2 pontas, ou seja, 4 acessórios de corte, mas nenhum "cabezal" (carretel de fio). Usei **"cuatro cuchillas"**. O corpo original continua dizendo "cuatro cabezales", porque é a fala da narradora e o corpo não pode ser mexido.
- **Repetição na emenda:** o corpo começa em "Mira, dos baterías, ruedas y cuatro cabezales". Por isso o B1 ("…mira cómo quedó. Mira, …") e o B6 (que já cita o kit) repetem palavras logo depois do gancho. É consequência da regra de manter o corpo intacto. Vale olhar se incomoda.
- **Narração curta:** no tom da narradora (rápido, mexicano), as falas aprovadas deram de 2,2 a 2,9 s, menos que os 3 s pedidos (só o B6 tem 4,3 s). Não desacelerei a voz. Para os ganchos ficarem com ≥2,9 s, abri com 0,30 s de texto na tela antes da fala e deixei uma pequena pausa antes do "Mira,".
- **Fundo do gancho:** usei o `no_vocals` dos primeiros 2,1 s do original, que emenda direto no corpo. Como o original não tem música, esse fundo é só ambiente residual (≈ −57 dBFS, inaudível). No B6, os primeiros ~3 s de fundo ficaram em silêncio digital (o fundo de 2,1 s não cobre os 4,9 s do gancho). Não dá para ouvir diferença.
- **Volume:** a voz do gancho foi ajustada para o nível da voz original. Gancho entre −14,4 e −14,7 LUFS, contra −14,3 LUFS no corpo.

## Voz
- Não havia clone desta narradora. Os clones "Podadora narrador A/B" são dos originais em inglês do lote anterior.
- **Clone criado:** "PODADORA venc-B narradora", `voice_id 57OUoWWIdEbPrxk0T02A` (Instant Voice Clone, sem custo). Amostra: stem `vocals` do demucs, 0–31,8 s. Nenhuma voz foi apagada.
- **TTS:** ElevenLabs `eleven_multilingual_v2`, 1 geração por gancho, 266 caracteres no total. **Custo ≈ US$ 0,044** (B1 41, B2 44, B3 34, B4 36, B5 48, B6 63 caracteres). Não houve nenhuma regeneração.
- Não usei crédito do HeyGen nem gerei imagem ou vídeo por IA.

## Revisão (`revisar_ad.py` pelo PowerShell, `--proibidos proibidos.txt` em UTF-8, `--passo 1`)
- **Termos proibidos** (precio, pesos, lucas, dólares, $+número, gratis, garantía, tiktok, link): **nenhum**, em B0–B6.
- **Transcrição do gancho (whisper es):** B1 "Ya ni se veía la orilla, mira cómo quedó"; B2 "Mis vecinos pensaron que contraté a alguien"; B3 "Esto lo hice en una tarde y sola"; B4 "Si tu patio se ve así, sigue viendo"; B5 "La parte más difícil era la orilla, hasta ahora"; B6 "Dos baterías, ruedas y cuatro cuchillas. Por eso valió la [pena]". No B6 o whisper cortou o segmento, mas a fala termina em 4,31 s, dentro do gancho de 4,93 s. **Nenhuma frase foi cortada.**
- **Decodificação:** OK. **Saltos de pts no áudio:** nenhum. **Quadro solto** (cortes a menos de 0,3 s): **nenhum** em todos.
- **Folha quadro a quadro da emenda gancho→corpo** (6 quadros antes e 6 depois, nas 6 variações): `_vencedores/B/emenda/emendas_quadro_a_quadro.jpg`. Cortes limpos e o B4 emenda contínuo, sem corte. Nível de áudio estável em toda a emenda.
- **"PROBLEMA: silêncio de 4,25 s no fim"** aparece em **todos, inclusive no B0**. Isso vem do próprio vencedor (moça sorrindo em silêncio) e foi mantido porque o corpo e o CTA não podem ser alterados. Se quiserem cortar, basta tirar os últimos ~3,6 s de cada vídeo.
- **Aviso "sem setas de CTA no fim":** esperado, porque o vencedor não tem setas e o CTA é falado ("Pícale aquí abajo").
- Relatórios e folhas de contato de cada vídeo: `_vencedores/B/revisao/*_revisao.txt|.jpg`.

## Arquivos de trabalho
`_vencedores/B/`: `montar_ganchos.py` (cenas de cada gancho + configs do `gerar_variacao.py montar`), `voz/B1–B6.mp3` (+ `.txt` e `.alinhamento.json`), `banco.json` + `folha*/` (tomadas e transcrição), `sep/` (demucs), `bed.wav`, `proibidos.txt`, `trab/B*/` (visual de cada gancho, config e `info.json`) e `up2x.mp4`.

## Pendências
- O texto do anúncio (título + texto principal por variação) ainda não foi feito. O briefing não pediu.
- Decidir se o silêncio final de 4,25 s do vencedor deve ser cortado em novas versões.
