# AD 05 — relatório (PT → espanhol neutro LATAM), 07/10/2026

## Arquivo final
`C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 05 - ORACION-FAMILIA-ES-LATAM.mp4`
- 95,5 s · 720x1280 · 30 fps · 27,0 MB · sem selo · setas a partir do primeiro "Toca" (73,4 s) até o fim.
- O original tem 6,4 min, mas só ~98,7 s têm conteúdo. Depois disso vem uma tela fixa (cruz com setas, sem fala) até 385 s, e ela saiu. O corte final fica ~0,7 s depois da última fala, com fade de 0,3 s.
- Também saíram 2,9 s do plano aberto da família (53,6–56,5 s do original). Nesse trecho o marido dizia "e ontem mesmo foi aprovado no meu nome aquele papel…" (promessa financeira), e sem a fala ficaria um silêncio longo.

## Roteiro em espanhol
O arquivo `roteiro_es.txt` traz o roteiro com os tempos.
- **CLARA:**
  - "Toma, mi amor, aquí está tu comida."
  - "Toma, papá, aquí está tu merienda."
  - "Ay, mi amor, es que mi papá no trabaja, y yo tampoco, y siento que traje una carga más a la casa. Como tú eres el único que se esfuerza, trato de ahorrar lo más que puedo. No quiero que mi papá sea una carga para ti."
- **MARIDO:**
  - "Gracias, mi reina."
  - "Amor, ¿por qué le serviste tan poquita comida a tu papá?"
  - "Escucha, Clara. Tu papá no es ninguna carga en esta casa. La comida que compro es para todos, porque este mes se desató un nudo que ataba nuestra vida. Recibí la oración de la Desatadora de Nudos, la novena de las nueve palabras, en mi celular. Recé en el orden correcto, y la bendición que estaba detenida empezó a llegar. Por eso volvió la paz a nuestra casa, y las puertas cerradas empezaron a abrirse."
- **DESATADORA:** "Este es un momento especial, porque cuando este hombre desató su nudo, le prometí que ayudaría a una persona más. Esa persona está viendo este video. Esa persona eres tú. Yo soy la Desatadora de Nudos, y no fue por casualidad que este video llegó hasta ti. No dejes pasar este momento. Toca el botón de abajo ahora: te dejé gratis el video con el orden correcto de las nueve oraciones, una para cada nudo, para desatar lo que ata tu vida. Presta atención: esta ayuda es para ti, y este es tu momento de recibirla. Toca el botón de abajo y recibe gratis la oración que fue preparada para ti."

## Vozes (ElevenLabs, uma por personagem)
| Personagem | Voz | Origem |
|---|---|---|
| Desatadora | "ORACAO-11 mulher" `UNDKAyEJ2rTv99l7gCy5` | **reaproveitada**: semelhança 0,909 (Resemblyzer) com a voz original da Desatadora do 05 |
| Clara (esposa) | "ORACAO-05 Clara (esposa)" `84WxgdFrdm1LAdwbQFZR` | **nova**, clonada de 15 s de fala limpa (demucs) |
| Marido | "ORACAO-05 marido" `Fn4faHoDwi31tC6L06Fl` | **nova**, clonada de 30 s de fala limpa |

"ORACAO-11 menina" não foi usada, porque não há personagem parecida (semelhança ≤ 0,58). Nenhuma voz foi apagada.

## Caracteres de TTS
- **Total:** 3.959 caracteres (~US$ 0,65), gerados em três rodadas:
  - 1ª: 1.583;
  - 2ª: 1.361 (b4, b5 e b6 encurtados para caber);
  - 3ª: 1.015 (b5 e b6 de novo).
- **Velocidade:** Clara 1,05x, marido 1,1x, Desatadora 1,08x. As falas curtas ficaram em 1,0x.
- O vídeo usa só a última versão de cada bloco.

