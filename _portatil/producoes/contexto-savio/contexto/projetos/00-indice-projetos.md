# Índice de projetos e lotes

> Lista de todos os projetos/lotes registrados, com frente, mercado, data e status. Abra primeiro para achar o arquivo do projeto certo.

## Contexto de uso
Situação em 13/10/2026. Frentes: COD, Infoproduto, X1 After-Pay; "e-com" = loja com cartão fora das três frentes clássicas.

| Projeto | Frente | Mercado | Data | Status | Arquivo |
|---|---|---|---|---|---|
| Lymphoria: adaptação dos ADs Mayaverra (LHYMPORIA AD 01-20) + 5 Linfarele IT | COD (+ e-com IT) | CL, GT, EC (+ Itália) | 03–05/10/2026 | Entregue; v2 corrigidos; v3 opcional pendente | [lymphoria-adaptacao-ads.md](lymphoria-adaptacao-ads.md) |
| Podadora inalámbrica | COD | Chile | 04/10 e 08/10/2026 | Entregue (fase 1 + vencedores + fora da caixa) | [podadora-chile.md](podadora-chile.md) |
| 30 criativos TikTok → Facebook EN (Tarte + Sungboon) | e-com | Países de língua inglesa | 04/10/2026 | Estudo pronto; produção adiada | [tiktok-en-30-criativos.md](tiktok-en-30-criativos.md) |
| Drenagem LATAM (Lymphoria, 55 criativos) | COD | CL, GT, EC | 05/10/2026 | Entregue; 6 validados no TikTok | [drenagem-latam.md](drenagem-latam.md) |
| Wyze Solar Cam Pan 2K EN → ES | COD/e-com (oferta não confirmada) | LATAM | 05/10/2026 | Entregue sem selo; aguarda oferta | [wyze-solar-cam-latam.md](wyze-solar-cam-latam.md) |
| Linfarele IT: 124 imagens (ângulos Erlona) | e-com (cartão) | Itália | 07/10/2026 | Entregue | [linfarele-imagens-erlona.md](linfarele-imagens-erlona.md) |
| Oración ES LATAM (página Keiko Tanaka) | Infoproduto | EUA hispânico + LATAM | 08/10/2026 | Entregue; aguarda produto/oferta e versão Espanha | [oracion-es-latam.md](oracion-es-latam.md) |
| Enzimas digestivas EN-EUA → EN-UK (Physician's Choice) | e-com (frente a confirmar) | Reino Unido | 08/10/2026 | Entregue (5 alterados + 6 sem troca); preço em £ a confirmar | [enzimas-uk.md](enzimas-uk.md) |
| Mopa H2O X5 EN → ES | COD | LATAM | 08/10/2026 | Entregue; ajustes menores pendentes | [mopa-h2o-x5-es.md](mopa-h2o-x5-es.md) |
| DeWalt taladro 20V MAX (DCD7781/DCD7771) | COD | Chile | 09–10/10/2026 | Pronto para subir; kit a confirmar | [dewalt-ads-cl.md](dewalt-ads-cl.md) |
| Yara Kit 3 Black Friday | COD | Chile | 09–10/10/2026 | Teste subido como está; onda 2 entregue | [yara-bf-chile.md](yara-bf-chile.md) |
| Perfumes Lattafa (loja chileverificada) | COD | Chile | 09–10/10/2026 | Pausado; v3 do tema aguarda publicar | [perfumes-lattafa-chile.md](perfumes-lattafa-chile.md) |
| Vitaly → Lymphoria CL (+ lote enxuto) | COD | Chile | 09–10/10/2026 | Entregue; V03/V11 bloqueados | [vitaly-lymphoria-cl.md](vitaly-lymphoria-cl.md) |
| Kit Hombre 3 en 1 (perfumes árabes): matriz Andromeda | COD | Chile | 10/10/2026 | Planejado; aguarda oferta/verba | [kit-hombre-3en1-cl.md](kit-hombre-3en1-cl.md) |
| Pellorini relógios | e-com | Mundo (US, GB, CA, AU no teste) | 10–11/10/2026 | Loja rebrandeada; temas aguardam publicar; pacote de subida pronto | [pellorini-relogios.md](pellorini-relogios.md) |
| San Benito ES: vencedores | Infoproduto | Espanhol (vários países) | 11/10/2026 | Análise entregue | [san-benito-es-vencedores.md](san-benito-es-vencedores.md) |
| San Benito FR (OP2 ASCENSAO + JESU V07) | Infoproduto | Francófonos | 13/10/2026 | Entregue (v2) | [san-benito-fr.md](san-benito-fr.md) |
| SB Reel Medalla ES (esqueleto do reel Sagrado Verso) | Infoproduto | Espanhol | 13/10/2026 | Em produção (roteiro, imagens base e voz prontos) | [sb-reel-medalla-es.md](sb-reel-medalla-es.md) |

- **Ligações entre projetos:** Lymphoria → Drenagem → Vitaly (mesma oferta Lymphoria, os corpos e o CTA validados passam de um para o outro); Yara ↔ Perfumes Lattafa (criativo × loja do mesmo kit); San Benito ES → San Benito FR → SB Reel Medalla ES (mesmo acervo e estilo SB-JESU); Yara/Perfumes ↔ Kit Hombre (mesma loja e projeto Flora); Enzimas UK ↔ Oración (mesmo método de lipsync); Oración ↔ San Benito (mesmo método de lipsync); Podadora → Wyze → Mopa (mesmo fluxo de tradução EN→ES).
- **Fonte:** memórias `project_*.md` do Claude Code + relatórios de cada pasta em `Downloads\`.

## Lógica de uso
Como registrar um projeto novo neste formato:
1. Criar `projetos/<slug>.md` (slug curto, minúsculo, com hífen; ex.: `produto-pais.md`), seguindo `../_MODELO.md`.
2. Título `# <Projeto>` + uma linha `>` dizendo do que trata e quando abrir.
3. **## Contexto de uso** — só fatos: frente (COD/Infoproduto/X1/e-com), produto e oferta, mercado, datas absolutas (DD/MM/AAAA), decisões da pessoa, quantidades entregues, custos reais, IDs úteis (projeto Flora, voz, avatar), pastas de entrega e de trabalho, status e pendências. Lacuna = "precisa de revisão manual".
4. **## Lógica de uso** — só o como: método em passos, scripts e comandos, ordem, o que deu errado e como evitar, o que fazer se a pessoa pedir mais. Nunca misturar com o contexto.
5. **## Relacionados** — links relativos para os temas (`../04-fluxo-producao-criativos.md`, `../05-traducao-de-criativos.md`, `../06-troca-de-marca.md`, `../07-variacoes-gancho-corpo.md`, `../09-lipsync-e-avatar-heygen.md` etc.) e para os projetos ligados.
6. Nunca incluir chaves, tokens, conteúdo de `.env`, dados pessoais ou de pagamento.
7. Acrescentar a linha do projeto na tabela acima e atualizar o status quando ele mudar (entregue, pausado, validado, vencedor).

## Relacionados
- [../_MODELO.md](../_MODELO.md)
- [../04-fluxo-producao-criativos.md](../04-fluxo-producao-criativos.md)
