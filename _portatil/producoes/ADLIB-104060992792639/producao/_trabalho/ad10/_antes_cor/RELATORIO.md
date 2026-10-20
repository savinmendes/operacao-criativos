# AD 10: relatório (PT → espanhol neutro LATAM), lote 07→08/10/2026

## Arquivo final
- `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 10 - ORACION-NUDO-ES-LATAM.mp4`
- 91,60 s, 720x1280, 30 fps (saída do `montar_ad.py`), AAC, 27,4 MB, sem selo. Junto: `_frames.jpg`, `_revisao.jpg`, `_revisao.txt`.
- Original: 379,6 s. Fala até 92,0 s; depois vem a tela parada da cruz com seta (sem fala), que saiu. Corte 0,7 s depois da última fala (90,84 s), fade de 0,3 s no áudio.
- Formato: cortes + lipsync mantendo o plano original (Jesus atrás, multidão ao fundo). Sem avatar.

## Roteiro em espanhol (tempos no vídeo final; voz a 1,03x, gancho a 1,0x)
| Tempo | Fala |
|---|---|
| 0,18–4,17 | Vine a traer paz a tu corazón, y a desatar el nudo que detiene tu vida. |
| 5,10–8,53 | Porque no fue por casualidad que este video llegó hasta ti ahora. |
| 9,98–12,17 | Fuiste tú a quien elegí entre tanta gente. |
| 12,75–21,85 | Hay una bendición grande separada con tu nombre, y ya está en camino hacia ti. Pero hay un nudo apretado en medio del camino, que la detiene afuera. |
| 22,38–36,67 | Y ese nudo no lo ataste tú. No es que tu fe sea débil. Rezaste, encendiste velas, hiciste promesas, y aun así sentías que tu vida no avanzaba, y tu corazón no encontraba descanso. |
| 37,20–46,38 | La culpa nunca fue tuya. Siempre fue ese nudo. Y solo se desata de una manera: con una oración de nueve palabras, rezada en el orden correcto, como yo te voy a enseñar. |
| 46,86–51,77 | No se trata de rezar más. Lo que desata ese nudo es rezar de la manera correcta. |
| 52,30–64,55 | Y cuando se desate, la paz vuelve a tu corazón, y la alegría vuelve a tu hogar. Esa preocupación que te quita el sueño se alivia, y ese peso que cargas hace tanto tiempo comienza a irse. |
| 65,13–72,57 | Pero presta mucha atención hasta el final, porque este mensaje es para ti, y esta oración sagrada llegó a tu vida por una razón. |
| 73,10–81,90 | Entonces toca el botón de abajo ahora, porque te dejé un video corto y gratuito, con el orden correcto de las oraciones, una para cada nudo. |
| 82,43–86,73 | Pero no dejes pasar este momento. Hay quien no quiere que este secreto llegue hasta ti. |
| 87,26–90,84 | Toca el botón de abajo y recibe lo que Dios ya preparó para ti. |

- A frase "Porque… ahora / Fuiste tú…" foi partida para não cair na transição com brilho do original (9,33–9,83 s).

## Vozes
- **"ORACAO-13 mulher" `ZsipxX9wNYg2lJhEScWc` (reaproveitada)**. Resemblyzer: Desatadora do 10 × mulher do AD 13 **0,965**; × Desatadora do AD 09 0,971; × "ORACAO-11 mulher" 0,892; × menina do 11 0,57. A fala do hospital (0–9,3 s) é a mesma voz (0,929 com a Desatadora do 10).
- Nenhuma voz nova, nenhuma apagada.

## Custos
- **TTS ElevenLabs:** 1.395 caracteres (11 blocos, uma rodada só), ≈ US$ 0,23. No roteiro final: 1.369 (o b1 foi usado em duas partes).
- **HeyGen:** 13 trechos em `mode speed`, 92,7 s de entrada (inclui o enchimento até 3 s dos trechos G, H e J).
  - Saldo da conta: 8.821 antes do lote do AD 10 → 8.816 ao terminar os jobs. **A cobrança do speed atrasa até ~1 h** e a conta é compartilhada, então o débito ainda não apareceu. Estimativa pela taxa do LICOES-LIPSYNC (≈ 1 crédito/s): **~85–93 créditos** (teto atual: 170).

## Lipsync (HeyGen, speed, recorte só no rosto de quem fala)
- Entrada: recorte 9:16 que segue o rosto da mulher quadro a quadro (detecção num recorte ampliado 2x, porque a cena é escura e o MediaPipe falhava no quadro inteiro; escolha do rosto limitada à região da mulher, porque a multidão à direita e o Jesus à esquerda confundiam), escalado para 720x1280, **com o áudio PT original**; o ES separado como `audio`. Parâmetros: speed, `enableDynamicDuration=false`, `keepTheSameFormat=true`, `fpsMode cfr`, sem marca d'água.
- Um trecho por tomada (todas ≤ 10 s), nenhum atravessa corte. Todos voltaram com o número exato de quadros. Recolocação só na elipse boca/queixo, cor bt709/tv.

