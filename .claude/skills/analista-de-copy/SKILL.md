---
name: analista-de-copy
description: Analisa a COPY dos criativos de vídeo (roteiro falado, texto na tela e texto do anúncio) em dois modos — antes de subir (revisão crítica com nota por critério e reescritas) e depois de rodar (cruza métricas por anúncio com a frase exata de cada trecho e conclui o que funciona) — e alimenta o banco de copy da operação. Use quando a pessoa pedir para analisar copy, roteiro, gancho ou texto de anúncio, perguntar "o que deu certo / o que não deu", "por que esse anúncio performou", "revisa a copy antes de subir", ou quando um lote de criativos estiver pronto para veicular ou já tiver dias de dados.
---

# Analista de copy

Fecha o ciclo copy → resultado → próxima copy. Não duplica outras skills:
- problema que não é de texto (edição, página, oferta, público) → aponte e indique `diagnostico-criativo`;
- escrever o próximo lote → entregue os aprendizados para `estrategista-criativo` / `esteira-de-hook`.

## 0. Contexto (sempre)
- Leia `contexto/banco-de-copy.md` (padrões já validados e reprovados) e `contexto/estrategias-criativos.md`.
- Identifique frente (COD / Infoproduto / X1), mercado, idioma, oferta e público. Nunca misture lógicas entre frentes.
- Reúna a copy de cada criativo pela fonte de verdade, não de memória:
  - roteiro do projeto (json/md de roteiro, textos de legenda);
  - texto na tela (títulos, selos, CTA final);
  - texto do anúncio (primary text e títulos).
  Se faltar, transcreva o vídeo (whisper em CPU) e marque como "transcrito".
- A chave de ligação é o **nome do anúncio = nome do arquivo** (ex.: `PRODUTO_H3_musica`). Sem esse padrão, o modo 2 não liga métrica a texto; avise.

## Modo 1 — Antes de subir (sem custo)
Para cada criativo, avalie de 0 a 5 com uma frase de justificativa:
1. **Gancho (0–3 s):** para quem é, curiosidade, tensão ou benefício. Está claro sem som (texto na tela)?
2. **Oferta:** mecânica entendida em uma frase? Aparece até ~8 s?
3. **Concretude:** benefício e sensação concretos em vez de adjetivo vazio; prova (demonstração, detalhe, uso).
4. **Fluxo:** cada frase puxa a próxima; o gancho promete o que o corpo entrega; sem repetição.
5. **CTA:** ação única e clara, com remoção de risco (ex.: paga ao receber) quando for o caso.
6. **Linguagem do mercado:** naturalidade no idioma/país; palavras que IA de voz pronuncia mal ou confunde com outro idioma (sinalize).
7. **Compliance:** promessa, escassez sem dado, depoimento encenado, marca de terceiros, preço comparativo. **Liste os riscos e pergunte; não suavize sozinho.**
8. **Coerência texto × tela × anúncio:** a mesma oferta e o mesmo tom nos três.

Saída: tabela criativo × critério, os 3 pontos mais fortes e os 3 mais fracos do lote, e até 2 reescritas por criativo fraco (só o trecho, não o roteiro inteiro). Diga qual criativo você apostaria e por quê, como hipótese a validar.
Se o lote tiver muitos criativos, use um agente por criativo em paralelo, com os critérios acima e a mesma escala.

## Modo 2 — Depois de rodar (com dados)
1. **Dados por anúncio** pelo conector de anúncios (ex.: Meta Ads), no período combinado:
   - gasto, impressões, CPM;
   - hook rate (visualizações de 3 s ÷ impressões);
   - retenção (ThruPlay ou 15 s, 25/50/75/95%);
   - CTR no link, CPC, compras e CPA.
   - Na frente COD, a efetividade de entrega por anúncio vem da fonte operacional (UTM/plataforma), seguindo as regras de efetividade em `contexto/`/memória.
   - Sem dado, diga a limitação; **nunca invente métrica**.
2. **Amostra mínima:** não conclua sobre anúncio com gasto < ~1× o CPA alvo ou < ~1.000 impressões. Marque como "inconclusivo".
3. **Cruzamento:**
   - Hook rate é efeito dos 3 primeiros segundos de texto e imagem.
   - A queda de retenção cai na frase que estava sendo dita naquele segundo; use o roteiro com os tempos (arquivo de legenda/alinhamento).
   - CTR e CPA são efeito do corpo, da oferta e do CTA.
   - Compare criativos que diferem em UMA variável (mesmo corpo, ganchos diferentes; mesmo gancho, músicas diferentes). Diferença com variável misturada fica como hipótese, não conclusão.
4. **Conclusões** no formato: padrão → evidência (anúncios e números) → confiança (alta/média/baixa) → ação (repetir, testar de novo, abandonar).
5. **Próximo passo:** 3–5 ideias de gancho/copy derivadas dos vencedores, para o próximo lote.

## Registrar
Acrescente em `contexto/banco-de-copy.md`, na seção do mercado e da frente:
- padrões validados e reprovados, com data, anúncios de origem e confiança;
- as frases exatas que venceram (gancho, oferta, CTA);
- palavras e construções a evitar (pronúncia, compliance, baixa retenção).
Só fatos observados. Atualize a confiança quando um teste novo confirmar ou contradizer.
Com análise longa, publique um relatório (página ou PDF) em `02-relatorios/`, no padrão de nomes do projeto.