## HeyGen (lipsync)
- **Créditos medidos:** 8.946 antes do lote e 8.931 depois = **15 créditos**, incluindo uma reexecução. O teto era 120.
  - A medição é da conta inteira e pode incluir consumo de outros vídeos rodando em paralelo.
  - Desde o início da sessão: 8.947 → 8.931.
- **Parâmetros:** `precision`, `enableDynamicDuration=false`, `keepTheSameFormat=true`, `fpsMode cfr`, sem marca d'água.
- **Entrada:** o vídeo leva o áudio PT original e o espanhol vai separado, como `audio`.
- **Blocos:** 13, todos com no máximo 11,7 s, num único batch em paralelo:
  - Clara: c1, c2, c3;
  - marido: m1, m2, m3, m4, m5;
  - Desatadora: d1 a d5.
- **Conferência da boca:** diferença média na região. O nível de ruído fica em ~1,5–1,9.
  - **Aprovados:** c1 10,0 · c2 19,4 · c3 16,7 · m1 5,3 · m3 21,5 · m4 15,2 · m5 15,0 · d1 18,9 · d2 20,7 · d3 17,0 · d4 17,0 · d5 23,8.
  - **c1:** tem dois rostos no quadro, mas o lipsync mudou só a boca da Clara.
  - **m1:** fala de 1,4 s; o bloco foi completado até 3 s com quadro congelado e só os 33 quadros reais foram usados. Conferido visualmente.
  - **m2 falhou duas vezes:** pico 2,1 e 2,5, só ruído. É o marido de perfil no plano aberto; foi tentado com recorte ampliado 3x e depois 2x. O trecho ficou com a boca original.
- **Mapas de diferença:** a mudança aparece só no rosto de quem fala. Os rostos ao fundo (a família atrás da Desatadora) não foram alterados.

## O que saiu ou foi trocado
- **Dinheiro:**
  - "paguei todas as contas e ainda sobrou dinheiro", "um depósito aqui, um pix ali" e "aprovado no meu nome aquele papel" viraram "volvió la paz a nuestra casa, y las puertas cerradas empezaron a abrirse";
  - o plano aberto em que essa fala acontecia foi encurtado.
- **Ameaça:**
  - "se você rejeitar essa ajuda agora, o nó continua apertado e a sua bênção fica presa mais uma vez" virou "Presta atención: esta ayuda es para ti, y este es tu momento de recibirla";
  - "Você tem poucos segundos para aceitar" virou "No dejes pasar este momento".
- **Hora do dia e "direito":**
  - "E hoje é um dia especial" virou "Este es un momento especial";
  - "o que já é seu por direito" virou "la oración que fue preparada para ti".
- **Brasil:** "pix" saiu. Não há moeda nem marca brasileira na imagem, então nenhuma cena foi trocada.
- **Mantidos:** a esquete familiar, a Desatadora de Nudos, a "novena de las nueve palabras", o gancho "Esa persona eres tú", a urgência suave e o CTA "Toca el botón de abajo".
- **Legenda PT queimada:** a faixa amarela (y 960–1090) saiu quadro a quadro, com máscara justa (glifo + contorno) e inpaint OpenCV. Rosto e boca não foram tocados.
  - O LaMa ficou inviável: a CPU estava tomada por outros processos, dando ~7 s por quadro, o que somaria ~4,6 h.
  - A placa temporal não serve porque todas as tomadas têm movimento.
  - A legenda nova em espanhol fica na mesma altura (y 1537 na escala 1080).
- **Fundo:**
  - A trilha que o demucs separou (`no_vocals`, ~-35 LUFS) não está muda, então foi mantida no nível original e cortada junto com o vídeo.
  - Não há português residual: a "transcrição pt" do revisor é só o espanhol lido como português.

## Revisão própria
- **`revisar_ad.py --idioma es --idioma-residual pt --proibidos …`:** OK, nenhum problema.
  - Idioma: es (0,98).
  - Nenhum termo proibido.
  - Nenhum silêncio acima de 0,7 s e nenhum salto de pts.
  - 9 cortes de cena, todos do original, sem pares a menos de 0,3 s.
  - Setas presentes no último quadro.
