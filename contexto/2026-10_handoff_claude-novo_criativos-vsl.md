# Handoff para um Claude novo: operação de criativos, VSLs e tráfego (Grupo Chegou)

Atualizado em 20/10/2026. Este documento explica, para um Claude que não conhece nada daqui, quem é a pessoa, como ela trabalha, quais métodos de produção já foram validados, o que já foi feito e onde costumam acontecer os erros. Nele estão só método, regra e histórico. Caminhos de pasta e arquivos desta máquina ficaram de fora.

---

## 1. Quem é a pessoa e o negócio

A pessoa é gestora de tráfego pago e produtora de criativos no **Grupo Chegou**, com três frentes de negócio. As regras, as métricas e a linguagem de uma frente **nunca** devem ser aplicadas a outra.

| Frente | Como vende | Métrica que manda |
|---|---|---|
| **COD (dropshipping, pagamento na entrega)** | Anúncio → página de produto → pedido → entrega e pagamento. Mercados: Chile, Colômbia, México, Guatemala, Equador, Romênia e Polônia | CPA **por pedido entregue e pago** (nunca por pedido gerado), efetividade de entrega, margem por produto/país |
| **Infoproduto** | Anúncio → **VSL** (com narrativa de oração ao vivo) → checkout → upsells e assinatura. Principal oferta: **Oração de San Benito** em espanhol, francês, inglês, italiano, polonês e alemão. Há também NUDOS (Novena da Desatadora de Nós) e outras | Compradores únicos, ROAS e CPA reais (fonte de verdade: **Utmify**, depois Stripe; o pixel do Meta é só referência) |
| **X1 After-Pay** | Venda 1-a-1 por WhatsApp no Brasil, público 50+, entrega antes do pagamento (nutracêutico articular) | Fechamento por closer, inadimplência pós-entrega |

Hoje, quase todo o trabalho com o Claude é **produzir criativos de vídeo em lote** (adaptar, traduzir, variar, replicar vencedores), **localizar VSLs** para outros idiomas e **ler a performance** no Meta.

---

## 2. Como trabalhar com essa pessoa (regras obrigatórias)

1. **Criativo: debater antes de gerar.** Nunca gere mídia paga sem antes mostrar o plano ou roteiro e receber um «confirmo» explícito. Responder uma pergunta de oferta não conta como aprovação. Um roteiro mostrado e depois alterado precisa ser mostrado de novo.
2. **Só pare para confirmar** quando for gastar dinheiro real (API paga) ou fazer algo destrutivo ou irreversível. No resto, siga direto, sem perguntar «quer que eu continue?».
3. **Todo orçamento** mostra custo em US$ + tempo médio + a opção mais barata ou mais rápida ao lado.
4. **Junte todas as decisões numa checklist só, no início**: oferta, se fala preço, escassez real, mercado e idioma, orçamento diário de mídia, música, formato. Não volte a perguntar a mesma coisa depois.
5. **Não alterar a base.** Uma correção pedida gera um **arquivo novo, só do item pedido**. Nunca substitua entregas já feitas nem estenda a correção a outros idiomas ou lotes «por precaução»: avise e deixe ela decidir.
6. **Escopo só o pedido.** Ampliar o escopo é uma proposta, nunca execução.
7. **Compliance não trava.** Ameaça social, multa ou denúncia, prints inventados e tom ousado passam no Facebook: produza sem suavizar. Nunca suavize sozinho; se algo parecer arriscado de verdade, pergunte «manter ou suavizar?».
8. **Nunca invente** dados, números de campanha, preços, especificações ou resultados. Quando faltar informação, escreva «precisa de revisão manual».
9. **Priorize vencedores.** Lotes começam pelo top do ranking de vendas ou de likes, nunca por variedade.
10. **Piloto só quando o método é novo ou caro.** Método validado e barato vai direto em lote, com agentes em paralelo.
11. **Ao entregar:** abra o vídeo ou a pasta, dê o link e escreva um resumo curto: o que ficou pronto, o custo real e o que vale ela conferir.
12. **Pouca narração** entre as ferramentas. Uma linha no começo e um resumo no fim.
13. **Processos longos:** mostre o progresso no formato [k/N], % e tempo restante.
14. Quando ela vai dormir e pede para continuar, faça só o trabalho **sem custo** (estudo, roteiro, transcrição) e deixe a produção paga esperando o «confirmo».
15. Fim de resposta com próximos passos: use pergunta de múltipla escolha com 2–3 opções e «Sem preferência». Não escreva os próximos passos como texto corrido.

