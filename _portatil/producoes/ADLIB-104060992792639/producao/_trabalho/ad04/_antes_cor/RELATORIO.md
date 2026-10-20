# AD 04: relatório (lote PT → espanhol neutro LATAM, 08/10/2026)

## Arquivo final
- `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 04 - ORACION-ENVIDIA-ES-LATAM.mp4`
- 83,10 s, 720x1280, 30 fps, AAC, 26,4 MB, sem selo. Setas a partir do 1º "Toca" (70,15 s) até o fim. Legenda ES pelo alinhamento em y 1360 (escala 1080), na altura da legenda PT antiga.
- O original (83,1 s) não tem tela parada no fim: a última fala ES termina em 82,42 s e o vídeo fecha em 83,10 s com fade de 0,3 s.
- Tema escolhido: ENVIDIA (o nó de inveja).

## Roteiro em espanhol (tempos no vídeo final)
| Tempo | Quem | Fala |
|---|---|---|
| 0,05–9,54 | MENINA | Señor, bendice a la persona que está viendo este video ahora. Te pido que le des la paz que pidió en oración, porque tiene fe y va a escuchar hasta el final. |
| 9,89–15,71 | DESATADORA | Hijo, yo soy la Desatadora de Nudos, tu madre del cielo, y vine a revelarte algo importante. |
| 15,90–20,04 | DESATADORA | Hay alguien cerca de ti que, por pura envidia, ató un nudo en tu vida. |
| 20,23–22,16 | DESATADORA | Ese nudo está apagando tu alegría. |
| 22,47–29,67 | DESATADORA | Por eso sientes que tus esfuerzos se escapan de tus manos, como arena. Por eso trabajas de sol a sol, haces todo bien, |
| 30,06–33,90 | DESATADORA | pero tu corazón sigue cansado, y tus caminos siguen cerrados. |
| 34,45–41,05 | DESATADORA | Me fue revelado cuál fue la atadura. Alguien te miró con envidia, y lanzó palabras escondidas sobre tu vida. |
| 42,35–51,66 | DESATADORA | Pero calma tu corazón, porque tu madre del cielo ya está actuando, y te trajo hasta este video. Cuando el mal es revelado, pierde su fuerza. |
| 51,80–56,97 | DESATADORA | La semana pasada, un hombre que vivía un momento muy difícil hizo esta oración conmigo. |
| 57,33–67,52 | DESATADORA | El nudo se desató, y él sintió una paz y una esperanza que no sentía hacía mucho tiempo. Su corazón volvió a descansar. Ahora es tu turno. |
| 67,77–69,86 | DESATADORA | Te pido solo una cosa, con todo mi amor. |
| 70,15–76,62 | DESATADORA | Toca el botón de abajo para recibir la oración de nueve palabras que desata ese nudo. Te la voy a enseñar gratis. |
| 76,94–82,42 | DESATADORA | No dejes pasar este momento. Toca el botón de abajo, y recibe la oración que preparé para ti. |

Velocidade 1,0x em todos os blocos (nenhum precisou acelerar).

## Vozes (ElevenLabs, nenhuma nova, nenhuma apagada)
- **Desatadora:** "ORACAO-11 mulher" `UNDKAyEJ2rTv99l7gCy5`. Resemblyzer, voz do 04 (demucs, 10–83 s) contra a fonte do clone do 11: **0,99** (contra "ORACAO-13 mulher": 0,87). É a mesma voz.
- **Menina:** "ORACAO-11 menina" `VtWz85Bf8UfJlJLifFE3`. Voz original do 04 contra a fonte do 11: 0,77; o TTS desse clone contra a menina do 04: **0,88** (tom médio 266 Hz contra 261 Hz). Reaproveitado em vez de clonar de só 9,6 s.

## Custos
- **TTS:** 1.251 caracteres (13 blocos, `eleven_multilingual_v2`, 1 geração cada), cerca de US$ 0,21.
- **HeyGen (lipsync `speed`):** 14 jobs somando ~88 s de entrada (13 trechos + 1 refação do w2 de 3,2 s). Pela regra de ~1 crédito/s, **~88 créditos** (teto 170).
  - Saldo medido: 8.829 antes do lote → 8.814 ao fechar AD 04 + AD 06 (a cobrança do speed chega com até 1 h de atraso e a conta é compartilhada com outros agentes, então esse delta ainda não reflete o gasto real).

## Lipsync (HeyGen `speed`, entrada recortada só no rosto de quem fala, áudio PT no vídeo, ES como `audio`, sem duração dinâmica, mesmo formato, cfr, sem marca d'água)
Recortes 9:16 de 288x512 (escala 2,5x), colagem só do nariz ao queixo (elipse suave que segue a boca quadro a quadro). Todos voltaram com o número exato de quadros (w2 e w3, completados até 3,2 s, usam só os quadros reais). Medidos com `checar_lipsync.py --rosto` no trecho colado:

