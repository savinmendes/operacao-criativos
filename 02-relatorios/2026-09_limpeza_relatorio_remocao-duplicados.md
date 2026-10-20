# Relatório — remoção de arquivos duplicados

Executado em 24/09/2026 às 15:04.

## Resumo

| | |
|---|---|
| Arquivos removidos | 5659 |
| Espaço liberado | 247.28 GB |
| Disco livre antes | 2.02 GB |
| Disco livre depois | 249.33 GB |
| Grupos preservados por segurança | 0 |
| Erros | 0 |

## Critério

Arquivos agrupados por **hash completo** — byte a byte idênticos, não
apenas mesmo nome ou tamanho. De cada grupo, exatamente uma cópia foi
preservada. Nenhum grupo ficou sem cópia.

Ordem de preferência de qual cópia fica: `01-arquivos-organizados` →
`_organizado` → `001- INBOX` → solto em Downloads. Empate resolvido por
nome sem sufixo `(1)`, depois caminho menos profundo, depois arquivo mais antigo.

## Origem das cópias removidas

| Pasta | Arquivos | GB |
|---|---|---|
| Produtividade com ia\001- INBOX | 5318 | 238.12 |
| Produtividade com ia\01-arquivos-organizados | 328 | 8.86 |
| ad 35 (1).mp4 | 1 | 0.12 |
| ADS 12.1.mp4 | 1 | 0.03 |
| ADS 12.1 (1).mp4 | 1 | 0.03 |
| video - 1789724467906.mp4 | 1 | 0.03 |
| HOOKS PODADORA | 1 | 0.02 |
| PROSPERIDADE CONCORRENTE | 2 | 0.02 |
| video - 1789682892368.mp4 | 1 | 0.01 |
| video - 1789724463324.mp4 | 1 | 0.01 |
| ADS_12.1_FINAL (1).mp4 | 1 | 0.01 |
| ADS S3 UTI (1).mp4 | 1 | 0.00 |
| Pedidos_Dropi_Chile_limpo (1).csv | 1 | 0.00 |
| Pedidos_Dropi_Chile_limpo (1).xlsx | 1 | 0.00 |

## Por extensão

| Extensão | Arquivos | GB |
|---|---|---|
| .mp4 | 4407 | 205.83 |
| .zip | 210 | 36.64 |
| .png | 802 | 1.31 |
| .pdf | 72 | 1.22 |
| .mov | 33 | 1.06 |
| .wav | 20 | 0.64 |
| .mp3 | 80 | 0.28 |
| .jpg | 23 | 0.24 |
| .pptx | 1 | 0.02 |
| .jpeg | 6 | 0.02 |
| .webm | 1 | 0.01 |
| .csv | 2 | 0.00 |

## Causa da duplicação

A maior parte veio de `001- INBOX`. Quando aquela pasta foi organizada,
o processo **copiou** os arquivos em vez de mover — regra de segurança
para não perder nada. O efeito colateral é que cada arquivo passou a
existir duas vezes. Esta limpeza desfez essa duplicação.

## Limitações

- Só foram removidas cópias **idênticas**. Arquivos parecidos mas não
  idênticos (mesmo vídeo em resoluções diferentes, por exemplo)
  permanecem, e isso é intencional — não há como decidir qual versão
  manter sem critério do dono.
- A remoção foi definitiva, não para a lixeira: 247 GB na lixeira não
  liberariam espaço, que era o objetivo.
- O índice completo do que saiu está em
  `2026-09_limpeza_indice_duplicados-removidos.csv`, nesta mesma pasta.

## Próximos passos

- Com espaço livre, a organização dos arquivos soltos de Downloads
  pode rodar no modo seguro (copiando).
- Vale revisar se `001- INBOX` ainda precisa existir: o material dela
  já está em `01-arquivos-organizados`.