# Copy antes do teste: Kit 3 Yara, Black Friday (COD Chile)

**Frente:** COD · **Mercado:** Chile, espanhol · **Oferta:** Kit 3 perfumes árabes (Yara, Yara Moi, Yara Elixir), Black Friday "paga 2 lleva 3", sem preço, pago contra entrega, envío gratis · **Público:** feminino (e presente)
**Data:** 09/10/2026 · **Modo:** 1, antes de subir (sem dados de veiculação) · **Skill:** `analista-de-copy`
**Lote:** `Downloads/YARA-CL/entregas/TESTE-7-criativos/` (CJ01–CJ07, música BbY WOW, US$ 14/dia por conjunto)

## 1. O que foi analisado

| Fonte | Arquivo |
|---|---|
| Fala (texto do roteiro) | `producao/edicao/textos_legenda.json`, `producao/roteiro_final.json` |
| Ordem dos trechos por criativo | `producao/edicao/ad_A_final.json`, `ad_C_final.json`, `volume/cfg_H1..H5.json` (gerados por `volume/gerar_configs.py`) |
| Texto na tela | títulos `titulo_abertura.png` e `volume/titulo_H2..H5.png`, rótulos do H5, banner, selo e `cta_final.png` (textos lidos em `gerar_overlays_sem_preco.py` e `gerar_titulos_volume.py`) |
| Tela de fato | quadros de 0–8 s (2 por segundo) e dos últimos 9 s de cada vídeo final, extraídos com ffmpeg |
| Pronúncia | transcrição de cada take de voz com faster-whisper small (CPU). É um **sinal**: confirme de ouvido |
| Anúncio | `TESTE-7-criativos/texto_do_anuncio.txt` |

**O que cada criativo é de fato (0–10 s):**

| Criativo | Tela 0–1,5 s | Fala de abertura | Corpo |
|---|---|---|---|
| CJ01 H1 | Consultora no balcão + "BLACK FRIDAY / PAGA 2 LLEVA 3 / LIQUIDACIÓN" | T1 inteiro: "¡Liquidación total por Black Friday! Llévate los tres Yara muy por debajo del precio del mercado. Hoy pagas dos y el tercero te lo llevas completamente gratis." | AD-C |
| CJ02 H2 | Punch-in na consultora + "BLACK FRIDAY / PAGA 2 / LLEVA 3 / EL TERCERO GRATIS" | "Pagas dos y te llevas los tres." → "Llévate los tres Yara muy por debajo del precio del mercado." | AD-C |
| CJ03 H3 | Close dela cheirando o Yara + "¿YA PROBASTE LOS PERFUMES ÁRABES?" (1,35 s sem fala) | T1 inteiro | AD-C |
| CJ04 H4 | Unboxing real, 9 cortes rápidos + "LIQUIDACIÓN / BLACK FRIDAY / PAGA 2 · LLEVA 3" e depois o selo | T1 inteiro em off sobre as mãos | AD-C |
| CJ05 H5 | 3 closes com rótulo "YARA / YARA MOI / YARA ELIXIR" + "3 PERFUMES ÁRABES / PAGA 2 · LLEVA 3" | T1 inteiro (o começo da fala fica sobre os rótulos) | AD-C |
| CJ06 AD-A | igual ao CJ01 | T1 inteiro | só consultora: T3, T4 (close), T5, T6 (borrifo), T7, T8 (close), T9 "Tres aromas, uno para cada momento", T10 (50,9 s) |
| CJ07 AD-C | igual ao CJ01 | T1 inteiro | consultora + unboxing real narrado (48,1 s) |

> **Achado de desenho de teste:** o CJ01 (H1) e o CJ07 (AD-C) são o mesmo vídeo, com um corte a mais em 1,30 s no CJ01. Os quadros de 0–8 s são iguais e a duração é a mesma (48,13 s). Na prática, o teste tem 6 variações. A diferença entre os dois pode servir de **medida de ruído**: se o CJ01 e o CJ07 derem CPA muito diferente, diferenças desse tamanho entre os outros também são ruído.
> Comparações limpas, com uma variável: **CJ01–CJ05** (só muda o gancho) e **CJ06 × CJ07** (mesmo gancho, só muda o corpo).

