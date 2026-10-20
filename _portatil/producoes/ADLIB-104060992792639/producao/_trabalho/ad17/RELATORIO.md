# AD 17: relatório (PT → espanhol neutro LATAM), 08/10/2026

## Arquivo final
- `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 17 - ORACION-NUDO-ES-LATAM.mp4`
- 87,10 s, 720x1280, 30 fps, AAC, 27,7 MB, −15,2 LUFS, sem selo. Tema: NUDO (a mesma Desatadora com Jesus atrás e a multidão; abre com a cena do homem chorando no quarto).
- O original tem 379 s: a fala acaba em 91,9 s e depois vem a tela parada da cruz com seta. O vídeo termina 0,7 s depois da última fala em espanhol (86,33 s), com fade de 0,3 s.

## Roteiro em espanhol (tempos no vídeo final)
| Tempo | Fala |
|---|---|
| 0,53–7,83 | Vine a traer paz a tu corazón (lote B; antes "alivio") y a desatar el nudo que detiene tu vida. Porque no fue por casualidad que este video llegó hasta ti. |
| 9,95–12,30 | Fuiste tú a quien elegí, entre tanta gente. |
| 12,88–22,21 | Hay una gran bendición separada con tu nombre, y ya viene en camino hacia ti. Pero hay un nudo apretado en medio del camino, que la detiene afuera. |
| 22,43–34,96 | Y ese nudo no lo ataste tú. No es que tu fe sea débil. Rezaste, encendiste velas, hiciste promesas, y aun así no encontrabas descanso. La culpa nunca fue tuya. |
| 35,31–48,60 | Siempre fue ese nudo. Y solo se desata con una oración de nueve palabras, rezada en el orden correcto, como te voy a enseñar. No se trata de rezar más, sino de rezar de la manera correcta. |
| 50,18–59,48 | Y cuando ese nudo se desate, la paz vuelve a tu corazón y la alegría a tu hogar. Esa preocupación que te quita el sueño empieza a aliviarse. |
| 60,36–66,37 | Pero presta mucha atención hasta el final, porque esta oración sagrada fue preparada con amor para ti. |
| 67,23–75,23 | Entonces toca el botón de abajo ahora, porque te dejé un video corto y gratuito con el orden correcto de las oraciones, una para cada nudo. |
| 76,16–86,33 | Pero no lo dejes para después. El enemigo no quiere que este mensaje llegue hasta ti. Toca el botón de abajo, y recibe lo que Dios ya preparó para ti. |

Velocidade: 1,0x (b0, b1, b5, b6, b7, b8), 1,05x (b4), 1,06x (b2), 1,07x (b3).

## Vozes
- **Reaproveitada: "ORACAO-13 mulher" `ZsipxX9wNYg2lJhEScWc`** (Resemblyzer, voz do 17 × fonte do clone do 13): 0,963 na mulher da multidão; 0,899 na cena do quarto (só 9 s, com música). "ORACAO-11 mulher" deu 0,89/0,81. Nenhuma voz nova, nenhuma apagada.

## Custos
- **TTS ElevenLabs:** 1.930 caracteres (9 blocos + 4 refeitos para caber no tempo), ≈ US$ 0,32.
- **HeyGen:** saldo da conta 8.840 antes do lote → 8.824 logo depois (a cobrança atrasa até ~1 h e a conta é compartilhada com outros agentes, então esse número não serve). **Estimativa pela taxa do LICOES:** 88 s em speed (~1 crédito/s ≈ 88) + os mesmos 88 s em precision, disparados antes de o LICOES chegar (~0,26/s ≈ 23) = **≈ 111 créditos**, dentro do teto de 170. A versão precision não foi usada.

