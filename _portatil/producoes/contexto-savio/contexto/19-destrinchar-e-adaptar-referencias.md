# Destrinchar e adaptar uma referência (reel ou anúncio de terceiro)

> Método para estudar um reel ou anúncio validado de outra página (estrutura cena a cena, mecânicas, riscos) e transformá-lo em roteiro próprio para a nossa oferta, sem copiar falas, rostos nem prova social de terceiros. Caso-modelo: reel "Sagrado Verso" → San Benito ES (13/10/2026). Abra quando a pessoa mandar um reel e pedir "faz um desse pra nossa oferta".

## Contexto de uso

### Caso-modelo: reel "Sagrado Verso" (13/10/2026)
- **Referência:** reel do Instagram `DeKy6u6xSr0`, perfil Sagrado Verso, 2:13, 9:16, PT-BR. Vende um livro físico ("Grimório de São Bento") pelo link do perfil e pelo Mercado Livre. A pessoa informou que ele é validado em vendas.
- **Arquivos** (`Downloads\REELS-REFERENCIA\`):
  - `sagrado-verso_DeKy6u6xSr0.mp4` (vídeo);
  - `sagrado-verso_DeKy6u6xSr0_narracao.txt` e `_sagrado\narracao_tempos.txt` (transcrição, uso interno);
  - `_sagrado\folha.jpg` (folha de quadros);
  - `sagrado-verso_DeKy6u6xSr0_analise.md` (destrinche);
  - `sagrado-verso_adaptacao-san-benito-ES.md` (1ª adaptação: Doña Rosa + sacerdote, ~2:00).
- **Esqueleto encontrado, em 8 blocos:**
  1. gancho visual sem fala de venda (0–8 s);
  2. virada antes × depois sem explicação (8–18 s);
  3. depoimento emocional de alguém igual ao público (55+);
  4. autoridade religiosa numa moldura "AO VIVO" + urgência;
  5. ritual participativo ("repitam comigo"), em que o espectador faz a oração no vídeo;
  6. lenda/mistério com objeto físico + prova social;
  7. gancho do produto (a oração precisa ser feita "do jeito certo");
  8. CTA com escassez, compromisso ("volte em 7 dias") e compartilhamento.
- **Mecânicas que explicam o resultado:**
  - abre com cena, não com venda;
  - a dor é concreta e dita por um par do público;
  - prova em duas camadas (fiel comum + sacerdote);
  - entrega valor antes de pedir;
  - o produto vende o *método correto*, não o conteúdo grátis;
  - formato nativo (moldura de live, prints);
  - cortes a cada 3–6 s com legenda palavra a palavra em amarelo.
- **Decisões e recomendações registradas:**
  - A pessoa já tinha decidido manter a ameaça/urgência nos SB atuais.
  - **Pessoa real como autoridade, depoimento fabricado e print de WhatsApp fabricado** são outra categoria (prova falsa para o consumidor). A recomendação é não usar, nem em teste.
  - Personagens fictícios, sem nome nem @ real.
  - Selo **"VIDEO FICTICIO"** no topo à direita durante o vídeo todo.
- **Desdobramento:** o roteiro em produção em 13/10/2026 é o lote [projetos/sb-reel-medalla-es.md](projetos/sb-reel-medalla-es.md). Ele trocou a oração inventada pela inscrição pública da medalha de São Bento e o destino por "transmisión en vivo".

## Lógica de uso

### 1. Baixar e medir (grátis)
- Baixe na maior qualidade (≥720p). Instagram/Facebook: `yt-dlp -f "bv*+ba/b" <url>`. Biblioteca do Meta: `video_hd_url` via `buscar_hd.py` (ver [10-limpeza-cor-e-qualidade-de-video.md](10-limpeza-cor-e-qualidade-de-video.md)). Confira com `ffprobe`. Fonte abaixo de 720p: avise.
- Salve em `Downloads\REELS-REFERENCIA\<perfil>_<id>.mp4`, com uma subpasta `_<perfil>\` para os auxiliares.

### 2. Transcrever e ver os quadros
- faster-whisper com tempo por palavra → `<id>_narracao.txt` + `narracao_tempos.txt`. Use só para estudo, nunca no criativo.
- Folha de quadros (`folhas_contato.py`, 1 quadro a cada 1–2 s) → `folha.jpg`. Para texto na tela, use RapidOCR em sequência com o whisper (nunca os dois em paralelo).
- Anote o formato nativo: moldura de live, prints, título queimado, estilo de legenda.

### 3. Escrever o destrinche (`<id>_analise.md`)
1. Cabeçalho: link, duração, formato, idioma, o que vende e como (canal de venda), se é validado e quem disse.
2. **Tabela de blocos:** `Tempo | Bloco | Visual | Fala (resumo, nunca verbatim longo) | Função`.
3. **Mecânicas:** por que funciona, em itens curtos (abertura, dor, prova, entrega de valor, mistério, compromisso, formato nativo, ritmo).
4. **Riscos:** `Elemento do original | Risco | Alternativa`. Itens a checar sempre:
   - pessoa real identificada;
   - depoimento com resultado (principalmente financeiro);
   - prints e números inventados ("+497 relatos", "918 anos");
   - conspiração/escassez falsa;
   - celebridade;
   - promessa de cura ou de dinheiro.
5. **Adaptação:** a diferença de modelo de venda (livro físico × página/VSL), o formato recomendado (longa ~2 min + curta 31–33 s, que são as durações dos vencedores SB), o roteiro por bloco, 3–4 variações de gancho com persona/cenário diferentes (Andromeda) e o que reaproveitar do acervo.
6. **Próximos passos:** as decisões da pessoa.

### 4. Escrever a adaptação (roteiro próprio)
- Siga a **sequência de blocos**, não as frases. Texto 100% nosso, no idioma do mercado, com tradução PT ao lado para revisão.
- Use o ângulo vencedor da nossa oferta (ex.: SB ES "mala suerte/bloqueio espiritual") quando o ângulo do original for outro.
- Troque o destino pelo nosso canal ("el video que está aquí abajo", botão "Más información"/LEARN_MORE).
- A oração/texto ritual vem da oferta ou de fonte pública. **Não invente texto "oficial" do produto:** se não houver, deixe provisório e pergunte.
- Tabela final "o que mudou em relação ao original e por quê".

### 5. Regras fixas
- **Nunca copiar** fala, roteiro literal, rosto, voz, nome ou @ de terceiros. Personagens fictícios sem nome real. Prova social só real (prints de clientes, anonimizados e autorizados).
- Selo "VIDEO FICTICIO" quando houver encenação de depoimento ou de live.
- Compliance: liste os riscos e **pergunte manter × suavizar** (ver [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md) §8). Prova falsa não entra em pergunta: recomende não usar.
- Antes de gastar: orçamento (Flora/Kling/Seedance + HeyGen + ElevenLabs) com custo, tempo e opção mais rápida. Teste de 1 cena se o método for novo.

### Checklist de saída
- [ ] Vídeo ≥720p salvo + transcrição + folha de quadros.
- [ ] `_analise.md` com blocos, mecânicas, riscos e adaptação.
- [ ] Roteiro próprio, sem frase do original, com tradução PT.
- [ ] Riscos levados à pessoa; decisões registradas no projeto.
- [ ] Lote aberto em `contexto/projetos/<slug>.md`.

## Relacionados
- [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md)
- [05-traducao-de-criativos.md](05-traducao-de-criativos.md)
- [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)
- [projetos/sb-reel-medalla-es.md](projetos/sb-reel-medalla-es.md)
- [projetos/san-benito-es-vencedores.md](projetos/san-benito-es-vencedores.md)
