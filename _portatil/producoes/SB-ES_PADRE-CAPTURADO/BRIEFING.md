# SB ES · «Padre capturado»: versão completa + 5 ganchos (19/10/2026, aprovado pela pessoa com «confirmo»)

## Base
- **Vídeo base:** `C:\Users\PICHAU\Downloads\SB-VIDEOS-FICTICIOS\03_GRIMORIO\GRIMORIO V2 - ES COLAR (VIDEO FICTICIO)_v4.mp4`
  - 2:39, 720x1280, 30 fps, espanhol neutro.
  - Vídeo próprio da pessoa, então reaproveitar takes e voz clonada está liberado.
  - Transcrição com tempos: `_ref/..._transcricao.txt`.
- **Trabalho da versão anterior** (base sem legenda, sobreposições, scripts, lipsync): `C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_es\`.
  - `visual\base_sem_legenda.mp4` é o vídeo sem a legenda queimada. Confira se ele ainda tem título, moldura e selo antes de usar.
  - `visual\overlays\`, `visual\textos_tela.json` e `audio\overlays_final.json` dão posição e estilo do título amarelo, da moldura da live e do selo.
  - `audio\legenda_es.py` faz a legenda em caixa palavra a palavra.
  - `audio\lipsync\` tem o fluxo HeyGen usado antes. **Não altere os arquivos dessa pasta: copie o que for usar.**
- **Áudio do v4:** `GRIMORIO_analise\_trabalho_es\audio\v4\`. Lá estão o fundo de igreja (`amb_a.mp3`), o grito novo (`g2.mp3`), o `remix2.py` e o vocal/música do trecho inicial separados pelo demucs (`sep\`).
- **Quadros de referência:** `_ref\q_*.png`.
  - 1 s: repórter.
  - 5,5 s: padre arrastado na igreja.
  - 10–12 s: selfie do padre chorando, o personagem "capturado".
  - 25–40 s: padre de roxo, que passa a ser o **padre Juan Méndez**.
- **Banco de b-roll SB:** `C:\Users\PICHAU\Downloads\SB-BANCO-BROLL\` (`indice_geral.json`). Exemplos: `oracion_06_velas-iglesia`, `oracion_30_capilla-noche-velas`, `sagrado_15_altar-velas-incenso`.

## Oferta e regras fixas
- **Oferta:** San Benito ES («Camino de Fe con San Benito»). O anúncio leva à VSL, que tem narrativa de oração ao vivo com milhares de pessoas.
- **Botão: «Ver más».** Use setas vermelhas apontando para baixo, para o botão real, e texto «TOCA EN «VER MÁS»» sem cara de botão.
- **Página que anuncia: Padre Juan Méndez. ROSTO = `_ref\padre_juan_mendez_PAGINA.png`** (homem de ~55 anos, óculos, casula verde e bordô; atualizado em 19/10 pela pessoa). O padre de roxo do v4 SAI: todas as falas do Juan Méndez vêm de um avatar HeyGen feito com esse rosto.
  - O título vira «EL PADRE JUAN MÉNDEZ LO VA A REVELAR TODO EN VIVO».
  - A arroba da moldura vira «padre.juanmendez».
- **Nunca diga:** «Grimorio», livro, colar, «24 horas», horário do dia, «no sé por cuánto tiempo», «entra mientras sea posible».
- **Nunca ensine as 12 palavras.** A oração da VSL é outra, então o anúncio não pode revelá-la.
- **Selo «VIDEO FICTICIO»:** pequeno, no topo à direita, do primeiro ao último quadro. Copie o do v4.
- **Público sênior:** legenda e textos grandes.
- **Compliance:** não suavize nada além do que está aqui.
- **Lições do projeto:** leia `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\CLAUDE.md` e as skills `editar-criativo`, `gerar-midia-ia` e `revisar-criativo` em `.claude\skills\`. As principais:
  - Lipsync HeyGen em mode **speed**, com trechos de até 12 s. O vídeo de entrada leva o áudio de origem e o áudio novo vai separado.
  - Nada de retoque na boca nem quadro congelado no rosto. Corte nas fronteiras das palavras e cubra as pausas com b-roll.
  - No Kling/Seedance: nada de porta abrindo e ninguém entrando ou saindo de veículo. O personagem ocupa ~25% da altura, com a dor legível no 1º quadro.
  - Cada take aparece uma vez só no mesmo vídeo.
  - Cor com matriz bt601 fixa.
  - Áudio sem salto de pts (`-reinit_filter 0` no montar_ad_rapido).
  - Uma voz por personagem. Registre as vozes em `_vozes.json` nesta pasta.
- **Vozes:**
  - Repórter: `cIBxLwfshLYhRB9lCXEg`.
  - Padre capturado/chorando: `sKgg4MPUDBy69X7iv3fA` (Alejandro Duran). Para grito, use `eleven_v3` com tags em espanhol.
  - Padre Juan Méndez (de roxo): `BskzYZ6zvapoZ3mBu93C`, clone, `eleven_multilingual_v2`.
  - A conta ElevenLabs está no limite de 160 vozes: não clone voz nova. Personagens novos usam voz da biblioteca latina.
- **Geração de imagem e vídeo:** use o ElevenLabs Creative pelo MCP `claude_ai_ElevenLabs`.
  - Seedance: `bytedance-seedance-v2` (tem áudio nativo).
  - Imagem: `gpt-image-2.5-sunburst`. O aspect_ratio vai em `model_parameters`, 9:16.
  - O Flora está sem saldo.
- **Rodar scripts:** `PYTHONIOENCODING=utf-8`; scripts do kit a partir de `kit-edicao-criativos\`.
- **Painel:** `python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa <id> "<título>" --texto "..." --k N --n M`. Também use `img <id> <arquivo> --legenda "..."`, `custo <id> <US$>` e `fim <id>`.

## Divisão (cada agente só escreve na sua subpasta; `PRONTO.txt` ao terminar)
| Agente | Subpasta | Entrega |
|---|---|---|
| Corpo | `corpo\` | `V0_COMPLETA.mp4` (gancho original do v4 + corpo novo) **e** `corpo_a_partir_selfie.mp4` (de «Es indignante…» até o fim, com legenda, sobreposições, CTA e selo, para os ganchos colarem na frente) + `corpo_info.json` (duração, tempo do 1º quadro da selfie, LUFS) |
| G1 + G3 | `ganchos_g1g3\` | `gancho_G1.mp4`, `gancho_G3.mp4` (prontos, com legenda, título e selo) e, depois que `corpo\PRONTO.txt` existir, `V1_MISSA.mp4` e `V3_ESCADARIA.mp4` |
| G2 + G4 | `ganchos_g2g4\` | `gancho_G2.mp4`, `gancho_G4.mp4` + `V2_SELFIE-ULTIMO-VIDEO.mp4` e `V4_LIVE-DERRUBADA.mp4` |
| G5 | `gancho_g5\` | `gancho_G5.mp4` + `V5_NOTICIA-TV.mp4` |

Ao final, cada agente copia os vídeos prontos (V*) para `ENTREGA\` e escreve, ao lado de cada um, `<nome>_texto-anuncio.txt`:
- Título: «🔴 EN VIVO: La oración a San Benito que casi nadie conoce 🙏»
- Botão: «Ver más»
- Texto principal: «Hay un mensaje que está tocando el corazón…». **Copie o texto completo da SB ES de um anúncio vencedor**, se estiver acessível. Se não estiver, deixe `[COPIAR DO ANÚNCIO VENCEDOR SB ES]`.

## Roteiro do CORPO (comum a todos)
| Bloco | Tempo aprox. | Fala | Cena |
|---|---|---|---|
| Gancho (só V0) | 0:00–0:08 | igual ao v4 | v4 0:00–8:05, com o título trocado para Juan Méndez |
| Selfie | 0:08–0:17 | igual: «Es indignante ver lo que me hicieron…» · «Pero la verdad no va a quedar escondida.» | v4 8:05–16:9 |
| | ~0:17–0:22 | **NOVA** (Alejandro, chorando): «Le enseñé esta oración a mi amigo, el padre Juan Méndez, y él la está rezando en vivo con miles de familias.» | Selfie com lipsync novo (fonte: v4 16:9–21:9) |
| Conexão | ~0:22–0:33 | **NOVA** (Juan Méndez, clone): «Cada día me escriben familias que trabajan sin descanso, que rezan… y aun así sienten que el dinero nunca alcanza y que algo les cierra el camino. No es falta de fe.» | Padre de roxo com lipsync (fonte: v4 22:0–31:5) + 1–2 b-rolls do banco |
| Prévia da reza | ~0:33–0:44 | igual: «Oh poderoso San Benito, guardián de los arcanos sagrados, que venciste a las serpientes… con tu fe inquebrantable.» | v4 32:4–44:1 |
| Prova do título | ~0:44–0:50 | **NOVA** (Juan Méndez): «Esta es la oración a San Benito que casi nadie conoce, y que está ayudando a muchas familias hispanas.» | Padre de roxo com lipsync (fonte: v4 1:01–1:07) |
| | ~0:50–0:57 | igual: «Solo un grupo de monjes tenía acceso a esta oración completa. Por eso nunca habían oído hablar de ella.» | v4 1:23,0–1:30,0 |
| Mecanismo | ~0:57–1:08 | igual: «Pero atención, tiene que hacerse de la forma correcta… una manera correcta de hacerla y de escucharla.» | v4 1:46,4–1:58,7 (sem «Fue increíble») |
| CTA | ~1:08–1:20 | **NOVA** (Juan Méndez): «Por eso la estoy rezando en vivo, completa, paso a paso, junto con miles de familias. Toca en «Ver más», aquí abajo, y entra a rezar conmigo.» | Padre de roxo com lipsync + b-roll de capela com velas + «🔴 EN VIVO» + setas vermelhas. **O vídeo termina no fim da fala** (+0,5 s) |
- O título amarelo fica só enquanto ele fazia sentido no v4 (gancho e selfie).
- A moldura da live do padre de roxo fica como no v4, com a arroba nova.
- A trilha é o fundo musical do v4, já separado. Conferir que a tensão do gancho e da selfie e a esperança a partir do ritual continuam audíveis.
- Duração-alvo: **~1:20**.

## Os 5 GANCHOS (6–9 s cada; terminam no corte para a selfie «Es indignante…»)
O padre capturado de todos os ganchos é o **mesmo homem da selfie** (`_ref\q_10s.png` / `q_12s.png`): use o rosto dele como referência de imagem. Em G1 e G3 ele está de batina/clergyman preto, como no v4 em 5,5 s.
| # | Cena | Fala / texto | Notas |
|---|---|---|---|
| G1 «Missa interrompida» | Padre no altar com microfone; dois homens de terno sobem, arrancam o microfone e seguram os braços dele; a igreja lotada se levanta | Padre gritando (Alejandro, v3): «¡Esta oración no se la van a quitar al pueblo!» · Tela: «LO SACARON DEL ALTAR POR ENSEÑAR ESTA ORACIÓN» | Plano aberto da nave; o padre ocupa ~25% da altura no 1º quadro |
| G2 «Su último video» | Selfie do padre escondido na sacristia, sussurrando para a câmera, com batidas fortes fora de quadro (sem porta abrindo) | Sussurro (Alejandro): «Si este video se corta… busquen al padre Juan Méndez. Él tiene la oración.» · Tela: «SU ÚLTIMO VIDEO» | Pode sair do HeyGen (avatar a partir do rosto da selfie, boca fechada e expressão de medo) + som de batidas (SFX) |
| G3 «Escadaria» | Escadaria externa da igreja, de dia; dois guardas levam o padre pelos braços; fiéis filmam com o celular; senhora de ~65 anos grita | Senhora (voz latina feminina da biblioteca): «¡Suéltenlo! ¡Él solo nos enseñaba a rezar!» · Tela: «SE LLEVARON AL PADRE» | Seedance com áudio nativo ou voz sobreposta; sem carro e sem viatura |
| G4 «Live derrubada» | Moldura «🔴 EN VIVO» (estilo da moldura do v4); o padre (rosto da selfie) reza na capela olhando o celular; uma mão tira o celular do tripé, a imagem treme e cai, e aparece «TRANSMISIÓN INTERRUMPIDA» | Padre, cortado no meio: «Oh poderoso San Benito, guar—» | Pode ser 1 take Seedance curto + efeito de queda/glitch no ffmpeg |
| G5 «Noticia TV» | Âncora no estúdio de telejornal hispânico + faixa «ÚLTIMA HORA: sacerdote retirado de su parroquia por enseñar una oración» + inserto do v4 4,1–7,7 s (padre arrastado, com o áudio do «¡Graben!») | Âncora (voz da biblioteca): «Un sacerdote fue retirado de su parroquia por enseñar una oración a San Benito. Este es el video que grabaron sus fieles.» | Âncora: imagem gpt-image + HeyGen Avatar IV 720p; personagem inventado, sem logo de canal real |

Cada gancho leva legenda em caixa palavra a palavra, como o corpo, e o selo. Na colagem gancho + corpo: corte seco para a selfie, áudio sem salto e música contínua. Se precisar, use crossfade de 0,15 s só no áudio.

## Orçamento (teto)
| Agente | Teto |
|---|---|
| Corpo | voz ~US$ 0,20; HeyGen até 60 créditos |
| G1+G3 | até US$ 4 em créditos ElevenLabs |
| G2+G4 | até US$ 2,50 |
| G5 | até US$ 2 + HeyGen até 40 créditos |

Registre o gasto real com `painel custo`. **Se um take sair errado, não refaça mais de 1 vez sem avisar.** Confira a olho antes de pagar refação.

## Revisão obrigatória antes do PRONTO
Rode `revisar_ad.py --idioma es` em cada V*. Confira:
- folha de contato;
- whisper em espanhol sem «Grimorio», «12 palabras», «24 horas» nem o nome «Pablo»;
- ausência de quadro solto;
- ausência de silêncio no fim;
- setas fora da legenda;
- lipsync a olho a 30 fps nas falas novas.