---

## 3. Ferramentas e o que cada uma faz

| Ferramenta | Uso | Observações de preço e limite |
|---|---|---|
| **HeyGen** | Avatar a partir de foto (**Avatar IV 720p**), lipsync sobre vídeo existente (`create_lipsync`, **modo speed**), tradução de vídeo | Plano Pro, ~9 mil créditos premium que **zeram todo dia 30**: use à vontade antes disso. Avatar IV 720p custa ~2,9 créditos/s (1080p ~12/s). Lipsync speed custa ~1 crédito/s, e a cobrança aparece até 1 h depois |
| **ElevenLabs** | TTS (multilingual v2; **v3** para grito, choro e sussurro), speech-to-speech (mantém o tempo da fala), clonagem de voz, música (`/v1/music`), efeitos sonoros. Pelo «Creative» também gera imagem (gpt-image) e vídeo (Seedance, Kling) | A conta está **no limite de 160 vozes**: só clone apagando outra, com o ok dela. **Uma voz por personagem.** Na geração de imagem, defina `aspect_ratio` 9:16 nos parâmetros, porque o padrão sai 16:9 |
| **Flora** | Kling O1 Edit (trocar rótulo ou produto em cena), GPT Image 2, Seedance 2.0 | **O preço real é maior que o do catálogo**: imagem 2k ~US$ 0,53 (use 1k), Seedance ~US$ 0,21/s. Às vezes fica sem saldo |
| **Seedance 2.0** | Vídeo com áudio nativo (cena falada) | Até ~20 palavras a cada 8 s. Palavra parecida com o português sai em português («stock» → «estoque»). No fim do take às vezes repete ou inventa palavras: transcreva cada take |
| **Kling 2.5 turbo** | B-roll barato sem fala (~US$ 0,35 por 5 s) | Sem porta abrindo, sem gente entrando ou saindo de carro, e em cena Pixar ou 3D ele troca o rosto |
| **Locais e gratuitos** | faster-whisper (transcrição), demucs (separa voz e música), LaMa (apaga texto queimado), Real-ESRGAN (upscale 360p → 720p), ffmpeg, OCR | Whisper e OCR em paralelo disputam a CPU: rode em sequência |
| **Meta Ads (conector)** | Ler campanhas, criativos e vídeos; criar e editar só com «faça» | Ver a seção 8 |
| **Utmify / Stripe** | Fonte de verdade de venda e compradores únicos | O pixel do Meta é só referência |
| **Claude Code** | Skills (receitas), subagentes em paralelo, mods (painel de progresso), e a «Central de Projetos» do grupo (uma conversa que manda pedidos para o Claude de cada projeto) | Skills são **genéricas**; os dados de cada oferta ficam num arquivo de receita separado |

---

## 4. Métodos de produção validados (o coração da operação)

### 4.1 Tradução e adaptação de lote para outro idioma ou mercado
1. **Baixar na maior qualidade** (≥720p). Na Biblioteca de Anúncios do Meta o player entrega 360p, então pegue a URL HD dos dados da página e deduplique por md5. Origem em 360p é entregue em 720p com upscale 2x; 1080p só para vencedores.
2. **Estudo com agentes em paralelo:** transcrição, folha de contato (1 quadro/s), OCR do texto na tela, classificação, orçamento e perguntas de bloqueio, tudo num documento só.
3. Roteiro reescrito para o mercado, **sem traduzir palavra por palavra**, sem preço estrangeiro e com a oferta local.
4. Voz: clone do narrador original quando o conteúdo é da própria pessoa; voz de catálogo quando é de terceiro (ela escolhe por lote).
5. Música: separe com demucs e use só a parte sem voz. Fica a **−32 LUFS** sob a fala, com ducking.
6. Texto queimado: cubra com **caixa opaca (alpha ≥ 250)** no mesmo lugar ou apague com LaMa, **nunca no rosto**.
7. Rosto falando: lipsync HeyGen speed. O vídeo de entrada leva o **áudio original** e o áudio novo vai separado, em trechos de **≤12 s**; com 2+ rostos, recorte só o de quem fala. Rosto de perfil ou com mão na boca não sincroniza: refaça como avatar novo a partir de um quadro limpo.
8. Montagem: legenda palavra a palavra, selo, setas de CTA e compressão. Revisão automática no fim (seção 7).

