# Série "COMPLETA": 10 personas no formato aprovado do Medalla COMPLETA v2 (14/10/2026)

**Modelo aprovado:** `C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\SB-ES_MEDALLA_COMPLETA.mp4`, montado por `_trabalho\montar_completa2.py` com legenda de `legenda_comp.py`, trilha de `gerar_trilha2.py` e selo `graficos\selo_ficticio_mini.png`. Leia esses scripts antes e copie para `_trabalho\personas\<slug>\completa\`. Os originais não mudam.

**Saída:** `C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\SB-ES_<SLUG>_COMPLETA.mp4` + `_narracion.txt`. Os vídeos antigos (`*_FICTICIO.mp4`) ficam intocados.

## Estrutura de cada vídeo (igual ao Medalla COMPLETA)
1. **Gancho (0–6 s)**
   - Fala: frase de gancho da persona (abaixo), em off, voz FIRME.
   - Cena: take NOVO "gancho_amplo". A persona ajoelhada rezando no lugar vazio dela, com o vazio legível no 1º quadro (cadeiras, mesas, objetos parados ao redor). Ela ocupa ~25% da altura do quadro, câmera um pouco acima, push-in lento.
   - Por cima: o título do gancho (`graficos\titulo_gancho.png`).
2. **Reza (6–10 s)**
   - Fala: reza curta da persona, sussurrada com reverb.
   - Cena: a cena "antes" que já existe da persona, ou o próprio gancho_amplo em close.
3. **Virada (10–13 s)**
   - Sem fala: a cena "depois" que já existe da persona.
   - Trilha: a de tensão vira a de esperança no corte (crossfade de 0,3 s).
4. **Frustrado (13–16 s)**
   - Fala: a 1ª frase da selfie.
   - Cena: take NOVO "frustrado". A persona em pé ou sentada, frustrada, olhando o próprio lugar vazio (ver abaixo), em luz melancólica.
5. **Selfie (16–29 s)**
   - Fala: o resto da selfie + a frase comum.
   - Cena: HeyGen a partir de um retrato NOVO com cara TRISTE e BOCA FECHADA, cantos da boca para baixo, sem sorriso. É isso que evita os dentes à mostra.
6. **Padre (29 s até o fim): IDÊNTICO ao Medalla COMPLETA, não gerar nada.**
   - Usar `_trabalho\completa\padre\padre_parte1.mp4`, `padre_parte2.mp4` e `padre.mp3`, com os mesmos b-rolls (medalla.mp4, BRV-35/03/47/14/50) e o mesmo CTA único "TOCA «MÁS INFORMACIÓN»" de `montar_completa2.py`.

**Frase comum no fim da selfie (todas as personas):** "Hasta que un padre explicó algo que nadie me había dicho sobre la medalla de San Benito."

## Personas: falas e cenas novas

### APP: motorista de app
- **Voz:** NOVA voz masculina latina de ~55 anos, diferente de todas em `_trabalho\personas\_vozes.json`. Registre no arquivo. Não usar Santiago.
- **Gancho:** "Recé dentro de mi carro, a las tres de la mañana, sin un solo viaje… y esto fue lo que pasó."
- **Reza:** "Oh glorioso San Benito… sácame de esta escasez."
- **Selfie:** "Pasé casi seis meses casi sin viajes. Mis hijos me pedían cosas y yo les decía que mañana. Me sentía un fracasado."
- **Gancho amplo:** de madrugada, sedã prata parado numa rua vazia e escura. Ele dentro do carro, rezando com as mãos no volante, visto de fora em plano médio, com a rua deserta visível. Sem logo.
- **Frustrado:** dentro do carro, ele olhando o celular no suporte com o app sem corridas e esfregando o rosto.
- **Base existente:** `_trabalho\app\`

### COSTURERA
- **Voz:** a registrada em `_vozes.json`.
- **Gancho:** "Recé de rodillas junto a mi máquina parada… y esto fue lo que pasó."
- **Reza:** "Oh glorioso San Benito… sácame de esta escasez."
- **Selfie:** "Pasé casi seis meses sin un solo encargo. Mis manos, que siempre trabajaron, ya no servían para nada. Me sentía inútil."
- **Gancho amplo:** ajoelhada no meio do ateliê, com a máquina parada, rolos de tecido intocados e cadeira vazia de cliente ao redor.
- **Frustrado:** sentada diante da máquina parada, olhando a agenda de encomendas vazia.

### ABUELA
- **Voz:** a registrada (Grandma Aurora).
- **Gancho:** "Recé frente a una mesa puesta para doce… y comí sola. Y esto fue lo que pasó."
- **Reza:** "Oh glorioso San Benito… devuélveme a mi familia."
- **Selfie:** "Pasé años poniendo la mesa para todos. Mis nietos crecían y yo los veía solo en fotos. Sentía que ya no le importaba a nadie."
- **Gancho amplo:** ajoelhada ao lado de uma mesa longa posta com 12 pratos e todas as cadeiras vazias.
- **Frustrado:** sentada sozinha na cabeceira, mexendo no prato sem comer e olhando as cadeiras vazias.

### MADRE
- **Voz:** a registrada.
- **Gancho:** "Recé en el piso de mi cocina, con las cuentas sobre la mesa… y esto fue lo que pasó."
- **Reza:** "Oh glorioso San Benito… protege a mis hijos."
- **Selfie:** "Trabajaba de sol a sol y aun así las cuentas no cerraban. Mi hijo me preguntó por qué siempre estaba triste. Sentía que les estaba fallando."
- **Gancho amplo:** de noite, ajoelhada no chão da cozinha simples, com as contas espalhadas na mesa e a geladeira com poucas coisas.
- **Frustrado:** sentada à mesa, com as mãos na cabeça, olhando a pilha de contas.

### CAMPESINO
- **Voz:** a registrada.
- **Gancho:** "Recé de rodillas en mi tierra seca… y esto fue lo que pasó."
- **Reza:** "Oh glorioso San Benito… mira mi tierra."
- **Selfie:** "Pasé meses viendo mi tierra secarse. La tierra de mi padre y de mi abuelo… y yo la iba a perder. Me sentía la vergüenza de mi familia."
- **Gancho amplo:** ajoelhado no meio da plantação seca, terra rachada e fileiras de pés mortos ao redor até o horizonte.
- **Frustrado:** em pé na cerca, olhando o campo seco, tirando o chapéu.

### DESEMPLEADO
- **Voz:** a registrada.
- **Gancho:** "Recé en un banco de la plaza, con mi carpeta de currículums… y esto fue lo que pasó."
- **Reza:** "Oh glorioso San Benito… sácame de esta escasez."
- **Selfie:** "A mis cincuenta y tantos me quedé sin trabajo. Salía de casa cada mañana de traje para que mi familia no supiera. Me sentía un inútil."
- **Gancho amplo:** sentado sozinho num banco de praça quase vazia, de manhã cedo, de olhos fechados rezando com a pasta no colo e bancos vazios ao redor. Em plano médio-aberto.
- **Frustrado:** na mesma praça, olhando a pasta com currículos e o celular sem chamadas.

### UCI (opção B, decisão da pessoa)
- **Voz:** a registrada.
- **Gancho:** "Recé de rodillas junto a la cama de mi esposo en terapia intensiva… y esto fue lo que pasó."
- **Reza:** "Oh glorioso San Benito… no me lo quites."
- **Selfie:** "Pasé días y noches en esa sala, mirando las máquinas. Volvía a casa y su lado de la cama estaba vacío. Sentía que me estaba apagando por dentro."
- **Gancho amplo:** ajoelhada ao lado do leito de UTI, à noite, com monitores ao redor, luz azul e corredor vazio pela janela da porta. Em plano médio. Sem nada chocante.
- **Frustrado:** em casa, sentada na beira da cama de casal, olhando o lado vazio do marido.
- **Virada:** a existente, ele abrindo os olhos.

### FERIA
- **Voz:** a registrada.
- **Gancho:** "Recé detrás de mi puesto lleno de fruta, sin un solo cliente… y esto fue lo que pasó."
- **Reza:** "Oh glorioso San Benito… quita lo que cerró mi camino."
- **Selfie:** "Mi puesto estaba lleno y nadie se acercaba. Veía a las vecinas venderlo todo y yo volvía a casa con la fruta perdida. Sentía que alguien me había echado la envidia encima."
- **Gancho amplo:** ajoelhada atrás da barraca cheia de frutas numa feira, com o corredor da feira vazio na frente, em dia cinzento.
- **Frustrado:** em pé atrás da barraca, olhando as bancas vizinhas com clientes, com a dela vazia.

### PAREJA
- **Voz:** a registrada.
- **Gancho:** "Recé de rodillas en mi cuarto, mientras mi esposo dormía en el sofá… y esto fue lo que pasó."
- **Reza:** "Oh glorioso San Benito… devuelve la paz a mi casa."
- **Selfie:** "Mi esposo y yo vivíamos como dos extraños. Treinta años juntos y ya no nos mirábamos a los ojos. Sentía que lo estaba perdiendo."
- **Gancho amplo:** ajoelhada ao pé da cama de casal arrumada e vazia, à noite. Pela porta aberta aparece a sala, com ele dormindo no sofá ao fundo.
- **Frustrado:** sentada à mesa de jantar com dois pratos; ele de costas, saindo da cozinha. Silêncio.

### PENSIÓN
- **Voz:** a registrada.
- **Gancho:** "Recé en la recepción de mi pensión, con todas las llaves colgadas… y esto fue lo que pasó."
- **Reza:** "Oh glorioso San Benito… sácame de esta escasez."
- **Selfie:** "Pasé casi seis meses sin un solo huésped. La casa que levanté con mi esposo se estaba cayendo a pedazos. Sentía que le estaba fallando."
- **Gancho amplo:** ajoelhada na recepção, com o quadro de chaves cheio (todas penduradas), o livro de hóspedes aberto em branco e as poltronas vazias.
- **Frustrado:** atrás do balcão, passando o dedo pelo livro de hóspedes vazio e olhando a porta.

## Regras (aprendidas na série)
- Rosto da persona: use o retrato existente da persona (em `_trabalho\personas\<slug>\` ou `_trabalho\app\`) como referência em TODAS as imagens novas, para ser a mesma pessoa.
- Kling: sem porta abrindo ou fechando, sem gente entrando ou saindo de veículo, movimento contido. QA quadro a quadro a cada 0,2 s.
- HeyGen: não usar `fechar_boca`, quadro segurado nem fusão no rosto. Pausas viram jump cut (zoom 1,0/1,13) ou b-roll. Expressividade baixa.
- Selo mini colado no topo, do primeiro ao último quadro. Trilha em dois climas. Áudio a −14 LUFS e true peak ≤ −1 dBTP.
- Revisão: `revisar_ad.py --idioma es`, zoom no rosto e CTA único.
- Teto por persona: US$ 1,20 no Flora/Kling (retrato triste + 2 imagens + 2 takes), 25 créditos no HeyGen, 350 caracteres no ElevenLabs.
