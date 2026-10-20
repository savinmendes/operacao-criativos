# Mapa produto Shopify → fornecedor Dropi (chileverificada.com)

Gerado em 09/10/2026. Fonte: conector Chegou Operações (operação `drop`).

## Como o mapa foi feito
- Juntei as vendas da loja **Chile** (`vendas_shopify_vendashopify` + `vendas_shopify_itemvendashopify`, desde 06/08/2026) com os pedidos da Dropi Chile (`metricas_dropi_dropipedido`, `pais='chile'`, sem pedidos sumidos).
  - A ligação é `dados->>'shop_order_id'` = `shopify_order_id`.
- Para não misturar produtos, só entraram as vendas com **1 produto Shopify** e os pedidos Dropi com **1 item** (`orderdetails[0]`).
  - Desses, li `product.user_id` (fornecedor), `product.id` e `product.name`.
- **Regra para etiquetar:** pelo menos 3 pedidos e pelo menos 90% deles no mesmo fornecedor, contando todo o histórico.
  - Também conferi os últimos 14 dias (desde 25/09), porque vários produtos já trocaram de fornecedor.
  - Nenhum produto que passou na regra tem os últimos 14 dias apontando para outro fornecedor.
- **Etiquetas:** cada produto válido recebeu `forn-<user_id>` + `dropi-<id do produto Dropi>`, via `tagsAdd`.
  - Foram **35 produtos**, todos sem erro.
  - Etiquetas que já existiam não foram mexidas.
- Dados de cliente não foram lidos nem copiados. Só usei contagens.

## Efeito no tema (carrinho cv)
- Todo produto com `forn-` passa a mostrar **"Agregar al carrito"** nos cards da coleção.
- Ele também entra no "Completa tu pedido" dos produtos com a mesma etiqueta.
- A trava de fornecedor passa a valer para ele. Um carrinho só aceita um `forn-`; produto sem etiqueta não entra junto.
- Para desfazer em um produto, use `tagsRemove` com as 2 etiquetas dele.

---

## Grupos por fornecedor: o que pode ir no mesmo pedido

Formato da coluna "Evidência": pedidos do fornecedor / pedidos casados no histórico (% · últimos 14 dias).

### 82275: perfumes árabes + trípode (+ câmera foco e taladro na Dropi, ainda sem página só dele)
| Produto Shopify (handle) | Fornecedor | Produto Dropi | Evidência | Etiqueta |
|---|---|---|---|---|
| TRÍPODE SOPORTE EXTENSIBLE ORIGINAL con Control Bluetooth (`tripode`) | 82275 | 35799 TRIPODE SOPORTE EXTENSIBLE ORIGINAL | 363/363 (100% · 0 em 14d, último 16/09) | ADICIONADA `forn-82275`, `dropi-35799` |
| Pack 3x1 Perfumes Hombre Armaf + Lattafa Asad + Afnan 9PM (`lattafa`) | 82275 | 177689 PACK DE 3 PERFUMES ÁRABES hombre (94) e 152575 Pack3 perfume AQUA BOURRON NOIR (36) | 130/130 (100% · 130 em 14d) | `forn-82275` já existia. ADICIONADA `dropi-177689` (o principal e o mais recente) |
| Pack 3x1 Perfumes Árabes Mujer Yara + Fakhar Rose + Sabah Al Ward (`yara`) | 82275 | 173562 Pack3 perfume PINK WHITE CANDY | 15/15 (100% · 15 em 14d) | `forn-82275` já existia. ADICIONADA `dropi-173562` |
| 13 Lattafa novos: 5 kits Mujer + 8 unitários (Yara, Yara Moi, Yara Tous, Yara Candy, Yara Elixir, Asad, Asad Bourbon, Asad Zanzibar) | 82275 (**a confirmar**) | sem pedido | 0 vendas | `forn-82275` mantida (suposição). Sem `dropi-` |

- O 82275 também vende na Dropi a **CAMARA FOCO DE SEGURIDAD HD PANORAMICA (32589)** e o **KIT TALADRO INALAMBRICO 28V (33828)**.
- Mas as páginas Shopify desses produtos não passaram na regra:
  - As câmeras são enviadas na maioria por outros fornecedores (ver "Ambíguos").
  - O taladro `dewalt` só tem 2 pedidos.
- Para eles entrarem no grupo 82275, a página precisa ficar fixa no 82275 na Dropi. Depois é só adicionar `forn-82275`.

