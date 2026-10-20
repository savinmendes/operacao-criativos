# Variações gancho × corpo, estáticos e carrossel

> Como multiplicar criativos a partir de vídeos já prontos (gancho novo sobre corpo existente, corpo novo montado de tomadas, matriz gancho × corpo) e tirar estáticos/carrossel de quadros reais. Abra quando o pedido for volume, matriz ou teste de ganchos.

## Contexto de uso

**O que é.** O script `gerar_variacao.py` do kit monta variações a partir de vídeos prontos. Ele cria um **banco de tomadas** de cada vídeo-fonte (detecção de cena `scdet` + grupos de cena contínua + transcrição por palavra), separa a música sem voz (demucs) para a emenda e monta cada combinação descrita num JSON. Antes de entrar no kit, o mesmo papel era cumprido por `_variacoes/gerar_variacao.py` (Podadora) e por `variacoes/gerar_var.py` + `prep_fonte.py` (Drenagem).

**Dois modos.**
- **Modo A** — gancho novo (fala + cenas do banco + caixas de texto por frase) + AD pronto a partir de um `corte`. Grava o arquivo final já finalizado.
- **Modo B** — corpo novo montado do banco sobre uma narração (ex.: matriz de originais traduzidos). Grava `corpo.mp4`, `alinhamento.json` e `receita_final.json` em `trab/<config>/`. Com `--montar-ad`, já roda o `montar_ad.py`.
- Nos dois modos, `info.json` guarda as tomadas sorteadas e a semente (para reproduzir).

**Lotes em que foi usado.**

