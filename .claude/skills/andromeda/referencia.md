# Referência Andromeda (regras de trabalho)

Resumo operacional do estudo de 10/2026. Fonte e link de cada item: `02-relatorios/reports/Meta Andromeda criativos por ângulo.md`.
Números de praticante são **ponto de partida para calibrar com dados da conta**, não benchmark. Quando os dados
da conta contradisserem esta página, vale o dado, e a contradição vai para `contexto/estrategias-criativos.md`.

## 1. O que é oficial × o que é mito

| Afirmação | Status |
|---|---|
| Andromeda é o motor de **retrieval**: reduz dezenas de milhões de anúncios a alguns milhares para o ranking (GEM/Lattice) | Oficial (Meta, 12/2024) |
| Diversificar mensagem, visual e formato é a principal alavanca; o criativo faz a segmentação | Oficial (Performance 5, white paper "The Creative Advantage", Blueprint) |
| Diversidade de formato + mensagem: até −32% CPA, +9% alcance incremental | Oficial (estudo Meta + AppsFlyer + Dentsu, via imprensa) |
| Anúncios que "parecem ou soam iguais" contam como variações do mesmo criativo | Oficial qualitativo, sem critério publicado |
| Desde 2026, LLMs no retrieval leem o conteúdo do anúncio (Generative Recommender) | Oficial (earnings Q2/2026), mecanismo não detalhado |
| Métrica "Creative Similarity" no Ads Manager | Real, "em desenvolvimento", só visual, sem limiar público. Não otimizar para ela |
| "Entity ID", "1 ticket no leilão", limiar 60%/40% | **Mito de agência.** Usar só como metáfora |
| "8–15 conceitos por campanha" / "10–20 por conjunto" como regra da Meta | **Heurística de praticante** |

## 2. Consenso × divergência

- **Consenso:** público aberto (a localização é o único controle rígido); estrutura consolidada; conceito novo vale
  mais que variação mínima; não desligar cedo o anúncio de CPA ruim que recebe verba (pode ser o topo do funil).
- **Divergem (escolher pela verba e pelo modelo de venda):**
  - Anúncios por conjunto: de 3 a 50. Com verba baixa, 3–6 por conjunto; o que importa é o nº de **conceitos**.
  - Teste separado da escala: separar protege vencedores com verba alta; com verba baixa, consolidar evita
    fragmentar o sinal.
  - ABO para garantir verba a conceito novo; CBO/Advantage+ para escalar.
  - Trocar só o gancho: conta só com **plano de abertura visual novo** e coerente com o corpo.
  - Melhorias automáticas do Advantage+ Creative: desligar em saúde/estética (a IA pode reescrever promessa).

## 3. Matriz de conceitos (colunas)

Uma linha = um conceito; 2–3 execuções visualmente distintas por conceito.

`ID | modelo de venda / país | persona (identidade + micro-momento) | ângulo | desejo central | consciência |
estado mental | formato 1 | formato 2 | formato 3 | elenco/voz (idade, sotaque) | abertura visual | oferta/CTA |
risco de compliance | hipótese em 1 frase`

- **Ângulos:** dor/alívio, aspiração/status, prova/autoridade, mecanismo, ocasião, oferta/remoção de risco,
  quebra de objeção, comparativo, identidade/tribo, rotina, sensorial.
- **Consciência (Schwartz):** inconsciente → consciente do problema → da solução → do produto → pronto para comprar.
- **Estado mental (Levinger):** gatilho → exploração → avaliação → compra.
- **Conceito = persona + ângulo + oferta.** O formato vem por último ("o que funciona é o que vai dentro dele").
- **O elenco segmenta:** idade, sotaque e aparência de quem aparece puxam a entrega para aquele público, e essa
  relevância deve continuar na página/quiz/conversa.
- **Remoção de risco é ângulo, não rodapé:** "paga ao receber", "recebe antes e paga depois" e a garantia
  sustentam um conceito próprio.
- **Personas entre si:** mesmo produto para outra persona = outro desejo, outra cena, outro elenco. Mudar só a
  legenda não cria persona nova.

## 4. O que conta como criativo diferente

| Mudança | Conta? |
|---|---|
| Cor, fonte, título, uma palavra, música de fundo | Não |
| Mesma filmagem com legenda/texto na tela novo | Não |
| Mesmo talento, cenário e enquadramento com roteiro revisado | Não |
| Mesma pessoa trocando a roupa e repetindo a fala | Não |
| Re-subir ou limpar metadados | Não |
| Gancho só em texto sobre a mesma abertura | Não |
| Gancho com plano de abertura visual novo, coerente com o corpo | Provavelmente sim |
| Outra pessoa (idade, corpo), outro cenário | Sim |
| Outro formato (talking head × demonstração × carrossel × estático × advertorial) | Sim |
| Outra voz, narração × silêncio, outra estrutura narrativa | Sim |
| Outra proposta de valor, desejo, consciência ou persona | Sim (conceito novo) |

