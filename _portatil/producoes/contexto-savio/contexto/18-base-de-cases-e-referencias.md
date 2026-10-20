# Base de cases e referências (transcrições, fichas, resumos)

> O que existe na base de transcrições de podcasts, aulas e vídeos de mercado, onde fica, o que já foi resumido (VTurb #173, #174 e #176, Bid Cap, Andromeda) e como consultar com a skill `consultor-de-cases`. Abra antes de responder "alguém já fez isso?", ao validar uma estratégia ou ao processar uma transcrição nova.

## Contexto de uso

### Onde fica a base (raiz `Produtividade com ia\`)
| Pasta | Conteúdo (contagem em 13/10/2026) | Origem |
|---|---|---|
| `01-arquivos-organizados\transcricoes-youtube\` | 22 transcrições `.md` (a maioria também tem um `.txt`): VTurb "Segredos da Escala" #173, #174 e #176, mais vídeos sobre apps de Shopify, clonar loja com Claude, achar produto vencedor e conversão de loja (PT, EN, ES, DE) | `ferramentas\transcritor-youtube\` |
| `01-arquivos-organizados\transcricoes-youtube\_fichas\` | 3 fichas: #173 (Braz Cardoso), #174 (Gustavo Lopes) e "How To Clone ANY Shopify Store Design With Claude AI". **O #176 ainda não tem ficha** | `consultor-de-cases\scripts\fichar.py` + leitura |
| `01-arquivos-organizados\transcricoes-bidcap\` | 27 transcrições sobre bid cap (`.md` + `.txt`) | estudo de 03/10/2026 |
| `research_notes\Meta Andromeda criativos por ângulo\` | Notas (`oficial_meta.md`, `frameworks_persona_angulo.md`, `br_latam_facebook.md`, `jar_notas_A/B/C.md`) e transcrições (`jar_txt`, `jar_subs`, `transcricoes_en`) | estudo Andromeda de 10/2026 |
| `reports\Meta Andromeda criativos por ângulo.md` | Relatório do estudo Andromeda, com a fonte de cada regra | idem |
| `05-pdfs-didaticos\2026-09_infoproduto_resumo_vturb-segredos-da-escala-173-174.md` | Resumo dos episódios #173 e #174, com a seção "o que se aplica à nossa operação" | transcrição de 22/09/2026 |
| `05-pdfs-didaticos\2026-10_infoproduto_prompt_bid-cap-meta-ads.md` | Achados sobre bid cap + prompt pronto para o agente de anúncios | 03/10/2026 |

### O que já foi destilado (resumo; números são **declarados** pelos convidados, nunca benchmark)
- **VTurb #174, Gustavo Lopes (infoproduto, DR):**
  - a VSL é o canal de aquisição, e o lucro vem dos funis plugados atrás dela (upsell, webinário diário, ascensão ao vivo, lançamento, time comercial);
  - o funil é matemático: CPM × CTR → CPC → connect rate → play rate → retenção no pitch → conversão → ticket médio. Subir o connect rate é mais barato que subir a conversão da VSL;
  - upsell 1 = **facilitador** (~25% declarado), upsell 2 = **aproximador** (5–10%), nunca "o próximo passo";
  - produção: 80% replica o que funciona e 20% testa formato/ângulo novo;
  - o que derruba o resultado sem mudança de criativo: troca de conta de anúncio, mais Pix (sem one-click no upsell), aprovação de cartão.
- **VTurb #173, Braz Cardoso:**
  - "ângulo de mercado" (vender o resultado, não o método);
  - por causa do Andromeda, sobem 15–20 anúncios novos do zero por semana, em vez de ~90 variações;
  - ordem de manutenção quando a oferta cai: 1º quadro do criativo → 3 primeiros segundos → anúncio inteiro → headline/autoplay da VSL → lead da VSL → só então a VSL inteira;
  - conteúdo orgânico de 1:30–2:30 como aquisição.
- **VTurb #176, Fellipe Ferini (DR global):** mercados por idioma, tickets por idioma, meios de pagamento locais e localização de VSL. Resumo operacional em [20-internacionalizacao-e-gateways.md](20-internacionalizacao-e-gateways.md). O episódio foi publicado em 06/10/2026 e transcrito em 13/10/2026 (legenda automática, 2:37:54).
- **Bid cap (27 vídeos, 03/10/2026):**
  - o lance ancora no ticket, mas o multiplicador varia de 0,5× a 2× entre criadores, então não se copia número;
  - 7 dos 27 vídeos ensinam **cost cap**, não bid cap;
  - só 3 dos 27 falam de fase de aprendizagem;
  - regras de condução (cada uma vista em 1 fonte só): +10% de lance por dia se não gasta, escala de +30%, −20 a 30% se o custo passar do alvo.
- **Andromeda:** resumo oficial × mito em [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md).

### Limites da base
- Só entra quem deu certo e topou contar (viés de sobrevivência). Os convidados vendem mentoria/evento, e o canal VTurb é uma plataforma de hospedagem de VSL, então a recomendação de VSL não é neutra.
- A maioria das transcrições é legenda automática: não tem pontuação e erra termo técnico e nome próprio (ex.: "Kiwify" saiu como "KFi"/"WiFi" no #176, "Selar" como "Celar", "Gumroad" como "Gun Road").
- Os timestamps dos resumos #173/#174 não foram conferidos um a um contra o vídeo: **precisa de revisão manual** antes de citar literalmente.
- Quase tudo vem de infoproduto. COD e X1 têm pouca cobertura (ver "o que não transfere" abaixo).

## Lógica de uso

### Consultar (skill `consultor-de-cases`, fluxo A)
1. Identifique a frente da pergunta (COD, Infoproduto, X1, e-com). Isso decide o que transfere.
2. Busque **primeiro o contra-caso**: quem falhou → quem discorda → sob que condições funcionou → só então quem confirma.
3. Comece pelas fichas e depois vá ao trecho literal:
   ```bash
   cd "Produtividade com ia/.claude/skills/consultor-de-cases"
   python scripts/buscar.py "../../../01-arquivos-organizados/transcricoes-youtube" "upsell" "opcel" "opsal" --so-fichas
   python scripts/buscar.py "../../../01-arquivos-organizados/transcricoes-youtube" "upsell" "opcel" "opsal" --contexto 1 --limite 30
   ```
   Sempre passe variações do termo ("ROAS" vira "ruas"/"rost"/"Ross"). Uma busca só com o termo certo dá falso negativo, e falso negativo vira a afirmação errada "ninguém falou disso".
4. Responda com: o que a base mostra (episódio + timestamp), onde diverge, sob que condições valeu, o que não se aplica e por quê, o que a base não cobre.
5. Classifique a força: **declarado** (padrão para todo número de entrevista), **convergente** (vários casos independentes) ou **verificado** (bate com dado da própria conta).

### Regra de transferência (o erro mais caro)
Antes de recomendar, confira os pressupostos do case: recompra, custo marginal, quando o dinheiro entra, unidade de diluição (pedido × entrega × assinatura), ticket e ciclo, estrutura de time.
- **Infoproduto:** quase tudo dos episódios VTurb transfere.
- **COD:** transferem a ordem de manutenção do criativo, 15–20 criativos novos por semana, ângulo de mercado, 80/20 e a reunião semanal (com KPIs do COD). **Não transfere:** upsell, ascensão, webinário e LTV (pressupõem recompra e custo marginal zero; no COD a conta é por entrega concretizada).
- **X1:** transferem a estrutura de time comercial (founder vende primeiro, depois SDR/closer), "mostrar o progresso" no pós-entrega e a teoria das restrições.
- Se o pressuposto quebra, diga que não transfere e qual quebrou. Não adapte em silêncio.

### Processar material novo (fluxo B)
1. Transcrever: `cd ferramentas/transcritor-youtube` → `python transcritor.py add <url>` → `python transcritor.py rodar` (usa a legenda do YouTube; sem legenda, Whisper local). Custo zero.
2. Copiar ou gerar a transcrição em `01-arquivos-organizados\transcricoes-youtube\` (cabeçalho com canal, duração, publicação, URL e origem da transcrição).
3. Gerar o esqueleto da ficha: `python scripts/fichar.py <transcricao.md>` ou `python scripts/fichar.py <pasta> --lote` (saída em `_fichas/<nome>.ficha.md`).
4. Ler por fatias e preencher os `[PREENCHER]`. **"Erros e contra-exemplos" e "Limites" nunca ficam vazios.** Dado decisivo: conferir no vídeo pelo timestamp.
5. Se o tema for operacional, registrar o resumo no `contexto/` certo (ex.: o #176 foi para o arquivo 20) e uma linha aqui.

### Bid cap: como usar o prompt pronto
- O prompt da seção "PROMPT PARA O AGENTE DE ANÚNCIOS" do arquivo `2026-10_infoproduto_prompt_bid-cap-meta-ads.md` serve como regra operacional para um agente de anúncios de infoproduto.
- Ordem: separar bid cap de cost cap → derivar o **CPA máximo** da economia da oferta (ticket − taxa − entrega − reembolso + contribuição do upsell medido) → CPA alvo = máximo − margem → lance inicial = CPA alvo.
- Sem CPA máximo: parar e pedir. Uma variável por vez. Toda regra de fonte única vai como "prescrição isolada, não validada".

### Pendências
- Ficha do #176: gerar com `fichar.py` e preencher (**precisa de revisão manual**).
- Fichas das transcrições de Shopify e de bid cap: não existem.

## Relacionados
- [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md)
- [13-analise-meta-ads-e-vencedores.md](13-analise-meta-ads-e-vencedores.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [20-internacionalizacao-e-gateways.md](20-internacionalizacao-e-gateways.md)
