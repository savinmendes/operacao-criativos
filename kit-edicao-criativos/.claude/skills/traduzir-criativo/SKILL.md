---
name: traduzir-criativo
description: Adapta um lote de criativos de vídeo de um idioma/mercado para outro (ex.: inglês → espanhol LATAM) — estudo do lote, briefing único para agentes em paralelo, narração nova sem rosto de terceiro falando, legenda queimada coberta, CTA e selo do mercado novo, revisão e entrega com relatório. Use quando pedirem para traduzir, dublar, "passar para espanhol" ou adaptar vídeos de outro país.
---

# Traduzir criativo

Fluxo de lote. Montagem, geração de mídia e revisão seguem `editar-criativo`, `gerar-midia-ia` e `revisar-criativo`; aqui só está o que é próprio da tradução. Leia antes o `CLAUDE.md` do kit (seção "Tradução de criativo de outro idioma" e as armadilhas). Nunca leia nem imprima `.env`.

## 1. Estudo do lote (antes de gastar qualquer coisa)
1. Baixe sempre na **maior qualidade disponível (≥720p)**: na Biblioteca do Meta, o `video_hd_url` dos dados da página, não o vídeo do player (360p); confira com `ffprobe` e deduplique por md5. Renomeie os originais para `originais/NN.mp4` e gere `indice-arquivos.csv` (nome original → NN).
2. Agentes em paralelo (1 por 3–6 vídeos), cada um com: transcrição faster-whisper (idioma automático, `cpu_threads=4`), folha de contato (1 quadro/s) e leitura dos quadros em tamanho cheio. Whisper e OCR em sequência, nunca juntos.
3. Para cada vídeo, listar o que **não serve** no mercado alvo: preço/moeda, país e bandeira, plataforma de origem (carrinho, "link abaixo"), cupom/desconto, data/estação/feriado, escassez não comprovável ("esgotou X vezes"), claims fora da ficha oficial, rosto de criador de terceiro, legenda queimada, dados pessoais em cena (rosto de terceiro, data/hora, número de casa, @perfil), medidas em unidade estrangeira.
4. Marcar duplicados (mesmo roteiro, filmagem diferente) e classificar: **A** sem rosto (só mãos/produto), **B** com rosto do criador, **C** outro produto.
5. Entregar `ESTUDO-<lote>.md` com: tabela por vídeo, lista de alegações proibidas, classificação, orçamento (custo em US$ + tempo + opção paga mais rápida, lado a lado) e as **perguntas de bloqueio**: a marca é da pessoa ou revende a original? ficha técnica oficial (link)? oferta e países (COD, frete, garantia, preço)? quais vídeos excluir? **criadores com rosto (grupo B): avatar próprio (B1, padrão) ou o mesmo criador (B2, só com autorização do criador)?** Sem essas respostas, não produzir.

## 2. Briefing único do lote
Escreva `producao/_trabalho/BRIEFING-AGENTES.md` e passe o mesmo arquivo a todos os agentes (1 agente por 1–2 vídeos). Conteúdo obrigatório:
- onde estão originais, transcrições, folhas, kit e o exemplo pronto de um lote anterior;
- **ficha oficial** (só o que pode ser dito) e a lista de trocas fixas ("funciona sem X" → frase segura; medida → unidade local);
- regra de marca: fica se a pessoa vende a original; senão desfocar/cobrir/Kling;
- **CTA** falado + palavra das setas; oferta só se confirmada (sem preço, país, frete ou garantia inventados);
- **voz**: narrador de terceiro → voz de catálogo (mesmo gênero e energia, a mesma em todos os vídeos do mesmo criador); clonar só no modo B2 (autorização do criador confirmada); marca própria → clone permitido (`clonar_voz.py`);
- fluxo A e B, limites de CPU/GPU (`-threads 4`, `PYTHONIOENCODING=utf-8`), teto de créditos por vídeo, revisão obrigatória e formato do relatório;
- "não pergunte nada; na dúvida escolha o lado seguro e registre a decisão".

