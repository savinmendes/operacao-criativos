---
name: organizacao-de-arquivos
description: Organiza qualquer pasta bagunçada em uma estrutura clara por categoria, renomeando arquivos com um padrão consistente e gerando um índice completo + relatório final em PDF. Use sempre que o usuário pedir para organizar, arrumar, separar, categorizar ou limpar uma pasta cheia de arquivos variados (documentos, PDFs, imagens, planilhas, recibos, comprovantes, anotações, contratos, relatórios, apresentações, materiais de estudo/aula, arquivos de viagem, arquivos financeiros ou pessoais) — mesmo que o usuário não use a palavra "skill" ou não descreva o fluxo completo, ex.: "organiza essa pasta de downloads pra mim", "separa esses arquivos por tipo", "arruma essa bagunça de PDFs e prints", "preciso categorizar esses documentos". Funciona em qualquer projeto, pasta ou tipo de usuário (profissional, estudante, empresa) — é genérica e não depende de nenhum contexto específico de negócio.
---

# Organização de Arquivos

Esta skill organiza uma pasta bagunçada de forma segura, reutilizável e
rastreável: analisa cada arquivo, classifica por categoria/tipo/assunto/data,
copia (nunca apaga nem move) para uma estrutura clara de subpastas, renomeia
com um padrão consistente e gera um índice completo + relatório final em PDF.

Funciona para qualquer pessoa, projeto ou tipo de arquivo — não assuma nada
sobre quem é o usuário ou que tipo de arquivos vai encontrar além do que os
arquivos de fato mostram.

## Quando usar

Use esta skill sempre que o usuário pedir para organizar, separar, categorizar,
arrumar ou limpar uma pasta com arquivos variados — mesmo em pedidos informais
("organiza essa pasta pra mim", "separa isso por tipo"). Não é necessária para
mover ou renomear um único arquivo específico — nesse caso um comando direto
já resolve.

## Onde esta skill está rodando — determine antes de começar

O que ela consegue alcançar muda conforme a superfície. Isso não é detalhe: o
usuário pode achar que a pasta dele foi arrumada quando na verdade só cópias na
nuvem foram organizadas.

| Ambiente | O que a skill alcança |
|---|---|
| **Assistente de terminal/CLI, com acesso ao disco** | A pasta real. Lê, copia e escreve direto no sistema de arquivos |
| **App de desktop com uma pasta conectada** | A pasta real, dentro do escopo conectado. É o caminho para organizar de verdade os arquivos do computador |
| **Web, com arquivos anexados na conversa** | **Apenas as cópias anexadas.** A organização acontece no ambiente de execução e volta como arquivos para download — a pasta de origem no computador do usuário permanece intocada |

**Se estiver no ambiente web com anexos, diga isso ao usuário antes de
começar**, em uma frase, e ofereça o caminho do app de desktop com a pasta
conectada caso ele espere que a pasta real seja reorganizada. Descobrir isso
depois de organizar 300 arquivos é frustração garantida.

## Qual script usar

Os dois scripts em `scripts/` fazem a mesma coisa e produzem o mesmo índice.

- **`organize_files.py` é o padrão.** Python existe em praticamente todo
  ambiente de execução, inclusive nos ambientes em nuvem. Use-o sempre que
  houver escolha.
- **`organize_files.ps1` é uma alternativa restrita ao Windows local**, para o
  caso de uma máquina Windows sem Python instalado. Não funciona em ambiente
  na nuvem, macOS ou Linux.

Uma diferença já observada entre eles: a versão PowerShell grava o `index.json`
com BOM. Qualquer código que leia esse índice depois precisa usar `utf-8-sig`,
não `utf-8`, senão quebra na primeira linha.

## Passo 0 — Parâmetros

Antes de organizar, determine estes parâmetros. Infira o que puder do contexto
(mensagem do usuário, pasta indicada, arquivos de `contexto/`, `sops/` ou
`templates/` do projeto se existirem, estrutura de pastas já existente).
**Só faça uma pergunta objetiva se algo essencial não puder ser inferido** —
normalmente isso é só a pasta de origem quando o usuário não indicou nenhuma.
Não pare para confirmar parâmetros que já têm um padrão razoável definido
abaixo.