| Lote | O que saiu | Onde |
|---|---|---|
| Podadora COD Chile | AD 05–12: 4 ganchos (JARDINERO, PERRO, AUMENTO, DEVOLVER) × corpos (A FUNCIONES, B CUCHILLA, C KIT); banco `_variacoes/banco.json`, mesa espelhada da v2 excluída. Estáticos: feed 4:5 01–07 + carrossel 1:1 1–4 via `_variacoes/est/gerar_estaticos.py` | `Downloads\PODADORA-CL\` |
| Drenagem LATAM (05/10/2026) | VAR 01–30: 10 ganchos × corpos AD20/AD05/AD30 | `Downloads\DRENAGEM-LATAM\producao\VARIACOES\` |
| Yara BF Chile (09/10/2026) | 15 versões (5 ganchos × 3 músicas) a custo zero, em `entregas/volume` | `Downloads\YARA-CL\` |

**Sinais de resultado já registrados.**
- Validados no TikTok pela pessoa (08/10/2026), com cópias em `Downloads\APROVADOS E VALIDADOS TIKTOK\`:
  - VAR 06 G6-DISCULPA×AD20;
  - VAR 21 G1-ESPOSO-AMIGA×AD30;
  - VAR 28 G8-POR-QUE-NOS-HINCHAMOS×AD30;
  - VAR 29 G9-PAGAS-AL-RECIBIR×AD30;
  - também AD 30 CURTO EXESPOSO-FILA.
- Leitura: o corpo AD 30 (exesposo na fila) e os ganchos de confissão, mecanismo e COD performam. Priorizar em novas variações.
- Regra da pessoa: lotes e subidas começam pelo **top 5 do ranking de vendas**, nunca por variedade de foto.
- Volume tem de caber na verba: no Yara saíram 25 vídeos para US$100/dia, que comporta ~7. Perguntar a verba diária antes de dimensionar.
- Quase-duplicata não conta como variação: o H1 do Yara saiu quase igual ao AD-C. A variação tem que mudar o gancho de verdade.

## Lógica de uso

### 1. Preparar as fontes
```
python ferramentas/gerar_variacao.py banco "AD 20 - X.mp4" --saida fontes/20/banco.json [--ate 90] [--idioma es] [--sem-whisper] [--folha]
python ferramentas/gerar_variacao.py fundo "AD 20 - X.mp4" --ate 10.933 --saida fontes/20/bed.wav
```
- `banco`: `--limiar 10` (threshold do scdet) e `--sim 0.70` (similaridade de histograma abaixo da qual começa outro grupo). `--modelo small` é o modelo do whisper; `--folha` gera folha de contato 1 q/s.
- `fundo`: música sem voz do trecho até o `corte`, para o gancho emendar no corpo sem pulo.
- Para modo B: rodar demucs em cada original e apontar `fundos` para os `no_vocals.wav`.

### 2. Escrever o config (modelo: `kit-edicao-criativos\exemplos\variacao_exemplo.json`)
Caminhos relativos ao JSON.
- Topo: `saida`, `resolucao` (`"720"`/`"1080"`), `limite_mb`, `semente`, `bancos` (nome → banco.json) e, no modo B, `fundos`.
- `gancho`:
  - `fala` (mp3 + `.alinhamento.json` do `tts_elevenlabs.py`). Se não existir e houver `texto` + `voz`, gera por TTS (pago).
  - `lead`/`cauda`: silêncio antes e depois da fala (ex.: 0,12/0,30).
  - `pool`: tomadas candidatas `[banco, de, até]`, com a 1ª janela preferida. **Ou** `trecho`: trecho fixo de uma fonte.
  - `tomada`: duração sorteada, ex. `[1.5, 2.5]`.
  - `caixas`: caixa branca por frase, que cobre a legenda queimada, ex. `{"cy":866,"min_w":540,"min_h":100,"px":46}`. **Ou** `caixa_fixa`: `{"linhas":[…],"px":29,"cy":235,"de":0,"ate":3}`.
  - `fundo`/`fundo_vol`: wav (modo A), `{"fonte":"1"}` (mesmo trecho da fonte) ou null.
- `corpo`:
  - modo A: `{"video":"ads/AD 20 - ….mp4","corte":10.933,"ganho_db":null}`;
  - modo B: `{"narracao":…, "pool":[…], "tomada":[3.0,4.3], "fundo":["3",3.3], "fundo_vol":1.6, "abertura":[["1",44,50]], "fechamento":[["3",40,44]], "excluir":[["2",12.6,19.7]], "cauda":0.8}`.
- `faixa`: aviso opaco no rodapé (opcional), ex. "Solo con fines demostrativos. Algunas escenas están aceleradas.", `topo` 1150.
- `receita` (modo B): `estilo`, `legenda.chaves`, `selo` (em 720 com faixa: `y` 1110), `cta` (`palavra`, `y` 1490).

### 3. Montar
```
python ferramentas/gerar_variacao.py montar var01.json [--semente 7] [--montar-ad]
```
Nome de saída no padrão do lote, ex. `VARIACOES/VAR 01 - G1-ESPOSA-AMIGO x AD20.mp4`.

### 4. Regras da matriz
- Margem nas bordas de cada tomada: o corte detectado pelo `scdet` não é exato.
- Grupos de cena contínua contam como **uma** tomada: não repetir pedaços da mesma cena.
- Nenhum take repete no vídeo; nunca dois seguidos da mesma fonte.
- Voz do gancho = voz do corpo (clone do narrador quando a marca é própria).
- Ganchos adaptados ao gênero de quem fala no corpo.
- Emendas em fim de frase; ouvir cada emenda.
- Trocar uma variável por vez quando o objetivo é teste (mesmo corpo, gancho diferente).
- Antes de subir, auditar a diversidade do lote com a skill `andromeda` (`.claude/skills/andromeda/scripts/aberturas.py` compara as aberturas).

### 5. Estáticos e carrossel
- Saem de **quadros reais** dos vídeos (produto fiel), não de imagem inventada. Modelo: `_variacoes/est/gerar_estaticos.py` da Podadora (ainda na pasta do lote, não no kit) — feed 4:5 + carrossel 1:1.
- Imagens novas por IA: image-to-image sempre a partir da foto ORIGINAL do produto (sem foto, parar e pedir); 1 aprovada antes do lote. Tradução de arte: edição de imagem com a lista exata de textos (ver [05-traducao-de-criativos.md](05-traducao-de-criativos.md)).
- Lição Pellorini (11/10/2026): o Gemini (Nano Banana) reescreve texto pequeno (mostrador, numerais, marca de fábrica) mesmo pedindo para não mexer → colar a região original de volta (`_orig_L3/fixdial.py`), sem regerar.

### Armadilhas
- Quase-duplicata tende a ser agrupada pelo Meta como o mesmo anúncio (critério da skill `andromeda`); volume ≠ diversidade.
- Música trend é liberada pela pessoa (instrumental via demucs + ducking, sem repetir alerta); citar no relatório quais foram usadas.
- `gerar_variacao.py` com `texto`+`voz` e sem `fala` gera TTS pago: avisar o custo antes.

### Checklist de saída
- [ ] Cada variação muda de fato o gancho (ou o corpo) em relação às outras.
- [ ] Sem take repetido, sem pulo de música na emenda, sem legenda queimada visível no gancho.
- [ ] `revisar_ad.py` em todas; `info.json` guardado para reproduzir.
- [ ] Nomes `VAR NN - <GANCHO> x <CORPO>` e textos de anúncio variando abertura e título por gancho.

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [02-regras-gerais-e-seguranca.md](02-regras-gerais-e-seguranca.md)
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [04-fluxo-producao-criativos.md](04-fluxo-producao-criativos.md)
- [05-traducao-de-criativos.md](05-traducao-de-criativos.md)
- [06-troca-de-marca.md](06-troca-de-marca.md)
- [08-voz-e-dublagem.md](08-voz-e-dublagem.md)
- [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)
- [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md)
- [13-analise-meta-ads-e-vencedores.md](13-analise-meta-ads-e-vencedores.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)
- [projetos/](projetos/)
