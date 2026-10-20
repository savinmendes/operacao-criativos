# Catálogo — arquivos soltos na pasta Downloads

Levantado em 25/09/2026. **Nenhum arquivo foi movido ou renomeado.**
Este documento é um inventário: serve para decidir o que fazer, não registra ação.

## Resumo

| | |
|---|---|
| Arquivos catalogados | 379 |
| Volume total | 8.00 GB |
| Vídeos | 249 (5.84 GB) |
| Sem projeto identificável pelo nome | 203 (54%) |

## Por tipo

| Tipo | Arquivos | GB |
|---|---|---|
| video | 249 | 5.84 |
| imagem | 79 | 0.08 |
| planilha | 19 | 0.00 |
| compactado | 14 | 2.08 |
| documento | 6 | 0.00 |
| audio | 6 | 0.00 |
| dados/codigo | 3 | 0.00 |
| outros | 3 | 0.00 |

## Projeto inferido pelo nome do arquivo

Inferido **apenas** quando o nome diz explicitamente. Não foi aberto nenhum
vídeo para adivinhar conteúdo — o que está como não identificado é não identificado.

| Projeto | Arquivos |
|---|---|
| (não identificado) | 203 |
| san-benito | 138 |
| criativo-generico | 30 |
| fe-prosperidade | 4 |
| calza | 2 |
| heygen | 1 |
| podadora | 1 |

## Os 245 vídeos

### Proporção

| Proporção | Qtd |
|---|---|
| 9:16 | 232 |
| 4:5 | 6 |
| 3:4 | 3 |
| 429:233 | 1 |
| 299:303 | 1 |
| 101:180 | 1 |
| 596:307 | 1 |

232 dos 245 estão em 9:16 — vertical, formato correto para Reels e Stories.

### Resolução

| Resolução | Qtd |
|---|---|
| 1080x1920 | 108 |
| 720x1280 | 108 |
| 360x640 | 11 |
| 576x1024 | 5 |
| 720x900 | 4 |
| 270x360 | 2 |
| 360x480 | 1 |
| 1716x932 | 1 |

**108 vídeos estão em 1080x1920**, prontos para subir.

**13 estão em 360x640 ou menor.** Essa é resolução de download da biblioteca
de anúncios do Meta, não de exportação de edição. Servem como referência de
concorrente, mas não têm qualidade para veicular.

## Pacotes compactados

| Arquivo | MB | Dias |
|---|---|---|
| San_Benito_—_formatos_nativos_(leva_2)_2026-09-23.zip | 670.83 | 1 |
| San_Benito_—_formatos_nativos_(leva_2)_2026-09-23 (2).zip | 436.60 | 1 |
| San_Benito_—_formatos_nativos_(leva_2)_2026-09-23 (1).zip | 280.21 | 1 |
| San_Benito_—_formatos_nativos_(leva_2)_2026-09-24 (2).zip | 164.79 | 0 |
| San_Benito_—_formatos_nativos_(leva_2)_2026-09-24 (1).zip | 162.01 | 1 |
| Hooks_Aparador_—_Duelo_(Seedance_2.5)_2026-09-22.zip | 160.25 | 2 |
| San_Benito_—_formatos_nativos_(leva_2)_2026-09-24 (3).zip | 155.56 | 0 |
| San_Benito_—_formatos_nativos_(leva_2)_2026-09-24.zip | 63.05 | 1 |
| heygen_project.zip | 37.03 | 1 |
| SB_estaticos_nativos.zip | 2.36 | 1 |
| orders_export_1.zip | 0.57 | 2 |
| banco_calza2x1_json.zip | 0.03 | 2 |

Somam 2.08 GB. Vários são levas repetidas do mesmo material, com sufixo
`(1)`, `(2)`, `(3)` — vale conferir se já foram extraídos antes de guardar.

## O achado principal

**203 dos 379 arquivos (54%) não têm projeto identificável pelo nome.**
São hashes do CDN do Facebook, UUIDs e nomes como `video - 1790186235705.mp4`.

O gargalo aqui não é falta de pasta — é falta de nome. Nenhuma estrutura de
subpastas resolve um arquivo chamado `AQM-nP-A8hjy6K...mp4`, porque para
arquivá-lo é preciso abrir e assistir. Renomear na hora do download custa
segundos; recuperar o contexto depois custa abrir 203 vídeos.

## Limitações

- Projeto foi inferido **só pelo nome**. Nenhum vídeo foi aberto para classificar.
- Não foi verificado se os ZIPs já estão extraídos em outro lugar.
- Duração e resolução vêm do ffprobe; arquivos corrompidos apareceriam com campos vazios.
- O inventário é do momento da leitura. A pasta recebe arquivos novos todo dia.

## Próximos passos sugeridos

1. Separar os 13 vídeos de baixa resolução — são referência, não material de veiculação.
2. Conferir os ZIPs repetidos antes de arquivar.
3. Adotar nome na hora do download para o material novo. É a única correção que
   impede o problema de voltar.
4. O índice completo, com caminho, duração, resolução e proporção de cada arquivo,
   está em `2026-09_downloads_catalogo_arquivos-soltos.csv`, nesta mesma pasta.