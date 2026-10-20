# San Benito ES: criativos vencedores no Meta

> Ranking dos criativos vencedores da Oração de San Benito em espanhol (vida útil da conta), com os vídeos baixados. Abra antes de produzir variação, tradução ou escala de San Benito.

## Contexto de uso
- **Frente:** Infoproduto — Oração de San Benito, público em espanhol.
- **Análise feita em 11/10/2026**, só leitura no Meta (nada criado, editado, pausado ou ativado).
- **Conta:** CONTA 01 (SAN BENITO), act 1929332567965953, USD. Escopo: 50 campanhas `SB ES` de vendas (datas no nome de 12/07 a 04/10/2026), 543 anúncios → 220 criativos depois de agrupar variações. Fora: `SB US`, `SB RESTO`, `SB FR` e 2 campanhas de engajamento.
- **Totais SB ES:** US$ 14.292,29 de gasto, 452 compras, CPA médio US$ 31,62, ROAS médio 1,22.
- **Vencedores (por ROAS):**
  1. SHAKIRA 1 + PAPA 1 — ROAS 3,82, CPA US$ 10,54 — **reprovado** no Meta, sem vídeo;
  2. ADS 6 — ROAS 2,64, gasto US$ 1.047,85, 71 compras;
  3. SHAKIRA 3 + PAPA 2 — ROAS 2,32 — **reprovado**, sem vídeo;
  4. ADS 20 — ROAS 1,91, gasto US$ 1.001,50;
  5. ADS 12.12 — ROAS 1,63, CTR 10,17 %;
  6. JESU V07 — ROAS 1,48, CTR 10,14 %;
  7. ADS 1 — ROAS 1,43 (só existe em 360x480);
  8. ADS 12 — ROAS 1,41;
  9. provisórios (< 5 compras): AD 81 (2,08) e ADS 12.1 GD (1,30).
- **Padrões observados:**
  - título `🔴 EN VIVO: La oración a San Benito que casi nadie conoce 🙏` em 6 dos 10;
  - ângulo "mala suerte / bloqueio tem causa espiritual" + oração "poco conocida" como saída; variações que venceram: solidão (JESU V07) e o homem que carrega tudo em silêncio (AD 81);
  - vídeos longos (~2 min) dão volume (US$ 1.000–1.200, 43–71 compras); curtos de 31–33 s dão CTR ~10 %;
  - família ADS 12: o corpo de 31,5 s funciona, mas depende da abertura (12.1, 12.7 e 12.18 perderam);
  - os 2 melhores em ROAS usam celebridade e estão reprovados.
- **Pasta:** `Downloads\SAN-BENITO-ES-VENCEDORES\` — 8 vídeos `SB-ES_NN_<NOME>.mp4` + `.txt` por criativo (campanhas, métricas, origem do arquivo) + `00-RELATORIO.md`.
- **Pendências:** Shakira sem arquivo (baixar pelo Gerenciador: `Ad Shakira 1 HK papa 1.mp4`, `Ad Shakira 3 HK papa 2.mp4`); ADS 1 só em 360p (procurar original antes de reaproveitar); reuso dos Shakira depende de decisão de compliance (tirar a celebridade).
- **Desdobramento:** em 13/10/2026 a pessoa apontou OP2 ASCENSAO e JESU V07 como vencedores e pediu a versão em francês (ver [san-benito-fr.md](san-benito-fr.md)).

## Lógica de uso
1. Puxar do Meta (só leitura) todas as campanhas da oferta/mercado com objetivo de vendas, `date_preset maximum`.
2. **Agrupar variações** do mesmo criativo (sufixos `| HOT`, `| HOT 2`, `| WHOP`, `— NV`, `B`), confirmando por video_id.
3. **Critério de vencedor:** gasto ≥ 2× o CPA médio (aqui ≥ US$ 63,24) **e** (CPA ≤ média **ou** ROAS > média); ordenar por ROAS (média ponderada pelo gasto); < 5 compras = provisório.
4. **Baixar os vídeos:** a API não liberou `download_hd_url` (veio null) → yt-dlp direto do Facebook (`-f "bv*+ba/b"`; AV1 convertido para H.264) ou arquivo local com a mesma duração; registrar a origem no `.txt`; conferir resolução (< 720p → avisar).
5. Escrever o padrão comum só com o que os dados mostram (não assistir quadro a quadro não autoriza conclusões sobre o conteúdo).
- **Se a pessoa pedir mais:** priorizar os vencedores (top 5) em novas variações/traduções; para celebridade, levar a decisão de compliance à pessoa (manter × tirar).

## Relacionados
- [san-benito-fr.md](san-benito-fr.md), [oracion-es-latam.md](oracion-es-latam.md)
- [../04-fluxo-producao-criativos.md](../04-fluxo-producao-criativos.md)
