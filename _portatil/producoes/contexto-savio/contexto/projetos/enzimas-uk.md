# Enzimas digestivas UK: localização EN-EUA → EN-UK

> Localização de criativos em inglês americano de enzimas digestivas (Physician's Choice) para o Reino Unido, trocando só as frases que não servem, com voz clonada da creator e lipsync HeyGen só no trecho trocado. Abra ao localizar criativo para outro país do mesmo idioma.

## Contexto de uso
- **Data:** 08/10/2026. **Mercado:** Reino Unido. **Frente:** e-com (não confirmada nas fontes; **precisa de revisão manual**).
- **Marca e creators:** segundo o briefing, são da pessoa. Clonar voz e fazer lipsync é permitido.
- **Pasta:** `Downloads\ENZIMAS DIGESTIVAS - CRIATIVOS\`.
  - `INGLES\` (EN 01–11, originais EUA);
  - `ESPANHOL\` (ES 01–12, uso não registrado);
  - `00-indice.csv` (arquivo, origem e início da fala de cada vídeo);
  - `UK\` (os 5 vídeos alterados);
  - `PRONTOS UK - INGLES\` (os 11 prontos para subir + `00 - AD COPY UK.txt`);
  - `_trabalho\BRIEFING-UK.md` e `_trabalho\uk\EN NN\RELATORIO.md`.
- **Decisões da pessoa (opção A):**
  - manter todos os claims de saúde ("six months pregnant", inchaço, barriga antes/depois);
  - preço em libras;
  - tirar só as referências a EUA, a TikTok/TikTok Shop e a dólar.
- **Trocas aprovadas:**
  - "the food in America" → "the food we eat";
  - "American food system/diet" → "our modern food system/diet";
  - "on TikTok right now / on here, cheaper than the grocery store" → "on offer right now, cheaper than in the shops";
  - "the orange part(s)" → "they're still in stock";
  - "under $20" → "under twenty pounds".
- **Alterados:** EN 01, 02, 04, 07, 08 (os outros 6 não tinham o que trocar e foram para `PRONTOS` como estão).
- **Texto do anúncio:** botão Shop Now, um headline + texto por vídeo, em inglês britânico e sem preço.
- **Voz:** clones registrados em `kit-edicao-criativos\VOZES-CLONADAS.md` (linhas "Enzimas UK").
- **HeyGen:** saldo de 8.797 antes e logo depois (a cobrança atrasa; outros agentes usavam a conta ao mesmo tempo). Estimativa ~1 crédito/s em speed. Ver [../09-lipsync-e-avatar-heygen.md](../09-lipsync-e-avatar-heygen.md).
- **Pendências registradas nos relatórios:**
  1. preço "under twenty pounds" (EN 04) a confirmar;
  2. reconferir o saldo HeyGen ~1 h depois;
  3. EN 02: o adesivo "Reply to …'s comment" e o print de avaliações com layout de TikTok Shop foram mantidos (a pessoa decide se cobre);
  4. EN 04: "triple dipper" (prato da rede americana Chili's) ficou;
  5. EN 08: erro de digitação "EMZYMES" no gancho original não foi corrigido;
  6. EN 01/02/07: índice de pausa não calculável (fala contínua), aprovação visual.
- **Risco de compliance anotado:** no UK a ASA só aceita claims de saúde autorizados para suplemento. Se o anúncio for reprovado, trocar por "supports digestion / mealtime comfort".

## Lógica de uso
1. **Mapear:** transcrição por palavra (faster-whisper en) → lista das frases a trocar, com tempo, quem fala e se a boca aparece.
2. **Voz:** `demucs --two-stems=vocals` → clonar a voz de cada creator pela voz isolada (`clonar_voz.py`) → TTS da frase nova, cabendo no tempo da original (±0,3 s). Emenda em pausa natural. Fora do trecho, o áudio original fica intocado. Volume igual ao original (LUFS).
3. **Boca:**
   - se aparece: HeyGen `create_lipsync` em `mode speed`, entrada recortada no rosto com o **áudio original**, trechos ≤ 12 s, colagem com elipse boca/queixo e cor bt601 fixa (`comum3.py`), aceite `checar_lipsync.py` (pausa ≤ 0,6);
   - se não aparece: só o áudio;
   - boca coberta (oclusão): o HeyGen falha (3 jobs falharam no EN 04); aceite só o áudio ou use outra ferramenta.
4. **Tela:** cubra (alpha ≥ 250) ou recorte UI de TikTok, "$" e EUA; legenda queimada com a frase antiga → trocar no mesmo estilo (LaMa para apagar).
5. **Revisão:** `revisar_ad.py --lipsync` **pelo PowerShell**, com proibidos em `.txt` UTF-8 (America, American, TikTok, dollar, "$", orange, "grocery store", "on here"); whisper en no final; folha quadro a quadro nas emendas; mesma resolução, fps e duração (±0,5 s).
6. **Copy:** grafia britânica (colour, flavour, £), sem preço não confirmado e só com fatos da página do produto.

## Relacionados
- [../05-traducao-de-criativos.md](../05-traducao-de-criativos.md) (§5 mesmo idioma, outro país)
- [../09-lipsync-e-avatar-heygen.md](../09-lipsync-e-avatar-heygen.md)
- [../20-internacionalizacao-e-gateways.md](../20-internacionalizacao-e-gateways.md)
