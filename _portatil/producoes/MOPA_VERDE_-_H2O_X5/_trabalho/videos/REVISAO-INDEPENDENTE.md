# Revisão independente: vídeos H2O X5 ES-LATAM (08/10/2026)

Revisor independente: não produzi estes vídeos. Não fiz nenhuma chamada paga, não abri players e não li arquivos `.env`. Formei as conclusões **antes** de ler os relatórios A, B e C.

## Como revisei
- **Fala:** faster-whisper small, em `es` e em `en`, com tempo por palavra, nos 15 vídeos.
- **Brand e residual:**
  - whisper `en` também nas trilhas de fundo `_trabalho\audio\<id>_no_vocals.wav`, que ficam por baixo da narração;
  - recortes só da marca, para conferir como ela soa.
- **Imagem:**
  - folha a 2 qps de cada ES e folha a 1 qps de cada original;
  - quadro a quadro (30 qps) em cada troca de caixa e corte suspeito;
  - recortes em resolução cheia das faixas de legenda (4 qps) e das caixas de título;
  - detector automático de quadro solto (1 e 2 quadros) no ES e no original;
  - `blackdetect`.
- **Áudio:**
  - `ebur128` (LUFS integrado e true peak) e `astats`;
  - `silencedetect` a -40 dB/0,7 s e a -35 dB/0,5 s;
  - salto de pts por `packet=pts_time`;
  - nível da trilha nas pausas da narração.
- **Pares:** correlação cruzada do áudio dos pares (defasagem por janela), comparação palavra a palavra do whisper e diff dos `prep.json`/`spec.json`.
- **Kit:** `revisar_ad.py` (PowerShell) rodado de novo nos arquivos que corrigi.

## Veredito por vídeo