- **Folhas de contato:** `AD 05 - ORACION-FAMILIA-ES-LATAM_revisao.jpg` / `.txt` e `_frames.jpg`.
- **Zoom na boca durante a fala:** 12 pontos, sem deformação, em `_trabalho\ad05\zoom_boca.jpg`.
- O vídeo não foi aberto: fica para o revisor independente.

## Pontos para a pessoa olhar
1. **8,8–11,9 s** ("Amor, ¿por qué le serviste tan poquita comida…"): sem lipsync, porque o HeyGen recusou o rosto de perfil no plano aberto. A boca é a do português, mas o rosto é pequeno e a duração é parecida.
2. **6,1–8,2 s** ("Toma, papá…"): sem lipsync, de propósito. A Clara aparece pequena e logo sai de quadro (close no pai).
3. **Onde ficava a legenda antiga:** sobra uma leve mancha do inpaint em texturas (toalha, avental, cadeira), visível nos intervalos entre as legendas novas.
4. **Plano aberto encurtado em ~53 s:** o plano aberto emenda direto no clarão da transição. Conferir se fica natural.
5. **Duração de 95,5 s:** mais longo que o AD 11, mas o original já era longo.
6. **Setas desde o primeiro "Toca" (73,4 s):** ficam ~22 s na tela. Podem ir para o segundo "Toca" (90,4 s), se preferir.

