# Estudo das IMAGENS Vitaly → Lymphoria (Chile)

Data: 09/10/2026. Fonte: `IMAGENS\` (**14 arquivos, não 15**: o `00-indice.csv` também lista só 14 anúncios de imagem). Leitura: RapidOCR (bruto em `_estudo\_ocr_imagens.json`) + leitura visual de cada imagem em tamanho cheio. Nada foi gerado nem gasto.

## Base de comparação: ficha Lymphoria
Fontes: chileverificada.com/products/lymphoria (lida hoje) e a memória do lote Lymphoria.
- **Fórmula:** 4 ervas (galio, trébol rojo, stillingia, fresno espinoso), 100% vegetal, sem álcool, sem açúcar, sem glúten, vegano.
- **Frasco:** âmbar com conta-gotas, faixa verde "LYMPHORIA · drenaje linfático", "Sabe a Miel". O frasco Vitaly também é âmbar com conta-gotas, mas tem rótulo marrom/creme em inglês ("Lymphatic Drainage · Herbal Experts"), então **o rótulo precisa ser trocado em todas as imagens**.
- **Oferta:** Compre 1 Reciba 2 $34.990 · 2→4 $54.990 · 3→6 $72.990. Despacho grátis, pagas al recibir, garantia de **90 dias**, entrega em 24–72 h (Starken/Blue Express).
- **Claims da página:** cara menos inchada pela manhã; menos líquido em pernas, tornozelos e pés; mais energia; pele. Linha do tempo: semana 1 → semana 4. Estatísticas: 97% cara, 84% pernas, 490 clientes.
- **Uso:** a memória registra "unas gotas bajo la lengua cada mañana". A página não mostrou a dose. **Dose a confirmar** (precisa de revisão manual). O Vitaly diz "20 gotas en agua mañana y noche".

## Como adaptar (vale para todas)
- **Frasco/rótulo:** edição de imagem com **Nano Banana 2** (Flora). Mandar a imagem original + a referência neutra do frasco Lymphoria (nó n59 do projeto `prj_ns7cvmdqvtn37b53wfnywhr9q58fjte1`). Prompt: "replace ONLY the bottle label with @Image2's label, keep layout, text, lighting and everything else identical". Custo de **~US$0,072–0,108 por imagem/tentativa**, e conta-se +1 tentativa para QA.
- **Textos (marca, oferta, datas, dose):** redesenho local sem custo (PIL: cobrir com a cor de fundo + reescrever na mesma fonte/peso). É mais seguro que pedir ao Nano Banana texto exato em espanhol. Opção: incluir as trocas de texto no mesmo prompt do Nano Banana e corrigir localmente o que sair errado.
- **Tempo médio:** cerca de 10–15 min por imagem (edit + texto + QA com zoom no rótulo).
- Compliance: os itens abaixo estão **só listados, não alterados**. A decisão de manter ou suavizar é da pessoa.

---

## 02 — Oferta "HOY 2x1" (1080x1350)
- **Formato:** oferta/produto (2 frascos inclinados, folhas, fundo menta).
- **Texto:** "VITALY" (logo topo) · "HOY" · "2x1" · "en GOTAS VITALY" · "+5.000 chilenas ya lo usan para sus piernas".
- **Marca:** logo no topo, "GOTAS VITALY" na faixa verde, **2 frascos com rótulo VITALY legível** (grandes).
- **Oferta:** 2x1 / título "Compre 1 Reciba 2". Bate com o pack 1→2 da Lymphoria.
- **Claims vs ficha:** "+5.000 chilenas" não está na ficha (só "490 clientes" na pesquisa) → precisa de revisão manual. "para sus piernas" bate.
- **Compliance:** urgência ("HOY"); número de usuárias não comprovado.
- **Adaptar:** Nano Banana para os 2 rótulos (o de trás é parcial) + texto local (logo e "GOTAS LYMPHORIA"). Fácil.
- **Copy (texto/título):** "¿Aún dudas?… garantía de 45 días" → trocar por **90 días**. Título "Compre 1 Reciba 2" pode ficar.
- **Potencial: 4.** Oferta limpa e reutilizável; 5 versões agrupadas no índice (sinal de escala).

## 04 — Notas do iPhone "Cara de Cortisol" (1638x2048)
- **Formato:** nativo/meme (print do app Notas) + produto.
- **Texto:** "El estrés de la vuelta al trabajo hizo esto 😢" · "El fin de tu 'Cara de Cortisol'" · "Hinchazón matutina y papada DESAPARECEN / Mandíbula y pómulos VUELVEN / Ojeras y párpados caídos SE REDUCEN" · "Por eso Gotas Vitaly 💚 tiene su PROMOCIÓN de MARZO. Las gotas virales que drenan el líquido mientras duermes 😴" · "COMPRA 1, RECIBE 2 + ENVÍO GRATIS 📫" · botão "DRENAR LA CARA DE CORTISOL →".
- **Marca:** "Gotas Vitaly" no texto; 1 frasco grande com rótulo legível.
- **Oferta:** Compra 1 Recibe 2 + envio grátis. Bate.
- **Claims vs ficha:** a cara menos inchada pela manhã bate (claim principal da Lymphoria). "Ojeras y párpados", "mandíbula y pómulos" e "mientras duermes" **não estão na ficha**. "PROMOCIÓN de MARZO" está datado.
- **Compliance:** "DESAPARECEN" (resultado absoluto); cortisol/estresse (termo fisiológico); copy com "hasta en un 40%" (estatística sem fonte).
- **Adaptar:** texto local (Vitaly→Lymphoria, MARZO→mês atual ou "de OCTUBRE"/remover) + Nano Banana no frasco. A hora "11:33" pode ficar.
- **Copy:** "…el estrés puede reducir tu drenaje linfático hasta en un 40%" → dado sem fonte, revisar. Título "Oferta 2x1" ok.
- **Potencial: 5.** Formato nativo, gancho de dor atual (cara inchada) e alinhado ao claim nº 1 da Lymphoria.

## 06 — Grade 2x2 de problemas (1638x2048)
- **Formato:** problema/agitação (3 fotos de corpo + quadrante do produto).
- **Texto:** "Hinchazón" · "Pies hinchados" · "Cara hinchada y papada" · "La solución: Gotas VITALY®" · botão "Ver la solución →".
- **Marca:** "Gotas VITALY®" + 1 frasco médio com rótulo legível.
- **Oferta:** nenhuma na arte; título "Oferta 2x1".
- **Claims vs ficha:** abdômen, pés e cara batem com a ficha.
- **Compliance:** fotos de partes do corpo (barriga exposta; pé avermelhado parece inflamação/condição médica); "La solución" implica tratamento.
- **Adaptar:** texto local ("Gotas LYMPHORIA®") + Nano Banana no frasco do 4º quadrante. Fácil.
- **Copy:** "Pensé que era grasa… pero era retención de líquidos…" serve como está, trocando só a marca (já não cita a marca).
- **Potencial: 4.** Identificação rápida com 3 dores da ficha; o risco está nas fotos.

## 07 — "Yo pasé de talla XL a M*" com frascos (1501x2001)
- **Formato:** antes/depois simbólico (frasco grande → frasco pequeno).
- **Texto:** logo "VITALY" · "YO PASÉ DE TALLA XL a M*" · "**Los resultados pueden variar según cada persona".
- **Marca:** logo + **2 frascos com rótulo VITALY grande e legível**.
- **Oferta:** nenhuma na arte; título "Compre 1 Reciba 2". **Landing masculina** (`advertorial-gotas-hombres`).
- **Claims vs ficha:** troca de talla **não está na ficha** (o mais próximo é "Marta perdió 10 cm" nos depoimentos).
- **Compliance:** redução de medida/talla (perda de peso implícita); antes/depois.
- **Adaptar:** Nano Banana nos 2 frascos (manter a diferença de tamanho) + logo local. Fácil, mas o claim é o ponto.
- **Copy:** "😱 La desinflamación aparece cuando menos lo esperas..." ok. Não existe landing masculina da Lymphoria → apontar para a página principal.
- **Potencial: 3.** Visual criativo e simples, mas o claim de talla está fora da ficha e há risco de Meta.

## 08 — "¿Aún luces embarazada?" Mes 1-3 (1152x2048, 9:16)
- **Formato:** antes/depois em ilustração (silhuetas de barriga) + oferta Cyber.
- **Texto:** logo "cybervitaly" · "¿AÚN LUCES EMBARAZADA? ¡Es retención de líquidos!" · "Mes 1 / Mes 2 / Mes 3" · "SÓLO POR CYBER LLEVA 2 PAGA 1 ¡SÓLO ESTA SEMANA!".
- **Marca:** "cybervitaly" (logo de evento) + 1 frasco médio legível.
- **Oferta:** Lleva 2 Paga 1 (equivale a 1→2, bate). **Cyber vencido.**
- **Claims vs ficha:** 3 meses até a barriga lisa **não está na ficha** (a ficha fala em 4 semanas e não promete barriga plana).
- **Compliance:** antes/depois de corpo (ilustrado); referência a gravidez/body shaming; urgência ("sólo esta semana").
- **Adaptar:** redesenho local do topo (trocar "cybervitaly" por logo Lymphoria ou remover) + "SÓLO POR CYBER" → outra urgência ou "ENVÍO GRATIS · PAGAS AL RECIBIR" + Nano Banana no frasco.
- **Copy:** "No es falta de tratamiento, es falta de constancia…" serve sem marca. Título "Compra 1 y Recibe 2 ✅" ok.
- **Potencial: 3.** Gancho forte, mas o maior risco de reprovação no Meta está aqui.

## 13 — Story UGC "¿20 gotas en agua y listo?" (1080x1920)
- **Formato:** UGC/depoimento em formato de story (Instagram) com conta-gotas pingando em copo d'água.
- **Texto:** "tamy.c 22h" · "¿20 gotas en agua y listo? ¿Así de simple? 😂" · "Mañana y noche. Un frasco dura el mes. Y desde la primera semana la ropa me 👏 empezó a quedar" (frase cortada) · "glen.quijada Abdomen desinflamado y cara deshinchada. Excelente producto 🔥".
- **Marca:** 1 frasco médio, levemente inclinado, rótulo VITALY legível.
- **Oferta:** nenhuma; título "Su fórmula líquida apoya un drenaje profundo"; CTA "Saiba mais" → página de produto.
- **Claims vs ficha:** **dose diferente** ("20 gotas en agua, mañana y noche, un frasco dura el mes" vs. "gotas bajo la lengua cada mañana") → precisa de revisão manual da dose real. "Desde la primera semana" bate (semana 1).
- **Compliance:** fotos de perfil de pessoas reais aparentes (tamy.c, glen.quijada) → avaliar uso de terceiros; depoimento de resultado.
- **Adaptar:** Nano Banana no frasco (foto realista, ótimo caso para o modelo) + texto local nos balões, se a dose mudar. Trocar ou desfocar avatares e @.
- **Copy:** "A diferencia de las limpiezas agresivas o los diuréticos…" bate com o "suave, sem diuréticos agressivos" da ficha.
- **Potencial: 5.** O mais nativo e de menor risco; mostra o modo de uso.

## 15 — FAQ "4 preguntas, 4 respuestas" (1638x2048)
- **Formato:** FAQ/objeções + produto central.
- **Texto:** "Todo lo que nadie te dice antes de comprarlo · 4 PREGUNTAS · 4 RESPUESTAS. SIN LETRA CHICA".
  1. "¿Tengo hipotiroidismo, puedo tomarlo? SÍ. Igual consulta con tu médico si tomas medicamentos."
  2. "¿Cómo y cuándo se toma? 20 GOTAS en la mañana y 20 EN LA TARDE, en un vaso de agua."
  3. "¿Cuándo empiezo a ver resultados? Las primeras diferencias desde el DÍA 7. Resultados completos AL MES."
  4. "¿Si dejo de tomarlo vuelve la hinchazón? Tu SISTEMA LINFÁTICO se reactiva. Con hábitos saludables los resultados se mantienen."

  Rodapé: "Sin trucos. Sin letra chica. Solo lo que necesitas saber para decidir." · "VER LAS GOTAS ✓" · "ENVÍO GRATIS A CHILE".
- **Marca:** só no frasco central (médio, legível), com trébol rojo ao lado (ingrediente comum às duas fórmulas).
- **Oferta:** envio grátis; título "Compra 1 y Recibe 2 ✅".
- **Claims vs ficha:** dia 7 e "al mes" batem com a linha do tempo da Lymphoria. **Dose diferente.** Hipotireoidismo "SÍ" **não está na ficha**.
- **Compliance:** doença (hipotireoidismo); menção a médico/medicamentos; promessa de resultado mantido.
- **Adaptar:** Nano Banana no frasco + texto local na resposta 2 (dose), se mudar. Layout limpo para o redesenho.
- **Copy:** mesmo texto da 08 ("No es falta de tratamiento…"), ok.
- **Potencial: 4.** Quebra objeções muito bem; precisa da dose correta e de decisão sobre o hipotireoidismo.

## 16 — Comparativo "China 40 días vs Chile 48 horas" (1080x1350)
- **Formato:** comparativo nós × eles.
- **Texto:** "Hay 2 formas de comprar DRENAJE LINFÁTICO." · "✗ Una viene de CHINA en 40 DÍAS" · "✓ La otra llega a tu casa en 48 horas DESDE CHILE" · "GENÉRICO DESCONOCIDO: Marca no reconocible / Origen incerto / Sin control de calidad" · "VITALY: Envíos rápidos y locales / Fórmula PREMIUM / Certificado y garantizado".
- **Marca:** selo verde "VITALY" grande + 1 frasco legível. O frasco genérico (sem rótulo) fica.
- **Oferta:** nenhuma; título "Oferta Solo por HOY".
- **Claims vs ficha:** a ficha diz 24–72 h (não 48 h) → usar "24 a 72 horas" ou manter 48 h após confirmação. "Certificado" e "Fórmula PREMIUM" **não estão na ficha**. Só vale para o Chile (mapa e bandeira).
- **Compliance:** "Certificado" sem comprovação; urgência no título ("Solo por HOY"); comparação com produto chinês (genérico, sem marca de terceiro).
- **Adaptar:** texto local (selo VITALY → LYMPHORIA; horas) + Nano Banana no frasco da direita.
- **Copy:** "Nuestras bodegas son LOCALES. Que no te engañen con productos genéricos exteriores" ok.
- **Potencial: 4.** Ângulo de confiança forte para COD Chile; poucos claims de saúde.

## 18 — "¿Tobillos hinchados?" antes/24h/4 semanas (1638x2048)
- **Formato:** antes/depois em ilustração (3 pés) + oferta Cyber.
- **Texto:** "cybervitaly" · "¿Tobillos hinchados? Prueba Vitaly®" · "ANTES / 24 HORAS / 4 SEMANAS" · "SÓLO POR CYBER LLEVA 2 PAGA 1 ¡SÓLO ESTA SEMANA!".
- **Marca:** logo cybervitaly, "Prueba Vitaly®" e 1 frasco legível (ao lado de um copo com líquido amarelo).
- **Oferta:** Lleva 2 Paga 1 (bate). **Cyber vencido.**
- **Claims vs ficha:** tornozelos batem (84%). "24 horas" **não está na ficha** (a ficha começa na semana 1); 4 semanas bate.
- **Compliance:** antes/depois (ilustrado); resultado em 24 h; urgência.
- **Adaptar:** igual à 08 (topo + faixa Cyber em texto local) + Nano Banana no frasco. O copo com líquido amarelo combina com "sabe a miel".
- **Copy:** "Probé de todo y lo único que me funcionó fueron estas gotas…" ok sem marca.
- **Potencial: 4.** Dor nº 2 da ficha, visual didático; trocar o rótulo "24 HORAS" se a pessoa quiser.

## 20 — Homem sem camisa "XL a M en 6 semanas" (1501x2001)
- **Formato:** antes/depois de corpo (calça larga, abdômen definido).
- **Texto:** logo "VITALY" · "Pasé de talla XL a M* EN 6 SEMANAS" · "**Los resultados pueden variar según cada persona".
- **Marca:** logo + 1 frasco inclinado, rótulo legível (faixa verde, diferente dos outros: variação de arte).
- **Oferta:** nenhuma; título "Compre 1 Reciba 2"; **landing masculina**.
- **Claims vs ficha:** talla/6 semanas e físico definido **não batem** (drenagem não gera tanquinho; a Lymphoria fala com mulheres).
- **Compliance:** perda de peso/talla com prazo; antes/depois de corpo; imagem corporal irreal.
- **Adaptar:** Nano Banana no frasco + logo local. Simples tecnicamente.
- **Copy:** "Un cambio que me sigue impresionando..." ok.
- **Potencial: 2.** Público errado para a Lymphoria e risco alto.

## 21 — "#1 del CyberDay Chile" mão segurando frasco (1080x1350)
- **Formato:** produto/oferta (foto realista: mão + caixa de envio com mais frascos).
- **Texto:** "LAS GOTAS DE DRENAJE #1 DEL CYBERDAY CHILE" · "CHAO HINCHAZÓN" · selo "COMPRA 2 LLEVA 4 GRATIS" · botão "APROVECHAR HASTA 61% OFF →".
- **Marca:** frasco na mão (grande, legível) + **2 frascos na caixa ao fundo** (desfocados, "VITALY" visível).
- **Oferta:** Compra 2 Lleva 4 (bate com o pack 2→4). "Hasta 61% OFF" → conferir: 3→6 a $12.165/unid. vs $34.990 dá ~65%; depende do preço de referência (precisa de revisão manual).
- **Claims vs ficha:** "#1 del CyberDay" **não está na ficha** e está datado.
- **Compliance:** ranking "#1" sem comprovação; desconto percentual a validar; evento vencido.
- **Adaptar:** Nano Banana para os 3 frascos (o da mão + os 2 da caixa; pode ser preciso 2 passes) + texto local ("#1 DEL CYBERDAY CHILE" → ex.: "LAS GOTAS DE DRENAJE QUE PAGAS AL RECIBIR").
- **Copy:** "Probé de todo…" ok.
- **Potencial: 3.** A foto é boa; o gancho depende do evento e precisa ser reescrito.

## 27 — Outdoor/relógio de rua com review (1152x2048, 9:16)
- **Formato:** mockup de outdoor (OOH) + depoimento.
- **Texto:** "+858 reseñas verificadas ★★★★★" · "“4 hierbas, dos gotas al día, cinturón que no aprieta.” – Carlos R." · selo "LLEVA 2, PAGA 1 SÓLO ESTA SEMANA" · botão "SIENTE LA DIFERENCIA →".
- **Marca:** 1 frasco grande inclinado, rótulo VITALY bem legível.
- **Oferta:** Lleva 2 Paga 1 (bate).
- **Claims vs ficha:** "4 hierbas" **bate**. "Dos gotas al día" não bate com o "20 gotas" do próprio Vitaly nem com a dose Lymphoria a confirmar. "+858 reseñas" **não está na ficha**. Review masculino.
- **Compliance:** número de reseñas não comprovado; depoimento; urgência.
- **Adaptar:** Nano Banana no frasco (o modelo lida bem com a luz do outdoor) + texto local (número de reseñas e dose). Opção: trocar Carlos R. por uma depoimento feminino.
- **Copy:** "Probé de todo…" ok.
- **Potencial: 4.** Formato premium diferente, claim de 4 ervas idêntico.

## 28 — Depoimento longo "Carla, 51 años" (1638x2048)
- **Formato:** depoimento (texto + foto de rosto + ícones de benefício).
- **Texto:** logo "VITALY" ★★★★★ · "Mi abdomen no había cambiado en 6 años, sin importar lo que intentara. Keto, Pilates 5 veces por semana, incluso Ozempic durante 8 meses. Después de 3 semanas usando Vitaly, mis jeans cierran sin luchar conmigo y mi rostro está menos hinchado. Quién sabe qué traerán las próximas 3 semanas." – Carla, 51 años · ícones "DRENA EL ABDOMEN / ESTÓMAGO MÁS PLANO / ROSTRO MENOS HINCHADO" · "• GOTAS LÍQUIDAS • 4 HIERBAS • LIBRE DE GMO •" · faixa "POR FIN, UNA SOLUCIÓN QUE FUNCIONA PARA MUJERES MAYORES DE 40."
- **Marca:** logo, "usando Vitaly" no texto, ícone da marca no rodapé, 1 frasco médio legível.
- **Oferta:** nenhuma; título "Obtén el tuyo ahora".
- **Claims vs ficha:** 4 ervas e rosto menos inchado batem. "Libre de GMO" não está na ficha (a ficha diz vegano/sem glúten) → trocar por "VEGANO" ou "SIN ALCOHOL". A página Lymphoria já tem uma "Carla, 36" com outro depoimento: **não misturar idade/nome**. A foto de rosto parece de pessoa real.
- **Compliance:** medicamento (Ozempic); idade/atributo pessoal ("mujeres mayores de 40" — política de atributos pessoais do Meta); "estómago más plano" (corpo/peso); depoimento de resultado.
- **Adaptar:** texto local (Vitaly→Lymphoria em 3 pontos, GMO) + Nano Banana no frasco. Avaliar troca da foto do rosto.
- **Copy:** "Probé de todo…" ok.
- **Potencial: 4.** Depoimento forte e público 40+ alinhado; tem mais itens sensíveis que os outros.

## 29 — Antes/depois real de abdômen (1080x1350)
- **Formato:** antes/depois fotográfico (barriga, ambiente clínico com papel de maca) + manchete.
- **Texto:** "De abdomen abultado a cintura marcada: el cambio sorprende" · "Vitaly® disminuye volumen retenido y que la forma natural del cuerpo se note" · "www.vitalychile.com".
- **Marca:** "Vitaly®" no texto, URL vitalychile.com e 1 frasco central legível.
- **Oferta:** nenhuma; título "Oferta 2x1".
- **Claims vs ficha:** "volumen retenido" é aceitável (retenção); "cintura marcada" **não está na ficha**.
- **Compliance:** antes/depois real de corpo (risco alto no Meta); ambiente que parece procedimento estético/clínico (a mudança pode não ser do produto).
- **Adaptar:** texto local (Vitaly®→Lymphoria®, URL → chileverificada.com) + Nano Banana no frasco.
- **Copy:** "Algo que está sirviendo a un montón de chilenas..." ok.
- **Potencial: 2.** Prova visual forte, mas é o mais arriscado e de origem duvidosa.

---

## Tabela-resumo

| Img | Formato | Marca a trocar (texto / frascos) | Oferta na arte | Compliance (só listado) | Adaptação | Pot. |
|---|---|---|---|---|---|---|
| 02 | Oferta 2x1 | logo + "GOTAS VITALY" / 2 frascos | HOY 2x1 | urgência, "+5.000 chilenas" | NB2 + texto local | 4 |
| 04 | Notas iPhone "Cara de Cortisol" | "Gotas Vitaly" / 1 | Compra 1 Recibe 2 + envio grátis, "Promo de MARZO" | "DESAPARECEN", cortisol, 40% (copy) | NB2 + texto (marca, mês) | **5** |
| 06 | Grade 2x2 de problemas | "Gotas VITALY®" / 1 | — | fotos de corpo, pé avermelhado, "la solución" | NB2 + texto | 4 |
| 07 | Frascos XL→M | logo / 2 | — | talla/peso, antes/depois simbólico, landing masculina | NB2 + logo | 3 |
| 08 | "¿Aún luces embarazada?" Mes 1-3 | "cybervitaly" / 1 | Lleva 2 Paga 1 (Cyber vencido) | antes/depois ilustrado, gravidez, urgência | NB2 + topo/faixa local | 3 |
| 13 | Story UGC copo d'água | — / 1 | — | dose diferente, avatares de terceiros | NB2 (+ balões se a dose mudar) | **5** |
| 15 | FAQ 4 perguntas | — / 1 | envio grátis | hipotireoidismo, médico, dose diferente | NB2 + texto (dose) | 4 |
| 16 | China 40 dias × Chile 48 h | selo "VITALY" / 1 | — | "certificado", 48 h vs 24–72 h, "Solo por HOY" | NB2 + texto | 4 |
| 18 | Tornozelos antes/24h/4 sem | "cybervitaly", "Prueba Vitaly®" / 1 | Lleva 2 Paga 1 (Cyber vencido) | antes/depois ilustrado, 24 h, urgência | NB2 + topo/faixa local | 4 |
| 20 | Homem abdômen XL→M 6 sem | logo / 1 | — | peso/talla com prazo, corpo, público masculino | NB2 + logo | 2 |
| 21 | Mão + caixa "#1 CyberDay" | — / 3 (1 + 2 no fundo) | Compra 2 Lleva 4, "hasta 61% OFF" | "#1" sem prova, % a validar, evento vencido | NB2 (2 passes) + texto | 3 |
| 27 | Outdoor com review | — / 1 | Lleva 2 Paga 1 sólo esta semana | "+858 reseñas", dose, urgência | NB2 + texto | 4 |
| 28 | Depoimento Carla 51 | logo + "Vitaly" + ícone / 1 | — | Ozempic, "mujeres mayores de 40", estómago plano, GMO | NB2 + texto | 4 |
| 29 | Antes/depois real de abdômen | "Vitaly®" + URL / 1 | — | antes/depois real de corpo, ambiente clínico | NB2 + texto | 2 |

**Custo do lote (Nano Banana 2):** 14 imagens, ~15 passes (a 21 precisa de 2): **~US$1,10–1,60** em 1 tentativa, **~US$2,20–3,20** com 1 refação de QA cada. O texto é local e sem custo. **Tempo:** ~2,5–3,5 h no total (~10–15 min/imagem), com cerca de 1 h a menos se o texto entrar no próprio prompt do NB2 (com risco de erro de grafia em espanhol).

## Texto do anúncio (00-indice.csv): notas de adaptação
- **Títulos:** "Compre 1 Reciba 2", "Compra 1 y Recibe 2 ✅" e "Oferta 2x1" batem com o pack 1→2 da Lymphoria e podem ficar. Os títulos "Oferta Solo por HOY" e "Obtén el tuyo ahora" funcionam como estão, sem marca. "Su fórmula líquida apoya un drenaje profundo" (13) também pode ficar.
- **Textos principais:** só o da **02** cita condição a mudar ("garantía de **45** días" → **90 días**). Os demais não citam a marca e podem ser reusados. Pontos de revisão:
  - 04: "hasta en un 40%" (estatística sem fonte).
  - 13: "a diferencia de… diuréticos" (ok com a ficha).
  - 16: "bodegas LOCALES" (ok para o Chile).
- **Link description:** "Descubre Vitaly Chile®…", "Vitaly® Chile" e "VITALY" → trocar pela marca Lymphoria/loja chileverificada.
- **Destino:** todas apontam para vitaly-chile.com. Trocar por https://chileverificada.com/products/lymphoria. Não há landing masculina nem advertorial equivalente mapeado → precisa de revisão manual (07 e 20 usavam `advertorial-gotas-hombres`; 08 e 15 usavam `drenaje-celulitis`).
- **Copy repetida:** 08 e 15 usam o mesmo texto; 18, 21, 27 e 28 também ("Probé de todo…"). Para a Lymphoria, vale variar.
- **Sugestão de fechamento universal** (coerente com o padrão dos vídeos): "Envío gratis · Pagas al recibir · 90 días de garantía".

## Pendências (revisão manual)
1. Dose real da Lymphoria (afeta 13, 15 e 27).
2. "+5.000 chilenas", "+858 reseñas", "#1", "61% OFF" e "Certificado": nenhum está na ficha.
3. Prazo de entrega no comparativo (48 h × 24–72 h).
4. Landings específicas (masculina/celulite) não existem para a Lymphoria.
5. Fotos de terceiros (avatares da 13, rosto da 28, corpos da 06 e 29): confirmar a origem e o direito de uso.
