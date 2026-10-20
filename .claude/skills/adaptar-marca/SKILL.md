---
name: adaptar-marca
description: Troca marca, oferta e mercado de um lote de criativos de marca própria (ex.: produto X → produto Y com a mesma fórmula, fim COD universal) — estudo e orçamento por caminho, upscale em fila, corte antes da apresentação da marca, fim universal com voz clonada, rótulo/texto/fala antigos trocados, versão curta, matriz gancho × corpo, revisão e entrega. Use quando pedirem para "virar" um vídeo para outra marca/oferta ou reaproveitar criativos antigos.
---

# Adaptar marca

Fluxo de lote. Montagem, geração e revisão seguem `editar-criativo`, `gerar-midia-ia` e `revisar-criativo`; aqui só o que é próprio da troca de marca. Leia antes o `CLAUDE.md` do kit (seção "Troca de marca em AD existente" e as armadilhas). Nunca leia nem imprima `.env`. Clonar a voz do narrador só é permitido porque os vídeos são da pessoa: confirme isso no estudo.

## 1. Estudo e orçamento
1. Baixe sempre na **maior qualidade disponível (≥720p)**: na Biblioteca do Meta, o `video_hd_url` dos dados da página, não o vídeo do player (360p); confira com `ffprobe` e deduplique por md5. Originais em `originais/NN.mp4` + `indice-arquivos.csv`. Agentes em paralelo (transcrição faster-whisper, folha de contato, OCR só onde precisar; sequencial, `cpu_threads=4`).
2. Classificar cada vídeo: **marca própria adaptável**, **já com a marca nova** (só fim/unidades), **concorrente** (só como referência de ângulo; nunca usar imagem, texto ou voz dele), **descartar** (outro produto, cópia, fraco).
3. Conferir **duplicados contra lotes anteriores** (mesmo roteiro já entregue como AD NN) para não refazer.
4. Listar os melhores ganchos/ângulos (com o tempo em que começam) e os **riscos de plataforma** (sexo/traição explícitos, antes/depois com kg, doença nomeada, medicamento, registro sanitário, menção a outra plataforma, "feito em" país estrangeiro, garantia diferente da oferta nova).
5. Orçamento por caminho, cada um com custo + tempo + opção paga mais rápida: **(1) adaptar** (cenas no Kling × preço/cena + voz), **(2) refazer do zero com avatar** (créditos), **(3) matriz gancho × corpo** (depende do 1). Dar a versão curta e a opção "desfocar em vez de Kling" como variantes mais baratas.
6. Perguntas de bloqueio: os vídeos são da pessoa? oferta e países (COD, frete, garantia, preço)? aprovação do gasto? Sem resposta, não produzir.

## 2. Preparação do lote
- Origem 360p → `upscale_video.py --escala 2` para 720 em **fila única de GPU** (um script de fila com log de progresso). Agentes não rodam upscale: esperam o `full_up720.mp4` em loop e, enquanto isso, adiantam no original (ponto de corte, mapa de cenas, voz).
- Briefing único `producao/_trabalho/BRIEFING-AGENTES.md` (1 agente por 1–2 ADs) com: oferta/CTA/garantia da marca nova, lista do que tirar, textos do fim A/B/C, regra de voz, teto de Kling por AD (cenas orçadas + 2), CPU/GPU, revisão, formato do relatório, "não pergunte; escolha o seguro e anote".

## 3. Por AD
1. **Ponto de corte:** transcrição por palavra; cortar antes do trecho em que o narrador apresenta a marca/oferta antiga (nome, preço, link, garantia).
2. **Fim universal** (serve a todos os países da oferta): fotos do produto novo + narração clonada + legenda + selo + setas. Texto **A** (a narração já citou os ingredientes), **B** ou **C** (apresenta do zero). Voz: `clonar_voz.py` a partir de um trecho limpo do narrador; antes, procure clone existente da mesma voz (`voz.txt` dos lotes anteriores) e reutilize por semelhança. Nunca apague vozes. `tts_elevenlabs.py` com alinhamento → `narr_fim.mp3`.
3. **Cenas com a marca antiga** (achar na folha de contato do `full_up720`): `trocar_rotulo_faixa.py` primeiro (grátis, quadro a quadro); Kling O1 Edit só onde a faixa não resolve e **nunca em rosto estilizado/3D** (ele deforma). Take ≥ 3 s com `tpad`, referência do frasco novo sobre fundo neutro; `encaixar_edit.py` + `substituir_trechos.py`. Marca pequena/ilegível ao fundo: manter e anotar.
4. **Texto na tela** (marca, preço, garantia antiga, origem): `trocar_texto_tela.py`; tela de celular/app: `desfocar_regioes.py`.
5. **Falas** com marca, garantia ou plataforma antiga: fala nova na voz clonada + `trocar_trecho_audio.py` (sem dessincronizar).
6. Tudo numa receita `rNN.json` (`corte`, `takes`, `extras`, `blur`, `textos`, `audios`, `cauda`, `saida`) rodada por um pipeline `processar_ad.py`-like que pula etapas já feitas; o fim passa por `montar_ad.py` em 720.
7. **Versão CURTA** (60–90 s): gancho (~8–15 s) + 2–3 trechos fortes (problema, mecanismo, prova) + o mesmo fim; cortar em fim de frase pela transcrição por palavra, usando só partes já tratadas para a marca antiga não voltar.
8. `revisar_ad.py` + **zoom 3x em cada take trocado** (o resto do rótulo antigo só aparece ampliado).

## 4. Matriz e UGC
- `gerar_variacao.py` em três passos: `banco <video>` (tomadas por `scdet` + transcrição por palavra), `fundo <video> --ate <corte>` (música sem voz para a emenda) e `montar config.json` (gancho com voz do corpo + cenas do banco com margem nas bordas, sem repetir a mesma cena; modelo em `exemplos/variacao_exemplo.json`). Ganchos adaptados ao gênero do corpo. Estáticos/carrossel saem de quadros reais.
- Ângulos bons de concorrentes viram **UGC com avatar próprio** (`gerar-midia-ia`): só a ideia, roteiro novo, cenas do produto novo. Meça os créditos no 1º.

## 5. Remover o que não vale na oferta nova
Garantia antiga, "feito em", claims fora da ficha, menção a outra plataforma, medicamento/doença como cura, cenas de risco (cobrir com a vizinha ou cortar). Unidades (libras/kg) só mudam se a oferta pedir. Não inventar depoimento, número ou estudo.

## 6. Revisão e entrega
- Por vídeo: `revisar_ad.py`; Whisper no idioma procurando marca antiga, garantia antiga, plataforma, preço, "link", termos de risco; folha de contato 1 quadro/2 s procurando rótulo antigo legível, cena de risco, quadro solto, silêncio no fim. Depois `revisar-criativo`. Longos acima de 30 MB: anotar (plataforma aceita), não degradar.
- `producao/AD NN - <MARCA>-<TEMA>-<IDIOMA>-<MERCADO>.mp4` (+ `AD NN CURTO - ...`), `_trabalho/adNN/RELATORIO.md` (takes Kling e US$, caracteres TTS, clone usado, o que saiu/trocou, revisão, pendências).
- `producao/00-RELATORIO-PRODUCAO.md`: custo real × orçado por bloco, decisões, tabela longos/curtos/variações/UGC, "para você olhar" (riscos de plataforma, restos de rótulo, emendas), bugs do kit achados e corrigidos.
- Textos de anúncio por AD (título, descrição, texto principal, TikTok ≤ 100 caracteres) e memória do projeto atualizada (clones por narrador, método, pendências).
