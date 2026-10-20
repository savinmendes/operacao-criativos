---
name: editar-criativo
description: Edita/monta criativos de vídeo 9:16 do Savin (legenda corrida, hook, tela dividida sem borda, setas de CTA, remover legenda, trocar/narrar áudio, trilha, selo COD, faixa San Benito) usando as ferramentas Python do kit. Use para qualquer pedido de edição de criativo/AD.
---

# Editar criativo

1. Leia as regras em `CLAUDE.md` (público sênior, CTA com setas, takes sem repetir, nomes AD NN).
2. Descubra o próximo número: liste `ads/` da pasta do produto e continue do maior AD (produto novo = AD 01).
3. Prefira **uma receita JSON** + `python ferramentas/montar_ad.py receita.json` (modelo em `exemplos/ad_exemplo.json`).
   Para tarefas isoladas use os scripts direto (tabela no CLAUDE.md). Todos têm `--help`.
4. Escolhas padrão:
   - Legenda: `alinhamento:` se a narração veio do `tts_elevenlabs.py`; senão `transcrever` (faster-whisper, idioma do mercado).
     Corrija palavras erradas da transcrição passando `texto:frases.txt` com o roteiro real.
   - Estilo `drop` para produto; `sb` para San Benito (Anton 116 y=1480 + faixa de topo).
   - Manchete no topo só durante o hook (`ate` = fim do hook). Manchete no meio da tela → legenda com `desde` depois dela.
   - CTA: `{"palavra": "toca"}` (ou "pide", "compra"...). Confira no _frames.jpg que as setas aparecem.
   - Hook novo sobre corpo existente: `hook.tipo = imagem` (som do corpo continua). Avatar com fala própria: `tipo = antes`.
   - Tela dividida: `video.py dividida` (sem borda; o áudio vem de cima por padrão). Rosto sempre na metade de cima, inteiro.
   - Remover legenda: rode `--preview` primeiro, ajuste `--faixa`/`--sens`, depois processe. Texto que não sai → `--modo blur` ou `cortar`.
5. Em lote: faça 1, mostre o `_frames.jpg` e o caminho, espere aprovação; depois rode o resto (pode ser em paralelo em background).
6. Entregue junto o `.txt` com título + texto principal por AD (regras de compliance no CLAUDE.md).
7. Resposta final curta: arquivos (caminho), duração, MB, e o que depende do Savin.
