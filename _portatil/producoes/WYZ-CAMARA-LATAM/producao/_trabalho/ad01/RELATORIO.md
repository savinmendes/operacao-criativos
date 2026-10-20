# AD 01 — Grupo B (criador em estúdio) — relatório

- **Arquivo:** `producao\AD 01 - WYZE-SOLAR-CAM-PAN-SIGUE-PERSONAS-ES-LATAM.mp4`. Tem 44,9 s (o original tem 52 s), 720x1280 e 25,8 MB, e decodifica sem erro.
- **Voz:** ElevenLabs "Mario - Animated and chatty", salva na conta como "WYZE 01-12 Mario animado" (`tomkxGQGz4b1kE0EM722`). É uma voz de catálogo em espanhol latino, masculina e enérgica, e **não foi clonada**. O modelo é eleven_multilingual_v2, na velocidade 1,0.
- **TTS:** 831 caracteres (~US$ 0,14).
- **HeyGen:**
  - Avatar próprio "WYZE Review Latino 35" (`430f346689b68545f1adbea9f186bd83`), um photo avatar criado por prompt e anotado em `_trabalho\avatar_masculino.txt`.
  - Vídeo `f64d73a07babe27a90d621139709a4e9`, com lipsync do áudio do ElevenLabs, Avatar IV, 1080p, expressividade alta.
  - O saldo foi de 9.072 para 9.021 (−51) entre a criação do avatar e este vídeo. Outros agentes podiam estar usando a conta ao mesmo tempo.
  - Pela medição limpa do AD 12 (~12 créditos para 41,5 s), o vídeo deste AD custou cerca de 13 créditos. O resto provavelmente foi a criação do avatar ou o uso paralelo.
- **Roteiro:** está em `roteiro_es.txt`.

## O que foi trocado ou cortado
- **Rosto do criador:** saiu do vídeo inteiro.
  - O avatar fala em tela cheia em 48% do tempo: gancho, "Esta es la Wyze…", "tres metros", "lo mejor es esto", 2K/visión nocturna, "para mí…" e o CTA.
  - O resto são takes do original **recortados abaixo do rosto** (y ≥ 470, recorte 9:16 com zoom de 1,58x): caixa, câmera, panel, cable, giro e tilt, câmera sobre a caixa.
- **Bandeira dos EUA:** ficava no alto, à esquerda (y < 280). Como nenhum recorte sobe acima de y = 470, ela não aparece em nenhum quadro. O letreiro "DR" da parede também ficou de fora.
- **Fala removida:** "link down here" e "I have the indoor version".
- **CTA:** "Pídela hoy. Toca el botón de abajo y pide la tuya." Não há preço, país, frete nem garantia.
- **Legenda em inglês:** coberta por uma faixa preta opaca (alpha ~252, y 576–696 em 720p) nos takes do original. A legenda nova em espanhol, gerada pelo alinhamento, fica dentro da faixa (y 954 em coordenadas de 1080p).
  - Nos trechos do avatar, a mesma legenda fica no peito, abaixo do queixo.
  - O avatar foi subido 70 px (zoom de 1,0625) para a legenda não cobrir a boca.
- **Título de gancho:** "WAIT… THIS CAMERA ACTUALLY FOLLOWS PEOPLE?!" virou "¿ESTA CÁMARA SIGUE A LAS PERSONAS? 👀" (manchete, de 0 a 3 s).
- **Setas de CTA:** entram no "Toca" (42,7 s) e ficam até o fim.
- **Selo:** não foi colocado. A receita pronta para incluir depois é `receita_com_selo.json` ("PAGO CONTRA ENTREGA").
- **Marca Wyze:** continua na fala e na caixa, como o briefing permite.

## Revisão
- **Whisper (es):** bate com o roteiro. Não há preço, país, TikTok, "link", Navidad/año nuevo nem alegação proibida.
  - Ele ouviu "Wyze" como "Y Solar Campaign", mas a pronúncia do TTS está certa.
- **Whisper (en):** só devolve a tradução do espanhol. Idioma detectado: es (1,0), sem fala em inglês por baixo.
- **Folha de contato** (1 quadro/s) e faixa da legenda (3 quadros/s):
  - Nenhuma legenda em inglês aparece; a borda vermelha que vazava foi corrigida ao alargar a faixa.
  - O rosto do criador real não aparece em nenhum quadro.
  - As setas ficam abaixo da legenda.
- **Cortes (scdet):** nenhum quadro solto; o menor trecho tem 0,83 s.
- **Fim:** o silêncio final tem 0,48 s.

## Pendências e observações
- Os takes do produto são recortes com zoom de 1,58x sobre 720p, então ficam um pouco mais suaves que o avatar.
- O briefing não pede, mas um selo de oferta só deve entrar quando a oferta for confirmada.
- O original não tinha trilha (era só a voz), então o AD saiu sem música.
- Scripts: `_trabalho\montar_corpo_b.py` + `plano.json` (segmentos) + `receita.json` (montar_ad).
