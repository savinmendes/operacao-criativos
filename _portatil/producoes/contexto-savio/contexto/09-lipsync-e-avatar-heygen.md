# Lipsync e avatar (HeyGen)

> Quando e como usar o HeyGen: avatar falando a partir de imagem × lipsync sobre vídeo existente (`create_lipsync`). Inclui parâmetros, custo em créditos, jobs parados, recorte no rosto, colagem só de boca e queixo e critério de aceite. Abra antes de qualquer job de avatar ou lipsync.

## Contexto de uso

**Conta.** HeyGen da pessoa no plano Pro (assinatura), com créditos premium que **zeram todo mês (~dia 30)**: 9.148 em 04/10/2026, reset em 30/10/2026. Por isso o HeyGen entra nos orçamentos como opção "sem custo extra" no lugar de gastar dólar em Kling/Flora. Saldo atual: `get_current_user` no MCP HeyGen.

**Dois usos diferentes.**
1. **Avatar falando a partir de imagem/photo avatar** — criativo UGC ou hook com personagem próprio, e o modo B1 da tradução (criador de terceiros sem autorização).
   - Kit: `create_video_from_image`, 9:16, 1080p, expressiveness high, fit cover; leva 5–8 min; polling com `get_video`.
   - Medido em 04/10/2026: ~15 créditos por UGC de ~50 s (photo avatar + Avatar IV, 720p, áudio ElevenLabs enviado), render ~2 min.
   - Avatares já criados: "Lymphoria UGC Latina 48"; "WYZE Review Latino 35" (id `430f346689b68545f1adbea9f186bd83`).
   - Voz HeyGen "JESU ESPANHOL": `485d82fb75ab42d397affd962ca338c4`.
2. **Lipsync sobre vídeo existente (`create_lipsync`)** — refazer a boca de quem já fala no vídeo original (tradução B2, marca própria, localização de trecho).
   - Lotes: Oración ES (18 ADs, 08/10/2026), Enzimas UK (08/10/2026), San Benito FR (13/10/2026).

**Histórico do método (por que é assim).**
- Lote Oración: o 1º piloto saiu com lipsync errado (a boca "seguia o português") e a pessoa perdeu a confiança. O método foi refeito no AD 01 e documentado em `Downloads\ADLIB-104060992792639\producao\_trabalho\LICOES-LIPSYNC.md`.
- Teste no trecho s06 do AD 01 (índice de pausa, meta ≤0,6):
  - quadro inteiro + PT + precision: **1,27**;
  - recorte só na mulher + precision: 1,05;
  - trechos ≤8 s em precision: 0,97;
  - vídeo sem áudio, com trilha de silêncio ou com fala invertida: **falhou** ("audio is missing", "uses the original speech… to detect who is speaking", "No speaker is detected");
  - **recorte + PT na entrada + speed: 0,19**.
- Por que precision falha: o HeyGen só refaz a boca **onde a fala original existe**. Nas pausas do áudio novo, a boca continua articulando o idioma original.
- AD 01 final: índice do conjunto 0,19 (antes 0,86; AD 11 aprovado 0,38).
- Formato aprovado pela pessoa: plano original (Jesus atrás) + voz clonada + lipsync. **Avatar completo gerado (imagem parecida no Flora + avatar HeyGen) foi rejeitado.** Avatar só como alternativa.

**Custo medido (créditos).**
- Logo após os testes do AD 01, o saldo caiu só 2 créditos. Depois foram 73, e no fim 89 créditos (8.914 → 8.825): a cobrança aparece até ~1 h depois. Estimativa da época: speed ≈0,9–1,0 crédito/s, precision ≈0,26 crédito/s.
- Lote Oración inteiro (18 ADs, speed): **~150–170 créditos (~9 por AD)**, saldo 8.965 → 8.797. A conta "1 crédito/s" superestimou 10x.
- Enzimas UK: ~40 s de speed em 5 vídeos (+3 jobs falhos com boca coberta) e o saldo seguiu 8.797 horas depois. A cobrança do speed "parece mínima ou nula"; conferir de novo antes de orçar.
- San Benito FR (2 ADs, 13/10/2026): ~346 créditos (7.982 → 7.636).
- Conclusão registrada: o custo varia entre lotes. Medir o saldo antes e ~1 h depois do último job, sem deixar agente esperando 1 h só para medir.

