---
name: editar-criativo
description: Edita, adapta ou monta criativos de vídeo 9:16 com as ferramentas Python do kit (legenda, hook, setas de CTA, selo, troca de marca/rótulo, tradução, versão curta, matriz gancho × corpo, corpo com avatar). Use para qualquer pedido de edição de criativo/AD.
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
11. Em lote: faça 1, mostre o `_frames.jpg` e o caminho, espere aprovação; depois rode o resto (paralelo em background). Processos longos: progresso `[k/N]` + % + tempo restante.
12. Termine com `finalizar.py` (ou `montar_ad.py`, que já chama) e rode a skill `revisar-criativo` antes de dizer que está pronto. Entregue junto o `.txt` com título + texto principal por AD.
13. Resposta final curta: arquivos (caminho), duração, MB, custo real × orçado, e o que depende da pessoa.
