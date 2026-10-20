# Pellorini (relógios): marca, loja e criativos de imagem

> Marca de relógios Pellorini sobre os best sellers da loja essiora.com (hoje pellorini.com): rebranding da loja, 417+ estáticos, plano Andromeda e pacote de subida no Meta. Abra ao mexer na loja Pellorini, gerar mais criativos ou subir campanha.

## Contexto de uso
- **Frente:** e-commerce mundial em inglês (fora das 3 frentes clássicas; o plano usa o prefixo `ecom`). **Datas:** 10–11/10/2026.
- **Marca da pessoa:** Pellorini. A pessoa tem **as duas marcas** (Pelvini e Pellorini), então a assinatura Pelvini no mostrador está liberada. Os produtos vinham titulados "Pelvini®" com reviews/números copiados da Pelvini — não usar esses números em criativo.
- **Decisões da pessoa (10/10/2026):** devolução real de **90 dias**; venda e envio para o **mundo todo** (sem citar país de origem).
- **Estudo de referência:** `Downloads\ESTUDO-IMAGENS-RELOGIOS\` (11 lojas, 5.772 imagens + textos + planilha; `anuncios.md` por loja). Plano: `Produtividade com ia\02-relatorios\2026-10_ecom_plano_andromeda-essiora-best-sellers.md` (9 conceitos × 3 execuções; abordagem A templates em código + B cenas IA).
- **Loja (Shopify), feito:**
  - 10/10: 49 produtos renomeados Pelvini → Pellorini (backup `Downloads\PELLORINI-LOJA\backup_produtos_antes.txt` e `produtos_antes.json`; levantamento em `PLANO-TROCAS.md`); handles/URLs não mudaram;
  - 11/10: 77 fotos rebrandeadas PELVINI → PELLORINI (59 caixas + 18 closes de mostrador; Nano Banana 2 no Flora, US$ 9,18) em `PELLORINI-LOJA\fotos-pellorini\<handle>_<pos>.jpg`, trocadas na Shopify mantendo id/posição da mídia (77/77 conferidas; backup `_backup_midia_loja_antes.json`); +8 caixas verde-água dos best sellers (só a faixa da tampa editada, `PELLORINI-CRIATIVOS\caixas_pellorini\so_tampa.py`) → 85 fotos;
  - 11/10: logo Essiora substituído por wordmark PELLORINI (original em `PELLORINI-LOJA\logo\`);
  - 11/10 noite: domínio principal = **pellorini.com** (4 mercados); tema publicado = "Dawn - Pellorini (feminino)" `193592000788`; coleção automática "All Watches" (handle `all`, tag best-sellers, template pelvini).
- **Temas pendentes de publicação:** "Dawn - Pellorini (sem Essiora)" `193596260628` (rodapé sem Essiora + botões #302D2A); "garantia 2 anos" `193582498068` (avaliações restauradas: pv-reviews, 4.8/5 – 13,066). Página feminina: template `product.pellorini-feminino.json` para 16 modelos femininos (lista no registro) — aplicar o templateSuffix só depois de publicar o tema.
- **Criativos:** `Downloads\PELLORINI-CRIATIVOS\` — 417 estáticos (lote1, lote2 com 348 imagens em 20 famílias 1:1 e 9:16, `lote3-vencedores`), scripts `gerar_lote*.py`, `gerar_vencedores.py`, textos em `lote1\TEXTOS-DOS-ANUNCIOS.md`.
- **Top 5 em vendas:** Vittorio, Dominante, Milano, Opulent, Maretti.
- **Pacote de subida (US$ 150/dia, CPA-alvo US$ 20):** `SUBIDA-META-150-VENCEDORES\` (`PLANO-DE-SUBIDA.md`, `plano-subida.json`, planilha, `LINKS.md`, prompts para outro Claude executar e verificar). Vendas ABO 5 × US$ 20 + Catálogo US$ 50; US/GB/CA/AU; oferta Buy 1 Get 1 Free, frete grátis rastreado, 90 dias de devolução, garantia de 24 meses; campanhas criadas pausadas.
- **Pendências:**
  - ainda com marca antiga: napoli #5 (PELVINI no fundo), pv-cmp-5 e pv-cmp-8 do tema (PELVINI na pulseira/mostrador);
  - rodapé ppfooter (Essiora Club/About Essiora) e logo Essiora nas páginas Dawn padrão até publicar o tema "sem Essiora"; essiora.com (sem www) não redireciona;
  - home (index.json) com "Ships From the UK" (gravação bloqueada pela trava de permissão); rodapé "home cleaning tips"; 30 × 90 dias; UK × US;
  - tema publicado segue **sem avaliações** até a pessoa publicar o tema com reviews (a API bloqueia editar/publicar o MAIN);
  - verba diária real e respostas de compliance.

## Lógica de uso
- **Rebranding de foto de produto:** gerar no Flora (Nano Banana 2) e **colar o mostrador original de volta** — o modelo reescreve texto pequeno (data, numerais, marca de fábrica) mesmo pedindo para não mexer (`_orig_L3\fixdial.py`, `_orig_L4\fixdial_L4.py`). Em caixa, editar só a faixa da tampa sobre a base original em 4000 px. Trocar na Shopify com `stagedUploadsCreate` + `fileUpdate(originalSource)` para manter id e posição; conferir por diferença de imagem; backup antes.
- **Tema:** API não grava no MAIN → duplicar, gravar na cópia, a pessoa publica. Nunca esconder avaliações sem pedido.
- **Criativos:** famílias por estratégia de referência (BOGO saturado, "Is a name worth", VS designer, "Which one are you", ranking, e-mail, carta, tweet, iMessage, pôster, limited, cores, maleta…); nome do arquivo `conceito_persona_familia_produto_formato` = nome do anúncio. Lotes e subidas começam pelo **top 5 de vendas**, nunca por variedade de foto.
- **Subida:** 1 relógio por imagem → carrossel (cada card para a página do relógio); vários relógios na imagem → formato flexível para a coleção. Lance sem limite nos dias 1–14, depois limite de custo de US$ 20.
- **Compliance:** listar riscos e perguntar manter × suavizar; orçamento sempre com custo + tempo + opção mais rápida.
- **Se a pessoa pedir mais:** gerar criativos femininos quando houver ranking feminino; resolver as fotos com marca antiga; ler resultado por conceito após a subida.

## Relacionados
- [../04-fluxo-producao-criativos.md](../04-fluxo-producao-criativos.md)
- [../06-troca-de-marca.md](../06-troca-de-marca.md) (rebranding de fotos)
