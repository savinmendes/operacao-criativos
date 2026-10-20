# AD 13: relatório (piloto PT → espanhol neutro LATAM, 07/10/2026)

## Arquivo final
- `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 13 - ORACION-PAZ-ES-LATAM.mp4`
- 119,80 s, 720x1280, 30 fps, AAC, 26,3 MB. Tema escolhido: **PAZ**.
- Ficaram junto: `_frames.jpg`, `_revisao.jpg` e `_revisao.txt`.

## Roteiro em espanhol (tempos no vídeo final)
| Tempo | Quem | Fala |
|---|---|---|
| 0,18–6,26 | JESUS | No te asustes si, después de hacer esta oración sagrada, sientes una paz que llena tu cuerpo y tu alma. |
| 6,66–13,21 | MULHER | Porque yo acabo de bajar para quitar el peso que cargas en el corazón, y cortar toda la envidia que cerró tus caminos. |
| 15,15–24,85 | MULHER | Fuiste tú a quien elegí entre tanta gente. Hay una bendición doble llegando hasta ti en esta oración: paz para tu cuerpo y tu alma, y alivio para tu corazón. |
| 26,45–31,51 | MULHER | La envidia ató un nudo ciego y pesado en tu camino, que bloquea tu paz y tu alegría. |
| 31,98–44,17 | MULHER | Y la culpa de lo que estás pasando nunca fue tuya. No es que tu fe sea débil. Rezaste, encendiste velas, hiciste promesas, y aun así tu corazón no encontraba descanso. |
| 44,63–58,10 | MULHER | La culpa nunca fue tuya. Siempre fue ese nudo de envidia. No se trata de rezar más. Lo que desata ese nudo y devuelve la calma a tu vida es hacer esta oración de la manera correcta, sin fallas. |
| 58,48–73,80 | MULHER | Y cuando el nudo se desate, una nueva fuerza y alegría llenarán tu espíritu, y la bendición de Dios llegará a tu hogar. Las preocupaciones que te quitan la paz se alivian, y tu corazón encuentra descanso. |
| 76,23–90,49 | MULHER | Una mujer que vivía el momento más difícil de su vida, con el corazón lleno de miedo, hizo la oración de nueve palabras. Y en ese mismo mes, sintió una paz y una esperanza que no sentía hace mucho tiempo. |
| 90,95–98,11 | MULHER | Pero presta atención, porque esta revelación puede salir del aire, y tienes pocos segundos para escuchar esta oración sagrada. |
| 98,56–107,33 | MULHER | Entonces toca el botón de abajo ahora, porque te dejé un video corto y gratuito con el orden correcto de las oraciones, una para cada nudo. |
| 107,81–119,07 | MULHER | Pero sé rápido. El enemigo no quiere que recibas esta bendición. No dejes pasar este momento. Toca el botón de abajo, y recibe lo que Dios ya preparó para ti. |

Velocidade da voz: 1,0x em todos os blocos.

## Vozes (ElevenLabs)
Nenhuma voz foi apagada.
- **Clones do AD 11 não reaproveitados.** Comparei as vozes com o Resemblyzer:
  - a mulher do 13 contra a "ORACAO-11 mulher" dá 0,84–0,87 de semelhança, e o tom médio é 225 Hz contra 191 Hz. O próprio clone do 11 contra a voz original dele dá 0,95. Ou seja, não é a mesma voz;
  - a "ORACAO-11 menina" dá 0,57;
  - o 13 não tem menina.
- **"ORACAO-13 mulher" `ZsipxX9wNYg2lJhEScWc` (nova):** clonada de 113 s de voz limpa (demucs, 6,6–120 s). A saída em espanhol fica a 0,93 da original.
- **"ORACAO-13 jesus" `lRnvtIq1W0SQIeABr1I4` (nova):** clonada dos únicos 6,6 s em que ele fala. A saída fica a 0,90 da original.

## TTS
- **Gerado:** 1.885 caracteres, ≈ US$0,31. O bloco 6 foi gerado duas vezes, porque a 1ª versão estourou o tempo.
- **No roteiro final:** 1.653 caracteres.