| Trecho | Tempo | Pausa (HeyGen) | Pausa (final) | Boca mudou (final) |
|---|---|---|---|---|
| h0 (hospital) | 0,00–9,33 | 0,07 | 0,07 | 89 % |
| A | 9,88–17,42 | 0,30 | 0,21 | 32 % |
| B | 17,46–26,42 | 0,03 | 0,04 | 43 % |
| C | 26,46–36,21 | 0,20 | 0,19 | 63 % |
| D | 36,25–45,83 | 0,03 | 0,04 | 72 % |
| E | 45,88–54,96 | 0,08 | 0,09 | 67 % |
| F | 55,00–64,92 | 0,08 | 0,06 | 66 % |
| G | 64,96–67,13 | 0,03 | sem pausa | 77 % (corr. ES 0,46 × PT 0,08) |
| H | 67,17–69,42 | 0,09 | sem pausa | 76 % (corr. ES 0,44 × PT 0,18) |
| I | 69,46–75,83 | 0,03 | 0,03 | 62 % |
| J | 75,88–78,67 | sem pausa | sem pausa | 78 % (corr. ES 0,43 × PT −0,07) |
| K (zoom até close) | 78,71–87,63 | 0,23 | 0,20 | 54 % |
| L | 87,67–91,54 | 0,04 | 0,04 | 80 % |
| **Conjunto** | | | **0,11** | APROVADO (meta ≤ 0,6) |

- Nenhum trecho reprovado, nenhuma refação. G, H e J só têm "aviso" por não terem pausa no ES (fala contínua); a correlação com o ES é bem maior que com o PT.
- Rosto falando fora do lipsync: só os 12 quadros da transição com brilho do original (9,33–9,83 s), com os dois planos sobrepostos e tingidos; ali nem o ES nem o PT falam.

## O que saiu ou foi trocado
- **Cura/saúde:** "Eu vim pra curar a sua doença, a sua dor" → "Vine a traer paz a tu corazón"; "a dor no seu corpo não passava" → "tu corazón no encontraba descanso"; "nó da escassez e da doença" → "ese nudo"; "a saúde volta pro seu corpo" → "la paz vuelve a tu corazón"; "aquela dor que te acompanha há tanto tempo começa a ir embora" → "ese peso que cargas hace tanto tiempo comienza a irse".
- **Dinheiro:** "o dinheiro sumia da sua mão" saiu; "a fartura volta pra sua casa" → "la alegría vuelve a tu hogar"; "aquela conta que tira o seu sono, você paga" → "esa preocupación que te quita el sueño se alivia"; "o que já é seu por direito" → "lo que Dios ya preparó para ti".
- **Urgência com contagem / ameaça:** "essa revelação vai ser removida / você tem poucos segundos" → "presta mucha atención hasta el final, porque este mensaje es para ti…"; "seja rápido, não fica muito tempo no ar" → "no dejes pasar este momento".
- **Mantidos:** a personagem com o Jesus atrás, o nó, a "oración de nueve palabras", "no se trata de rezar más / de la manera correcta", o vídeo curto e gratuito, "hay quien no quiere que este secreto llegue hasta ti" e o CTA "Toca el botón de abajo".
- **Imagem:** legenda PT amarela (y 982–1064) e setas vermelhas PT (a partir de 69,5 s, y 768–975) removidas com LaMa na GPU, máscara justa; a detecção das setas só liga a partir do quadro 1660, para não apagar a túnica vermelha da personagem na cena do hospital. Não há moeda, marca ou famoso do Brasil.
- **Áudio:** narração a −16 LUFS por bloco + fundo do demucs (`no_vocals`, −25,2 LUFS; o whisper não acha fala nele) no nível original.
- **Legenda/setas:** legenda pelo alinhamento, y 1534 (escala 1080); setas a partir do 1º "toca" (73,55 s) até o fim; sem selo.

## Revisão própria
- `revisar_ad.py … --idioma es --idioma-residual pt --proibidos "real,reales,dinero,depósito,cantidad,riqueza,cura,curada,enfermedad,cáncer,horas,segundos,aire,borrada" --lipsync <13 trechos>` (PowerShell):
  - decodificação OK, sem saltos de pts, nenhum silêncio > 0,7 s; setas no último quadro;
  - idioma es (0,98), **nenhum termo proibido**, sem fala residual em PT; transcrição bate com o roteiro;
  - lipsync: 10 APROVADO + 3 aviso (sem pausa), conjunto **0,11**;
  - 1 "PROBLEMA": "quadro solto? cortes em 9,63 e 9,80 s". É a **transição com brilho do próprio original** (9,33–9,83 s, várias mudanças de quadro seguidas, igual no `10.mp4`), não um quadro solto da edição. Conferido na folha de 1 em 1 quadro.