## 2. Notas por critério (0–5)

Critérios: 1 Gancho · 2 Oferta · 3 Concretude · 4 Fluxo · 5 CTA · 6 Linguagem do mercado · 7 Compliance (5 = sem risco) · 8 Coerência entre texto, tela e anúncio

| Criativo | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | **Média** |
|---|---|---|---|---|---|---|---|---|---|
| CJ01 H1 oferta + tema | 3 | 5 | 4 | 4 | 4 | 3 | 3 | 5 | **3,88** |
| CJ02 H2 oferta direta | 4 | 5 | 4 | 3 | 4 | 4 | 3 | 5 | **4,00** |
| CJ03 H3 sensorial + pergunta | 4 | 3 | 4 | 3 | 4 | 3 | 3 | 4 | **3,50** |
| CJ04 H4 unboxing real | 4 | 5 | 4 | 4 | 4 | 3 | 3 | 5 | **4,00** |
| CJ05 H5 lista dos nomes | 3 | 5 | 4 | 3 | 4 | 3 | 3 | 5 | **3,75** |
| CJ06 AD-A só consultora | 3 | 5 | 3 | 4 | 4 | 2 | 3 | 5 | **3,63** |
| CJ07 AD-C consultora + unboxing | 3 | 5 | 4 | 4 | 4 | 3 | 3 | 5 | **3,88** |

**Justificativas:**

- **CJ01 / CJ07 (gancho H1)**
  - 1 = 3: a oferta fica clara sem som, mas é um "anúncio de liquidação" genérico, com a consultora parada no plano médio. Não diz para quem é e não traz nenhum elemento novo.
  - 2 = 5: "PAGA 2 LLEVA 3" aparece em 0 s e a fala "hoy pagas dos y el tercero… gratis" entra em ~6–10 s.
  - 3 = 4: o corpo dá notas e ocasião de cada perfume ("para el día a día / para una cita / para la noche") e mostra o unboxing real. Falta prova de uso (borrifo, duração, reação).
  - 4 = 4: gancho, 3 perfumes e CTA seguem em ordem, sem buraco.
  - 5 = 4: uma ação só ("pide"), com "pagas al recibir" e "envío gratis". O "antes que se acabe" é escassez sem dado.
  - 6 = 3: sinais de pronúncia no T1 ("Licudación"), no T5 ("Yaramuyo") e no T10 ("Piede el tuyo").
  - 8 = 5: a oferta e as descrições são as mesmas no vídeo e no anúncio.
- **CJ02 H2**
  - 1 = 4: a oferta é falada e escrita no quadro 1, com punch-in. É o gancho mais direto do lote.
  - 4 = 3: a fala repete "…te llevas los tres." e logo depois "Llévate los tres Yara…" (a repetição aparece na legenda em ~3–4 s).
  - 6 = 4: pula o "Liquidación" mal pronunciado. Ainda tem "Moi" e "Piede".
- **CJ03 H3**
  - 1 = 4: tem movimento, um gesto sensorial e uma pergunta que seleciona quem gosta de perfume árabe.
  - 2 = 3: o título não tem a oferta. A mecânica só é falada em ~9–11 s (o banner do topo, pequeno, diz só "Black Friday · pago contra entrega").
  - 4 = 3: a pergunta "¿ya probaste?" não é respondida (o vídeo vai direto para a liquidação) e a descrição dos aromas só começa em ~16 s.
  - 8 = 4: o anúncio não retoma a pergunta.
