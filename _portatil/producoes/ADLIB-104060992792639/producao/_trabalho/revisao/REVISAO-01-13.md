# Revisão independente: AD 01 e AD 13 (07/10/2026)

Revisor independente. Nenhum vídeo nem arquivo de trabalho foi editado. Tudo o que foi gerado está nesta pasta (`_trabalho\revisao\`).

| Vídeo | Veredito | Motivo principal |
|---|---|---|
| AD 01 - ORACION-TRES-BENDICIONES-ES-LATAM.mp4 | **REPROVADO** | O lipsync não acompanha a fala em espanhol em 9 dos 13 trechos. A boca foi refeita, então não é a boca do português, mas ela mexe nas pausas do espanhol e fica parada quando a voz fala. |
| AD 13 - ORACION-PAZ-ES-LATAM.mp4 | **REPROVADO** | Tem um quadro solto em 88,90 s (close da mulher no meio do plano aberto) e o termo proibido "segundos" em 94,9 s. O lipsync está no nível do AD 11 aprovado. |

---

## Como o lipsync foi conferido (e por que o resultado é diferente do que dizem os relatórios)

1. **O `checar_lipsync.py` do kit, rodado direto nas saídas do HeyGen, dá resultado falso nestes ADs** (`checar_lipsync.log`).
   - Os planos têm dois rostos, e a ferramenta mede o maior, que no AD 01 é o **Jesus calado** atrás da mulher.
   - Por isso ela deu "boca não mudou" em 11 dos 13 trechos do AD 01, quando a boca da mulher mudou.
   - **Correção para o kit:** escolher o rosto que fala, ou aceitar um recorte do rosto.
2. **Rodei de novo com o vídeo recortado só no rosto de quem fala** (`checar_lipsync_recorte_rosto.log`, recortes em `crop\`).
   - **A boca mudou em todos os trechos dos dois ADs** (86–100 % dos quadros, contra ruído de cerca de 1). Ou seja, **nenhum trecho devolveu a boca original do português**.
   - A pergunta passa a ser se a boca nova acompanha o espanhol.
3. **Varri o vídeo final inteiro, quadro a quadro, contra o original** (`varrer_boca.py` → `boca_adNN.csv`, analisado em `metricas_adNN.txt`).
   - A medida segue a boca do personagem que fala.
   - **"Mudou?"** é a diferença de pixels contra o original.
   - **"Teste de pausas"** compara a abertura da boca nas pausas da voz ES com a abertura durante a fala ES. Uma boca sincronizada fecha nas pausas.
   - **Correlação** é entre a abertura da boca e a energia da voz ES.
4. **Calibrei com o AD 11, que a pessoa aprovou.** A mesma medida foi rodada nele:

| Medida | AD 11 (aprovado) | AD 13 | AD 01 | Original × voz ES (referência sem sincronia) |
|---|---|---|---|---|
| Índice de pausa (menor = fecha nas pausas do ES) | **0,38** | **0,56** | **0,86** | 0,86–1,01 |
| Correlação boca × voz ES, no vídeo todo, atraso 0 | 0,13 (pico em 0 ms) | 0,16 (pico em 0 ms) | **0,04 (sem pico em 0 ms)** | ~0,02 |
| Correlação por trecho | 0,39–0,47 | 0,02–0,64 (9 de 14 ≥ 0,17) | −0,17 a 0,59 (4 de 13 ≥ 0,26) | — |

- **Nota de método:** na varredura do AD 13, 211 quadros de close (rosto com mais de 240 px) ficaram sem a medida de abertura, por um limite de recorte do script do revisor (já corrigido). Esses quadros só ficaram de fora da média. O AD 01 não foi afetado (8 quadros), e as conclusões continuam as mesmas.
- O AD 01 fica no nível de uma boca **sem sincronia** com o espanhol.
- O AD 13 fica perto do AD 11.
- A voz ES enviada ao HeyGen foi conferida: os `es_sNN.mp3` batem com `narracao_es.wav` e com o áudio final, com atraso de 0 ms. O problema não é deslocamento do áudio, e sim a saída do HeyGen.

---

## AD 01: REPROVADO

### Lipsync, trecho por trecho

Os tempos são do vídeo final, que tem a mesma linha do tempo do original.

| Trecho | Tempo | Boca mudou (recorte) | Corr. ES | Índice de pausa | Veredito |
|---|---|---|---|---|---|
| s01 | 0,00–8,40 | 98 % | 0,15 | 1,09 | **REPROVADO** |
| s02 | 8,40–15,90 | 99 % | 0,02 (PT 0,14) | 1,15 | **REPROVADO** |
| s03 | 15,90–19,47 | 99 % | 0,55 | 0,66 | aprovado |
| s04 | 19,47–20,97 | 91 % | 0,49 | — (1,5 s, sem pausa) | aprovado (curto) |
| s05 | 20,97–32,63 | 99 % | −0,16 | 1,35 | **REPROVADO** |
| s06 | 32,63–42,00 | 99 % | −0,03 | 1,26 | **REPROVADO** |
| s07 | 42,00–49,00 | 92 % | 0,19 (PT 0,20) | 0,90 | **REPROVADO** (na dúvida) |
| s08 | 49,00–60,27 | 99 % | 0,14 (PT 0,28) | — | **REPROVADO** |
| s09 | 60,27–72,47 | 96 % | 0,07 (PT 0,20) | 0,83 | **REPROVADO** |
| s10 | 72,47–83,30 | 99 % | 0,33 | 0,49 | aprovado |
| s11 | 83,30–93,73 | 100 % | −0,04 | 1,07 | **REPROVADO** |
| s12 | 93,73–104,77 | 98 % | 0,12 | 0,86 | **REPROVADO** |
| s13 | 104,77–115,50 | 98 % | 0,29 | 0,64 | aprovado |

Nos trechos s02, s08 e s09, a boca nova chega a acompanhar mais o áudio PT do que o ES. Não é a boca do original, mas a sincronia está errada.

**Exemplos que dá para ver nas folhas** (linha de cima = final, de baixo = original, barra verde = voz ES, vermelha = voz PT):
- **`ad01_emendas_trechos.jpg` e `ad01_boca_21-27.jpg`, 20,97–21,30 s:** a voz ES está em silêncio, entre os blocos, e a boca abre bem ("aah") no início do s05.
- **`ad01_boca_34-40.jpg`:**
  - 36,13–36,67 s: a voz ES fala "es una provisión", e os lábios ficam quase fechados e parados;
  - 37,40–37,60 s: a voz ES está em pausa e a boca abre, mostrando os dentes;
  - 39,40–39,55 s: a voz ES está em pausa e a boca fica bem aberta, no mesmo momento em que o PT original falava.
- **`ad01_quadro_30s_final_x_orig.jpg`, 30,2 s:** a legenda marca "ATABAN" sendo falado, e a boca está fechada, sorrindo.
- **Lista completa das pausas do ES com a boca aberta:** `metricas_ad01.txt`, seção "pausas". São 23 pausas, de 0,73 s a 109,67 s.

**Rosto falando fora do lipsync:** nenhum. Os 13 trechos cobrem de 0 a 115,77 s, o vídeo inteiro.

**Ponta dos trechos:**
- Todos voltaram com o número certo de quadros e o alinhamento é de 0 quadro (`alinhamento_ad01.txt`). Não há boca congelada no fim.
- Nas emendas sem corte de câmera, a boca dá um pulo de um quadro para o outro: a diferença na boca é de 15 a 17, contra 2 a 5 normalmente.
  - Exemplos: 19,43→19,47 s (fechada→aberta), 20,93→20,97 s e 49,00 s.
  - O relatório dizia "4 a 6". Esse número vale para o rosto inteiro, não para a boca.

### Fala
- `revisar_ad.py --idioma es --idioma-residual pt --proibidos "real,reales,dinero,depósito,cantidad,riqueza,cura,curada,enfermedad,cáncer,horas,segundos,borrada"` deu **OK** (`AD 01 - …_revisao.txt`).
  - Idioma: es (1,00). Nenhum termo proibido. A passada forçada em PT só traduz o espanhol, sem fala residual.
- **O texto bate com o roteiro do relatório.** O whisper junta o "Toca" de 105,0 s à frase anterior, o que já estava no relatório. "Hob" é Job pronunciado em espanhol.
- **Dinheiro, cura e ameaça:** não há.
  - "La segunda es una provisión… muy cerca de tocar la puerta de tu casa" sugere ganho material de leve. A gravidade é baixa e está no tom do AD 11 ("llega la abundancia a tu hogar").
  - "el enemigo quiso robar" não é ameaça a quem assiste.

### Imagem
- Folha de 1 q/s (`AD 01 - …_revisao.jpg`):
  - nenhuma legenda nem texto em português;
  - o cartão "CLIQUE E RECEBA!" saiu no corte;
  - a mancha da remoção de legenda é tolerável (quadro a 30,2 s em resolução cheia);
  - sem quadro solto, sem cena duplicada ou espelhada;
  - 1 corte de cena.

### Áudio
- −15,0 LUFS, LRA 2,0. Nenhum silêncio acima de 0,4 s, nem no meio nem no fim (fim 0,7 s depois da fala, com fade). Nenhum corte no meio de palavra foi detectado.

### CTA
- As setas entram em 104,97 s, com "Toca" em 105,02 s, e continuam até o último quadro (y 1105–1170).
- A legenda fica em y≈1358 (escala 1080), na barriga, legível e longe da boca (`ad01_cta_109s.jpg`).

### Defeitos do AD 01

| # | Tempo | Defeito | Gravidade | Correção sugerida |
|---|---|---|---|---|
| 1 | 0,00–15,90; 20,97–72,47; 83,30–104,77 (s01, s02, s05–s09, s11, s12) | Lipsync sem sincronia com a voz ES: a boca mexe nas pausas e fica parada na fala. Em s02, s08 e s09 ela acompanha mais o PT. | **Alta** | Refazer esses 9 trechos no HeyGen (cerca de 85 s, cerca de 22 créditos). Testes que valem a pena:<br>(a) mandar o vídeo **sem áudio**, ou com o PT bem baixo, mais o ES como `audio`;<br>(b) recortar o vídeo de entrada **só na mulher** (sem o rosto do Jesus no quadro) e depois recolocar;<br>(c) trechos mais curtos (6–8 s).<br>Conferir cada saída com o teste de pausas, buscando índice ≤ 0,6, como o AD 11 (0,38) e o AD 13 (0,56). |
| 2 | 20,97–21,30 | A boca abre bem durante o silêncio entre blocos, no início do s05. | Média | Sai junto com o item 1. Se continuar, congelar a boca da base nesses 10 quadros. |
| 3 | 19,47; 20,97; 49,00; 72,47; 83,30; 93,73 | A boca pula de forma em 1 quadro na emenda entre trechos, numa tomada contínua. | Baixa | Fazer uma fusão de 3–4 quadros só na região da boca na emenda, ou cortar os trechos nos cortes de câmera. |
| 4 | Kit | O `checar_lipsync.py` mede o rosto maior (o personagem calado) e dá o resultado errado em plano com dois rostos. Foi assim que o defeito do item 1 passou na revisão própria. | Média (processo) | Adicionar `--recorte x,y,w,h` ou a escolha do rosto por posição e usar o teste de pausas como critério. |

---

## AD 13: REPROVADO

### Lipsync, trecho por trecho

| Trecho | Tempo | Quem | Boca mudou (recorte) | Corr. ES | Índice de pausa | Veredito |
|---|---|---|---|---|---|---|
| j1 | 0,00–6,60 | Jesus | 74 % (barba) | 0,27 | 0,76 | aprovado: boca diferente do original durante a fala ES e fechada na pausa de 6,3–6,6 s (`ad13_j1_jesus_0-6.jpg`) |
| w01 | 7,03–15,17 | mulher | 98 % | 0,50 | 0,39 | aprovado |
| w02 | 15,17–23,07 | mulher | 86 % | 0,22 | 0,57 | aprovado |
| w03 | 23,07–29,10 | mulher | 97 % | 0,18 | 0,78 | aprovado, com os 4 últimos quadros congelados (ver defeitos) |
| w04 | 33,43–43,57 | mulher | 89 % | 0,13 | 0,81 | aprovado com ressalva, com os 4 últimos quadros congelados |
| w05 | 47,13–53,00 | mulher | 86 % | 0,07–0,08 | 0,91 | **duvidoso**: na folha `ad13_w05_47-52.jpg` a boca articula, mas abre na pausa de 50,47–50,97 s |
| w06 | 53,00–59,80 | mulher | 97 % | 0,10 | 0,51 | aprovado |
| w07 | 63,63–67,10 | mulher | 97 % | 0,31 | 0,58 | aprovado |
| w08 | 67,10–76,17 | mulher | 97 % | 0,62 | 0,39 | aprovado |
| w09 | 76,17–83,90 | mulher | 89 % | 0,23 | 0,63 | aprovado, com os 2 últimos quadros congelados |
| w10 | 88,90–98,30 | mulher | 99 % | 0,46 | 0,28 | aprovado na boca, mas o **1º quadro é um quadro solto** |
| w11 | 98,30–106,40 | mulher | 95 % | 0,06 | 0,98 | aprovado na folha `ad13_w11_99-104.jpg`: fecha nas pausas de 99,27–99,40 s e 101,13–101,40 s. A métrica é fraca por causa do corte de câmera em cerca de 104,4 s. |
| w12 | 106,40–116,00 | mulher | 97 % | 0,37 | 0,47 | aprovado |
| w13 | 116,00–119,80 | mulher | 100 % | 0,43 | 0,60 | aprovado |

**Rosto falando fora do lipsync:**
- **6,60–7,03 s (transição com glitch):** o rosto da mulher aparece com a boca original enquanto a voz ES começa "Porque yo acabo" (6,66 s). Fica muito distorcido pelo glitch (`ad13_transicao_6-7.jpg`, `ad13_glitch_6s.jpg`). Gravidade baixa.
- **43,57–47,13 s (b-roll da mulher na mesa):** a boca original não foi tocada. Ela não está falando: a boca fica entreaberta e depois aberta, como espanto, sem articular (`ad13_broll_mesa_43-47.jpg`). Aceitável.
- **29,10–33,43 s (corda), 59,80–63,63 s (esteira) e 83,90–88,90 s (quarto):** não há rosto. No quarto, o detector só acha o crucifixo.

**Ponta dos trechos:**
- O alinhamento é de 0 quadro em todos (`alinhamento_ad13.txt`).
- Nos trechos que voltaram curtos do HeyGen, o `recolocar.py` congela o quadro **inteiro**:
  - w01: os 2 últimos quadros (15,10–15,13 s), numa pausa e antes de um corte. Imperceptível;
  - w03: os 4 últimos quadros (28,97–29,07 s), **com a voz falando** ("…que bloquea"), logo antes do corte para a corda;
  - w04: os 4 últimos quadros (43,43–43,53 s), **com a voz falando**, antes do corte para o b-roll;
  - w09: os 2 últimos quadros (83,83–83,87 s), antes do corte para o quarto.
- As outras emendas caem em cortes de câmera ou continuam suaves (53,0 e 98,3 s) (`ad13_emendas_trechos.jpg`).

### Fala
- O `revisar_ad.py` com a lista pedida deu **PROBLEMA: termo proibido "segundos" em 94,9 s** ("y tienes pocos segundos para escuchar esta oración sagrada") (`AD 13 - …_revisao.txt`).
- Idioma: es (0,99). Sem fala residual em PT.
- **O texto bate com a tabela do relatório.**
- **Dinheiro e cura:** não há. "paz para tu cuerpo y tu alma" e "alivio para tu corazón" estão dentro da regra.
- **Pressão e ameaça:**
  - "esta revelación puede salir del aire, y tienes pocos segundos" é urgência falsa com contagem regressiva. É o que sobrou do "você tem 30 segundos / antes que apaguem", que o briefing manda tirar;
  - "El enemigo no quiere que recibas esta bendición" está no nível do AD 11 aprovado, então pode ficar.

### Imagem
- Folha de 1 q/s (`AD 13 - …_revisao.jpg`): nenhuma legenda nem texto em português, a mãozinha "toque aqui" saiu e a mancha da remoção é tolerável.
- **Quadro solto em 88,90 s (quadro 2667):**
  - entre o quarto e o plano aberto da mulher com Jesus, aparece **1 quadro de um close da mulher** que não existe no original naquele tempo;
  - é o 1º quadro da saída do HeyGen do w10, que já não batia com o original: diferença de 11,8 contra cerca de 2 nos outros trechos (`ad13_quadro_solto_88.9s.jpg`, `ad13_quarto_transicoes.jpg`).
- A cena do quarto (83,9–88,9 s) está sem pessoa e sem espelhamento ou duplicação.
- O `revisar_ad` não acusa cortes a menos de 0,3 s, porque o quadro solto fica colado a um corte.

### Áudio
- −15,1 LUFS, LRA 3,2.
- Pausas de 0,58–0,63 s em 46,1 s, 48,3 s e 90,4 s, que são pausas de frase.
- Fim 0,7 s depois da fala. Voz de Jesus (clone de 6,6 s) audível e coerente no gancho. Nenhum corte no meio de palavra.

### CTA
- As setas entram com "toca" (cerca de 99,4 s) e ficam até o último quadro.
- A legenda (y 1493 na escala 1080) fica legível e abaixo do queixo, inclusive nos closes de 109–111 s e 116 s (`ad13_quadros_20-56-110-116.jpg`).

### Defeitos do AD 13

| # | Tempo | Defeito | Gravidade | Correção sugerida |
|---|---|---|---|---|
| 1 | 88,90 s (quadro 2667) | Quadro solto: 1 quadro de close da mulher no início do w10. | **Alta** | No `recolocar.py`, descartar o 1º quadro do `ls_w10.mp4` e usar o 2º duplicado, ou o quadro da base, e remontar. Sem custo de HeyGen. |
| 2 | 94,9 s | Termo proibido "segundos", em "tienes pocos segundos". É urgência falsa com contagem regressiva. | **Alta** (está na lista de proibidos) | Trocar por "no dejes pasar este momento" ou "presta atención hasta el final", que tem a mesma duração. Regerar só esse bloco de TTS e o lipsync do w10 (cerca de 9 s). Vale tirar "puede salir del aire" junto. |
| 3 | 28,97–29,07 e 43,43–43,53 s | Quadro inteiro congelado por 4 quadros com a voz falando, antes do corte (w03 e w04 voltaram curtos). | Média | Cortar o pedaço de entrada com `-ss/-t` + `tpad` (armadilha do kit), ou espalhar os quadros que faltam em vez de congelar o fim. O jeito mais simples é recolocar a base original nesses 4 quadros. |
| 4 | 50,47–50,97 s (w05) | A boca abre numa pausa de 0,5 s do ES. As métricas do w05 são as mais fracas do AD. | Baixa/média | Conferir assistindo. Se incomodar, refazer o w05 (5,9 s). |
| 5 | 6,60–7,03 s | A voz ES da mulher começa durante o glitch, com a boca original (distorcida). | Baixa | Atrasar o início do bloco 2 para cerca de 7,05 s, ou aceitar. |
| 6 | 83,83–83,87 s e 15,10–15,13 s | 2 quadros congelados antes de um corte. | Baixa | Sai junto com a correção do item 3. |

---

## Arquivos desta revisão
- **Folhas de boca, de 1 a 3 em 3 quadros (final em cima, original embaixo):**
  - AD 01: `ad01_boca_21-27.jpg`, `ad01_boca_34-40.jpg`, `ad01_boca_72-78.jpg`, `ad01_emendas_trechos.jpg`;
  - AD 13: `ad13_j1_jesus_0-6.jpg`, `ad13_w05_47-52.jpg`, `ad13_w11_99-104.jpg`, `ad13_emendas_trechos.jpg`, `ad13_transicao_6-7.jpg`, `ad13_broll_mesa_43-47.jpg`.
- **Imagem:**
  - folhas de 1 q/s: `AD 01 - …_revisao.jpg` e `AD 13 - …_revisao.jpg`;
  - quadros avulsos: `ad01_quadro_30s_final_x_orig.jpg`, `ad01_cta_109s.jpg`, `ad13_quadros_20-56-110-116.jpg`, `ad13_quadro_solto_88.9s.jpg`, `ad13_quarto_transicoes.jpg`, `ad13_glitch_6s.jpg`.
- **Dados:**
  - `boca_ad01.csv`, `boca_ad13.csv` e `boca_ad11.csv` (calibração);
  - `metricas_ad01.txt`, `metricas_ad13.txt` e `metricas_ad11.txt`;
  - `checar_lipsync.log` (kit sem recorte: resultado falso) e `checar_lipsync_recorte_rosto.log`;
  - `alinhamento_ad01.txt` e `alinhamento_ad13.txt`;
  - `AD 01 - …_revisao.txt` e `AD 13 - …_revisao.txt`.
- **Scripts do revisor:** `varrer_boca.py`, `analisar.py`, `pausas.py`, `lag.py`, `folha_boca.py`, `alinhamento.py` e `rodar_checar.sh`.
