# 22 — Lições de produção de vídeo com IA (o que foi refeito e a regra que ficou)

> Erros que custaram versões refeitas nas séries San Benito de 13–14/10/2026 e a regra que passou a valer. Leia antes de produzir qualquer lote com avatar, takes de IA ou tradução.

## Contexto de uso

Lotes em que estas lições apareceram:
- **SB FR:** OP2 ASCENSAO e JESU V07, de espanhol para francês.
- **Série SB Medalla:** comerciante, motorista de app e mais 9 personas, em duas versões. A segunda é a "COMPLETA", gerada depois do raio-x com `completar-criativo`.

Cada item abaixo foi apontado pela pessoa ao assistir, pelo revisor independente ou pelo raio-x, e resolvido numa versão nova.

Onde as regras estão hoje, na máquina da operação:
- Skills `gerar-midia-ia`, `editar-criativo`, `revisar-criativo`, `traduzir-criativo` e `completar-criativo`.
- Seção "Armadilhas" do `CLAUDE.md` do projeto.
- Relatório completo: `02-relatorios/2026-10_infoproduto_revisao-producao-san-benito.md`.

| # | O que aconteceu | Regra que ficou |
|---|---|---|
| 1 | Retoque para fechar a boca do avatar (segurar ou fundir quadros) gerou quadro fantasma, rosto congelado e salto | Cortar o avatar nas fronteiras das palavras. Pausas viram B-roll ou jump cut (zoom 1,0/1,13). Nunca segurar nem fundir quadros no rosto |
| 2 | Avatar gerado de foto sorrindo mostrava os dentes em fala triste | Retrato base já triste, boca fechada, cantos para baixo. Expressividade baixa não resolve |
| 3 | Lipsync sobre vídeo existente deixou o rosto mole | Colar só boca e queixo sobre o take original, com a cor ajustada, e medir a nitidez |
| 4 | Kling deformou a porta do carro | Nada de porta abrindo, gente entrando ou saindo de veículo, nem objeto passando de mão em mão. Câmera travada perto das bordas |
| 5 | Close com zoom de 1,8x ficou mole | Gerar o enquadramento final. Zoom de montagem até ~1,2x |
| 6 | Gancho com personagem minúsculo, ou fechado demais sem o contexto | Personagem ocupando ~25% da altura e a dor legível no 1º quadro. O título não cobre o personagem |
| 7 | Close de objeto na fala da dor | Mostrar o personagem frustrado olhando o próprio lugar vazio |
| 8 | Mesma trilha do problema até a virada | Dois climas, tensão → esperança, com crossfade no corte |
| 9 | Selo "vídeo fictício" grande e moldura falsa de "ao vivo" com nome do personagem | Só o selo, pequeno, colado no topo à direita |
| 10 | Vídeo abria um loop e não fechava, e tinha 2 CTAs com botões diferentes | Entregar o mecanismo antes do CTA. Um CTA só, sem fala depois |
| 11 | CTA traduzido ao pé da letra (francês) | Usar a forma nativa ("Appuie sur…") e nome próprio na grafia local |
| 12 | B-roll destoando da persona e take repetido 2x | O B-roll casa com idade e cenário da persona. Nenhum take repete |
| 13 | QA por IA reprovou um take limpo | Confirmar a olho, quadro a quadro, antes de pagar refação |
| 14 | Whisper inventou uma despedida em trecho só de trilha | Falso alarme conhecido. Conferir antes de tratar como defeito |
| 15 | Personagens diferentes com a mesma voz | Uma voz por personagem, registrada antes de gerar |
| 16 | Divisão de trabalho entre agentes no meio do caminho e arquivo sobrescrito | Dividir antes. `PRONTO.txt` por pasta e subpasta própria por agente |
| 17 | Agente suavizou o texto do anúncio sem pedir | Em compliance, listar o risco e perguntar. Nunca suavizar sozinho |
| 18 | Pastas intermediárias de montagem encheram o disco (14 GB) | Apagar `mont*` depois da entrega aprovada, com o ok da pessoa |
| 19 | Pedido de copiar falas e rostos de um reel de terceiro | Aproveitar só a estrutura. Personagens novos, roteiro próprio e selo "vídeo fictício" em teste |

## Lógica de uso

1. **Antes de orçar um lote**, passe pela tabela e ajuste o plano:
   - takes sem movimento arriscado (item 4);
   - retrato base triste quando a fala é de dor (2);
   - gancho amplo (6);
   - uma voz por personagem (15);
   - divisão de agentes definida (16).
2. **No briefing de cada agente**, copie as regras que se aplicam ao trabalho dele. Isso vale principalmente para 1, 4, 5, 13 e 16.
3. **Na montagem**, confira os itens 6 a 10 e o 12 antes de renderizar.
4. **Na revisão**, use o checklist "olho humano" da skill `revisar-criativo`. Os itens 13 e 14 são falsos alarmes: confirme antes de refazer.
5. **Quando surgir um erro novo que obrigue a refazer**, acrescente uma linha nesta tabela e na skill correspondente, com a data.

## Relacionados
- [09-lipsync-e-avatar-heygen.md](09-lipsync-e-avatar-heygen.md)
- [10-limpeza-cor-e-qualidade-de-video.md](10-limpeza-cor-e-qualidade-de-video.md)
- [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)
- [19-destrinchar-e-adaptar-referencias.md](19-destrinchar-e-adaptar-referencias.md)
- [projetos/sb-reel-medalla-es.md](projetos/sb-reel-medalla-es.md)
