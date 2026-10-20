# Copy por persona: «Novena de las 9 Palabras de María Desatadora de Nudos»

**O que é:** 68 vídeos da própria pessoa (página «Camino con María»), em espanhol neutro latino, com tratamento «tú». Eles vão para uma **campanha de teste**: 1 conjunto por persona, com todos os anúncios da persona dentro.

**Oferta única:** «la Novena de las 9 Palabras de María Desatadora de Nudos». O destino ainda não foi confirmado, por isso o CTA é genérico: «Toca en "Más información"».

**Base:** `personas.csv` (separador `;`) tem, para cada vídeo, o ângulo, o formato, o gancho e o texto antigo. A transcrição completa está em `<id>.json` e a folha de quadros em `<id>_folha.jpg`, nesta mesma pasta.

## As personas (hipóteses; não há pesquisa de comentários)
- **P1-DINERO-CAMINOS-CERRADOS:** quem trabalha muito e o dinheiro nunca chega. Tem dívidas e a sensação de que as portas se fecham. Também entram os de fé cansada, que rezam e nada muda.
- **P2-ENVIDIA-BLOQUEO:** quem sente que alguém lhe deseja mal. Inveja, mau-olhado, «serpientes» no caminho, coisas que travam sem explicação. Quer proteção.
- **P3-SALUD-FAMILIA:** quem carrega a saúde própria ou de alguém querido, a família desunida ou o lar sem paz. Reza pelos seus.

## Para cada vídeo da sua persona
1. **Título novo**, com até 40 caracteres.
   - Na voz da persona, ligado ao gancho daquele vídeo.
   - **Não repita título dentro da persona:** cada um tem que ser diferente.
2. **Texto principal novo**, com 3 a 5 linhas curtas e 1 a 3 emojis comedidos (🙏🕯️✨).
   1. Abertura com o micro-momento da persona (cena ou sentimento concreto, sem acusar quem lê).
   2. Ponte para o vídeo ou a mensagem.
   3. O nome da oferta por extenso: «la Novena de las 9 Palabras de María Desatadora de Nudos».
   4. «Toca en "Más información"».
   - Varie as aberturas dentro da persona: nada de começar todos do mesmo jeito.
3. **Proibido:**
   - «gratis», preço ou prazo («en 7 días», «hoy mismo»);
   - número de testemunhos;
   - cura ou dinheiro garantidos;
   - ameaça direta a quem lê.

   A promessa fica no nível de fé, paz, proteção e caminhos que se abrem.
4. **Nome do anúncio:** `<persona-curta>_<NN>_<ANGULO>_<GANCHO-CURTO>`, por exemplo `P2-ENVIDIA_23_ENVIDIA-DINERO_DETEN-TODO`. Sem acentos, em maiúsculas, com até 60 caracteres.

## Saída
Arquivo `copy_<persona-curta>.csv` (P1, P2 ou P3), em UTF-8 com BOM, separado por `;`.

Colunas: `NN;persona;nome_anuncio;titulo;texto_principal`

No campo `texto_principal`, troque cada quebra de linha por ` / `.
