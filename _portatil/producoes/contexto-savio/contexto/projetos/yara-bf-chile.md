# Yara Kit 3 (Lattafa) COD Chile, Black Friday "paga 2 leva 3"

> Criativos do kit com 3 perfumes Yara para o Chile, do teste de gancho com IA até a onda 2 por diversidade Andromeda, mais o vídeo da loja. Abra ao subir, ler resultado ou produzir mais Yara.

## Contexto de uso
- **Frente:** COD Chile. **Produto:** Kit Yara + Yara Moi + Yara Elixir (Lattafa), chileverificada.com, CLP 59.900. **Início:** 09/10/2026.
- **Oferta definida pela pessoa:** liquidação de estoque Black Friday, "paga 2 e leva o 3º grátis", "muito abaixo do mercado", **não falar preço**. "Quedan pocas unidades" vai no texto do anúncio (aprovado em 09/10/2026).
- **Pasta:** `Downloads\YARA-CL\` (`_ref`, `banco`, `preprod`, `teste`, `producao`, `loja`, `entregas`).
- **Entregas (09/10/2026, em `entregas\`):**
  - teste de gancho: cena da pessoa (arabeperfumes + placa BF) → GPT Image 2 → Seedance 11 s ES, US$ 2,86;
  - `TRECHO-A`: 2 cenas da consultora, 10 s;
  - `AD-C`: 48 s (consultora + B-roll real), voz única por clone + speech-to-speech do ElevenLabs (sem HeyGen); versões de música trend (BbY WOW, Bam Bam, SUPERESTRELLA) e IA (A, B, C), todas a −32 LUFS sob a fala;
  - `AD-A` (opção econômica): 50,9 s, 3 cenas novas com a loja movimentada (US$ 5,81), sem música / bbywow / bambam;
  - `volume\`: 15 versões (5 ganchos × 3 trilhas) sobre o corpo do AD-C, custo zero;
  - `TESTE-7-criativos\` (CJ01–07 + `ESTRUTURA_CAMPANHA.txt` + `texto_do_anuncio.txt`): a pessoa decidiu subir como está, sem reescrever o CTA.
  - Gasto no Flora em 09/10: ~US$ 22 no dia (o registro também cita ~US$ 14 numa etapa).
- **Onda 2 (10/10/2026, `entregas\ONDA2\`, `LEIA-ME_onda2.md`):** 7 criativos, 1 por conceito — C1 sensorial sem fala, C2 "uno para cada momento", C3 "1, 2… gratis", C4 elogio da amiga, C5 "lo estás aplicando mal", C6 Natal (**subir em novembro**), C7 "¿cuánto pagué?" (feito sem citar marca de grife; o risco "cheiro de luxo" é decisão da pessoa). Base: análise dos 50 virais orgânicos (`_ref\virais\_analise\matriz_andromeda_yara.md`). Avatares a partir do print da pessoa (personagens inventados, segundo ela). Custo US$ 20,32 de teto 25. `sem-musica\` com as versões sem trilha.
- **Todos os criativos com texto:** `entregas\TODOS-CRIATIVOS\` (01–14 + `00_TEXTOS_TODOS.txt`).
- **Estrutura de campanha:** US$ 100/dia; fase 1 teste ABO com 7 conjuntos × US$ 14 (CJ01–07), 4 dias; fase 2 escala.
- **Loja:** vídeo de boas-vindas (avatar na fachada "arabeperfumes") no ar desde 09/10 no fim da coleção perfumes-arabes (seção `pa-colecao-video`); vídeo também nas páginas dos 15 produtos da coleção (seção `pa-produto-video` no footer-group, tema "... + video loja + produtos" `167235715328`, aguardando a pessoa publicar). Detalhes de loja em [perfumes-lattafa-chile.md](perfumes-lattafa-chile.md).
- **Análise de copy pré-teste:** `Produtividade com ia\02-relatorios\2026-10_cod_relatorio_copy-pre-teste-yara-bf.md`. O modo 2 da analista-de-copy fica para depois de ~3 dias rodando.
- **Pendência:** ler o resultado do teste (dados de campanha não registrados aqui — precisa de revisão manual).

## Lógica de uso
1. **Teste por bloco antes do lote:** gerar só o gancho (imagem → vídeo IA), medir custo e qualidade, depois montar o AD completo.
2. **Voz única:** clonar uma voz e passar as falas por speech-to-speech do ElevenLabs, para a consultora soar igual em todas as cenas.
3. **Legenda "modo roteiro"** (alinhamento CTC com o texto do roteiro): 100 % das palavras com erro ≤ 100 ms. É o padrão agora.
4. **Música:** trend liberada pela pessoa (assume o risco), instrumental via demucs + ducking, −32 LUFS sob a fala; sempre gerar versão sem música de reserva.
5. **Volume barato:** ganchos × trilhas sobre o mesmo corpo, tudo local.
6. **Onda de diversidade:** analisar virais orgânicos → matriz persona × ângulo × etapa do funil → 1 criativo por conceito com elenco, cenário e abertura diferentes (skill andromeda + estrategista-criativo; estratégia geral em `contexto/estrategias-criativos.md`).
7. **Tema da loja:** o conector Shopify bloqueia gravar no tema publicado e publicar → `themeDuplicate`, gravar na cópia e a pessoa clica em Publicar.
- **Lição de dimensionamento (retrospectiva Yara):** 25 vídeos para US$ 100/dia foi demais, cabiam ~7. Fechar orçamento de mídia antes de definir o volume.
- **Se a pessoa pedir mais:** rodar o modo 2 da analista-de-copy com ~3 dias de dados; escalar o conceito vencedor; subir o C6 em novembro.

## Relacionados
- [../07-variacoes-gancho-corpo.md](../07-variacoes-gancho-corpo.md)
- [../04-fluxo-producao-criativos.md](../04-fluxo-producao-criativos.md)
- [perfumes-lattafa-chile.md](perfumes-lattafa-chile.md), [dewalt-ads-cl.md](dewalt-ads-cl.md)