**Tempo de job.** Speed: 20–40 min por trecho no AD 01; trecho de 24 s travou >30 min e em 2 partes de 12 s saiu em 4 min; um job de 11,3 s ficou >2 h em "processing" e o reenvio idêntico voltou em ~25 min.

**Lição do San Benito FR (13/10/2026).** O lipsync do HeyGen deixa o rosto mole (menos nítido). Colar só boca + queixo sobre o take original, com nitidez casada, recupera a qualidade (`SB-VENCEDORES_OP2-ASCENSAO_JESU-V07\_trabalho\v07\colar_boca.py`). Medição de nitidez FR × ES: `nitidez.py` (variância do Laplaciano no rosto).

**Ferramenta de aceite.** `kit-edicao-criativos\ferramentas\checar_lipsync.py`: local e grátis (MediaPipe Face Landmarker + ffmpeg). O modelo `face_landmarker.task` (3,7 MB) é baixado na 1ª vez para `~/.cache/kit-edicao/`. Calibração: AD 11 bom 0,37 / AD 13 0,57 / AD 01 ruim 0,85. Testes: `python -m unittest tests.test_checar_lipsync -v`.

## Lógica de uso

### A. Avatar falando (UGC, B1, hook)
1. Photo avatar por prompt coerente com o público; criar um por nicho e reutilizar. Mesmo avatar = mesma voz no lote todo.
2. Gerar o áudio no kit (`tts_elevenlabs.py`, com alinhamento) e enviar ao HeyGen. A integração ElevenLabs↔HeyGen dá `VOICE_CONFIG_ERROR`.
3. Medir créditos no 1º vídeo e fixar o teto por vídeo antes do resto. Polling a cada 30 s.
4. Intercalar b-roll de produto a cada ~10–15 s de avatar; a legenda não cobre a boca (subir o enquadramento: `A_zoom`/`A_shift` no `montar_corpo_avatar.py`). Cortar o hook 0,35 s após a última palavra.
5. Corpo B1: `montar_corpo_avatar.py plano.json` (ver [05-traducao-de-criativos.md](05-traducao-de-criativos.md)).

### B. Lipsync sobre vídeo existente — receita
1. **Ver se a boca aparece.** Boca coberta (produto na frente, mão, desfoque) → o HeyGen devolve a boca intacta e gasta crédito: trocar só o áudio.
2. **Achar quem fala.** Com 2+ rostos, medir landmarks por trecho (`_lote/rostos.py` do lote Oración) e escolher um recorte 9:16 que contenha o rosto inteiro de quem fala e deixe os olhos do outro de fora. Ex. AD 01: recorte 288×512 em (318,196), escalado 2,5x para 720×1280.
3. **Entrada.** Trecho de **até ~12 s** recortado no rosto, com o **áudio ORIGINAL** (idioma de origem) embutido no vídeo. O áudio novo vai **separado**, como mp3 do mesmo intervalo. Mandar o vídeo já com o áudio novo faz o HeyGen devolver a boca intacta (custa e parece "pronto").
4. **Parâmetros do `create_lipsync`:** `mode: "speed"` (não `precision`), `enableDynamicDuration: false`, `keepTheSameFormat: true`, `fpsMode: "cfr"`, `enableWatermark: false`.
5. **Upload:** `create_asset_upload_batch` → PUT de cada arquivo (curl com `x-amz-server-side-encryption: AES256`, `put.sh` do lote) → `complete_asset_batch`.
6. **Esperar.** Polling; se passar de ~45 min em "processing", reenviar igual (custa de novo: checar o orçamento antes).
7. **Baixar** (`baixar.sh ids.txt` do lote: `https://resource2.heygen.ai/video_translate/<id>/original.mp4`). Voltam com o número exato de quadros (30 fps cfr).
8. **Colar de volta só boca + queixo** sobre o take original, com elipse suave, cor ajustada pelo anel de pele em volta da boca e nitidez casada:
   ```
   python colar_boca.py in.mp4 out.mp4 dest.mp4 [--fechar ini:fim ...]
   ```
   (`_trabalho\v07\colar_boca.py`; `--fechar` = janelas em s em que a boca volta ao original.) Leitura e gravação com matriz bt601 fixa (ver [10-limpeza-cor-e-qualidade-de-video.md](10-limpeza-cor-e-qualidade-de-video.md)). Na versão do lote Oración (`colar.py`/`recolocar2.py`): reamostrar no tempo por interpolação (não congelar o último quadro) e crossfade de 2 quadros nas emendas sem corte de câmera (corte = diferença média da base >10).
