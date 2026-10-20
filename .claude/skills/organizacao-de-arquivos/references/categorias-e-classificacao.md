# Categorias padrão e heurísticas de classificação

Referência de apoio para a skill `organizacao-de-arquivos`. Consulte este arquivo
ao classificar arquivos cujo tipo/categoria não seja óbvio pelo nome.

## Categorias genéricas sugeridas

Use estas como ponto de partida e adapte/crie subpastas conforme o que for
encontrado de fato na pasta de origem — não force um arquivo para uma categoria
que não combina só para seguir a lista.

| Categoria | Quando usar | Exemplos de sinal |
|---|---|---|
| `documentos` | Documentos genéricos sem categoria mais específica | `.doc`, `.docx`, `.odt`, `.txt` sem outro sinal |
| `pdfs` | PDFs que não se encaixam em recibo/relatório/contrato/estudo | `.pdf` genérico |
| `imagens` | Fotos, prints, imagens sem contexto de recibo/comprovante | `.png`, `.jpg`, `.jpeg`, `.heic`, `.webp` |
| `planilhas` | Dados tabulares, controle, orçamento | `.xlsx`, `.xls`, `.csv`, nomes com "controle", "planilha", "orçamento" |
| `apresentacoes` | Slides | `.pptx`, `.ppt`, `.key` |
| `recibos-e-comprovantes` | Comprovante de pagamento, recibo, nota fiscal | nomes/conteúdo com "recibo", "comprovante", "nota fiscal", "pagamento", prints de transferência |
| `financeiro` | Extratos, boletos, planilhas financeiras, declarações | "extrato", "boleto", "fatura", "imposto", "declaração" |
| `estudos` | Material de estudo pessoal, resumos, anotações de curso | "resumo", "anotação", "estudo", "curso" |
| `materiais-de-aula` | Conteúdo de quem dá ou recebe aula (slides de aula, listas de exercício, apostilas) | "aula", "exercício", "apostila", "turma" |
| `trabalho` | Documentos profissionais que não são relatório/apresentação/planilha específicos | "reunião", "proposta", "briefing", nomes de projetos de trabalho |
| `clientes` | Material relacionado a um cliente específico (contratos, entregas, comunicação) | nome de cliente/empresa no arquivo, "contrato", "proposta comercial" |
| `projetos` | Arquivos de um projeto específico, não necessariamente ligado a um cliente | nome de projeto no arquivo |
| `viagens` | Passagens, reservas, roteiros, comprovantes de hospedagem | "passagem", "reserva", "hospedagem", "voucher", "roteiro" |
| `pessoal` | Documentos pessoais sem outra categoria mais específica (RG, certidões, receitas médicas) | "RG", "CPF", "certidão", "receita médica", "exame" |
| `relatorios` | Relatórios de performance, resultado, status | "relatório", "resultado", "performance", "status report" |
| `arquivos-para-revisao` | Conteúdo genuinamente ambíguo, corrompido, sem extensão reconhecível, ou nome sem nenhum sinal útil | qualquer coisa que não dá para classificar com segurança |
| `outros` | Não se encaixa em nada acima e não é ambíguo o bastante para revisão | ex.: instaladores, arquivos de sistema, zips genéricos |

Subcategorias são opcionais e só devem ser criadas quando ajudam de verdade
(ex.: `recibos-e-comprovantes/2026`, `clientes/nome-do-cliente`,
`estudos/nome-da-materia`). Não crie subpastas de um único arquivo sem necessidade.

## Como decidir tipo, assunto e data

1. **Nome do arquivo primeiro.** Datas em formatos comuns (`2026-05-03`,
   `03-05-2026`, `20260503`, `mai-2026`) e palavras-chave (recibo, contrato,
   aula, resumo, relatório, comprovante) geralmente já indicam tipo e parte do
   assunto.
2. **Metadados do arquivo** (data de criação/modificação) só devem ser usados
   como *data_identificada* quando o nome/conteúdo não trazem uma data mais
   confiável — deixe claro que é uma data de arquivo, não necessariamente a
   data do evento/documento, e prefira `sem-data` a arriscar uma data errada
   quando a metadata claramente não bate com o conteúdo (ex.: arquivo
   modificado recentemente mas texto menciona ano diferente).
3. **Conteúdo do arquivo**, quando puder ser lido com segurança e sem custo alto
   (arquivos de texto, PDFs pequenos, planilhas) — use para confirmar tipo e
   assunto, nunca para inventar um dado que não está lá.
4. **Nunca invente.** Se não houver assunto reconhecível, use uma descrição
   aproximada e honesta baseada no nome (ex.: `documento-sem-titulo`), nunca um
   nome de pessoa, empresa, valor ou data que não apareça no arquivo.

## Quando marcar "precisa de revisão manual"

Marque `status_revisao = precisa de revisao manual` sempre que:

- O tipo de arquivo não pode ser aberto/lido para confirmar o conteúdo (binário
  desconhecido, arquivo corrompido, formato não suportado pelas ferramentas
  disponíveis).
- O nome do arquivo não dá nenhum sinal de conteúdo, tipo ou data (ex.:
  `IMG_4821.jpg`, `Novo Documento.pdf`, `sem_titulo.txt`).
- Há sinal de conteúdo sensível (pessoal, financeiro, jurídico, médico) e a
  classificação exata do assunto exigiria abrir/reproduzir esse conteúdo com
  mais detalhe do que é seguro registrar no índice/relatório — nesse caso,
  classifique pela categoria (ex.: `pessoal`, `financeiro`) e marque para
  revisão em vez de tentar adivinhar o assunto exato.
- Existe conflito real entre sinais (nome sugere uma coisa, conteúdo sugere
  outra) e não é possível resolver com confiança.

## Cuidado com conteúdo sensível

Arquivos que pareçam pessoais, financeiros, jurídicos, médicos ou confidenciais
devem ser organizados normalmente (copiados para a categoria certa), mas:

- Nunca reproduza valores, números de documento, dados de saúde, dados
  bancários ou trechos do conteúdo no índice ou no relatório final — só a
  categoria e observações genéricas ("comprovante de pagamento", "documento
  pessoal") bastam.
- Nunca misture esses arquivos com materiais destinados a terceiros
  (criativos, páginas de vendas, relatórios para clientes) — eles devem ficar
  em categorias claramente pessoais/internas (`pessoal`, `financeiro`,
  `arquivos-para-revisao`).