- **CJ04 H4**
  - 1 = 4: produto real nas mãos em cortes rápidos, com cara de UGC e menos cara de IA. A oferta está no título e no selo.
  - 3 = 4: o produto real aparece desde 0 s, o que ajuda na confiança do COD.
  - 6 = 3: a fala é o mesmo T1.
- **CJ05 H5**
  - 1 = 3: os nomes só valem para quem já conhece Yara. Para o público frio, "YARA" sozinho não diz nada (o "3 PERFUMES ÁRABES" no rodapé salva parte).
  - 4 = 3: na tela aparece "YARA / YARA MOI / YARA ELIXIR" enquanto a voz diz "¡Liquidación total por Black Friday!". Áudio e tela competem.
- **CJ06 AD-A**
  - 3 = 3: tem a copy mais completa (notas, borrifo e o fecho "Tres aromas, uno para cada momento"), mas nenhum produto real: só a consultora de IA segurando os frascos.
  - 6 = 2: tem todos os takes com problema de pronúncia já registrados no banco de copy: "Orquía" (T4), "frutita / grosilla" (T8), "Jasmini Durasno" (T6), além de T1, T5 e T10. No AD-C essas notas saem pelo TTS clonado ("Orquídea… frutilla, grosella", corretos).
  - 4 = 4: é o maior (50,9 s), com o mesmo rosto o tempo todo.
- **Compliance (todos = 3):** detalhes na seção 6. A comparação de preço sem referência, a escassez sem dado e o "Black Friday" em outubro estão em todos os criativos.

### Texto do anúncio (primary text + 3 títulos)

| Critério | Nota | Justificativa |
|---|---|---|
| Gancho (1ª linha) | 4 | "🖤 BLACK FRIDAY: ¡paga 2 y llévate 3! 🖤" passa a oferta na linha visível antes do "ver más". |
| Concretude | 4 | Um perfil e uma ocasião por perfume, iguais ao vídeo. Falta um motivo para escolher perfume árabe. |
| CTA e risco | 4 | ✅ Pagas al recibir, 🚚 envío gratis e "Pide el tuyo". |
| Público e presente | 2 | Não fala de regalo em nenhuma linha, mas o público inclui presente e a data é de compra de presente. |
| Compliance | 3 | "que todas quieren" (popularidade sem dado) e "quedan pocas unidades" (escassez sem dado). |
| Títulos | 4 | O 1 (oferta) e o 2 (redução de risco) são bons. O 3 repete a oferta: dá para trocar por presente. |

## 3. Pontos fortes do lote
1. **Oferta legível sem som em 0–2 s** em 6 dos 7 criativos (só o H3 não tem), e a mesma oferta aparece no vídeo, no selo, no CTA final e no anúncio. A coerência é alta.
2. **Concretude do corpo:** cada perfume tem nome, perfil em 3 adjetivos, notas reais e ocasião ("Para la noche, cuando quieres que se note que llegaste" é a melhor frase do lote). O AD-C ainda mostra o produto real.
3. **Desenho de teste quase limpo:** 5 ganchos sobre o mesmo corpo e 2 corpos sob o mesmo gancho. O CTA tira o risco ("pagas al recibir y el envío es gratis") em todos.

## 4. Pontos fracos do lote
1. **Pronúncia na fala da IA** em frases que estão em todos os criativos: "Liquidación" (→ "Licudación", sinal no T1), "Yara Moi" (→ "Yaramuyo", T5) e "Pide" (→ "Piede", no CTA, T10). No AD-A ainda entram "Orquía", "frutita", "grosilla" e "Jasmini". A legenda corrige na tela, mas o ouvido do chileno percebe.
2. **Ninguém diz para quem é nem fala de presente.** Nenhum gancho chama a cliente ("si te gustan los perfumes dulces…") nem o comprador de presente. Os ganchos variam a forma (oferta, sensorial, unboxing, lista) e quase não variam o ângulo: 4 dos 5 falam a mesma frase T1.
3. **Variações gastas:** o CJ01 é quase igual ao CJ07, e a escassez e a comparação de preço ("muy por debajo del precio del mercado", "antes que se acabe", "quedan pocas unidades") se apoiam em afirmações sem dado.

