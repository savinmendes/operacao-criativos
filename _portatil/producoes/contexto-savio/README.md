# contexto-savio

Memória de contexto e lógica de trabalho da operação de tráfego pago e criativos (Grupo Chegou), escrita para ser lida por pessoas e por IAs (Claude) antes de qualquer tarefa.

## Como este repositório está organizado

Cada arquivo em `contexto/` trata de um tema e é dividido sempre em duas partes:

- **Contexto de uso:** o que é, quando se aplica, fatos, histórico, decisões já tomadas, números com data e onde estão os arquivos.
- **Lógica de uso:** como fazer, com passo a passo, regras, critérios, comandos, armadilhas e checklist.

O modelo está em [`contexto/_MODELO.md`](contexto/_MODELO.md).

## Índice

### Operação e regras
| Arquivo | Tema |
|---|---|
| [01-perfil-e-operacao](contexto/01-perfil-e-operacao.md) | As 3 frentes (COD, Infoprodutos, X1 After-Pay), mercados e métricas de cada uma |
| [02-regras-gerais-e-seguranca](contexto/02-regras-gerais-e-seguranca.md) | Segurança, dados sensíveis, pastas, nomes de arquivo e checklist de qualidade |
| [03-preferencias-de-trabalho](contexto/03-preferencias-de-trabalho.md) | Como a pessoa quer que a IA trabalhe, com o porquê de cada regra |
| [17-orquestracao-agentes-e-painel](contexto/17-orquestracao-agentes-e-painel.md) | Agentes em paralelo, briefings, painel ao vivo e entrega |
| [21-github-e-repositorio](contexto/21-github-e-repositorio.md) | Como atualizar este repositório (gh, pull → commit → push) e o que nunca subir |

### Produção de criativos
| Arquivo | Tema |
|---|---|
| [04-fluxo-producao-criativos](contexto/04-fluxo-producao-criativos.md) | Pipeline completo, receita JSON e montagem |
| [05-traducao-de-criativos](contexto/05-traducao-de-criativos.md) | Levar um criativo para outro idioma ou mercado |
| [06-troca-de-marca](contexto/06-troca-de-marca.md) | Trocar marca, rótulo ou oferta num AD existente |
| [07-variacoes-gancho-corpo](contexto/07-variacoes-gancho-corpo.md) | Matriz gancho × corpo, estáticos e carrossel |
| [08-voz-e-dublagem](contexto/08-voz-e-dublagem.md) | ElevenLabs, voz clonada, trilha e loudness |
| [09-lipsync-e-avatar-heygen](contexto/09-lipsync-e-avatar-heygen.md) | HeyGen: avatar, lipsync e critérios de aceite |
| [10-limpeza-cor-e-qualidade-de-video](contexto/10-limpeza-cor-e-qualidade-de-video.md) | Remover legenda, cor bt601, upscale e download em alta |
| [11-revisao-e-qualidade](contexto/11-revisao-e-qualidade.md) | Revisão automática e revisão independente |
| [19-destrinchar-e-adaptar-referencias](contexto/19-destrinchar-e-adaptar-referencias.md) | Destrinchar reel/anúncio de terceiro e adaptar para a nossa oferta sem copiar |
| [22-licoes-producao-video](contexto/22-licoes-producao-video.md) | O que deu errado na produção e foi refeito, e a regra que ficou |
| [16-ferramentas-e-servicos](contexto/16-ferramentas-e-servicos.md) | Inventário de ferramentas, custos e quando usar cada uma |

### Estratégia, dados e lojas
| Arquivo | Tema |
|---|---|
| [12-estrategia-criativa-e-copy](contexto/12-estrategia-criativa-e-copy.md) | Formatos vencedores, Andromeda e banco de copy |
| [13-analise-meta-ads-e-vencedores](contexto/13-analise-meta-ads-e-vencedores.md) | Contas, critério de vencedor e cruzamento gasto × venda |
| [14-unit-economics-cod](contexto/14-unit-economics-cod.md) | Margem e CPA por entrega no COD |
| [15-lojas-e-paginas](contexto/15-lojas-e-paginas.md) | Shopify, páginas, Dropi e Chegou Operações |
| [18-base-de-cases-e-referencias](contexto/18-base-de-cases-e-referencias.md) | Transcrições, fichas, resumos VTurb e Bid Cap; como consultar com `consultor-de-cases` |
| [20-internacionalizacao-e-gateways](contexto/20-internacionalizacao-e-gateways.md) | Idiomas × mercados, tickets por idioma e meios de pagamento locais |

### Projetos e lotes
[`contexto/projetos/00-indice-projetos.md`](contexto/projetos/00-indice-projetos.md) traz a tabela de todos os lotes já produzidos, com status e um arquivo por projeto.

## Regras deste repositório

- **Fica de fora:** vídeos, imagens, áudios, arquivos `.env`, chaves de API, documentos pessoais e dados de clientes.
- **Dados com data:** números e decisões levam a data absoluta. O que não foi confirmado aparece como "precisa de revisão manual".
- **Atualização:** ao terminar um lote novo, crie `contexto/projetos/<slug>.md` no mesmo modelo e acrescente uma linha no índice.
