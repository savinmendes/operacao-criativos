Você vai **auditar**, sem alterar nada, as campanhas da marca **Pellorini** que já foram criadas na conta do Meta Ads. Use as ferramentas do Meta Ads só para leitura e compare o que existe na conta com o plano abaixo, item por item. O plano inteiro está neste texto: não dependa de nenhum arquivo.

## Regras
- **Não crie, não edite, não ative e não pause nada.**
- Para cada item, marque ✅ (igual ao plano), ⚠️ (diferente mas aceitável, diga por quê) ou ❌ (errado ou faltando), com o valor esperado × o encontrado.
- O que não der para verificar pela API: marque "não verificável" e diga onde eu confiro no gerenciador.

## 1. Pré-requisitos
- Pixel da loja pellorini.com recebendo `Purchase` com valor nos últimos 7 dias
- Domínio pellorini.com verificado no Business Manager
- Página e Instagram dos anúncios = os da **Pellorini**
- Catálogo conectado, com um conjunto de produtos best-sellers (~45 produtos)
- Conta de anúncios sem restrição e com pagamento ativo

## 2. Campanha 1: `PELLORINI | Vendas | BOGO | EN | ABO`
- Objetivo Vendas; orçamento por **conjunto** (ABO); status **PAUSADA**
- Cada um dos 5 conjuntos: US$ 20/dia · compra no site com o pixel · maior volume, **sem** limite de custo · 7 dias após o clique ou 1 dia após a visualização · países **US, GB, CA, AU** (nenhum outro) · 18–65+, todos os gêneros · Advantage+ sem interesses · posicionamentos Advantage+ · pausado

Em todos os anúncios: CTA **SHOP_NOW** · parâmetros de URL = `utm_source=facebook&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_term={{adset.name}}&utm_content={{ad.name}}` · melhorias de **texto** do Advantage+ Creative desligadas · Página Pellorini.

Formatos:
- **flexível**: todas as imagens listadas (1:1 e 9:16), todas as variações de texto, título e descrição do conceito; link = coleção.
- **carrossel**: os cards **na ordem**, cada um com a imagem, o título, a descrição e o **link da página do relógio** indicados; texto principal = o texto 1 do conceito; card final "ver mais" = coleção. ❌ se algum card apontar para a coleção ou para o relógio errado.

### Conjunto `CJ1 | Masculino | Oferta`

- `A01 | C1_P2_bogo-saturado` · **flexível** · conceito `oferta` · link https://pellorini.com/collections/best-sellers · 8 imagens: A01__C1_P2_bogo-saturado_Vittorio-Milano_1x1.jpg, A01__C1_P2_bogo-saturado_Vittorio-Milano_9x16.jpg, A01__C1_P2_bogo-saturado_Dominante-Opulent_1x1.jpg, A01__C1_P2_bogo-saturado_Dominante-Opulent_9x16.jpg, A01__C1_P2_bogo-saturado_Milano-Maretti_1x1.jpg, A01__C1_P2_bogo-saturado_Milano-Maretti_9x16.jpg, A01__C1_P2_bogo-saturado_Maretti-Dominante_1x1.jpg, A01__C1_P2_bogo-saturado_Maretti-Dominante_9x16.jpg
- `A02 | C2_P1_vs-designer` · **carrossel** · conceito `preco` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A02__C2_P1_vs-designer_Vittorio_1x1.jpg` · título `Pellorini Vittorio` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/vittorio
  - card 2: `A02__C2_P1_vs-designer_Dominante_1x1.jpg` · título `Pellorini Dominante` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-dominante
  - card 3: `A02__C2_P1_vs-designer_Milano_1x1.jpg` · título `Pellorini Milano` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-milano
  - card 4: `A02__C2_P1_vs-designer_Opulent_1x1.jpg` · título `Pellorini Opulent` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-opulent
  - card 5: `A02__C2_P1_vs-designer_Maretti_1x1.jpg` · título `Pellorini Maretti` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-maretti
- `A03 | C2_P1_is-name-worth` · **carrossel** · conceito `preco` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A03__C2_P1_is-name-worth_Vittorio_1x1.jpg` · título `Pellorini Vittorio` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/vittorio
  - card 2: `A03__C2_P1_is-name-worth_Dominante_1x1.jpg` · título `Pellorini Dominante` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-dominante
  - card 3: `A03__C2_P1_is-name-worth_Milano_1x1.jpg` · título `Pellorini Milano` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-milano
  - card 4: `A03__C2_P1_is-name-worth_Opulent_1x1.jpg` · título `Pellorini Opulent` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-opulent
  - card 5: `A03__C2_P1_is-name-worth_Maretti_1x1.jpg` · título `Pellorini Maretti` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-maretti
