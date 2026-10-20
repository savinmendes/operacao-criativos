---
name: project-vsl-lead2-de
description: "VSL San Benito 'Lead 2' (42:43, ES) → ALEMÃO (19/10/2026): avatar do padre é da pessoa, lipsync; Papa cortado; 37 €; voz clonada PADRE VSL LEAD2; pasta VSL-LEAD2-DE"
metadata:
  type: project
---

**19/10/2026.** A VSL `Downloads/Lead 2.mp4` tem 42:43, 720x960, selo EN VIVO e legenda queimada. Vai só para ALEMÃO (a ideia inicial de inglês caiu). O padre de casula verde é avatar 100% da pessoa, então o lipsync nele está liberado.

**Decisões da pessoa:**
- Tratamento formal "Sie".
- Cortar os vídeos do Papa Francisco. Nas falas em que "o Papa entregou a oração", trocar por "ein Bischof" ou "Archive des Vatikans"; rezar pelo Papa pode ficar.
- Preço 37 € (os downsells de 25,90 € e 19 € ficam no checkout, fora do vídeo).
- Valores da história convertidos em €.
- Remover a FAQ de câmbio.
- Clonar a voz do padre. A vaga foi liberada apagando a "Voz Elon Musk", com o ok da pessoa.

**Orçamento passado:** ~US$ 10 de ElevenLabs, ~300–350 créditos HeyGen, ~4–5 h e ~2–3 M tokens.

**Fluxo combinado:** o roteiro DE + revisão nativa + retrotradução PT (`ROTEIRO_DE_PARA_APROVAR.md`) passa pela aprovação dela ANTES de gerar a voz. A base (LaMa + LIVE + demucs + clone) roda em paralelo.

Relacionado: [[feedback-debater-criativo-antes-de-gerar]], [[feedback-chiado-tts-demucs]]

**20/10/2026, lipsync concluído:** os lotes 1–4 entregaram L022–L292.
- **Abertura cortada:** o apresentador de traje papal se parecia com o Papa Leão XIV; a pessoa escolheu cortar 0–03:25 inteiro.
- **HeyGen:** de 4.737 para 4.627 créditos (~110), medido logo após os lotes. A cobrança ainda pode subir.
- **Duplicação:** o lote 3 enviou o batch em dobro, porque reenviou com os assets ainda processando.

**Lições técnicas:**
- Não reenvie o batch enquanto os jobs estiverem "pending" com os assets processando.
- `-colorspace bt709` no encode de uma saída HeyGen sem tag escurece ~2,4 níveis de luma. Recodifique com o YUV intacto e marque a tag via `h264_metadata`.

**Montagem final** em andamento, em `_trabalho/montagem`.

**20/10, pausa por limite de créditos:** a v1 está em `VSL-LEAD2-DE/VSL-LEAD2-DE.mp4` (06:39, 38:20). Ela tem sobras de legenda ES em alguns trechos e 1 quadro solto em 18:35.

**O agente de montagem estava fazendo:**
- re-render v2 com os patches de resíduo (`_trabalho/montagem/residuo`, `chk/render_N.log`);
- depois `revisar_ad` + `RELATORIO_FINAL.md`.

**Para retomar:** conferir se os blocos v2 terminaram, fazer concat e QA, e substituir o mp4. A pessoa escolheu MANTER sem modelagem cultural por enquanto (testar primeiro).