| Vídeo | Veredito | Achados (com tempo) |
|---|---|---|
| **07** (9:16) | **APROVADO** com aviso | A fala bate com a legenda, e o CTA falado vai de 24,9 a 26,6 s. O card "Haz clic en Más información" entra em 25 s, com setas a partir de 26 s. Sem inglês na fala, nem no fundo. Áudio: -15,3 LUFS, TP -1,2. Sem silêncio, sem salto de pts e sem quadro preto. **Aviso:** de 20,17 a 20,27 s (4 quadros), "¡Solo vapor y un paño!" e "¡Mira qué limpio!" aparecem juntos. O fade do original faz o mesmo, então é aceitável. O artigo científico em inglês (0–3,6 s) é textura de cena, como o estudo previa. |
| **60** (4:5, par do 07) | **AVISO** | Texto, voz e trilha são os mesmos do 07, mas o **tempo da narração não é igual**. A fala vem **+0,6 s** depois no gancho (começa em 0,7 s em vez de 0,1 s) e +0,4–0,5 s entre 4 e 16 s; volta a bater a partir de ~17 s. Efeito: "…te están enfermando?" termina em 3,86 s, já em cima da cena ANTES/DESPUÉS (a caixa do gancho sai em 3,48 s). O produtor fez isso de propósito (`prep.json`: narração em 0,7/4,12/8,78/16,88 contra 0,1/3,65/8,4/16,75 no 07, para o pop da legenda não cair no "falso corte" de 0,33 s). Fora isso está OK: -15,1 LUFS e CTA presente. |
| **08** (1:1, música) | **CORRIGIDO → APROVADO** | Achei 3 defeitos e corrigi os 3:<br>(a) **2,12–2,20 s**: a caixa "5 EN 1 / SISTEMA DE LIMPIEZA" entrava **3 quadros antes do corte**, por cima do logo "H2OX5" e do "Presentamos";<br>(b) **18,82–18,89 s**: a caixa "CAMBIA TU FORMA" seguia por baixo de "CON EL PODER" e aparecia como degrau escuro em cima dela. Em 17,05 s, "CAMBIA…" também entrava 1 quadro antes do corte, porque a conversão 29,97→30 qps desloca 1 quadro depois de ~15,5 s;<br>(c) em **21,10–21,16 s**, "CON EL PODER DEL VAPOR" ficava 2 quadros por cima da cena final, e o CTA entrava atrasado. Ainda no 08, o **áudio estava em -10,0 LUFS e +0,1 dBTP**, fora da faixa de -16 a -12 (o original já era -9,9). Depois da correção: -13,8 LUFS e TP -3,1. Sem inglês na tela; as caixas cobrem tudo. A mopa vermelha em 17–18,9 s fica, como decidido. |
| **10** (4:5, música) | **APROVADO** | A faixa "LIMPIADOR A VAPOR H2O X5" cobre o texto original o tempo todo. CTA e setas a partir de 5,0 s. -14,2 LUFS, TP -2,9. O whisper só ouve música. |
| **15** (4:5, par do 10) | **APROVADO** | O vídeo é idêntico ao 10 (correlação do áudio 0,99, defasagem 0). -14,1 LUFS. |
| **16** (4:5, par do 32) | **APROVADO** com aviso | A fala bate com a legenda e o CTA falado vai de 16,26 a 17,76 s. A faixa preta cobre toda a legenda em inglês; conferi em 4 qps, em resolução cheia. -15,2 LUFS. **Avisos:** quadro congelado de ~2,4 s no fim (permitido pelo briefing); o whisper ouve a marca como "H2 su X5" (ver pronúncia abaixo). |
| **17** (9:16, música cantada) | **APROVADO** com aviso | A música em inglês fica por decisão da dona. As caixas trocam no quadro exato de cada corte; conferi pelos números de quadro 90, 126, 172, 197, 273 e 354. CTA a partir de 10,0 s. -14,3 LUFS. **Aviso:** o selo grande fica **no centro da tela** (y≈720) e cobre parte do produto em 0–2,5 s e 5,5–6,5 s. É escolha de layout, não defeito, mas destoa dos outros 9:16. |
| **21** (4:5, par do 54) | **CORRIGIDO → APROVADO** | Áudio com **true peak +1,2 dBTP** e pico de amostra +0,54 dBFS (clip), herdado do original, que chega a +2,6. Normalizei para -14,0 LUFS, com TP de -0,7. O "quadro solto" que o kit aponta em 7,67/7,73 s é um quadro de movimento borrado do original (25→30 qps); não é defeito da edição. **Aviso:** selo no centro (y 445 de 900), logo abaixo da caixa. |
| **24** (9:16) | **APROVADO** com aviso | A fala bate com a legenda e o CTA falado vai de 19,12 a 20,86 s. Faixa e caixas cobrem todo o inglês. -15,9 LUFS, TP -0,8. **Avisos:**<br>- a trilha é baixa (-37 dB nas pausas), no mesmo nível do fundo separado do original (-36 dB), então não é defeito;<br>- quadro congelado de ~2,1 s no fim;<br>- o selo grande no topo encosta no produto em alguns planos;<br>- a alegação "seguro con niños y mascotas" fica por decisão da dona. |
| **25** (9:16) | **APROVADO** com aviso | A fala bate com a legenda e o CTA falado vai de 19,28 a 20,62 s. A máquina de lavar em 17,8–18,3 s é do original; não é quadro solto. -15,3 LUFS. **Avisos:**<br>- "No puedo creer que **no compré**…" soa coloquial; o neutro seria "que no haya comprado". Fica como sugestão, não mudei a voz;<br>- quadro congelado de ~2 s no fim. |
| **31** (4:5, par do 46) | **APROVADO** com aviso | É um recorte do 46: áudio idêntico (correlação 1,0) e mesmo texto e tempo. -15,4 LUFS. Avisos: os mesmos do 46. |
| **32** (9:16) | **APROVADO** com aviso | O whisper lê "Me encanta el H2O X5". Setas abaixo da faixa. -15,1 LUFS. **Aviso:** de ~9,5 a 11 s, a fala "azulejos, vidrios" cai sobre a cena da roupa. É defasagem natural da narração nova, aceitável. |
| **44** (1:1, sem som) | **APROVADO** com aviso | O 1º quadro com a lista completa é igual ao do original (quadro de capa), então não é quadro solto. Botão "Haz clic en Más información" com setas a partir de 1,0 s. Sem "Shop now". A faixa de áudio é silenciosa, porque o original não tem áudio. **Aviso:** diz "14 MILLONES VENDIDOS", e o 08 diz "VENDIDAS". Padronize (sugiro "vendidos", que concorda com "millones"). |
| **46** (9:16) | **APROVADO** com aviso | A fala bate com a legenda, e a legenda "SIN / QUÍMICOS / AGRESIVOS" está completa em 15,0–16,2 s. CTA falado de 22,82 a 24,18 s. -15,4 LUFS. **Avisos:**<br>- o selo grande (y≈300) cobre parte da caixa do produto em 3,5–4,5 s e o cabo em 8–9 s;<br>- o whisper ouve a marca como "H2O **XC5**": conferir de ouvido se a voz diz "equis cinco" limpo. |
| **54** (9:16) | **CORRIGIDO → APROVADO** | Mesmo clip de áudio do 21 (TP +1,2 dBTP). Normalizei para -14,0 LUFS, com TP de -0,8. O `revisar_ad.py` deu OK depois da correção. **Aviso:** selo no centro (y≈600), logo abaixo da caixa; encosta no produto em 0–1 s. |

Em todos:
- **Termos proibidos:** nenhum (FBX5, USA, UK, Canada, Shop now, código, cuotas, envío desde) e nenhum parcelamento.
- **Imagem:** nenhum quadro preto, nenhum salto de pts e nenhum quadro solto criado pela edição.
- **Fala antiga:** nenhuma em inglês sob a narração. O whisper `en` nos fundos `no_vocals` só devolve "Music"/"You", com no_speech de ~0,5.
- **Fim dos narrados:** a cauda abaixo de -35 dB tem ≤0,6 s.

