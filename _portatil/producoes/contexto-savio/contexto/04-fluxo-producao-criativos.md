# Fluxo de produção de criativos (visão geral do pipeline)

> Mapa do caminho de um criativo de vídeo, do briefing à entrega: o que existe, onde está e em que ordem rodar. Abra antes de qualquer produção ou edição de AD.

## Contexto de uso

**O que é.** A produção de criativos da pessoa roda num kit de scripts Python próprio (`kit-edicao-criativos`), com ffmpeg por baixo e serviços de IA plugados (Flora/Kling, HeyGen, ElevenLabs). O Claude Code atua como editor, roteirista e operador técnico e entrega o vídeo **pronto para subir**, não sugestões.

**Onde fica.**
- Kit: `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\` (regras em `CLAUDE.md`, scripts em `ferramentas\`, receitas-modelo em `exemplos\`, fontes Anton/Poppins em `fonts\`, testes em `tests\`).
- Skills que guiam o fluxo: `editar-criativo`, `gerar-midia-ia`, `revisar-criativo`, `traduzir-criativo`, `adaptar-marca` (em `.claude\skills\` do projeto; as três primeiras são atalhos para `kit-edicao-criativos\.claude\skills\`). Para planejar diversidade de lote: skill `andromeda`.
- Requisitos: Windows, Python 3.12, `ffmpeg`/`ffprobe` no PATH, `pip install -r requirements.txt` (instalação descrita em `README-INSTALACAO.md`). Chave do ElevenLabs no `.env` do kit (nunca ler nem imprimir).

**Peças do pipeline (o que cada uma faz).**
- `comum.py`: resolução, FPS, fontes, layout padrão por formato.
- `montar_ad.py`: lê uma receita JSON e monta o AD inteiro. Delega para `montar_ad_rapido.py` (uma passada de ffmpeg: partes → legenda ASS de `legenda.py` → overlays de `overlays.py` → setas de CTA → compressão). Receitas com `cortar_pausas`, `trilha` ou hook `tipo: imagem` caem automaticamente no caminho clássico; `--classico` força o clássico.
- `finalizar.py`: reencoda no padrão de entrega, decodifica o arquivo inteiro, confere resolução/áudio e gera `<nome>_frames.jpg`. O `montar_ad.py` já chama.
- `revisar_ad.py`: revisão automática final (ver [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)).

**Padrão de entrega (fixo).** H.264 high, yuv420p, 30 fps, AAC 48 kHz estéreo 128k, `+faststart`, ≤30 MB (o `finalizar.py` calcula o bitrate). Vídeo longo que não cabe em 30 MB com qualidade sai acima do limite e isso é anotado; nunca degradar abaixo do piso.

**Resolução (decisão de 03/10/2026).** Origem 360p/480p que precisa de upscale → entrega em **720×1280** (`upscale_video.py --escala 2` + receita `"resolucao": "720"`). No teste lado a lado do AD 03 a diferença foi "imperceptível" nas palavras da pessoa, com metade do tempo (32 s × 64 s para 30 s de vídeo) e metade do tamanho. **1080×1920** só quando a origem já é ≥720p ou quando um AD vencedor é refeito. O `montar_ad_rapido` em 720 usa piso de 900 kbps.

**Formatos aceitos pelo kit.** 9:16 (padrão), 4:5 e 1:1, em 720 ou 1080 de largura:

| Formato | 720 | 1080 | Quadro base das posições |
|---|---|---|---|
| 9:16 | 720×1280 | 1080×1920 | 1080×1920 |
| 4:5 | 720×900 | 1080×1350 | 1080×1350 |
| 1:1 | 720×720 | 1080×1080 | 1080×1080 |

Antes dessa mudança (lote Mopa, 08/10/2026) o kit só aceitava 9:16 e os agentes escreveram compositor próprio para 4:5/1:1. Hoje isso não é mais necessário; existe a pasta `_backup_formatos_20261009` no kit.

**Padrões visuais fixos.**
- Legenda (público sênior): grande, branca com contorno preto, 1 palavra-chave amarela por bloco, blocos ≤3 palavras/16 caracteres, "pop" de entrada. Estilo `drop`: Poppins Bold ~107 px, centro y=1060. Estilo `sb` (San Benito): Anton ~116 px, centro y=1480 + faixa de topo "‼️ Un último aviso ‼️ …".
- CTA sem cara de botão: 2 setas vermelhas (~170 px, x 300 e 610, y 1630 oscilando ±20 px) que entram na palavra do CTA ("Toca"/"Pide") e ficam até o fim. O botão do Meta precisa bater com o que o vídeo manda tocar (San Benito: "Ver más"/SEE_MORE ou "Más información"/LEARN_MORE; COD: SHOP_NOW).
- Drop COD: manchete no topo (y≈140) só durante o hook + selo COD ("PAGO CONTRA ENTREGA · ¡PAGAS AL RECIBIR!").
- Nada cobre o rosto/boca de quem fala. Manchete fixa no meio = sem legenda ao mesmo tempo.
- Sem hora do dia ("esta noche", "hoy") na fala ou no texto.
- Receita do vencedor: hook (~4,5–5 s) + corpo que começa exatamente na 1ª frase do corpo + CTA com setas até o fim. Escalar trocando **uma variável por vez**.

**Nomenclatura.** Cada produto/oferta tem sua sequência (`AD 01` para produto novo; San Benito segue a dele). Arquivo `AD NN - <OFERTA>-<FORMATO>-<VOZ/IDIOMA>-<VARIAÇÃO>.mp4`. No Meta: nome do conjunto = nome do anúncio = "AD NN". Pastas de lote: `<AAAA-MM>_<tipo>_<produto>/` com `ads/`, `takes/`, `imagens/`, `audio/`, `textos/`; lotes de tradução/adaptação usam `producao/` + `producao/_trabalho/adNN/`.

**Decisões de processo já tomadas.**
- Checklist de abertura numa mensagem só (09/10/2026, após a produção Yara BF): oferta e se fala preço, mercado, avatar, referências, **orçamento diário de mídia**, teto de produção e música. No Yara saíram 25 vídeos para uma verba que comportava ~7, e a oferta mudou no meio (com preço → sem preço).
- Piloto antes do lote só quando o método é novo ou caro; método já validado e barato → todos os vídeos em paralelo, máximo de agentes.
- Confirmação só antes de gasto real (API paga) ou ação destrutiva; orçamento sempre com custo + tempo + opção paga mais rápida lado a lado.
- Toda tarefa longa registra etapas no painel ao vivo (`painel/painel.py`, http://127.0.0.1:8765) — ver [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md).
- Ao terminar uma prova/versão: abrir o vídeo (`Start-Process`) e pôr o link clicável no topo da resposta.

## Lógica de uso

### 1. Abertura (antes de gastar)
1. Mandar **uma** mensagem com a checklist: oferta (mecânica, fala ou não preço, escassez, tema), mercado/país, avatar, referências, orçamento diário de mídia, teto de produção (US$), música.
2. Classificar a origem do material — decide voz e rosto (ver [05-traducao-de-criativos.md](05-traducao-de-criativos.md) e [06-troca-de-marca.md](06-troca-de-marca.md)):
   - marca própria → clone de voz permitido;
   - criador de terceiros com rosto → a pessoa escolhe B1 (avatar próprio, padrão) ou B2 (mesmo criador, só com autorização confirmada);
   - rosto Pixar/3D → não usar Kling no rosto.
3. Baixar a fonte na maior qualidade (≥720p) e conferir com `ffprobe` (ver [10-limpeza-cor-e-qualidade-de-video.md](10-limpeza-cor-e-qualidade-de-video.md)).
4. Descobrir o próximo número de AD: listar `ads/` (ou `producao/`) da oferta e continuar do maior.
5. Orçamento: peças × preço = total, tempo médio e opção paga mais rápida. Parar para aprovação só se houver gasto real.

### 2. Mídia IA (quando precisa gerar)
- Imagens base → aprovar → só então vídeo/avatar ("frames antes de vídeo").
- Takes Kling 5 s por padrão, QA por outro modelo de visão, avatar HeyGen, narração ElevenLabs. Detalhes em [08-voz-e-dublagem.md](08-voz-e-dublagem.md), [09-lipsync-e-avatar-heygen.md](09-lipsync-e-avatar-heygen.md) e [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md).

### 3. Montagem por receita
Padrão: **uma receita JSON** + `python ferramentas/montar_ad.py receita.json`. Tarefa isolada → script direto (todos têm `--help`). Rodar com o diretório de trabalho em `kit-edicao-criativos\`; no Git Bash, prefixar `PYTHONIOENCODING=utf-8`.

Campos da receita (só `saida` e `corpo` — ou `narracao`+`takes` — são obrigatórios):

| Campo | Valores / exemplo | Observação |
|---|---|---|
| `saida` | `"ads/AD 08 - DESMALEZADORA-FERNANDO-ES-CL-G-GRAMA.mp4"` | |
| `estilo` | `"drop"` ou `"sb"` | `sb` liga a faixa de topo |
| `corpo` | `"corpo/fernando_es.mp4"` | vídeo com a fala |
| `narracao` + `takes` | `"audio/narr.mp3"`, `["takes/N01.mp4", …]` | monta b-roll sem repetir |
| `cortar_pausas` | `true` | tira silêncios longos (caminho clássico) |
| `hook` | `{"tipo":"imagem","video":"hook.mp4","ate":4.5}` · `{"tipo":"imagem","trechos":[["X04.mp4",0.9,1.6]],"vel":1.3}` · `{"tipo":"antes","video":"hook_avatar.mp4"}` | `imagem` cobre a imagem do início e o som do corpo segue; `antes` = avatar com fala própria antes do corpo |
| `trilha` | `"audio/trilha.mp3"` | trilha baixa com ducking |
| `legenda` | `{"fonte":"alinhamento:narr.alinhamento.json","chaves":["árboles"],"desde":0}` | `fonte`: `transcrever` · `alinhamento:<json>` · `texto:frases.txt` · `nenhuma` |
| `legenda_hook` | `{"fonte":"transcrever","idioma":"it","corrigir":[[regex, troca]]}` | legenda a parte 1 (vídeo dublado) e corrige grafia da marca |
| `manchete` | `{"texto":"¡DEJA EL PASTO PERFECTO! 😱","y":140,"ate":4.5,"px":64}` | `ate` = fim do hook |
| `faixa_sb` | `true` | padrão no estilo `sb` |
| `selo` | `{"linhas":["…","PAGO CONTRA","ENTREGA","¡PAGAS AL RECIBIR!"],"x":160,"y":1225,"desde":5}` | aceita `escala` |
| `cta` | `{"palavra":"pide"}` ou `{"inicio":22.5}` | setas entram na palavra; aceita `y`, `escala` |
| `formato` | `"9:16"` · `"4:5"` · `"1:1"` | |
| `resolucao` | `"720"` · `"1080"` | largura |
| `limite_mb` | `30` | |

Posições (`legenda.y`, `manchete.y`, `selo.x/y`, `cta.x/y`, `faixa_sb.y`) são px do **quadro base de 1080 de largura** do formato, mesmo com `"resolucao": "720"`. Alternativa: `"y_rel"` (0–1 da altura). Sem posição, vale o padrão do formato:

| Formato | Legenda y | Selo | Setas | Escala selo/setas |
|---|---|---|---|---|
| 9:16 | 1060 (drop) / 1480 (sb) | padrão de sempre | 1630 | 1 |
| 4:5 | 745 | topo, y=243 | 1114 | 0,85 |
| 1:1 | 596 | y=216 | 876 | 0,75 |

Ajustes conhecidos: em 720 com faixa no rodapé, `selo.y ≈ 1110` e `cta.y ≈ 1490` para as setas não ficarem sobre a faixa. Receitas-modelo: `exemplos/ad_exemplo.json` (drop), `sb_exemplo.json` (San Benito), `ad_4x5_exemplo.json`, `ad_1x1_exemplo.json`.

Escolhas padrão: legenda por `alinhamento:` quando a narração veio do `tts_elevenlabs.py`; senão `transcrever` no idioma do mercado; transcrição errada → `texto:` com o roteiro real. Padrão novo (09/10/2026): **legenda pelo roteiro** com alinhamento forçado desde a 1ª versão (whisper sobre o vídeo montado atrasou até 0,7 s e obrigou a remontar 21 vídeos).

Scripts avulsos mais usados (`video.py`): `vertical` (sem barra preta, `--formato`), `dividida` (avatar em cima + b-roll embaixo, sem borda), `montagem` (hook rápido), `hook` (troca a imagem dos 1ºs s), `takes` (b-roll 4–5 s/take, velocidade = máx(0,5; mín(1; duração/4,8))), `concat`.

### 4. Finalizar
```
python ferramentas/finalizar.py bruto.mp4 -o "AD 08 - DESM-H09-GRAMA.mp4"
python ferramentas/finalizar.py bruto_4x5.mp4 -o final.mp4 --formato 4:5 --resolucao 720
python ferramentas/finalizar.py final.mp4 --so-revisar
```
Abrir o `_frames.jpg` e olhar antes de seguir.

### 5. Revisão
`revisar_ad.py` em todo arquivo final + skill `revisar-criativo` + zoom 3x em takes editados. Lote ≥10 vídeos: revisor independente (subagente). Ver [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md).

### 6. Entrega
- Lote: fazer 1, mostrar `_frames.jpg` + caminho, esperar aprovação quando o método for novo; depois o resto em paralelo. Processos longos com `[k/N]` + % + tempo restante.
- Junto de cada vídeo, `.txt` com o texto do anúncio: cabeçalho (conta, botão CTA pelo nome da API, link, regra de nomes) e, por AD, título (≤ ~40 caracteres) + texto principal (3–4 linhas) + versão TikTok ≤100 caracteres quando pedido.
- Relatório do lote (`00-RELATORIO-PRODUCAO.md`): custo real × orçado, decisões, "para você olhar", bugs do kit achados.
- Resposta final curta: arquivos (caminho), duração, MB, custo real × orçado, o que depende da pessoa.

### Armadilhas do fluxo
- Corpo montado por concat `-c copy` de partes com metadados de cor diferentes (HeyGen sem tag + original `tv/bt709`) → o ffmpeg reconfigura o filtergraph no meio: overlays PNG somem e o buffer do `loudnorm` (~3 s) é descartado, abrindo salto de pts no áudio. Corrigido em 05/10/2026 com `-reinit_filter 0` no `montar_ad_rapido.py`; mesmo assim recodifique as partes com as mesmas tags de cor antes de juntar. O `silencedetect` não pega esse defeito.
- Dois agentes editando o mesmo script compartilhado ao mesmo tempo: arriscado. Etapa que altera ferramenta comum roda sozinha.
- Heredoc no Git Bash estraga barra invertida em script Python: criar o `.py` com a ferramenta de escrita.

### Checklist de saída
- [ ] Checklist de abertura respondida (oferta, mercado, verba diária, teto, música).
- [ ] Resolução certa (720 para origem baixa; 1080 só origem ≥720p/vencedor) e formato certo.
- [ ] `finalizar.py` rodou; `_frames.jpg` aberto.
- [ ] `revisar_ad.py` com RESULTADO OK + checklist do `revisar-criativo`.
- [ ] `.txt` do anúncio com botão igual ao CTA falado.
- [ ] Custo real ≤ informado; relatório e memória do projeto atualizados.

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [02-regras-gerais-e-seguranca.md](02-regras-gerais-e-seguranca.md)
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [05-traducao-de-criativos.md](05-traducao-de-criativos.md)
- [06-troca-de-marca.md](06-troca-de-marca.md)
- [07-variacoes-gancho-corpo.md](07-variacoes-gancho-corpo.md)
- [08-voz-e-dublagem.md](08-voz-e-dublagem.md)
- [09-lipsync-e-avatar-heygen.md](09-lipsync-e-avatar-heygen.md)
- [10-limpeza-cor-e-qualidade-de-video.md](10-limpeza-cor-e-qualidade-de-video.md)
- [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)
- [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md)
- [13-analise-meta-ads-e-vencedores.md](13-analise-meta-ads-e-vencedores.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)
- [projetos/](projetos/)
