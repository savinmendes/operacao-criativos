# Carrosséis SB ES: oferta "oração ao vivo" (AD 51 a 59). Aprovado pela pessoa ("Ok faça") em 19/10/2026

**Prova aprovada, use como padrão:** `AD-50_PEDIDO-EN-SILENCIO/`.
- Arquivos da prova: `slide1..4.png`, `legenda.txt`, `receita.json`, `_contato.jpg`.
- Ferramenta: `_ferramentas/carrossel.py` (copie e adapte para layouts novos num script SEU; não quebre o do AD 50).
- Imagem do santo: `_ferramentas/santo.png`.

**Fonte das adaptações (texto já escrito em espanhol):** doc "Swipe @santaespiritualidade → San Benito" (Claude Docs `908b588c-4797-4da5-8565-1331b0e0ba19`).
- Leia com o conector Claude Docs (ToolSearch "select:mcp__claude_ai_Claude_Docs__read").
- Use `read` ref node `64232df4-b387`, engine `prose`, container {kind:project,id:908b588c-4797-4da5-8565-1331b0e0ba19}, payload {"kind":"view","from":"m57sy1sqy9m.3221"}.
- NÃO edite o doc.

**Referências visuais:** `C:\Users\PICHAU\Downloads\IG-santaespiritualidade\top20\NN_*\img*.jpg` + `legenda.txt` (posts reais do concorrente).
- Use só a COMPOSIÇÃO e o estilo; gere arte própria.
- Mapa AD → posts de referência (nº do ranking):

| AD | Posts de referência |
|---|---|
| 51 | #3, #16, #19, #20 |
| 52 | #4, #17 |
| 53 | #5, #14 |
| 54 | #6, #7 |
| 55 | #8, #11, #15 |
| 56 | #9 |
| 57 | #10 |
| 58 | #12 |
| 59 | #13 |

## MUDANÇA OBRIGATÓRIA: a oferta é a ORAÇÃO AO VIVO, não o Grimorio
- Tire TODA menção a Grimorio/Breviario/livro como produto.
  - No AD 51 o original mostra a mão segurando o livro verde: troque por mão segurando uma medalha de San Benito ou um cartão de oração.
- **CTA:** a última lâmina de cada carrossel (ou o rodapé da imagem única) chama para a live, ex.:
  - "EN ESTE MOMENTO SE ESTÁ REZANDO LA ORACIÓN DE SAN BENITO EN VIVO. TOCA EN «MÁS INFORMACIÓN» Y ÚNETE A LA ORACIÓN AHORA ↓"
  - Inclua as setas vermelhas apontando para baixo.
  - Varie a frase entre os ADs, mantendo a ideia.
- **AD 57** ("¡NO LO RECHACES! San Benito está pasando ahora..."): CTA "ENTRA A LA ORACIÓN EN VIVO QUE ESTÁ SUCEDIENDO AHORA ↓". Nunca "misa".
- **Compliance:** sem preço. Pode manter o teor de bênção/abertura de caminhos que está no doc.
- **AD 55:** faça mesmo assim. O doc diz que ele é melhor como orgânico.

## Produção
- **Formato:** lâminas 1080x1350 PNG.
- **Imagens base:** ElevenLabs Creative (ToolSearch "select:mcp__claude_ai_ElevenLabs__creative_generate_image,mcp__claude_ai_ElevenLabs__creative_get_flow_run_status").
  - Modelo `gpt-image-2.5-sunburst`.
  - Crie UM flow seu e reutilize.
  - **generations_count 2** por imagem, para economizar.
  - Peça a imagem SEM TEXTO; todo o texto vai por script (Pillow, `_ferramentas/Poppins-Bold.ttf`, desenhando → e ↓ como faz o carrossel.py).
  - Polling com poll_after_seconds até concluir. NUNCA repita uma chamada de geração para "tentar de novo".
  - As imagens vêm 1280x720: peça a composição pensando em recorte vertical, ou figura central sobre fundo liso para recortar.
- **Reaproveitamento:** reaproveite `_ferramentas/santo.png` sempre que o layout for "santo no canto + fundo liso".
- **Saída:** uma pasta por AD (`AD-NN_<NOME>/`) com:
  - `slide1..N.png` (imagem única = `slide1.png`);
  - `legenda.txt` em espanhol (fecho chamando para a oração en vivo + "Más información", 5 a 8 hashtags);
  - `_contato.jpg`;
  - o script/receita usado.
- **QA (olhe cada lâmina):**
  - acentos, ¿ ¡ « » certos;
  - texto sem encostar em figura nem cortar;
  - sem texto gerado pela IA na imagem;
  - mãos e rosto sem deformação.
- Trabalhe SÓ nas pastas dos seus ADs. Não mexa no AD 50 nem nas pastas de outro agente. Não mate processos.
- **Relatório curto:** pastas, nº de lâminas, imagens geradas e créditos.
