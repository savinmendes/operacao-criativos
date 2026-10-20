---
name: project-pellorini-relogios
description: "Marca de relógios Pellorini — loja essiora.com (best sellers), plano Andromeda de criativos em imagem a partir do estudo de 11 lojas (10/10/2026)"
metadata:
  node_type: memory
  type: project
  originSessionId: 222fc591-a4ca-45ce-9081-248e3667a3bb
  modified: 2026-10-11T01:28:01.780Z
---

- Marca da pessoa: **Pellorini** (relógios), usando os produtos da coleção best-sellers de essiora.com (hoje titulados "Pelvini®", com reviews/números copiados da Pelvini — não usar em criativo; propor renomear).
- Decisões da pessoa (10/10/2026): devolução real = **90 dias**; venda/envio = **mundo todo** (sem citar país de origem).
- Estudo de referência: `Downloads/ESTUDO-IMAGENS-RELOGIOS/` (11 lojas, 5.772 imagens + textos + planilha). Plano: `02-relatorios/2026-10_ecom_plano_andromeda-essiora-best-sellers.md` (9 conceitos × 3 execuções; abordagem A templates em código + B cenas IA).
- 10/10/2026 feito: 49 produtos renomeados Pelvini→Pellorini (backup `Downloads/PELLORINI-LOJA/backup_produtos_antes.txt`); tema cópia "Dawn - Pellorini (mundo, 90 dias)" id 193568080148 com textos corrigidos (aguarda a pessoa publicar). Home (index.json, aspirador) ficou com "Ships From the UK" — gravação bloqueada pela trava de permissão. Handles/URLs e fotos (logo PELVINI) não mudaram.
- 10/10/2026: pessoa tem as DUAS marcas (Pelvini e Pellorini) — assinatura Pelvini no mostrador está liberada. 417 estáticos em `Downloads/PELLORINI-CRIATIVOS/` (lote1, lote2, scripts gerar_lote*.py regeneram tudo). Top 5 vendas: Vittorio, Dominante, Milano, Opulent, Maretti (lote3-vencedores). Pacote de subida US$150/dia (CPA-alvo US$20): `SUBIDA-META-150/` (plano-subida.json, PLANO-DE-SUBIDA.md, planilha, prompt p/ outro Claude); Vendas ABO 5×US$20 + Catálogo US$50, US/GB/CA/AU, links essiora.com (pellorini.com redireciona).
- Pendente (antigo): correções na loja (rodapé "home cleaning tips", 30×90 dias, UK×US) — conector Shopify precisa reconectar na Essiora; verba diária do teste; respostas de compliance.

Relacionado: [[feedback-compliance-perguntar]], [[feedback-orcamento-com-tempo]]
- 11/10/2026: 77 fotos da loja rebrandeadas PELVINI→PELLORINI (59 caixas + 18 closes de mostrador), Nano Banana 2 no Flora, US$9,18 real. Saída `Downloads/PELLORINI-LOJA/fotos-pellorini/<handle>_<pos>.jpg` + resultado_L1..L7.json; trocadas na Shopify em 11/10 via stagedUploadsCreate + fileUpdate(originalSource) mantendo id/posição da mídia (77/77 conferidas por diferença de imagem); backup da lista de mídia em _backup_midia_loja_antes.json. Lição: o Gemini reescreve o texto pequeno do mostrador (data, marca de fábrica, numerais) mesmo pedindo pra não mexer → sempre colar o mostrador original de volta (`_orig_L3/fixdial.py`, `_orig_L4/fixdial_L4.py`), sem regerar.
- 11/10/2026: +8 caixas verde-água dos best sellers (Vittorio, Milano, Dominante, Opulent x3, Maretti x2) trocadas na loja (base original 4000px + só a faixa da tampa editada: `PELLORINI-CRIATIVOS/caixas_pellorini/so_tampa.py`). Total 85 fotos. Ainda com marca antiga (fora de caixa): napoli #5 (PELVINI no fundo), pv-cmp-5 e pv-cmp-8 do tema (PELVINI na pulseira/mostrador).
- 11/10/2026: avaliações restauradas no tema "garantia 2 anos" (193582498068): pv-reviews reativada, rating_text padrão 4.8/5 – 13,066, pell_fix removido do produto e da coleção. Tema publicado (193568080148) segue SEM avaliações até a pessoa publicar o 2 anos (API bloqueia publicar/editar MAIN).
- 11/10/2026: página feminina igual Pelvini — template product.pellorini-feminino.json no tema "Dawn - Pellorini (feminino)" 193592000788 (lifestyle pv-fem-life-1..6, 24K Gold, Eternal Elegance/Grace in Every Detail, reviews femininas, sugestões femininas). 16 femininos (lista = coleção Women da pelvini.com): bellissima, aurora, perla, aria, gemma, carina, valentina, livia, grazia, valore, fiorella, luna-perla, lunetta, serpina, serafina, clovera → templateSuffix pellorini-feminino só DEPOIS de publicar o tema.
- 11/10/2026 noite: domínio principal = pellorini.com (4 mercados nele); tema publicado = "Dawn - Pellorini (feminino)" 193592000788; criada coleção automática "All Watches" handle all (tag best-sellers, template pelvini) p/ /collections/all. Pendente: rodapé ppfooter ainda diz Essiora (Essiora Club/About Essiora) e logo Essiora nas páginas Dawn padrão; essiora.com (sem www) não redireciona.
- 11/10/2026: logo essiora-logo-A.jpg substituído (fileUpdate) por wordmark PELLORINI (original salvo em PELLORINI-LOJA/logo/); rodapé sem Essiora + botões roxos→#302D2A no tema "Dawn - Pellorini (sem Essiora)" 193596260628 (aguarda publicar).