## 3. Grupo A (sem rosto)
1. `python -m demucs --two-stems=vocals` → usar só o `no_vocals.wav` (GPU liberada: `-d cuda`). Se a voz original ainda vazar no fundo, entregar sem trilha e anotar.
2. Roteiro no idioma alvo com a **mesma estrutura** (gancho, benefícios, CTA), ~15% mais curto que o original, sem o que o estudo listou. Salvar `adNN/roteiro_<idioma>.txt`.
3. `tts_elevenlabs.py --arquivo roteiro.txt` (gera o alinhamento). Não cabe? Enxugue o texto ou estique cenas com congelamento curto; velocidade da voz ≤ 1,1x; frase a frase no tempo das cenas.
4. `preparar_corpo_traducao.py prep.json` (modelo em `exemplos/traducao_exemplo.json`): corta a capa, cobre a legenda queimada com faixa opaca (alpha ≥ 250) e o título do gancho com caixa nova, troca o áudio (fundo + narração), gera o alinhamento deslocado. Cenas proibidas: cortar ou `desfocar_regioes.py`.
5. `montar_ad.py` em `"resolucao": "720"` com legenda pelo alinhamento e setas na palavra do CTA; `revisar_ad.py` no final.

## 4. Grupo B (rosto do criador) — a pessoa escolhe o modo por lote ou por vídeo
**B2 — mesmo criador** (só quando a pessoa confirma que o criador autorizou o uso de imagem e voz para fala nova/tradução: contrato, licença de UGC ou permissão direta):
- Registre no estudo e no `RELATORIO.md`: "uso do criador autorizado pela pessoa em DD/MM/AAAA" e quais vídeos.
- Voz: `clonar_voz.py` a partir de um trecho limpo do criador (1 clone por criador, reutilizado em todos os vídeos dele) → `tts_elevenlabs.py` com o roteiro traduzido.
- Rosto: lipsync do HeyGen sobre o vídeo original (ou tradução de vídeo do HeyGen com o roteiro revisado), medindo créditos no 1º. Cubra a legenda queimada e siga o grupo A no resto.
- Sem autorização confirmada, **não** use B2: vá de B1.

**B1 — avatar próprio** (padrão):
- Nada de lipsync nem fala nova sobre o rosto real.
- Reaproveite só takes sem o rosto (produto, mãos, app, gravações); recorte 9:16 abaixo do rosto quando preciso.
- Parte falada com **avatar próprio** (HeyGen, via `gerar-midia-ia`): áudio do `tts_elevenlabs.py` enviado para o lipsync do avatar. Meça os créditos no 1º vídeo e fixe o teto antes de rodar os outros.
- `montar_corpo_avatar.py plano.json`: intercala avatar (~40–60%) com os takes sem rosto (tela cheia ou dividida), depois `montar_ad.py` + `revisar_ad.py`.

## 5. Selo de oferta
Só com oferta confirmada pela pessoa. Sem confirmação, deixe `adNN/receita_com_selo.json` pronta (selo "pago contra entrega" ou o da oferta) e registre no relatório que falta renderizar.

## 6. Revisão (por vídeo final)
`revisar_ad.py` + Whisper no idioma alvo (texto bate com o roteiro; nenhum item proibido) + Whisper no idioma original (nenhuma fala antiga por baixo) + folha de contato 1 quadro/s (nenhuma legenda antiga, quadro solto no corte, silêncio no fim, seta sobre a faixa). Depois `revisar-criativo`.

## 7. Entrega
- Pasta numerada: `producao/AD NN - <PRODUTO>-<TEMA>-<IDIOMA>-<MERCADO>.mp4`, trabalho em `producao/_trabalho/adNN/` com `RELATORIO.md` (voz usada, caracteres TTS, créditos, o que saiu/trocou, revisão, pendências).
- `producao/00-RELATORIO-PRODUCAO.md`: custo real × orçado, decisões aplicadas a todos, tabela de ADs, lista "para você olhar" (revisão manual), bugs do kit encontrados.
- Textos de anúncio por AD: título, descrição, texto principal e versão TikTok ≤ 100 caracteres, com compliance.
- Atualize a memória do projeto (lote, método, pendências) para o próximo lote partir daqui.