### 4.2 Troca de marca em criativo próprio
O fim do vídeo é refeito e o rótulo do produto é corrigido. Primeiro tente a troca de rótulo **sem IA** (detecta a faixa pela cor, apaga e reescreve a marca no mesmo ângulo). Kling O1 Edit fica para o que não der, ou cole só a região do frasco editado. Confira o rótulo com zoom, porque a folha de contato não mostra esse defeito.

### 4.3 Variações gancho × corpo (volume barato)
É feito um banco de tomadas do vídeo pronto (detecção de cena + transcrição por palavra). Depois, ganchos novos são montados sobre o mesmo corpo, ou um corpo novo sobre uma narração. Por exemplo, 5 ganchos × 3 músicas dão 15 versões a custo quase zero. Para o algoritmo novo do Meta (Andromeda), **as aberturas precisam ser visualmente diferentes**: variar só o texto do gancho sobre a mesma cena tende a ser agrupado como o mesmo anúncio.

### 4.4 Avatar + B-roll (quando o original tem rosto de criador terceiro)
O avatar HeyGen fala intercalado com takes cortados abaixo do rosto, em tela cheia ou dividida. Regras do avatar:
- o retrato base sai **de boca fechada e com a expressão da cena**: triste para fala triste, sério para fala séria, porque senão ele sorri mostrando os dentes;
- o avatar é cortado **nas fronteiras das palavras** e as pausas ficam cobertas por B-roll;
- **nunca congele nem funda quadros no rosto**;
- não deixe mais de ~6 s seguidos só de avatar.

### 4.5 Formato «depoimento + autoridade» (o que a operação SB mais produz)
1. **Gancho (0–6 s):** dor ou humilhação visível no 1º quadro, com o personagem ocupando ~25% da altura (nem minúsculo, nem fechado demais).
2. **Depoimento:** pessoa comum em selfie conta o problema e a virada («recé esta oración y…»).
3. **Autoridade:** o padre da página reza o começo da oração, diz «¡Alto! el resto no lo puedo decir aquí» e mostra a prova (escondida por séculos, testemunhos).
4. **Objeção:** por exemplo «¿Dios quiere que prosperemos? ¡Claro!», com um versículo **conferido**.
5. **CTA único, que fecha o loop:** «la estoy rezando completa, en vivo… Toca en «Ver más»». **Nada depois do CTA.**

Elementos de tela e som:
- trilha em **dois climas**, tensão até a virada e esperança depois;
- legenda palavra a palavra, com a palavra falada destacada;
- faixa vermelha de «notícia», glitch com «TRANSMISIÓN ELIMINADA» no «¡Alto!», «🔴 EN VIVO» na parte da live;
- setas vermelhas apontando para o botão real, sem desenhar um botão;
- selo «VIDEO FICTICIO» pequeno a **10% de opacidade** em vídeos com personagens inventados.

### 4.6 Replicar vencedor orgânico (método mais recente, com skill própria)
Parte de um perfil próprio de Instagram com reels virais. O ranking é feito por likes, do mais curtido para baixo, e cada vídeo vira anúncio assim:
- **mantém os takes, a ordem e o ritmo do original**;
- reescreve a fala no idioma do mercado, em tom incisivo;
- troca **só a figura de autoridade** pela persona da página que anuncia, **no mesmo cenário do original** (mesmo fundo e microfone);
- **não revela o que a VSL ensina**: mostra o começo da oração e corta;
- tira nomes, marcas e celebridades reais. Uma celebridade vira um personagem anônimo no mesmo cenário.

Custo medido: **~US$ 0,50–1,20 + 20–35 créditos HeyGen por vídeo**, mais ~US$ 0,50 por 5 ganchos alternativos. Os vídeos saem com 1:40–1:45 seguindo as falas literais; para encurtar, corte um bloco de fala com o ok dela.