## HeyGen (lipsync)
- **Trechos:** 14, somando 103 s: Jesus 0–6,6 s e mais 13 trechos da mulher de 3,5 a 10,1 s.
- **Parâmetros:** precision, `enableDynamicDuration=false`, `keepTheSameFormat=true`, `fpsMode cfr`, sem marca d'água.
- **Entrada:** o vídeo leva o áudio PT original e o espanhol vai separado, como `audio`.
- **Créditos:** 8.947 antes e 8.916 depois, ou seja, **31 créditos** de queda na conta, abaixo do teto de 120.
  - Atenção: outros pilotos rodavam ao mesmo tempo na mesma conta, então 31 é o teto do que este AD pode ter gasto.
- **Conferência:** todos os 14 trechos foram conferidos pela diferença na região da boca entre o original e o lipsync.
  - O bloco mais alterado ficou entre 9 e 16/255, contra um ruído de 1,0 a 1,7/255. O lipsync aconteceu em todos, sem refação.
  - Folhas de zoom: `lipsync/zoom_*.jpg` e `zoom_final.jpg`.
- **Quadros a menos:** 4 trechos voltaram com 2 a 4 quadros a menos (w01, w03, w04, w09). O `recolocar.py` completa congelando o último quadro.

## O que saiu ou foi trocado
- **Promessa de cura e saúde:**
  - saiu: "dor curada em menos de seis horas", "daqui cinco horas arrancar todas as suas enfermidades", "milagre duplo de cura total", "câncer", "arranca a doença do corpo", "vitalidade e saúde de uma jovem nos ossos", "dor crônica / farmácia", "a doença desapareceu", "continuar doente";
  - entrou: "paz para tu cuerpo y tu alma", "alivio para tu corazón", "descanso", "nueva fuerza y alegría en tu espíritu".
- **Dinheiro:**
  - saiu: "riqueza divina", "Pix seis vezes maior", "dinheiro sumia", "avalanche de riqueza no mesmo dia", "dívida paga à vista", "maior contrato", "miséria";
  - entrou: "bendición de Dios en tu hogar" e "caminos".
- **Pessoa real:** saiu a citação de **Ana Maria Braga** e a cena do quarto com uma mulher parecida com ela (83,9–88,9 s).
  - A cena virou um recorte do mesmo quarto, só com o crucifixo e a cabeceira, sem pessoa, com aproximação lenta.
  - O depoimento virou "una mujer… sintió paz y esperanza".
- **Ameaça:**
  - saiu: "o inimigo está denunciando", "você tem 30 segundos", "antes que apaguem a sua única salvação para sempre";
  - entrou: "el enemigo no quiere que recibas esta bendición" e "no dejes pasar este momento".
- **Acusação:** "uma falsa mulher que você chama de amiga" virou "la envidia ató un nudo".
- **Brasil:** saiu o "Pix". Nenhuma cena tinha moeda ou marca brasileira.
- **Vídeo:**
  - a legenda PT queimada (y 972–1024, longe de boca e queixo) foi tirada com LaMa local, quadro a quadro;
  - o ícone de mãozinha "toque aqui" (98–104 s) também saiu.
- **Mantido:**
  - o gancho "No te asustes…" na voz de Jesus, a personagem, o nó de inveja, "no se trata de rezar más / de la manera correcta, sin fallas", a "oración de nueve palabras", a urgência e o CTA "Toca el botón de abajo";
  - sem selo.
- **Áudio:**
  - narração a −16 LUFS por bloco + fundo do demucs (no_vocals, −31 LUFS, não estava mudo), no volume original;
  - o vídeo foi cortado 0,7 s depois da última fala, com fade de 0,3 s.
- **Legenda e setas:**
  - legenda pelo alinhamento, na altura da legenda antiga (y 1493 na escala 1080);
  - setas a partir do 1º "Toca" (99,42 s) até o fim.