- **Regra do lote:** ≥ 4 famílias, cada uma diferente das outras em ≥ 2 dimensões (formato, visual/elenco/cenário,
  mensagem principal).
- **Testes rápidos:** grade de primeiros quadros (`scripts/aberturas.py`); na entrega, quase todo o gasto em
  1–2 anúncios com as variações deles sem impressão é **indício** de agrupamento; frequência > 2 em público frio.
- **Matriz gancho × corpo** (variações montadas de um banco de tomadas): cada gancho precisa de **cenas de
  abertura diferentes** do banco e do mesmo assunto que o corpo; trocar só a legenda do gancho sobre o mesmo
  plano tende a ser agrupado.
- **Calibração do `aberturas.py`** (lote real de 12 ADs gancho × corpo, 10/2026): mesmo gancho = 0,89–1,00;
  ganchos diferentes = 0,45–0,64. Limiar padrão 0,85.

## 5. Teste e escala por modelo de venda

**Base comum (praticantes, calibrar):**
- Verba de teste por conjunto ≥ 3× o CPA-alvo; julgamento em blocos de 7 dias.
- Corte: gasto de 2× o CPA-alvo sem conversão, ou 7 dias sem conversão. Julgar o **conjunto** antes do anúncio.
- Escala: +10% 1–3×/semana (−15% se passar do CPA) ou +20% a cada ~4 dias. Pré-requisito: ≥ 4 vencedores
  diferentes entre si.
- Volume: com gasto < US$ 10 mil/mês, ~8–12 conceitos distintos/mês; taxa de acerto típica de 4–6% ⇒ ~1 vencedor
  a cada 16–25 criativos. Orçar o lote, não o criativo avulso.
- Ferramenta nativa "Creative testing" (2–5 versões, ≤ 20% da verba) para detalhe: gancho, cor, texto.
- Não fazer: anúncio novo contra vencedor com histórico; pausar os antigos ao subir novos; adicionar anúncio em
  conjunto que está batendo meta.

| | Pagamento na entrega | Funil digital (VSL/quiz → checkout) | Venda por conversa (mensagem) |
|---|---|---|---|
| Unidade de campanha | País × produto | Oferta × mercado | Oferta × mercado |
| Lançamento | 4–6 ângulos × 2–3 execuções (8–12 ativos); ângulo com > 60% do gasto ganha campanha própria | 3 ângulos por perfil × 5–6 tipos de criativo | 8–15 anúncios (estático, carrossel, vídeo) por nível de consciência; início agendado ≥ 12 h após criar |
| KPI de decisão | CPA por **pedido entregue/pago** e margem, cruzado por ângulo (o gerenciador só vê o pedido) | CAC do front + upsell | Custo por **venda paga**; fechamento por atendente |
| Guardrails de topo | CTR > 0,8%; pedidos iniciados 10–12% das visitas; conversão > 3% | Baseline próprio | Baseline próprio |
| Formatos-chave | Pessoa local com sotaque, demonstração, entrega e pagamento na porta | VSL curta, advertorial/quiz como anúncio, depoimento | Estático com copy longa, VSL, depoimento de par etário (público mais velho) |
| Atribuição | 7d clique / 1d view | Padrão | Evitar 1d view (compra demora dias) |
| Etiqueta obrigatória | Ângulo no nome do anúncio, ligado ao pedido | Persona/ângulo até a página | ID do anúncio/conceito em cada conversa |

## 5b. Leitura do funil por anúncio (método JarBuildsBrands, praticante)

O criativo decide em que etapa o anúncio roda. Antes de cortar, classifique cada anúncio pela "assinatura"
de métricas e julgue o time, não o jogador.

| Etapa | Gasto | CPM | Frequência **diária** | CPA / ROAS atribuído | Formatos típicos |
|---|---|---|---|---|---|
| Topo | alto | baixo | 1,00–1,10 | CPA alto, ROAS baixo, muito público novo | reação, teste em público, história, educativo, fundador mostrando o produto |
| Meio | médio | médio | 1,15–1,20 | médio | demonstração, unboxing, perguntas frequentes |
| Fundo | baixo | alto | 1,25–1,5+ | CPA baixo, ROAS alto | estático de oferta, kit, "últimas unidades" |

- Frequência no **dia**, não no período (no período engana). Custo por engajamento barato com muito
  engajamento também indica topo.
- **Não corte o topo por CPA atribuído:** ele alimenta o fundo; cortar "seca o funil" e o fundo piora junto.
  O anúncio que mais gasta costuma ter o pior ROAS atribuído e a maior fração de visitantes novos.
- **Diagnóstico pelo elo mais fraco:** topo fraco → mais criativos de topo; sem fundo → estáticos de oferta.
- Gasto concentrado em poucos anúncios é normal (top 3–5% levam a maior parte); não force gasto igual.

## 5c. Outras regras do JarBuildsBrands (praticante, e-commerce pré-pago nos EUA; adaptar)