## 5. Reescritas (só o trecho, espanhol chileno, sem preço)

| Criativo | Trecho atual | Reescrita | Por quê |
|---|---|---|---|
| **Todos (CTA, T10)** | "¡Pide el tuyo antes que se acabe!" | **"Pídelo hoy y pagas recién cuando te llegue a la casa."** | Tira a escassez sem dado, reforça o pago contra entrega no fim e evita o "Piede". O "recién" soa chileno. |
| CJ02 H2 | "Pagas dos y te llevas los tres. Llévate los tres Yara muy por debajo del precio del mercado." | **"Pagas dos y te llevas los tres. Sí: Yara, Yara Moi y Yara Elixir, por Black Friday."** | Tira a repetição e põe os 3 nomes cedo (com o nome também na tela, por causa do "Moi"). |
| CJ02 H2 (alternativa) | título "EL TERCERO GRATIS" | **"EL TERCERO ES DE REGALO"** | Usa a palavra do ângulo presente sem prometer nada a mais. |
| CJ03 H3 | (sem fala nos 1,35 s) + T1 | **"¿Nunca has probado un perfume árabe? Parte por estos tres: Yara, Yara Moi y Yara Elixir. Y por Black Friday, pagas dos y te llevas los tres."** | Responde a pergunta do gancho e traz a oferta para antes de ~6 s. Como alternativa só de edição, ponha "PAGA 2 · LLEVA 3" no rodapé do título H3. |
| CJ03 H3 (título) | "¿YA PROBASTE LOS PERFUMES ÁRABES?" | **"¿YA PROBASTE LOS PERFUMES ÁRABES?" + faixa "PAGA 2 · LLEVA 3"** | A oferta fica legível sem som desde o quadro 1. |
| CJ05 H5 | voz "¡Liquidación total por Black Friday!" sobre os rótulos | **"Yara… Yara Moi… y Yara Elixir. Tres perfumes árabes, uno para cada momento."** e depois "Por Black Friday, pagas dos y te llevas los tres." | Voz e tela dizem o mesmo nome no mesmo segundo e reaproveitam a melhor frase-resumo do AD-A. |
| CJ06 AD-A | T4 "Orquídea, mandarina y un fondo de vainilla" / T8 "Frutilla, grosella negra, caramelo y vainilla" | **"Floral, con mandarina y un fondo de vainilla."** / **"Frutos rojos, caramelo y vainilla."** | Tira as palavras que a IA pronuncia mal. Alternativa: colar o TTS clonado (que já pronuncia certo) sobre esses trechos. |
| CJ01 H1 (é a quase-duplicata) | gancho H1 | **"¿Buscando regalo? Tres perfumes árabes: uno para tu mamá, uno para tu amiga… y uno para ti. Pagas dos, te llevas los tres."** | Troca uma vaga repetida por um ângulo novo (presente) para o próximo lote. Não refazer agora sem decisão. |
| Anúncio | "Los 3 perfumes Yara que todas quieren" / título 3 | **"3 perfumes árabes, uno para cada momento (y para regalar 🎁)"** / título 3: **"Kit 3 Yara: para ti o para regalar"** | Põe o ângulo presente e tira a afirmação de popularidade. |

Todas as reescritas faladas exigem voz nova (TTS com o clone, custo desprezível) e remontagem. **Nada foi alterado.** É decisão da pessoa.

## 6. Aposta (hipótese a validar, não conclusão)
- **Gancho:** aposto no **CJ04 (H4, unboxing real)**. Ele junta a oferta no quadro 1 (título e selo "PAGA 2 · LLEVA 3"), movimento desde o primeiro corte e produto real nas mãos. É o que tira a cara de IA e dá a confiança que o COD precisa para o cliente aceitar e pagar na entrega. Também é o formato do vencedor de referência ("consultora + unboxing real").
  - Segundo lugar: **CJ02 (H2)**, pela oferta mais direta (melhor CTR/CPA provável). O hook rate dele deve ser menor, porque o quadro 1 é a mesma consultora do H1.
  - O H3 deve ter hook rate bom e CTR pior (a oferta chega tarde).
