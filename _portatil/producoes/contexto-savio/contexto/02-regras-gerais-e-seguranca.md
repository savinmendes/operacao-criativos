# Regras gerais e segurança

> Regras fixas do projeto: segurança de arquivos e dados, nomes de arquivos, estrutura de pastas, inbox, como montar apresentações/relatórios/dashboards, formato visual certo, ordem de prioridade e checklist final. Abra antes de gerar qualquer saída ou mexer em arquivos.

## Contexto de uso

### De onde vêm estas regras
- `Produtividade com ia/CLAUDE.md` (regras do projeto) e a skill `organizacao-de-arquivos`.
- O projeto não é repositório git nem projeto único: são ferramentas Python independentes (Windows, Python 3.12, `ffmpeg`/`ffprobe` no PATH).

### Estrutura de pastas prevista (raiz `Produtividade com ia/`)
```
contexto/                  perfil, regras, prioridades, modelo de relatório, preferências visuais, tom
00-inbox/                  arquivos novos não triados
01-arquivos-organizados/   arquivos já processados
02-relatorios/             relatórios de performance (por frente/oferta/país)
03-dashboards/             dashboards de métricas
04-apresentacoes/          apresentações internas
05-pdfs-didaticos/         materiais de apoio, guias, documentação de processo
06-infograficos/           resumos visuais, comparações, fluxos
07-notion-sync/            exports do Notion (catálogo de preços, hubs de oferta)
sops/                      procedimentos operacionais padrão
templates/                 modelos reutilizáveis
```
Estado no disco (segundo o CLAUDE.md do projeto): existem `Contexto/` (com `banco-de-copy.md` e `estrategias-criativos.md`), `01-arquivos-organizados/`, `02-relatorios/`, `03-dashboards/`, `05-pdfs-didaticos/`, `06-infograficos/`, `ferramentas/`, `skills/`, `kit-edicao-criativos/`, `painel/` e atalhos (junctions) `entregas-*` para pastas de lote em `Downloads/`. Ainda não existem `00-inbox/`, `04-apresentacoes/`, `07-notion-sync/`, `sops/`, `templates/`: são criadas quando a primeira saída do tipo for gerada.

### Pasta legada de inbox
- `001- INBOX/` tem mídia, arquivos pessoais e administrativos não triados. É tratada como o `00-inbox/` até a triagem acabar.
- Em 21/09/2026 a pessoa aprovou o escopo "só os arquivos soltos na raiz" para organização dessa pasta.
- Fora do escopo deste repositório de contexto: o conteúdo dela não é lido nem resumido aqui.

### Dados sensíveis
- Informações pessoais, agenda, viagens, documentos privados e finanças pessoais servem só como contexto de organização. Nunca aparecem em criativos, páginas de venda ou relatórios para terceiros sem pedido explícito.
- Chaves de API: `kit-edicao-criativos/.env` (ElevenLabs), `.env` do gerador de criativos. **Nunca ler nem imprimir.** Os scripts carregam sozinhos.

## Lógica de uso

### Segurança de arquivos
1. **Nunca apague** sem autorização explícita. Nunca sobrescreva ou modifique um original.
2. Na dúvida, **copie** para a pasta nova em vez de mover. A skill `organizacao-de-arquivos` sempre copia, nunca move nem apaga.
3. Em lote de criativos: copie os originais para `<LOTE>/originais/NN.mp4` + `indice-arquivos.csv`; nunca mexa nos originais em `Downloads/`.
4. Confirme antes de alteração destrutiva em massa (especialmente na `001- INBOX/`). Fora isso, siga sem pedir confirmação (ver [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)).
5. Arquivos pessoais, recibos, comprovantes, documentos privados e administrativos ficam **separados** de materiais de campanha, criativos e comerciais.
6. Nunca exponha dados pessoais, financeiros, de fornecedores ou custos internos em criativo, página de venda ou material externo.
7. Nunca invente dados (produto, fornecedor, custo, oferta, mercado, métrica, data, cliente, resultado). Quando faltar, escreva **"precisa de revisão manual"**.

### Organizar uma pasta / inbox
1. Rode a skill `organizacao-de-arquivos` (`scripts/organize_files.py` é o padrão; o `.ps1` só para Windows sem Python; o índice do `.ps1` sai com BOM, então leia com `utf-8-sig`).
2. Classifique por categoria, frente (COD/Infoproduto/X1), assunto e data.
3. Gere **sempre** um índice com: nome original, novo nome, categoria, frente, nova localização, observações.
4. Gere um relatório final explicando o que foi feito e o que ficou para revisão manual.