- `A04 | C8_P2_postit` · **carrossel** · conceito `oferta` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A04__C8_P2_postit-produto_Vittorio_1x1.jpg` · título `Pellorini Vittorio` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/vittorio
  - card 2: `A04__C8_P2_postit-produto_Dominante_1x1.jpg` · título `Pellorini Dominante` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-dominante
  - card 3: `A04__C8_P2_postit-produto_Milano_1x1.jpg` · título `Pellorini Milano` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-milano
  - card 4: `A04__C8_P2_postit-produto_Opulent_1x1.jpg` · título `Pellorini Opulent` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-opulent
  - card 5: `A04__C8_P2_postit-produto_Maretti_1x1.jpg` · título `Pellorini Maretti` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-maretti
  - card 6: `A04__C8_P2_postit_pellorini-milano_5_1x1.jpg` · título `Pellorini Milano` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-milano

### Conjunto `CJ2 | Masculino | Desejo`

- `A05 | C7_P1_poster` · **carrossel** · conceito `desejo_h` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A05__C7_P1_poster_Vittorio_1x1.jpg` · título `Pellorini Vittorio` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/vittorio
  - card 2: `A05__C7_P1_poster_Dominante_1x1.jpg` · título `Pellorini Dominante` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-dominante
  - card 3: `A05__C7_P1_poster_Milano_1x1.jpg` · título `Pellorini Milano` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-milano
  - card 4: `A05__C7_P1_poster_Opulent_1x1.jpg` · título `Pellorini Opulent` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-opulent
  - card 5: `A05__C7_P1_poster_Maretti_1x1.jpg` · título `Pellorini Maretti` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-maretti
- `A06 | C2_P1_pulso-frase` · **carrossel** · conceito `desejo_h` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A06__C2_P1_pulso-frase_vittorio_5_1x1.jpg` · título `Pellorini Vittorio` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/vittorio
  - card 2: `A06__C2_P1_pulso-frase_pellorini-milano_5_1x1.jpg` · título `Pellorini Milano` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-milano
  - card 3: `A06__C1_P2_vida-bogo_vittorio_5_1x1.jpg` · título `Pellorini Vittorio` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/vittorio
  - card 4: `A06__C1_P2_vida-bogo_pellorini-milano_5_1x1.jpg` · título `Pellorini Milano` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-milano
- `A07 | C7_P1_split` · **carrossel** · conceito `desejo_h` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A07__C7_P1_split_vittorio_5_1x1.jpg` · título `Pellorini Vittorio` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/vittorio
  - card 2: `A07__C7_P1_split_pellorini-milano_5_1x1.jpg` · título `Pellorini Milano` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-milano
