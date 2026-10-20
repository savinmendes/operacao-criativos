# Kit 1 Yara + Yara Moi + Yara Elixir: imagens da página (Chile)

Data: 09/10/2026 · Produto Shopify: `gid://shopify/Product/10212552179968` (continua em **RASCUNHO**, preço 0 sem alteração)
Admin: https://admin.shopify.com/store/13cc83-26/products/10212552179968
Canvas Flora: https://app.flora.ai/projects/ns72zge7hvbtq4mb73es6nkgm98fyfzn

## Estrutura copiada da página base (pack 3x1 masculino)
A base usa 4 imagens 1:1 na galeria (hero do kit e uma foto de cada frasco) e 5 imagens altas embutidas na descrição: 4 blocos de 937x1678 e a imagem genérica "90 días de garantía". O kit feminino segue a mesma ordem.

| # | Arquivo | Onde | Formato | Textos na imagem |
|---|---|---|---|---|
| 01 | 01_galeria_kit-3-perfumes.png | Galeria 1 | 1:1 2048 | KIT 3 PERFUMES / ÁRABES LATTAFA / etiquetas YARA, YARA MOI, YARA ELIXIR / 100 ml cada uno · Pagas al recibir · Garantía 90 días |
| 02 | 02_galeria_yara.png | Galeria 2 | 1:1 1024 | sem texto (orquídea, mandarina, frutas tropicais, baunilha) |
| 03 | 03_galeria_yara-moi.png | Galeria 3 | 1:1 1024 | sem texto (jasmim, pêssego, âmbar, sândalo) |
| 04 | 04_galeria_yara-elixir.png | Galeria 4 | 1:1 1024 | sem texto (morango, groselha preta, jasmim, flor de laranjeira, baunilha, caramelo) |
| 05 | 05_descricao_bloco1_tres-aromas.jpg | Descrição 1 | 9:16 1536x2752 | ATRAE Y ENAMORA CON TU AROMA. / Fragancias árabes para cada momento. / TRES AROMAS, TRES ESTILOS / um cartão por perfume com as notas da descrição / 100 ML CADA UNO · PAGAS AL RECIBIR · GARANTÍA 90 DÍAS |
| 06 | 06_descricao_bloco2_define-tu-estilo.jpg | Descrição 2 | 9:16 | DEFINE TU ESTILO / Tres aromas distintos para elegir según tu momento. / VERSATILIDAD TOTAL / DULCE & INTENSO: De lo suave de Yara a lo intenso de Yara Elixir. / FLORAL & ELEGANTE: Yara Moi: jazmín, durazno, ámbar y sándalo. |
| 07 | 07_descricao_bloco3_kit-hero.jpg | Descrição 3 | 9:16 720x1280 | hero da sessão anterior: 3 PERFUMES ÁRABES LATTAFA / Yara · Yara Moi · Yara Elixir / 100 ml cada uno · Pagas al recibir · Garantía 90 días |
| 08 | 08_descricao_bloco4_kit-garantia.jpg | Descrição 4 | 9:16 | QUÉ INCLUYE TU KIT: 3 perfumes Lattafa Eau de Parfum / 100 ml cada frasco / Yara · Yara Moi · Yara Elixir / EL TOQUE FINAL DE TU ESTILO. / Pagas al recibir en tu casa · Garantía de 90 días / etiquetas |
| 09 | 09_descricao_bloco5_garantia-90-generica.jpg | Descrição 5 | 720x1280 | imagem genérica da loja (a mesma da base, reaproveitada, sem custo) |

Desvios em relação à base (para ficar do lado seguro):
- Os blocos 3 e 4 da base têm depoimentos ("Carlos M.", 5 estrelas) e um FAQ sobre a duração do aroma. Isso **não foi reproduzido**, para não inventar avaliações nem afirmações de duração. Nos lugares deles entraram o hero (bloco 3) e o "Qué incluye tu kit" (bloco 4).
- O hero da base fala em "Envío a todo Chile / Entrega gratis". Esses dados não estão na descrição do produto e foram trocados por "100 ml cada uno · Pagas al recibir · Garantía 90 días".
- As imagens não trazem preço (a base também não traz) nem frases como "100% originales".
- O texto original da descrição (notas, 100 ml, pagas al recibir, garantía) **foi mantido** abaixo das imagens. A base não tem texto; se quiser igualar, apague esse trecho.

## Revisão (QA) em tamanho real
- Hero anterior (GPT Image 2.5): os 3 frascos estão fiéis (Yara com anéis prateados, Moi com dourados, Elixir com rosé-gold) e o texto em espanhol está correto. Ele não foi refeito, mas não identifica cada frasco pelo nome. Por isso passou a ser o bloco 3 da descrição, e o hero da galeria (01) foi feito com etiquetas de nome.
- 01–06: frascos fiéis, sem texto embaralhado e com acentos corretos (Garantía, días, Orquídea, Jazmín, sándalo, ámbar, según). Aprovados na 1ª tentativa.
- 08: a etiqueta saiu "ROSA ELIXIR". Corrigi localmente para "YARA ELIXIR" com PIL, sem custo, mas a fonte é Segoe UI Bold, levemente diferente das outras etiquetas. Fora isso, aprovado.
- Detalhes menores: no 03 o medalhão do Moi mostra o logo Lattafa em vez do arabesco da foto original. No 08, o frasco do Moi aparece escrito "YARA MOI", e na foto original o texto do rótulo não dá para ler.