## Revisão própria
- **Script:** `revisar_ad.py --idioma es --idioma-residual pt --proibidos "real,reales,dinero inesperado,depósito,cantidad inesperada,borrada para siempre,curada,cura,horas"` deu **OK: nenhum problema**.
- **Checagens:**
  - idioma detectado: es (1,00);
  - termos proibidos: nenhum;
  - silêncio acima de 0,7 s: nenhum;
  - saltos de pts: nenhum;
  - cortes a menos de 0,3 s: nenhum;
  - setas no último quadro: sim.
- **Transcrição em espanhol:** bate com o roteiro.
- **Português residual:** a passada forçada em pt só "traduz" o espanhol (portunhol do Whisper). Não sobrou fala em português.
- **Folha de contato:** sem legenda PT residual nem mãozinha, e a cena do quarto sem pessoa.
- **Zoom na boca:** as bocas mudam e não há borrão visível.
- **Correção feita:** na 1ª montagem, a cena do quarto mostrava a transição espelhada do original e o crucifixo duplicado. Foi refeita a partir de um quadro parado.

## Pontos para a pessoa olhar
1. **Voz de Jesus:** clonada de só 6,6 s. Pode soar menos natural que a da mulher; vale ouvir o gancho.
2. **Cena do quarto (83,9–88,9 s):** é um quadro parado com zoom, porque o recorte amplia 2,7x. Fica mais suave e menos nítido que o resto.
3. **Desvio leve de sincronia:** nos trechos w01, w03, w04 e w09 (6,9–29 s, 33–43 s e 76–84 s), o HeyGen devolveu 2 a 4 quadros a menos. Pode haver até ~0,13 s de desvio no fim de cada um.
4. **Silêncio da mulher em 73,8–76,2 s:** ela fica na tela de boca fechada (pausa entre blocos).
5. **"Dormir tranquilo" saiu:** o original dizia isso; o espanhol ficou só com "tu corazón encuentra descanso", sem hora do dia.
6. **Texto de urgência:** "esta revelación puede salir del aire / tienes pocos segundos" foi mantido. Vale avaliar contra a política do Meta.

---

