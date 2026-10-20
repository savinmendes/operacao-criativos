# AD 09: relatório (PT → espanhol neutro LATAM), lote 07→08/10/2026

## Arquivo final
- `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 09 - ORACION-SERPIENTES-ES-LATAM.mp4`
- 103,30 s, 720x1280, 30 fps (saída do `montar_ad.py`), AAC, 26,8 MB, sem selo. Junto: `_frames.jpg`, `_revisao.jpg`, `_revisao.txt`.
- Original: 392,6 s. Conteúdo com fala até 105,3 s; depois vem a tela parada da cruz com seta "CLIQUE" (sem fala), que saiu. Corte 0,7 s depois da última fala (102,57 s), fade de 0,3 s no áudio.
- Formato: cortes + lipsync mantendo o plano original (Jesus atrás). Sem avatar.

## Roteiro em espanhol (tempos no vídeo final; voz a 1,04x, gancho a 1,0x)
| Tempo | Fala |
|---|---|
| 0,28–7,56 | En este momento, estoy quitando de tu camino las serpientes que se enredaron en tu vida y no dejan llegar tu bendición. |
| 8,98–18,98 | Yo soy la Desatadora de Nudos, y no fue por casualidad que vine a hablar contigo. Fuiste tú a quien elegí entre tanta gente, para recibir lo que estaba guardado para ti. |
| 19,51–24,98 | Hay una bendición grande separada con tu nombre, y ya salió, ya está en camino hacia ti. |
| 25,51–33,75 | Pero hay un nudo apretado en medio del camino, que la detiene afuera. Y ese nudo no lo ataste tú. No es que tu fe sea débil. |
| 34,23–39,55 | Rezaste, encendiste velas, hiciste promesas, y aun así sentías que tu vida no avanzaba. |
| 40,08–55,33 | La culpa nunca fue tuya. Siempre fue ese nudo, y se desata con una oración de nueve palabras, rezada en el orden correcto. No se trata de rezar más. Lo que desata ese nudo es rezar de la manera correcta. |
| 55,91–64,21 | Y cuando ese nudo se desate, la bendición que estaba detenida va a empezar a llegar, y tu vida entra en un tiempo de paz y de alegría. |
| 64,74–71,72 | Esa preocupación que te quita el sueño se alivia, y por primera vez en mucho tiempo, tu corazón descansa sin ese peso en el pecho. |
| 72,25–79,60 | Pero presta mucha atención hasta el final, porque este mensaje es para ti, y esta oración sagrada llegó a tu vida por una razón. |
| 80,12–90,95 | Entonces toca el botón de abajo ahora, porque te dejé un video corto y gratuito, con el orden correcto de las oraciones, una para cada nudo, comenzando por el primero, el que más aprieta tu vida. |
| 91,48–98,69 | Pero no dejes pasar este momento. Guarda esta oración en tu corazón. Hay quien no quiere que este secreto llegue hasta ti. |
| 99,22–102,57 | Toca el botón de abajo y recibe lo que Dios ya preparó para ti. |

## Vozes
- **"ORACAO-13 mulher" `ZsipxX9wNYg2lJhEScWc` (reaproveitada)** para a Desatadora e para a mulher do espelho (0–8,3 s). Resemblyzer:
  - Desatadora do 09 × voz original da mulher do AD 13: **0,952** (× "ORACAO-11 mulher": 0,861; × Desatadora do AD 05: 0,921; × menina do 11: 0,54).
  - Mulher do espelho × Desatadora do 09: 0,886 (mesma voz, trecho curto e com eco). Na fonte, a mesma voz faz as duas falas.
- Nenhuma voz nova, nenhuma apagada.