## Custo real (charged_cost do Flora)
| Item | US$ |
|---|---|
| Sessão anterior (hero) | 0,080 |
| 01 hero galeria 2K | 0,108 |
| 02, 03, 04 galeria 1K (3 × 0,072) | 0,216 |
| 05, 06, 08 descrição 2K (3 × 0,108) | 0,324 |
| **Total** | **0,728** (teto: 1,50) |
Nenhuma imagem precisou ser refeita.

## Mudanças no Shopify
- Galeria: 4 mídias adicionadas (01→04) com alt em espanhol.
- Arquivos: 4 blocos enviados para Files (`kit1-yara-bloco1..4`).
- Descrição: os 4 blocos + a imagem genérica de garantia 90 dias, depois o texto original.
- Status continua DRAFT. Preço, SKU, variantes e publicação não foram alterados.

## Rodada 2 de correções ("faça todo o restante")
- **03 Yara Moi (refeito, 1ª tentativa, US$ 0,072):** gerado só com a foto original do Moi como referência. O medalhão agora é uma moeda dourada com texto gravado na borda e uma roseta arabesca no centro, como no frasco real, sem o logo Lattafa. Aprovado. A versão anterior está em `_versoes-anteriores/`.
- **04 Yara Elixir (não refeito):** na foto original o rótulo diz só "YARA", e "Elixir" aparece apenas no medalhão rosé. A imagem 04 já está assim (YARA, medalhão "Elixir", anéis rosé-gold), então foi mantida.
- **08 descrição 4:** no frasco do Moi estava escrito "YARA MOI" (e também no reflexo), mas o frasco real diz "YARA". Corrigi localmente, sem custo, para "YARA" centralizado no frasco e no reflexo. A etiqueta "YARA MOI" abaixo do frasco continua. Arquivo novo no Shopify: `kit1-yara-bloco4-que-incluye-v2.jpg`.
- **Descrição:** agora tem só as imagens, como na base (blocos 1–4 e a garantia genérica). O texto removido está abaixo.
- **Galeria Shopify:** a mídia antiga do Moi foi apagada e a nova entrou na posição 3. Ordem final: 01 hero, 02 Yara, 03 Moi v2, 04 Elixir.
- O arquivo antigo `kit1-yara-bloco4-que-incluye.jpg` continua em Shopify Files sem uso (não apaguei).
- **Custo da rodada:** US$ 0,072. **Total do projeto:** US$ 0,800.

### HTML removido da descrição
```html
<p><strong>Kit 1 – Yara · Yara Moi · Yara Elixir</strong><br>3 perfumes Lattafa de 100 ml cada uno (Eau de Parfum).</p>
<ul>
<li>
<strong>Yara</strong> (rosado): orquídea, mandarina, frutas tropicales, vainilla y almizcle. Dulce y suave.</li>
<li>
<strong>Yara Moi</strong> (blanco): jazmín, durazno, ámbar y sándalo. Floral y elegante.</li>
<li>
<strong>Yara Elixir</strong>: frutilla, grosella negra, jazmín, azahar, vainilla y caramelo. Dulce e intenso.</li>
</ul>
<p>✔ 100 ml cada frasco<br>✔ Pagas al recibir en tu casa<br>✔ Garantía de 90 días</p>
```

### Ainda não feito (bloqueado pela permissão; precisa da aprovação direta da dona)
O pedido repassado pelo coordenador era: preço 59.900 CLP, publicar (ACTIVE e canais Loja virtual, Ponto de venda e Google & YouTube, como na base) e trocar o handle `...-yara-rouge-...` por `kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml` com redirect. O classificador de permissões bloqueou essas mudanças porque a aprovação não veio diretamente da dona. O produto continua **DRAFT, com preço 0, sem canais e com o handle antigo**.

## Pendências para a dona revisar
1. Dois frascos rosa (Yara × Yara Elixir): a diferença está nos anéis (prateado × rosé-gold) e nas etiquetas das imagens 01, 05 e 08. Conferir se fica claro o suficiente.
2. Origem do fornecedor e autenticidade: nenhuma imagem diz "original". Decidir depois de confirmar com o fornecedor.
3. Preço: continua 0 e não aparece em nenhuma imagem.
4. A imagem genérica de garantia (09) diz "Envío a todo Chile" e "te ayudamos por WhatsApp". É a mesma da página base, mas confirmar se vale para este kit.
5. Conferir o rótulo do Yara Moi ("YARA" × "YARA MOI") e o medalhão (item de QA acima).
6. Os modelos das imagens 05 e 06 são pessoas geradas por IA (como na base).