- **Duas alavancas:** criativo (pré-clique, traz o clique certo) e oferta/página (pós-clique, vende). Oferta
  para caber no CAC: kits, "leve 2", brinde, garantia; testar oferta e página por **lucro por visitante**.
- **Ficha de conceito:** hipótese + persona + ângulo + desejo + nível de consciência + **sofisticação do
  mercado** (Schwartz). Roteiro descendo a escada de consciência. Mensagem acima de estética. Começar pelo
  formato mais barato (estático/foto) e só produzir vídeo do conceito que deu sinal.
- **Mesmo roteiro gravado por várias pessoas** (idade, gênero, etnia diferentes) para abrir "bolsões" de
  público; trocar só cor/legenda não abre.
- **Metas pela economia da unidade:** ROAS-alvo ≈ ROAS de equilíbrio × 1,2; decidir por margem de
  contribuição e receita total ÷ gasto total (MER), acima do ROAS da plataforma; piso de gasto que pague o
  custo fixo.
- **Cadência estável:** revisão semanal com 7 dias de dados; 1–2 mudanças por semana; uma variável por vez;
  3–7 dias para ler o efeito; não mexer por um dia ruim.
- **Escala (versão mar/2026):** decisão diária pela média de 3 dias × meta: acima → +20% (ou +10% se mal
  passou); abaixo mas 7 dias acima → manter; ambas abaixo → −20%, salvo se já estiver no piso de gasto.
- **Escala (versão out/2026, mais recente):** 1 campanha CBO por objetivo de negócio, conjuntos só quando a
  economia muda (produto/oferta/ticket diferente), muitos anúncios por conjunto, sem campanha de teste,
  **controle de custo** (cost cap ou ROAS mínimo) no conjunto com orçamento diário bem acima do gasto normal
  (vira teto), ajustar lance em vez de orçamento, e **não desligar anúncios**. Ele não mostra como calibrar o
  lance (fica na comunidade paga): ponto de maior risco de copiar.
- **Ele mudou de opinião** (registrar ao citar): "pequenas variações ajudam" (out/2025) → "pequena variação =
  mesmo anúncio" (nov/2025); "matar e lançar toda semana" (mar/2026) → "não mato anúncios" (out/2026);
  "~3 conceitos/semana, sniper" (jan/2026) → "volume e variedade com IA" (fev–out/2026); e "se bate a meta,
  só sobe orçamento, sem criativo novo" (out/2025, contrário ao mercado).

**Ajuste obrigatório para pagamento na entrega e venda por conversa:** cost cap, "não matar" e média de 3 dias
só funcionam se o evento que o Meta otimiza representar dinheiro de verdade. Em pagamento na entrega o evento é
o pedido, não a entrega paga; em conversa, é o lead. O CPA-alvo do lance precisa embutir a efetividade
(CPA por pedido aceitável = CPA por entrega paga aceitável × efetividade) e a leitura de 3 dias engana quando a
entrega só confirma dias depois. Sem conversão de valor real devolvida ao Meta (API de conversões com entrega ou
pagamento confirmado), o lance otimiza para o evento errado.

## 6. Erros comuns
1. Dezenas de variações quase iguais ("50 anúncios disputando 1 vaga").
2. Fragmentar a estrutura (públicos empilhados, remarketing em camadas, 1-3-1).
3. Confundir agrupamento por similaridade com fadiga e "refrescar" com variação, quando a saída é criador,
   cenário e formato novos.
4. Comparar novo contra vencedor com histórico; pausar os antigos ao subir novos.
5. Começar pelo formato, não pelo ângulo.
6. Mirar o nível de consciência errado (falar de produto com quem nem reconhece o problema).
7. Escalar agressivamente sobre os mesmos criativos.
8. Culpar o algoritmo sem checar página, oferta, sazonalidade.
9. Decidir pelo CPA do gerenciador quando o modelo de venda paga na entrega ou na conversa.

## 7. Compliance (saúde, suplemento, estética, público mais velho)
Fonte secundária; conferir a política vigente da Meta antes de virar regra.
- **Atributos pessoais:** proibido afirmar ou insinuar que o usuário tem uma condição ("sua dor no joelho",
  "você tem X?"). Escrever em 3ª pessoa, narrativa ou depoimento de personagem; persona por **situação**, não
  por diagnóstico.
- **18+** para dieta, saúde, emagrecimento e suplementos.
- **Antes/depois:** permitido para cosmético (18+); proibido em emagrecimento.
- **Cura:** não alegar "curar/eliminar"; "aliviar/controlar sintomas" é permitido.
- **Sinais de saúde:** não nomear públicos personalizados ou conversões com o nome de condição.
- **Crença/religião:** evitar 2ª pessoa sobre a fé ou a situação do usuário (sem regra específica confirmada).
- **Decisão de suavizar é da pessoa:** listar riscos e perguntar manter × suavizar.
