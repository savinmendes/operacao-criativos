# Briefing: vídeos em inglês (EUA) → Reino Unido (08/10/2026)

A pessoa aprovou a **opção A**: voz clonada da creator + lipsync HeyGen só no trecho trocado.
- **Não pergunte nada.** Na dúvida, escolha o lado seguro e registre.
- **Nunca leia nem imprima arquivos `.env`.**
- **Não abra os vídeos** em players.

## Contexto
- **A marca (Physician's Choice, enzimas digestivas) e as creators são da pessoa.** Clonar a voz e fazer lipsync é **permitido**.
- **Mercado novo:** Reino Unido.
- **Decisões da pessoa:**
  - **manter todas as alegações** de saúde como estão ("six months pregnant", inchaço, barriga antes/depois);
  - preço em **libras**;
  - tirar só as referências a **EUA**, a **TikTok/TikTok Shop** (carrinho laranja, "on here", "on TikTok") e a **dólar**.
- **Trocas aprovadas:**
  - "the food in America" → "the food we eat";
  - "American food system/diet" → "our modern food system/diet";
  - "on TikTok right now / on here, cheaper than the grocery store" → "on offer right now, cheaper than in the shops";
  - "the orange part(s)" → "they're still in stock";
  - "under $20" → "under twenty pounds". **Preço a confirmar pela pessoa:** registre no relatório.

  Mantenha o restante da fala original intacto. "Link below", "sale" e "offer" ficam.
- **Inglês britânico** na legenda nova, se houver: "colour", "flavour", "favourite", £.

## Método (leia antes)
- `C:\Users\PICHAU\Downloads\Produtividade com ia\CLAUDE.md`: armadilhas, sobretudo "Lipsync HeyGen", "Cor escurecendo", "PowerShell × Git Bash" e "Remover legenda queimada".
- `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\LICOES-LIPSYNC.md` e os scripts de `ad01\lipsync2\`, que servem de modelo:
  - `preparar.py`;
  - upload (`put.sh`);
  - `baixar.sh`;
  - `colar.py` / `medir_out.py`;
  - `fechar.py`;
  - `ad13\lipsync3\comum3.py`, para a cor exata.
- Kit: `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\`, com `clonar_voz.py`, `tts_elevenlabs.py`, `checar_lipsync.py` e `revisar_ad.py`. Use `PYTHONIOENCODING=utf-8` e `-threads 4`. A GPU está sem CUDA, então rode na CPU. Whisper e OCR em sequência.

## Passos por vídeo
1. **Mapear:**
   - transcrição palavra a palavra (faster-whisper small/medium, en);
   - para cada frase a trocar: tempo exato, se o rosto de quem fala aparece com a boca visível, e quem fala (o EN 01/07 tem 2 pessoas);
   - folha de quadros do trecho.
2. **Voz:**
   - demucs `--two-stems=vocals` no vídeo, para ter fundo e voz separados;
   - clonar a voz de cada creator com `clonar_voz.py` a partir da voz isolada, com o máximo de fala limpa disponível. Nome: "ENZIMAS UK <video> <pessoa>".
3. **Fala nova:** `tts_elevenlabs.py` com a frase de troca, no mesmo ritmo e energia. Ela tem que caber no tempo da frase original (±0,3 s); se não couber, ajuste o texto, mantendo o sentido.
   - **Emendas:** em pausa natural.
   - **Áudio do trecho:** fundo do demucs + voz nova.
   - **Fora do trecho:** áudio original intocado.
   - **Volume:** a voz nova no mesmo nível da original (compare em LUFS).
4. **Rosto:**
   - **Se a boca aparece no trecho:** HeyGen `create_lipsync`.
     - `mode speed`, entrada recortada só no rosto de quem fala, com o **áudio original** do trecho, e a frase nova como `audio`;
     - trechos de até 12 s;
     - colar de volta com elipse na boca e no queixo, com leitura e gravação de cor exatas (`comum3.py`);
     - aceite: `checar_lipsync.py` com índice de pausa ≤ 0,6;
     - plano B sem custo: `fechar.py`.
   - **Se a boca não aparece:** só a troca de áudio.
5. **Tela:** se aparecer qualquer elemento de TikTok (carrinho, botão, @, marca d'água), $ ou EUA, cubra (alpha ≥ 250) ou recorte. Se o trecho tiver legenda queimada com a frase antiga, troque pela nova no mesmo estilo; para apagar, use LaMa local (venv `ADLIB…\_trabalho\_vg`, `_lote\lama_base.py`).
6. **Revisão:**
   - `revisar_ad.py --lipsync` **pelo PowerShell**, com os termos proibidos num `.txt` em UTF-8: America, American, TikTok, dollar, "$", "orange", "grocery store", "on here";
   - whisper en no final: a fala bate com o roteiro novo, sem sobra da frase antiga;
   - folha 1 em 1 quadro nas emendas: nenhum pulo de imagem, cor igual, boca natural;
   - mesma resolução, fps e duração (±0,5 s) do original.

## Saída
- **Vídeos:** `C:\Users\PICHAU\Downloads\ENZIMAS DIGESTIVAS - CRIATIVOS\UK\<mesmo nome> - UK.mp4`.
- **Trabalho:** `_trabalho\uk\<EN NN>\`.
- **Relatório por vídeo** (`RELATORIO.md`):
  - frases trocadas, com tempo;
  - id da voz;
  - caracteres de TTS;
  - créditos HeyGen (saldo com `get_current_user` antes e ~1 h depois);
  - índice de lipsync;
  - resultado da revisão;
  - pendências.
