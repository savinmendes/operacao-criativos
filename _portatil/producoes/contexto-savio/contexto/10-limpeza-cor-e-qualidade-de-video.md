# Limpeza, cor e qualidade de vídeo

> Como conseguir a melhor fonte, tirar legenda/marca queimada, aumentar resolução, cobrir texto e não perder cor nem quadros ao reprocessar. Abra antes de baixar originais ou de qualquer script que leia e regrave quadros.

## Contexto de uso

**Fonte na maior qualidade (regra de 07/10/2026).** Todo download (Biblioteca de Anúncios do Meta, TikTok, Drive, qualquer fonte) deve vir na maior qualidade disponível, **≥720p**. Fonte abaixo de 720p: avisar a pessoa antes de produzir.
- Motivo: o 1º download da Biblioteca do lote Oración veio em 360×640, porque o `<video src>` do player é a versão SD. A HD 720×1280 existia nos dados da página.
- Modelo pronto: `Downloads\ADLIB-104060992792639\buscar_hd.py` (Playwright + Chrome headless). Abre a página, captura nas respostas de rede (graphql/ads library) e no HTML os campos `video_hd_url`/`video_sd_url` por `ad_archive_id`, rola a página 25 vezes e grava um JSON.
- A mesma página sobe o mesmo vídeo em vários anúncios: deduplicar por md5.
- Posts do Facebook pelo Playwright pedem login depois de ~2 posts. Nesse caso, pedir o link da Biblioteca ou o arquivo.

