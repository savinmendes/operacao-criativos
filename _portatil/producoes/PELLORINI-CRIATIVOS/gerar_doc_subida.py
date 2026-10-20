# -*- coding: utf-8 -*-
"""Gera PLANO-DE-SUBIDA.md, LINKS.md, PROMPT-PARA-O-OUTRO-CLAUDE.md e PROMPT-VERIFICACAO-PARA-O-CLAUDE.md
a partir do plano-subida.json (rodar depois do montar_subida.py)."""
import json
import os

PASTA = "SUBIDA-META-150-VENCEDORES"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), PASTA)
CAMINHO = "C:\\Users\\PICHAU\\Downloads\\PELLORINI-CRIATIVOS\\" + PASTA + "\\"
p = json.load(open(os.path.join(OUT, "plano-subida.json"), encoding="utf-8"))
NOMES = {"oferta": "Oferta (BOGO)", "preco": "Preço / status", "qualidade": "Qualidade", "risco": "Risco zero (90 dias)",
         "desejo_h": "Desejo – masculino", "desejo_m": "Desejo – feminino", "presente": "Presente", "escolha": "Escolha (qual você?)"}
V, D, C = p["campanha_vendas"], p["padrao_conjunto"], p["campanha_catalogo"]
NADS = sum(len(cj["anuncios"]) for cj in p["conjuntos"])
NCAR = sum(1 for cj in p["conjuntos"] for a in cj["anuncios"] if a["formato"] == "carrossel")


def bloco_anuncio(ad, a):
    if ad["formato"] == "carrossel":
        a(f"**{ad['nome']}**: **carrossel**, textos do conceito *{NOMES[ad['conceito']]}* (texto principal 1). Card final \"ver mais\": {ad['url']}")
        for c in ad["cards"]:
            a(f"  - `{c['imagem']}` → **{c['titulo']}** · {c['descricao']} · {c['link']}")
        a("")
    else:
        a(f"**{ad['nome']}**: formato flexível, textos do conceito *{NOMES[ad['conceito']]}*\n- Destino: {ad['url']}\n- Imagens ({len(ad['imagens'])}): "
          + ", ".join(f"`{x}`" for x in ad["imagens"]) + "\n")


def textos(a, cab="## Textos por conceito (EN)"):
    a(cab + "\nNo formato flexível, cada anúncio leva todas as variações do seu conceito. No carrossel, só o texto principal 1.\n")
    for k, t in p["textos_por_conceito"].items():
        a(f"### Conceito `{k}`: {NOMES[k]}\n")
        for i, x in enumerate(t["textos"], 1):
            a(f"Texto principal {i}:\n```\n{x}\n```")
        a("Títulos: " + " | ".join(f"`{x}`" for x in t["titulos"]) + "  \nDescrições: " + " | ".join(f"`{x}`" for x in t["descricoes"]) + "\n")


# ---------------- PLANO ----------------
L = []
a = L.append
a("# Plano de subida no Meta: Pellorini (US$ 150/dia)\n")
a("Loja: pellorini.com (mesma loja Shopify da essiora.com) · Mercado: EUA, Reino Unido, Canadá e Austrália · Idioma: inglês · CPA-alvo: US$ 20 · "
  "Oferta: Buy 1 Get 1 Free, frete grátis rastreado, 90 dias para devolver, garantia de 24 meses.\n")
a("**Foco:** os anúncios masculinos e de presente usam os **5 relógios mais vendidos** (Vittorio, Dominante, Milano, Opulent, Maretti). "
  "A linha feminina ainda não tem ranking e usa os modelos com as melhores fotos.\n")
a(f"**Destino:** anúncio com 1 relógio por imagem vira **carrossel** ({NCAR} anúncios), e cada card leva à página daquele relógio. "
  f"Anúncio com vários relógios na mesma imagem (pares BOGO, presente, maleta, \"qual você\") usa o **formato flexível** e vai para a **coleção** ({NADS - NCAR} anúncios).\n")
a("## Resumo do orçamento\n| Campanha | Conjuntos | Orçamento/dia |\n|---|---|---|\n"
  "| PELLORINI · Vendas · BOGO · EN · ABO | 5 conjuntos × US$ 20 | US$ 100 |\n| PELLORINI · Catálogo · BOGO · EN | 1 conjunto | US$ 50 |\n| **Total** | | **US$ 150** |\n")