## Pares
| Par | Texto | Tempo | Observação |
|---|---|---|---|
| 07 / 60 | igual | **diferente** (+0,6 s no gancho, +0,4–0,5 s até 16 s) | Proposital (produtor A). Ver aviso acima. Para ficar idêntico, use no 60 as posições de frase do 07 menos 0,08 s e monte de novo. Não tem custo, mas a mudança é de montagem e preferi não fazer. |
| 32 / 16 | igual | igual (defasagem 0, correlação 0,96–0,999) | OK |
| 46 / 31 | igual | igual (correlação 1,0) | OK |
| 54 / 21 | igual | igual (correlação 1,0) | OK. As caixas trocam em 4,87/4,88 s, diferença de ≤1 quadro. |
| 10 / 15 | igual | igual (correlação 0,99) | OK |

## Pronúncia da marca "H2O X5"
| Vídeo | Whisper es (frase) | Whisper (só o trecho da marca) | Duração da marca / sílabas estimadas |
|---|---|---|---|
| 07 / 60 | "H2O-X5" / "H2O X5" | "el H2O X5" | 1,66 s / ~6 |
| 32 / 16 | "H2O X5" / "H2 su X5" | "H2OX5" (en: "H2 or X5") | 1,08 s / ~6 |
| 24 | "H2O-X5" | "H2O-X5" | 1,58 s / ~6 |
| 25 | "H2O X5" | "H2OX5" | 1,48 s / ~7 |
| 46 / 31 | "H2O XC5" | "el H2O XC5" | 1,42 s / ~8 |

- **Nenhum narrado soa em inglês.** O whisper `en` não reconheceu "aitch two oh" sem um prompt forçado. As durações e o número de sílabas são compatíveis com a leitura em espanhol ("hache dos o equis cinco"), igual à do 32/16, que foi regravado com esse texto.
- A diferença está no **ritmo**: o 32/16 é rápido (1,08 s) e engole o "o" (daí "H2 su"), e o 46/31 sai como "XC5".
- **Recomendação:** padronizar **"hache dos o equis cinco"** e escrever assim no texto do TTS em gravações futuras. Ouvir o 46/31 e o 32/16; regravar só a frase da marca, se ela soar truncada. Isso é pago e não fiz.

## Correções que fiz (sem chamada paga, sem mexer em roteiro nem voz)
1. **08:**
   - em `_trabalho\videos\08\spec.json`, mudei os tempos de 4 camadas para casar com os cortes reais da saída. Os cortes originais caem nos quadros 66 e 511/564/632; na saída a 30 qps, os três últimos viram 512/565/633:
     - "5 EN 1": `de` 2,12 → 2,2022;
     - "VAPORIZADOR DE ROPA": `ate` 17,05 → 17,084;
     - "CAMBIA TU FORMA": 17,05–18,92 → 17,084–18,852;
     - "CON EL PODER": 18,819–21,19 → 18,852–21,12;
     - CTA: `de` 21,19 → 21,12;
   - montei de novo com `_C\compor.py` e passei `loudnorm` (I -14, TP -1,5) só no áudio, com `-c:v copy`, cortando o áudio na duração do vídeo;
   - conferi quadro a quadro em 2,13–2,27, 16,98–17,13, 18,75–18,92 e 21,03–21,20 s: todas as trocas caem no quadro do corte, sem sobreposição;
   - resultado: -13,8 LUFS, TP -3,1;
   - o `revisar_ad.py` só aponta a resolução 720x720 (falso positivo esperado).
2. **21 e 54:** passei `loudnorm` (I -14, TP -1,5) só no áudio, com `-c:v copy`, cortando o áudio na duração do vídeo. Resultado: -14,0 LUFS, TP -0,7/-0,8, sem clip. `revisar_ad.py`: o 54 deu OK; no 21 só sobram a resolução e o falso "quadro solto" do original.
3. **Backups** (os arquivos anteriores foram preservados):
   - `_trabalho\videos\08\_backup_revisao\` (`spec.json` e `08 AD - ES.orig.mp4`);
   - `_trabalho\videos\21\_backup_revisao\`;
   - `_trabalho\videos\54\_backup_revisao\`.

## Pendências para a pessoa decidir
1. **07/60:** igualar o tempo da narração do 60 ao do 07 (remontagem sem custo) ou aceitar a defasagem de até 0,6 s.
2. **Selo grande no meio da tela** no 17, 21 e 54 (e grande no topo no 24/46/31), contra o selo compacto no 07/60/16/32/25 e no canto no 08/10/15/44. Padronizar se a consistência visual entre os criativos importar.
3. **"vendidas" × "vendidos":** 08 contra 44.
4. **Ouvir a marca** no 46/31 ("XC5") e no 32/16 (rápido).
5. **Compliance (alegações mantidas por decisão):**
   - "te están enfermando" e "certificado en laboratorio" (07/60);
   - "seguro con niños y mascotas" (24).
