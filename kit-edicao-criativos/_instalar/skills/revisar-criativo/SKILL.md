---
name: revisar-criativo
description: Checklist de revisão antes de entregar um criativo do Savin (decodificação, duração, tamanho, frames, legenda, CTA, takes, nomes, texto do anúncio). Use antes de dizer que um vídeo está pronto.
---

# Revisar criativo

1. `python ferramentas/finalizar.py "<arquivo>.mp4" --so-revisar --frames 1,<meio>,<cta+0.5>,-1`
   e ABRA o `_frames.jpg` (Read na imagem). RESULTADO tem que ser OK.
2. Checklist (tudo sim):
   - [ ] Nome `AD NN - ...` na sequência certa do produto.
   - [ ] 1080×1920, ≤30 MB, decodifica sem erro, duração conferida.
   - [ ] Legenda grande e legível, nada cobrindo rosto; sem legenda junto de manchete no meio da tela.
   - [ ] Setas vermelhas aparecem na palavra do CTA e apontam para baixo; nenhum "botão falso" desenhado.
   - [ ] Corpo começa na frase certa; nenhum resto do hook antigo; nenhum texto em outro idioma (ex.: português) sobrando.
   - [ ] Nenhum take repetido; takes 4–5 s; produto idêntico ao original em todos os takes.
   - [ ] Áudio: voz clara (−15 LUFS), trilha baixa, sem estalo nos cortes.
   - [ ] Texto do anúncio (.txt) com título + principal, compliance ok, botão do Meta igual ao do vídeo.
   - [ ] Custo gasto ≤ custo informado.
3. Se algo falhar, corrija antes de entregar e diga o que foi corrigido em 1 linha.