- `A08 | C7_P1_caixa-maos` · **carrossel** · conceito `desejo_h` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A08__C7_P1_caixa-maos_vittorio_2_1x1.jpg` · título `Pellorini Vittorio` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/vittorio
  - card 2: `A08__C7_P1_caixa-maos_pellorini-dominante_2_1x1.jpg` · título `Pellorini Dominante` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-dominante
  - card 3: `A08__C7_P1_caixa-maos_pellorini-milano_2_1x1.jpg` · título `Pellorini Milano` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-milano
  - card 4: `A08__C7_P1_caixa-maos_pellorini-opulent_2_1x1.jpg` · título `Pellorini Opulent` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-opulent
  - card 5: `A08__C7_P1_caixa-maos_pellorini-maretti_2_1x1.jpg` · título `Pellorini Maretti` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-maretti

### Conjunto `CJ3 | Presente`

- `A09 | C1_P2_imessage` · **flexível** · conceito `presente` · link https://pellorini.com/collections/best-sellers · 4 imagens: A09__C1_P2_imessage_pai-dominante_1x1.jpg, A09__C1_P2_imessage_pai-dominante_9x16.jpg, A09__C1_P2_imessage_irmao-milano_1x1.jpg, A09__C1_P2_imessage_irmao-milano_9x16.jpg
- `A10 | C1_P2_his-hers` · **flexível** · conceito `presente` · link https://pellorini.com/collections/best-sellers · 6 imagens: A10__C1_P2_his-hers_vittorio-clovera_1x1.jpg, A10__C1_P2_his-hers_vittorio-clovera_9x16.jpg, A10__C1_P2_his-hers_milano-serafina_1x1.jpg, A10__C1_P2_his-hers_milano-serafina_9x16.jpg, A10__C1_P2_his-hers_opulent-lunetta_1x1.jpg, A10__C1_P2_his-hers_opulent-lunetta_9x16.jpg
- `A11 | C8_P2_maleta` · **flexível** · conceito `oferta` · link https://pellorini.com/collections/best-sellers · 4 imagens: A11__C8_P2_maleta_bestsellers_1x1.jpg, A11__C8_P2_maleta_bestsellers_9x16.jpg, A11__C8_P5_maleta_mulher_1x1.jpg, A11__C8_P5_maleta_mulher_9x16.jpg
- `A12 | C7_P1_qual-voce` · **flexível** · conceito `escolha` · link https://pellorini.com/collections/best-sellers · 8 imagens: A12__C7_P1_qual-voce_classic-bold_1x1.jpg, A12__C7_P1_qual-voce_classic-bold_9x16.jpg, A12__C7_P1_qual-voce_green-blue_1x1.jpg, A12__C7_P1_qual-voce_green-blue_9x16.jpg, A12__C7_P1_qual-voce_chrono-clean_1x1.jpg, A12__C7_P1_qual-voce_chrono-clean_9x16.jpg, A12__C7_P1_qual-voce_grey-green_1x1.jpg, A12__C7_P1_qual-voce_grey-green_9x16.jpg

### Conjunto `CJ4 | Feminino`

- `A13 | C7_P5_poster` · **carrossel** · conceito `desejo_m` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A13__C7_P5_poster_Clovera_1x1.jpg` · título `Pellorini Clovera` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-clovera
  - card 2: `A13__C7_P5_poster_Serafina_1x1.jpg` · título `Pellorini Serafina` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-serafina
  - card 3: `A13__C7_P5_poster_Lunetta_1x1.jpg` · título `Pellorini Lunetta` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-lunetta
  - card 4: `A13__C7_P5_poster_Fiorella_1x1.jpg` · título `Pellorini Fiorella` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-fiorella
  - card 5: `A13__C7_P5_poster_Grazia_1x1.jpg` · título `Pellorini Grazia` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-grazia