### Nomes de arquivos
- Padrão: `AAAA-MM_frente_tipo_assunto.extensao`. Sem data clara: `frente_tipo_assunto.extensao`.
- Minúsculas, sem espaços, separadas por hífen ou underline. `frente` = `cod`, `infoproduto` ou `x1` quando fizer sentido.
- Exemplos: `2026-06_cod_relatorio_performance-chile.pdf`, `2026-06_infoproduto_apresentacao_planejamento-onda-tesla.pptx`, `2026-06_x1_dashboard_efetividade-pagamento.xlsx`, `pessoal_comprovante_aluguel.pdf`, `sop_infografico_fluxo-producao-criativo.png`.
- Criativos: o **nome do arquivo = nome do anúncio** no gerenciador, carregando conceito/persona/ângulo/formato (ex.: `C03_presente_ocasiao_unboxing_v1`, `DW7781_G<n>_C1`). Sem isso não dá para ligar métrica a texto depois.

### Ao criar qualquer material
Considere: objetivo, público-alvo, frente, país/mercado, formato de saída, profundidade, tom e uso final. Verifique se falta material complementar (roteiro, PDF de apoio, checklist, dashboard, relatório final) e sugira ou registre como pendência.

### Roteamento visual (qual formato usar)
| Situação | Formato |
|---|---|
| Reunião, treinamento de equipe/closers, planejamento, explicação ao vivo | Apresentação |
| Material de apoio, SOP, guia, documentação, entrega final, consulta posterior | PDF |
| Dados de campanha, métricas, prazos, progresso, indicadores | Dashboard |
| Comparação, passo a passo, resumo visual, regra ou processo curto | Infográfico |
| Execução prática, conferência, revisão de criativo, rotina de publicação | Checklist |
| Memorização, revisão rápida de conceitos/roteiros/objeções | Flashcards |
| Dados tabulares, controle de fornecedor/preço, tarefas, base estruturada | Planilha |

### Apresentações
Estrutura padrão (adaptável): Capa → Contexto → Objetivo → Problema/tema → Explicação central → Exemplos/aplicações → Passo a passo/método → Atividade/ação prática → Erros comuns/cuidados → Resumo → Próximos passos → Encerramento.

### Roteiros e materiais de apoio
- Roteiro de criativo: hook, sequência clara, falas de apoio, prova/exemplo, CTA e, quando couber, transições e fechamento.
- SOPs, briefings, checklists: prefira formatos visuais e fáceis de consultar (PDF, checklist, guia, infográfico).

### Relatórios e dashboards
- Relatório de performance: tom profissional, objetivo, didático. Inclui contexto (frente/oferta/país/período), o que foi analisado, principais achados, pontos de atenção, recomendações e próximos passos práticos.
- Dashboard: **só dados disponíveis** (Meta/Kwai/TikTok/Notion/planilhas/Chegou Operações). Nunca inventar CPA, ROAS, ticket ou margem. Se faltar dado, explique a limitação.
- Indicadores por frente: CPA e margem por produto/país (COD); CAC, ticket e conversão de funil (Infoproduto); efetividade de pagamento e fechamento por closer (X1).
- Saída em `02-relatorios/` ou `03-dashboards/`, no padrão de nomes.

### Priorização de tarefas
Colunas típicas em Notion/planilhas: A fazer, Fazendo, Em revisão, Aguardando, Feito, Prioridade alta, Próximos prazos, Ideias, Materiais pendentes.

Ordem:
1. Prazo mais próximo.
2. Prioridade alta.
3. Em andamento.
4. O que desbloqueia outras tarefas (ex.: criativo pendente travando lançamento).
5. Materiais para compromissos já agendados.
6. Entregáveis reutilizáveis (templates, SOPs).
7. Organização de arquivos importantes (catálogo, fornecedores, Notion).
8. Melhorias visuais e refinamentos.

Se faltar dado para priorizar, registre a limitação e diga o que precisa de revisão manual.

### Skills e agentes genéricos
- Skills: só fluxo e processo. Nada de produto, fornecedor, oferta, mercado, agenda ou ferramenta específica dentro da skill. O dado vem de `contexto/` em tempo de execução.
- Agents: genéricos, função clara, sem sobreposição; buscam contexto em `contexto/`, `07-notion-sync/` etc.
- A pasta `.claude/skills/` local é a fonte de verdade; `python ferramentas/empacotar-skills.py` gera os .zip para o claude.ai.

### Checklist de qualidade antes de finalizar
- [ ] O objetivo foi atendido?
- [ ] A frente certa (COD/Infoproduto/X1) foi considerada?
- [ ] Os arquivos de `contexto/` relevantes foram lidos?
- [ ] Saída na pasta correta, com nome padronizado?
- [ ] Conteúdo correto, organizado, sem informação inventada?
- [ ] Gramática, ortografia e acentuação revisadas (inclusive espanhol/inglês do mercado)?
- [ ] Dados pessoais, financeiros e de fornecedores protegidos?
- [ ] Originais preservados?
- [ ] Índice, relatório ou resumo gerado quando necessário?
- [ ] Limitações explicadas e próximos passos claros?

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)
- [13-analise-meta-ads-e-vencedores.md](13-analise-meta-ads-e-vencedores.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)
- [projetos/](projetos/)