- Folha de 1 em 1 quadro em volta dos cortes: `_tmp\cortes_final.jpg` — sem quadro solto.
- Zoom do rosto final × original (inclusive o close de 85 s): `lipsync\chk\rosto_zoom.jpg` — sem emenda visível.

## Pontos para a pessoa olhar
1. **(Resolvido no lote B: abertura reenquadrada, ver abaixo.)** **Cena do hospital (0–9,3 s):** idoso entubado no leito, com a personagem ao lado. A fala de cura saiu ("Vine a traer paz a tu corazón"), mas a imagem ainda sugere contexto de doença. Não foi trocada (não há outro plano do próprio vídeo para cobrir 9 s de fala da personagem). Avaliar contra a política do Meta para saúde.
2. **Créditos HeyGen:** conferir o saldo daqui a ~1 h (estimativa ~85–93 créditos para este AD).
3. **Transição com brilho em 9,33–9,83 s** (original): o revisor automático acusa como quadro solto; é o efeito da fonte.
4. **Fantasma das setas antigas** (69,5–91 s, sobre as cordas): mancha leve do inpaint, em parte coberta pela legenda e pelas setas novas.
5. **"Hay quien no quiere que este secreto llegue hasta ti"** mantido (nível do AD 13 aprovado).

## Arquivos de trabalho (`producao\_trabalho\ad10\`)
- Áudio (`_audio\`): `orig.wav`, `demucs\`, `palavras_pt.json`, `sim.py`, `tts\b0–b10`, `blocos.json` (com corte "de/até" dentro do b1), `montar_narracao.py`, `tempos_reais.json`.
- Base (`_tmp\`): `lama_gpu.py` (3º argumento = quadro em que as setas começam), `montar_base.py` → `base_sem_legenda.mp4`.
- Lipsync (`lipsync\`): `segs.json` (com `busca`/`roi`/`regra` por tomada), `preparar.py`, `in\`, `up.tsv`, `ids.txt`, `out\`, `chk_heygen.txt`, `recolocar.py`, `plano.json`, `trechos.py`, `chk\`.
- Montagem: `base_lipsync.mp4`, `montar_corpo.py`, `corpo_ad10.mp4`, `receita_ad10.json`.

## Correção do lote B (compliance da abertura), 08/10/2026
- **Defeito (revisor):** de 0 a 9,3 s aparecia um idoso entubado no leito, com monitor e oxigênio, sob "Vine a traer paz a tu corazón". Isso lê como cura pela fé (risco alto no Meta).
- **Correção (sem crédito):** reenquadrei a abertura **só na personagem**, como no AD 16.
  - Recorte 320x569 em (400,230), ampliado 2,25x com Lanczos, nos quadros q24 0–232. Isso inclui a transição com brilho até o último quadro do plano do hospital; do q233 em diante já é o plano do Jesus.
  - O recorte foi aplicado sobre a `base_lipsync.mp4` **já sincronizada**, então o lipsync do h0 continua o mesmo. Script: `_tmp\loteB\reenquadrar.py`.
  - Saem do quadro o leito, o idoso, o tubo, o monitor e os aparelhos. Fica a personagem do véu ao rosário, contra a cortina escura.
- **Folha da abertura:** `_tmp\loteB\folha_abertura_reenquadrada.jpg`.
  - Linha 1: antes. Linha 2: depois, de 0 a 9 s.
  - Linhas 3 e 4: a transição de 9,0 a 9,9 s, quadro a quadro.
  - Nenhum quadro mostra leito ou monitor.
- **Remontagem:** `montar_corpo.py 10` → `montar_ad.py`. O final tem 91,60 s e 27,4 MB.
- **Revisão (`revisar_ad.py --lipsync`, PowerShell, proibidos em .txt UTF-8):**
  - es 0,98, nenhum termo proibido, sem silêncio;
  - h0 checado contra o original recortado igual (`lipsync\chk\orig_h0_crop.mp4`, rosto 33;186;326;387): **0,09 APROVADO**, a boca mudou em 80 % dos quadros;
  - **conjunto 0,12** APROVADO.
  - O único "PROBLEMA" é o quadro solto em 9,63/9,67 s. É a transição com brilho do próprio original, o mesmo falso positivo de antes, conferido na folha.
  - Log: `_revisar_loteB.log`.
- **Pontos para olhar:**
  - a abertura ampliada 2,25x fica mais suave que o resto do vídeo, como no AD 16;
  - no canto superior esquerdo do recorte, uma bolsa de soro muito escura pode aparecer contra a cortina (quase invisível na folha).
- **Versões anteriores:** `_antes_loteB\`. **Créditos HeyGen:** 0.