| Trecho | Tempo | Quem / plano | Mudou | Índice de pausa | Corr. ES (PT) | Veredito |
|---|---|---|---|---|---|---|
| g1 | 0,00–9,67 | menina de perfil | — | — (perfil: o MediaPipe não acha o rosto) | — | conferido na folha `lipsync\out\folha_g1.jpg`: boca diferente da original e fechada nas pausas do ES (0,0 / 0,6 / 2,0 / 3,2 / 4,0 / 5,6 / 6,6–6,8 / 7,8 s) |
| w1 | 9,77–17,43 | Desatadora | 94 % | — (5 q de pausa) | 0,34 (0,32) | AVISO; na folha `folha_w1.jpg` fecha nas pausas de 0,7 / 2,7 / 3,9 / 6,0 s |
| w2 | 17,43–20,07 | Desatadora + overlay das invejosas | 85–89 % | — | 0,03–0,04 (0,26) | **REPROVADO 2x** (a refação com recorte mais justo saiu igual) → **boca coberta**: zoom no overlay da mulher invejosa do próprio quadro (recorte 0,660,349,620), áudio intacto |
| w3 | 20,07–22,30 | Desatadora | 88 % | — | 0,43 (0,31) | AVISO (curto, sem pausa) |
| w4 | 22,30–27,00 | Desatadora + overlay do homem | 93 % | — | 0,45 (−0,01) | AVISO (sem pausa) |
| w5 | 27,00–34,77 | Desatadora | 99 % | 0,55 | 0,35 | APROVADO |
| w6 | 34,77–43,07 | Desatadora + anjos | 98 % | 0,36 | 0,38 | APROVADO |
| w7 | 43,07–52,87 | Desatadora | 94 % | 0,07 | 0,46 | APROVADO |
| w8 | 52,87–57,33 | Desatadora + anjos (cena trocada) | 97 % | 0,03 | 0,40 | APROVADO |
| w9 | 57,33–63,53 | Desatadora | 98 % | 0,08 | 0,50 | APROVADO |
| w10 | 63,53–66,80 | Desatadora + anjos (cena trocada) | 95 % | 0,05 | 0,57 | APROVADO |
| w11 | 66,80–77,00 | Desatadora | 96 % | 0,41 | 0,40 | APROVADO |
| w12 | 76,53–83,10 | Desatadora | 95 % | 0,58 | 0,36 | APROVADO |

- **Índice de pausa do conjunto (11 trechos medidos): 0,29** na revisão final (0,28 na 1ª montagem) (meta ≤ 0,6).
- w11 e w12 se sobrepõem 14 quadros (76,53–77,00 s) na mesma tomada: crossfade linear na sobreposição, sem pulo de boca. As outras emendas caem em cortes de câmera.
- Nenhum quadro final tem boca falando português: todos os rostos falando estão em trechos de lipsync ou cobertos (w2).

## O que saiu ou foi trocado
- **Dinheiro:**
  - "envie para ela a quantia que ela pediu" virou "le des la paz que pidió";
  - "esse nó está sugando a tua vida financeira" virou "ese nudo está apagando tu alegría";
  - "o dinheiro entra na tua mão mas some no mesmo dia, igual areia" virou "tus esfuerzos se escapan de tus manos, como arena";
  - "a geladeira continua vazia e o carnê das lojas só acumula juros" virou "tu corazón sigue cansado, y tus caminos siguen cerrados".
