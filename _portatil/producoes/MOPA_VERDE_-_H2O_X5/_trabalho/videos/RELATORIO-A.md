# Relatório do agente A: vídeos 07, 60, 32, 16 e 25 (H2O X5, ES neutro LATAM, 08/10/2026)

## Entregas (`ES-LATAM\VIDEOS\`)
| Arquivo | Formato | Duração | Base | Voz |
|---|---|---|---|---|
| `07 AD - ES.mp4` | 720x1280 (9:16, mestra) | 28,80 s | 07 | voz_07 |
| `60 AD - ES.mp4` | 720x900 (4:5, par da 07) | 28,70 s | 60 original + narração da 07 | voz_07 |
| `32 AD - ES.mp4` | 720x1280 (9:16, mestra) | 18,70 s (+2,3 s de quadro congelado no fim) | 32 | voz_16 |
| `16 AD - ES.mp4` | 720x900 (4:5, par da 32) | 18,70 s (+2,4 s congelado) | 16 original + narração da 32 | voz_16 |
| `25 AD - ES.mp4` | 720x1280 | 21,50 s (+2,0 s congelado) | 25 | voz_25 |

Todos os arquivos têm H.264 e AAC 48 kHz e ficaram abaixo de 30 MB.

## Vozes (ElevenLabs, Instant Voice Clone)
| Clone | voice_id | Usada em |
|---|---|---|
| MOPA X5 narradora 07 | `D7veSz4mUoXEHTJ4BiI7` | 07 e 60 |
| MOPA X5 narradora 16 | `G8cAfhSwImuQFtP8slqP` | 32 e 16 |
| MOPA X5 narradora 25 | `O7yBra2v5jyiQoDuDLW8` | 25 |

As vozes 16 e 25 foram clonadas separadamente, o lado seguro: não dá para confirmar de ouvido se são a mesma pessoa, e o clone não tem custo.

## Caracteres de TTS: 974 no total (limite: 2.500)
- 07/60: 355 caracteres.
- 32/16: 257 caracteres, mais 38 na regravação da 1ª frase. Na fala original, o whisper ouviu a marca como "I2O X5"; a regravação diz "hache dos o equis cinco" e, na legenda, o texto foi trocado de volta para "H2O X5".
- 25: 324 caracteres.
- Custo aproximado: US$ 0,16.

## Roteiros finais (falados)
**07 / 60**
> ¿Sabías que las bacterias de tu cocina te están enfermando? Esta es tu señal para desinfectar tu cocina con el H2O X5. Sus 1300 watts de vapor supercaliente eliminan el 99 % de bacterias y gérmenes donde preparas la comida. Certificado en laboratorio. Solo vapor y un paño. ¡Mira qué limpio! Sin gérmenes. Me impresionó mucho. Haz clic en Más información.

- Diferença do roteiro do estudo: foi acrescentado "Me impresionó mucho" para acompanhar o card da tela ("Very impressed with this!"). A frase é neutra quanto ao gênero.
- Textos da tela, todos em caixa branca opaca nas mesmas posições:
  - "¿Sabías que las bacterias de tu cocina te están enfermando?"
  - "ANTES ❌" / "DESPUÉS ✅"
  - "¡Esta es tu señal para desinfectar tu cocina con el H2O X5!"
  - "Usa 1300 watts de vapor supercaliente que elimina el 99 % de bacterias y gérmenes donde preparas la comida"
  - "Certificado en laboratorio ✅"
  - "¡Solo vapor y un paño!"
  - "¡Mira qué limpio! Sin gérmenes 🥰"
  - "¡Me impresionó mucho!"
- Tela final (25 s em diante):
  - os 6 cards de avaliação foram traduzidos fielmente, sem inventar, no mesmo lugar e na mesma inclinação dos originais;
  - a faixa vermelha "Get Yours Now / 4000+ ★ / REVIEWS" virou "Haz clic en / Más información / 4000+ ★★★★★ reseñas", que é o CTA escrito;
  - a legenda corrida para antes do CTA para não ficar em cima dos cards;
  - as setas entram na palavra "Más" (25,97 s) e ficam até o fim, embaixo.

**32 / 16**
> Me encanta el H2O X5. No es solo un trapeador: es un sistema completo de limpieza a vapor. Trapeador y vaporizador de mano: limpia pisos, azulejos, vidrios, ropa y más. Solo vapor, sin químicos. Limpieza profunda en cada rincón. Haz clic en Más información.

- Título (0–6 s, caixa branca): "Cinco herramientas de limpieza en un vaporizador liviano y potente".
- A legenda queimada em inglês (palavra por palavra) foi coberta por uma faixa preta opaca, e a legenda nova entra sobre ela.

**25**
> ¡No puedo creer que no compré el H2O X5 antes! Es tan liviano y fácil de mover. Limpio pisos, alfombras, ventanas y hasta ropa con un solo aparato. Cero químicos: el poder del vapor elimina la mugre y desinfecta cada superficie. La verdad, limpiar ahora es más rápido y seguro. ¡Estoy encantada! Haz clic en Más información.

