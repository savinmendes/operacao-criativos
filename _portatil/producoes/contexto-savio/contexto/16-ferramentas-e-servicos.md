# Ferramentas e serviços (inventário)

> Tudo o que a produção de criativos e a operação usam: serviços pagos, IA local grátis, ffmpeg, cada script do kit, as ferramentas de `ferramentas/` e os conectores (MCPs). Para cada um: custo, quando usar e onde está. Abra para escolher a ferramenta certa ou montar um orçamento.

## Contexto de uso

Raiz do projeto: `C:\Users\PICHAU\Downloads\Produtividade com ia\`. Kit de edição: `kit-edicao-criativos\` (scripts em `ferramentas\`). Chaves ficam em `.env` (kit: ElevenLabs; `ferramentas\gerador-criativos-video\.env`: fal.ai/ElevenLabs/HeyGen). **Nunca ler nem imprimir `.env`.** Preços abaixo são os registrados nas fontes, com data quando houver; orçar sempre pelo preço real medido.

### Serviços pagos de IA

| Serviço | Custo registrado | Quando usar | Onde / como |
|---|---|---|---|
| **ElevenLabs** (TTS, clone, STS, Dubbing) | ~US$0,165 / 1.000 caracteres (`eleven_multilingual_v2`); clone instantâneo sem cobrança por uso no plano; Dubbing usa créditos do plano | Narração com alinhamento para legenda, voz clonada do narrador, troca de trecho de fala, STS para voz única por avatar | `tts_elevenlabs.py`, `clonar_voz.py`, `dublar.py`; MCP ElevenLabs (1 geração por vez) |
| **HeyGen** (avatar, lipsync) | Plano Pro, créditos premium que zeram ~dia 30 (9.148 em 04/10/2026). UGC ~50 s ≈15 créditos; lipsync speed: Oración ~9 créditos/AD, SB FR ~346 para 2 ADs (custo varia; medir saldo antes e ~1 h depois) | Avatar UGC/hook, modo B1, lipsync sobre vídeo existente (B2/marca própria). Opção "sem custo extra" em orçamentos | MCP HeyGen (`create_video_from_image`, `create_lipsync`, `get_current_user`) |
| **Flora** (canvas de imagem/vídeo/QA) | i2i `i2i-gpt-image-2-5-flare` ~US$0,073/img; Nano Banana Pro `i2i-gemini-3-pro` ~US$0,18; vídeo `i2v-kling-2.5` ~US$0,294/5 s e US$0,588/10 s; QA `v2t-gemini-3.1-pro` ~US$0,025/vídeo. Medido no Yara: imagem 2k US$0,53 (cotação dizia 0,25); GPT Image 2 1k ~US$0,27 | Imagens base i2i a partir da foto original, takes de vídeo, QA de cada take por outro modelo | MCP Flora; upload local com `flora_upload.py`/`flora_up.py`. Projeto San Benito `prj_ns721bmqbf08c3b5ewg8ys06ds8ezc95` |
| **Kling O1 Edit** (via Flora) | ~US$0,706 por clipe (Lymphoria) | Trocar rótulo/produto em cena quando a faixa não resolve; nunca em rosto Pixar/3D; take ≥3 s | MCP Flora |
| **Seedance** (via Flora) | ~US$0,21/s (Seedance 2.0, Yara 09–10/10/2026) | Take com personagem falando gerado do zero (gancho) | MCP Flora; transcrever cada take (erra palavras raras/"ñ", repete frase no fim) |
| **Nano Banana 2** (via Flora) | Linfarele: ~US$10,37 por 144 gerações; Pellorini: US$9,18 por 77 fotos; Mopa: US$1,40 em imagens | Edição/rebrand de imagens e tradução de arte | MCP Flora; reescreve texto pequeno — colar a região original de volta |
| **fal.ai** | Não registrado nas fontes — precisa de revisão manual | Motor do `gerador-criativos-video` (b-roll e imagem de avatar por prompt) | Padrões `fal-ai/bytedance/seedance/v1/pro/text-to-video` (vídeo) e `fal-ai/flux-pro/v1.1` (imagem) |
| **Canva** | Não registrado nas fontes — precisa de revisão manual | Conector disponível (designs, export, brand kit); sem uso registrado na produção de criativos | MCP Canva (claude.ai) |

### IA local grátis

| Ferramenta | Para quê | Onde / como |
|---|---|---|
| **faster-whisper** | Transcrição com tempo por palavra (legenda, ponto de corte, revisão, banco de tomadas) | `legenda.py --transcrever`, `palavras_trecho.py`, `revisar_ad.py`, `gerar_variacao.py banco`. Modelo `small` (~250 MB, baixa na 1ª vez). GPU falhou com `cublas64_12.dll` no Yara → `device='cpu', compute_type='int8'` |
| **RapidOCR** (`rapidocr_onnxruntime`) | Ler texto queimado na tela (tradução, revisão) | scripts de lote (ex.: `_trabalho\revisor\ocr.py` do SB FR). Rodar em sequência com o whisper |
| **demucs** | Separar música da voz (`--two-stems=vocals`): fundo para tradução/variação, amostra limpa para clone | `python -m demucs --two-stems=vocals arquivo` (`-d cuda`); `gerar_variacao.py fundo` |
| **Real-ESRGAN** | Upscale 2x/3x (`realesr-animevideov3`) | `upscale_video.py`; binário em `kit-edicao-criativos\_ferramentas_extras\realesrgan\` |
| **LaMa** (`simple_lama_inpainting`, GPU) | Tirar legenda queimada sem borrão (método padrão) | venv `ADLIB-104060992792639\producao\_trabalho\_vg`, `_lote\lama_base.py` |
| **MediaPipe Face Landmarker** | Achar rosto/boca: aceite de lipsync, colar boca, fechar boca | `checar_lipsync.py` (modelo de 3,7 MB em `~/.cache/kit-edicao/`), `colar_boca.py`, `fechar.py` |
| **OpenCV** | Inpaint simples, troca de rótulo/texto quadro a quadro | `remover_legenda.py`, `trocar_rotulo_faixa.py`, `trocar_texto_tela.py` |
| **Playwright + Chrome headless** | Capturar `video_hd_url` na Biblioteca do Meta | `ADLIB-104060992792639\buscar_hd.py` |
| **yt-dlp** | Baixar vídeo/áudio de plataformas | `-f "bv*+ba/b"`; usado também pelo `transcritor-youtube` |

**ffmpeg/ffprobe** (instalado via `winget install Gyan.FFmpeg`): base de tudo. Medição (`ffprobe`), corte (`-ss -t` + `tpad=stop_mode=clone`), `loudnorm`, `scdet`, `silencedetect`, filtros `ass`/`overlay`. Na versão 9: `-fps_mode passthrough` no lugar de `-vsync`.

### Scripts do kit (`kit-edicao-criativos\ferramentas\`, 32 arquivos)

| Script | Uma linha |
|---|---|
| `audio.py` | `mix` (voz −15 + trilha −29 com ducking), `trocar` (narração nova no vídeo), `pausas` (corta silêncios), `normalizar` |
| `caixa_legenda.py` | Acha a caixa da legenda queimada num instante, pronta para o `trocar_texto_tela.py` |
| `checar_lipsync.py` | Aceite de lipsync: a boca mudou? fecha nas pausas da voz nova? (índice de pausa) |
| `clonar_voz.py` | Instant Voice Clone do ElevenLabs a partir de um trecho do vídeo → voice_id |
| `colar_produto.py` | Cola só o produto do take editado por IA sobre o original (silhueta de frasco âmbar/verde/preto) |
| `comum.py` | Funções comuns: resoluções, formatos, layout padrão, fontes, checagens |
| `desfocar_regioes.py` | Desfoca caixas num intervalo (tela de celular, marca de terceiros) |
| `dublar.py` | Dublagem automática ElevenLabs Dubbing (tradução literal) |
| `encaixar_edit.py` | Realinha take do Kling (24 fps) ao tempo original e restaura a legenda queimada (só na faixa 0,62–0,90) |
| `finalizar.py` | Reencoda no padrão de entrega ≤30 MB, decodifica, confere e gera `_frames.jpg` |
| `flora_up.py` | Upload compacto para o slot signed-url do Flora |
| `flora_upload.py` | Upload de arquivos/lote para os slots signed-url do `flora_create_asset` |
| `folhas_contato.py` | Folhas de contato 1 quadro a cada N s com o tempo escrito |
| `gerar_variacao.py` | Variações gancho × corpo: `banco`, `fundo`, `montar` (modos A/B) |
| `legenda.py` | Legenda corrida palavra a palavra (alinhamento ElevenLabs, whisper ou texto), estilos `drop`/`sb` |
| `montar_ad.py` | Monta o AD inteiro por receita JSON e finaliza |
| `montar_ad_rapido.py` | Versão de uma passada de ffmpeg (usada pelo `montar_ad.py`), com `-reinit_filter 0` |
| `montar_corpo_avatar.py` | Corpo com avatar HeyGen intercalado com takes sem rosto (A/P/S/T) |
| `overlays.py` | PNGs de camada: manchete, faixa SB, selo COD, seta |
| `palavras_trecho.py` | Transcreve um trecho com tempo por palavra para achar pontos de corte |
| `preparar_corpo_traducao.py` | Corpo traduzido: cortes, faixas/caixas opacas, título novo, aviso, desfoque, narração + fundo demucs, fim congelado |
| `remendo_rastreado.py` | Troca texto plano que se move pouco (cabeçalho de tela) rastreando a caixa |
| `remover_legenda.py` | Remove legenda/marca por `inpaint`/`blur`/`delogo`/`cortar` (OpenCV) |
| `revisar_ad.py` | Revisão automática final (whisper, proibidos, folha, quadro solto, silêncio, pts, setas, lipsync) |
| `substituir_trechos.py` | Troca trechos do vídeo por clipes corrigidos, quadro a quadro, mantendo o áudio |
| `trocar_rotulo_faixa.py` | Troca o texto da faixa do rótulo sem IA (`--auto`, `--seguir`, `--caixa`) |
| `trocar_texto_tela.py` | Troca texto queimado na tela (marca na legenda) num intervalo |
| `trocar_trecho_audio.py` | Troca uma fala por outra no mesmo tempo (0,8x–1,25x) |
| `tts_elevenlabs.py` | Narração ElevenLabs com alinhamento por caractere (apelidos `divina`, `chilena`) |
| `upscale_video.py` | Upscale Real-ESRGAN em blocos de 30 s, com progresso |
| `varrer_produto.py` | Varre vídeos atrás de um rótulo por moldes e estima quantos takes trocar |
| `video.py` | `vertical`, `dividida`, `montagem`, `hook`, `takes`, `concat` |

Testes do kit: `tests\test_formatos.py`, `tests\test_checar_lipsync.py`. Receitas-modelo em `exemplos\` (ver [04-fluxo-producao-criativos.md](04-fluxo-producao-criativos.md)).

### Ferramentas em `Produtividade com ia\ferramentas\`

| Ferramenta | O que é | Como rodar |
|---|---|---|
| `gerador-criativos-video\` | Gera criativo 9:16 a partir de `roteiro.json` (cenas `broll` e `avatar` com `cutaways`) via fal.ai + ElevenLabs + HeyGen (API direta, `.env` próprio) + ffmpeg. `lib/flora_client.py` existe, mas não é o padrão | `python main.py [--roteiro outro.json --aspect-ratio 9:16]`; testes `python -m pytest tests/test_smoke.py -v` |
| `corrigir-videos-tiktok\` | Site local (porta 8750) que acha vídeos recusados por resolução/bitrate e corrige em lote para `corrigidos/`. Perfis: TikTok Ads 540×960 e 350 kbps; Meta Ads 500×500. Não sobrescreve originais | `abrir-corretor.bat` ou `python servidor.py [porta] [--sem-navegador]`; testes `python -m unittest discover -s tests` |
| `transcritor-youtube\` | Fila de links → transcrição (legenda do YouTube; senão Whisper local `large-v3` na GPU) | `python transcritor.py add <url>` · `lista` · `rodar [--motor legenda\|whisper] [--limite 20]` |
| `empacotar-skills.py` | Gera os .zip das skills de `.claude/skills/` para o claude.ai. Para se o `name:` ≠ nome da pasta ou se houver caminho local nos arquivos | `python ferramentas/empacotar-skills.py` |
| `calculadora-cod\` | Unit economics do COD (fora do escopo de criativos) | `python -m unittest discover -s tests` |
| `arrumar-downloads.py` | Mantém `Downloads` navegável: move só **arquivos soltos da raiz** para `1-VIDEOS`, `2-IMAGENS`, `3-AUDIO`, `4-DOCUMENTOS`, `5-PLANILHAS`, `6-PACOTES`, `7-OUTROS` (sem subpastas, sem renomear, nunca toca em pastas). Arquivos mais novos que `--dias` ficam na raiz. Log CSV por execução (`Downloads\_arrumacao-AAAAMMDD-HHMMSS.csv`) | Simula por padrão; `--executar [--dias 3]`; `--desfazer <log.csv>`. Tarefa agendada do Windows "Arrumar Downloads" roda todo dia às 09:00; `Downloads\_arrumar.bat` roda na hora. Consequência: arquivo citado como solto em `Downloads\` pode estar em `Downloads\1-VIDEOS\` etc. |
| `painel\painel.py` (raiz) | Painel ao vivo de etapas, http://127.0.0.1:8765 | ver [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md) |

### Conectores (MCPs)

Estado observado na sessão de 13/10/2026 (pode mudar):

| Conector | Para quê | Observações |
|---|---|---|
| **Meta Ads** | Campanhas, conjuntos, anúncios, criativos, insights, Biblioteca de Anúncios | conectado |
| **TikTok for Business** | Relatórios, Smart+ (campanha/conjunto/anúncio), pixels, identidades | conectado |
| **Stripe** | Saldo, analytics, API de leitura e escrita | conectado |
| **Shopify** | Produtos, coleções, pedidos, tema (GraphQL) | o conector bloqueia gravar no tema publicado e publicar tema: `themeDuplicate` → gravar na cópia → a pessoa publica |
| **DropKiller** | Biblioteca de anúncios Meta/TikTok, radar de lojas Shopify, produtos vencedores | conectado no claude.ai; o servidor do projeto (`.mcp.json`) pedia autenticação |
| **WinningHunter** | Anúncios FB/TikTok/Google/Pinterest, lojas, produtos, transcrição de anúncio | conectado no claude.ai; o do projeto pedia autenticação |
| **Minerador** (de Ofertas) | Mineração COD/e-com, Raio-X global, top criativos | ferramentas que gastam créditos avisam na descrição; uma 2ª instância pedia autenticação |
| **Dropi / Chegou Operações** | Dados do Drop e do X1 (somente leitura, SELECT único por frente) e páginas livres | o "Dropi" do claude.ai falhou (502) nesta sessão; o `chegou-operacoes` do projeto pedia autenticação |
| **Flora**, **HeyGen**, **ElevenLabs** | Geração de mídia (ver acima) | declarados no `_instalar\mcp.json` do kit; conectados no claude.ai |
| **Canva** | Designs e export | sem uso registrado |
| **Google Drive**, **Gmail** | Arquivos e e-mail | conectados |
| **OpusClip** | Cortes de vídeo | exige plano Pro/Max/Enterprise para MCP |
| **Claude Docs** | Documentos editáveis | conectado |
| ATOMICAT, Higgsfield, UTMFY, Video Tolkil, WHOP | — | pediam autenticação nesta sessão; uso não registrado nas fontes |

## Lógica de uso

### Escolher a ferramenta
1. **Existe script do kit?** Use-o (todos têm `--help`) antes de escrever código de lote. Formatos 4:5/1:1 já são do kit: não escrever compositor próprio.
2. **Dá para fazer grátis/local?** Prefira:
   - `trocar_rotulo_faixa.py` antes do Kling;
   - `fechar.py` antes de reenviar lipsync;
   - demucs, whisper e OCR locais.
3. **Pago:** orçar peças × preço real medido (não a cotação do catálogo), tempo médio e opção paga mais rápida, lado a lado. Parar para aprovação só aí. Oferecer HeyGen (créditos que vencem) como opção sem custo extra quando servir.
4. **Teto por peça** definido antes do lote; estourou → parar e relatar. Nunca repetir geração paga sem avisar; informar o custo real no fim.

### Ambiente
- Rodar os scripts do kit com o diretório de trabalho em `kit-edicao-criativos\`.
- Git Bash: `PYTHONIOENCODING=utf-8`. `revisar_ad.py --lipsync` pelo PowerShell.
- Uma tarefa pesada de GPU por vez (fila). Whisper e OCR em sequência.
- Flora: `flora_list_generations` às vezes dá timeout; esperar ~60 s e consultar de novo (o job continua). Seedance: esperar até ~30 min antes de regerar.
- HeyGen: job >45 min parado → reenviar igual (custa de novo).

### Pendências / revisão manual
- Custo do fal.ai e do Canva: não registrado.
- `audio.py mix` usa trilha a −29 LUFS; o padrão da pessoa desde 09/10/2026 é −32 LUFS.
- A skill `revisar-criativo` cita `--residual`; o argumento real do `revisar_ad.py` é `--idioma-residual`.

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [02-regras-gerais-e-seguranca.md](02-regras-gerais-e-seguranca.md)
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [04-fluxo-producao-criativos.md](04-fluxo-producao-criativos.md)
- [05-traducao-de-criativos.md](05-traducao-de-criativos.md)
- [06-troca-de-marca.md](06-troca-de-marca.md)
- [07-variacoes-gancho-corpo.md](07-variacoes-gancho-corpo.md)
- [08-voz-e-dublagem.md](08-voz-e-dublagem.md)
- [09-lipsync-e-avatar-heygen.md](09-lipsync-e-avatar-heygen.md)
- [10-limpeza-cor-e-qualidade-de-video.md](10-limpeza-cor-e-qualidade-de-video.md)
- [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)
- [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md)
- [13-analise-meta-ads-e-vencedores.md](13-analise-meta-ads-e-vencedores.md)
- [14-unit-economics-cod.md](14-unit-economics-cod.md)
- [15-lojas-e-paginas.md](15-lojas-e-paginas.md)
- [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)
- [projetos/](projetos/)
