# Briefing: subir os vencedores San Benito FR por persona (Meta Ads)

Este documento é para o Claude com o conector Meta Ads. **Conta: CONTA 01 (SAN BENITO), `1929332567965953`, em USD.**

**Crie tudo PAUSADO.** Mostre o resumo e só ative quando a pessoa disser «ativar». Não pause nem altere as campanhas que já estão rodando.

## Por que separar por persona
Os 5 vencedores falam com 3 pessoas diferentes. Com um conjunto por persona, dá para ver qual público compra mais barato e escalar só ele.

Dados de todo o período da conta, somando todas as campanhas FR, até 16/10/2026:

| Persona | Criativo | Compras | CPA | ID de anúncio de referência (para copiar texto, link e pixel) |
|---|---|---|---|---|
| **P1 · APPEL DIVIN**: quem sente que Deus o chamou, ignorou os sinais e tem caminhos bloqueados | **AD 9 FR** | 51 | US$ 6,96 | `120248711149360259` |
| | SB-FR-OP2-ASCENSAO | 14 | US$ 17,76 | `120248746361180259` |
| **P2 · PROSPÉRITÉ / ARGENT**: quem quer bênção financeira e está endividado | **AD 7 FR** | 56 | US$ 11,78 | `120248710471030259` |
| | AD 6 FR | 17 | US$ 26,28 | `120248710471420259` |
| **P3 · HISTOIRE / ÉCHEC**: dono de negócio que fracassou e tem vergonha em casa (história em 1ª pessoa) | 01_SB-FR_MEDALLA | 2 | US$ 25,49 (subiu em 15/10, ainda em teste) | `120248763254010259` |

## Estrutura
- **Campanha:** `SB [FRA] [EUR] PERSONAS VENCEDORES - <DD/MM> - CBO 1-3-5 - BID 50`
  - Mesmo padrão das campanhas que funcionam: objetivo **Vendas**, evento **Purchase**, CBO.
  - **Lance:** limite de lance (bid cap) de US$ 50, como a FRANCOFONIA de 11/10, que é a melhor campanha (CPA US$ 9,35).
  - **Orçamento:** [PENDENTE — a pessoa define].
- **Conjuntos:**
  - `P1_APPEL-DIVIN` (2 anúncios)
  - `P2_PROSPERITE-ARGENT` (2 anúncios)
  - `P3_HISTOIRE-ECHEC` (1 anúncio)
- **Segmentação** dos 3 conjuntos: **igual à do conjunto da campanha `SB [FRA] [EUR] FRANCOFONIA - 11/10`** (id `120248710462620259`). Copie países, idioma, idade e posicionamentos de lá. Não use interesses.

## Anúncios
Para cada anúncio da tabela:
- **Use o mesmo vídeo** do anúncio de referência (`video_id` do criativo dele) ou suba o arquivo da pasta da persona: `C:/Users/PICHAU/Downloads/SB-FR-VENCEDORES/<persona>/`.
- **Texto principal, título, link de destino, botão (LEARN_MORE / «En savoir plus») e pixel:** copie **exatamente** do anúncio de referência. É a copy que vendeu; não reescreva.
- **Nome do anúncio:** `<PERSONA>_<CRIATIVO>`, por exemplo `P1_AD-9-FR`.

**Atenção:** o AD 9 FR aparece como «WITH_ISSUES» em duas campanhas (`120248744602600259` e `120248725812990259`). Antes de subir, verifique o motivo em `ads_get_errors` e use o criativo da versão que está ACTIVE (`120248711149360259`).

## Depois de subir
Leia em blocos de 7 dias, primeiro **por conjunto (persona)** e depois por anúncio.
- **Escala:** a persona com CPA abaixo de US$ 12 por 3 dias ganha +20% de orçamento.
- **Corte:** anúncio que gastar 2× o CPA-alvo (~US$ 25) sem compra é pausado.