## v2: correções da revisão independente (REVISAO-01-13.md)
A v1 ficou guardada em `_v1\` (vídeo final, narrações, alinhamento, corpo, base, `recolocar.py`, `ls_w10.mp4`).

1. **Quadro solto em 88,90 s (quadro 2667):** era o 1º quadro do `seg_w10` (e da saída do HeyGen), um close de outra tomada. O `recolocar.py` ganhou a opção `nome=arquivo@k`, que descarta os k primeiros quadros. O w10 entra com `@1`. A emenda agora vai direto do quarto para o plano aberto.
2. **Urgência falsa:** a frase do bloco 8 virou *"Pero presta mucha atención hasta el final, porque este momento es para ti, y esta oración sagrada fue preparada con amor para ti."* (90,91–98,21 s).
   - Gerada com a voz "ORACAO-13 mulher" `ZsipxX9wNYg2lJhEScWc` a 1,06x (`_audio/tts/b8v4.*`). Foram 3 gerações: a frase-exemplo curta saiu com 6,4 s e deixaria 1,3 s de silêncio, e a longa a 1,0x estourava. Total de 372 caracteres, cerca de US$0,06; a frase final tem 129.
   - `narracao_es.wav`, `narr_mulher.wav`, o alinhamento, `tempos_reais.json`, `blocos.json` e `roteiro_es.txt` foram atualizados.
   - Lipsync do w10 refeito (88,90–98,30 s, 9,4 s). Entrada: `pt_w10.mp4` com o áudio PT original. O espanhol foi separado (`es_w10_v2.mp3`). precision, sem duração dinâmica, mesmo formato, cfr, sem marca d'água. Job `11c6c993e0124125913c8624d0dfb00f`, saída em `lipsync/ls_w10_v2.mp4` com 282 quadros.
   - **Créditos:** 8.914 antes e 8.912 depois, ou seja, **2 créditos**.
   - **Conferência:** na frase nova, a diferença de boca entre v2 e v1 é de 14,0, contra 2,5 no trecho de fala igual. Índice de pausa do w10: 0,02 (v1: 0,29). A correlação da boca com a voz nova é 0,33, contra 0,23 com a voz antiga. Folha: `_v2chk/boca_w10_frase_nova.jpg`.
3. **Quadros congelados:** o `recolocar.py` não congela mais o fim. Ele **reamostra** o trecho no tempo (`setpts*(n/m)` + `fps=30` + `trim` exato). Os quadros que faltavam viraram duplicatas isoladas de 1 quadro, espalhadas (w01: 242→244, w03: 177→181, w04: 300→304, w09: 230→232). Não há mais 4 ou 2 quadros parados com a voz falando.
4. **6,60–7,03 s:** o "Porque" saiu do bloco 1 (corte em 0,37 s do bloco, mesmo deslocamento). A fala começa em 6,98 s com "Yo acabo de bajar…", no fim do glitch (último quadro distorcido: 6,97 s). O sentido é o mesmo, e o w01 não precisou ser refeito porque o tempo do resto da fala não mudou.
5. **Remontagem:** `audio_corpo.wav` refeito com `_audio/montar_corpo_audio.py`. Os ganhos e o atraso foram medidos na v1, que o script reproduz com resíduo de 0,0002. O corpo foi refeito e passou de novo pelo `montar_ad.py` com a mesma receita (setas no "toca", 99,42 s).

### Revisão v2
- **`revisar_ad.py --proibidos "…,horas,segundos,aire"`:** deu **OK: nenhum problema**.
  - idioma es (0,99), nenhum termo proibido, nenhum silêncio acima de 0,7 s, nenhum salto de pts;
  - 18 cortes, nenhum par a menos de 0,3 s;
  - setas no último quadro.
- **Arquivo:** 119,80 s, 26,4 MB.
- **Emendas, de 1 em 1 quadro em volta dos 18 cortes:** `_v2chk/emendas_1.jpg` e `emendas_2.jpg`. Não há quadro solto.

---

## v3: correções da revisão do lote A (REVISAO-LOTE-A.md, AD 13 reprovado)
A v2 ficou guardada em `_v2\`: vídeo final (`AD13_v2.mp4`), `base_lipsync`, corpo, áudio do corpo, narrações, alinhamento, roteiro, `recolocar.py`, `tempos_reais.json` e `montar_narracao.py`.
Todo o trabalho novo está em `lipsync3\`.

### 1. Lipsync refeito em `speed` (w03, w04, w05, w06, w07, w09, w11 e w12)
- **Como no `LICOES-LIPSYNC.md`:**
  - `mode: speed`, `enableDynamicDuration=false`, `keepTheSameFormat=true`, `fpsMode cfr`, sem marca d'água;
  - o vídeo de entrada é o recorte só no rosto da mulher, com o áudio PT original (`UNICOS_HD\13.mp4`);
  - o espanhol vai separado, como `audio` (`in\es_<seg>.mp3`, da `narracao_es.wav` nova).
- **Recorte:**
  - `varrer.py` acha os rostos e os cortes de câmera por quadro (`rostos.json`, `cortes.json`).
  - `plano3.py` é adaptado do `ad17\lipsync\plano.py`:
    - recorte 9:16 que segue a mulher (à esquerda), suavizado dentro de cada tomada e reiniciado nos cortes;
    - descarta detecções duplas;
    - o recorte termina antes do rosto do Jesus (`x1` < `x0` do Jesus em todas as tomadas com ele);
    - folha de conferência: `chk_crops.jpg`, com só a mulher e, no máximo, a borda do ombro ou do cabelo dele.
  - A entrada é gerada pelo `cortar.py` (do AD 17).
- **Mesmos limites de trecho da v1:** os trechos que já atravessavam cortes de câmera (por exemplo, w06 em 58,37 s e w12 em 109,0 e 111,87 s) continuaram assim. O recorte acompanha cada tomada.
- **Jobs:**

| Trecho | Job |
|---|---|
| w03 | `9f5f841b6bac4443aa9967d531e779f1` |
| w04 | `0f82623863554cfba67c1b65aded2d55` |
| w05 | `6cddc8e27eb641279ce053c96f37989b` |
| w06 | `a7b132511b6d457a9ac0d0a33fad86e0` |
| w07 | `8e8f95923ccc4b669715722162c967c8` |
| w09 | `84212d69f7bf4305a8b7a2ac855bc207` |
| w11 | `a6232a29029b4b4cb1ca927e60a16240` |
| w12 | `55988a09ccdf4401ae16ec47d4556cd9` |

  - Todos voltaram em menos de 5 min e com o número exato de quadros, então não houve reamostragem nem quadro congelado.
- **`fechar3.py` (sem crédito):**
  - É o `fechar_crop.py` com a boca de referência tirada só da mesma tomada e a pausa cortada nos cortes de câmera.
  - Foi aplicado onde a folha ainda mostrava boca aberta numa pausa do ES:
    - w05, 50,47–51,0 s: início do close, a boca abria logo depois do corte;
    - w11, 105,75–106,05 s.
  - Folhas: `chk_w05F.jpg` e `chk_w11F.jpg`.
- **Trechos não refeitos (sem crédito):** a mesma correção foi aplicada na pausa final do j1 (6,2–6,6 s, Jesus) e do w13 (119,1–119,8 s), com o `fechar_base.py`.
- **Recolocação (`recolocar3.py`):**
  - parte da `base_lipsync` da v2 (j1, w01, w02, w08, w10 v2 e w13) e cola a saída speed só na boca e no queixo, sobre a `base_sem_legenda`;
  - crossfade de 2 quadros na única emenda sem corte (w05→w06, 53,00 s); as outras 13 emendas caem em cortes de câmera.
- **Cor:**
  - O cv2 lê tudo com a matriz bt601, e o encoder em pipe gravava com outra conversão. Cada passada escurecia o quadro em cerca de 2–3 níveis, e duas passadas seguidas dobravam isso. Achei isso numa 1ª montagem e refiz tudo.
  - Agora a leitura é feita pelo ffmpeg com a matriz bt601 fixa e `accurate_rnd`, a gravação usa a conversão inversa exata, e a etiqueta bt709/tv vai no bitstream. A ida e volta dá 0,84 (só a compressão).
  - O desvio que o recorte de entrada levou para o HeyGen (BGR ≈ +1,6/+3,7/+5,1) é compensado antes de colar.
  - A dif. de controle do revisor caiu de ~5 para ~1 nos trechos refeitos.

### 2. "Pero sé rápido" → "No lo dejes para después."
- Gerada com a voz "ORACAO-13 mulher" `ZsipxX9wNYg2lJhEScWc` a 1,0x, junto com a frase seguinte para a entonação fechar natural. Usei só a 1ª frase (`_audio/tts/b10a.*`).
  - Foram 74 caracteres, cerca de US$0,01.
- Entra em 107,63 s; a fala vai de 107,68 a 109,16 s.
- O resto do bloco 10 ("El enemigo…") ficou no mesmo lugar (109,53 s), com o mesmo áudio da v2.
  - A diferença entre a narração da v2 e a da v3 fica só entre 107,6 e 109,2 s.
  - A duração total não mudou.
- `montar_narracao.py`, `narracao_es.wav`, as narrações por personagem, o alinhamento, `tempos_reais.json`, `blocos.json`, `roteiro_es.txt` e `audio_corpo.wav` foram atualizados.
- O w12 foi refeito em speed com o áudio novo. Folha: `chk_w12.jpg`; a boca articula a frase nova e fecha na pausa.
- **Atenção:** a frase nova fica perto de "No dejes pasar este momento" (112,7 s). As duas são pressão suave e sem prazo.

### 3. Índice de pausa
Medido no vídeo final, com cada trecho recortado do final, rosto da mulher em `--rosto` e `revisar_ad.py --lipsync`.

| Trecho | Tempo | v2 (revisor) | v3 |
|---|---|---|---|
| w03 | 23,07–29,10 | 0,69 | **0,07** |
| w04 | 33,43–43,57 | 0,90 | **0,24** |
| w05 | 47,13–53,00 | 0,98 | **0,06** |
| w06 | 53,00–59,80 | 0,71 | **0,10** |
| w07 | 63,63–67,10 | 0,65 | **0,13** |
| w09 | 76,17–83,90 | 0,67 | **0,08** |
| w11 | 98,30–106,40 | 0,83 | **0,36** |
| w12 | 106,40–116,00 | 0,24 | **0,04** (frase nova) |
| j1 (não refeito) | 0,00–6,60 | 0,62 | 0,78 (aviso, só 8 q de pausa) |
| w01 / w02 / w08 / w10 / w13 (não refeitos) | | 0,36 / 0,16 / 0,35 / – / 0,56 | 0,39 / 0,52 / 0,35 / 0,02 / 0,26 |
| **Conjunto (14 trechos)** | | 0,57 | **0,26** |

- **Medida do kit no próprio trecho, antes da montagem** (`medir3.py` → `checar_lipsync --rosto`): w03 0,07, w04 0,24, w05 0,45 (0,06 após o fechar), w06 0,12, w07 0,12, w09 0,08, w11 0,45 (0,38 após o fechar), w12 0,04. Todos APROVADOS. A correlação da boca com o ES ficou entre 0,33 e 0,61; com o PT, entre −0,02 e 0,29.
- **j1:** o aviso vem da barba. A boca está fechada na pausa final (folha `chk_j1_ab.jpg`, antes e depois), mas o detector lê abertura de cerca de 0,05 contra 0,07 na fala.
- **Bocas falando PT que o revisor apontou** (folhas `chk_w04.jpg`, `chk_w05.jpg`/`chk_w05F.jpg` e `chk_w11F.jpg`):
  - 34,5–35,4 s e 36,9–37,4 s: fechadas;
  - 48,3–48,9 s: fechada;
  - 50,47–51,0 s: fechada depois do `fechar3`;
  - 105,8–106,0 s: fechada.

### 4. Remontagem e revisão
- O `corpo_ad13.mp4` é a `base_lipsync` + `audio_corpo.wav`, com 3.594 quadros e 119,80 s. Passou pelo `montar_ad.py` com a mesma receita (setas no "toca", 99,42 s, sem selo).
- **`revisar_ad.py --lipsync` (PowerShell):** deu **OK: nenhum problema**. Log em `lipsync3\rev\revisar_v3.log`.
  - Os proibidos incluíram "rápido".
  - idioma es (0,99), nenhum termo proibido, nenhum silêncio acima de 0,7 s, nenhum salto de pts;
  - 18 cortes, nenhum par a menos de 0,3 s;
  - setas no último quadro;
  - a transcrição mostra "No lo dejes para después." em 107,66–109,56 s;
  - lipsync do conjunto: 0,26, APROVADO;
  - único aviso: o j1.
- **Emendas, de 1 em 1 quadro em volta dos 18 cortes:** `_v3chk/emendas_1.jpg` e `emendas_2.jpg`. Não há quadro solto.
  - O glitch de 6,6–7,0 s e a troca de plano em 83,87 s vêm do original, iguais na v2.
- **Arquivo:** `AD 13 - ORACION-PAZ-ES-LATAM.mp4`, 119,80 s, 720x1280, 26,3 MB. O vídeo não foi aberto.

### Créditos HeyGen
- Antes: 8.815. Logo depois dos jobs: 8.814, mas a cobrança atrasa até ~1 h.
- Estimativa: 8 jobs speed, somando 57,7 s, ou seja, **~58 créditos**, abaixo do teto de 75. Nenhum job falhou nem foi reenviado.
- **Conferir o saldo de novo cerca de 1 h depois** (esperado ≈ 8.757).

### Pontos para a pessoa olhar
1. **j1 (gancho do Jesus):** o kit dá aviso (0,78 com 8 quadros) por causa da barba, mas a boca está fechada na folha. Vale assistir o fim do gancho.
2. **Frase nova em 107,7 s:** "No lo dejes para después." seguida, 3 s depois, de "No dejes pasar este momento". As duas são suaves, mas parecidas.
3. **w06 e w12 atravessam cortes de câmera** (mesmos limites da v1). Nas emendas não aparece defeito.
