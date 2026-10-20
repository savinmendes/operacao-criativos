---
name: editar-criativo
description: Edita, adapta ou monta criativos de vídeo 9:16, 4:5 ou 1:1 com as ferramentas Python do kit (legenda, hook, setas de CTA, selo, troca de marca/rótulo, tradução, versão curta, matriz gancho × corpo, corpo com avatar). Use para qualquer pedido de edição de criativo/AD.
---

# Editar criativo

1. Leia `CLAUDE.md` do kit (regras fixas, tabela de scripts, armadilhas). Todos os scripts têm `--help`; rode com o diretório de trabalho na pasta do kit e `PYTHONIOENCODING=utf-8` no Bash.
2. Descubra o próximo número: liste `ads/` da oferta e continue do maior AD (oferta nova = AD 01).
3. Padrão: **uma receita JSON** + `python ferramentas/montar_ad.py receita.json` (modelo em `exemplos/`). Tarefa isolada → script direto.
4. Classifique a origem antes de tocar nela; isso decide voz e rosto:
   - **Marca própria** (criativo da própria operação): clonar a voz do narrador é permitido. Antes de clonar, procure um clone existente da mesma voz e reutilize se a semelhança for alta. Nunca apague vozes.
   - **Criador de terceiros com rosto**: a pessoa escolhe. **Padrão (B1):** sem clone, sem lipsync no rosto real; takes sem rosto + `montar_corpo_avatar.py` com avatar próprio, voz de catálogo (1 por criador). **Mesmo criador (B2):** só se a pessoa confirmar que o criador autorizou uso de imagem e voz; aí clone da voz + lipsync no vídeo original, registrando a autorização no relatório (ver `traduzir-criativo`).
   - **Rosto estilo Pixar/3D**: a IA de edição troca o rosto ou deixa fotorrealista; troque o rótulo com `trocar_rotulo_faixa.py` (ver skill `gerar-midia-ia`).
5. Escolhas padrão da receita:
   - **Resolução:** origem 360p/480p → `upscale_video.py --escala 2` + `"resolucao": "720"`. `"1080"` só para origem ≥720p ou vencedor refeito.
   - **Legenda:** `alinhamento:` se a narração veio do `tts_elevenlabs.py`; senão `transcrever` no idioma do mercado. Transcrição errada → `texto:frases.txt` com o roteiro real. `legenda_hook` com `corrigir: [[regex, troca]]` para grafia do nome da marca.
   - **Faixa sobre texto queimado** (legenda/aviso estrangeiro): alpha ≥ 250, senão o texto original aparece por baixo. Em 720 com faixa no rodapé: `selo.y ≈ 1110` e `cta.y ≈ 1490`, para as setas não ficarem em cima da faixa.
   - **CTA:** `{"palavra": "toca"}` (ou a palavra do mercado). Confira no `_frames.jpg` que as setas aparecem.
   - Manchete no topo só durante o hook (`ate` = fim do hook). Hook novo sobre corpo existente: `hook.tipo = imagem`; avatar com fala própria: `tipo = antes`.
   - Tela dividida: `video.py dividida` (sem borda; rosto inteiro na metade de cima). Remover legenda: `--preview` primeiro.