- `A14 | C7_P5_pulso-frase` · **carrossel** · conceito `desejo_m` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A14__C7_P5_pulso-frase_pellorini-clovera_3_1x1.jpg` · título `Pellorini Clovera` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-clovera
  - card 2: `A14__C7_P5_pulso-frase_pellorini-aria_4_1x1.jpg` · título `Pellorini Aria` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-aria
  - card 3: `A14__C7_P5_pulso-frase_pellorini-bellissima_6_1x1.jpg` · título `Pellorini Bellissima` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-bellissima
  - card 4: `A14__C7_P5_pulso-frase_pellorini-carina_4_1x1.jpg` · título `Pellorini Carina` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-carina
- `A15 | C7_P5_split` · **carrossel** · conceito `desejo_m` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A15__C7_P5_split_pellorini-clovera_4_1x1.jpg` · título `Pellorini Clovera` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-clovera
  - card 2: `A15__C7_P5_split_pellorini-aria_3_1x1.jpg` · título `Pellorini Aria` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-aria
  - card 3: `A15__C7_P5_split_pellorini-bellissima_3_1x1.jpg` · título `Pellorini Bellissima` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-bellissima
  - card 4: `A15__C7_P5_split_pellorini-carina_6_1x1.jpg` · título `Pellorini Carina` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-carina
- `A16 | C1_P5_vida-bogo` · **carrossel** · conceito `oferta` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A16__C1_P2_vida-bogo_pellorini-aria_4_1x1.jpg` · título `Pellorini Aria` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-aria
  - card 2: `A16__C1_P2_vida-bogo_pellorini-clovera_3_1x1.jpg` · título `Pellorini Clovera` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-clovera
  - card 3: `A16__C1_P2_vida-bogo_pellorini-carina_3_1x1.jpg` · título `Pellorini Carina` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-carina
  - card 4: `A16__C1_P2_vida-bogo_pellorini-bellissima_4_1x1.jpg` · título `Pellorini Bellissima` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-bellissima

### Conjunto `CJ5 | Confiança`

- `A17 | C4_P3_garantia-90d` · **carrossel** · conceito `risco` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A17__C4_P3_garantia-90d_Vittorio_1x1.jpg` · título `Pellorini Vittorio` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/vittorio
  - card 2: `A17__C4_P3_garantia-90d_Dominante_1x1.jpg` · título `Pellorini Dominante` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-dominante
  - card 3: `A17__C4_P3_garantia-90d_Milano_1x1.jpg` · título `Pellorini Milano` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-milano
  - card 4: `A17__C4_P3_garantia-90d_Opulent_1x1.jpg` · título `Pellorini Opulent` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-opulent
  - card 5: `A17__C4_P3_garantia-90d_Maretti_1x1.jpg` · título `Pellorini Maretti` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-maretti
- `A18 | C3_P3_generico-x-nos` · **carrossel** · conceito `qualidade` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A18__C3_P3_generico-x-nos_Vittorio_1x1.jpg` · título `Pellorini Vittorio` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/vittorio
  - card 2: `A18__C3_P3_generico-x-nos_Dominante_1x1.jpg` · título `Pellorini Dominante` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-dominante
  - card 3: `A18__C3_P3_generico-x-nos_Milano_1x1.jpg` · título `Pellorini Milano` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-milano
  - card 4: `A18__C3_P3_generico-x-nos_Opulent_1x1.jpg` · título `Pellorini Opulent` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-opulent
  - card 5: `A18__C3_P3_generico-x-nos_Maretti_1x1.jpg` · título `Pellorini Maretti` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-maretti
- `A19 | C2_P1_tweet` · **carrossel** · conceito `preco` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A19__C2_P1_tweet_Vittorio_1x1.jpg` · título `Pellorini Vittorio` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/vittorio
  - card 2: `A19__C2_P1_tweet_Dominante_1x1.jpg` · título `Pellorini Dominante` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-dominante
  - card 3: `A19__C2_P1_tweet_Milano_1x1.jpg` · título `Pellorini Milano` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-milano
  - card 4: `A19__C2_P1_tweet_Opulent_1x1.jpg` · título `Pellorini Opulent` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-opulent
  - card 5: `A19__C2_P1_tweet_Maretti_1x1.jpg` · título `Pellorini Maretti` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-maretti
