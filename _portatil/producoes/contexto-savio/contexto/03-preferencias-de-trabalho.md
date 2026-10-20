# Preferências de trabalho

> Como a pessoa quer que o Claude trabalhe: quando perguntar e quando seguir, como entregar, como orçar, padrões de qualidade de vídeo, regras de voz/rosto/música/compliance, escopo em loja. Cada regra traz o porquê. Abra no início de toda sessão.

## Contexto de uso

Cada preferência abaixo nasceu de um episódio real (data entre parênteses). Elas vêm das memórias `feedback_*` e das regras globais (`~/.claude/CLAUDE.md`).

| # | Preferência | Origem / porquê |
|---|---|---|
| 1 | **Só pedir confirmação para gasto real ou ação destrutiva** | 21/09/2026: "Pare de me pedir permissão pra tudo, quero que me peça permissão apenas se for algo crítico, faça o serviço completo". Antes, três pausas seguidas numa sessão (escopo de pasta, rodar script aprovado, escolher interpretação) custaram turnos sem agregar nada |
| 2 | **Narração mínima no VS Code** | 20/09/2026: a pessoa quer o visual do Claude.ai, sem texto enchendo o chat; as linhas de ferramenta já são expansíveis |
| 3 | **Abrir o vídeo/imagem ao terminar + link clicável** | 03/10/2026: não quer procurar a pasta. 07/10/2026: o player do VS Code não toca AAC (ela achou que os vídeos estavam mudos) |
| 4 | **Mostrar tempo restante** em processos longos | 03/10/2026: pediu "alguma coisa que mostre o tempo faltante" |
| 5 | **Orçamento com custo + tempo + opção paga mais rápida** | 03/10/2026, depois de ~3 h esperando o lote 1 só no PC: "às vezes vale mais a pena pagar um pouco mais pra terminar mais rápido" |
| 6 | **720p como padrão para origem baixa** | 03/10/2026, teste AD 03: diferença 720 × 1080 "imperceptível", metade do tempo (32 s × 64 s para 30 s de vídeo), metade do tamanho (volta a caber em 30 MB). "Colocar na base para sempre fazer em 720p quando for assim" |
| 7 | **Baixar sempre na maior qualidade (≥720p)** | 07/10/2026: o 1º download da Biblioteca do Meta veio 360×640 (o `src` do player é SD) e a versão 720×1280 existia nos dados da página |
| 8 | **Piloto só para método novo ou caro; senão, máximo de agentes em paralelo** | 08/10/2026, Oración: o 1º piloto saiu com lipsync errado e a pessoa perdeu confiança; depois do piloto aprovado liberou os 17 de uma vez. No mesmo dia estranhou piloto de 1 agente num método já validado (lote UK enzimas): "porque está usando só 1 agente". Rejeitou avatar completo no lugar do lipsync |
| 9 | **Compliance: perguntar, nunca suavizar sozinho** | 08/10/2026: no lote Oración as suavizações foram feitas sem perguntar; a pessoa disse que isso "deve ser perguntado a mim, se quero seguir com isso" |
| 10 | **Criador terceiro: a pessoa escolhe avatar (B1) ou mesmo criador (B2)** | 06/10/2026, lote Wyze: "poder usar o mesmo criador com a minha permissão" |
| 11 | **Marca própria: clonar a voz do narrador é liberado sempre** | 03/10/2026: os criativos enviados para adaptar são das marcas dela (expansão de mercado, ex.: Mayaverra → Lymphoria); quer manter a mesma voz para não quebrar o padrão |
| 12 | **Música trend liberada** | 09/10/2026: avisada que música com direitos pode ser silenciada/reprovada no Meta, respondeu "não cai não, pode usar". Decisão de risco dela |
| 13 | **Escopo só o pedido (loja)** | 09/10/2026: um agente etiquetou 33 produtos não-perfume; ela: "quem pediu isso? remova agora, só quero alterações nas páginas de perfumes e coleção" |
| 14 | **Priorizar vencedores** | 10/10/2026, plano Pellorini focou em modelos com mais foto e deixou o Dominante (#3 em vendas) quase de fora: "se os vencedores são esses modelos, por que focou em outros?" |
| 15 | **Nunca esconder avaliações** | 10–11/10/2026: cópia de tema Pellorini saiu com reviews desativados e CSS escondendo estrelas; ela viu "as avaliações sumiram" e mandou voltar na hora |
| 16 | **Checklist de abertura numa mensagem só** | 09/10/2026, produção Yara BF: a oferta mudou no meio (com preço → sem preço), música e legenda refeitas em 21 vídeos, 25 vídeos para um orçamento de mídia que comporta ~7, perguntas repetidas em várias mensagens |
| 17 | **Painel ao vivo + voz** | 09–10/10/2026: pediu "uma janela acoplada aqui no chat para ver as execuções em tempo real" |
| 18 | **Regras globais**: plano e 3 abordagens antes de código, TDD, code review crítico, Get Shit Done | `~/.claude/CLAUDE.md` |

### Conflito conhecido entre regras
- A regra global diz "apresente plano + 3 abordagens e **aguarde aprovação** antes de escrever código".
- A memória de 21/09/2026 (mais recente e explícita) diz "nada de apresentar plano e aguardar".
- Conciliação usada na prática (skill `estrategista-criativo` §4): apresentar as 3 abordagens com prós, contras, custo e tempo, recomendar uma e **só esperar aprovação quando houver gasto real**. Se a pessoa quiser outra leitura: **precisa de revisão manual**.

## Lógica de uso

### 1. Perguntar × seguir
- **Seguir sem perguntar:** mover/renomear em massa (fora da `001- INBOX/`), rodar script já escrito, instalar dependência local, escolher estrutura de pastas, decidir entre duas modelagens. Na ambiguidade: escolha a leitura mais razoável, declare a premissa em uma linha e siga.
- **Parar e perguntar só quando:** for gastar dinheiro real (API paga, mídia) ou destruir dado insubstituível.
- **Exceções que sempre perguntam:** compliance (manter × suavizar), criador terceiro (B1 × B2), oferta/preço quando não estiver numa fonte.
- Salvaguardas que não custam turno: copiar em vez de mover quando houver dúvida real, nunca apagar, gerar índice e relatório, declarar limitações no fim.
- Nunca pergunte "quer que eu continue?". Entregue tudo de uma vez; se for longo, divida em partes e entregue todas sem pausar.

### 2. Comunicação
- Uma frase curta no início, nada entre as ferramentas, resumo final (o que mudou / o que falta).
- No início de cada pedido novo: `python painel/painel.py pedido "<resumo curto>"` (vira o título da aba do painel).

### 3. Entrega de vídeo/imagem
1. Abra o arquivo no **Windows Media Player** (o player do VS Code não toca AAC):
   `Start-Process "$env:ProgramFiles\Windows Media Player\wmplayer.exe" -ArgumentList "`"<arquivo>`""`
2. Ponha um **link markdown clicável no topo** da resposta. Avise que o link abre no VS Code sem som.
3. O VS Code só abre links de arquivos **dentro do workspace** `Produtividade com ia`. Para pastas de fora, use (ou crie) uma junction `entregas-<lote>/`. Link relativo com `../..` falha.

### 4. Tempo e orçamento
- Scripts longos imprimem `[k/N] item | % | decorrido | falta ~X` (modelo: `kit-edicao-criativos/ferramentas/folhas_contato.py`). Ao esperar Flora/HeyGen/upscale, diga o tempo restante na mensagem.
- Todo orçamento mostra lado a lado: **custo em US$ + tempo médio + opção paga mais rápida** ("grátis/local: X h" × "pago: +US$ Y, Z min").
- Referências medidas no PC da pessoa (RTX 4070): upscale Real-ESRGAN ≈ 3× a duração; upscale 2× (720p) ≈ 1× a duração; montagem pelo kit com PC livre ≈ 0,1–0,2× a duração (~0,7× com outra tarefa em paralelo); Kling O1 Edit no Flora ≈ 3–7 min por take; ElevenLabs ≈ segundos. Nunca rodar 2 montagens longas em paralelo.
- Orce com o preço **cobrado**, não com a cotação do catálogo (ver [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md), custos medidos).
- HeyGen tem créditos já pagos que zeram todo mês: ofereça como opção "sem custo extra" (ver [09-lipsync-e-avatar-heygen.md](09-lipsync-e-avatar-heygen.md)).

### 5. Resolução e download
- Origem 360p/480p → entregue **720×1280** (`upscale_video.py --escala 2`, receita `"resolucao": "720"`). 1080×1920 só se a origem já for ≥720p ou o AD virou vencedor. Orce o tempo com upscale ≈ 1,5× a duração.
- Download sempre ≥720p. Biblioteca do Meta: capture `video_hd_url` (`Downloads/ADLIB-104060992792639/buscar_hd.py`, Playwright + Chrome headless), confira com `ffprobe`, deduplique por md5. yt-dlp: `-f "bv*+ba/b"`. Fonte abaixo de 720p: **avise antes de produzir**.

### 6. Piloto × paralelo
- Método **novo ou caro** (lipsync, avatar, tradução com rosto): 1 vídeo completo → abrir no WMP → aprovação → lote. Depois do aprovado, não peça aprovação vídeo a vídeo.
- Método **já validado e barato**: todos em paralelo desde o início, com o **máximo de agentes**.
- Lotes A/B/C: revisor independente.

### 7. Voz, rosto e música
- **Marca própria:** clone a voz do trecho limpo da narração original (ElevenLabs) e use em qualquer fala nova. Não alerte sobre direito autoral. Continue informando o custo das gerações pagas.
- **Criador terceiro:** pergunte no estudo do lote, junto das perguntas de bloqueio:
  - **B1 (padrão):** avatar HeyGen próprio + takes sem rosto, voz de catálogo, sem clone.
  - **B2:** clone da voz do criador + lipsync no vídeo original, só com autorização do criador confirmada pela pessoa. Registre "autorizado em DD/MM" no relatório.
  - Sem autorização confirmada → B1.
- **Música:** pode usar música viral real do mercado (trend TikTok do país), instrumental via demucs, com ducking. Não repita o alerta de direitos; só liste no relatório as músicas usadas. Deixe uma trilha original de IA como alternativa quando for barato. Volume padrão: **-32 LUFS sob a fala**, ducking de 11 dB.

### 8. Compliance
- Não remova nem suavize por conta própria: promessa de dinheiro/cura, ameaça, contagem regressiva, pessoa famosa, depoimento com resultado, cenas de hospital/remédio/cédula/PIX, "originais/certificado", escassez sem dado.
- Liste o que aparece em cada vídeo com o risco de reprovação e pergunte **manter × suavizar**. É pergunta de bloqueio no estudo do lote. A escolha vai no relatório e em `contexto/estrategias-criativos.md` para não perguntar de novo.

### 9. Loja (Shopify)
- Mexa **só** nos produtos/páginas pedidos. Nos briefings de agentes de loja, escreva o escopo explícito e proíba estender. Ideias de expansão → proponha, não execute.
- Avaliações, estrelas, "X reviews", "Based on N orders" ficam **sempre visíveis**. Ao duplicar/limpar tema, compare com o original e preserve review/rating. Dúvida de compliance sobre review → pergunte.

### 10. Vencedores primeiro
- Antes de montar lote ou plano de subida, levante o ranking (ordem da coleção best-sellers, analytics, ferramenta de espionagem, gerenciador) e use o **top 5** como base; o resto vai para reserva.
- Sem ranking: diga isso e pergunte.

### 11. Checklist de abertura de produção (uma mensagem só)
Pergunte de uma vez apenas o que ainda não estiver respondido:
1. Link do produto e da página de destino.
2. Oferta: mecânica, **fala preço ou não**, escassez real, tema (BF, Natal…).
3. Mercado e idioma; avatar/cena base.
4. Vencedores de referência e projeto do Flora.
5. **Orçamento diário de mídia** (define quantos criativos) e teto de produção em US$.
6. Música e formato (9:16; precisa 4:5?).
7. Compliance (manter × suavizar) e criador terceiro (B1 × B2), quando aplicável.

Enquanto a resposta não chega, adiante só o estudo (grátis). Desde a primeira versão use: legenda pelo roteiro (alinhamento forçado), música a -32 LUFS, transcrição de cada take antes de usar, voz única por clone + STS. Não repita a mesma pendência em várias mensagens.

### 12. Painel ao vivo
Em toda tarefa longa, registre etapas em `painel/painel.py` (detalhes em [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)). Há hook de voz ("Sávio, terminei" / "Sávio, preciso de você").

### 13. Regras globais de código
- Antes de código: plano detalhado + 3 abordagens com prós e contras (ver conciliação acima).
- **TDD:** testes primeiro, depois a implementação.
- Ao terminar: **code review crítico** do próprio código.
- Manter resumo do contexto do projeto atualizado e não esquecer decisões técnicas da sessão.
- Produção noturna (a pessoa dorme): trabalhe sozinho, cheque a cada ~25 min se algo travou, corrija e entregue relatório no fim.

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [02-regras-gerais-e-seguranca.md](02-regras-gerais-e-seguranca.md)
- [04-fluxo-producao-criativos.md](04-fluxo-producao-criativos.md)
- [05-traducao-de-criativos.md](05-traducao-de-criativos.md)
- [06-troca-de-marca.md](06-troca-de-marca.md)
- [08-voz-e-dublagem.md](08-voz-e-dublagem.md)
- [09-lipsync-e-avatar-heygen.md](09-lipsync-e-avatar-heygen.md)
- [10-limpeza-cor-e-qualidade-de-video.md](10-limpeza-cor-e-qualidade-de-video.md)
- [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)
- [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md)
- [15-lojas-e-paginas.md](15-lojas-e-paginas.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)
- [projetos/](projetos/)
