# SB Itália: estrutura de conjuntos pela lógica Andromeda (16/10/2026)

- **Frente:** Infoproduto. É um funil digital: anúncio → oração ao vivo → checkout.
- **Mercado:** Itália (EUR). A conta é a CONTA 01 (SAN BENITO), em USD.
- **Lote:** 9 vídeos IT em `Downloads/SB-IT-OFERTA-LIVE/PARA-SUBIR/`.
- **Referência de custo:** a Itália ainda não tem dado. Usei o FR dos últimos 14 dias até 15/10: custo/compra US$ 12,91 e ROAS 3,21.

## Auditoria do lote
- **Aberturas:** o `aberturas.py` não achou nenhum par parecido acima de 0,85 (grade em `SB-IT-OFERTA-LIVE/_andromeda/`).
- **Famílias de mensagem:** 5. A meta é ≥ 4 famílias.

| Família | Criativos | Mensagem | Formato / voz |
|---|---|---|---|
| A · PERDA | ADS 12.18, ADS 12.1 GD, ADS 12 | "Se mi ignori… darò il miracolo a qualcun altro" + oração perdida da Bíblia | Jesus falando (lipsync), ~30 s, voz Jesus. **Mesmo roteiro nos 3**: o Meta tende a tratá-los como um anúncio só. |
| B · PREGHIERA PERDUTA | JESU V07, OP2 ASCENSAO | "Se chiudi questo video…" + oração perdida de San Benedetto | Jesus (Getsêmani/coroa) com b-roll, ~27–31 s. Mesmo roteiro, visuais diferentes. |
| C · LETTERA DI GESÙ | ADS 9 | "Figlio mio, mi ignori da tanto tempo…", sinais e mensagens | Jesus falando, longo (1:43), termina na live |
| D · ANGELO / BENEDIZIONE | ADS 7 | Anjo da guarda + bênção financeira | Anjo em close, 25 s, voz Brian |
| E · ULTIMO AVVISO | ADS 6, ADS 20 | "Ultimo avviso", Dio ti ha fermato qui | Narrador Brian, longo (2:19–2:27). O ADS 20 abre com Jesus. |

## Lacunas
- **Persona:** só uma, a pessoa de fé em crise ou com sensação de abandono. Não há persona específica (mãe, idoso, dívida, doença).
- **Formato:** tudo é vídeo, sem estático nem carrossel.
- **Nível de consciência:** quase todos ficam em inconsciente/problema. O ADS 7 é o único com desejo concreto (dinheiro).

## Estrutura recomendada
**Campanha:** `SB [ITA] [EUR] ITALIA | LIVE`. Objetivo Vendas, com o mesmo pixel e evento das campanhas FR.
- **Orçamento:** por conjunto (ABO) na fase de teste. Com CBO, a verba iria para 1 família e as outras não seriam lidas.

**Conjuntos:** um por família, porque cada família é um conceito.

| Conjunto | Anúncios | Prioridade |
|---|---|---|
| `IT · C LETTERA` | 01_ADS-9 | 1. É o melhor da conta no FR. |
| `IT · D ANGELO` | 02_ADS-7 | 2. É o 2º melhor no FR nos 14 dias. |
| `IT · B PREGHIERA PERDUTA` | 03_JESU-V07, 09_OP2-ASCENSAO | 3 |
| `IT · A PERDA` | 04_ADS-12.18, 05_ADS-12.1-GD, 08_ADS-12 | 4. Os 3 competem entre si dentro do conjunto. |
| `IT · E ULTIMO AVVISO` | 06_ADS-6, 07_ADS-20 | 5. Venderam no passado e estão fracos nos últimos 14 dias. |

**Verba e regras (base: custo/compra do FR, US$ 12,91):**
- **Verba por conjunto:** ≥ 3× o CPA, ~US$ 40/dia. Com os 5 conjuntos, são ~US$ 200/dia.
- **Versão enxuta (~US$ 120/dia):** só C, D e B. A e E entram na 2ª semana.
- **Corte:** o conjunto que gastar 2× o CPA (~US$ 26) sem compra, ou ficar 7 dias sem compra.
- **Julgamento:** o conjunto antes do anúncio, em blocos de 7 dias.
- **Escala:** depois de ≥ 4 vencedores diferentes, consolidar numa CBO com +10–20% a cada 3–4 dias.
- **Nome do anúncio:** `IT_<família>_<nº>_<criativo>` (ex.: `IT_C-LETTERA_01_ADS-9`), para depois ler o resultado por família.
- **Em cada conjunto:** só Itália, público aberto (Advantage+), idioma italiano, mesma faixa de idade do FR e posicionamento Advantage+.