## Lipsync (recorte que segue o rosto + PT no vídeo + ES como `audio`, `mode speed`, sem duração dinâmica, mesmo formato, cfr, sem marca d'água)
- 12 trechos, um por tomada (nenhum atravessa corte; trechos < 3 s completados até 3 s com o último quadro e silêncio, e só os quadros reais entram).
- Recorte 9:16 por quadro, centrado no rosto da mulher (landmarks MediaPipe a cada 8 quadros, interpolados e suavizados), empurrado para fora do rosto do Jesus; na tomada final com zoom (78,7–87,1 s) o recorte cresce até o quadro inteiro. Folha das entradas: `lipsync\chk_crops.jpg` (um rosto só em cada).
- Colagem de volta só numa elipse na boca e no queixo, com borda suave, sobre a base sem legenda.

| Trecho | Tempo (s) | Índice de pausa | Corr. ES |
|---|---|---|---|
| s00 | 0,00–9,00 | 0,08 | 0,53 |
| s02 | 9,88–17,46 | 0,43 | 0,32 |
| s03 | 17,46–26,46 | 0,05 | 0,45 |
| s04 | 26,46–36,25 | 0,09 | 0,49 |
| s05 | 36,25–45,88 | 0,05 | 0,40 |
| s06 | 45,88–55,00 | 0,03 | 0,57 |
| s07 | 55,00–64,96 | 0,08 | 0,48 |
| s08 | 64,96–67,17 | 0,04 | 0,78 |
| s09 | 67,17–69,46 | 0,05 | 0,64 |
| s10 | 69,46–75,88 | 0,03 | 0,42 |
| s11 | 75,88–78,71 | 0,05 (era 0,91 REPROVADO) | 0,60 |
| s12 | 78,71–87,04 | 0,16 | 0,48 |

- **Conjunto: 0,08 → APROVADO** (meta ≤ 0,6; AD 11 aprovado 0,38).
- s11 veio reprovado (boca aberta numa pausa de 10 quadros); corrigido sem crédito com `lipsync\fechar_crop.py` (versão do `fechar.py` do AD 01 para a saída recortada: cola a boca mais fechada do próprio trecho, alinhada por olhos e nariz, nas pausas ≥ 6 quadros).
- Todos os trechos voltaram com o número certo de quadros (24 fps): sem reamostragem e sem quadro congelado. Todas as emendas caem em cortes de câmera; o 1º quadro de cada saída é da mesma tomada.
- Glitch do original (9,33–9,83 s) não tem fala em ES nem lipsync; a fala começa depois dele.
- **Fim do s00 (9,00–9,33 s):** a boca original ainda falava PT depois que o ES tinha acabado; esses 8 quadros receberam a boca fechada do próprio trecho (`lipsync\estender.py` + `fechar_crop.py`, sem crédito). Folha: `..\ad18\_rev\fim_s00.jpg` (linha de cima).
- Arquivo remontado depois dessa correção: 87,10 s, 27,6 MB; `revisar_ad.py` de novo **OK** (conjunto 0,08).

## O que saiu ou foi trocado
- **Cura/saúde:** "Eu vim para curar a sua doença, a sua dor" → "Vine a traer alivio a tu corazón"; "a dor no seu corpo não passava", "o nó da escassez e da doença", "a saúde volta para o seu corpo", "aquela dor que te acompanha… começa a ir embora" saíram.
- **Dinheiro:** "o dinheiro sumia da sua mão", "a fartura volta para sua casa", "aquela conta que tira o seu sono, você paga" → "no encontrabas descanso", "la alegría a tu hogar", "esa preocupación que te quita el sueño empieza a aliviarse".
- **Contagem regressiva/ameaça:** "essa revelação vai ser removida / poucos segundos / não fica muito tempo no ar / seja rápido" → "presta mucha atención hasta el final… preparada con amor para ti" e "no lo dejes para después". "Tem quem não queira que esse segredo chegue até você" → "El enemigo no quiere que este mensaje llegue hasta ti" (nível do AD 11/13 aprovados).
- **"Receba o que já é seu por direito"** → "recibe lo que Dios ya preparó para ti".
- **"Agora" no gancho** saiu (sem hora do dia).
- **Imagem:** legenda PT amarela removida com LaMa na GPU, máscara justa (glifo h 22–40 dilatado ~9 px), longe da boca; a **seta vermelha com faíscas do original (69,4 s em diante)** também saiu (2ª passada, `_tmp\seta_patch.py`). Não havia moeda, marca ou famoso do Brasil.
- **Áudio:** narração a −16 LUFS por bloco + fundo do demucs (`no_vocals`, −25 LUFS, sem fala residual) no nível original.