## Arquivos de trabalho (`producao\_trabalho\ad05\`)
- **Áudio** (`_audio\`):
  - `orig.wav`, `demucs\`, `palavras_pt.json` (whisper com tempo por palavra);
  - `tts\` (b0–b6 e alinhamentos), `montar_narracao.py`, `tempos_reais.json`.
- **Narração montada:** `narracao_es.wav` + `.alinhamento.json`, `narr_clara.wav`, `narr_marido.wav`, `narr_desatadora.wav`, `fundo_es.wav`.
- **Vídeo base:** `_tmp\telea.py` (tira a legenda) e `base_sem_legenda.mp4`, que já tem o corte.
- **Lipsync** (`lipsync\`): `cortar.py`, `blocos.json`, `pt_*`, `es_*`, `ls_*`, `conferir.py`, `recolocar.py`, `ids.txt`.
- **Montagem:** `base_lipsync.mp4`, `montar_corpo.py`, `corpo_ad05.mp4`, `receita_ad05.json`, `roteiro_es.txt`, `zoom_boca.jpg`.

---

# Correção v2 (07/10/2026): bocas em português e manchas da legenda

O arquivo final foi remontado no mesmo caminho, com a mesma receita (`receita_ad05.json`): 95,5 s, 720x1280, 30 fps, 27,0 MB, mesma narração, mesmo corte, setas a partir de 73,4 s e legenda na mesma altura. A versão anterior foi guardada em `_fix\AD05_v1.mp4`, junto com `base_lipsync_v1.mp4` e `corpo_ad05_v1.mp4`.

## 1. Bocas em português (6,1–8,2 s e 8,8–11,9 s)
- **(a) Nova tentativa de lipsync** (precision, PT no vídeo e ES separado, `cortar_v2.py`):
  - `cl`: Clara, tomada 119–161, recorte 270x480 escalado 2,67x e completado até 3 s. Reprovado: "mudou 0%".
  - `cl2`: mesma tomada, recorte 360x640. Reprovado: a boca mudou em 43% dos quadros, mas não acompanha o áudio (corr −0,33). A boca ficava na borda do recorte.
  - `mz`: marido de perfil, 212–286, recorte 180x320 escalado 4x. Reprovado: "mudou 0%".
- **(b) Boca coberta** (`lipsync\cobrir.json`, aplicado em `recolocar_v2.py`), com zoom no próprio quadro e o áudio intacto:
  - **4,96–6,71 s** (quadros 119–161, tomada da Clara servindo): enquadramento nas mãos, no prato e na mesa, recorte (0,500,405,720). A boca da Clara sai do quadro.
  - **8,17–11,92 s** (quadros 196–286, plano aberto): enquadramento na Clara escutando e no pai, recorte (0,260,450,800). O marido, que fala, sai do quadro.
  - **6,7–8,2 s** é o close do pai. Ali a boca da Clara não aparece, então o trecho ficou como estava.
  - Pelo áudio PT (vocals do demucs), a Clara não fala em 8,0–8,9 s, e no recorte ela aparece calada.
- **Também refeitos:** `m3` e `d1`, que o `revisar_ad.py --lipsync` acusou com correlação baixa.
  - `m3` foi aprovado (corr 0,22).
  - `d1` deu corr 0,08 nas duas versões, mas a boca mudou em 99% dos quadros. A fala em espanhol é quase contínua (só duas pausas, de 0,3 e 0,4 s), e nelas a boca fecha (`_fix\d1_boca.jpg`). Ficou a versão nova.
- **Créditos HeyGen:** 8.916 → 8.914 = **2 créditos** em 5 jobs (cl, mz, cl2, m3 r2, d1 r2). A medição é da conta inteira. O teto era 20.

## 2. Manchas da legenda: LaMa na GPU
- **Remoção:** `_fix\lama_gpu.py` roda no `_vg` (torch CUDA, RTX 4070), 2.368 quadros em 170 s.
  - A máscara é **justa**: glifo amarelo mais o contorno escuro, dilatados 9 px e limitados à caixa da legenda.
  - A caixa inteira (1ª rodada) deixava borrão escuro na corda da Desatadora (`_fix\teste_mask.jpg`).
  - Boca e queixo ficam fora da faixa y 960–1090.
- **Base:** `_fix\montar_base_lama.py` gera `base_sem_legenda_lama.mp4`, com o mesmo corte (1286–1355), borda suave e EMA leve que zera nos cortes.
- **Blocos de lipsync de quadro inteiro:** a saída do HeyGen tinha sido gerada sobre a base antiga. A faixa da legenda voltou a ser a do LaMa, só dentro da máscara (`recolocar_v2.py`).
- **Comparação:** `_fix\cmp_telea_lama.jpg`, com OpenCV à esquerda e LaMa à direita.

## Revisão
- **`revisar_ad.py --idioma es --idioma-residual pt --proibidos … --lipsync <12 blocos>`:**
  - es (0,98), nenhum termo proibido, nenhum silêncio, nenhum salto de pts, setas no último quadro;
  - 8 cortes, sem pares a menos de 0,3 s;
  - 10 de 12 trechos de lipsync aprovados.
- **c1:** o revisor mede o rosto do marido, que está calado no quadro. Medido só na Clara (`_fix\ls_c1_clara.mp4`), dá APROVADO: mudou 100%, corr 0,71.
- **d1:** reprovado por correlação (ver acima). É boca nova, não boca em PT.
- **Folhas:**
  - `_fix\zoom_bocas_v2.jpg`: todas as bocas em 58 pontos de fala;
  - `_fix\cobertos_v2.jpg`: 5,9–12 s a cada 0,25 s;
  - `_fix\zoom_faixa_v2.jpg`: a área da antiga legenda sem a legenda nova;
  - `AD 05 …_revisao.jpg/.txt` e `_frames.jpg`.

---

# Correção v3 (08/10/2026): lipsync da Desatadora, m1/m4 e compliance da fala do marido

Remontado no mesmo caminho, com a mesma receita (`receita_ad05.json`): 95,5 s, 720x1280, 30 fps, 27,3 MB, sem selo, setas a partir de 73,4 s e legenda na mesma altura. A v2 foi guardada em `_v2\` (`AD05_v2.mp4`, `base_lipsync_v2.mp4`, `corpo_ad05_v2.mp4`, narração, alinhamento, `tempos_reais.json`, `blocos.json`). Scripts e arquivos desta rodada ficam em `_v3\`.

`LICOES-LIPSYNC.md` ainda não existe. Por isso segui o que o AD 01 já tinha testado em `ad01\lipsync2\` (`preparar.py` e `fechar.py`): a entrada vai recortada só no rosto de quem fala, com o áudio PT de referência, e a boca é fechada nas pausas do ES. O HeyGen (precision) devolve a boca da entrada, ainda falando PT, sempre que a voz nova fica em silêncio.

## 1. Compliance: fala do marido reescrita
- **Saiu:** "La comida que compro es para todos, porque este mes se desató un nudo que ataba nuestra vida" e "la bendición que estaba detenida empezó a llegar". Por precaução também saiu "las puertas cerradas empezaron a abrirse", que pode ser lido como resultado material.
- **Texto novo** (os mesmos espaços de tempo, sem relação entre comida e oração e sem resultado material):
  - "Escucha, Clara. Tu papá no es ninguna carga en esta casa." (27,25–30,25 s)
  - "Lo que hay en la mesa es para todos, porque aquí somos una familia, y nos cuidamos unos a otros." (31,28–35,88 s)
  - "Recibí la oración de la Desatadora de Nudos, la novena de las nueve palabras, en mi celular." (37,30–42,58 s)
  - "Recé en el orden correcto, con fe, y mi corazón encontró descanso." (42,85–46,77 s)
  - "Por eso volvió la paz a nuestra casa, y hoy vivimos con más fe y unión." (47,90–51,60 s)
- **Voz:** "ORACAO-05 marido" `Fn4faHoDwi31tC6L06Fl`, a 1,1x (`_audio\tts\b5v3` + `b5v3s2`). **TTS: 453 caracteres** (357 + 96, ~US$ 0,075).
- **Montagem:** `_audio\montar_narracao_v3.py` refez `narracao_es.wav`, `narr_*.wav`, o alinhamento e `tempos_reais.json`. As falas da Clara e da Desatadora não mudaram.
- O bloco do marido acaba 0,5 s antes do original (51,6 s em vez de 52,1 s). A Desatadora continua começando em 54,3 s.
- O whisper do `revisar_ad.py` transcreveu o texto novo certinho.

## 2. Lipsync refeito (HeyGen, precision, PT no vídeo e ES separado, `_v3\cortar_v3.py`)
| Bloco | Quadros (24 fps) | Entrada |
|---|---|---|
| d1 | 1302–1474 (7,2 s) | recorte 288x512 em (0,150), só no rosto da Desatadora, escala 2,5x. A família fica fora do quadro (`_v3\in_prev.jpg`). |
| d2a / d2b | 1474–1573 / 1573–1712 (4,1 / 5,8 s) | o mesmo recorte. O corte em 1573 cai na pausa entre "eres tú" e "Yo soy". |
| m1 | 87–119 | recorte 450x800 no marido, completado até 3 s |
| m3a / m3b | 653–739 / 739–893 | quadro inteiro (o marido é o único rosto) |
| m4a / m4b | 893–1025 / 1025–1129 | quadro inteiro. O m4 antigo (883–1133) atravessava os cortes de câmera em q893 e q1129, e agora não atravessa mais. |
| m5 | 1129–1271 | quadro inteiro (refeito porque a fala mudou) |

Todos os trechos têm no máximo 8 s, e todos vieram com o número certo de quadros.

**Pós-processamento** (`_v3\processar_v3.py`): em cada pausa do ES com 5 quadros ou mais, inclusive o fim depois da última palavra, a boca e o queixo recebem o quadro mais fechado do próprio trecho. Esse quadro é alinhado por pontos estáveis do rosto e entra com rampa de 3 quadros.

**Recolocação** (`_v3\recolocar_v3.py`): só a parte de baixo do rosto (nariz–queixo) volta para a base limpa (LaMa), com borda suave e o recorte desfeito. Nas emendas da mesma tomada (q739, 1025, 1474 e 1573) entra um crossfade.
- Os outros blocos aprovados (c1–c3, d3–d5) e os trechos cobertos foram refeitos sem perda (`_v3\recolocar_v2_rgb.py`).
- Assim a cor não escurece mais uma vez a cada geração. Na v2, cada nova codificação escurecia ~2,5 níveis, o que criaria salto de brilho em 71,3 s.

**m1 ("Gracias, mi reina"): boca coberta.**
- A saída do HeyGen continuou quase igual à original: no bruto, "mudou" 40 % e corr. 0,83 = REPROVADO; depois do fechamento, AVISO com 72 %; no vídeo montado, REPROVADO com 25 %.
- A tomada inteira (q87–119, de corte a corte) virou um enquadramento nas mãos, no garfo e no prato, recorte (40,560,405,720). O áudio ficou intacto (`_v3\m1_coberto.jpg`).
- Agora 3,6–6,7 s fica todo em enquadramentos de detalhe, em duas tomadas seguidas.

## 3. Índices de pausa (`checar_lipsync.py` novo, medido no vídeo montado, nos mesmos limites da revisão)
| Trecho | Tempo | Índice de pausa (v2 → v3) | Boca mudou | Veredito |
|---|---|---|---|---|
| d1 | 54,25–61,42 | 1,46 → **0,05** | 81 % | APROVADO |
| d2 | 61,42–71,33 | 1,05 → **0,07** | 64 % | APROVADO |
| m3 | 27,21–37,21 | 0,62 → **0,14** | 90 % | APROVADO |
| m4 | 37,21–47,04 | 0,66 → sem pausa ≥ 8 q (a maior tem 5 q) | 81 % | AVISO só por não ter pausa para o índice (corr. ES 0,32) |
| m5 | 47,04–52,96 | 0,17 → **0,13** | 83 % | APROVADO |
| m1 | 3,62–4,96 | coberto | — | — |
| c1, c2, c3, d3, d4, d5 (sem mudança) | — | 0,50 / – / 0,13 / 0,33 / 0,30 / 0,02 | 93–100 % | aprovados (c2 é AVISO por não ter pausa) |

**Saídas cruas do HeyGen**, antes do fechamento: d1 1,51, m5 0,77, m3a 0,19, m3b 0,32. O recorte sozinho não resolveu o d1. O que resolveu foi fechar a boca nas pausas. Os dois logs estão em `_v3\checar_fx.log` e `_v3\med\medida_final_v3.log`.

**60,9–61,4 s** (fim do d1, depois de "…una persona más"): a boca fica fechada (`_v3\folha_bocas_v3.jpg`). As emendas d1→d2a, d2a→d2b, m3a→m3b e m4a→m4b não mostram salto.

## 4. Revisão (`revisar_ad.py --lipsync`, 11 trechos, pelo PowerShell; log em `_v3\revisao_v3.log`)
- **OK, nenhum problema:**
  - es (0,97), nenhum termo proibido;
  - nenhum silêncio acima de 0,7 s, nenhum salto de pts;
  - 8 cortes, sem pares a menos de 0,3 s;
  - setas no último quadro.
- **Índice de pausa do conjunto: 0,18** (APROVADO; na v2 era 0,49).
- Avisos só em c2 e m4, porque esses trechos não têm pausa longa para calcular o índice. Os dois conferidos na folha.

## Créditos
- **HeyGen:** 8.842 → 8.828 = **14 créditos**, em 9 jobs (um único batch, sem reexecução). O teto era 60. A medição é da conta inteira.
- **ElevenLabs:** 453 caracteres.

## Pontos para a pessoa olhar
1. **A fala nova do marido** (31–52 s): confira se soa natural, sobretudo "y nos cuidamos unos a otros" e "hoy vivimos con más fe y unión".
2. **3,6–6,7 s:** duas tomadas seguidas em detalhe (prato/mãos e depois mãos/mesa), por causa da cobertura do m1.
3. **Bocas fechadas nas pausas:** são quadros do próprio lipsync colados na boca. Conferir se não fica "parado" nas pausas mais longas (fim do m3b e do m5, ~1,3 s).
4. `roteiro_es.txt` ainda mostra o texto antigo do marido. O texto que vale é o desta seção.
