# Briefing: nomear e escrever título + texto principal (73 vídeos da página «Camino con María»)

São **vídeos da própria pessoa** (infoproduto, espiritualidade, público hispânico). As ofertas de destino são duas:
- **Novena de las 9 Palabras**
- **María Desatadora de Nudos** (oração/novena)

**O destino do anúncio ainda não foi confirmado** (VSL, página, live ou WhatsApp). Por isso o CTA fica genérico: «Toca en "Más información"».

## Para cada vídeo do seu lote
Fonte de cada vídeo, tudo em `C:\Users\PICHAU\Downloads\ADLIB-CAMINO-CON-MARIA\`:
- vídeo: `TODOS\<id>.mp4`;
- transcrição: `_analise\<id>.json` (idioma, duração, texto);
- folha de quadros: `_analise\<id>_folha.jpg`.

### 1. Entender
Leia a transcrição e olhe a folha. Anote:
- o gancho dos primeiros 3 s;
- o ângulo ou dor: dinheiro, família, saúde, proteção, amor, desespero, etc.;
- o formato: avatar falando, narração com b-roll, notícia, texto na tela, etc.;
- a oferta que o vídeo já sugere: 9 palavras, desatadora, outra ou nenhuma.

### 2. Escolher a oferta
- Use **9_PALABRAS** ou **DESATADORA**, a que combinar com o conteúdo. Se o vídeo citar uma das duas, use essa.
- Se for genérico, escolha a que encaixa melhor no ângulo:
  - **desatadora** para «nudos»: problemas travados, família, dívidas, relacionamentos;
  - **9_PALABRAS** para «palabras poderosas / antes de dormir / milagro».

### 3. Nome do arquivo
`<NN>_<OFERTA>_<ANGULO>_<GANCHO-CURTO>.mp4`
- Tudo em maiúsculas, sem acento, palavras separadas por hífen, até ~60 caracteres.
- Exemplo: `07_9-PALABRAS_DINERO_REZA-ANTES-DE-DORMIR.mp4`.
- `NN` é o número do vídeo na lista global, que vem no prompt.

### 4. Título e texto principal (espanhol latino neutro, tratamento «tú»)
- **Título:** até 40 caracteres, conversa com o gancho do vídeo.
- **Texto principal:** 3 a 6 linhas curtas, com 1–3 emojis comedidos (🙏🕯️✨). Estrutura:
  1. Abertura com a dor ou o gancho do vídeo.
  2. Ponte para a oferta, pelo nome: «la Novena de las 9 Palabras» ou «la oración a María Desatadora de Nudos».
  3. CTA genérico: «Toca en "Más información"».
- **Palabras propias.** Não copie a fala do vídeo palavra por palavra no texto (pode ecoar o gancho).
- **Não invente nada:**
  - nem resultado garantido;
  - nem número de testemunhos;
  - nem «gratis»;
  - nem prazo;
  - nem preço.

  A promessa fica no nível do vídeo: fé, paz, caminhos abertos.

## Saída
Arquivo `C:\Users\PICHAU\Downloads\ADLIB-CAMINO-CON-MARIA\_analise\copy_<lote>.csv`, em UTF-8 com BOM, separador `;`.

Colunas: `NN;id_original;nome_novo;oferta;angulo;formato;duracao;idioma;gancho_3s;titulo;texto_principal`

No `texto_principal`, troque a quebra de linha por ` / `.

Não renomeie nem mova nenhum vídeo: quem renomeia depois sou eu.