## Revisão própria
- `revisar_ad.py … --idioma es --idioma-residual pt --proibidos "real,reales,dinero,depósito,cantidad,riqueza,cura,curada,enfermedad,cáncer,horas,segundos,aire,borrada" --lipsync <12 trechos>` (PowerShell): **OK, nenhum problema**. es 0,98; nenhum termo proibido; nenhum silêncio > 0,7 s; sem salto de pts; 9 cortes, nenhum par < 0,3 s; setas no último quadro (y 1122–1188). A passada em PT só "traduz" o espanhol (sem fala residual). A transcrição bate com o roteiro.
- **Folha de 1 em 1 quadro em volta dos 11 cortes:** `_rev\cortes.jpg`. Sem quadro solto.
- **Folha de boca (final em cima, original embaixo), 3 pontos por trecho:** `_rev\boca.jpg`. Boca diferente do original e natural, sem emenda visível.
- Folhas do kit: `AD 17 - …_frames.jpg` e `_revisao.jpg/.txt`. O vídeo não foi aberto.

## Pontos para a pessoa olhar
1. **(Resolvido no lote B: frascos apagados, ver abaixo.)** **Cena do quarto (0–9 s):** a mulher de pé é outra atriz (rosto diferente da Desatadora da multidão), mas a voz original é a mesma e o clone também. Em cima da mesa há **frascos de remédio** e um relógio "3:14"; a fala de cura saiu, mas a imagem sugere doença. Ficou como está (não é moeda/marca/famoso).
2. **Glitch de transição (9,3–9,8 s)** é do original.
3. **Legenda em espanhol** em y 1537 (escala 1080), na altura da antiga; setas a partir do 1º "Toca" (67,92 s) até o fim.
4. **Crédito HeyGen:** o lote precision foi disparado antes do LICOES e não foi usado (≈ 23 créditos perdidos).
5. **Duração 87 s** (o original falado tinha 92 s): o roteiro em espanhol ficou mais enxuto depois de tirar cura/dinheiro.