## Custos
- **TTS ElevenLabs:** 2.021 caracteres gerados (1.647 da 1ª rodada + 374 do b1 e b5 encurtados para caber), ≈ US$ 0,33. No roteiro final: 1.574.
- **HeyGen:** 18 trechos em `mode speed`, 106,2 s de entrada no total (inclui o enchimento até 3 s dos trechos curtos D, N, O e P).
  - Saldo da conta: 8.839 no início do AD 09 → 8.826 antes do lote → 8.821 ao terminar os jobs → 8.816 depois do AD 10. **A cobrança do speed atrasa até ~1 h**, e outros agentes usam a mesma conta: o débito real deste AD ainda não apareceu. Pela taxa do LICOES-LIPSYNC (≈ 1 crédito/s em speed), a estimativa é **~100–106 créditos** (abaixo do teto de 170 do briefing atualizado; acima do teto antigo de 90, que valia quando o lote foi disparado em speed).

## Lipsync (HeyGen, speed, recorte só no rosto de quem fala)
- Entrada: recorte 9:16 que segue o rosto da mulher quadro a quadro (MediaPipe, suavizado), com o rosto do Jesus apagado por inpaint dentro do recorte, escalado para 720x1280, **com o áudio PT original**; o ES vai separado como `audio`. Parâmetros: speed, `enableDynamicDuration=false`, `keepTheSameFormat=true`, `fpsMode cfr`, sem marca d'água.
- Trechos ≤ 12 s, um por tomada (a tomada 40,0–54,2 s foi dividida em E1/E2 por ter 14 s; a emenda E1|E2 levou fusão de boca de 4 quadros). Nenhum trecho atravessa corte.
- Recolocação: só uma elipse boca/queixo do rosto (borda suave) volta para a base limpa; 1 trecho voltou com 1 quadro a menos (E1, 169/170) e foi reamostrado no tempo (sem congelar). Cor bt709/tv.
- Índice de pausa (meta ≤ 0,6) medido na saída do HeyGen (`checar_lipsync.py`, saída × entrada) e no trecho colado no vídeo final (`revisar_ad.py --lipsync`):

| Trecho | Tempo | Pausa (HeyGen) | Pausa (final) | Observação |
|---|---|---|---|---|
| m0 (espelho) | 0,00–8,33 | 0,14 | 0,20 | APROVADO |
| A | 8,83–18,54 | 0,07 | 0,07 | |
| B | 18,54–28,33 | 0,20 | 0,23 | |
| C | 28,33–37,96 | 0,06 | 0,06 | |
| D | 38,00–40,04 | 0,04 | 0,02 | ver nota 1 |
| E1 | 40,04–47,12 | 0,51 | 0,60 | no limite |
| E2 | 47,12–54,21 | 0,04 | 0,04 | zoom in |
| F | 54,21–61,54 | 0,27 | 0,32 | |
| G | 61,54–71,54 | 0,09 | 0,16 | |
| H | 71,54–76,42 | 0,01 | 0,02 | |
| I | 76,42–79,50 | sem pausa | sem pausa | corr. ES 0,47 × PT 0,35 |
| J | 79,50–82,92 | 0,03 | 0,03 | |
| K | 82,92–86,46 | sem pausa | sem pausa | corr. ES 0,44 × PT 0,25 |
| L | 86,46–91,38 | 0,05 | 0,04 | |
| M | 91,38–96,75 | 0,21 | 0,24 | |
| N | 96,75–99,33 | 0,02 | 0,02 | |
| O | 99,33–100,67 | 0,03 | sem pausa | ver nota 2 |
| P | 100,67–103,30 | 0,02 | 0,03 | |
| **Conjunto** | | | **0,16** | APROVADO (meta ≤ 0,6) |

