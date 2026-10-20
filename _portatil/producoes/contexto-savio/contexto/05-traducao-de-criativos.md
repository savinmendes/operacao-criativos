# Tradução de criativos (outro idioma ou outro país)

> Como levar um criativo de vídeo de um idioma/mercado para outro: estudo, roteiro, voz, música, cobertura de texto queimado, rosto (avatar ou lipsync) e montagem. Abra quando pedirem para traduzir, dublar, "passar para espanhol/francês" ou localizar para outro país.

## Contexto de uso

**Quando se aplica.** Vídeo pronto em outro idioma (ou no mesmo idioma, mas de outro país) que precisa rodar num mercado novo. Fluxo de lote guiado pela skill `traduzir-criativo` (versão mais completa em `Produtividade com ia\.claude\skills\traduzir-criativo\SKILL.md`); montagem, geração e revisão seguem `editar-criativo`, `gerar-midia-ia` e `revisar-criativo`.

**Classificação usada no estudo.**
- **A** sem rosto (só mãos/produto) · **B** com rosto do criador · **C** outro produto · **D** sem narração (só música + texto na tela).
- Grupo B: a pessoa escolhe por lote ou por vídeo. **B1 (padrão)** = avatar próprio HeyGen + takes sem rosto, voz de catálogo, sem clone e sem lipsync no rosto real. **B2 (mesmo criador)** = clone da voz + lipsync no vídeo original, só quando a pessoa confirma que o criador autorizou uso de imagem e voz (registrar "uso do criador autorizado pela pessoa em DD/MM/AAAA" no relatório). Decisão da pessoa em 06/10/2026.
- Marca própria (criativo da própria operação ou página da pessoa) → clone da voz liberado.

**Lotes já feitos com este fluxo.**

