# Relatório: imagens Vitaly → Lymphoria (COD Chile)

**Data:** 09/10/2026
**Base:** `_trabalho/BRIEFING-PRODUCAO-LYMPHORIA.md` e `_estudo/IMAGENS.md`
**Trabalho:** `ADLIB-VITALY-CL/_trabalho/prod/IMGS/`

## Entregue: 12 de 14

| Imagem | Resolução (igual à original) | O que mudou |
|---|---|---|
| 02 - LYMPHORIA.jpg | 1080x1350 | oferta "COMPRE 1 / RECIBA 2", logo, pílula, 2 rótulos |
| 04 - LYMPHORIA.jpg | 1638x2048 | marca, mês removido, oferta, DESAPARECEN→DISMINUYEN, rótulo |
| 06 - LYMPHORIA.jpg | 1638x2048 | "Gotas LYMPHORIA®", rótulo |
| 07 - LYMPHORIA.jpg | 1501x2001 | logo, 2 rótulos |
| 08 - LYMPHORIA.jpg | 1152x2048 | logo, Cyber removido, oferta, rótulo |
| 13 - LYMPHORIA.jpg | 1080x1920 | rótulo |
| 15 - LYMPHORIA.jpg | 1638x2048 | hipotiroidismo→otras vitaminas, rótulo |
| 16 - LYMPHORIA.jpg | 1080x1350 | selo da marca, rótulo |
| 18 - LYMPHORIA.jpg | 1638x2048 | logo, "Prueba Lymphoria®", Cyber removido, oferta, rótulo |
| 21 - LYMPHORIA.jpg | 1080x1350 | manchete "QUE PAGAS AL RECIBIR", selo 2→4, botão sem %, 3 rótulos |
| 27 - LYMPHORIA.jpg | 1152x2048 | selo "COMPRE 1, RECIBA 2", rótulo |
| 28 - LYMPHORIA.jpg | 1638x2048 | logo, marca no texto, Ozempic→ayunos, GMO→sin alcohol, ícone, rótulo |

**Também na pasta:**
- `00-folha.jpg`: folha de contato;
- `00-TEXTOS-LYMPHORIA.txt`: título e texto principal de cada imagem;
- `TROCAS.md`: registro de cada troca.

**Não produzidas:** a 20 (homem, "XL a M en 6 semanas") e a 29 (antes/depois real de abdômen). Nas duas, a promessa está na foto e não no texto, então a suavização não ficaria limpa. O motivo de cada uma está em `TROCAS.md`.

## Como foi feito

1. **Rótulo.** Recortei a região do frasco na resolução cheia e passei pelo **Nano Banana 2** (`is2i-gemini-3.1-flash-image`, Flora, projeto Lymphoria). A referência foi o frasco neutro (nó n59).
   - Colei de volta **só a área do rótulo**: máscara por diferença, casco convexo e borda suavizada. Assim, fundo, mãos, folhas e textos continuam com os pixels originais.
2. **Textos.** Redesenhados localmente, sem custo (PIL/OpenCV).
   - O texto antigo foi apagado com fundo reconstruído: inpaint, gradiente ajustado ou cor da faixa.
   - Fontes usadas: Inter, Poppins, Montserrat, Anton, Archivo Black e Roboto Condensed.
   - O logo Lymphoria usa a folha extraída do rótulo n59 e o texto em Montserrat.
3. **Retentativas** (1 por imagem, no máximo):
   - **13**: a 1ª saída mudou o enquadramento (zoom out e mão nova). A 2ª ficou alinhada.
   - **18**: a 1ª saída tinha um ombro duplo no frasco, e a 2ª veio pior (reenquadrada). Fiquei com a 1ª e corrigi localmente: estiquei o vidro âmbar original entre o ombro e o rótulo.
   - **28**: o frasco do NB2 saiu ~8% mais baixo. Estiquei verticalmente para casar com o original, sem gerar de novo.

## QA (em tamanho cheio)

- Zoom 100% em cada rótulo e em cada texto trocado.
- Corrigi sobras do rótulo antigo na 02 e na 07, a mordida na manchete da 18, o halo no selo da 27 e a faixa do rodapé da 28.
- OCR (RapidOCR) nas 12 finais. Nenhuma ocorrência de: Vitaly, Cyber, 2x1, 45/60 días, kg/kilos, cancer, Ozempic, hipotiroidismo, marzo, "lleva/paga 1", 61%, "Lymphatic Drainage" ou "Herbal Experts".

## Custo

| Item | US$ |
|---|---|
| NB2, 1ª rodada, 12 gerações (02, 04 e 07 em 2K; o resto em 1K) | 0,972 |
| Retentativa 13 | 0,072 |
| Retentativa 18 (descartada) | 0,072 |
| **Total** | **1,116** (teto: 3,20) |

O texto local não teve custo.

## Pontos de atenção (revisão manual)

1. **Claims mantidos** porque não entram na regra de suavização:
   - "YO PASÉ DE TALLA XL a M*" (07);
   - silhuetas "Mes 1-3" e "¿Aún luces embarazada?" (08);
   - "24 HORAS" (18);
   - "+5.000 chilenas" (02);
   - "+858 reseñas" (27);
   - "48 horas", "Certificado y garantizado" e "Fórmula PREMIUM" (16);
   - "mujeres mayores de 40" (28);
   - "estómago más plano" (28);
   - "hasta en un 40%" no texto do anúncio da 04.
   Nenhum deles está na ficha Lymphoria.
2. **Dose.** Ficou a que cada imagem já dizia: "20 gotas" (13 e 15) e "dos gotas al día" (27). A dose real da Lymphoria segue a confirmar.
3. **Rótulo da 21.** Saiu com "Dietary Supplement 1.7 FL OZ (30 ML)" em inglês, no frasco da mão (letra pequena). Os ícones do rótulo n59 têm legendas sem sentido ("Cafimie Drainage"…), como na referência original. Em zoom isso aparece; no feed, não.
4. **Fotos de terceiros**, mantidas como no original e com direito de uso a confirmar: avatares da 13, rosto da "Carla" (28) e corpos da 06.
5. **Destino dos anúncios.** Sugestão: https://chileverificada.com/products/lymphoria (não existe landing masculina nem de celulite).
