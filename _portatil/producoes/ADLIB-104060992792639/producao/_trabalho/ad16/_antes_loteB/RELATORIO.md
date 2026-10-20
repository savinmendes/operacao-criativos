# AD 16: relatório (PT → espanhol neutro LATAM), 08/10/2026

## Arquivo final
- `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 16 - ORACION-NUDO-ES-LATAM.mp4`
- 92,40 s, 720x1280, 30 fps, AAC, 27,3 MB, sem selo. Tema: **NUDO**.
- O original tem 379,6 s: a fala vai até 91,9 s, e de 92,4 s ao fim vem uma tela parada (cruz e seta, sem fala), que saiu.
- O corte fica 0,7 s depois da última fala, com fade de 0,3 s.
- Junto: `_frames.jpg`, `_revisao.jpg` e `_revisao.txt`.

## Roteiro em espanhol (tempos no final)
| Tempo | Fala |
|---|---|
| 0,14–4,71 | Vine a traer paz a tu corazón, y a desatar el nudo que detiene tu vida. |
| 6,75–9,63 | Porque no fue por casualidad que este video llegó hasta ti. |
| 10,01–17,83 | Fuiste tú a quien elegí, entre tanta gente. Hay una gran bendición separada con tu nombre, y ya está en camino hacia ti. |
| 17,91–22,18 | Pero hay un nudo apretado en medio del camino, que la detiene del lado de afuera. |
| 22,54–25,40 | Y ese nudo no lo ataste tú. No es que tu fe sea débil. |
| 25,69–33,58 | Rezaste, encendiste velas, hiciste promesas, y aun así tu corazón no encontraba descanso, y ese peso en tu pecho no se iba. |
| 33,68–36,56 | La culpa nunca fue tuya. Siempre fue ese nudo. |
| 36,63–44,48 | Y solo se desata de una manera: con una oración de nueve palabras, rezada en el orden correcto, tal como te voy a enseñar. |
| 44,64–49,05 | No se trata de rezar más. Lo que desata ese nudo es rezar de la manera correcta. |
| 50,31–54,73 | Y cuando se desate, la paz vuelve a tu corazón, y la alegría vuelve a tu hogar. |
| 55,01–60,99 | Las preocupaciones que te quitan el sueño se alivian, y ese peso que te acompaña hace tanto tiempo empieza a irse. |
| 62,66–68,36 | Pero presta mucha atención hasta el final, porque esta oración sagrada fue preparada con amor para ti. |
| 69,84–78,88 | Entonces toca el botón de abajo ahora, porque te dejé un video corto y gratuito con el orden correcto de las oraciones, una para cada nudo. Pero sé rápido. |
| 82,34–87,01 | No dejes pasar este momento. Hay quien no quiere que esta bendición llegue hasta ti. |
| 88,26–91,64 | Toca el botón de abajo, y recibe lo que Dios preparó para ti. |

Velocidade: 1,0x na maioria dos blocos, e 1,04 a 1,087x em b03, b06, b07 e b08.

## Vozes
- **"ORACAO-13 mulher" `ZsipxX9wNYg2lJhEScWc` (reaproveitada).** No Resemblyzer, a voz do 16 contra a voz original do AD 13 dá **0,962**: é a mesma personagem.
- As outras comparações: o TTS desse clone dá 0,910, a Desatadora do AD 05 dá 0,924 e a "ORACAO-11 mulher" dá 0,892.
- Nenhuma voz foi criada nem apagada.

## Custos
- **TTS:** 1.351 caracteres, 15 blocos gerados uma vez só, cerca de US$ 0,22.
- **HeyGen:**
  - **medido:** de 8.823 para 8.815, ou seja, 8 créditos até agora. Foram 13 jobs speed (92,4 s) mais 1 refação do i1 (6,4 s).
  - **esperado:** perto de 1 crédito/s, então cerca de 99 créditos quando a cobrança atrasada (até ~1 h) aparecer. Fica abaixo do teto de 170.
  - A conta é compartilhada com outros agentes.

