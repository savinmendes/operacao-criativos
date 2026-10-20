# Pellorini, lote 2: 348 imagens em 20 famílias (1:1 e 9:16)

Nome do arquivo: `conceito_persona_familia_produto_formato`. Use o mesmo prefixo no nome do anúncio no Meta.
O texto do anúncio de cada conceito (C1, C2, C3, C4, C8) está em `../lote1/TEXTOS-DOS-ANUNCIOS.md`.

| Pasta | Estratégia de referência (estudo) | Qtd |
|---|---|---|
| bogo-saturado | AlphaGear: fundo laranja/amarelo/vermelho, FREE gigante | 12 |
| is-name-worth | Laphont: "Is a name worth $4,000?", setas à mão | 8 |
| vs-designer | Monomods: VS de preço, sem foto/nome de marca de luxo | 8 |
| qual-voce | AlphaGear: "Which one are you?" com 2 relógios | 8 |
| ranking | AlphaGear: "Top 4" numerado | 4 |
| email | AlphaGear: aviso em formato de e-mail | 4 |
| carta | Lucky Fours: carta só de texto | 4 |
| tweet | Lucky Fours: post da marca estilo X | 6 |
| imessage | Pascal/Lucky Fours: conversa de presente (dramatização, não é depoimento) | 4 |
| poster | Venezianico: pôster de lançamento por modelo (20 modelos) | 40 |
| limited | Chrono Customs: edição limitada (só Abito e Serpina, marcados como Limited na loja) | 4 |
| cores | Marble Veil: modelo + miniaturas das cores | 8 |
| maleta | Pelvini: 12–15 modelos "Pick 2. Pay for 1." | 4 |
| sazonal | Lucky Fours/AlphaGear: Black Friday, Christmas, Valentine | 12 |
| detalhes | Pascal Design: grade de detalhes com legenda | 6 |
| split | Pascal Design: metade pulso, metade produto | 40 |
| pulso-frase | Lucky Fours: foto no pulso + frase em etiqueta | 56 |
| estudio | Aston Paris: foto limpa só com a marca | 56 |
| vida-bogo | Pelvini/AlphaGear: foto no pulso + BOGO | 40 |
| postit | Lucky Fours: post-it escrito à mão | 24 |

**Fora do lote, de propósito:**
- Comentários, Reddit e cards de avaliação. Seriam avaliações inventadas, porque a marca ainda não tem avaliações próprias.
- Foto de celebridade.
- Nome ou foto de marca de luxo.
- Fotos da caixa e closes do mostrador, porque mostram "PELVINI" grande.

**Pendente:** o mostrador dos relógios tem a assinatura "Pelvini". Assim que estiver decidido, as fotos de origem são limpas e todo o lote é refeito com `python gerar_lote.py` e `python gerar_lote2.py`.

**Para subir (Andromeda):**
- Imagens da mesma família que mudam só o relógio contam como variações do mesmo anúncio.
- Suba **1 anúncio por família**, com 3 a 6 imagens dela em formato flexível. Não suba 1 anúncio por imagem.
- Ponto de partida: as 20 famílias = 20 conceitos visuais.
