# Revisão da produção San Benito (13–14/10/2026)

**Frente:** infoproduto, oferta San Benito.
**O que cobre:** tudo o que foi produzido nestes dois dias, o que precisou ser refeito e onde cada lição ficou registrada.

## 1. O que foi entregue

| Lote | Entrega | Pasta |
|---|---|---|
| Vencedores ES → FR | OP2 ASCENSAO e JESU V07 em francês (v2 após revisão independente) | `Downloads/SB-VENCEDORES_OP2-ASCENSAO_JESU-V07/FR/` |
| Referência destrinchada | Narração, análise e adaptação do reel "Sagrado Verso" | `Downloads/REELS-REFERENCIA/` |
| Série Medalla (1ª versão) | 11 vídeos com selo "VIDEO FICTICIO" (comerciante, motorista de app e 9 personas) | `Downloads/SB-MEDALLA-SERIE-ES/` |
| Raio-x do 01 Medalla | `completar-criativo` → versão completa (v2 com gancho amplo, frustração, trilha em 2 climas e selo pequeno) | `Downloads/SB-REEL-MEDALLA-ES/` |
| **Série Medalla COMPLETA** | 11 vídeos no formato aprovado, cada persona com voz própria e o mesmo padre | `Downloads/SB-MEDALLA-COMPLETA-ES/` |
| Textos do anúncio | Título e texto principal por vídeo (feitos para a 1ª versão; atualizar para as falas da COMPLETA) | `SB-MEDALLA-SERIE-ES/00_TEXTOS-DO-ANUNCIO.md` |

**Custo aproximado no período:**
- Flora/Kling: ~US$ 25
- ElevenLabs: ~US$ 2
- HeyGen: ~1.000 créditos do plano (o saldo foi de ~7.982 para 7.012)

## 2. O que deu errado, o que foi refeito e a regra que ficou

| # | O que aconteceu | Como apareceu | Regra nova | Onde ficou |
|---|---|---|---|---|
| 1 | Retoque "fechar a boca" do avatar (segurar ou fundir quadros) | A pessoa viu bugs nas primeiras falas do padre: quadro fantasma, rosto congelado, salto | Cortar o avatar nas fronteiras das palavras e cobrir as pausas com B-roll ou jump cut. Nunca segurar nem fundir quadros no rosto | `gerar-midia-ia`, `CLAUDE.md` |
| 2 | Sorriso com dentes em fala triste (HeyGen) | Todas as selfies da 1ª série | Retrato base já triste, de boca fechada. Expressividade baixa não resolve | `gerar-midia-ia`, `revisar-criativo` |
| 3 | Rosto mole depois do lipsync (V07 FR) | Revisor independente: nitidez em 43–75% do original | Colar só boca e queixo sobre o take original e medir a nitidez | `gerar-midia-ia`, `traduzir-criativo` |
| 4 | Porta do carro deformada (Kling) | Pessoa: "a porta ficou toda bugada" | Sem porta abrindo, sem gente entrando ou saindo de veículo, câmera travada perto das bordas | `gerar-midia-ia`, `CLAUDE.md` |
| 5 | Close com zoom 1,8x ficou mole | Taxista | Gerar o enquadramento final; zoom de montagem ≤ ~1,2x | `gerar-midia-ia` |
| 6 | Gancho com personagem minúsculo ou fechado demais | Pessoa: "não aparece as cadeiras e mesas vazias" | Personagem com ~25% da altura e a dor legível no 1º quadro; título sem cobrir o personagem | `gerar-midia-ia`, `editar-criativo` |
| 7 | Close de mesa em "seis meses sin clientes" | Pessoa sugeriu o dono frustrado olhando o salão | A fala da dor ganha o personagem olhando o próprio vazio | `editar-criativo` |
| 8 | Mesma trilha da reza à virada | Pessoa | Dois climas, tensão → esperança, com crossfade no corte | `editar-criativo`, `revisar-criativo` |
| 9 | Selo grande e moldura falsa "EN VIVO" com nome | Pessoa mandou tirar | Só o selo, pequeno, colado no topo à direita | `editar-criativo` |
| 10 | Loop aberto sem fechamento e 2 CTAs com botões diferentes | Raio-x (`completar-criativo`) | O mecanismo é entregue antes do CTA; um CTA só, sem fala depois | `completar-criativo`, `editar-criativo` |
| 11 | CTA francês literal ("Touche…") | Revisor independente | Forma nativa ("Appuie sur…"); nome próprio na grafia local | `traduzir-criativo` |
| 12 | B-roll destoante da persona e take repetido 2x | Revisão e pessoa | O B-roll casa com idade e cenário; nenhum take repete | `editar-criativo`, `revisar-criativo` |
| 13 | Gemini reprovou take limpo (2x) | QA do agente | Confirmar a olho antes de pagar refação | `gerar-midia-ia`, `revisar-criativo`, `CLAUDE.md` |
| 14 | Whisper inventou "gracias por ver el video" | Transcrição do OP2 | Falso alarme conhecido em trecho só de trilha | `revisar-criativo` |
| 15 | Avatares diferentes com a mesma voz | Pessoa: "ideal é uma voz diferente para cada avatar" | 1 voz por personagem, registrada em `_vozes.json` antes de gerar | `gerar-midia-ia`, `CLAUDE.md` |
| 16 | Divisão de trabalho no meio do caminho e arquivo sobrescrito no scratchpad | Voz gerada em dobro; teto do ElevenLabs estourado | Dividir antes, `PRONTO.txt` por pasta, subpasta por agente | `editar-criativo`, `CLAUDE.md` |
| 17 | Agente suavizou o texto do anúncio sem pedido | Relatório do agente | Compliance: listar e perguntar, nunca suavizar sozinho | `revisar-criativo` |
| 18 | Disco do PC a 98% (14 GB de intermediários num projeto) | PC lento | Apagar `mont*` depois da entrega aprovada, com ok | `editar-criativo`, `CLAUDE.md` |
| 19 | `revisar-criativo` mandava `--residual` (opção inexistente) | Agente técnico | Corrigido para `--idioma-residual` | `revisar-criativo` |
| 20 | Referência de terceiros: pedido de copiar falas e rostos | Pedido do reel | Aproveitar a estrutura; falas, rostos, nomes reais e provas não. Selo "vídeo fictício" em teste | `completar-criativo`, repositório (arquivo 19) |

## 3. Pendências que dependem da pessoa
- Subir a série COMPLETA: falta definir a campanha, o orçamento, o link do "Camino de Fe" e o botão ("Más información").
- Atualizar os textos do anúncio para as falas da COMPLETA.
- Registrar o resultado por persona em `Contexto/estrategias-criativos.md` quando houver dados.