a("## Campanha 1: Vendas\n")
for k, v in V.items():
    a(f"- **{k}:** {v}")
a("\n**Configuração de cada conjunto (igual nos 5):**\n")
for k, v in D.items():
    a(f"- **{k}:** {', '.join(v) if isinstance(v, list) else v}")
a(f"- **parâmetros de URL (UTM):** `{p['parametros_url']}`\n- **CTA:** Shop Now\n- **Página / Instagram:** os da marca Pellorini\n")
for cj in p["conjuntos"]:
    a(f"### {cj['nome']}: US$ {cj['orcamento_diario_usd']}/dia\n")
    for ad in cj["anuncios"]:
        bloco_anuncio(ad, a)
a("## Campanha 2: Catálogo\n")
for k, v in C.items():
    if k != "textos":
        a(f"- **{k}:** {v}")
a("- **Textos:** os do conceito *Oferta (BOGO)*\n")
textos(a)
a("## Regras de operação\n")
for r in p["regras"]:
    a(f"- {r}")
a("\n## Checagens antes de ativar\n- O pixel recebe `Purchase` com valor (app Facebook & Instagram da Shopify, com API de conversões).\n"
  "- O domínio pellorini.com está verificado no Business Manager.\n- O catálogo está sincronizado e o conjunto 'best-sellers' existe.\n"
  "- O tema \"Dawn - Pellorini (mundo, 90 dias)\" está publicado.\n- A moeda da loja é GBP: se o foco for os EUA, ativar USD no Shopify Markets.\n")
a("## Reserva\n`lote3-vencedores/` (bogo-caixa, cores, detalhes, ranking, estúdio, caixa-mãos em 9:16), `lote2/` e `lote1/`. "
  "Entram em conjunto novo quando algum anúncio for cortado.\n")
open(os.path.join(OUT, "PLANO-DE-SUBIDA.md"), "w", encoding="utf-8").write("\n".join(L))

# ---------------- LINKS ----------------
prods = {}
for cj in p["conjuntos"]:
    for ad in cj["anuncios"]:
        for c in ad.get("cards", []):
            prods[c["titulo"]] = c["link"]
LK = ["# Links: Pellorini (vencedores)\n", "## Coleção (anúncios em formato flexível e card final dos carrosséis)",
      "https://pellorini.com/collections/best-sellers\n", "## Parâmetros de URL", f"`{p['parametros_url']}`\n",
      "## Páginas de produto usadas nos carrosséis", "| Produto | Link |", "|---|---|"]
LK += [f"| {k} | {v} |" for k, v in sorted(prods.items())]
LK += ["\n## Loja", "- Os anúncios usam pellorini.com (mesma loja da essiora.com).",
       "- Prévia do tema Pellorini: https://pellorini.com/collections/best-sellers?preview_theme_id=193568080148",
       "- Publicar antes de ativar: Admin → Loja virtual → Temas → \"Dawn - Pellorini (mundo, 90 dias)\" → Publicar."]
open(os.path.join(OUT, "LINKS.md"), "w", encoding="utf-8").write("\n".join(LK))

