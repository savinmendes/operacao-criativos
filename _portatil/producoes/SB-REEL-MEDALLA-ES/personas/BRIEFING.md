# Série Medalla — 10 vídeos (13/10/2026)

Modelo de montagem: `_trabalho\montar_app.py` + `legenda_app.py` (motorista de app, versão final). O trecho do SACERDOTE é IDÊNTICO em todos (clipes `avatar2\sacA_high.mp4`/`sacB_high.mp4`, voz e b-rolls da v2, CTA, selo "VIDEO FICTICIO"). Não gerar nada novo para o sacerdote.

## Falas comuns
- Fala 1 (reza, sussurrada): "Oh glorioso San Benito, hoy pronuncio las palabras grabadas en tu medalla."
- Fala 4 (selfie): "Hasta que, en una transmisión en vivo, un padre explicó la forma exacta de pedirle a San Benito."
- Sacerdote: idêntico à v2.

## Vozes
- Masculina: Santiago `VXZKNah1ssrzM8c81OiY` (as falas 1 e 4 já existem: corte da v2/taxista em vez de regerar).
- Feminina (55+): Grandma Aurora `aYQAm4rWuigkeuRA5i92` (es-latin-american). Para a MÃE SOLO (45), escolha 1 voz feminina latina de meia-idade da biblioteca e anote.
- Femininas: gerar as falas 1 e 4 UMA vez por voz e reaproveitar entre os vídeos dessa voz.

## Personas (fala 2 / fala 3 / fala 5 · cena de abertura → virada)

| # | Saída | Voz | Fala 2 | Fala 3 | Fala 5 | Abertura (antes) | Virada (depois) |
|---|---|---|---|---|---|---|---|
| 1 | ~~taxista v2~~ | — | CANCELADO pela pessoa (13/10/2026) | | | | |
| 2 | SB-ES_COSTURERA_FICTICIO.mp4 | Aurora | Sácame de esta escasez. Si me escuchas… ayúdame. | Pasé casi seis meses sin un solo encargo. Mi máquina se quedó quieta y llegué a pensar en venderla. | Ese día recuperé la paz. Y poco a poco, las puertas empezaron a abrirse. | Costureira 60+ ajoelhada no ateliê em casa, máquina parada, tecidos intocados | Ateliê com encomendas, cliente provando roupa, ela sorrindo |
| 3 | SB-ES_ABUELA_FICTICIO.mp4 | Aurora | Devuélveme a mi familia. Si me escuchas… no me dejes sola. | Pasé años poniendo la mesa para todos… y comiendo sola. Mis hijos ya ni me llamaban. | Ese día recuperé la paz. Y poco a poco, mi casa volvió a llenarse. | Avó 70+ rezando diante de mesa posta com cadeiras vazias | Família reunida à mesa, netos, ela servindo |
| 4 | SB-ES_MADRE_FICTICIO.mp4 | (meia-idade) | Protege a mis hijos. Si me escuchas… dame fuerzas. | Trabajaba de sol a sol y aun así las cuentas no cerraban. Lloraba en la cocina cuando los niños dormían. | Ese día recuperé la paz. Y poco a poco, las puertas empezaron a abrirse. | Mãe 45 ajoelhada na cozinha à noite, contas na mesa | Manhã clara, filhos tomando café, ela sorrindo |
| 5 | SB-ES_FERIA_FICTICIO.mp4 | Aurora | Quita lo que cerró mi camino. Si me escuchas… ayúdame. | Mi puesto estaba lleno de fruta y nadie se acercaba. Yo sentía que alguien me había echado la envidia encima. | Ese día recuperé la paz. Y poco a poco, la gente volvió a mi puesto. | Feirante 55 rezando atrás da barraca vazia, garoa | Barraca com fila de clientes, sol |
| 6 | SB-ES_CAMPESINO_FICTICIO.mp4 | Santiago | Mira mi tierra. Si me escuchas… no me abandones. | Pasé meses viendo mi tierra secarse. Llegué a pensar que lo iba a perder todo. | Ese día recuperé la paz. Y poco a poco, todo volvió a florecer. | Agricultor 65 ajoelhado na terra rachada, plantação seca | Chuva sobre plantação verde, ele de braços abertos |
| 7 | SB-ES_DESEMPLEADO_FICTICIO.mp4 | Santiago | Sácame de esta escasez. Si me escuchas… ayúdame. | A mis cincuenta y tantos me quedé sin trabajo. Toqué mil puertas y en todas me dijeron que no. | Ese día recuperé la paz. Y poco a poco, las puertas empezaron a abrirse. | Homem 55 de camisa social rezando sentado num banco de praça, pasta no colo | Ele apertando a mão de alguém num escritório, sorrindo |
| 8 | SB-ES_PAREJA_FICTICIO.mp4 | Aurora (ela narra) | Devuelve la paz a mi casa. Si me escuchas… ayúdanos. | Mi esposo y yo vivíamos bajo el mismo techo como dos extraños. Cada uno en un cuarto, sin hablarnos. | Ese día recuperé la paz. Y poco a poco, volvimos a reír juntos. | Ela 60+ ajoelhada no quarto; casa em silêncio, ele sozinho na sala | Os dois rindo juntos na varanda |
| 9 | SB-ES_UCI_FICTICIO.mp4 | Aurora | No me lo quites. Si me escuchas… dame fuerzas. | Pasé días y noches en esa sala, mirando las máquinas, sin saber si él iba a despertar. Sentía que me estaba apagando por dentro. | Ese día recuperé la paz. Y poco a poco, volví a tener esperanza. | Mulher 55 ajoelhada ao lado do leito de UTI à noite, segurando a mão do marido, monitores, luz azul | OPÇÃO B (decisão da pessoa): ele abre os olhos e aperta a mão dela (ou os dois saindo juntos do hospital) |
| 10 | SB-ES_PENSION_FICTICIO.mp4 | Aurora | Sácame de esta escasez. Si me escuchas… ayúdame. | Pasé casi seis meses con todas las llaves colgadas. Ni un solo huésped. Llegué a pensar en cerrar mi pensión. | Ese día recuperé la paz. Y poco a poco, las puertas empezaron a abrirse. | Dona de pensão 60 rezando na recepção, quadro com todas as chaves penduradas | Chaves quase todas fora, hóspedes chegando com malas |

## Regras de produção (aprendidas nesta série)
- Personagens fictícios, rostos novos só por texto; retrato primeiro e usado como referência nas outras 2 imagens.
- Kling: NADA de porta abrindo/fechando nem pessoa entrando/saindo de veículo; movimento contido. Close gerado já fechado (zoom ≤ 1,15).
- HeyGen selfie: sem `fechar_boca`, sem quadro segurado, sem fusão no rosto; pausas com jump cut (zoom 1,0/1,13) ou b-roll.
- Sem marcas/logos. Selo "VIDEO FICTICIO" do 1º ao último quadro. −14 LUFS, true peak ≤ −1 dBTP.
- Revisão: `revisar_ad.py --idioma es` + zoom no rosto + quadro a quadro nos takes Kling (mãos, bordas, objetos).
- Saída na pasta `C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\` + `<nome>_narracion.txt`. Trabalho em `_trabalho\personas\<slug>\`.