## Arquivos (`producao\_trabalho\ad17\`)
- `_audio\` (orig, demucs, `tts\` b0–b8 + v2, `blocos.json`, `montar_narracao.py`, `tempos_reais.json`); `narracao_es.wav` + alinhamento, `narr_mulher.wav`.
- `_tmp\base_lama.py`, `_tmp\seta_patch.py`, `_tmp\rostos.py` (+ `rostos.json`), `_tmp\cortes.py`, `_tmp\vad.py`, `_tmp\sim.py`.
- `lipsync\`: `segs.json`, `plano.py` (caixas por quadro), `cortar.py`, `up.txt`/`put.sh`, `ids_sp.txt`/`ids_pr.txt`, `baixar.sh`, `out\ls_*.mp4`, `fechar_crop.py`, `recolocar.py`, `checar_v1.log`.
- `base_sem_legenda.mp4`, `base_lipsync.mp4`, `montar_corpo.py`, `corpo_ad17.mp4`, `receita_ad17.json`, `_rev\`.

## Correção do lote B (compliance da abertura + fala), 08/10/2026
1. **Frascos de remédio apagados** (0–9,7 s, q24 0–232, até o fim da transição com brilho).
   - LaMa na GPU (`_vg`), com máscara fixa nos 3 frascos, na tampa solta e na sombra deles (a mesa quase não se move no plano), dilatada ~9 px e com EMA leve no tempo. Script: `_tmp\loteB\frascos_lama.py`; máscara em `frascos_mask.npy`.
   - O copo, o relógio e o celular ficam.
   - Folha: `_tmp\loteB\frascos_antes_depois.jpg` (zoom na mesa).
   - Na 1ª passada sobrava a sombra dos frascos; a máscara foi ampliada para a esquerda.
2. **"alivio" → "paz":** "Vine a traer paz a tu corazón y a desatar el nudo que detiene tu vida. Porque no fue por casualidad que este video llegó hasta ti."
   - TTS do bloco b0 inteiro (130 caracteres, ≈ US$ 0,02) com "ORACAO-13 mulher" `ZsipxX9wNYg2lJhEScWc`: `_audio\tts\b0paz.*`. O `montar_narracao.py` passou a usar o b0paz.
   - A fala vai de 0,53 a 7,83 s (antes, 0,51–8,46).
3. **Avaliação do homem chorando:** está sentado na cama de um quarto, sem leito hospitalar nem aparelhos. Sem os frascos e sem "alivio", a cena lê como tristeza ou aflição, não como doença.
   - **Não reenquadrei**, porque um recorte só na personagem cortaria o homem pela cabeça e pelas mãos no meio do quadro.
   - Fica anotado para a pessoa decidir.
4. **s00 refeito em `mode speed`** (1 job, 9,33 s, 224 quadros), com recorte no rosto (`caixas_s00_X.npy`) sobre a base já sem frascos, PT original no vídeo e o ES novo como `audio`.
   - Parâmetros: sem duração dinâmica, mesmo formato, cfr, sem marca d'água. Job `ac47fb2bdfda49d6b4bb5d6b6a1f1401`; saída `lipsync\out\ls_s00_loteB.mp4`.
   - Voltou com os 224 quadros exatos. Kit na saída: **0,10 APROVADO**, a boca mudou em 100 %, corr. ES 0,61 × PT 0,13.
   - O `cortar.py` agora respeita o `cx` do `segs.json`.
   - Remontado com `recolocar.py s00=lipsync/out/ls_s00_loteB.mp4 s11=lipsync/out/ls_s11_F.mp4`. Os demais trechos ficaram idênticos (diferença média de 2/255, só da recompressão).
- **Remontagem:** `montar_corpo.py 17` → `montar_ad.py`. O final tem 87,10 s e 27,5 MB.
- **Revisão (`revisar_ad.py --lipsync`, PowerShell, proibidos em .txt UTF-8, incluindo "alivio"):** **OK, nenhum problema.**
  - es 0,99, nenhum termo proibido, sem silêncio, 9 cortes sem par < 0,3 s, setas no último quadro;
  - s00 0,11; **conjunto 0,09** APROVADO;
  - os avisos "pixels quase iguais" são o falso alarme conhecido do teste de pixels (grão/recompressão).
  - Trechos em `lipsync\chk\` (`lipsync\trechos.py`). Log: `_revisar_loteB.log`.
  - Folha da boca do s00 (final em cima, original embaixo): `_tmp\loteB\boca_s00.jpg`. A boca é outra e fica fechada de 7,9 a 9,2 s, onde o original ainda fala PT.
  - Folha da abertura (antes × depois, de 0 a 9 s): `_tmp\loteB\folha_abertura.jpg`.
- **Créditos HeyGen:** saldo 8.814 antes e logo depois. A cobrança do speed atrasa até ~1 h; a estimativa é de **~9–10 créditos** (9,33 s).
- **Versões anteriores:** `_antes_loteB\` (final + folhas, as duas bases, corpo, narração e alinhamento, `tempos_reais.json`, `ls_s00*.mp4`, caixas, RELATORIO).

## Correção de cor do lote C (08/10/2026, sem crédito HeyGen)
Motivo: REVISAO-LOTE-C reprovou o 17 pela cor do gancho (s00): área colada −10,5 níveis contra o rosto e rosto −16,6 e magenta contra o original.
- **Versão anterior** guardada em `_antes_cor\` (final + `_frames`/`_revisao`, `base_lipsync`, `corpo_ad17`, RELATORIO).
- **Causa:** cada passada lia com o cv2 (bt709 nos arquivos etiquetados) e gravava em bt601. A `base_sem_legenda` já vinha escurecida (LaMa, frascos, seta), e o recorte do HeyGen levou mais passadas.
- **Geração única** (`_trabalho\_ad1718\recolocar_cor.py 17`), a partir da `base_sem_legenda.mp4` e das saídas do HeyGen já baixadas (`ls_s00_loteB.mp4`, `ls_s02…s12.mp4`, `ls_s11.mp4`):
  - leitura e gravação com a conversão exata do `ad13\lipsync3\comum3.py` (bt601 fixo + `accurate_rnd`, inversa exata, etiqueta bt709 só no bitstream);
  - cor global: afim BGR robusta base → original (48 quadros, alinhamento 0 conferido), aplicada em todos os quadros (`_ad1718\cor_global_17.npy`);
  - cor de cada trecho: afim robusta saída do HeyGen → base corrigida, medida no anel de pele em volta da elipse colada (1,3–2,8x), fora da boca;
  - o `fechar_crop` do s11 foi refeito em memória (`_ad1718\fechar_mem.py`), sem arquivo intermediário. Nenhuma passada repetida.
- **Remontagem:** `montar_corpo.py` → `montar_ad.py receita_ad17.json` (mesma narração, legenda, setas no "toca" 67,92 s). 87,10 s, 29,0 MB.

### Medidas (`revisao\loteC\cor.py` e `brilho.py`, final − original, luma)
| | Antes | Depois |
|---|---|---|
| s00: degrau boca − face (cor / brilho) | −10,5 / −15,2 | −1,0 / +0,3 |
| s00: rosto vs original | −16,6 (U +4,9) | −0,1 (U +0,8) |
| Todos: degrau (cor / brilho) | −3,2 / −6,3 | +1,0 / +0,8 |
| Todos: rosto vs original | −13,2 | −0,6 |
| Fundo vs original | −4,6 | +0,1 |
- s02, s08 e s09 ficam com +3,4 a +5,5 no `cor.py`/`brilho.py`. **Não é cor:** é a boca nova (formato diferente da boca PT nas caixas fixas do lábio e do queixo). Provas:
  - a mediana de final − original dentro da elipse colada contra o anel de pele (`_ad1718\degrau_mediana.py`), que ignora o ± do lábio que mudou de lugar, dá degrau 0 a +1 em todos os trechos (antes: −5 a −11);
  - o mapa de diferença (`_rev_cor\mapa_s08s09.jpg`) só mostra o contorno do lábio, sem mancha elíptica.

### Revisão (`revisar_ad.py --lipsync`, PowerShell, proibidos de `_lote\proibidos.txt`)
- es (0,99), nenhum termo proibido, sem silêncio, setas no último quadro. Log: `_rev_cor\revisar_cor.log`; trechos em `_rev_cor\chk\` (`_ad1718\trechos.py`).
- **Índice de pausa do conjunto: 0,09** (igual ao lote B).
- O script acusa "quadro solto" em 9,63/9,67/9,80 s. É o light-leak do próprio original (9,33–9,83 s): com a cor restaurada, os quadros laranja e rosados voltaram à intensidade do original e passaram do limiar do detector.
  - Na folha `_rev_cor\glitch_9s5.jpg` (novo, anterior e original, de 9,40 a 9,97 s), a sequência é a mesma do original, sem quadro de outra tomada.
  - É o mesmo falso positivo já aceito no AD 10.