- Na saída do HeyGen, todos os 18 deram APROVADO (boca mudou em 75–100 % dos quadros).
- **Nota 1 (D):** no vídeo final o revisor acusa "boca não mudou (20 %)". É falso alarme do teste de pixels: o original tem grão forte e a região de controle já difere ~9/255 entre final e original (recompressão), então a boca nova (~16/255) não passa o limiar. Na folha `lipsync\chk\boca_D_O.jpg` (final em cima, original embaixo) a boca é outra e **fecha em 39,5–40,0 s, onde o ES está calado e o PT ainda falava**. Na saída do HeyGen o D deu 75 % de mudança, índice 0,04.
- **Nota 2 (O):** 1,3 s de fala contínua, sem pausa para o índice; a correlação curta deu 0,04. Na folha `lipsync\chk\boca_O.jpg` a boca é diferente da original e articula; na saída do HeyGen (com o enchimento) deu 0,03 APROVADO.
- Os "avisos" de "pixels quase iguais" nos outros trechos têm a mesma causa (grão/recompressão); o índice de pausa de todos fica ≤ 0,6.
- Nenhuma refação foi necessária. Nenhum quadro final tem boca falando PT: os 103,3 s estão cobertos por lipsync, exceto a transição com brilho de 8,33–8,83 s (do original), em que nem o ES nem o PT falam.

## O que saiu ou foi trocado
- **Dinheiro:** "bênção financeira grande" → "bendición grande"; "o dinheiro entrava numa mão e sumia na outra" → "sentías que tu vida no avanzaba"; "nó da escassez e da pobreza" → "ese nudo"; "tempo de fartura e de multiplicação" → "tiempo de paz y de alegría"; "aquela conta que tira o seu sono você paga" → "esa preocupación que te quita el sueño se alivia"; "o que já é seu por direito" → "lo que Dios ya preparó para ti".
- **Urgência com contagem / ameaça:** "essa revelação vai ser removida e você tem poucos segundos" → "presta mucha atención hasta el final, porque este mensaje es para ti…"; "seja rápido, uma revelação dessas não fica muito tempo no ar" → "no dejes pasar este momento. Guarda esta oración en tu corazón."
- **Hora do dia:** "vim falar com você hoje" e "aperta a sua vida hoje" perderam o "hoje".
- **Entrou** a "oración de nueve palabras" (o original tinha a frase truncada "Sempre foi esse nó, rezada na ordem certa").
- **Mantidos:** gancho das serpentes no espelho, a Desatadora com o Jesus atrás, o nó, "no se trata de rezar más / de la manera correcta", o vídeo curto e gratuito, "hay quien no quiere que este secreto llegue hasta ti" e o CTA "Toca el botón de abajo".
- **Imagem:** legenda PT amarela (y 982–1064) e as setas vermelhas PT com brilhos (77–105 s, y 760–975) removidas com LaMa na GPU, máscara justa (glifo + contorno dilatados 9 px; seta + borda branca), longe da boca (y ≈ 400–560). Não há moeda, marca ou famoso do Brasil na imagem.
- **Áudio:** narração a −16 LUFS por bloco + fundo do demucs (`no_vocals`, −27,5 LUFS, sem fala residual: o whisper só alucina "Legendas pela comunidade Amara.org" em 0–2 s) no nível original.
- **Legenda/setas:** legenda pelo alinhamento, y 1534 (escala 1080), na altura da antiga e longe da boca; setas do kit a partir do 1º "toca" (80,6 s) até o fim; sem selo.

## Revisão própria
- `revisar_ad.py … --idioma es --idioma-residual pt --proibidos "real,reales,dinero,depósito,cantidad,riqueza,cura,curada,enfermedad,cáncer,horas,segundos,aire,borrada" --lipsync <18 trechos>` (PowerShell):
  - decodificação OK, pts do áudio sem saltos, nenhum silêncio > 0,7 s;
  - 15 cortes, nenhum par a < 0,3 s; setas no último quadro;
  - idioma es (0,98); **nenhum termo proibido**; a passada em PT só "traduz" o espanhol (sem fala residual);
  - transcrição bate com o roteiro;
  - lipsync: conjunto 0,16 APROVADO; 2 "PROBLEMA" (D e O), explicados nas notas 1 e 2 (falso alarme do teste de pixels / trecho curto sem pausa).