# ---------------- PROMPT DE SUBIDA ----------------
PROMPT = f"""Você vai subir no Meta Ads as campanhas da marca de relógios **Pellorini** (loja pellorini.com) usando as ferramentas do Meta Ads. O plano completo já está pronto: execute exatamente o que ele diz e não invente nada que não esteja nele.

## Arquivos (pasta `{CAMINHO}`)
- `plano-subida.json`: a fonte da verdade (campanhas, conjuntos, anúncios, formato, imagens, cards, textos, links, regras).
- `PLANO-DE-SUBIDA.md`: o mesmo, para humano. `LINKS.md`: os links.
- `IMAGENS-PARA-O-GERENCIADOR\\`: as imagens; o nome começa pelo ID do anúncio (`A01__...`). Se você não conseguir ler esta pasta, peça para eu subir as imagens na biblioteca de mídia da conta com os mesmos nomes e mapeie pelo nome.

## Passo a passo
1. Leia o plano inteiro antes de qualquer ação.
2. **Confirme comigo numa mensagem só, antes de criar qualquer coisa:** a conta de anúncios, a Página e o Instagram da **Pellorini**, o pixel da loja pellorini.com (confira `Purchase`) e o catálogo com o conjunto de produtos best-sellers. Se houver dúvida ou mais de uma opção, pergunte.
3. Use as imagens da biblioteca (ou suba-as) e guarde o hash de cada uma pelo nome do arquivo.
4. **Campanha 1: `{V['nome']}`**
   - Objetivo Vendas, orçamento por conjunto (ABO), status **PAUSADO**.
   - 5 conjuntos (CJ1–CJ5), cada um com:
     - US$ {D['orcamento_diario_usd']}/dia;
     - compra no site com o pixel da loja;
     - maior volume, sem limite de custo;
     - 7 dias após o clique ou 1 dia após a visualização;
     - países {', '.join(D['paises'])};
     - 18–65+, todos os gêneros, Advantage+ sem interesses, posicionamentos Advantage+.
   - Anúncios com o nome exato do plano. Siga o campo `formato` de cada um:
     - **`flexivel`**: formato flexível / asset feed, com todas as `imagens` (1:1 e 9:16), todos os `textos_principais`, `titulos` e `descricoes`; link = `url` (a coleção).
     - **`carrossel`**: 1 card por item de `cards`, na ordem, cada um com a própria `imagem`, `titulo`, `descricao` e **`link` (a página daquele relógio)**. Texto principal = `textos_principais[0]`. O link do card final / "ver mais" = `url` (a coleção).
     - Em todos: CTA `SHOP_NOW` e parâmetros de URL = `parametros_url`.
   - Desligue as melhorias do Advantage+ Creative que reescrevem ou geram texto e os efeitos automáticos de imagem.
   - Não troque um carrossel por um anúncio de imagem única com o link da coleção: o motivo do carrossel é cada relógio levar à própria página. Se a API recusar o carrossel, pare e me avise.
5. **Campanha 2: `{C['nome']}`**
   - Anúncio de catálogo (Advantage+ catalog), US$ {C['orcamento_diario_usd']}/dia, **PAUSADA**.
   - 1 conjunto com o mesmo público e a mesma otimização.
   - Anúncio `A21 | C9_catalogo-bogo` com o conjunto best-sellers, os textos do conceito `oferta` e a moldura `A21__moldura-catalogo-bogo.png` (se a conta permitir).
6. **Não ative nada.** Entregue uma tabela com nome, ID e status de cada item, as pendências e qualquer diferença em relação ao plano.
7. Só ative quando eu escrever "pode ativar".

## Regras
- Não altere textos, links, nomes, orçamentos nem países. Se algo for recusado, pare, mostre o erro e pergunte.
- Não crie públicos, regras automáticas nem campanhas extras. Antes de repetir uma criação que falhou, confira pelo nome o que já existe.
"""
open(os.path.join(OUT, "PROMPT-PARA-O-OUTRO-CLAUDE.md"), "w", encoding="utf-8").write(PROMPT)

