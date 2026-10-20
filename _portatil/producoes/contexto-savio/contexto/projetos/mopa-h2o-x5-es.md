# Mopa H2O X5: EN → ES LATAM

> Tradução de 15 vídeos e 12 imagens da mopa a vapor H2O X5 (loja da pessoa) para espanhol neutro LATAM. Abra ao continuar esse produto, ao traduzir os outros produtos do mesmo zip ou ao traduzir imagens com texto.

## Contexto de uso
- **Frente:** COD LATAM (selo "Pago contra entrega"). **Produto:** H2O X5 (mopa verde), da própria pessoa; ficha oficial h2oforyou.co.uk/products/h2o-x5-steam-cleaner-tvpr (1300W, 5 en 1, aquece em < 30 s, < 2,3 kg, 99 % de bactérias em 15 s, 30 dias de devolução, 2 anos de garantia, 14 milhões vendidos).
- **Pasta:** `Downloads\MOPA VERDE - H2O X5\`. Originais em `VIDEOS\`, `IMAGENS\`, `TEXTOS\` (separados do zip `criativos-2026-10-08.zip`); entrega em `ES-LATAM\` (`VIDEOS\`, `IMAGENS\`, `00-RELATORIO.md`, `00-TEXTOS-ANUNCIOS-H2O-X5-ES.txt`); trabalho e briefing em `_trabalho\` (`ESTUDO-MOPA.md`, `BRIEFING-VIDEOS.md`).
- **Entregue em 08/10/2026:**
  - 15 vídeos no formato do original: narrados com voz clonada (07, 60, 16, 32, 24, 25, 31, 46), só música (08, 10, 15, 17, 21, 54), sem som (44);
  - 12 imagens + `00-folha.jpg`;
  - textos com título, texto principal, descrição e versão TikTok (a linha "nota" é interna).
- **Decisões da pessoa:** marca mantida; vozes das narradoras clonadas; **manter todas as alegações** ($55, 14 millones, 99 %, "lab certified", "seguro con niños y mascotas"); tirar só "USE CODE FBX5"; tirar envio de UK/EUA/Canadá e parcelamento; LATAM geral com "tú"; CTA "Haz clic en Más información".
- **Custo real:** ~US$ 1,70 (orçado US$ 4–5): imagens Nano Banana 2 no Flora US$ 1,40 (13 gerações; projeto "MOPA H2O X5 - imagens ES (2026-10-08)") + TTS ~US$ 0,27.
- **O mesmo zip tem** H2O HD (amarela/preta), grama GrowTrax e IronLess — **não traduzidos**.
- **Pendências / revisão manual:** pronúncia de "H2O X5" (46/31, 32/16); fala do 60 até 0,6 s atrás da do 07; selo sem padrão de tamanho/posição (cobre produto em 17, 21, 31, 46, 54); "vendidas" × "vendidos" (correto: vendidos); imagem 45 diz "1 año de garantía" (ficha diz 2); "$55" dólar ou moeda local; link COD por país em branco; compliance mantido por decisão ("te están enfermando", "certificado en laboratorio", "seguro con niños y mascotas"); mopa vermelha em 17–19 s no 08.

## Lógica de uso
- **Vídeos:** fluxo de tradução do kit (transcrição + OCR → roteiro ES → voz clonada → demucs para a música → cobrir texto queimado → montar → revisar), 1 agente por vídeo + revisor independente (que corrigiu 08, 21 e 54).
- **Formatos 4:5 e 1:1:** na época `montar_ad.py`/`revisar_ad.py` só aceitavam 9:16, e os agentes usaram um compositor próprio (`_trabalho\videos\_C\compor.py`). Hoje o kit aceita `formato` "4:5" e "1:1" na receita e `revisar_ad.py --formato`.
- **Imagens:** Flora, Nano Banana 2 i2i em 2K, um prompt por imagem listando cada texto (antigo → novo); redimensionar para o tamanho da fonte (LANCZOS); QA em tamanho cheio com zoom + OCR (RapidOCR). Fallback local com PIL se o modelo errar texto.
- **Regra de compliance:** suavizar promessa é decisão da pessoa — listar os riscos e perguntar manter × suavizar.
- **Se a pessoa pedir mais:** padronizar selo, corrigir "vendidos" e alinhar o 60 (sem custo); traduzir H2O HD, GrowTrax e IronLess do mesmo zip com o mesmo método.

## Relacionados
- [../05-traducao-de-criativos.md](../05-traducao-de-criativos.md)
- [../04-fluxo-producao-criativos.md](../04-fluxo-producao-criativos.md)
- [podadora-chile.md](podadora-chile.md), [wyze-solar-cam-latam.md](wyze-solar-cam-latam.md)
