---
name: feedback-execucao-paga-precisa-confirmacao
description: "Não pedir permissão nem confirmação — executar o serviço completo. Só parar se for realmente crítico (gastar dinheiro real ou destruir dado insubstituível)."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 68966334-b2d9-4891-bbd6-2776cdfc0763
  modified: 2026-09-22T00:27:12.319Z
---

**Regra:** executar a tarefa inteira sem parar para pedir aval. Nada de `AskUserQuestion` para escolher entre abordagens, nada de "quer que eu rode?", nada de apresentar plano e aguardar. Quando houver ambiguidade, escolher a leitura mais razoável, declarar a premissa em uma linha e seguir. Só interromper quando for **crítico de verdade**: gastar dinheiro real (API paga, mídia), ou destruir dado insubstituível sem possibilidade de reversão.

**Por quê:** o usuário reclamou explicitamente em 21/09/2026 — "Pare de me pedir permissao pra tudo, quero que me peça permissao apenas se for algo critico, faça o serviço completo". Antes disso eu tinha parado três vezes seguidas numa mesma sessão: para escolher escopo de organização de pasta, para confirmar execução de um script já aprovado, e para decidir qual de três interpretações de um pedido seguir. Cada pausa custou um turno e não agregou nada — em todos os casos havia uma opção obviamente melhor que eu poderia ter escolhido sozinho e justificado depois.

**Como aplicar:** mover/renomear arquivos em massa, rodar script já escrito, instalar dependência local, escolher estrutura de pastas, decidir entre duas modelagens — tudo isso é para fazer, não para perguntar. Preservar as salvaguardas que não custam turno: copiar em vez de mover quando houver dúvida real, nunca apagar, gerar índice e relatório, e declarar limitações no final. A regra do CLAUDE.md sobre confirmar movimentação em massa na `00-inbox/` já foi satisfeita uma vez: o usuário aprovou o escopo "só os arquivos soltos na raiz". Relacionado a [[feedback_narracao-minima-vscode]] — mesma linha: menos fricção no meio do fluxo.