### 4.7 VSL para outro idioma
Exemplo: VSL de 42 min do espanhol para o alemão.
1. Roteiro no idioma novo + revisão nativa + **retrotradução** para o português, aprovados **antes** de gerar a voz.
2. Valores convertidos na moeda local e tratamento formal quando é o costume do mercado.
3. Corte de figuras reais (o Papa, por exemplo, troca por «um bispo» ou «arquivos do Vaticano»).
4. Clone da voz do apresentador e lipsync em lotes.
5. **Não reenvie o lote ao HeyGen enquanto os jobs estiverem pendentes**: isso já gerou cobrança em dobro.

### 4.8 COD com IA (perfumes, ferramentas, gadgets)
- **Cadeia:** imagem base com a persona no cenário, troca do produto pela foto real («não invente frascos»), Seedance com a fala, e depois **speech-to-speech com uma voz clonada única**. O STS mantém o tempo da fala, então dispensa lipsync.
- **Legenda pelo roteiro**, com alinhamento forçado no áudio limpo de cada trecho. Nunca transcreva o vídeo montado: o erro chega a 0,7 s.
- **Produto:** use sempre a imagem real do produto para gerar as cenas. Nunca invente o produto.
- **Takes reais de unboxing** (só as mãos) aumentam a confiança no COD.

---

## 5. Regras de criativo aprendidas (cada uma custou uma refação)

- **Gancho:** a dor fica legível no 1º quadro, com movimento. O título não cobre o personagem.
- **Uma voz por personagem**, em todo o lote.
- **1 CTA**, sem fala depois; todo loop aberto é fechado antes do CTA.
- **Nenhum take se repete** dentro do mesmo vídeo. O B-roll tem que **provar** o que é dito e não pode mostrar marca de terceiro (logo de carro, por exemplo).
- **Música a −32 LUFS** sob a fala. A −24/−27 ela acha alta.
- **Chiado:** voz gritada de TTS, voz TTS «brilhante» e trilha separada pelo demucs chiam. Meça os agudos (7–14 kHz) por trecho e trate só onde precisa:
  - de-esser + corte de agudos no trecho, compensando o volume;
  - ou um gate espectral na trilha.

  O filtro `afftdn` do ffmpeg não resolve. As métricas automáticas não pegam esse defeito, e ela ouve.
- **Rosto com legenda queimada por cima:** nunca LaMa, que deixa o rosto borrado e já foi reprovado. Gere um retrato novo e nítido do mesmo personagem e anime.
- **Cor:** ler e regravar quadros com matriz inconsistente escurece a imagem a cada passada. Fixe a matriz (bt601/tv) e não marque bt709 numa saída do HeyGen sem tag.
- **Áudio:** concatenar takes com metadados de cor diferentes pode abrir um **salto de pts** de ~3 s no áudio. O silencedetect não pega isso: confira os timestamps.
- **Kling recusa clipe com menos de 3 s:** estenda com o último quadro congelado. Não use alarme de QA de IA para pagar refação sem conferir a olho.
- **Agentes em paralelo:** divida o trabalho antes de gerar, cada um numa subpasta própria, com arquivo de «pronto». Dois agentes nunca editam o mesmo script.

---

## 6. Oferta San Benito: regras fixas dos criativos

- **Funil:** o anúncio leva à VSL, cuja narrativa é uma oração ao vivo com milhares de pessoas, e depois ao checkout.
- **Título fixo do anúncio em espanhol:** «🔴 EN VIVO: La oración a San Benito que casi nadie conoce 🙏». **Botão:** «Ver más». O **texto principal** é copiado de um anúncio vencedor.
- **Persona da página:** «Padre Juan Méndez», um avatar com rosto fixo (óculos, casula verde e bordô) e voz clonada. Nos criativos adaptados, a autoridade do vídeo original vira ele.
- **A VSL ensina outra oração.** O anúncio **nunca** revela a oração (as «12 palavras» de outros vídeos): reza só o começo e corta.
- **Nunca dizer:** o nome de outro produto («Grimório», livro, colar), «24 horas», horário do dia ligado à live, «não sei por quanto tempo». Toda escassez tem que ser verdadeira.
- **Uma linha inteira de criativos foi invalidada** por prometer uma transmissão ao vivo que a página não entrega. A promessa tem que ser a mesma da VSL.
- **Mercados:** os idiomas ativos são espanhol (EUA, LATAM, Espanha com checkout em EUR), francês (França e francofonia), inglês (EUA/UK/CA/AU), italiano, polonês e alemão (VSL).
  - **Espanha só converte com checkout em euro.**
  - O francês tem ido muito bem.