### 2924
| Produto Shopify (handle) | Fornecedor | Produto Dropi | Evidência | Etiqueta |
|---|---|---|---|---|
| Shark PowerPro Aspiradora 2 en 1 (`asp`) | 2924 | 99909 M - ASPIRADORA 2 EN 1 BLANCA HOME | 378/378 (100% · 37) | ADICIONADA `forn-2924`, `dropi-99909` |
| Shark PowerPro Aspiradora 2 en 1 (`asp-ttk`) | 2924 | 99909 | 6/6 (100% · 6) | ADICIONADA |
| EUREKA Aspiradora 2 en 1 Blanca (`asp-new400`) | 2924 | 99909 | 4/4 (100% · 0) | ADICIONADA |
| DREAME Aspiradora 2 en 1 Blanca (`dreame`) | 2924 | 99909 | 214/214 (100% · 37) | ADICIONADA |
| BISSELL Aspiradora 2 en 1 (`asp-bissel`) | 2924 | 99909 | 260/278 (93,5% · 85/90; o resto é 1098) | ADICIONADA |
| Aspiradora 2 en 1 Blanca (`trucozie`) | 2924 | 99909 | 11/11 (100% · 0) | ADICIONADA |
| BISSELL Aspiradora 2 en 1 (`bissel-ttk`) | 2924 | 99909 | 123/123 (100% · 123) | ADICIONADA |
| Sostén Sin Aros que Levanta y Moldea (`sosten`) | 2924 | 112435 SÑ - Sósten premium sin Aros | 34/34 (100% · 0) | ADICIONADA `forn-2924`, `dropi-112435` |
| Sostén Premium Sin Aros 1, 2 o 3 (`sosten-ttk2`) | 2924 | 112435 | 126/126 (100% · 17) | ADICIONADA |
| Calza Push Up Moldeadora (`calza123`) | 2924 | 21440 Premium Leggings Efecto piel Pack 2X | 46/46 (100% · 0) | ADICIONADA `forn-2924`, `dropi-21440` |
| Calza Push Up Moldeadora (`calza-ttk`) | 2924 | 21440 | 56/56 (100% · 38) | ADICIONADA |

### 99722
| Produto Shopify (handle) | Fornecedor | Produto Dropi | Evidência | Etiqueta |
|---|---|---|---|---|
| Cámara de Seguridad Panoramica 360° (`cam360-ttk`) | 99722 | 37258 Camara Foco De Seguridad Hd Panoramica | 111/111 (100% · 111) | ADICIONADA `forn-99722`, `dropi-37258` |
| PROMOCIÓN 2x1 Calza Premium Tiro Alto (`calza2x1`) | 99722 | 57649 Leggings gruesos pack 2 | 36/37 (97% · 0) | ADICIONADA `forn-99722`, `dropi-57649` |
| PROMOCIÓN 2x1 Calza Premium Tiro Alto (`calza2x1-ttk`) | 99722 | 57649 | 24/24 (100% · 24) | ADICIONADA |

### 27887
| Produto Shopify (handle) | Fornecedor | Produto Dropi | Evidência | Etiqueta |
|---|---|---|---|---|
| Podadora Inalambrica Cesped Ruedas (`desbrozadora`) | 27887 | 97825 Podadora Inalámbrica Césped + Ruedas | 330/330 (100% · 142) | ADICIONADA `forn-27887`, `dropi-97825` |
| Podadora Inalámbrica para Césped con Ruedas (`desbrozadora-ttk`) | 27887 | 97825 | 240/240 (100% · 197) | ADICIONADA |
| Podadora Black Inalambrica (`podablack`) | 27887 | 97825 | 6/6 (100% · 6) | ADICIONADA |

### 18419: perfumes de grife
| Produto Shopify (handle) | Fornecedor | Produto Dropi | Evidência | Etiqueta |
|---|---|---|---|---|
| KIT DE 3 PERFUMES Invictus + 1 Million + Bleu (`invictus`) | 18419 | 40800 KIT DE 3 PERFUMES PREMIUM DE 100ml | 243/265 (91,7% · 183/196; o resto é 82275 "AQUA BOURRON NOIR") | ADICIONADA `forn-18419`, `dropi-40800` |
| Kit 3 Perfumes Premium para Hombre (`kithombre-ttk`) | 18419 | 40800 | 14/14 (100% · 14) | ADICIONADA |

