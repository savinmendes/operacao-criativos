# Linfarele IT: 124 imagens a partir dos ângulos da Erlona

> Lote de anúncios de imagem em italiano para a Linfarele (drenagem linfática, Itália), criados a partir dos ângulos da concorrente Erlona. Abra ao gerar mais imagens Linfarele ou ao repetir o método "ângulo do concorrente → imagem própria".

## Contexto de uso
- **Frente:** e-commerce com cartão na Itália (sem COD). Marca **Linfarele**: gotas com 4 ervas (galio, stillingia, trifoglio rosso, frassino spinoso), poucas gotas sob a língua, sabor de mel.
- **Entregue em 07/10/2026.**
- **Pasta:** `Downloads\ERLONA-REFERENCIA-2026-10-07\` (atalho `entregas-linfarele-imagens/` → `linfarele-it\`).
  - Entrada: export da Biblioteca do Meta da Erlona (125 anúncios de imagem IT/FR em `criativos\` + `conceitos.json` + `textos-criativos-2026-10-07.csv`). O 192 é Elettronew e ficou fora.
  - Saída: `linfarele-it\imagens\LC001–LC124.jpg`, `textos\*.json`, `00-TESTI-ANNUNCI-LINFARELE-IT.csv/.txt`, `00-folha-imagens.jpg`.
  - Briefing dos agentes: `BRIEFING-AGENTES.md`.
- **Ferramenta e custo:** Flora, projeto `prj_ns73srpqeednwwk30jzwzxfkgs8ftzsn`, Nano Banana 2, ~US$ 10,37 (144 gerações).
- **Decisões da pessoa:**
  - imagem **sem frasco nem produto** (como a Erlona faz), só cena + texto;
  - concorrente serve só de ângulo: nunca copiar imagem nem texto, e não subir a imagem deles no Flora (gerar do zero).
- **Oferta usada:** spedizione gratuita + 90 giorni di garanzia (soddisfatti o rimborsati), CTA "Acquista ora", sem preço.
- **Pendência:** confirmar no site se o frete grátis e os 90 dias valem (a mesma dúvida do lote de vídeos Linfarele) — precisa de revisão manual.

## Lógica de uso
1. Exportar os anúncios da concorrente e montar um `conceitos.json` (id, imagem de referência, texto, gancho, título, idioma).
2. Dividir os conceitos entre agentes. Para cada conceito: ler a imagem e o texto de referência, extrair o ângulo (quem fala, dor, virada, emoção) e gerar **1 imagem nova** (text-to-image) + título, texto principal e descrição em italiano específicos daquela imagem.
3. **Regras de imagem (saúde/aparência no Meta):**
   - proibido: antes/depois, close de celulite/barriga/pernas inchadas, corpo de lingerie em foco, balança com número, fita métrica, exames/órgãos, remédios, médico segurando produto, promessa na imagem ("-9 kg");
   - permitido: só o "depois" positivo (mulher 40–60 vestida, leve), objeto como prova (aliança, sapato, jeans que fecha), cena da dor sem corpo;
   - profissionais de saúde viram fisioterapeuta/osteopata "explicando".
4. Como a imagem não mostra o produto, o texto nunca diz "veja o frasco".
5. Consolidar textos em CSV/TXT e gerar a folha de contato para revisão.
- **Se a pessoa pedir mais:** reaproveitar o mesmo `conceitos.json` em outro idioma/mercado, ou gerar uma segunda execução dos ângulos que performarem.

## Relacionados
- [../04-fluxo-producao-criativos.md](../04-fluxo-producao-criativos.md)
- [lymphoria-adaptacao-ads.md](lymphoria-adaptacao-ads.md) (vídeos Linfarele IT)

## Complemento (13/10/2026): kit de mídia do Instagram LinfaRelè
### Contexto de uso
- Pasta `Downloads\TIKTOK\kit_linfarele_it\`, gerada pelo Minerador em 03/10/2026: `README.md`, `CLAUDE.md` (regras do agente), `REVISAO.md`, `plano/` (perfil, destaques, posts, calendário), `prompts/`, `pesquisa/compilado.md`, `produto/` (fotos originais) e `assets/` (saída).
- Objetivo: montar o perfil orgânico do Instagram da marca (foto, destaques, 9 primeiros posts da grade 3x3, legendas, stories). Se o perfil foi criado/publicado: **precisa de revisão manual**.
### Lógica de uso
- Abrir a pasta no Claude Code e pedir "gere todo o kit de mídia seguindo o CLAUDE.md".
- Regras do kit: todo texto em italiano nativo; público 40+ (letra grande); produto sempre i2i da foto original em `produto/` (sem foto → parar e pedir); sem promessa de cura, detox ou antes/depois; não marcar hora do dia; frames aprovados antes de gerar vídeo (clipes de 5 s); 1 peça revisada antes do lote; depoimento só de cliente real.
- Publicação opcional pela Graph API exige token e ID da conta, guardados só em `.env`.
