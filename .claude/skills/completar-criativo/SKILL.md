---
name: completar-criativo
description: Raio-x de um criativo de vídeo PRONTO pela estrutura de copy de resposta direta (quebra de transe, gancho 80/20, dor de identidade, 4 blocos persuasivos, CTA indireto). Diz o que já funciona, o que falta e devolve uma "versão completa" sugerida (roteiro por bloco, 5 ganchos alternativos, ajustes de imagem e de edição). Use quando a pessoa mandar um criativo pronto e pedir "o que dá pra melhorar", "como deixar completo", "outra visão desse criativo", "avalia esse anúncio" ou "o que falta nele".
---

# Completar criativo (raio-x + versão completa)

**Entrada:** um vídeo pronto (arquivo local ou link) e, se houver, o texto do anúncio e a oferta.
**Saída:** um diagnóstico curto + uma **versão completa** pronta para produzir. A skill **não edita** o vídeo:
- para produzir a versão nova: `estrategista-criativo` → `editar-criativo`;
- para mais ganchos do mesmo corpo: matriz gancho × corpo (`gerar_variacao.py`);
- para QA técnico: `revisar-criativo`.

Ela também não substitui `analista-de-copy` (métricas e banco de copy) nem `andromeda` (diversidade do lote).

## 0. Contexto
- Leia `contexto/estrategias-criativos.md` e `contexto/banco-de-copy.md` (vencedores, personas, decisões de compliance) e o `CLAUDE.md` do projeto.
- Descubra a **frente de negócio** (COD, infoproduto ou venda por conversa), o país e o idioma, a oferta e o público. Sem isso, pergunte numa mensagem só.
- **Compliance:** liste os riscos, mas **nunca suavize sozinho**. Pergunte "manter ou suavizar" (regra da pessoa).

## 1. Ler o criativo (sem custo)
1. Transcrição palavra a palavra com tempos: faster-whisper, `device='cpu'`, `compute_type='int8'`, no idioma do vídeo.
2. Folha de contato de 1 quadro/s, com close dos primeiros 3 s a 4 quadros/s, e OCR do texto na tela (RapidOCR).
3. Mapeie a linha do tempo: fala, texto na tela, cena, quem aparece, música e CTA.

## 2. Raio-x pela estrutura (nota de 0 a 2 por item, com o tempo exato como evidência)

### A. Quebra de transe (0–3 s)
- O 1º quadro **para o scroll sozinho, sem som?** (movimento, contraste, rosto, objeto estranho, título grande)
- A 1ª frase cria **tensão a resolver** ou é uma pergunta genérica do tipo "você sofre com X?"
- **Regra 80/20:** o gancho carrega a maior parte do resultado. Se ele for fraco, o resto do vídeo não importa: priorize o gancho na recomendação.

### B. Segmentação pela mensagem
- A 1ª frase **chama o comprador certo pelo comportamento** (o que ele faz, evita ou sente no dia a dia), em vez de chamar pelo rótulo ("gordo", "endividado", "ansioso")?
- Elenco, sotaque, idade e cenário batem com quem compra? O algoritmo usa isso para escolher o público.

### C. Tipo de gancho (identifique qual é usado; os melhores combinam 2)
- **Contraintuitivo:** contradiz o senso comum, e o cérebro precisa resolver a contradição.
- **Loop aberto:** uma pergunta ou história que só se resolve mais à frente. Um criativo forte abre vários loops e fecha um a um.
- **Filtro de identidade:** descreve uma cena que só quem tem o problema reconhece.
- **Origem validada:** padrão de título ou thumbnail que já provou clique em conteúdo orgânico (vídeos de muitas views do nicho, cortes de podcast com frase polêmica de especialista) ou na Biblioteca de Anúncios.

### D. Profundidade da dor (escada dos "porquês")
Classifique **até onde a copy desce**:

| Nível | O que é |
|---|---|
| 0 | Desejo de superfície |
| 1 | Incômodo físico ou prático |
| 2 | O que a pessoa evita socialmente |
| 3 | Medo de julgamento ou de perder alguém |
| 4 | Culpa ou frustração interna ("já tentei tudo") |
| 5 | Dor de identidade ("não me reconheço mais") |