| Parâmetro | Como resolver |
|---|---|
| Pasta de origem | Pasta indicada pelo usuário. Se não houver nenhuma pista razoável, pergunte objetivamente qual pasta organizar. |
| Pasta de destino | Se o usuário indicar, use. Senão, infira: se o projeto já tem uma pasta do tipo `arquivos-organizados`/`organizado`, use-a; senão, crie `<nome-da-pasta-origem>-organizado` como pasta irmã da origem. |
| Padrão de renomeação | Padrão genérico desta skill (ver "Padrão de nomes" abaixo), a menos que `contexto/` do projeto defina outro padrão explícito — nesse caso, siga o do projeto. |
| Modo de organização | Sempre **copiar**. Nunca mover, nunca apagar o original. Isso não é uma escolha do usuário nesta skill — é uma regra de segurança fixa. |
| Categorias | Lista padrão em `references/categorias-e-classificacao.md`, adaptada ao que for realmente encontrado. Use as categorias que o usuário pedir explicitamente, se pedir. |
| Formato do índice | PDF (índice completo + relatório final consolidados em um único PDF), a menos que o usuário peça outro formato explicitamente. |

Se existir uma pasta `contexto/` (ou equivalente) no projeto, verifique antes
de começar se há algum arquivo com regras de organização, padrão de
nomenclatura ou modelo de índice já definidos para este projeto/usuário — se
houver, siga-o em vez do padrão genérico desta skill. Se não houver nada, use
os padrões genéricos definidos aqui.

## Fluxo de execução

1. **Listar a pasta de origem** recursivamente (nome, extensão, tamanho, datas
   de criação/modificação de cada arquivo). Note também subpastas existentes —
   elas ajudam a entender o contexto, mas cada arquivo é classificado
   individualmente.
2. **Analisar cada arquivo**: nome, extensão, metadados e, quando for seguro e
   barato (arquivos de texto, PDFs pequenos, planilhas), o conteúdo. Não abra
   arquivos muito grandes ou binários não suportados só para classificar — use
   o nome/extensão/metadados nesses casos.
3. **Classificar** cada arquivo em categoria, subcategoria (opcional), tipo,
   assunto aproximado e data identificada, seguindo as heurísticas de
   `references/categorias-e-classificacao.md`. Quando não houver segurança
   suficiente, classifique pelo nome do arquivo e marque
   `status_revisao = precisa de revisao manual` — nunca invente data, assunto,
   nome de cliente/aluno/projeto ou qualquer outro dado que não esteja
   evidente no arquivo.
4. **Definir o novo nome** de cada arquivo seguindo o padrão de nomes (abaixo).
5. **Montar o plano de organização**: uma lista JSON com um item por arquivo,
   no formato esperado por `scripts/organize_files.py` (veja o cabeçalho do
   script para o schema exato — inclui `caminho_original`, `categoria`,
   `subcategoria`, `novo_nome`, `tipo`, `assunto`, `data_identificada`,
   `observacoes`, `status_revisao`).
6. **Executar a cópia com segurança**: rode
   `python scripts/organize_files.py <plano.json> --destino "<pasta-destino>"`.
   Esse é o caminho padrão em qualquer ambiente. Só caia para o equivalente em
   PowerShell
   (`powershell -File scripts/organize_files.ps1 -Plano <plano.json> -Destino "<pasta-destino>"`)
   quando estiver numa máquina **Windows local sem Python** — ver "Qual script
   usar" acima.
   Qualquer um dos dois cria a estrutura de subpastas por categoria, copia
   cada arquivo preservando o original, resolve colisões de nome com sufixo
   numérico (nunca sobrescreve) e gera `index.json`/`index.csv` em
   `<destino>/_indice/` com as 10 colunas do índice.
7. **Gerar o PDF final** (índice completo + relatório final, ver estrutura
   abaixo) a partir do `index.csv`/`index.json` gerado, usando a skill de PDF
   disponível no ambiente. Salve o PDF na pasta de destino (ou na subpasta de
   relatórios do projeto, se o projeto já tiver uma convenção para isso). Se a
   geração de PDF falhar por falta de Python/dependências no ambiente, gere o
   índice e o relatório em Markdown (ou CSV para o índice) como alternativa,
   e avise claramente o usuário que o PDF não pôde ser gerado e por quê.
8. **Resumir para o usuário** no chat: quantidade de arquivos organizados, por
   categoria, quantos precisam de revisão manual, e onde o PDF final foi
   salvo.

## Padrão de nomes

Padrão principal: `AAAA-MM-DD_tipo_assunto.extensao`

- Quando a data não estiver clara: `sem-data_tipo_assunto.extensao`
- Quando o assunto não estiver claro: use uma descrição aproximada baseada no
  nome do arquivo ou no conteúdo identificado, sem inventar informação.
- Sempre minúsculo, sem espaços, palavras separadas por hífen.

Exemplos:
- `2026-06-12_recibo_compra-material.pdf`
- `2026-05-03_aula_verbos-irregulares.docx`
- `sem-data_comprovante_hospedagem.pdf`
- `sem-data_planilha_controle-financeiro.xlsx`
- `2026-06-01_estudo_resumo-produtividade.pdf`

