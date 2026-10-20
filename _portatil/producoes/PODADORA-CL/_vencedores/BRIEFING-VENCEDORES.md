# Briefing — variações dos 2 vencedores da Podadora (08/10/2026)

A pessoa aprovou. **Não pergunte nada.** **Nunca leia nem imprima arquivos .env.** Não use crédito HeyGen: sem lipsync, só ganchos com cenas **sem rosto falando**. ElevenLabs só para a voz dos ganchos.

## Contexto
- **Os dois vídeos são da pessoa.** Clonar a voz do narrador de cada um é permitido.
- **Produto:** Podadora/Desbrozadora inalámbrica 3 en 1 com rodas (marca impressa SEESE), COD Chile.
- **Referência do produto:** `PODADORA-CL\_vencedores\produto_kit.webp`. Mostra o kit com 2 discos de serra metálicos, 2 lâminas de 2 pontas, protetor, 2 rodas, **2 baterias de 21V**, carregador, chave, discos de fixação e fios.
  - **Não invente** nada que não esteja na foto ou no próprio vídeo.
  - Se o gancho citar o kit, use só o que aparece aí.
  - Se precisar de uma cena de kit, use a própria foto (zoom lento, 9:16, fundo ampliado/desfocado) em vez de gerar imagem nova.
- **Kit de edição:** `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\` (leia o `CLAUDE.md`). Siga a skill `editar-criativo` e use `gerar_variacao.py` (banco/fundo/montar), `montar_ad.py` e `revisar_ad.py`.
- **Regra fixa: o corpo e o CTA do vencedor ficam exatamente como estão.** Só o gancho é trocado. Corte no fim do gancho original, em fim de frase pela transcrição, e cole o gancho novo + o corpo original até o fim.
- **Gancho:** 3–6 s de narração. O visual vem das cenas do próprio vencedor (e da foto do kit, se servir), sem rosto falando, com texto grande na tela (caixa no estilo do kit) e a música e o fundo do original (demucs `no_vocals`) para emendar sem pulo.

## Entregas (por vencedor)
1. **Versão 1080p do vencedor original, sem mudar nada:** upscale com `upscale_video.py` (Real-ESRGAN, GPU local). Saída: `PODADORA-CL\VENCEDORES\<X>0 - <NOME>-1080.mp4`.
2. **6 variações de gancho**, em 720x1280 (a mesma resolução do corpo original; não suba a resolução do corpo nas variações).
3. **Revisão de cada uma:**
   - `revisar_ad.py`, rodado pelo PowerShell, com os termos proibidos num **.txt em UTF-8**: preço, "gratis" fora do selo, garantia não confirmada, TikTok, "link";
   - folha de 1 em 1 quadro na emenda gancho→corpo;
   - nenhuma frase cortada, nenhum quadro solto, nenhum rosto falando no gancho.
4. **Relatório** em `PODADORA-CL\VENCEDORES\RELATORIO-<X>.md`: a lista das variações com o gancho, as cenas usadas, a duração, o custo de TTS e o resultado da revisão.

**Não abra os vídeos.**