6. **Tradução de outro idioma:** transcreva (faster-whisper) e leia o texto da tela (OCR); reescreva o roteiro para o mercado (sem preço/moeda/país/link/estação estrangeiros); TTS com alinhamento, velocidade ≤ 1,1x (se não couber, corte sobras ou congele um take); separe a música com `demucs --two-stems=vocals` e use só `no_vocals.wav`; `preparar_corpo_traducao.py` cobre a legenda queimada, redesenha o título, corta e desfoca o que o estudo mandou e troca o áudio; depois `montar_ad.py`.
7. **Troca de marca em AD existente:** corte no ponto em que o narrador apresenta a marca/oferta antiga (transcrição por palavra, corte em fim de frase); troque rótulos (`trocar_rotulo_faixa.py` → Kling só onde não resolve → `encaixar_edit.py` → `substituir_trechos.py`); `trocar_texto_tela.py`/`desfocar_regioes.py` nas telas; falas com `trocar_trecho_audio.py`; fim novo com a oferta atual, montado por `montar_ad.py`.
8. **Versão CURTA (60–90 s):** gancho (~8–15 s) + 2–3 trechos fortes (problema, mecanismo, prova) + o mesmo fim. Corte sempre em fim de frase pelo alinhamento/transcrição por palavra e monte **a partir das partes já tratadas**, para nada da marca antiga voltar.
9. **Matriz gancho × corpo:** `gerar_variacao.py banco <video>` cria o banco de tomadas (scdet); `gerar_variacao.py montar <config.json>` monta cada combinação. Regras: margem nas bordas de cada tomada (o corte detectado não é exato), grupos de cena contínua contam como uma tomada, nenhum take repete, nunca dois seguidos da mesma fonte, voz do gancho = voz do corpo. Estáticos/carrossel saem de quadros reais.
10. **Corpos montados por concat:** recodifique as partes com os mesmos metadados de cor (`-colorspace/-color_primaries/-color_trc/-color_range` iguais) antes de juntar; partes diferentes disparam o reinit do filtro e deixam quadro solto ou buraco de áudio.
10b. **Montagem: regras que já custaram refação**
   - **Selo de aviso** (ex.: "vídeo fictício"): pequeno e colado no topo, à direita, do 1º ao último quadro. Não invente moldura de rede social (avatar, nome, "ao vivo", contador, barra de comentários) sem pedido: a pessoa mandou tirar.
   - **Trilha por clima:** tensão no trecho do problema e troca de verdade para esperança na virada, com crossfade curto no corte. A mesma trilha só subindo o volume não serve. Use trilha própria (gerada) ou liberada, nunca música de terceiros sem a pessoa liberar.
   - **CTA único:** um botão, um texto na tela e nenhuma fala depois do CTA. O botão que o vídeo manda tocar é o mesmo do anúncio. Dois CTAs com botões diferentes confundem.
   - **B-roll casa com a persona e com a fala:** idade, gênero e cenário iguais aos do personagem (senhora idosa num vídeo de mãe de 45 anos destoa). Para a fala da dor, prefira o personagem frustrado olhando o próprio lugar vazio a um close de objeto.
   - **Nenhum take repetido** no mesmo vídeo. Se só existe um, gere outro ou corte em trechos diferentes.
   - **Título nunca cobre rosto ou corpo** do personagem: reposicione o título ou gere a imagem com espaço livre.
   - **Loop aberto tem que fechar:** se a fala promete algo ("a forma exata de…"), o trecho seguinte entrega o mecanismo antes do CTA (ver skill `completar-criativo`).
11. Em lote: faça 1, mostre o `_frames.jpg` e o caminho, espere aprovação; depois rode o resto (paralelo em background). Processos longos: progresso `[k/N]` + % + tempo restante.
11b. **Agentes em paralelo:** divida o trabalho **antes** de qualquer agente gerar (quem faz voz, quem faz avatar, quem monta). Dividir no meio do caminho fez dois agentes gerarem a mesma voz e estourou o teto. Cada agente grava numa pasta própria e marca o fim com `PRONTO.txt`; o montador espera esses arquivos. Arquivos temporários de cada agente ficam numa subpasta só dele (o scratchpad é compartilhado e já houve arquivo sobrescrito).
11c. **Disco:** as pastas intermediárias de montagem (`mont*`, segmentos, `corpo.mp4`) pesam 0,5–1 GB por vídeo. Depois da entrega aprovada, peça para apagá-las; mantenha takes, avatares, vozes, imagens base e scripts (é com eles que se remonta sem pagar de novo).
12. Termine com `finalizar.py` (ou `montar_ad.py`, que já chama) e rode a skill `revisar-criativo` antes de dizer que está pronto. Entregue junto o `.txt` com título + texto principal por AD.
13. Resposta final curta: arquivos (caminho), duração, MB, custo real × orçado, e o que depende da pessoa.