## Lipsync (`mode speed`, PT original no vídeo, ES separado, recorte no rosto de quem fala)
- **Parâmetros:** `enable_dynamic_duration=false`, `keep_the_same_format=true`, `fps_mode cfr`, sem marca d'água.
- **Recorte:** 288x512 em (350,180), só a mulher, deixando os olhos do Jesus de fora.
  - Na abertura, o recorte foi feito sobre a nova abertura (ver abaixo).
  - O k1 (78,8–87,8 s, com close) foi com quadro inteiro.
- **Retorno:** todos voltaram com o número exato de quadros e sem quadro de outra tomada.

| Trecho | Tempo | Índice de pausa | Corr. ES | Kit |
|---|---|---|---|---|
| a1 | 0,00–9,73 | 0,18 | 0,56 | APROVADO |
| b1 | 9,93–17,57 | — (fala contínua) | 0,32 | AVISO (sem pausa) |
| c1 | 17,57–25,57 | 0,05 | 0,39 | APROVADO |
| c2 | 25,57–36,33 | 0,31 | 0,14 | APROVADO |
| d1 | 36,33–45,97 | 0,16 | 0,43 | APROVADO |
| e1 | 45,97–55,10 | 0,06 | 0,53 | APROVADO |
| f1 | 55,10–65,07 | 0,03 | 0,53 | APROVADO |
| g1 | 65,07–67,27 | — (fala contínua) | 0,36 | AVISO (sem pausa) |
| h1 | 67,27–69,57 | 0,04 | 0,76 | APROVADO |
| i1 → **i1r** | 69,57–75,97 | — (fala contínua) | 0,12 → **0,15** | REPROVADO → **AVISO** |
| j1 | 75,97–78,80 | 0,51 | 0,42 | APROVADO |
| k1 | 78,80–87,77 | 0,09 | 0,82 | APROVADO |
| l1 | 87,77–92,40 | 0,03 | 0,62 | APROVADO |
| **Conjunto** | | **0,13** | | **APROVADO** |

- **i1:** o 1º resultado reprovou por correlação (0,12, sem pausa no ES).
  - Refiz uma vez com um recorte mais justo (216x384 em (342,225)). O i1r deu 0,15 (AVISO) e foi o que entrou.
  - Na folha `_tmp/boca_i1.jpg`, a boca é nova (92 % dos quadros), articula durante toda a fala e fecha nas micropausas de 71,4, 72,0 e 73,2 s.
- **b1 e g1:** a fala ES é contínua, então o índice não se aplica. Na folha `_tmp/boca_b1.jpg`, a boca articula e é diferente da original.
- **Colagem:** só uma elipse na boca e no queixo (`_lote/recolocar.py`).
  - Na emenda c1/c2 (25,57 s, mesma tomada) há mistura de 2 quadros na boca.
  - As outras emendas caem em cortes de câmera.

## O que saiu ou foi trocado
- **Cura e saúde:**
  - "Eu vim para curar a sua doença, a sua dor" virou "Vine a traer paz a tu corazón";
  - "a dor no seu corpo não passava" virou "ese peso en tu pecho no se iba";
  - "nó da escassez e da doença" virou "ese nudo";
  - "a saúde volta para o seu corpo" virou "la paz vuelve a tu corazón";
  - "aquela dor que te acompanha" virou "ese peso que te acompaña".
- **Dinheiro:**
  - "o dinheiro sumia da sua mão" saiu;
  - "a fartura volta para a sua casa" virou "la alegría vuelve a tu hogar";
  - "aquela conta que tira o seu sono você paga" virou "las preocupaciones que te quitan el sueño se alivian".
- **Urgência falsa e contagem regressiva:**
  - "essa revelação vai ser removida / você tem poucos segundos" virou "presta mucha atención hasta el final… fue preparada con amor para ti";
  - "não fica muito tempo no ar" virou "No dejes pasar este momento".
