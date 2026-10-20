---
name: gerar-midia-ia
description: Gera imagens base, takes de vídeo IA, troca de rótulo/produto em cena, avatar falando e narração para criativos (Flora, Kling, HeyGen, ElevenLabs), com orçamento antes, QA por outra IA e canvas organizado. Use quando pedirem imagens, takes, rótulo trocado, hooks com avatar ou áudio narrado.
---

# Gerar mídia com IA

## Orçamento (sempre antes de gerar)
1. Informe peças × preço = total em US$ (ou créditos), **tempo médio** e a **opção paga mais rápida** lado a lado.
2. Pare para aprovação só quando for gastar dinheiro real. Nunca repita geração paga sem avisar; informe o custo real no fim.
3. Teto por peça/vídeo definido antes do lote; estourou → pare e relate.

## Imagens base (Flora)
- Projeto da oferta no Flora (crie "<Oferta> — Criativos" se não existir). Suba a foto ORIGINAL do produto (`flora_create_asset` ou `flora_upload.py`).
- i2i 9:16, quality high. Prompt: descrição EXATA do produto (cor, peças, acessórios), cena da dor/função, 15% livre no topo e 25% na base, fotorrealista, sem texto/logo.
- Faça 1, mostre, aprove; depois o lote. Canvas: 1 grupo por lote, 5 colunas, sem sobrepor. Salve prompt + node id em `imagens/<codigo>.txt`.

## Takes de vídeo (Flora)
- i2v Kling 5 s por padrão (10 s só se pedido). Prompt de movimento curto e físico. Kling não faz física de corte/destruição: gere o "antes" e use só o 1º trecho limpo ou filmagem real.
- **QA obrigatório** por v2t (modelo de visão): produto igual à referência? física correta? deformação? texto/logo? APROVADO/REPROVADO + trecho limpo. Reprovado não entra.
- **O QA por IA dá falso alarme.** Antes de pagar uma refação, confirme o defeito a olho: quadro a quadro de 0,2 em 0,2 s, com zoom em mãos, rostos e bordas. Já houve take reprovado 2 vezes pelo modelo de visão que estava limpo.
- **Movimentos que o Kling deforma (não peça):** porta abrindo ou fechando, pessoa entrando ou saindo de veículo, objeto passando de uma mão para outra, gente entrando pela borda do quadro. Se a cena precisa disso, mostre o "depois" já feito (ex.: passageiro já sentado) e deixe o movimento para a paisagem ou a respiração. Câmera travada quando há pessoas perto da borda.
- **Gere o enquadramento final.** Zoom de montagem acima de ~1,2x deixa o take mole. Se precisa de close, peça o close na imagem base.
- **Gancho amplo:** o personagem ocupa ~20–30% da altura do quadro (nem minúsculo, nem cortando o cenário) e o contexto que conta a dor (mesas vazias, campo seco, quadro de chaves cheio) fica legível no 1º quadro. Deixe livre a faixa onde entra o título, para ele não cobrir rosto nem corpo.
- **Continuidade:** todas as cenas de um personagem saem da mesma imagem de referência (rosto) e do mesmo cenário (estação, vegetação, luz). Já saiu praça com árvores verdes na selfie e sem folhas no gancho.
- Baixe os aprovados para `takes/` com código.

## Troca de rótulo/produto em cena (ordem obrigatória)
1. **`trocar_rotulo_faixa.py`** primeiro (grátis, não altera personagem): `--auto` acha a faixa do rótulo, `--caixa` fixa a região, `--seguir` acompanha o movimento.
2. **Kling O1 Edit** só onde a faixa não resolve (rótulo em ângulo, ilustração, tampa). Nunca em cena com rosto estilo Pixar/3D: troca o rosto ou vira fotorrealista. Se precisar mesmo, cole só a região do produto editado sobre o original (`colar_produto.py`).
   - Take de cena única com ≥3 s: `-ss ini -t dur` + `tpad=stop_mode=clone`. Nunca `-frames:v` (corta o padding e o Kling recusa).
   - Referência do produto recortada sobre fundo cinza neutro. Prompt: "@Image1 is ONLY a reference for the label design… local edit only, every pixel outside the product identical".
   - Depois `encaixar_edit.py` (24 fps → tempo original); a cópia da legenda queimada fica limitada à faixa da legenda, nunca ao quadro inteiro.
   - Custo por take; teto por AD = cenas previstas + 2. Falhou → cena vizinha, desfoque ou manter quando a marca não é legível.