## Categorias

Ver lista completa e heurísticas de classificação em
[`references/categorias-e-classificacao.md`](references/categorias-e-classificacao.md).
Categorias genéricas de partida: `documentos`, `pdfs`, `imagens`, `planilhas`,
`apresentacoes`, `recibos-e-comprovantes`, `financeiro`, `estudos`,
`materiais-de-aula`, `trabalho`, `clientes`, `projetos`, `viagens`, `pessoal`,
`relatorios`, `arquivos-para-revisao`, `outros`. Adapte/crie categorias
conforme o conteúdo real da pasta — a lista é um ponto de partida, não uma
camisa de força.

## Regras de segurança

- **Nunca apague, mova ou sobrescreva** um arquivo original. A ação é sempre
  copiar (`scripts/organize_files.py` já garante isso).
- **Colisão de nome no destino** → resolvida automaticamente com sufixo
  numérico (`_2`, `_3`, ...); nunca sobrescreve, e o conflito fica registrado
  no índice.
- **Nunca invente** data, assunto, nome de cliente/aluno/projeto, valor ou
  qualquer outro dado que não esteja evidente no arquivo. Na dúvida, use
  `sem-data`, uma descrição aproximada honesta, e marque para revisão manual.
- **Conteúdo sensível** (pessoal, financeiro, jurídico, médico, confidencial):
  organize com cuidado normalmente, mas nunca reproduza valores, números de
  documento, dados de saúde ou trechos do conteúdo no índice ou no relatório —
  só a categoria e uma observação genérica. Nunca misture esses arquivos com
  materiais destinados a terceiros.
- **Ações destrutivas em massa** (mover/apagar) nunca são feitas por esta
  skill. Se o usuário pedir explicitamente para apagar os originais depois de
  conferir a organização, isso é uma ação separada que exige confirmação
  explícita dele antes de qualquer exclusão — esta skill nunca apaga por
  conta própria.

## Formato de saída

### Estrutura de pastas

```
<pasta-destino>/
├── <categoria-1>/
│   └── (subcategoria opcional)/
│       └── arquivos renomeados
├── <categoria-2>/
│   └── ...
└── _indice/
    ├── index.json
    ├── index.csv
    └── <nome>.pdf   (índice completo + relatório final)
```

### Índice (mínimo 10 colunas)

`nome_original, novo_nome, extensao, categoria, subcategoria,
data_identificada, nova_localizacao, acao_realizada, observacoes,
status_revisao`

Gerado automaticamente por `scripts/organize_files.py` em `index.json` e
`index.csv` — use esses arquivos como fonte de dados ao montar a tabela do
índice no PDF final, não redigite os valores.

### Relatório final (segunda seção do mesmo PDF)

Estrutura fixa:

1. Resumo da organização
2. Pasta de origem analisada
3. Pasta de destino usada
4. Quantidade total de arquivos encontrados
5. Quantidade de arquivos organizados
6. Quantidade de arquivos que precisam de revisão manual
7. Categorias criadas
8. Arquivos com informações incompletas
9. Arquivos duplicados ou com possível conflito
10. Limitações da análise
11. Próximos passos recomendados

Use apenas dados reais apurados na execução — se algo não pôde ser
determinado, declare a limitação em vez de preencher com suposição.

## Checklist de qualidade antes de finalizar

- [ ] O usuário sabe **onde** os arquivos organizados foram parar (pasta real do
      computador x cópias no ambiente de execução)?
- [ ] A pasta de origem e a pasta de destino usadas estão corretas e confirmadas?
- [ ] Todos os arquivos originais continuam intactos (só cópias foram criadas)?
- [ ] Cada arquivo copiado tem categoria, novo nome e localização registrados no índice?
- [ ] Nomes seguem o padrão definido (`AAAA-MM-DD_tipo_assunto.ext` ou `sem-data_tipo_assunto.ext`)?
- [ ] Nenhuma data, assunto, nome ou valor foi inventado?
- [ ] Arquivos incertos foram marcados como "precisa de revisão manual"?
- [ ] Conteúdo sensível foi tratado com cuidado e não foi reproduzido no relatório?
- [ ] Colisões de nome foram resolvidas sem sobrescrever nada?
- [ ] O índice tem as 10 colunas mínimas e está completo?
- [ ] O relatório final foi gerado em PDF com a estrutura definida?
- [ ] As limitações da análise foram explicadas com clareza?
- [ ] Os próximos passos recomendados ficaram claros para o usuário?