# ---------------- PROMPT DE VERIFICAÇÃO (autossuficiente) ----------------
Q = []
q = Q.append
q("Você vai **auditar**, sem alterar nada, as campanhas da marca **Pellorini** que já foram criadas na conta do Meta Ads. Use as ferramentas do Meta Ads só para leitura e compare o que existe na conta com o plano abaixo, item por item. O plano inteiro está neste texto: não dependa de nenhum arquivo.\n")
q("## Regras\n- **Não crie, não edite, não ative e não pause nada.**\n- Para cada item, marque ✅ (igual ao plano), ⚠️ (diferente mas aceitável, diga por quê) ou ❌ (errado ou faltando), com o valor esperado × o encontrado.\n- O que não der para verificar pela API: marque \"não verificável\" e diga onde eu confiro no gerenciador.\n")
q("## 1. Pré-requisitos\n- Pixel da loja pellorini.com recebendo `Purchase` com valor nos últimos 7 dias\n- Domínio pellorini.com verificado no Business Manager\n- Página e Instagram dos anúncios = os da **Pellorini**\n- Catálogo conectado, com um conjunto de produtos best-sellers (~45 produtos)\n- Conta de anúncios sem restrição e com pagamento ativo\n")
q(f"## 2. Campanha 1: `{V['nome']}`\n- Objetivo Vendas; orçamento por **conjunto** (ABO); status **PAUSADA**\n- Cada um dos 5 conjuntos: US$ {D['orcamento_diario_usd']}/dia · compra no site com o pixel · maior volume, **sem** limite de custo · 7 dias após o clique ou 1 dia após a visualização · países **{', '.join(D['paises'])}** (nenhum outro) · 18–65+, todos os gêneros · Advantage+ sem interesses · posicionamentos Advantage+ · pausado\n")
q(f"Em todos os anúncios: CTA **SHOP_NOW** · parâmetros de URL = `{p['parametros_url']}` · melhorias de **texto** do Advantage+ Creative desligadas · Página Pellorini.\n")
q("Formatos:\n- **flexível**: todas as imagens listadas (1:1 e 9:16), todas as variações de texto, título e descrição do conceito; link = coleção.\n- **carrossel**: os cards **na ordem**, cada um com a imagem, o título, a descrição e o **link da página do relógio** indicados; texto principal = o texto 1 do conceito; card final \"ver mais\" = coleção. ❌ se algum card apontar para a coleção ou para o relógio errado.\n")
for cj in p["conjuntos"]:
    q(f"### Conjunto `{cj['nome']}`\n")
    for ad in cj["anuncios"]:
        if ad["formato"] == "carrossel":
            q(f"- `{ad['nome']}` · **carrossel** · conceito `{ad['conceito']}` · ver mais: {ad['url']}")
            for i, c in enumerate(ad["cards"], 1):
                q(f"  - card {i}: `{c['imagem']}` · título `{c['titulo']}` · descrição `{c['descricao']}` · link {c['link']}")
        else:
            q(f"- `{ad['nome']}` · **flexível** · conceito `{ad['conceito']}` · link {ad['url']} · {len(ad['imagens'])} imagens: " + ", ".join(ad["imagens"]))
    q("")
q(f"## 3. Campanha 2: `{C['nome']}`\n- Anúncio de catálogo (Advantage+ catalog), US$ {C['orcamento_diario_usd']}/dia, pausada\n- 1 conjunto (`CJ6 | Catálogo | Best Sellers`), com o mesmo público, países, otimização e atribuição\n- Anúncio `A21 | C9_catalogo-bogo`: conjunto best-sellers, textos do conceito `oferta`, SHOP_NOW, moldura `A21__moldura-catalogo-bogo.png` (⚠️ se a conta não permitir)\n")
textos(q, "## 4. Textos esperados (palavra por palavra, com emojis e quebras de linha)")
q(f"## 5. Totais\n- 2 campanhas, 6 conjuntos, {NADS + 1} anúncios ({NCAR} carrosséis + {NADS - NCAR} flexíveis + 1 catálogo), US$ 150/dia no total\n- Nenhum item duplicado ou extra com \"PELLORINI\" no nome\n")
q("## 6. Abra 3 links (1 coleção + 2 páginas de produto)\n- Abrem sem erro em pellorini.com\n- Mostram **Pellorini** (não Pelvini), \"Buy 1 Get 1 Free\", **90 dias** (nenhum \"30-Day\") e entrega **worldwide** (sem \"UK delivery\")\n- Se ainda aparecer UK, 30 dias ou Pelvini, o tema Pellorini não foi publicado: marque ❌ e diga isso\n")
q("## Formato da resposta\n1. Pré-requisitos\n2. Campanhas e conjuntos: esperado × encontrado\n3. Por anúncio: formato, imagens/cards (os que faltam ou estão errados), textos, links, parâmetros de URL, CTA\n4. Resumo ✅/⚠️/❌ e as correções em ordem de prioridade. **Não aplique nenhuma correção**: espere eu pedir.")
open(os.path.join(OUT, "PROMPT-VERIFICACAO-PARA-O-CLAUDE.md"), "w", encoding="utf-8").write("\n".join(Q))
print("ok:", NADS, "anúncios |", NCAR, "carrosséis | prompts, plano e links gerados em", PASTA)