- Criativo que fica no **benefício lógico** (números, termos técnicos) está no nível 0–1. A emoção compra e a lógica só justifica depois.
- Aponte **a cena cotidiana** que mostraria o nível mais fundo sem dizer a dor em voz alta.
- **Ego do público:** para público masculino, o peso costuma estar em status, respeito, autonomia e comparação com outros homens. Para o feminino, em comparação social, atratividade, medo de abandono e sensação de invisibilidade. Use como hipótese e confira com a pesquisa de público.
- **Projeção indireta:** a copy acusa a pessoa ("você é…")? Prefira terceira pessoa, uma história ou uma situação em que ela se reconheça sem se sentir atacada.

### E. Os 4 blocos persuasivos (marque início e fim de cada um no vídeo)

| Bloco | Faixa típica | Função |
|---|---|---|
| 1. Gancho e tensão | 0–10 s | Interromper a inércia e abrir uma tensão |
| 2. Transição e conexão | ~10–25 s | Mostrar que entende o dia a dia dele com detalhe concreto, tirá-lo da defensiva, qualificar sem arrogância e prometer o que vem a seguir |
| 3. Mecanismo + projeção de futuro | ~25 s até o fim do argumento | **Tirar a culpa da pessoa** (o problema era a abordagem, não ela), contrariar as soluções tradicionais que ela já tentou, apresentar o mecanismo novo e fazer a pessoa **sentir o depois** em cenas concretas |
| 4. CTA indireto | final | Evitar o "alarme de venda": o clique vira um ato de esperteza ou acesso, com motivo para agir agora **verdadeiro** |

Para cada bloco: existe? Está no lugar certo? Está concreto ou genérico?

### F. Execução que sustenta a copy
- Troca de plano a cada 1,5–4 s.
- Título ou palavra gigante nos pontos-chave.
- Legenda palavra a palavra.
- Inserções que **provam** o que é dito.
- Música baixa sob a fala.
- Mesma persona do início ao fim.
- Página, quiz ou atendimento continuam a promessa do gancho.

## 3. Entrega (em português, curta)
1. **Placar:** tabela com os itens A–F, nota de 0 a 2, evidência (tempo e frase) e o que falta.
2. **Os 3 maiores ganhos**, em ordem de impacto (o gancho quase sempre vem primeiro).
3. **Versão completa sugerida.** Roteiro por bloco, com:
   - fala e texto na tela;
   - cena ou take: o que **reaproveitar** do vídeo atual (com o tempo) e o que é **novo**;
   - duração-alvo.
4. **5 ganchos alternativos:** 1 contraintuitivo, 1 loop aberto, 1 filtro de identidade, 1 de cena cotidiana (nível 4–5) e 1 de origem validada (cite de onde veio o padrão). Cada um com a 1ª imagem sugerida. Aberturas visualmente diferentes entre si contam como criativos novos para o Meta (ver `andromeda`).
5. **Custo e caminho de produção:**
   - **barato:** reaproveitar takes, cortar, trocar o gancho, trocar o texto;
   - **médio:** voz clonada ou avatar;
   - **caro:** cenas novas geradas.

   Informe US$ e tempo de cada um, com uma opção mais rápida lado a lado.
6. **Compliance:** lista do que pode reprovar no anúncio ou gerar reclamação, com a pergunta "manter ou suavizar?".

## Regras
- **Nunca invente:** estudo, número, depoimento, ingrediente ou garantia. Use só a ficha do produto e o que a pessoa confirmar. Urgência só se for verdadeira.
- **Linguagem do mercado:** a copy sugerida sai no idioma e no tom do país do anúncio.
- **Registro:** salve em `02-relatorios/AAAA-MM_<frente>_raio-x_<criativo>.md` quando a pessoa pedir ou quando for um lote.
- **Aprendizado:** ao confirmar algo com dado de performance, registre em `contexto/estrategias-criativos.md` (só o observado, com data).
- **Erros que o raio-x já encontrou e que viram checagem fixa:**
  - loop aberto sem fechamento ("explicou a forma exata…" e o vídeo nunca explica): o bloco 3 tem que entregar o mecanismo;
  - dois CTAs com botões diferentes, ou fala depois do CTA;
  - gancho com o personagem minúsculo (câmera de segurança) ou fechado demais (sem o contexto da dor);
  - troca brusca de tom entre o depoimento (acolhedor) e a autoridade (ameaça) sem ponte;
  - trilha igual do problema à virada.
- **Referência de terceiros:** aproveite a estrutura, o ritmo e as mecânicas. As falas, os rostos, os nomes de pessoas reais e as "provas" (depoimento, print, número) não se copiam: personagens novos gerados só por texto e roteiro próprio. Em teste com personagens inventados, selo "vídeo fictício".