9. **Medir cada trecho antes de encaixar:**
   ```
   python ferramentas/checar_lipsync.py saida.mp4 --audio-novo es.mp3 --original pt.mp4
   python ferramentas/checar_lipsync.py full_s06.mp4 --audio-novo es_s06.mp3 --original orig_s06.mp4 --rosto 330,280,200,260
   ```
   - Sempre passar `--original`: "a boca mudou" pega o lipsync que devolveu a boca antiga e, com vários rostos, indica quem fala.
   - `--rosto x,y,w,h` força o rosto; `--sem-audio-original` quando o original já vem com o áudio novo.
   - Resultado: APROVADO/AVISO/REPROVADO. Sai com código 1 se reprovar e 2 se não achar rosto.
10. **No AD final:** `revisar_ad.py … --lipsync "saida1.mp4:es1.mp3:pt1.mp4,saida2.mp4::pt2.mp4:320;280;400;440"` (rodar pelo **PowerShell**: o Git Bash converte os `:`). O AD é decidido pelo **índice do conjunto**.

### Critério de aceite
- **Índice de pausa** = abertura média da boca nas pausas da voz nova ÷ abertura na fala. **≤0,60 APROVADO**; 0,60–0,75 AVISO (conferir a olho); >0,75 REPROVADO. Com <20 quadros de pausa, só reprova acima de 0,90.
- Índice por trecho é ruidoso (poucas pausas, corte de câmera, barba). Trecho em AVISO/REPROVADO isolado num AD que passa no conjunto: olhar a boca nas pausas (folha de 3 em 3 quadros) antes de refazer.
- Fala contínua sem pausa: sem número; aprovar a olho e avisar a pessoa.
- Avatar HeyGen inteiro (não lipsync) costuma reprovar no checker: falso positivo registrado no lote Vitaly (C1-A/C3-A). Conferir a olho.

### Plano B sem crédito
Boca abrindo numa pausa → `fechar.py` (`ADLIB-104060992792639\producao\_trabalho\ad01\lipsync2\fechar.py`): cola uma boca fechada do próprio trecho, alinhada por olhos e nariz, nas pausas ≥6 quadros, com rampa de 3 quadros. AD 01: s03/s10/s13 foram de 0,66/0,49/0,64 para 0,03/0,03/0,04.

### Fluxo de lote
- Método novo → piloto completo, mostrar, aprovar, depois o lote. Método já validado e barato → todos em paralelo, máximo de agentes.
- Revisor independente em lotes A/B/C: mede o índice no rosto de quem fala e manda refazer o que reprovar; repetir até passar. No lote Oración, 10 de 18 vídeos voltaram pelo menos 1 vez.

### Armadilhas
- `precision` → boca segue o idioma original nas pausas. Usar `speed`.
- Áudio novo embutido na entrada → boca intacta.
- Vídeo de entrada sem fala real (sem áudio, silêncio ou fala invertida) → job falha.
- Trecho longo (>12 s) → trava.
- Rosto mole/menos nítido → colar só boca + queixo com nitidez casada.
- Cor escurecendo na colagem → leitura/gravação bt601 fixa + ajuste pelo anel de pele.
- Lipsync em profissional de saúde com fala nova → bloqueado pelo filtro de segurança (Vitaly V03/V11).

### Checklist de saída
- [ ] Saldo medido antes e depois (~1 h) e anotado no relatório.
- [ ] Cada trecho medido com `checar_lipsync.py` contra o original, rosto certo.
- [ ] Índice do conjunto ≤0,60 no `revisar_ad.py --lipsync`.
- [ ] Nitidez e cor do rosto iguais às do original (comparar quadro a quadro com zoom).
- [ ] Autorização registrada quando é criador de terceiros (B2).

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [02-regras-gerais-e-seguranca.md](02-regras-gerais-e-seguranca.md)
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [04-fluxo-producao-criativos.md](04-fluxo-producao-criativos.md)
- [05-traducao-de-criativos.md](05-traducao-de-criativos.md)
- [08-voz-e-dublagem.md](08-voz-e-dublagem.md)
- [10-limpeza-cor-e-qualidade-de-video.md](10-limpeza-cor-e-qualidade-de-video.md)
- [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)
- [projetos/](projetos/)
