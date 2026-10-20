# Lote SB EN 2: AVATAR_REST + ADS 24 → inglês (aprovado com "confirmo" em 18/10/2026)
- **Mercado:** EUA, Reino Unido, Canadá, Austrália e depois worldwide. Inglês americano natural e neutro, tom espiritual.
- **Nome do santo:** "San Benito" vira **"Saint Benedict"**.
- **Destino:** a ORAÇÃO AO VIVO (live prayer).
- **CTA final:** **"Tap Learn More below and join the live prayer now."** O botão do Meta é LEARN_MORE. Pode manter a frase de urgência do original.
- **Proibido no vídeo:** produto e preço.
- **Compliance:** mantenha o mesmo teor do original (promessas e urgência), sem suavizar. A decisão é da pessoa.
- **Referências de vocabulário:** `C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\*\*_roteiro-en.txt` (lote EN 1) e `BRIEFING_LOTE_EN.md`, na mesma pasta.

## REGRAS DA PESSOA (obrigatórias)
- Não altere nem substitua NADA que já existe (bases, pastas EN/FR/IT/PL, PARA-SUBIR, scripts de outros lotes). Copie o que precisar para o seu `_trabalho`.
- Não estenda mudanças a outros vídeos ou idiomas.

## Método
1. **Roteiro EN:** transcreva o original com faster-whisper es e escreva o roteiro em inglês. Tradução natural, com duração parecida. O texto que aparece na tela (títulos e cartões) também vai para inglês, no mesmo estilo.
2. **Voz (ElevenLabs):**
   - A chave está em `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env`. Não imprima.
   - Modelo eleven_multilingual_v2.
   - A conta está no LIMITE de vozes: não crie, não clone e não apague nenhuma. Use só vozes que já existem na conta.
   - **Uma voz por personagem.** Registre a escolha.
   - Confira no whisper en se a pronúncia está natural.
3. **Rosto falando:**
   - Lipsync no HeyGen em mode **speed**. O vídeo de entrada leva o áudio ORIGINAL e o áudio EN vai separado. Trechos de até ~12 s.
   - OU gere a pessoa do zero no HeyGen a partir de um quadro (create_video_from_image, Avatar IV, **720p**), quando o briefing do vídeo pedir.
   - Corte nas fronteiras das palavras e cubra as pausas com b-roll ou jump cut. NÃO retoque a boca.
   - Aceite: `checar_lipsync.py` com índice de pausa ≤ 0,6.
   - Job parado há mais de 45 min: reenvie igual. Não reenvie antes disso.
   - Cor bt601 fixa e `-reinit_filter 0`.
4. **Legenda queimada ES:** remova com LaMa local.
   - Venv: `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Scripts\python.exe`
   - Script: `...\_trabalho\_lote\lama_base.py`
   - Confira com zoom que não sobrou nada.
5. **Legenda EN:** palavra a palavra, no estilo do original. Setas no CTA na mesma cor do original. Música do original sem a voz (demucs) a ~-32 LUFS.
6. **ÁUDIO SEM CHIADO (obrigatório):**
   - Aplique a receita `C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\RECEITA_LIMPAR_CHIADO.md`. O código está em `...\SB-FR-NOVOS-VENCEDORES\_chiado\chiado.py`: `limpar_voz`, `limpar_trilha`, `dip_pausas`, `finalizar_mix`.
   - Meça o ruído na faixa de 7–14 kHz nas pausas.
   - Volume final ~-16 LUFS. Iguale o volume das vozes entre personagens.
7. **Resolução:** a mesma da fonte.

## QA
1. Rode `revisar_ad.py` do kit a partir de `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\`, com PYTHONIOENCODING=utf-8 e whisper en.
   - Lista de proibidos em .txt UTF-8: "San Benito", "oración", "Toca", "más información", "saber más", "misa", "$", "€".
2. Confira:
   - folha de contato;
   - boca nas pausas;
   - quadro solto;
   - silêncio no fim;
   - salto de pts;
   - sincronia áudio×vídeo depois de cada corte.
3. Chame 1 revisor independente e ESPERE o resultado. Corrija o que ele achar. Nenhum revisor mata processos.
4. NÃO abra os vídeos.

## Saída
- **Pasta:** `C:\Users\PICHAU\Downloads\SB-EN-NOVOS-VENCEDORES\<NN>_<NOME>\`
- **Arquivos:**
  - `SB-EN-<NOME>.mp4`
  - `SB-EN-<NOME>_roteiro-en.txt` (ES × EN e decisões)
  - `SB-EN-<NOME>_texto-anuncio.txt`: Headline ≤40 / Primary text / Short version ≤125 / Button: LEARN_MORE. Notas internas só depois de uma linha "Notes:".
  - `SB-EN-<NOME>_frames.jpg`
  - `PRONTO.txt`
- **Trabalho:** só em `_trabalho\`. Apague os intermediários pesados no fim.
- **Painel:** `python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa sben2-<nome> "<título>" --texto "..."`
- **Custos:**
  - ElevenLabs: centavos.
  - HeyGen: créditos do plano.
  - Meça o saldo HeyGen (get_current_user) antes e depois e registre.
- **Relatório curto:** arquivo, duração, vozes, jobs HeyGen, créditos e imperfeições com tempos.
