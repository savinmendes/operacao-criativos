# Banco de copy — o que funciona e o que não funciona

Alimentado pela skill `analista-de-copy`. Só fatos observados, com data, anúncios de origem e confiança (alta/média/baixa).
Lido por `estrategista-criativo` antes de escrever roteiros. Separado por frente e mercado.

## COD · Chile · perfumes árabes

### Padrões validados
- (vazio: aguardando os dados do teste YARA-BF de out/2026)

### Padrões reprovados / a evitar
- 09/10/2026: palavras parecidas com o português na fala da IA de vídeo saem em PT ("stock" → "estoque"). Use "liquidación total". Confiança alta (observado na transcrição).
- 09/10/2026: nomes que a IA de voz pronuncia mal: "Moi" (→ "muy"), "Orquídea" (→ "Orquía"), "frutilla" (→ "frutita"), "grosella" (→ "grosilla"). Prefira frases em que o nome também apareça escrito na tela. Confiança alta.

### Hipóteses em teste
- 09/10/2026 · teste YARA-BF (7 criativos, mesma música BbY WOW). Ganchos:
  - H1: oferta + tema ("¡Liquidación total por Black Friday!")
  - H2: oferta direta ("Pagas dos y te llevas los tres")
  - H3: sensorial + pergunta na tela ("¿Ya probaste los perfumes árabes?")
  - H4: unboxing real + voz
  - H5: lista visual dos 3 nomes

  Formatos: AD-A (consultora em todas as cenas) × AD-C (consultora + unboxing real).
- 09/10/2026 · hipóteses do pré-teste (análise de copy, sem dados; relatório `02-relatorios/2026-10_cod_relatorio_copy-pre-teste-yara-bf.md`):
  - O H4 (unboxing real + "PAGA 2 · LLEVA 3" no quadro 1) vence em CPA, porque o produto real aumenta a confiança no COD. O H2 (oferta falada no quadro 1) deve vir em segundo. O H3 (pergunta sem oferta na tela) deve ter hook rate bom e CTR pior. Não validado.
  - O AD-C (consultora + unboxing narrado com TTS) supera o AD-A (só consultora, com mais palavras mal pronunciadas) em retenção e CPA. CJ01 e CJ07 são quase iguais: a diferença entre eles mede o ruído do teste. Não validado.
  - O lote não testa ângulo de presente nem chamado ao público. Hipótese para o próximo lote: o gancho "¿Buscando regalo?…" e o CTA "Pídelo hoy y pagas recién cuando te llegue a la casa" (sem escassez) mantêm ou melhoram o CPA. Não validado.

### Frases vencedoras (literal)
- (vazio)

## COD · Chile · ferramentas (DeWalt DCD7781)

### Hipóteses em teste
- 10/10/2026 · lote DW7781 Pre Black Friday (sem preço, pago contra entrega), análise pré-teste sem dados (`02-relatorios/2026-10_cod_relatorio_copy-pre-teste-dewalt-dcd7781.md`):
  - G5 ("Dos baterías, cargador y maleta: todo incluido") vence em CPA; G2 ("¿Sigues peleando con un taladro débil?" + broca no muro) vence em hook rate; G1 ("bueno, bonito y barato") e G4 ("¡Llegó el Pre Black Friday, maestro!") ficam atrás em CPA. Não validado.
  - Corpo C2 (demonstração + "mientras una trabaja, la otra se carga") retém mais que C1 (inventário de 13 frases). Não validado.
  - Teste planejado: 5 ganchos no mesmo corpo (C1), nomes `DW7781_G<n>_C1`.

### Padrões reprovados / a evitar
- 10/10/2026: whisper ouviu "DeWalt" como "de Waltz"/"de Walt" e "Pre Black Friday" como "Free Black Friday" na voz IA. Marca e "Pre" devem aparecer escritos na tela; ouvir antes de subir. Confiança média (só transcrição).
