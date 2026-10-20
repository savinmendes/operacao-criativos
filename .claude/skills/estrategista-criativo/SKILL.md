---
name: estrategista-criativo
description: Transforma criativos vencedores, referências (reels, canvas do Flora, anúncios) e um produto/oferta em um plano de produção pronto (formato, roteiro por take, ângulos, macetes de retenção, orçamento e teste), seguindo as estratégias da operação registradas em contexto/. Use sempre que a pessoa mandar vencedores ou referências e pedir "faz um pra esse produto", "estuda esse vídeo", "como seria", "adequa às nossas produções", ou quiser planejar um criativo/lote antes de produzir.
---

# Estrategista de criativo

Camada de estratégia: decide O QUE produzir e COMO. A execução fica com `gerar-midia-ia` (imagens, takes, voz),
`editar-criativo` (montagem), `revisar-criativo` (QA) e, em lotes, `traduzir-criativo`/`adaptar-marca`.

## 0. Carregar o contexto (sempre primeiro)
- Leia `contexto/estrategias-criativos.md`: formatos que já venceram, pipeline de IA validado, custos medidos,
  armadilhas e decisões de compliance já tomadas. É a memória estratégica — a skill não guarda dados de produto.
- Leia o que existir da oferta (página do produto, `09-notion-sync/`, memória do projeto). Preço, oferta,
  estoque e garantia só entram se estiverem numa fonte; senão, "confirmar com a pessoa".
- Identifique a frente (COD / Infoproduto / X1), o mercado e o idioma. Não misture lógicas entre frentes.

## 0.5 Checklist de abertura (numa mensagem só, antes de produzir qualquer coisa)
Leia a "Retrospectiva" e o "Checklist de abertura" em `contexto/estrategias-criativos.md` e pergunte de uma vez
apenas o que ainda não estiver respondido:
- oferta fechada (mecânica, **fala preço ou não**, escassez real, tema sazonal);
- mercado/idioma e avatar ou cena base;
- referências (arquivos ou links da Biblioteca de Anúncios);
- **orçamento diário de mídia** (dimensiona o volume) e teto de produção;
- música e formatos.
Enquanto a resposta não chega, adiante só o estudo, que é grátis. Não produza roteiro nem overlay com oferta em aberto.
As decisões ficam numa lista única; não repita a mesma pendência em várias mensagens.

## 1. Estudar as referências (grátis, em paralelo)
Dispare agentes em paralelo (um por fonte) e registre no painel.
- **Vencedores**: baixe na maior qualidade (≥720p; Meta: `video_hd_url`; posts do Facebook com Playwright,
  que pede login após ~2 posts — avise e siga com os que vieram). Para cada um: folha de contato, transcrição
  com timestamps, cortes de cena (`scdet`). Decomponha: gancho (tipo, duração), corpo (estrutura por bloco),
  CTA, legenda, faixas/adesivos fixos, ritmo de corte, voz, texto do anúncio.
- **Canvas do Flora**: leia via `flora_get_canvas` (dump grande → subagente parseia o JSON). Extraia modelos,
  cadeias (nó → nó), prompts-padrão verbatim, fases e o que fica fora do Flora.
- **Reels/aulas de referência**: extraia os macetes acionáveis (não o conteúdo) e diga como cada um vira
  decisão de edição ou de geração.
- Saída do estudo: tabela "o que o vencedor faz → como replicamos → ferramenta".

## 2. Desenhar o criativo
- Estrutura por take: nº, cena/local, enquadramento (aberto, médio, close, detalhe, plano baixo, lateral),
  ação/movimento, fala no idioma do mercado e duração. Máx. ~20 palavras a cada 8 s de fala.
- Aplique os macetes de retenção da lista de `contexto/estrategias-criativos.md` (ângulo novo por frase,
  movimento no 1º quadro, título grande antes da fala, legenda palavra a palavra, zoom rápido no rosto nos cortes, inserções por cima da fala,
  CTA claro). Diga quais entram na geração e quais entram de graça na edição.
- **Consistência**: mesma persona, roupa e voz em todo o vídeo. Se cada take for gerado à parte, a voz muda —
  resolva com voz única (ElevenLabs) + lipsync, ou com modelo que aceite áudio de entrada.
- Combine material real (banco de takes de mãos/produto, sem rosto nem marca d'água) com IA onde faltar.
- Texto do anúncio + 3 títulos no estilo do vencedor.

## 3. Compliance (perguntar, não decidir)
Liste os riscos (promoção sem condição real, depoimento encenado por IA, "original/certificado", estoque
limitado sem dado, promessa de resultado, marca de terceiros) e pergunte manter × suavizar. Registre a
decisão em `contexto/estrategias-criativos.md` para não perguntar de novo.

## 4. Orçamento e teste
- Apresente 3 abordagens (prós, contras, custo em US$, tempo) e recomende uma.
- Use preços medidos no contexto (o Flora cobra por segundo de vídeo e por resolução de imagem; a cotação do catálogo
  costuma vir abaixo do cobrado). Peça aprovação só quando houver gasto real.
- **Teste antes do lote** quando o método for novo ou caro: 1 cena/bloco, mostre e espere o aprovado.
  Método já validado e barato → todos em paralelo.
- Ao fim, informe o custo real e atualize os preços em `contexto/estrategias-criativos.md`.

## 4.5 Padrões de produção (evitam retrabalho já vivido)
- Transcreva cada take gerado por IA **antes** de usar: idioma, palavras parecidas com o português, nomes de marca.
- Voz única: clone a voz do gancho aprovado e converta a fala de cada take (speech-to-speech), mantendo o tempo.
- Legenda sempre pelo texto do roteiro, com alinhamento forçado no áudio limpo de cada segmento. Nunca pelo whisper do vídeo montado.
- Música de fundo baixa (cama, cerca de -32 LUFS sob a fala, com ducking).
- Variações têm que mudar algo de verdade (gancho, formato); nada de quase-duplicata.
- Ferramenta compartilhada (montador, mixador) é alterada por um agente de cada vez.
- Entrega em loja/site: grave numa cópia do tema, teste pela prévia, a pessoa publica. Depois mande a URL exata e onde está.
- Ao fechar: pasta de teste com N criativos = o que o orçamento de mídia comporta, nomes no padrão do gerenciador e estrutura de campanha em txt.

## 5. Registrar o aprendizado
Ao terminar (ou quando a pessoa aprovar/reprovar algo), acrescente em `contexto/estrategias-criativos.md`:
formato que venceu, macete validado, custo medido, armadilha nova, decisão de compliance. Só fatos
observados, com data.
