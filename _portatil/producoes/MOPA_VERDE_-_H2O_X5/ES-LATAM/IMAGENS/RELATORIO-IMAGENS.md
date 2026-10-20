# Relatório: imagens H2O X5 traduzidas para espanhol neutro LATAM (08/10/2026)

- **Origem:** `IMAGENS/NN AD.jpg` (12 imagens). Os originais não foram alterados.
- **Saída:** `ES-LATAM/IMAGENS/NN AD - ES.jpg`, na mesma resolução da fonte, mais a folha de contato `00-folha.jpg` (EN | ES lado a lado).
- **Método:** FLORA, modelo Nano Banana 2 (`i2i-gemini-3.1-flash-image`) em 2K, com image-to-image e um prompt por imagem listando cada string (antigo → novo). Projeto: "MOPA H2O X5 - imagens ES (2026-10-08)" (https://app.flora.ai/projects/ns7f3t3stvqyj2j86ehj7jhbcn8fxvzv).
- **Pós-processamento:** saída de 2048 px redimensionada (LANCZOS) para o tamanho da fonte. A imagem 11 saiu em 1856×2304, foi recortada 6 px por lado para voltar a 4:5 e depois redimensionada para 1638×2048.
- **QA:** cada saída foi vista em tamanho cheio, com zoom em produto, logo da base e rodapé. Também passou por OCR (RapidOCR) para conferir o texto.
- **Fallback local com PIL:** não foi necessário.

## Custo real (charged_cost)

| Item | Execuções | Custo |
|---|---|---|
| 1ª tentativa (12 imagens × US$ 0,108) | 12 | US$ 1,296 |
| Retry da imagem 47 | 1 | US$ 0,108 |
| **Total** | **13** | **US$ 1,404** (teto: US$ 4,00) |

## Decisões aplicadas (todas as imagens)

- **Marca:** "H2O X5" mantida. Os logos com ™ e ® também foram mantidos.
- **Claims mantidos:**
  - "$55" (o símbolo $ ficou como no original)
  - 14 milhões vendidos
  - 4,000+ e 3026+ avaliações
  - 99%
  - OFERTA e unidades limitadas
  - estrelas
  - frete grátis
  - garantias
- **Números:** "4,000+" ficou com vírgula, como no original. CL/CO usam "4.000"; MX/GT usam "4,000". Revisar se a campanha for para um país específico.
- **Botões** "SHOP NOW" / "Claim My $55 Savings" → "MÁS INFORMACIÓN".
- **"USE CODE: FBX5"** (imagens 36 e 62) → pílula "PAGO CONTRA ENTREGA" no mesmo estilo. O FBX5 sumiu.
- **Referências EUA/Canadá/UK:** nenhuma aparece nas imagens (só nos textos do anúncio, fora do escopo). Não há "£" nem "Ships from USA" nas artes, então nada foi trocado por "Envío a toda Latinoamérica".
- **Marcadores de rodapé** "*", "**" e "#" foram mantidos como no original. A imagem 45 tem "ENVÍO GRATIS#" e "GARANTÍA... 30 DÍAS**", mas a nota de rodapé correspondente não existe na arte nem no original. Vale revisar se faz sentido manter.
- **Vocabulário:** "mopa", "pisos", "aparato" e "unidades limitadas" foram escolhidos por serem neutros. A tradução usa "tú".

## Por imagem

| # | Strings (EN → ES) | Tent. | Custo | QA |
|---|---|---|---|---|
| 01 | 14 MILLION SOLD WORLDWIDE → 14 MILLONES VENDIDOS EN EL MUNDO; 5-IN-1 STEAM CLEANER → LIMPIADOR A VAPOR 5 EN 1; FLOOR/CARPET/GLASS CLEANER → LIMPIADOR DE PISOS/ALFOMBRAS/VIDRIOS; GARMENT/HANDHELD STEAMER → VAPORIZADOR DE ROPA/DE MANO; SHOP NOW → MÁS INFORMACIÓN; (3026+ Reviews) → (3026+ reseñas) | 1 | 0,108 | OK. O produto foi levemente redesenhado, mas está fiel. |
| 11 | Copy/Select All/Look Up → Copiar/Seleccionar todo/Buscar; Now you can clean every surface in your home with just one device → Ahora puedes limpiar *cada superficie* de tu hogar con ***un solo aparato***; H2O X5 5-in-1 Steam Cleaner → H2O X5 5 en 1 / Limpiador a vapor | 1 | 0,108 | OK. O "1" fica sobre o aparelho, como o original. |
| 13 | JUST ADD WATER. → SOLO AGREGA AGUA.; LET STEAM DO THE CLEANING. → DEJA QUE EL VAPOR LIMPIE POR TI.; 4,000+ 5-STAR REVIEWS → 4,000+ RESEÑAS DE 5 ESTRELLAS | 1 | 0,108 | OK |
| 28 | STEAM MOP → MOPA A VAPOR; SALE → OFERTA; NOW ON! → ¡YA DISPONIBLE!; LIMITED STOCK ONLY! → ¡UNIDADES LIMITADAS!; SHOP NOW → MÁS INFORMACIÓN | 1 | 0,108 | OK |
| 33 | ONE MOP. → UNA MOPA.; WHOLE-HOME CLEAN. → TODA LA CASA LIMPIA.; 5 cleaning modes. Powerful steam. → 5 modos de limpieza. Vapor potente.; No added cleaning chemicals. → Sin químicos de limpieza añadidos.; 5-STAR REVIEWS → RESEÑAS DE 5 ESTRELLAS | 1 | 0,108 | OK |
| 36 | STEAM CLEANER → LIMPIADOR A VAPOR; SALE → OFERTA; NOW ON! → ¡YA DISPONIBLE!; LIMITED STOCK ONLY! → ¡UNIDADES LIMITADAS!; USE CODE: FBX5 → PAGO CONTRA ENTREGA | 1 | 0,108 | OK. FBX5 removido. |
| 45 | LIMITED TIME OFFER → OFERTA POR TIEMPO LIMITADO; $55 OFF → $55 DE DESCUENTO; POWERFUL STEAM → VAPOR POTENTE; A HEALTHIER HOME → UN HOGAR MÁS SALUDABLE; KILLS 99%... → ELIMINA EL 99% DE BACTERIAS, VIRUS Y GÉRMENES*; CHEMICAL FREE → SIN QUÍMICOS; 5-IN-1 MULTI-SURFACE VERSATILITY → 5 EN 1 VERSATILIDAD MULTISUPERFICIE; FLOORS/KITCHEN/BATHROOM/CARPETS/WINDOWS → PISOS/COCINA/BAÑO/ALFOMBRAS/VENTANAS; rodapé → 4,000+ RESEÑAS DE 5 ESTRELLAS / ENVÍO GRATIS# / GARANTÍA DE DEVOLUCIÓN DE 30 DÍAS** / 1 AÑO DE GARANTÍA GRATIS | 1 | 0,108 | OK. O logo da base sai espelhado/ilegível, igual ao original. Ver a nota sobre "#" e "**". |
| 47 | ONE DEVICE... → UN SOLO APARATO...; 5 CLEANING SOLUTIONS FOR EVERY CORNER OF YOUR HOME! → ¡5 SOLUCIONES DE LIMPIEZA PARA CADA RINCÓN DE TU HOGAR!; Handheld Steamer → Vaporizador de mano; Comes with many attachments → Incluye muchos accesorios; Floor Cleaner → Limpiador de pisos; and carpet steamer → y vaporizador de alfombras; Must-have for every home → Imprescindible en todo hogar; H2O X5 5-in-1 Steam Cleaner → H2O X5 5 en 1 / Limpiador a vapor | 2 | 0,216 | Na 1ª tentativa o emoji de estrela cobria as reticências. A 2ª (usada) deixa as reticências legíveis, mas o emoji ainda encosta no último ponto e na haste da mopa. É um detalhe estético. |
| 58 | LIGHTWEIGHT. → LIGERA.; EASY TO MOVE. → FÁCIL DE MOVER.; Clean upstairs, downstairs and everywhere between. → Limpia arriba, abajo y en todas partes.; 4,000+ 5-STAR REVIEWS → 4,000+ RESEÑAS DE 5 ESTRELLAS | 1 | 0,108 | OK |
| 59 | LIMITED TIME OFFER → OFERTA POR TIEMPO LIMITADO; $55 OFF → $55 DE DESCUENTO; A CLEANER HOME → UN HOGAR MÁS LIMPIO; NATURALLY → NATURALMENTE; POWERFUL STEAM. REAL RESULTS. NO HARSH CHEMICALS. → VAPOR POTENTE. RESULTADOS REALES. SIN QUÍMICOS AGRESIVOS.; ícones e tiles iguais aos da 45 | 1 | 0,108 | OK |
| 61 | EXCLUSIVE LIMITED-TIME OFFER → OFERTA EXCLUSIVA POR TIEMPO LIMITADO; A Healthier Home, Powered by Steam → Un hogar más saludable, con el poder del vapor; SAVE $55 → AHORRA $55; On the H2O X5 Steam Cleaner → En el limpiador a vapor H2O X5; 5-in-1 → 5 en 1; Kills 99%... → Elimina el 99% de bacterias, virus y gérmenes*; Chemical-Free → Sin químicos; 5-in-1 Versatility → Versatilidad 5 en 1; 4,000+ Reviews → 4,000+ reseñas; 30-Day Money-Back Guarantee → Garantía de devolución de 30 días; Claim My $55 Savings > → MÁS INFORMACIÓN >; nota → *Según pruebas de laboratorio controladas. La eficacia varía según el tiempo de aplicación y la superficie. | 1 | 0,108 | OK |
| 62 | STEAM CLEANER → LIMPIADOR A VAPOR; SALE → OFERTA; LIMITED TIME ONLY → SOLO POR TIEMPO LIMITADO; USE CODE: FBX5 → PAGO CONTRA ENTREGA | 1 | 0,108 | OK. FBX5 removido. |

## Precisa de revisão manual

1. **Imagem 47:** o emoji de estrela encosta nas reticências de "UN SOLO APARATO...". É leve e o texto está legível. Se incomodar, apague o emoji num editor.
2. **Imagem 45:** os marcadores "#" (ENVÍO GRATIS#) e "**" (GARANTÍA...) apontam para notas que não existem na arte. Confirme se a oferta LATAM tem frete grátis e garantia de 30 dias e 1 ano; se não tiver, ajuste a arte.
3. **Formato do número:** confirme "4,000+" vs "4.000+" conforme o país de veiculação.
4. **Moeda:** o "$55" foi mantido por decisão da dona. Confirme se o desconto vale em USD ou em moeda local no país da campanha.