- Caixa verde (0–6,7 s), no mesmo estilo e na mesma cor: "¡Limpia tu casa a fondo en minutos, no en horas!".
- A legenda queimada foi coberta por uma faixa preta opaca, com a legenda nova sobre ela.

**Em todos os vídeos:**
- selo amarelo "PAGO CONTRA ENTREGA" no topo;
- fundo `<id>_no_vocals.wav` + narração nova;
- CTA falado e escrito, com setas vermelhas na palavra "Más".

## Revisão (`revisar_ad.py` pelo PowerShell, whisper es + en, proibidos FBX5/USA/UK/Canada/Shop now/código/cuotas/envío desde)
| Vídeo | RESULTADO | Observações |
|---|---|---|
| 07 | **OK** | O whisper em espanhol bate com o roteiro. O residual em inglês só traduz a fala em ES, sem fala antiga. Sem termos proibidos, quadro solto, silêncio no fim ou salto de pts. |
| 60 | **OK** | Idem. Só passou depois de 2 ajustes: (a) cortei os 0,08 s iniciais do original, que tinham um falso corte de cena; (b) a narração começa em 0,7 s para o "pop" da 1ª legenda não ficar a menos de 0,3 s do salto do artigo em 0,33 s. |
| 32 | **OK** | O whisper agora lê "Me encanta el H2O X5". Setas abaixo da faixa (y 1180–1245 contra a faixa 1065–1108). |
| 16 | **OK** | O original tem um quadro solto em 14,77/14,80 s. Tirei 1 quadro (14,76–14,80 s) para corrigir. |
| 25 | **OK** | Setas acima da faixa (y 930–996 contra a faixa 1133–1174). |

- **Folhas de 1 quadro/s:** `_trabalho\videos\NN\NN AD - ES_revisao.jpg`. Também conferi com zoom as transições de cada caixa (fade-in e fade-out dos textos originais) e as faixas: não sobra texto em inglês na tela. O que aparece em inglês é só o que está impresso no produto ou na cena ("H2O MOP X5" no mop, "IMPORTANT" no reservatório, "BOSCH" no fogão).
- No 07/60, o artigo científico de 0–4 s continua em inglês, como textura de fundo, como o estudo previa.

## Decisões e desvios das ferramentas padrão
- **Prep:** usei uma cópia do `preparar_corpo_traducao.py` (`_A_ferramentas\prep_A.py`) com 3 extensões:
  - resolução livre (para o 720x900);
  - caixa de título com cor de fundo e de texto (para a caixa verde do 25);
  - camadas PNG por tempo, para o selo e a tela de avaliações.
- **Selo:** fica no corpo, numa versão compacta de uma linha, em vez do `selo` da receita. O selo grande do kit não cabia sem cobrir os textos e os cards. No 07/60 o selo sai em 25 s, quando entra a tela de avaliações com o CTA.
- **Montagem 4:5:** as mestras 9:16 foram montadas com o `montar_ad.py` padrão. O 60 e o 16 usaram uma cópia do `montar_ad_rapido.py` (`montar_45_A.py`): espaço 1080x1350 → saída 720x900, legenda de 96 px e setas de 120 px.
- **Revisão 4:5:** o `revisar_45_A.py` é o `revisar_ad.py` aceitando também 720x900. Fora isso, nada muda.
- **Pares 4:5:** foram montados a partir do original 4:5 de cada um, porque o 60 e o 16 não são um recorte do 9:16 (os textos estão em outras posições). Mantêm o mesmo texto, a mesma narração e o mesmo fundo.
- Nenhum arquivo do kit nem nenhum original foi alterado.

## Pendências e revisão manual
1. **Alegações mantidas por decisão da dona:** "Certificado en laboratorio" e "Te están enfermando" (risco de compliance Meta: afirma algo sobre quem vê o anúncio).
2. **Pronúncia da marca:** no 32/16 ficou "hache dos o equis cinco". No 07 e no 25 ficou a pronúncia que o TTS escolheu, e o whisper transcreveu "H2O X5". Vale ouvir para ver se a pronúncia está consistente com a dos outros agentes.
3. **Vozes 16 e 25:** confirmar de ouvido se o clone soa como a narradora original. As amostras eram curtas (15–19 s).
4. **Quadro congelado no fim (2,0–2,4 s) no 32/16/25,** para caber o CTA, como o briefing permite.
5. **Cards do 07/60:** texto pequeno, ilegível no celular como no original. A tradução é fiel e nenhum depoimento foi inventado.

## Arquivos de trabalho
- Em `_trabalho\videos\NN\`:
  - `narr.txt`, `narr.mp3` e o alinhamento;
  - `prep.json`, `corpo.mp4`;
  - `receita.json`;
  - `cards.json` e `avaliacoes.png` (07/60);
  - `*_revisao.txt` e `*_revisao.jpg`, `*_frames.jpg`.
- Ferramentas em `_trabalho\videos\_A_ferramentas\`.