### 8457: fajas
| Produto Shopify (handle) | Fornecedor | Produto Dropi | Evidência | Etiqueta |
|---|---|---|---|---|
| PROMOCIÓN 2x1 FAJA BODY ENTERO (`easyslide`) | 8457 | 24486 FAJA BODY ENTERO | 279/302 (92,4% · 0; o resto é 28960) | ADICIONADA `forn-8457`, `dropi-24486` |
| PROMOCIÓN 2x1 FAJA BODY ENTERO (`faja-easyslide-ttk`) | 8457 | 24486 | 30/30 (100% · 0) | ADICIONADA |
| PAGA 1 Y RECIBE 3 Faja sin Costuras (`fajaseamless`) | 8457 | 46872 WAS Faja Body Moldeador Cintura | 22/22 (100% · 0) | ADICIONADA `forn-8457`, `dropi-46872` |

### 1152
| Produto Shopify (handle) | Fornecedor | Produto Dropi | Evidência | Etiqueta |
|---|---|---|---|---|
| SmartWatch T500 (`gla2`) | 1152 | 3357 Reloj Smartwatch T500 ULTRA | 22/22 (100% · 0) | ADICIONADA `forn-1152`, `dropi-3357` |
| FAJA REDUCTORA COMPLETA (`faja`) | 1152 | 55224 FAJA REDUCTORA COMPLETA | 224/224 (100% · 0) | ADICIONADA `forn-1152`, `dropi-55224` |

### 11394
| Produto Shopify (handle) | Fornecedor | Produto Dropi | Evidência | Etiqueta |
|---|---|---|---|---|
| Mopa Limpiador Rociador Trapeador (`mopa`) | 11394 | 6555 Mopa Limpiador Rociador Trapeador | 107/107 (100% · 0) | ADICIONADA `forn-11394`, `dropi-6555` |
| Mopa Limpiador Rociador Trapeador (`mopa-ttk`) | 11394 | 6555 | 5/5 (100% · 0) | ADICIONADA |

### 233027: suplementos
| Produto Shopify (handle) | Fornecedor | Produto Dropi | Evidência | Etiqueta |
|---|---|---|---|---|
| Resveratrol 1800mg (`resveratrol`) | 233027 | 60078 RESVERATROL 60 CAP | 27/27 (100% · 0) | ADICIONADA `forn-233027`, `dropi-60078` |
| Visionyx Fórmula para la Vista (`vs`) | 233027 | 59461 VISIONYX VITAMINAS PARA TUS OJOS | 19/19 (100% · 19) | ADICIONADA `forn-233027`, `dropi-59461` |

### Fornecedores com 1 produto só (não formam grupo de upsell hoje)
| Produto Shopify (handle) | Fornecedor | Produto Dropi | Evidência | Etiqueta |
|---|---|---|---|---|
| Shark SilkiPro 3 en 1 (`silkipro`) | 4175 | 51133 Plancha Térmica Para Cabello | 23/23 (100% · 0) | ADICIONADA `forn-4175`, `dropi-51133` |
| OFERTA 2X1 Creatina + Colágeno + BCAA (`creawomen`) | 69545 | 54559 2 x Old School Labs Creatina | 5/5 (100% · 0) | ADICIONADA `forn-69545`, `dropi-54559` |
| Pack 2x1 Perfumes Hombre One Million + Sauvage (`sauvage`) | 22718 | 13076 Perfumes | 7/7 (100% · 7) | ADICIONADA `forn-22718`, `dropi-13076` |
| Gotas Lymphoria (`lymphoria`) | 368717 | 159173 LYMPHORIA DRENAJE LINFATICO X 60 ML | 26/26 (100% · 26) | ADICIONADA `forn-368717`, `dropi-159173` |

---

## Ambíguos: NÃO etiquetados (mais de um fornecedor)
Precisam de revisão manual: definir na Dropi um fornecedor fixo por página.