- `A20 | C2_P1_ancora-10k` · **carrossel** · conceito `preco` · ver mais: https://pellorini.com/collections/best-sellers
  - card 1: `A20__C2_P1_ancora-10k_Vittorio_1x1.jpg` · título `Pellorini Vittorio` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/vittorio
  - card 2: `A20__C2_P1_ancora-10k_Dominante_1x1.jpg` · título `Pellorini Dominante` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-dominante
  - card 3: `A20__C2_P1_ancora-10k_Milano_1x1.jpg` · título `Pellorini Milano` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-milano
  - card 4: `A20__C2_P1_ancora-10k_Opulent_1x1.jpg` · título `Pellorini Opulent` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-opulent
  - card 5: `A20__C2_P1_ancora-10k_Maretti_1x1.jpg` · título `Pellorini Maretti` · descrição `Buy 1 Get 1 Free` · link https://pellorini.com/products/pellorini-maretti

## 3. Campanha 2: `PELLORINI | Catálogo | BOGO | EN`
- Anúncio de catálogo (Advantage+ catalog), US$ 50/dia, pausada
- 1 conjunto (`CJ6 | Catálogo | Best Sellers`), com o mesmo público, países, otimização e atribuição
- Anúncio `A21 | C9_catalogo-bogo`: conjunto best-sellers, textos do conceito `oferta`, SHOP_NOW, moldura `A21__moldura-catalogo-bogo.png` (⚠️ se a conta não permitir)

## 4. Textos esperados (palavra por palavra, com emojis e quebras de linha)
No formato flexível, cada anúncio leva todas as variações do seu conceito. No carrossel, só o texto principal 1.

### Conceito `oferta`: Oferta (BOGO)

Texto principal 1:
```
One for you. One for them. 🎁
Buy any Pellorini watch and the second one is on us.
✔ 316L stainless steel
✔ 2-year warranty
✔ 90-day money-back guarantee
✔ Free tracked worldwide shipping
```
Texto principal 2:
```
BUY 1, GET 1 FREE ⌚⌚
Pick any two Pellorini watches. You only pay for one.
No code needed: the discount is applied in your cart.
```
Texto principal 3:
```
Why buy one watch when the second is free?
Choose your two favorites from our best sellers and pay for just one.
Free tracked worldwide shipping and 90 days to return.
```
Títulos: `Buy 1 Get 1 Free` | `Pick Any Two Watches` | `Second Watch Free`  
Descrições: `Free worldwide shipping` | `No code needed`

### Conceito `preco`: Preço / status

Texto principal 1:
```
The look people notice. The price nobody guesses. ⌚
Pellorini watches are made with 316L stainless steel and a scratch-resistant face, without the luxury markup.
Right now, the second watch is free.
```
Texto principal 2:
```
Most of what you pay for a designer watch is the name on the dial.
We skip the logo tax: 316L steel, sapphire crystal and a 2-year warranty.
Buy 1, get 1 free.
```
Texto principal 3:
```
Unpopular opinion: you don't need to spend $5,000 to look like you did.
Shop the Pellorini best sellers. Second watch free.
```
Títulos: `The $10K Look, Without the Price Tag` | `Skip the Logo Tax` | `Buy 1 Get 1 Free`  
Descrições: `Buy 1 Get 1 Free` | `Free worldwide shipping`

### Conceito `qualidade`: Qualidade

Texto principal 1:
```
Most cheap watches tarnish, scratch and end up in a drawer.
Pellorini is different:
✔ 316L stainless steel that doesn't tarnish
✔ Sapphire crystal
✔ Adjustable bracelet with sizing tool
✔ 2-year warranty and 90 days to return
```
Texto principal 2:
```
Built to be worn every day, not saved for special occasions.
316L steel, sapphire crystal and a 2-year warranty on every watch.
Buy 1, get 1 free.
```
Títulos: `Built to Last. Priced to Make Sense.` | `Made to Be Worn Every Day`  
Descrições: `2-year warranty` | `Buy 1 Get 1 Free`