- **Corpo:** **CJ07 (AD-C) > CJ06 (AD-A)**. O AD-C tem produto real, é 2,8 s mais curto e tem menos palavras mal pronunciadas.
- **Leitura:** CJ01–CJ05 pelo hook rate primeiro (gancho), depois CTR e CPA. CJ06 × CJ07 por retenção 25/50% e CPA. CJ01 × CJ07 como medida de ruído.

## 7. Compliance: perguntas (nada foi suavizado)
1. **"Muy por debajo del precio del mercado"** (falado em todos os 7) é comparação de preço sem referência. Existe um preço de mercado comprovável (print de outras lojas) para sustentar a frase se a Meta ou o SERNAC questionarem? Manter ou suavizar?
2. **"Liquidación total" / "antes que se acabe" / "quedan pocas unidades"**: a liquidação de estoque e o estoque limitado são reais? Se não houver limite, manter ou suavizar?
3. **"Black Friday" em outubro**: a oferta vai durar até a data do Black Friday chileno (fim de novembro)? Usar o nome do evento semanas antes, ou por tempo indeterminado, pode ser lido como promoção enganosa. Manter o tema ou trocar por "pre-Black Friday"?
4. **"Paga 2 lleva 3" / "el tercero es gratis"**: a página mostra o preço unitário de um perfume, de modo que "pagas dos" corresponda a 2× esse preço? Se o kit só existe a preço fechado, o "gratis" pode ser questionado.
5. **Marca de terceiros:** os frascos e caixas mostram "Lattafa", e a copy usa os nomes Yara, Yara Moi e Yara Elixir. Os produtos são originais Lattafa? O letreiro do balcão diz "FRAGANCIAS ÁRABES ORIGINALES": essa afirmação está confirmada pelo fornecedor?
6. **Consultora e loja geradas por IA:** a cena mostra uma loja física ("arabeperfumes", "envíos a todo Chile") e uma "consultora". Essa loja existe? Quer marcar o anúncio como conteúdo feito com IA, ou manter como está?
7. **Envío gratis a todo Chile** (anúncio e banner): vale também para regiões extremas (Aysén, Magallanes, Isla de Pascua)?
8. **Música BbY WOW (trend):** está liberada para uso em anúncio pago (Sound Collection da Meta ou licença)? Música de trend sem licença pode ser silenciada ou o anúncio pode ser reprovado.
9. **"Los 3 perfumes Yara que todas quieren"** (anúncio): afirmação de popularidade sem dado. Manter?

## 8. Próximos passos
1. A pessoa responde as perguntas de compliance (seção 7) e decide se aplica a reescrita do CTA (vale para todos) antes de subir.
2. Ouvir "Liquidación", "Yara Moi" e "Pide" nos vídeos finais. Se o erro se confirmar, trocar só a palavra por TTS clonado (custo ~0).
3. Definir o CPA alvo (está pendente em `ESTRUTURA_CAMPANHA.txt`) para o modo 2 ter régua de amostra mínima.
4. Depois de 48–96 h de dados: rodar o **modo 2** desta skill (hook rate × gancho, retenção × frase, CPA e efetividade de entrega por anúncio via UTM).
5. Próximo lote (para `esteira-de-hook`): testar o ângulo **presente** e o **chamado ao público** ("si te gustan los perfumes dulces…"), que hoje não estão em nenhum criativo.

*Limitações: não há dados de veiculação. As notas são julgamento editorial com a mesma escala para os 7 criativos. Os sinais de pronúncia vêm do whisper small e precisam ser confirmados de ouvido.*