| Produto Shopify (handle) | Fornecedores nos pedidos (histórico) | Últimos 14 dias |
|---|---|---|
| Cámara de Seguridad Panorámica 4G (`cam4g`) | 2924/171647: 591 · 99722/37258: 452 · 1152/12875: 276 · 82275/32589: 4 | 2924: 220 · 99722: 246 · 82275: 4 |
| Cámara de Seguridad Panoramica 360° (`cam-360`) | 99722: 41 · 1152: 23 · 2924: 15 · 82275: 10 (46%) | 99722: 21/21. Provavelmente o atual é o 99722. Confirmar e etiquetar `forn-99722` |
| Cámara de Seguridad Panorámica AOC (`cam-aoc`) | 2924: 310 · 99722: 224 · 1152: 46 · 82275: 2 | 2924: 158 · 99722: 164 · 82275: 2 |
| Cámara de Seguridad Panorámica 24/7 (`cam-2k`) | 2924: 248 · 99722: 120 · 1152: 71 | 2924: 51 · 99722: 33 |
| Cámara de Seguridad Panorámica 4G (`cam-ttk`) | 2924: 577 · 99722: 263 · 82275: 14 | 2924: 563 · 99722: 230 · 82275: 14 |
| Cámara de Seguridad Panorámica AOC (`aoc-ttk`) | 2924: 166 · 99722: 150 | igual |
| TRÍPODE con Control Bluetooth (`tripode-ttk3`) | 82275/35799: 139 · 1152/9828: 23 (85,8%) | 82275: 9 · 1152: 7 |
| Mopa a Vapor SharkPower (`mopa-shark`) | 11394/6555: 145 · 1152/18694: 42 (77,5%) | 11394: 84 · 1152: 42 |
| Calza Push Up Tiro Alto (`calza-deportiva-ttk`) | 99722/57649: 58 · 2924/21440: 10 (85%) | sem pedidos |

## Evidência insuficiente: NÃO etiquetados (menos de 3 pedidos)
| Produto Shopify (handle) | O que apareceu |
|---|---|
| Taladro Inalámbrico DeWalt (`dewalt`; nas vendas aparece como `tla-ttk`) | 82275/33828 KIT TALADRO 28V: 2 pedidos. É o fornecedor esperado, mas falta volume. Se a dona confirmar, adicionar `forn-82275` |
| Escurridor de Cocina 2 Niveles (`escurridor`) | 11394/34602: 2 |
| Hidrolavadora Inalámbrica (`hidrolavadora`) | 3199/34577: 2 |
| NeoCell Multi-Colageno (`neocell`) | 52743/84659: 1 |
| Mop Giratorio 360° (`mop-giratorio`) | 1098/34794: 1 |

## Ativos sem pedido casado desde 06/08 (sem etiqueta)
- Lista: `tla-ttk2`, `duc-ttk`, `box-ttk`, `lv-ttk`, `mc-ttk2`, `hidro-ttk`, `hd-ttk`, `cortadora-de-pasto-recortadora-de-malaza`, `guadanadora-ttk`, `proy-ttk2`, `tel`, `fj-ttk`, `fj-ttk-2`, `faja-bf`, `faja-body-short2`, `mg`, `mg1`, `mag-vsl`, `magnesio-ttk`, `sw-ttk`, `cepillo`, `wavytalk-…-ttk`, `rizador`, `calza`, `calza2`, `calzalan`, `fk-calza`, `sosten-ttk`, `sosten2x1`, `sosten3x1`, `sosten-up`, `body`, `body2`, `cinta`, `cinturilla`, `cinturilla-ttk`, `cinturillaa`, `short`, `drone-ttk`, `dron`, `dron4k`, `fly`, `flydron-con-camara-full-hd-4k-bateria-extra`, `sabanas`, `sabanas-ttk`, `sabanas2-ttk`, `almohada`, `almohada-ttk`, `manta`, `setcocina`, `cafetera`, `robotasp`, `bloodsugar`, `bloodsugar-ttk`, `bl`, `resveratrol-ttk`, `candidacleanse`, `candidacleanse-ttk`, `lemmeburn`, `lemmeburn-ttk`, `lemmeburn1`, `yerbamate`, `yerba-ttk`, `nad`, `nad-ttk`, `tiroides`, `oxido`, `turkesterona`, `turkesterona-ttk`, `oregano`, `peptides`, `creatina`, `creawomen-ttk`, `vaginales`, `intestinal`, `moringa`, `remolacha`, `serum`, `enzimas`, `migra`, `lymp`, `cam-gg`, `camara`, `gopro`, `mopa-sweet`, `mopa-1`, `mopah2o`, `mopashark-ttk`, `bissel-furfinder`, `llave-de-impacto-inalambrica-1000-n-m-2-baterias-maletin`, `aire-acondicionado-portatil-splitmax-ultra-potente-fuctz`.
- Alguns podem ter vendido só em pedidos com mais de 1 produto, que ficaram fora do mapa.
- **Atenção:** o produto `pack-3x1-perfumes-hombre-…-teste` está **ATIVO** e parece ser um produto de teste. Revisar.

