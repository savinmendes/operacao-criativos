# Estudo de CTA: vencedores validados x lote Lymphoria ES-CL (10/10/2026)

Fontes: `APROVADOS E VALIDADOS TIKTOK\` (AD 30 curto, VAR 06/21/28/29 = corpo do AD20/AD30 do lote Drenagem, AD 23 Supermercado).
As folhas dos últimos 12–14 s estão em `ADLIB-VITALY-CL\_trabalho\prod\_cta_v2\estudo\w1..w6.jpg`.

## Como os vencedores terminam
| Item | O que acontece |
|---|---|
| Duração do fim | 10–12 s a partir de "pides ahora". As setas ficam só nos últimos ~3 s. |
| Imagem | Foto fixa dos 3 frascos Lymphoria (P1_kit3) no AD 30 e nas VAR. No AD 23 (Pixar) o fim continua com takes da história e do frasco. **Nenhum preço na tela.** |
| Fala | "...pides ahora, te llega con envío gratis y pagas al recibir en tu casa. Y tienes noventa días de garantía o te devolvemos tu dinero. Toca el botón de abajo y pide el tuyo." Sem preço na fala. Oferta dita em poucas palavras. |
| Legenda | É a legenda normal palavra a palavra: Poppins branca com contorno, 2–3 palavras por vez, palavra-chave em amarelo (GRATIS, RECIBIR, NOVENTA). Fica um pouco abaixo do meio. |
| Selo | O selo COD do kit (preto, amarelo e vermelho: "PAGO CONTRA ENTREGA") fica no fim inteiro do AD 30 e das VAR, e no AD 23 aparece desde o começo. |
| Setas | Dois triângulos vermelhos com contorno branco, balançando, abaixo do selo. Entram na palavra "Toca" e vão até o último quadro (`cta.palavra = "toca"` do `montar_ad.py`). |

## O que estava errado no lote Lymphoria ES-CL
- Card com 3 linhas de preço ($34.990 / $59.990 / $79.990) ou caixa "COMPRE 1, RECIBA 2 · $34.990", ocupando metade da tela. A pessoa não gostou de mostrar preço.
- Card + selo grande + legenda + setas ao mesmo tempo: quatro blocos disputando a tela. Ficava "poluído", e as setas se perdiam embaixo do bloco amarelo.
- O mesmo fim (card/foto fixa) em todos os vídeos.

## Fim novo (v2)
1. **Takes de vídeo Lymphoria em movimento** (3 por vídeo, ~2,7 s cada), em combinação diferente para cada vídeo. Último take = frasco em destaque.
2. **Mesma voz** do fim anterior de cada vídeo. Reaproveitei o áudio que já existia, que não fala preço, e encurtei: saíram a frase da garantia e "gotitas de drenaje..." ⇒ "Se llama Lymphoria. Compre uno y reciba dos, con envío gratis, y pagas al recibir en tu casa. Toca el botón de abajo y pide el tuyo." (~8 s). Custo zero e sem TTS novo.
3. **Na tela, só:** a legenda palavra a palavra (keywords amarelas), o **selo pequeno** só com o bloco amarelo "PAGO CONTRA ENTREGA" (escala 0,55, sem faixa preta e sem faixa vermelha), que entra em "pagas", e as **setas vermelhas** no "Toca" até o fim.
4. Sem card, sem preço e sem bloco multicolorido. "Compre 1, Reciba 2" aparece só na fala e na legenda.
5. Música do vídeo contínua por baixo da fala (-32 LUFS). Ela continua a faixa original a partir do corte e volta ao começo quando acaba. O V09 não tem música no original (fala da criadora, sem trilha), então o fim dele fica só com a voz.
