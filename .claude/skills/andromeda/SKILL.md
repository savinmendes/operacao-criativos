---
name: andromeda
description: Especialista em diversidade criativa e estrutura de campanha na era Meta Andromeda. Três modos — (1) planejar: monta a matriz persona × ângulo × consciência × formato de um produto e aponta lacunas; (2) auditar: antes de subir, confere se os criativos de um lote são diferentes de verdade (abertura, pessoa, cenário, formato, mensagem) ou se tendem a ser agrupados como o mesmo anúncio; (3) ler resultado: julga por conjunto e por eixo (persona/ângulo/formato), diz o que escalar, manter, cortar e qual conceito falta. Use quando a pessoa falar em Andromeda, diversidade criativa, "esses criativos estão parecidos?", quantos criativos subir, estrutura de campanha/teste/escala no Meta, vender o mesmo produto para públicos diferentes, ou antes de subir um lote de criativos.
---

# Andromeda: diversidade criativa e estrutura

O público agora é escolhido pelo criativo: idade e sotaque de quem aparece, a dor que o gancho nomeia, a promessa
que o corpo sustenta. Esta skill decide **quais conceitos** um produto precisa e **se o lote é diverso de verdade**.
Não escreve roteiro nem edita:
- roteiro por take, formato e orçamento de produção → `estrategista-criativo`;
- leva de ganchos → `esteira-de-hook`; ângulos minerados do mercado → `mineracao-angulo`;
- texto/copy → `analista-de-copy`; peça quebrada (hook/corpo/CTA/página) → `diagnostico-criativo`;
- QA técnico do vídeo → `revisar-criativo`.

## 0. Contexto (sempre primeiro)
- Leia `referencia.md` (nesta pasta): o que é oficial da Meta × mito de agência, regras de diversidade,
  teste/escala por modelo de venda e compliance. Para fonte e link de cada regra, o estudo completo fica em
  `02-relatorios/reports/Meta Andromeda criativos por ângulo.md` (se existir).
- Leia `contexto/estrategias-criativos.md` e `contexto/banco-de-copy.md` (vencedores, personas e ângulos já
  testados, decisões de compliance). A skill não guarda dado de produto: tudo vem dessas fontes ou da pessoa.
- Identifique o **modelo de venda** (pagamento na entrega / funil digital com checkout / venda por conversa),
  o mercado/país, o idioma e a oferta. Nunca misture as regras de um modelo com as de outro.
- Tarefa longa: registre as etapas no painel do projeto, se existir (`painel/painel.py etapa|fim ...`).

## Modo 1 — Planejar (matriz de conceitos)
1. **Pesquisa antes do formato.** Junte a linguagem real do cliente: avaliações, comentários de anúncio,
   conversas de atendimento, pesquisa de mercado já feita. Sem isso, marque as personas como hipótese.
2. **Personas por identidade e micro-momento**, não por demografia ("quem chega cansado e não quer cozinhar",
   não "mulher 25–34"). 2–4 personas por lote, priorizadas por dor e sazonalidade.
3. **Matriz** (uma linha = um conceito; colunas em `referencia.md` §3): persona, ângulo, desejo, nível de
   consciência, sofisticação do mercado, estado mental, etapa do funil que o conceito deve ocupar, 3 formatos, elenco/voz, abertura visual, oferta/CTA, risco de compliance e a
   **hipótese em 1 frase**. Conceito = persona + ângulo + oferta; o formato vem por último.
4. **Lacunas:** aponte o que falta. Níveis de consciência sem cobertura, persona sem elenco correspondente, só um
   formato, nenhum ângulo de oferta/remoção de risco, só um estado mental.
5. **Tamanho do lote** pela verba e pelo modelo de venda (`referencia.md` §5). Com verba baixa, menos conceitos
   bem diferentes valem mais que muitas variações.
6. Saída: a matriz preenchida + a lista de lacunas + a recomendação de quantos conceitos e execuções produzir.
   Entregue para `estrategista-criativo` transformar em roteiro.

## Modo 2 — Auditar o lote antes de subir
1. **Abertura visual (automático, sem custo):**
   `python .claude/skills/andromeda/scripts/aberturas.py <pasta-do-lote> --saida <pasta>/_andromeda`
   - Gera `aberturas.json` (similaridade 0–1 entre aberturas) e `aberturas_grade.jpg` (quadros 0,2 s, 1 s e 2 s
     de cada vídeo). Sai com código 1 quando acha par acima do limiar.
   - Limiar padrão 0,85. É um sinal de que "parece igual na grade", não o critério da Meta, que não é público.
     Abra a grade e confirme com os olhos antes de condenar um par.
2. **Ficha por criativo:** para cada anúncio, preencha persona, ângulo, consciência, formato, elenco, cenário,
   voz e mensagem principal. Use o nome do arquivo, o roteiro ou a transcrição, nunca a memória.
3. **Agrupe em famílias.** Dois criativos são da mesma família quando mudam só cor, texto, título, música,
   legenda, camiseta ou o gancho escrito sobre a mesma cena (`referencia.md` §4). A meta é **≥ 4 famílias, cada
   uma diferente das outras em ≥ 2 dimensões** (formato, visual/elenco/cenário, mensagem).
4. **Coerência:** gancho fala do mesmo assunto que o corpo; persona do anúncio continua na página/quiz/saudação
   da conversa; elenco e sotaque batem com o país.
5. **Compliance:** liste riscos (`referencia.md` §7). **Não suavize sozinho**: pergunte manter × suavizar.
6. Saída: tabela criativo × família × dimensões; a lista "parecidos demais → refazer o quê" (ex.: "AD 05 e AD 06
   abrem com a mesma cena: trocar a abertura de um por outra cena/pessoa"); as lacunas da matriz; e o veredito
   (pode subir / subir com ressalvas / refazer N peças).

## Modo 3 — Ler o resultado
1. **Dados** pelo conector de anúncios (gasto, impressões, CPM, frequência, hook rate, retenção, CTR, CPA) e,
   quando o modelo de venda pede, pela fonte operacional (entregas/pagamentos, vendas fechadas). Sem dado, diga
   a limitação; **nunca invente métrica**.
2. **KPI de decisão do modelo de venda**, não o do gerenciador (`referencia.md` §5): pedido entregue/pago,
   CAC com upsell ou venda paga por conversa.
3. **Julgue o conjunto primeiro.** Anúncio com CPA ruim dentro de conjunto que bate meta pode estar fazendo o
   papel de topo: não corte por padrão. Classifique cada anúncio como topo/meio/fundo pela assinatura de
   métricas (`referencia.md` §5b: frequência diária, CPM, custo por engajamento) e aponte o elo mais fraco do
   funil. Corte só pelos critérios de gasto/tempo da referência.
4. **Leia por eixo:** some por persona, ângulo, consciência e formato (o nome do anúncio precisa carregar isso).
   Sinais de agrupamento: quase todo o gasto em 1–2 anúncios e as variações deles sem impressão; frequência > 2
   em público frio.
5. Saída: escalar / manter / cortar / substituir, com evidência (anúncios e números) e confiança; o conceito que
   falta para o próximo lote (volta ao Modo 1).

## Registrar
- Acrescente em `contexto/estrategias-criativos.md` as personas e ângulos validados ou reprovados, com data,
  mercado, anúncios de origem e confiança. Só fatos observados.
- Análise longa: relatório em `02-relatorios/` no padrão de nomes do projeto.
- Ao achar uma regra da referência que os dados da conta contradizem, anote a contradição em
  `contexto/estrategias-criativos.md`: o dado próprio vale mais que a heurística de mercado.