- Folha de 1 em 1 quadro em volta dos 18 cortes: `_tmp\cortes_final.jpg` — sem quadro solto, sem cena repetida.
- Zoom do rosto final × original: `lipsync\chk\rosto_zoom.jpg` — sem emenda visível da elipse.

## Pontos para a pessoa olhar
1. **Créditos HeyGen:** o speed custa ~1 crédito/s e a cobrança atrasa; conferir o saldo daqui a ~1 h (estimativa ~100–106 créditos para este AD).
2. **E1 (40,0–47,1 s):** índice 0,60, no limite; vale olhar se a boca abre em alguma micro-pausa.
3. **Fantasma das setas antigas** (77–103 s, sobre as mãos e as cordas): ficou uma mancha leve do inpaint; as setas e a legenda novas cobrem parte dela.
4. **Mulher do espelho (0–8,3 s):** usa a mesma voz da Desatadora, como no original.
5. **"Hay quien no quiere que este secreto llegue hasta ti"** foi mantido (nível do AD 13 aprovado: não ameaça quem assiste).

## Arquivos de trabalho (`producao\_trabalho\ad09\`)
- Áudio (`_audio\`): `orig.wav`, `demucs\`, `palavras.py`/`palavras_pt.json`, `sim.py` (Resemblyzer), `tts\b0–b11` (+ alinhamentos), `blocos.json`, `montar_narracao.py`, `tempos_reais.json`.
- Base (`_tmp\`): `cortes.py`, `faixa.py`, `lama_gpu.py` (legenda + setas), `montar_base.py`, `folha.py`, `folha_cortes.py` → `base_sem_legenda.mp4`.
- Lipsync (`lipsync\`): `segs.json`, `preparar.py` (recorte que segue o rosto + inpaint do outro rosto), `in\`, `up.tsv`, `ids.txt`, `baixar.sh`, `out\`, `chk_heygen.txt`, `recolocar.py` (elipse boca/queixo, reamostragem, fusão nas emendas), `plano.json`, `trechos.py`, `folha_boca.py`, `chk\`.
- Montagem: `base_lipsync.mp4`, `montar_corpo.py`, `corpo_ad09.mp4`, `receita_ad09.json`.

## Correção do lote B (revisão independente `revisao\REVISAO-LOTE-B.md`), 08/10/2026
- **Defeito:** em 46,93–47,07 s (fim do E1, q24 1126–1130) a boca abria mostrando os dentes, como no original (PT), numa pausa do ES.
- **Correção (sem crédito):** `lipsync\fechar_e1.py` cola nesses quadros a boca mais fechada de 46,77–46,90 s (ref. q1124, abertura 0,055), alinhada por olhos e nariz, só boca e queixo. O q1130, que é o ataque da fala ES seguinte, entra com peso 0,6.
  - Abertura nos 5 quadros: 0,096–0,117 → 0,057–0,063 (q1130: 0,085).
  - Folha `_tmp\loteB_E1_boca.jpg` (antes em cima, depois embaixo): os dentes somem e fica o "o" fechado da referência.
- **Remontagem:** `base_lipsync.mp4` → `montar_corpo.py 09` → `montar_ad.py receita_ad09.json`. O arquivo final continua com 103,30 s e 26,8 MB.
- **Revisão (`revisar_ad.py --lipsync`, PowerShell, proibidos em `revisao\proibidos_loteB.txt` UTF-8):**
  - es 0,98, nenhum termo proibido (lista do briefing + a do revisor + "alivio"), sem silêncio, sem salto de pts, 15 cortes sem par < 0,3 s;
  - **E1: 0,60 → 0,56**; **conjunto 0,15** APROVADO;
  - o único "PROBLEMA" é o O (correlação 0,04, sem pausa), o mesmo de antes, explicado na nota 2. Log: `_revisar_loteB.log`.
- **Versões anteriores:** `_antes_loteB\` (final + folhas, `base_lipsync.mp4`, `corpo_ad09.mp4`, RELATORIO).
- **Créditos HeyGen:** 0.