3. Texto em tela de celular/legenda: `trocar_texto_tela.py`, `remendo_rastreado.py` ou `desfocar_regioes.py` (não é caso de Kling).
4. Confira cada take com zoom 3x (a folha de contato não mostra rótulo antigo reaparecendo).

## Avatar falando (HeyGen)
- Photo avatar por prompt coerente com o público (crie um por nicho e reutilize). Mesmo avatar = mesma voz em todo o lote.
- Gere o áudio no ElevenLabs (`tts_elevenlabs.py`, com alinhamento) e envie para o HeyGen fazer o lipsync do avatar; a integração ElevenLabs↔HeyGen pode falhar.
- Meça os créditos no 1º vídeo e fixe o teto por vídeo antes do resto. Polling a cada 30 s.
- Intercale B-roll de produto a cada ~10–15 s de avatar; avatar não cobre a boca com legenda (suba o enquadramento se precisar).
- Corte o hook 0,35 s após a última palavra.
- **A expressão vem da imagem base.** Avatar a partir de foto sorrindo continua sorrindo (dentes à mostra) mesmo em fala triste; expressividade baixa e prompt de "rosto sério" quase não mudam isso. Para fala de dor, gere o retrato já triste: boca fechada, cantos da boca para baixo, olhos marejados.
- **Pausas no rosto:** corte o clipe do avatar nas fronteiras das palavras e cubra as pausas com B-roll ou jump cut (zoom 1,0 ↔ 1,13). **Nunca feche a boca segurando ou fundindo quadros** no rosto: gera quadro fantasma (dois rostos sobrepostos), rosto congelado e salto. Esse retoque custou uma versão inteira refeita.
- **Lipsync sobre vídeo existente deixa o rosto mole** (perde nitidez). Cole só boca e queixo do resultado sobre o take original, com elipse suave e cor ajustada pelo anel de pele; meça a nitidez (variância do Laplaciano) contra o original.
- Job do HeyGen parado em "pending" 10–15 min é normal; acima de ~45 min, reenvie.

## Voz e narração (ElevenLabs)
- **Clonar só quando a origem é marca própria, ou criador de terceiros com autorização confirmada pela pessoa (modo B2)** (`clonar_voz.py`, trecho limpo). Antes, reutilize um clone existente da mesma voz. Nunca apague vozes.
- Terceiros sem autorização (padrão): voz de catálogo no idioma/sotaque do mercado, mesmo gênero e energia; **1 voz por criador/narrador**, mantida em todos os vídeos dele.
- Prefira `tts_elevenlabs.py --arquivo roteiro.txt -o audio/narr.mp3 --voz <nome>` (salva o alinhamento para a legenda). Pelo MCP: 1 geração, não variações.
- Velocidade ≤ 1,1x. Nome de marca que o TTS pronuncia errado → grafia fonética no texto do áudio (o roteiro e a legenda ficam com a grafia certa).
- Roteiro no idioma do mercado, sem hora do dia, sem promessa de resultado.
- **1 voz diferente por personagem** em todo o lote (a pessoa pediu: avatares distintos não dividem voz). Em agentes paralelos, registre cada escolha num arquivo comum (ex.: `_vozes.json`) **antes** de gerar, para dois agentes não pegarem a mesma.
- Sussurro: a tag `[whispers]` do eleven_v3 pode estragar palavras (nome de santo/marca). Prefira a voz normal com volume mais baixo e reverb leve na edição.
- Termo estrangeiro (latim, nome próprio): grafia fonética só no texto enviado ao TTS; legenda e roteiro com a grafia certa. Ouça/transcreva de volta.
- Voz lenta alonga o gancho (já passou de 6 para 8 s): meça a duração do áudio antes de animar o avatar e ajuste o texto, não a velocidade acima de 1,1x.