- **Depoimento com resultado financeiro e pessoa com nome:** "o seu Roberto, que ia perder o carro na justiça… em menos de três dias um dinheiro esquecido de um antigo fundo foi liberado, quitou o carro à vista e ainda sobrou para um terreno" virou "un hombre que vivía un momento muy difícil… sintió una paz y una esperanza…". Saiu o prazo ("três dias").
- **Imagem:** as duas cenas do depoimento (guincho levando o carro, 52,87–57,33 s; aperto de mão na frente do carro vermelho, 63,53–66,80 s) foram trocadas pelo overlay dos anjos em oração do próprio vídeo (quadros 1046–1179 e 1186–1283), colado só na metade de baixo, com a Desatadora intacta em cima.
- **Ameaça:** "Fechar este vídeo é virar as costas para a tua bênção e entregar a tua riqueza na mão do invejoso" virou "No dejes pasar este momento. Toca el botón de abajo, y recibe la oración que preparé para ti."
- **Acusação a um conhecido:** "alguém que diz ser seu amigo… alguém que já comeu na tua mesa te olhou com falsidade" virou "alguien cerca de ti… alguien te miró con envidia".
- **Outros:** "hoje" e "assustador" saíram ("vine a revelarte algo importante"); "Leva um minuto" virou "con todo mi amor".
- **Mantidos:** a menina orando (gancho), a Desatadora / mãe do céu, o nó de inveja, "cuando el mal es revelado, pierde su fuerza", a "oración de nueve palabras", "gratis" e o CTA "Toca el botón de abajo".
- **Clarão da transição (9,5–10,2 s, quadros 286–305):** a máscara por cor não pegava a legenda PT tingida de vermelho/amarelo e sobrava um fantasma do texto; refeito com máscara de caixa do texto e sem média temporal nesses quadros (`_tmp\lama_flash.py`).
- **Tela:** legenda PT amarela (y 867–947) e as setas vermelhas do original (com os brilhos, quadros ≥ 2100) removidas com LaMa na GPU, máscara justa (glifo + contorno dilatados 9 px; seta preenchida pelo contorno convexo). Boca e queixo (y < 500) não foram tocados.
- **Áudio:** narração a −16 LUFS por bloco + fundo do demucs (`no_vocals`, −45 LUFS, sem fala residual pelo whisper) no nível original.

## Revisão própria
- `revisar_ad.py --idioma es --idioma-residual pt --proibidos "real,reales,dinero,depósito,cantidad,riqueza,cura,curada,enfermedad,cáncer,horas,segundos,aire,borrada" --lipsync <11 trechos>` (PowerShell):
  - idioma es (1,00); **nenhum termo proibido**; a transcrição bate com o roteiro; a passada em pt só "traduz" o espanhol (sem fala residual em português);
  - decodificação OK, sem salto de pts, setas no último quadro;
  - índice de pausa do conjunto **0,29 → APROVADO**; avisos (sem pausa suficiente para o índice) em w1, w3 e w4, conferidos na folha;
  - **1 "problema" que é falso positivo:** "quadro solto? cortes em 9,67 e 9,77 s". É o clarão branco de transição do próprio original entre a menina e a Desatadora (3 quadros de luz), conferido na folha `_tmp\emendas_1.jpg`. Não é quadro de outra tomada.
  - Silêncio 82,36–83,10 s: é o fim com fade (0,7 s depois da última fala), como manda o briefing.
- **Emendas de 1 em 1 quadro em volta dos 12 cortes:** `_tmp\emendas_1.jpg` e `emendas_2.jpg`. Nenhum quadro solto; as trocas de cena (anjos) entram e saem nos cortes do original.
- Folhas: `producao\AD 04 - ORACION-ENVIDIA-ES-LATAM_frames.jpg`, `_revisao.jpg`, `_revisao.txt`; bocas em `lipsync\out\folha_g1.jpg`, `folha_w1.jpg`, `folha_w2.jpg`.
- O vídeo não foi aberto (fica para o revisor independente).

## Pontos para a pessoa olhar
1. **Menina (0–9,7 s):** lipsync em rosto de perfil. A ferramenta automática não mede perfil; na folha a boca muda e fecha nas pausas. Vale olhar.
2. **17,4–20,1 s:** em vez da Desatadora com o overlay, entra um zoom (2x) na mulher invejosa do overlay, porque o lipsync dessa tomada curta não passou duas vezes. Fica um pouco menos nítido e o overlay tem a própria transição borrada nas pontas.
3. **Overlay dos anjos aparece 3 vezes** (34,8–43,1 s original; 52,9–57,3 s e 63,5–66,8 s no lugar do carro). Se incomodar, dá para trocar uma das vezes por outra imagem gerada.
4. **"La semana pasada, un hombre…"** continua sendo um depoimento, agora só com paz/esperanza (sem resultado material). Avaliar contra a política do Meta.
5. **Clarão em 9,67 s:** transição do original, mantida.

## Arquivos de trabalho (`producao\_trabalho\ad04\`)
- Áudio: `_audio\blocos.json`, `gerar_tts.py`, `tts\`, `montar_narracao.py`, `palavras_pt.json`, `sim.py` (semelhança de voz), `demucs\`.
- Base: `_tmp\lama04.py`, `_tmp\montar_base.py` → `base_sem_legenda.mp4`.
- Lipsync: `lipsync\segs.json`, `preparar.py`, `rastrear.py`, `recolocar.py`, `plano.json`, `medir.sh`, `folha.py`, `ids.txt`, `in\`, `out\`.
- Montagem: `base_lipsync.mp4`, `montar_corpo.py`, `corpo_ad04.mp4`, `receita_ad04.json`.