---

## Pedido de teste (Task 2): preparado, NÃO executado
Arquivos:
- `pedido-teste.graphql`: `orderCreate` + `orderCancel`, os dois validados no schema.
- `pedido-teste.variables.json`: chaves `orderCreate` e `orderCancel`.

### Estrutura dos pedidos reais (6 pedidos recentes, só a estrutura)
- `sourceName` = `5690175`, app **Releasit COD Form**.
- Gateway `Cash on Delivery (COD)`.
- Status financeiro `PENDING`, ou `VOIDED` quando cancelado.
- Frete "Envío gratis" $0.
- Etiquetas: vazio, `OK` ou `CANC: SEMELHANTE`.
- Endereço de entrega: país CL + região.
- `customAttributes` (chaves): `Country code`, `Nombre y Apellido`, `Número WhatsApp`, `Región`, `Comuna`, `Calle y número de casa`, `Punto de Referencia` (opcional), `Confirmo que estaré disponible para recibir y pagar mi pedido.` e `IP address`.

### O teste preparado
| Item | Valor |
|---|---|
| Linha 1 | Pack 3x1 Mujer (`yara`), $49.900 |
| Linha 2 | Yara Tous unitário, $34.900 |
| Desconto | Código `PRUEBA-BF-PERFUME-50` de −$17.450 (total $67.350) |
| Transação | `SALE`/`PENDING` no gateway "Cash on Delivery (COD)" |
| Status financeiro | `PENDING` |
| Etiquetas | `TESTE-CLAUDE`, `NO-ENVIAR` |
| Nota | "PRUEBA – NO ENVIAR – cancelar" |
| Nome, telefone e endereço | Falsos ("PEDIDO DE PRUEBA CLAUDE", +56900000000) |
| Opções | `test: true`, `sendReceipt`/`sendFulfillmentReceipt` = false, `inventoryBehaviour: BYPASS` |
| Cancelamento | `reason OTHER`, `refundMethod.originalPaymentMethodsRefund=false`, `restock=false`, `notifyCustomer=false` |

Diferenças em relação a um pedido real:
- **Desconto:** o `orderCreate` não aplica desconto automático. Usei um código de valor fixo, então o desconto pode aparecer distribuído entre as linhas, e não só no perfume.
- **Origem:** o `sourceName` do Releasit não foi copiado. O pedido vai aparecer como criado pela API/app. Assim, ele não se passa por pedido do formulário.
- **IP:** a chave "IP address" ficou de fora.

### Fluxo para a Dropi: RISCO ALTO
- **Todo pedido não cancelado da loja Chile é importado pela Dropi.** A etiqueta `OK` não é filtro.
  - De 26/09 a 07/10, os pedidos não cancelados chegaram à Dropi em 98–99% dos casos, com ou sem `OK`.
  - Pedidos com `OK`: 580/596. Com outras etiquetas: 2109/2146.
  - O app da Dropi marca esses pedidos com `Order sent to dropi`.
  - Até pedidos com etiqueta `CANC:` que não foram cancelados entraram (47/89).
- **Pedidos criados no admin também vão.** `shopify_draft_order`: 14/14 não cancelados chegaram à Dropi. Até 3 de 4 cancelados chegaram, porque foram cancelados cerca de 25 h depois.
- **O que impede a importação é o cancelamento rápido no Shopify.**
  - Cancelados em menos de 10 min: 0/306 chegaram. Em menos de 1 h: 0/17.
  - Cancelados entre 1–6 h: 1/52. Depois de 6 h: 22/562.
  - A importação mais rápida medida foi de 1 a 6 h depois da compra. Antes de 1 h não houve nenhuma.
  - Quando um pedido importado é cancelado depois, a Dropi o marcou como `CANCELADO` (22/23), mas 1 virou `DEVOLUCION`.
- **Conclusão:** criar o pedido **pode gerar envio real na Dropi**, se ele ficar aberto.
  - Não ficou claro se `test: true` ou um SKU não vinculado na Dropi (`LAT-YARA-TOUS-100`) bloqueiam a importação. Não há dados sobre isso.
- **Para rodar com segurança:**
  1. Executar o `orderCancel` logo depois do `orderCreate` (segundos).
  2. Ou pausar a sincronização do app Dropi antes.
  3. Depois, conferir que o pedido NÃO ganhou a etiqueta `Order sent to dropi`.
  4. Conferir também que ele não aparece na Dropi.