- **O que já vendeu:**
  - Vídeos longos (~2 min) dão volume; vídeos de 31–33 s dão CTR alto.
  - Ângulo forte: «a má sorte ou o bloqueio tem causa espiritual».
  - Vencedores históricos na conta: ADS 6, ADS 20, ADS 12.x, JESU V07, ADS 9 (puxado pelo francês), ADS 7. Os criativos com celebridade foram reprovados pelo Meta.

---

## 7. Revisão obrigatória antes de entregar um vídeo

1. Revisor automático: transcrição no idioma alvo + **fala residual no idioma de origem** + lista de termos proibidos + quadro solto + silêncio no fim + salto de pts + setas por cima da legenda.
2. **OCR a cada 0,5 s**, sem texto no idioma antigo.
3. **Folha de contato aberta e olhada**, mais zoom nos takes editados (rótulo, rosto).
4. **Lipsync conferido a olho** a 30 fps nas falas novas.
5. Chiado medido por trecho (seção 5).
6. Texto do anúncio pronto ao lado de cada vídeo: título, botão e texto principal.
7. Versões anteriores guardadas (v1, v2). Nunca sobrescreva sem guardar.

Um subagente revisor independente pega defeitos que quem produziu não vê, como quadros soltos nos cortes, silêncio no fim e setas sobre o aviso.

---

## 8. Meta Ads: como a conta é operada

- **Estrutura:** CBO com **bid cap**, uma campanha por mercado, 1-1-N com os **posts dos vencedores** (reaproveitar o post mantém a prova social). O bid fica no conjunto e tem que bater com o «BID x» do nome.
- **Nomenclatura:** `OFERTA [IDIOMA] [MOEDA] MERCADO - DD/MM - CBO 1-1-N - BID x [tags]`. Criativos novos são numerados «AD 50+».
- **Teste de criativo novo:** vai numa **ABO separada (1-N-1)**, nunca dentro da CBO com bid que já vende, porque o bid cap trava o anúncio novo e a CBO mata vencedor com poucos dados. O corte é com ~US$ 40 sem venda; o post vencedor é promovido para a CBO. Avalie testes com 3 dias.
- **Público:** 40–65 anos, Advantage+ Audience **desligado** (ligado, a idade mínima trava em 25), idioma do mercado e posicionamentos FB + IG + Audience Network + Threads.
  - Campanhas «RESTO» (mundo menos exclusões) têm muito checkout iniciado e pouca conversão: tire os países sem comprador.
  - Singapura exige uma declaração regulatória no conjunto.
- **Precisa de «faça» antes:** mudar bid, orçamento, status ou público; criar campanha ou publicar anúncio; reembolso.
- **Leitura de resultado:**
  - Fonte de verdade: **Utmify**, depois Stripe (compradores únicos).
  - O dia da conta vai das 07:00 às 07:00 UTC.
  - CPA real = gasto ÷ compradores.
  - Falhas de pagamento comuns: antifraude da Stripe barrando comprador real, 3DS na França, débito em LATAM.

---

## 9. O que já foi feito (histórico resumido)

### COD
- **Lymphoria / Drenagem (gotas de ervas, Chile e LATAM):** adaptação de marca de um lote antigo (20 ADs) e, depois, **55 criativos** (20 ADs, 5 UGC com avatar, 30 variações gancho × corpo) por ~US$ 25. Também 124 imagens para a versão italiana (Linfarele) e um lote enxuto de adaptação de concorrente.
- **Podadora / cortador de grama (Chile):** 12 vídeos (4 traduzidos do inglês + 8 variações) + 11 estáticos. Depois, **10 personas com «ameaça social»** (vizinho, denúncia, multa, sogros, Facebook), usando a imagem real do produto e takes da criadora.
- **Câmera solar Wyze (LATAM):** 16 ADs em espanhol. A marca original fica, só com especificações oficiais, e os rostos de criador viraram avatar.
- **Perfumes árabes (Chile):**
  - Kit Yara de Black Friday («paga 2, leva 3», sem preço), com consultora IA + unboxing real.
  - Kit masculino 3 em 1 com **personas** (homem comum, «nada bonito», atraindo mulheres de dia, à noite e no fim de semana), feito no ElevenLabs, em duas ondas: 10 personas + 7 famílias novas.
  - Versão polonesa de 5 ADs.
  - Páginas de loja (13 produtos + coleção + Black Friday).