**Upscale (Real-ESRGAN, local, GPU).**
- `upscale_video.py` processa em blocos de 30 s (extrai quadros → Real-ESRGAN → grava o bloco → apaga os PNGs) e junta no fim com o áudio original.
- Modelo padrão `realesr-animevideov3`. Binário em `kit-edicao-criativos\_ferramentas_extras\realesrgan\` (há também o `resrgan.zip`).
- Padrão: `--escala 2` para entregar 720×1280 (decisão de 03/10/2026). Escala 3 leva 360×640 a 1080×1920.
- Tempo: orçar ≈1,5× a duração do vídeo. No teste do AD 03, 32 s (2x) × 64 s (3x) para 30 s de vídeo.
- Com ffmpeg 9 usa-se `-fps_mode passthrough`, não `-vsync`.

**Remoção de legenda/marca queimada — três opções.**

| Opção | Custo | Qualidade | Onde |
|---|---|---|---|
| **LaMa na GPU local** | grátis | sem borrão; método padrão | venv `ADLIB-104060992792639\producao\_trabalho\_vg`, modelo pronto `_lote\lama_base.py` (`simple_lama_inpainting`) |
| `remover_legenda.py` do kit (OpenCV) | grátis | modos `inpaint` (texto claro com contorno), `blur` (mancha), `delogo` (logo fixo pequeno), `cortar` (perde quadro) | kit |


**Cor que escurece a cada passada (lote Oración, 08/10/2026).**
- Sintoma: ler quadros com cv2/ffmpeg e regravar perdia 2–3 níveis de luma por passada.
- Causa: o cv2 lê bt709 quando o arquivo tem etiqueta e bt601 quando não tem; os encoders gravavam bt601 com etiqueta bt709.
- Solução: leitura e gravação com a matriz **bt601/tv fixa** (`ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3\comum3.py`: `quadros()` + `ENC_VF` + `ENC_TAG`). Num trecho colado, ajustar a cor pelo anel de pele em volta da boca (`_lote\cor_trecho.py`).
- Os scripts do lote San Benito FR (13/10/2026) já usaram esse padrão (`compose.py`, `colar_boca.py`, `compor_v2.py`).

**Metadados de cor em concat.** Partes com tags de cor diferentes (HeyGen sem tag + original `tv/bt709`) emendadas por `-c copy` fazem o ffmpeg reconfigurar o filtergraph no meio. Resultado: overlays somem e abre um buraco de ~3 s no áudio (AD 06 do lote Wyze: 8,49 → 11,49 s). O `montar_ad_rapido.py` usa `-reinit_filter 0` desde 05/10/2026. O `montar_corpo_avatar.py` sai sempre em bt709/tv com emenda recodificada.

**Faixa sobre texto queimado.** Tem que ser quase opaca (**alpha ≥250**), senão o texto original aparece por baixo. O `preparar_corpo_traducao.py` usa alpha 252 na faixa de aviso.

**Correção em massa de recusa por resolução/bitrate.** `ferramentas\corrigir-videos-tiktok\` (site local na porta 8750). Resolve a **recusa**, não a qualidade: esticar não cria detalhe.

## Lógica de uso

### 1. Baixar
1. Biblioteca do Meta: `python buscar_hd.py "<URL da página da Biblioteca>" saida.json` → baixar os `hd` de cada `ad_archive_id`.
2. yt-dlp (TikTok/YouTube/outros): `yt-dlp -f "bv*+ba/b" <url>`.
3. Conferir com `ffprobe` (largura/altura ≥720 no lado curto vertical) e deduplicar por md5. Renomear para `originais/NN.mp4` + `indice-arquivos.csv`.
4. Abaixo de 720p: avisar antes de produzir. Se seguir, upscale 2x.

### 2. Upscale
```
python ferramentas/upscale_video.py entrada.mp4 saida.mp4 --escala 2 [--ate 316.6] [--modelo realesr-animevideov3] [--bloco 30]
```
Em lote: **uma fila única de GPU** com log de progresso; agentes não rodam upscale em paralelo, esperam o arquivo pronto.

### 3. Tirar legenda/texto queimado
- **LaMa (grátis, preferido para legenda colorida):** `_vg\Scripts\python lama_base.py config.json` com `{"video": "...mp4", "saida": "base_sem_legenda.mp4", "faixa": [y0, y1], "ctx": [c0, c1], "seta": {...}, "ate": N}`. O script usa máscara justa da legenda (glifo + contorno + sombra, dilatada ~9 px) e grava bt709/tv sem áudio.

- **Kit (OpenCV):** sempre testar a máscara antes:
  ```
  python ferramentas/remover_legenda.py in.mp4 out.mp4 --faixa 0,1250,1080,350 --preview mascara.png
  python ferramentas/remover_legenda.py in.mp4 out.mp4 --faixa 0,1250,1080,350 [--sens 200]
  python ferramentas/remover_legenda.py in.mp4 out.mp4 --faixa 120,600,480,200 --modo delogo
  ```
  Coordenadas no tamanho ORIGINAL. Se sobrar texto, baixar `--sens`.
- **Cobrir em vez de apagar:** faixa/caixa opaca no `preparar_corpo_traducao.py` (`faixas`, `caixas`, `titulos`, `aviso`) ou caixas por frase no `gerar_variacao.py`. Alpha ≥250.
- Ordem no fluxo de adaptação: limpar legenda no original → upscale → troca de produto → legenda nova do kit.

### 4. Ler e regravar quadros sem perder cor
- Ler: `ffmpeg -i in.mp4 -vf "scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24" -fps_mode passthrough -f rawvideo -`.
- Gravar: `-vf scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p` + etiqueta só no bitstream `-bsf:v h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1`.
- Copiar `comum3.py` para o lote em vez de reescrever. Conferir a média de luma original × final (o revisor do SB FR guardou `luma_*.json` por vídeo).

### 5. Emendar partes
Recodificar todas as partes com os mesmos `-colorspace/-color_primaries/-color_trc/-color_range` antes de juntar. Conferir o pts do áudio no final (ver [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)).

### Armadilhas
- `<video src>` da Biblioteca = 360p. Usar `video_hd_url`.
- Faixa com alpha baixo deixa a legenda antiga aparecer.
- Kling recusa vídeo <3 s; cortar com `-ss ini -t dur` + `tpad=stop_mode=clone` (nunca `-frames:v`).
- Upscale roda numa fila única de GPU (agentes não disparam upscale em paralelo). Whisper e OCR em paralelo disputam a CPU e ficam até 10x mais lentos: rodar em sequência.
- faster-whisper na GPU falhou no Yara (`cublas64_12.dll`): usar `device='cpu', compute_type='int8'`.
- Na receita em 720 com faixa no rodapé: `selo.y≈1110`, `cta.y≈1490`.

### Checklist de saída
- [ ] Fonte ≥720p (ou aviso dado) e sem duplicados.
- [ ] Nenhum resto de legenda/marca antiga (folha + zoom).
- [ ] Luma média do final igual à do original (sem escurecer).
- [ ] Emendas sem salto de pts e sem overlay sumindo.

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [02-regras-gerais-e-seguranca.md](02-regras-gerais-e-seguranca.md)
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [04-fluxo-producao-criativos.md](04-fluxo-producao-criativos.md)
- [05-traducao-de-criativos.md](05-traducao-de-criativos.md)
- [06-troca-de-marca.md](06-troca-de-marca.md)
- [09-lipsync-e-avatar-heygen.md](09-lipsync-e-avatar-heygen.md)
- [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)
- [projetos/](projetos/)

> Vmake deixou de ser usado em 14/10/2026 (skill e ferramenta removidas). Legenda queimada: LaMa local.