### Conceito `risco`: Risco zero (90 dias)

Texto principal 1:
```
Wear it for 90 days.
If you don't love it, send it back for a full refund. No questions asked.
Every Pellorini also comes with a 2-year warranty and free tracked worldwide shipping.
```
Texto principal 2:
```
Buying a watch online feels like a risk. So we removed it.
90-day money-back guarantee + 2-year warranty.
And today, the second watch is free.
```
Títulos: `90-Day Money-Back Guarantee` | `Love It or Return It`  
Descrições: `Buy 1 Get 1 Free` | `2-year warranty`

### Conceito `desejo_h`: Desejo – masculino

Texto principal 1:
```
Meet our best sellers. ⌚
Sunray dials, 316L stainless steel and a bracelet that fits any wrist.
Pick any two, the second one is free.
```
Texto principal 2:
```
Dressed up or down, it just works.
Discover the Pellorini best sellers with free tracked worldwide shipping.
```
Texto principal 3:
```
The watch people ask about.
Shop Pellorini: buy 1 and get 1 free.
```
Títulos: `Meet the Pellorini Best Sellers` | `Your New Everyday Watch` | `Buy 1 Get 1 Free`  
Descrições: `Buy 1 Get 1 Free` | `Free worldwide shipping`

### Conceito `desejo_m`: Desejo – feminino

Texto principal 1:
```
Small details. Big difference. ✨
Delicate gold-tone watches made for every day.
Pick any two, the second one is free.
```
Texto principal 2:
```
The everyday piece she'll never take off.
Free tracked worldwide shipping and 90 days to return.
```
Texto principal 3:
```
Quiet luxury, every day.
Shop our women's best sellers: buy 1, get 1 free.
```
Títulos: `Everyday Elegance` | `Buy 1 Get 1 Free` | `The Gift She'll Wear Every Day`  
Descrições: `Free worldwide shipping` | `Buy 1 Get 1 Free`

### Conceito `presente`: Presente

Texto principal 1:
```
The gift that comes in pairs. 🎁
Buy a Pellorini for them and the second one is free. Keep it or gift it.
Free tracked worldwide shipping.
```
Texto principal 2:
```
Anniversary, birthday or just because.
Buy 1 Pellorini watch, get 1 free: one for you, one for them.
```
Títulos: `One for You. One for Them.` | `Buy 1 Get 1 Free`  
Descrições: `Free worldwide shipping` | `90-day returns`

### Conceito `escolha`: Escolha (qual você?)

Texto principal 1:
```
Classic or iced? Silver or gold?
You don't have to choose: buy 1 Pellorini, get the second one free.
```
Texto principal 2:
```
Which one are you?
Pick your two favorites from our best sellers and pay for just one.
```
Títulos: `Can't Choose? Get Both.` | `Buy 1 Get 1 Free`  
Descrições: `Free worldwide shipping` | `No code needed`

## 5. Totais
- 2 campanhas, 6 conjuntos, 21 anúncios (15 carrosséis + 5 flexíveis + 1 catálogo), US$ 150/dia no total
- Nenhum item duplicado ou extra com "PELLORINI" no nome

## 6. Abra 3 links (1 coleção + 2 páginas de produto)
- Abrem sem erro em pellorini.com
- Mostram **Pellorini** (não Pelvini), "Buy 1 Get 1 Free", **90 dias** (nenhum "30-Day") e entrega **worldwide** (sem "UK delivery")
- Se ainda aparecer UK, 30 dias ou Pelvini, o tema Pellorini não foi publicado: marque ❌ e diga isso

## Formato da resposta
1. Pré-requisitos
2. Campanhas e conjuntos: esperado × encontrado
3. Por anúncio: formato, imagens/cards (os que faltam ou estão errados), textos, links, parâmetros de URL, CTA
4. Resumo ✅/⚠️/❌ e as correções em ordem de prioridade. **Não aplique nenhuma correção**: espere eu pedir.