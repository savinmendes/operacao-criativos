---
name: feedback-narracao-minima-vscode
description: "Preferência de estilo de resposta no VS Code (Focus view) — quase nenhum texto solto entre chamadas de ferramenta, só uma linha no início e um resumo final."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 68966334-b2d9-4891-bbd6-2776cdfc0763
  modified: 2026-09-20T12:38:14.410Z
---

**Regra:** ao trabalhar nesta extensão do VS Code (ambiente "Focus view", onde chamadas de ferramenta já aparecem como linhas resumidas/expansíveis), minimizar texto solto entre uma ação e outra — nada de narrar cada passo com frases tipo "vou ler o arquivo X", "agora vou ajustar Y". Só uma frase curta no início da tarefa e um resumo final (o que mudou / o que falta), deixando o "acompanhar tudo em detalhe" a cargo das próprias linhas expansíveis de ferramentas que a extensão já recolhe — o usuário pode clicar nelas se quiser ver passo a passo.

**Por quê:** o usuário pediu explicitamente pra imitar o visual/comportamento do Claude.ai, onde a execução de tarefas não "enche" o chat de texto — só um indicador compacto que dá pra expandir. Perguntei se ele queria isso (cortar quase todo texto) ou só compactar as atualizações, e ele escolheu cortar quase tudo.

**Como aplicar:** relacionado a [[feedback_execucao-paga-precisa-confirmacao]] (mesma linha de raciocínio: menos fricção/texto no meio do fluxo, só parar quando for algo que realmente importa — aqui, o início e o fim da tarefa).