- **"O que já é seu por direito":** virou "lo que Dios preparó para ti".
- **"Agora":** saiu do "chegou até você agora".
- **Mantido:** gancho, a escolha "entre tanta gente", o nó, "no es que tu fe sea débil", "no se trata de rezar más", a "oración de nueve palabras", "pero sé rápido", "hay quien no quiere…" e o CTA "Toca el botón de abajo".
- **Imagem:**
  - **Abertura (0–9,7 s):** era a mulher com a mão na cabeça de um idoso **em cadeira de rodas**, uma cena que lê como cura. Fiz um enquadramento no próprio plano (recorte 360x640 ampliado 2x): ficam a mulher e a cabeça do idoso com as cordas, e a cadeira de rodas sai do quadro.
  - **Transição com glitch (9,73–9,90 s):** mostrava de novo o plano aberto com a cadeira. Virou uma fusão com clarão quente do enquadramento novo para o plano do Jesus.
  - **Legenda PT amarela (y 960–1100):** saiu com LaMa na GPU, com máscara justa.
  - **Seta vermelha animada (69,6–92,4 s, sobre o peito e as cordas):** saiu com máscara fixa, mais o vermelho que escapava nos pulos da seta.
- **Áudio:** narração no nível da voz original, mais o fundo do demucs (`no_vocals`, −25 LUFS), sem fala residual (conferido no whisper PT). O final tem −14,0 LUFS.
- **Legenda nova:** pelo alinhamento, em y 1500 (escala 1080), na altura da antiga e abaixo das mãos. As setas entram no 1º "Toca" (70,45 s) e vão até o fim.

## Revisão própria
- **`revisar_ad.py`** (`--idioma es --idioma-residual pt`, com a lista completa de proibidos e `--lipsync` nos 13 trechos): **OK, nenhum problema**.
  - idioma es (0,98), nenhum termo proibido, nenhum silêncio acima de 0,7 s, pts sem saltos;
  - 9 cortes, sem pares a menos de 0,3 s;
  - setas no último quadro;
  - índice de pausa do conjunto 0,13.
  - Na 1ª montagem, o revisor acusou "quadro solto" em 9,73–9,90 s (o glitch do original, que mostrava o plano aberto). Corrigi com a fusão.
- **Transcrição:** bate com o roteiro. O PT residual é só o espanhol lido como português.
- **Folhas:**
  - `_tmp/cortes.jpg` e `_tmp/cortes_final.jpg`: 1 em 1 quadro em volta dos 12 cortes, sem quadro solto;
  - `_tmp/transicao.jpg`: a fusão nova;
  - `_tmp/boca_a1.jpg`, `boca_b1.jpg` e `boca_i1.jpg`: boca, final x original;
  - `_tmp/chk_lama.jpg`: legenda e seta.
- O vídeo não foi aberto.

## Pontos para a pessoa olhar
1. **Abertura reenquadrada (0–9,7 s):** ampliada 2x, fica mais suave que o resto. O idoso continua no canto inferior (cabeça e cordas), e a cadeira de rodas saiu. Se preferir o plano original, é só trocar, mas ele sugere cura.
2. **Fusão em 9,7–9,9 s:** substitui o glitch rosa/laranja do original.
3. **Trechos de fala contínua** (b1 10–17,6 s, g1 65–67 s, i1 69,6–76 s): o kit só dá AVISO, porque não há pausa para medir. Vale olhar a boca no i1, que tem a correlação mais fraca (0,15).
4. **Onde ficava a seta antiga** (peito e cordas, 69,6–92 s): o preenchimento do LaMa pode tremer de leve nas cordas, mas fica atrás das setas novas.
5. **"Pero sé rápido" e "Hay quien no quiere…":** urgência suave, no nível do AD 13.
6. **Créditos HeyGen:** confira o saldo mais tarde. A cobrança do speed atrasa, e devem cair cerca de 99 créditos por este AD.

## Arquivos e scripts
- **Deste AD:**
  - `_audio\blocos.txt`, `pecas.json`, `lama.json`;
  - `_tmp\crop_abertura.py` (recorte da abertura e fusão);
  - `lipsync\segs.json` e `segs_i1r.json` (este é o usado na montagem final);
  - `lipsync\ids.txt` e `ids_i1r.txt`;
  - `receita_ad16.json`.
- **Scripts do lote:** `_trabalho\_lote\`.
  - `recolocar.py` passou a aceitar elipse de colagem com quadros-chave e colagem de quadro inteiro (`cola: null`).
  - `lama_base.py` ganhou a seta com máscara fixa e `vermelho_extra`.
