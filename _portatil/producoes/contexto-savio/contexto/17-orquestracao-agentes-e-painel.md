# Orquestração de agentes e painel ao vivo

> Como dividir uma produção em agentes paralelos, o que todo briefing de agente precisa ter, como registrar o andamento no painel local, quando confirmar custo e como entregar. Abra antes de disparar qualquer lote ou tarefa longa.

## Contexto de uso

### Por que agentes em paralelo
- A pessoa prefere **sempre o máximo de agentes em paralelo** (08/10/2026: estranhou um piloto com 1 agente só num método já validado). Em 13/10/2026, no San Benito FR, pediu "máximo de agentes": 1 agente por AD + revisor.
- Revisores independentes (whisper es/en + OCR + folha de contato) pegaram defeitos que a folha `_frames.jpg` não mostra: quadros soltos nos cortes, silêncio no fim, setas sobre o aviso.
- Lotes já entregues desse jeito: Drenagem LATAM (55 criativos), Wyze (16 ADs), Oración (18 ADs), Mopa, DeWalt, kits de perfume (8 agentes com um briefing único `Downloads\KITS-PERFUMES\BRIEFING.md`). Ver `projetos/`.

### O painel ao vivo
- Criado em 09/10/2026 porque a pessoa pediu "uma janela acoplada aqui no chat para ver as execuções em tempo real".
- Pasta `Produtividade com ia/painel/`: `index.html` lê `status.json` a cada 3 s; servidor `painel/iniciar.ps1`, porta **8765** (http://127.0.0.1:8765), aberto numa aba do VS Code ao lado do chat.
- `painel.py` grava em `status.json` (gravação atômica via `.tmp`). Cada tarefa guarda: título, estado (`rodando`/`pronto`/`erro`/`aguardando`), etapa, `k`/`n`, custo acumulado em US$, até 24 imagens (arquivos locais são copiados para `painel/img/`), links e as últimas 10 linhas de log.
- Feed automático: hook global `~/.claude/hooks/atividade.py` grava cada ação em `painel/atividade.jsonl` ("O que o Claude está fazendo agora").
- Hook de voz `~/.claude/hooks/falar.ps1`: "Sávio, terminei" / "Sávio, preciso de você".

## Lógica de uso

### 1. Antes de disparar
1. `python painel/painel.py pedido "<resumo curto do pedido>"` (título da aba). Se o painel não responder, rode `painel/iniciar.ps1`.
2. Feche a checklist de abertura numa mensagem só (oferta, preço, mercado, orçamento de mídia, música, compliance, criador terceiro B1/B2). Ver [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md).
3. **Confirmação de custo:** só pare para gasto real (API paga, mídia) ou ação destrutiva. Mostre o orçamento com custo em US$ + tempo médio + opção paga mais rápida. Use HeyGen (créditos já pagos) como opção "sem custo extra" quando servir.
4. Decida piloto × paralelo: método novo/caro → 1 piloto completo aprovado; método validado e barato → todos de uma vez.

### 2. Como dividir
- **Estudo:** 1 agente por fonte (vencedores, canvas do Flora, referências) ou por 1–2 vídeos (transcrição + folha de contato). Rode em background.
- **Produção:** 1 agente por AD (ou por 1–2 vídeos, ou por produto/kit em loja).
- **Revisão:** pelo menos 1 **revisor independente** que não produziu o vídeo (obrigatório em lotes A/B/C).
- **Recursos compartilhados em fila única:** upscale na GPU roda em fila única; nunca 2 montagens longas em paralelo; Whisper e OCR em sequência (disputam CPU, até 10× mais lentos); uma ferramenta compartilhada (`montar.py`, mixador) é alterada por **um agente de cada vez**, os outros esperam.
- Descobertas entre agentes (truque grátis, bug) são repassadas por `SendMessage`.

### 3. Briefing de agente (o que incluir)
Escreva um briefing único (ex.: `producao/_trabalho/BRIEFING-AGENTES.md`) e passe a cada agente o recorte dele:
- **Escopo explícito:** quais arquivos/ADs/produtos/páginas; proibição de estender a outros (regra de loja).
- **Frente, mercado, idioma, oferta** (mecânica, se fala preço, CTA) e as decisões já tomadas (compliance, B1/B2, música).
- **Skill a seguir:** `adaptar-marca`, `traduzir-criativo`, `editar-criativo`, `gerar-midia-ia`, `revisar-criativo`.
- **Caminhos absolutos:** originais, pasta de trabalho, pasta de saída, nome do arquivo final.
- **Padrões fixos:** resolução (720p para origem baixa), legenda pelo roteiro, música -32 LUFS, transcrever cada take, voz única.
- **Teto de custo** e obrigação de registrar custo real.
- **Critério de aceite** e comando de revisão (`revisar_ad.py ...`).
- **Não ler nem imprimir chaves** (`.env`).
- `PYTHONIOENCODING=utf-8` no Bash; rodar scripts do kit com diretório de trabalho em `kit-edicao-criativos/`.
- **Instrução do painel com caminho absoluto:**
  `python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa <id> "<título>" --texto "<o que está fazendo>" --k <k> --n <n>`
- Não deixar agente esperando 1 h só para medir saldo do HeyGen: o orquestrador mede depois.

### 4. Comandos do painel
```
python painel/painel.py pedido "texto"                                  # título da aba = pedido atual
python painel/painel.py etapa <id> "<título>" --texto "..." --k 3 --n 6 # etapa e progresso
python painel/painel.py img <id> <url-ou-arquivo> --legenda "..."       # cada imagem/quadro gerado
python painel/painel.py custo <id> <US$>                                # soma ao custo da tarefa
python painel/painel.py link <id> "<rótulo>" <url>                      # link (substitui o de mesmo rótulo)
python painel/painel.py fim <id>                                        # pronto
python painel/painel.py fim <id> --erro "motivo"                        # erro
python painel/painel.py fim <id> --aguardando "decisão que falta"       # aguardando a pessoa
python painel/painel.py limpar                                          # remove prontas há mais de 24 h
```
Um `id` por tarefa/agente (ex.: `ad07`, `kit1`). Use `--k/--n` para o progresso aparecer como `[k/N]`.

### 5. Acompanhar
- Processos longos: `[k/N] | % | decorrido | falta ~X` nos scripts e tempo restante nas mensagens.
- Produção noturna: cheque a cada ~25 min se algo travou e corrija.
- Job do HeyGen parado > ~45 min em "processing": reenvie igual. Seedance: espere até ~30 min antes de regerar.

### 6. Entrega
1. Revisão (`revisar_ad.py` + revisor independente) antes de dizer que está pronto.
2. Pasta numerada + índice + `00-RELATORIO-PRODUCAO.md` (custo real × orçado, decisões, músicas usadas, autorização B2 se houver, "para você olhar") + textos de anúncio.
3. Abra o arquivo no **Windows Media Player** (o player do VS Code não toca AAC) ou abra a pasta com `Start-Process`.
4. **Link clicável no topo** da resposta. Só funciona para arquivos dentro do workspace: use/crie junction `entregas-<lote>/`.
5. `painel.py fim <id>` em cada tarefa; atualize a memória do projeto (`projetos/`).
6. Resposta final curta: o que foi entregue, custo real, o que falta decidir.

### Armadilhas
- Subagente pode ser bloqueado em mutation da Shopify (desconto, pedido): o orquestrador faz, com aprovação da pessoa.
- Agente que edita ferramenta compartilhada enquanto outro roda quebra o lote.
- Piloto de 1 agente só em método validado irrita a pessoa; paralelismo total em método novo e caro arrisca o lote inteiro.

## Relacionados
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [04-fluxo-producao-criativos.md](04-fluxo-producao-criativos.md)
- [05-traducao-de-criativos.md](05-traducao-de-criativos.md)
- [06-troca-de-marca.md](06-troca-de-marca.md)
- [09-lipsync-e-avatar-heygen.md](09-lipsync-e-avatar-heygen.md)
- [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)
- [15-lojas-e-paginas.md](15-lojas-e-paginas.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [projetos/](projetos/)