| Lote | Rota | Data | Como foi | Onde |
|---|---|---|---|---|
| Podadora COD Chile | EN → ES-CL | até 05/10/2026 | AD 01–04 traduzidos, voz clonada do narrador (A=01/02, B=03/04), música separada com demucs | `Downloads\PODADORA-CL\` |
| Wyze Solar Cam | EN → ES LATAM | 05/10/2026 | 16 ADs, criadores de terceiros → B1 (voz de catálogo + avatar HeyGen nos vídeos com rosto 01, 06, 12, 14, 16); a pessoa vende a Wyze original, então a marca fica | `Downloads\WYZ-CAMARA-LATAM\` |
| Oración (página "Keiko Tanaka", da pessoa) | PT → ES neutro | 08/10/2026 | 18 vídeos, plano original + voz clonada + lipsync HeyGen speed; avatar completo foi testado e **rejeitado** | `Downloads\ADLIB-104060992792639\` |
| Mopa H2O X5 | EN → ES LATAM | 08/10/2026 | 15 vídeos + 12 imagens, marca da pessoa mantida, ~US$1,70 | `Downloads\MOPA VERDE - H2O X5\` |
| Enzimas UK | EN-EUA → EN-UK (localização) | 08/10/2026 | troca só das frases que não servem, voz clonada, lipsync só no trecho | `…\uk\` (ver `VOZES-CLONADAS.md`) |
| San Benito FR (vencedores OP2 ASCENSAO e JESU V07) | ES → FR | 13/10/2026 | refazer só fala, boca e legenda; visual igual | `Downloads\SB-VENCEDORES_OP2-ASCENSAO_JESU-V07\` |

**Caso ES → FR de 13/10/2026 (San Benito, infoproduto).**
- A pessoa apontou OP2 ASCENSAO e JESU V07 como vencedores do SB em espanhol (OP2 com ~US$2,1k de gasto na vida, ativo ES/US/EURO).
- Decisões:
  - francês geral, com "tu" (mesma publicação para todos os países francófonos);
  - mesma página de destino do ES;
  - mesma voz ElevenLabs "Jesus The Chosen ESPANHOL" (`AkQxVSf1kENGmX9WjeDE`);
  - San Benito → **"saint Benoît"**;
  - "caminho 1": refazer só fala/boca/legenda, com o visual igual;
  - máximo de agentes (1 agente por AD + revisor independente).
- Material limpo reaproveitado: b-rolls em `Downloads\SAN BENITO B-ROLS\`, takes limpos em `1-VIDEOS\SB-CORPO_CTA_COMPLETO_JESU.mp4`, hooks em `HOOKS SAO BENITO\`.
- Os ADs SB-JESU foram feitos fora do kit (sem receita JSON), com legenda queimada caixa alta branco + amarelo. O estilo de legenda deles não existe no kit, por isso o lote usou scripts próprios em `_trabalho\op2` e `_trabalho\v07`.
- CTA: **"Appuie sur « En savoir plus » maintenant."**, botão do Meta **LEARN_MORE**, a mesma lógica do "Más información" do ES. A v1 dizia "Touche « En savoir plus »" e foi trocada na v2. Por isso "touche" entrou na lista de termos proibidos do OP2.
- Entregue (v2, após revisor independente): `FR\SB-FR-OP2-ASCENSAO.mp4` (27,4 s; o `revisar_ad` mede 28,0 s) e `FR\SB-FR-JESU-V07.mp4` (31,9 s), em 1080×1920. As v1 ficaram em `FR\_versoes-antigas\`. Textos de anúncio e roteiros ES/FR em `FR\*.txt`.
- Custo: HeyGen ~346 créditos no total (7.982 → 7.636); ElevenLabs < US$0,40.
- Lição: o lipsync do HeyGen deixa o rosto mole. Colar só boca e queixo sobre o take original (`_trabalho\v07\colar_boca.py`) recupera a nitidez.
- Compliance: a fala manteve o mesmo teor do ES aprovado ("Ferme cette vidéo, et le miracle passe à une autre personne"), sem suavizar e sem intensificar, por decisão da pessoa.

**Regras de conteúdo já fixadas.**
- Nada de preço/moeda, país, plataforma de origem ("carrinho laranja", "link abaixo"), cupom, data/estação, escassez não comprovável, claims fora da ficha oficial.
- Oferta, selo, frete e garantia só se confirmados pela pessoa. A ficha oficial vale mais que o criativo.
- Nicho espiritual/fé: não suavizar nada por conta própria. Listar os riscos e perguntar "manter × suavizar".
- Fala nova em profissional de saúde (nutricionista/médica) foi bloqueada pelo filtro de segurança no lote Vitaly (V03/V11): não produzir.
- Lista de termos por país: `kit-edicao-criativos\exemplos\termos-por-pais.md`.

## Lógica de uso

### 1. Estudo do lote (antes de gastar)
1. Baixar na maior qualidade (≥720p; Biblioteca do Meta → `video_hd_url`), conferir com `ffprobe`, deduplicar por md5, renomear para `originais/NN.mp4` + `indice-arquivos.csv`.
2. Agentes em paralelo (1 por 3–6 vídeos): transcrição faster-whisper (idioma automático, `cpu_threads=4`), folha de contato 1 quadro/s, leitura dos quadros em tamanho cheio, OCR (RapidOCR) do texto da tela. **Whisper e OCR em sequência, nunca juntos.**
3. Conferir se o produto dos vídeos é o mesmo que a pessoa vende (modelo, cor, potência). Se não bater, parar e perguntar antes de orçar.
4. Por vídeo: o que não serve no mercado alvo, conflitos com a ficha, amostra de voz de cada narrador (voz isolada pelo demucs; com <30 s de fala o clone sai pior, avisar).
5. Duplicados: mesmo roteiro ou mesmo vídeo em outro formato (9:16 × 4:5 × 1:1). Duplicado de formato → uma mestra 9:16 e o par no outro formato com o mesmo texto, a mesma voz e o mesmo tempo.
6. Entregar `ESTUDO-<lote>.md` com tabela, alegações proibidas, classificação A/B/C/D, orçamento (US$ + tempo + opção mais rápida) e perguntas de bloqueio: marca da pessoa ou revenda? ficha oficial? oferta e países? vídeos a excluir? compliance sensível (manter/suavizar)? grupo B: B1 ou B2? Sem resposta, não produzir.

### 2. Briefing único
`producao/_trabalho/BRIEFING-AGENTES.md`, o mesmo para todos (1 agente por 1–2 vídeos): onde estão originais/transcrições/kit/exemplo pronto, ficha oficial e trocas fixas, regra de marca, CTA falado + palavra das setas, regra de voz, limites de CPU/GPU (`-threads 4`, `PYTHONIOENCODING=utf-8`), teto de créditos, revisão, formato do relatório, **pronúncia da marca escrita por extenso no texto do TTS (siglas e números soletrados), a mesma grafia em todos os vídeos**, e "não pergunte; na dúvida escolha o lado seguro e registre".

### 3. Grupo A (sem rosto)
1. Separar a música: `python -m demucs --two-stems=vocals <arquivo>` (GPU: `-d cuda`) e usar só o `no_vocals.wav`. Se a voz original ainda vazar, entregar sem trilha e anotar.
2. Roteiro no idioma alvo com a mesma estrutura (gancho, benefícios, CTA), ~15% mais curto que o original. Salvar `adNN/roteiro_<idioma>.txt`.
3. Narração: `python ferramentas/tts_elevenlabs.py --arquivo roteiro.txt -o adNN/narr.mp3 --voz <voice_id>` (gera `narr.alinhamento.json`). Velocidade ≤1,1x; se não couber, enxugar texto ou congelar take.
4. Corpo: `python ferramentas/preparar_corpo_traducao.py prep.json` (modelo `exemplos/traducao_exemplo.json`). Gera `corpo.mp4` + `alinhamento.json`.
5. `montar_ad.py` com `"resolucao": "720"`, legenda `alinhamento:` e setas na palavra do CTA. Depois `revisar_ad.py`.

Campos do `prep.json` (tempos em s; coordenadas em px da **saída**; caminhos relativos ao JSON):

| Campo | O que faz |
|---|---|
| `video`, `resolucao`, `formato` | original; `"720"`/`"1080"`; `"9:16"`/`"4:5"`/`"1:1"` |
| `cortes` | trechos mantidos do original, ex. `[[0.0, 30.0], [32.8, 52.0]]`; omitido = inteiro |
| `fundo`, `fundo_vol` | `no_vocals.wav` alinhado ao original (null = sem fundo) e multiplicador |
| `narr`, `narr_vol` | narração nova (+ `.alinhamento.json` ao lado) |
| `narr_inicio` + `atempo` · `offsets` · `blocos` | 3 modos: inteira com velocidade; por frase (início de cada frase no tempo do corpo); por blocos `[índice do 1º caractere, instante]` |
| `trocas` | correções de texto no alinhamento, ex. `[["Uais","Wyze"]]` |
| `faixas` | faixa preta opaca na largura toda, `{"y":[925,1062],"grad":18}` (ou `y_rel`) |
| `caixas` | caixas opacas, `{"rect":[…],"cor":[0,0,0],"raio":10,"de":…,"ate":…}` (ou `rect_rel`) |
| `titulos` | caixa branca com texto novo (emoji colorido), `linhas`, `px`, `cy`, `cobrir_w/h`, `de/ate` (ou `cy_rel`) |
| `aviso` | faixa de rodapé com texto pequeno, ex. "Solo con fines demostrativos." (`topo` ou `topo_rel`) |
| `desfocar` | `blur`/`preto`, `caixa`/`elipse`, chaves `[t, x0, y0, x1, y1]` interpoladas |
| `fim` | `{"folga":0.4,"max_total":null}`: congela o último quadro se a fala passar do vídeo |

### 4. Grupo B (rosto do criador)
**B1 (padrão):** sem lipsync e sem fala nova sobre o rosto real. Usar takes sem rosto (recorte 9:16 abaixo do rosto) + avatar próprio (~40–60% do tempo) com `montar_corpo_avatar.py`:
```
python ferramentas/montar_corpo_avatar.py plano.json [--saida corpo.mp4] [--placeholder] [--resolucao 720]
```
Segmentos do `plano.json` (modelo `exemplos/plano_avatar_exemplo.json`): `A` = avatar; `P` = tela cheia recortada do original (`x, y, w` + `faixa` opaca + `desfocar`); `S` = dividida (avatar em cima `av_y/av_h` + recorte do original `src_y/src_h` embaixo); `T` = clipe pronto. Formato: `["P", ini, fim, src_ini, vel, {sobrescreve}]`. `A_zoom`/`A_shift` sobem o rosto para a legenda não cobrir a boca. `--placeholder` usa a foto parada antes do HeyGen ficar pronto. Todas as partes saem com cor bt709/tv e emenda recodificada.

**B2 (mesmo criador, autorizado):** procurar clone em `kit-edicao-criativos\VOZES-CLONADAS.md` antes de clonar; `clonar_voz.py` → `tts_elevenlabs.py`; lipsync HeyGen pelo método de [09-lipsync-e-avatar-heygen.md](09-lipsync-e-avatar-heygen.md); aceite `checar_lipsync.py` com índice de pausa ≤0,6. Piloto completo antes do lote quando o método é novo. Manter o plano original; avatar completo só como alternativa.

### 5. Mesmo idioma, outro país (localização)
Não refazer o vídeo; trocar só as frases que não servem.
1. Mapa de troca: transcrição palavra a palavra + leitura da tela + `termos-por-pais.md`. Propor original → nova frase a frase e aprovar com a pessoa.
2. Emendas em pausa natural, medidas no envelope da voz isolada (demucs). Sem pausa antes: começar a troca na frase anterior e regravar as mesmas palavras.
3. Voz clonada de quem fala, fala nova no tempo da original (±0,3 s, velocidade 0,9–1,1x), mesmo LUFS; fora da troca, áudio original. Ferramenta: `trocar_trecho_audio.py` (ver [08-voz-e-dublagem.md](08-voz-e-dublagem.md)).
4. Rosto: lipsync só no trecho. Boca coberta (produto, mão, desfoque) → o HeyGen devolve a boca intacta e gasta crédito: trocar só o áudio.
5. Tela: apagar interface e país da plataforma de origem nas capturas; de preferência trocar a captura inteira.
6. Fala contínua sem pausa: o índice de pausa não dá número; aprovar a olho, quadro a quadro, e avisar a pessoa.

### 6. Imagens (estáticos e carrossel)
Tradução por edição de imagem com IA (lista exata original → novo, "nada mais muda"), no máximo 1 refação; se falhar, cobrir e reescrever localmente. Conferir com zoom (grafia, acentos, produto). Entregar folha original × tradução e listar o que a arte afirma e a ficha não confirma.

### 7. Receita do caso ES → FR (refazer só fala, boca e legenda)
Pasta de trabalho por AD: `_trabalho\op2\`, `_trabalho\v07\`.
1. Transcrever o ES por palavra (`transc.py`/`palavras.py`; `es_words.json`) e escrever o roteiro FR frase a frase no mesmo tempo das cenas (`audio\hook_fr.txt`, `audio\corpo_fr.txt`).
2. Gerar a voz FR com a mesma voz ElevenLabs, com alinhamento. Regravar uma frase isolada (ex.: o CTA) via API `with-timestamps` com `previous_text`/`next_text` para manter a entonação, `speed` 0.9 (`tts_cta.py`), e emendar no áudio do corpo cortando a meio caminho entre as palavras vizinhas, com fade de 10 ms, e reescrever o alinhamento (`splice.py`).
3. Casar a fala com as cenas do ES: inserir silêncios nos pontos medidos e deslocar o alinhamento (`esticar_pausas.py`).
4. Música: demucs no áudio do AD ES e reconstrução do `no_vocals` cena a cena, alinhada pelo fim de cada cena, com rampas de 30 ms e fade final de 0,4 s (`bed.py`, `mix_audio_v2.py`).
5. Boca: recortar os trechos com Jesus falando (`ls\in_*.mp4` com o áudio ES original, `au_*.mp3` com o FR), lipsync HeyGen por trecho (`out_*.mp4`), colar só boca + queixo no take original (`colar_boca.py`, resultado `pt_*.mp4`).
6. Compor o vídeo sem legenda (`compose.py`/`compor_v2.py`): cenas da timeline, push-in leve 1,00 → 1,06, fusão de 0,2 s (corte seco entre gancho e corpo, como no ES), vinheta medida no AD ES, leitura e gravação com matriz bt601 fixa.
7. Legenda própria no estilo do ES (`legenda_fr.py`, `gerar_legenda_v2.py`): ASS karaokê caixa alta, branco + palavra falada em amarelo, centro y≈1463–1465 (Poppins ExtraBold 83 no V07, Poppins Bold 60 no OP2), blocos ≤3 palavras/16 caracteres, frase do CTA em blocos fixos.
8. Mix e render (`montar_final.sh`): voz `loudnorm I=-15:TP=-2`, fundo −6,7 dB, mix final `loudnorm I=-14:TP=-1.5`, seta amarela oscilando a partir do instante do CTA, H.264 crf 14, AAC 192k.
9. Revisão: `revisar_ad.py --idioma fr --idioma-residual es --proibidos proibidos_fr.txt --lipsync …` + revisor independente (OCR, luma ES × FR, nitidez do rosto FR × ES com `nitidez.py`, folhas da boca).

### Armadilhas
- **CTA FR:** usar "Appuie sur « En savoir plus »", não "Touche" (a v1 saiu com "Touche" e foi refeita; o motivo da troca não está registrado — precisa de revisão manual se for virar regra geral). O botão precisa ser LEARN_MORE.
- **Whisper residual em idioma próximo** (ES sobre áudio FR) devolve uma "tradução" da fala nova ("Ferme este video, y el Miracle…"), não fala residual de verdade. Ler o conteúdo e procurar frases do roteiro original, não contar linhas.
- **Seta amarela** (estilo SB-JESU) faz o `revisar_ad.py` avisar "não achei setas vermelhas no último quadro": falso alerta, conferir a olho.
- Faixa sobre legenda queimada precisa de alpha ≥250, senão o texto original aparece por baixo.
- Velocidade da voz acima de 1,1x soa apressada: enxugar o texto.
- Preço em "$" lê como moeda local na LATAM; números 4.000 (CL/CO) × 4,000 (MX/GT).

### Checklist de saída
- [ ] Estudo respondido (marca, ficha, oferta, B1/B2, compliance).
- [ ] Whisper alvo bate com o roteiro; residual sem fala original; nenhum termo proibido em áudio e tela.
- [ ] Nenhuma legenda/texto antigo, nem por 0,3 s nas emendas.
- [ ] Lipsync (se houver) com índice do conjunto ≤0,6 e nitidez do rosto conferida.
- [ ] CTA falado = palavra das setas = botão do Meta.
- [ ] `RELATORIO.md` por AD (voz, caracteres TTS, créditos, trocas, pendências) + `00-RELATORIO-PRODUCAO.md` + textos de anúncio.

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [02-regras-gerais-e-seguranca.md](02-regras-gerais-e-seguranca.md)
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [04-fluxo-producao-criativos.md](04-fluxo-producao-criativos.md)
- [06-troca-de-marca.md](06-troca-de-marca.md)
- [08-voz-e-dublagem.md](08-voz-e-dublagem.md)
- [09-lipsync-e-avatar-heygen.md](09-lipsync-e-avatar-heygen.md)
- [10-limpeza-cor-e-qualidade-de-video.md](10-limpeza-cor-e-qualidade-de-video.md)
- [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)
- [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md)
- [13-analise-meta-ads-e-vencedores.md](13-analise-meta-ads-e-vencedores.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)
- [projetos/](projetos/)