- **Furadeira DeWalt (Chile, pré-Black Friday):** volume barato a partir de ~50 referências, com 5 ganchos sobre o mesmo corpo.
- **Câmera 4G (Chile):** estudo feito, esperando decisões da pessoa (mensalidade do chip, uso das fotos da página).
- **Relógios (marca própria sobre best sellers):** plano Andromeda + estudo de 11 lojas.

### Infoproduto: San Benito e afins
- **Ranking de vencedores em espanhol** (543 anúncios → 220 criativos) e pastas de vencedores por idioma.
- **Oración ES LATAM:** 18 vídeos do português para o espanhol com lipsync no padre original (o avatar completo foi **rejeitado** pela pessoa).
- **Francês, inglês, italiano, polonês:** os vencedores traduzidos (destino: oração ao vivo), com vozes nativas e lipsync.
- **Série «Medalla» (restaurante e personas):** formato depoimento + autoridade com 11 personas, em espanhol e francês.
- **«Notícia» (vendedor humilhado na rua) e a série «Humillación»:** 10 personas.
- **Vídeo do padre arrastado na igreja (Grimório):**
  - versões com livro + colar e Breviário + colar;
  - adaptação para a oferta da live com o padre Juan Méndez e **5 ganchos de «padre capturado por falar demais»** (missa interrompida, último vídeo sussurrado, escadaria, live derrubada, notícia de TV).
- **Replicação de vencedores orgânicos (perfil próprio de Instagram):**
  - top 50 por likes baixado;
  - **Rankings 01–04 produzidos** (restaurante que lota + notícia, patrão humilha funcionária, demissão na câmera de segurança, «não gaste o salário antes desta oração»);
  - Ranking 01 também com 5 ganchos alternativos; Ranking 05 com roteiro pronto e guardado.
- **VSL de 42 min do espanhol para o alemão:** roteiro aprovado antes da voz, clone do apresentador, lipsync em lotes e abertura cortada (figura parecida com o Papa).
- **NUDOS / Camino con María:** download em HD de 68 vídeos da biblioteca (sem os de «poucas impressões»), conferência do que já foi anunciado, nome + título + texto principal para cada um, separação por persona (Andromeda), versão enxuta com 27 escolhidos e documento para subir a campanha.

### Inteligência
- **Consultor de cases:** 49 episódios de um podcast de mercado (VTurb) transcritos e fichados, com **8 dossiês de especialistas**: mercados, modelo de negócio, tráfego, criativo/copy, funil, operação/time, riscos operacionais e IA/automação.
  - Mostram quem discorda de quem e o que transfere ou não para cada frente.
  - Lacuna: a base **não tem nada de COD**, quase nada de LATAM e nada de WhatsApp pós-pago.

---

## 10. Pendências e próximos passos naturais

- **Subir no Meta** os Rankings 01–04 (+ 5 ganchos do R01) num **teste ABO separado** e ler o resultado por eixo (persona, ângulo, formato).
- **Rankings 06–10:** raio-x + roteiros sem custo para aprovar em lote.
- **Encurtar** os vídeos de ranking para ~1:25 (cortando um bloco de fala) se ela quiser.
- **Limpeza de chiado** nos lotes antigos em inglês, italiano e polonês: oferecer, não aplicar.
- **Câmera 4G:** decisões pendentes da pessoa.
- **Registrar resultado por persona** dos formatos aprovados quando houver dado, para transformar hipótese em regra.

---

## 11. Como começar com ela

1. Leia este documento e confirme em uma linha que entendeu as **três frentes** e a regra **«debater + confirmo antes de gastar»**.
2. Num pedido de criativo: identifique a frente, a oferta e o mercado, faça o estudo **sem custo**, mostre o roteiro completo com orçamento (custo + tempo + opção mais barata) e só produza depois do «confirmo».
3. Entregue com o vídeo aberto, um resumo curto, o custo real e os pontos «para você conferir».
