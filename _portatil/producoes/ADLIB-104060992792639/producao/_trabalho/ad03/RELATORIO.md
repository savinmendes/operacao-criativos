# AD 03: relatório (PT → espanhol neutro LATAM), 08/10/2026

## Correção de cor (08/10/2026, depois da REVISAO-LOTE-C)

A versão anterior está em `_trabalho\ad03\_antes_cor\`: vídeo, folhas, `base_lipsync`, `base_sem_legenda`, corpo, `montar_corpo.py` e relatório.

- **Causa:** a leitura pelo cv2 (matriz bt709 nos arquivos com essa etiqueta) e a gravação em bt601 escureciam ~2–3 níveis por passada. A base passava pelo LaMa e pela colagem, e o recorte enviado ao HeyGen levava mais uma ou duas passadas.
- **Leitura e gravação:** as do `ad13\lipsync3\comum3.py`, ou seja, ffmpeg bt601 com `accurate_rnd`, conversão inversa exata e etiqueta bt709/tv só no bitstream.
- **Base:** refeita a partir do original `UNICOS_HD`, com as faixas do LaMa já calculadas (nenhum LaMa novo). Os PNG do LaMa vieram da leitura cv2, então foram convertidos para a leitura nova por uma afim fixa, medida no próprio original (resíduo 0,97).
- **Cor de cada trecho do HeyGen:** antes de colar, uma afim BGR robusta leva a saída para a cor da base nova (`_trabalho\_cor0104\util.py`).
- **Nenhum crédito HeyGen e nenhum job novo.** As saídas já baixadas foram reaproveitadas.

**O que foi feito:** `_trabalho\_cor0104\recolocar_cor_03.py`, numa geração só. Faz o mesmo que `_tmp\montar_base.py` + `lipsync\recolocar.py` + `_tmp\loteA.py quadro`.
- **Base:**
  - original + LaMa (`_tmp\lama` e `_tmp\mask`, mesma EMA e mesma zeragem nos cortes);
  - split 1198–1436 com a `_tmp\broll_cruz.mp4`, que já estava na leitura certa porque foi feita por ffmpeg (conferido contra o 06.mp4).
- **Trechos do HeyGen:** colados no recorte inteiro, como antes.
  - A afim foi medida no recorte fora da boca.
  - As saídas já batiam com a base (desvio de +0,1). Só o p07 estava −1/−3/−5 BGR.
  - O escuro do 03 era só da base.
- **Mantido:**
  - as mesmas emendas: 9 cortes e 5 crossfades de 2 quadros;
  - **o quadro 9,40 s (q282) com a boca do q283** (lote A);
  - o **ambiente de sala** do lote A (`_audio\room_tone.wav`, o mesmo `montar_corpo.py`).
- **Conferência:** boca nova × anterior com diferença de estrutura de 1,64 e máximo de 2,3. Não há quadro diferente.
- **Remontagem:** `montar_corpo.py` e `montar_ad.py receita_ad03.json`. Resultado: RESULTADO OK, 96,30 s, CTA em 60,46 s.

**Medidas** (`cor.py`/`brilho.py` com `loteC\escolha_03.json`; saídas em `revisao\loteC\cor0104\`):

| | Antes | Depois |
|---|---|---|
| Área colada − rosto (cor.py / brilho.py) | +0,7 / +0,8 | **+1,6 / +1,4** |
| Rosto × original | −8,5 (U +3,0 / V −2,6) | **+0,1** (U 0,0 / V +0,3) |
| Fundo × original (sem o p07, que tem a cruz) | −7,4 | **+1,6** |
| Degrau pela mediana (elipse × anel) | −2 (0 a −2 por trecho) | **+1** (0 a +1 por trecho) |

- **p08, p12, p13 e p15 ficam com +3,6 a +4,7 nas caixas fixas do `cor.py`. Não é cor:**
  - eles já davam +3 a +4 antes;
  - é a boca nova (fechada, de outro formato) dentro das caixas fixas do lábio e do queixo;
  - a mediana dentro da elipse contra o anel de pele, que ignora o ± do lábio, dá 0 a +1 em todos os trechos.

**Revisão** (`revisar_ad.py --lipsync`, PowerShell, `_lote\proibidos.txt`; trechos em `_cor_rev\`):
- es (0,96), nenhum termo proibido, nenhum silêncio.
- **Índice de pausa do conjunto:** 0,06 antes e **0,07** depois. Por trecho, a variação fica em ±0,02.
- **"PROBLEMA" que já existia antes:**
  - "quadro solto" em 9,13/9,27/9,37 s é o clarão do original (falso positivo já aceito);
  - p02 "acompanha mais o original" já aparecia antes (0,64/0,50, agora 0,58/0,48). É um trecho de 1,1 s.
- **Saiu** o falso "setas sobre a faixa escura".
- O vídeo não foi aberto.

---


## Arquivo
`producao\AD 03 - ORACION-PADRE-ROMERO-ES-LATAM.mp4`
- 96,3 s, 720x1280, 30 fps, 26,0 MB, sem selo.
- Setas a partir do 1º "toca" (60,46 s) até o fim.
- O original termina com o padre falando, sem tela parada. O corte fica 0,7 s depois da última fala, com fade.

## Roteiro (padre, tempos no final; também em `roteiro_es.txt`)
| Tempo | Fala |
|---|---|
| 0,00–6,26 | En el nombre del Padre, del Hijo y del Espíritu Santo, con esta ruda y esta espada de San Jorge, quito toda envidia |
| 6,54–10,47 | y el mal de ojo, y profetizo una lluvia de bendiciones en tu vida. |
| 10,75–16,46 | Quédate hasta el final de este video, porque este mensaje llegó hasta ti por una razón muy especial que Dios preparó. |
| 16,74–22,91 | Yo vengo con el romero divino y con la Desatadora de Nudos, para traer una revelación muy importante para tu vida. |
| 24,06–27,61 | Una bendición de paz muy grande está preparada para llegar a tu hogar. |
| 28,56–36,83 | Por eso este video llegó a tu pantalla ahora, porque la oración de nueve palabras ya tocó el corazón de muchas personas que la rezaron con fe. |
| 38,86–47,39 | Una mujer que vivía el momento más difícil de su vida la rezó con fe, y sintió una paz y una esperanza que no sentía hace mucho tiempo. |
| 48,00–54,44 | Y ahora Dios pide que la Desatadora de Nudos corte, con su amor, el nudo que está atando tu vida y cerrando tus caminos. |
| 55,22–59,27 | Pero para eso, tú necesitas aceptar su bendición con el corazón abierto. |
| 60,08–65,56 | Por eso, toca el botón de abajo ahora mismo, porque yo te dejé un acceso totalmente gratis, con mucho cariño, |
| 67,54–73,82 | al audio que revela las nueve palabras de la oración de la Desatadora de Nudos, preparada especialmente para ti. |
| 74,76–82,31 | Una palabra para cada lazo que está trabando tu vida: en tu hogar, en tu familia, en tus sueños y en tu corazón, para que vuelva la paz. |
| 82,96–92,13 | Presta mucha atención, porque esta oración fue preparada con amor, y llegó hasta ti porque Dios quiere bendecir tu camino y llenar tu casa de paz. |
| 92,41–95,60 | Toca el botón de abajo, y recibe lo que Dios preparó para ti. |

- **Velocidade:** 1,1x nos blocos 0–2 e 1,0–1,04x no resto.
- **Textos alongados de propósito:** para cobrir a fala PT. Com eles, não sobra boca parada nem pausa longa.

## Vozes
- **"ORACAO-03 padre" `5JUCUUmKATtNYJaNlP0n` (nova):** clonada de 0–96 s de voz limpa (demucs).
- É o único personagem que fala, e não havia clone parecido. Nenhuma voz foi apagada.

## Custos
- **TTS:** 2.632 caracteres gerados (cerca de US$ 0,43), em 2 rodadas.
  - A 1ª ficou curta e deixava pausas longas, então 12 blocos foram regenerados mais longos.
  - O roteiro final usa 1.507 caracteres.
- **HeyGen:** 15 trechos em **speed**, cerca de 93 s de rosto, ou seja, **~93 créditos** estimados (teto de 170).
  - O saldo da conta compartilhada foi de 8.840 para 8.818 até a última leitura.
  - A cobrança do speed atrasa até ~1 h.

## Lipsync
- **Entrada:** recorte 360x640 em (170,0), escala 2x, com o PT na entrada e o ES como `audio`.
- **Parâmetros:** speed, `enableDynamicDuration=false`, `keepTheSameFormat=true`, `fpsMode cfr`, sem marca d'água.
- **Quadros:** todas as saídas voltaram com o número exato.
- **Emendas:** 9 em cortes reais e 5 com crossfade de 2 quadros.

| Trecho | Quadros | Índice de pausa |
|---|---|---|
| p01 | 0–72 | sem pausa (corr. ES 0,46 × PT 0,12) |
| p02 | 73–106 (completado até 3 s) | 0,14 |
| p03 | 107–273 | sem pausa (0,18 × 0,04) |
| p04 | 283–498 | sem pausa (0,34 × 0,22) |
| p05 / p06 | 499–1197 | 0,06 / 0,04 |
| p07 (split, metade de cima) | 1198–1436 | 0,02 |
| p08 | 1437–1532 | sem pausa (0,28 × 0,21) |
| p09 / p10 / p11 | 1626–2241 | 0,05 / 0,05 / 0,13 |
| p12 | 2242–2293 (completado até 3 s) | 0,12 |
| p13 / p14 / p15 | 2294–2889 | 0,03 / sem pausa (0,25 × 0,13) / 0,03 |
| **Conjunto (15 trechos)** | | **0,08 APROVADO** |

## O que saiu ou foi trocado
- **Dinheiro:**
  - Saiu: "chuva de riqueza", "depósito muito farto na sua conta em duas horas", "riqueza seis vezes maior", "nó da pobreza", "riqueza imediata", "começando pelo seu dinheiro" e "continue pobre".
  - Entrou: "lluvia de bendiciones", "bendición de paz… para tu hogar" e "el nudo que está atando tu vida".
- **Saúde:** saiu "laço de dores e problemas de saúde".
- **Ameaça e pressão:**
  - Saiu: "nem pensem em pular… estará pecando", "falsos amigos denunciando", "em trinta segundos", "tem que ser rápido", "imediatamente" e "acesso emergencial".
  - Entrou: "Quédate hasta el final…" e "Presta mucha atención…".
- **Depoimento e pessoa:** saiu "dona Geisa, 59 anos… ligação do gerente". Entrou "Una mujer… sintió una paz y una esperanza", o mesmo padrão aceito no AD 13.
- **Hora do dia e herança:** saíram "hoje" e "toma posse do que já é seu por herança".
- **Imagem:**
  - **Tela dividida (39,93–47,90 s):** embaixo havia o depoimento com celular e "PIX Recebido R$ 35.000,00".
    - A metade de baixo virou a cruz dourada do próprio acervo (06.mp4, 108 s, só a parte de cima, sem a seta).
    - O padre continua em cima, com lipsync.
  - **Legenda PT** (y ~985–1010; no split, ~628–650): saiu com LaMa GPU e máscara justa. A boca fica em y ~250–440.
  - **Mãozinha "AQUI/clique" (60,9–63,8 s):** saiu.
- **Mantido:** o padre, a ruda, a espada de São Jorge, o romero divino, a Desatadora de Nudos, a "oración de nueve palabras", o take da corda (51,1–54,2 s) e o CTA "Toca el botón de abajo".

## Revisão própria
- **`revisar_ad.py`** (proibidos da lista + "pobreza", `--lipsync` com 15 trechos):
  - idioma es (0,96);
  - nenhum termo proibido;
  - nenhuma fala PT residual;
  - índice do conjunto 0,08.
- **Os 3 "problemas" que o script acusa foram conferidos a olho e são falsos positivos:**
  - **"Quadro solto" em 9,13–9,37 s:** é o clarão de transição do próprio original, quadros 274–281 (`_tmp\folha_flash.jpg`).
  - **"Setas sobre faixa escura":** a faixa é a madeira do púlpito. Não há texto embaixo das setas (`_tmp\q80.jpg`).
- **Silêncios de 0,9–1,4 s em 23, 37, 59 e 66 s:** são pausas de frase, iguais às do PT, e a boca fica fechada.
- **Folhas de 1 em 1 quadro:** `folha_cortes_1.jpg` e `folha_cortes_2.jpg` cobrem os 9 cortes e as 5 emendas. Não há quadro solto nem pulo de boca.

## Pontos para a pessoa olhar
1. **Clarão de 9,13–9,40 s (8 quadros):** é a transição original e ficou sem lipsync. O rosto aparece lavado de amarelo, com a boca original, enquanto o ES fala. Não dá para ler a boca.
2. **Cruz dourada no split (40–48 s):** é a mesma cruz das telas finais de outros ADs. Para trocar, edite `_tmp\broll_cruz.mp4` e rode `_tmp\montar_base.py`, `lipsync\recolocar.py`, `montar_corpo.py` e `montar_ad.py`.
3. **Depoimento suave (38,9–47,4 s):** "una mujer… sintió paz y esperanza". Se a pessoa quiser zero depoimento, é preciso refazer só o p07 (cerca de 8 créditos).
4. **Planos fechados (74,7–83 s):** a legenda passa sobre as mãos e o ramo, abaixo da boca.
5. **Voz nova do padre:** vale ouvir o tom.

---

# Correção lote A (08/10/2026): observações do revisor (sem crédito)

## 1. Ambiente de sala por baixo dos silêncios absolutos
- **Script:** `_tmp\loteA.py room`.
- **Origem do ambiente:** o room tone foi extraído do **próprio original** (`_audio\orig.wav`).
  - Entraram as janelas de 20 ms sem voz: vocals do demucs abaixo do pico −40 dB, no_vocals abaixo de −50 dB (sem os efeitos de transição) e vizinhas também sem voz.
  - Saíram 20 janelas (0,40 s), com nível mediano de −52,6 dB.
  - O original fala o tempo todo, então não há trecho maior sem voz.
  - O demucs `no_vocals` puro não serviu: fica em −57/−60 dB, que é praticamente o "buraco" atual.
- **Loop:** embaralhado, com crossfade de 10 ms e sem DC, gravado em `_audio\room_tone.wav` a −50 dB.
  - Só entra nos silêncios absolutos da mistura (< −50 dB por ≥ 0,5 s), com rampa de 120 ms.
  - Silêncios cobertos: 22,90–24,05, 27,70–28,50, 36,90–38,85, 54,70–55,25, 59,25–60,10, 65,75–67,50, 82,30–83,00 e 95,60–96,30 s (dentro do fade final). São os 4 apontados pelo revisor e mais 4 pausas curtas, para o fundo ficar uniforme.
- **`montar_corpo.py`:** agora mistura narração + no_vocals + `room_tone.wav`. A versão anterior do script está em `_antes_loteA\`.
- **Medido no final** (antes → depois):

| Silêncio | Antes | Depois |
|---|---|---|
| 22,9 s | −59,9 dB | −47,4 dB |
| 37,4 s | −58,6 dB | −45,5 dB |
| 59,2 s | −59,0 dB | −46,2 dB |
| 66,4 s | −57,2 dB | −45,7 dB |

- **Nenhuma janela abaixo de −55 dB por ≥ 0,5 s.**
- **A fala não mudou:** nas janelas com voz, a diferença média de nível contra o final anterior é de 0,03 dB.

## 2. Quadro de 9,40 s (q282) com a boca original aberta
- **Correção:** `_tmp\loteA.py quadro` colou a região de boca e queixo do q283 no q282, com elipse suave.
  - O q283 é o 1º quadro do p04 (lipsync), da mesma tomada, com a boca quase fechada.
  - O resto do q282 (ramo de alecrim e clarão) ficou como estava, então não há quadro repetido.
- **Base:** `base_lipsync.mp4` foi reescrita. A anterior está em `_antes_loteA\`.
- **Folha:** `folha_q282_loteA.jpg`, de 1 em 1 quadro, de 273 a 289. A boca no q282 agora está fechada e emenda com o p04.

## Remontagem e revisão
- **Montagem:** `montar_corpo.py`, depois `montar_ad.py receita_ad03.json`. Resultado: RESULTADO OK, 96,30 s, 26,0 MB, setas a partir de 60,46 s.
- **`revisar_ad.py --lipsync`** (15 trechos, PowerShell; log em `lipsync\revisar_loteA.log`):
  - idioma es (0,96), nenhum termo proibido;
  - nenhum silêncio > 0,7 s;
  - o lipsync não mudou: p02 0,14 · p05 0,06 · p06 0,04 · p07 0,02 · p09 0,05 · p10 0,05 · p11 0,13 · p12 0,12 · p13 0,03 · p15 0,03;
  - p01, p03, p04, p08 e p14 sem pausa (aviso);
  - **conjunto 0,08, APROVADO**.
- **Os 3 "PROBLEMA" do script são os mesmos falsos positivos já conferidos pelo revisor:**
  - "quadro solto" em 9,13/9,27/9,37 s é o clarão do original;
  - "setas sobre a faixa escura" é a madeira do púlpito.
- **Versão anterior:** `_antes_loteA\` guarda o final, as folhas, a revisão, `base_lipsync.mp4`, `corpo_ad03.mp4`, `montar_corpo.py` e o relatório.

## Ponto para olhar
- **O ambiente** é um loop de 0,4 s de sala real do original, a cerca de −46 dB no final. Vale ouvir uma das pausas (37,4 s) para confirmar que soa como sala e não como chiado.
