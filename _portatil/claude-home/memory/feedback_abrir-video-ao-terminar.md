---
name: feedback-abrir-video-ao-terminar
description: "Ao terminar qualquer prova/versão de vídeo (ou imagem), abrir o arquivo automaticamente no player e dar link clicável na resposta"
metadata:
  node_type: memory
  type: feedback
  originSessionId: fefd88e1-1970-4576-a429-cf0c1248f170
  modified: 2026-10-16T16:14:13.856Z
---

Sempre que terminar uma prova, prévia ou versão final de criativo, abrir o arquivo na hora (`Start-Process "<caminho>.mp4"` no PowerShell) e colocar na resposta um link clicável para ele, para o usuário não precisar procurar a pasta.

**Why:** usuário pediu (03/10/2026) para não ter que ficar pesquisando onde está o vídeo.
**Links:** o VS Code só abre links de arquivos DENTRO do workspace (`Produtividade com ia`). Entregas fora dele: usar o atalho (junção) `08-entregas/cod_lymphoria-cl/` → `Downloads\LHYMPORIA AD 01-20\lymphoria`; para outras pastas de fora, criar junção parecida antes de linkar. Link relativo com `../..` falha.
**How to apply:** em toda entrega de vídeo/imagem: (1) Start-Process no arquivo; (2) link markdown clicável no topo da resposta. Relacionado: [[feedback-narracao-minima-vscode]]

Atualização 16/10/2026: «Deixe sempre a pasta clicável». Em TODA entrega: abrir a pasta (Start-Process) E dar link clicável da PASTA, não só do arquivo. Para pastas fora do workspace, criar antes uma junção dentro de `Produtividade com ia/` (ex.: `08-entregas/infoproduto_camino-con-maria` → `Downloads\ADLIB-CAMINO-CON-MARIA`) e linkar pelo caminho da junção.

Atualização 07/10/2026: o player embutido do VS Code NÃO toca áudio AAC (a pessoa achou que os vídeos estavam mudos). Abrir sempre no Windows Media Player: `Start-Process "$env:ProgramFiles\Windows Media Player\wmplayer.exe" -ArgumentList "`"<arquivo>`""`. Avisar que o link do chat abre no VS Code sem som.
