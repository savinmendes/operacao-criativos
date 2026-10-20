# Lote SB FR 2: vencedores ES/US → francês (aprovado com "confirmo" em 17/10/2026)
- **Por que este lote existe:** são 3 criativos que venderam em espanhol desde 01/10 e nunca foram traduzidos para o FR. O FR é o melhor mercado da conta.
- **Mercado:** França, Canadá FR, Bélgica, Suíça e Caribe francês (Guadalupe, Martinica, Guiana). Francês natural e neutro, com tutoyer, como nos FR vencedores.
- **Nome do santo:** "San Benito" vira **"saint Benoît"** ("la prière de saint Benoît", "la médaille de saint Benoît").
- **Destino:** o mesmo das campanhas FR atuais (a live/VSL).
- **CTA final:** **"Appuie sur « En savoir plus » ci-dessous et rejoins la prière en direct."** Pode manter a frase de urgência do original, como "Reçois ton miracle avant que la porte ne se ferme pour toujours." O botão do Meta é LEARN_MORE ("En savoir plus").
- **Restrições de conteúdo:** sem preço e sem produto. Mantenha o teor do original, com as promessas e a urgência, sem suavizar.
- **Referência de vocabulário:** os vencedores FR. A transcrição deles está em `C:\Users\PICHAU\Downloads\SB-FR-VENCEDORES\*_transcricao.txt` (AD 9 FR, AD 7 FR, OP2 FR). Use o mesmo registro.

## Método B (validado em FR/EN/IT/PL)
1. **Transcrição e roteiro**
   - Transcreva o original com faster-whisper es.
   - Escreva o roteiro FR: tradução natural, duração parecida, texto na tela (títulos/cartões) em FR no mesmo estilo.
2. **Voz ElevenLabs**
   - A chave está em `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env`. Não imprima.
   - Use o modelo eleven_multilingual_v2.
   - A conta está no **LIMITE de vozes**: não crie, não clone e não apague nenhuma. Use vozes que já existem na conta e registre a escolha.
   - **Uma voz por personagem.** Jesus/narrador sagrado: "Jesus The Chosen" (AkQxVSf1kENGmX9WjeDE). Outros personagens: escolha uma voz existente com o mesmo gênero e idade do original.
   - Confira no whisper fr que a pronúncia é francesa.
3. **Lipsync HeyGen** em mode **speed**
   - O vídeo de entrada leva o áudio ORIGINAL (ES) e o áudio FR vai separado, em trechos de até ~12 s.
   - Com 2+ rostos, recorte só o rosto de quem fala e cole a boca e o queixo de volta.
   - Rosto pequeno no quadro: recorte e amplie 2x antes de mandar.
   - Critério de aceite: `checar_lipsync.py` com índice de pausa ≤ 0,6.
   - Se a boca falhar numa pausa, corte na fronteira da palavra ou cubra com b-roll/jump cut. **Não retoque a boca.**
   - Job parado há mais de 45 min: reenvie igual. **Não reenvie antes disso.**
   - Use cor bt601 fixa e `-reinit_filter 0`, e confira se há salto de pts.
4. **Limpeza da legenda queimada:** LaMa local.
   - Venv: `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Scripts\python.exe`.
   - Base: `...\_trabalho\_lote\lama_base.py`.
   - A faixa precisa cobrir todo o texto. Confira com zoom.
5. **Legenda FR:** palavra a palavra, no estilo do original. Use uma fonte com os acentos FR (é è ê à ç ô û ï) e confira.
   - Setas no CTA, com a mesma cor do original.
   - Música do original sem voz (demucs) a ~-32 LUFS.
6. **Resolução:** a mesma da fonte, nunca abaixo de 720p.

## QA
1. Rode `revisar_ad.py` do kit a partir de `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\`, com PYTHONIOENCODING=utf-8 e whisper **fr**.
   - Termos proibidos (em .txt UTF-8): resíduo de espanhol ("San Benito", "oración", "en vivo", "Toca", "más información", "ver más"), resíduo de inglês ("Learn More", "Tap") e preço ("$", "€").
2. Confira a folha de contato, a boca nas pausas, os quadros soltos, o silêncio no fim e se sobrou legenda ES (zoom).
3. Chame 1 subagente revisor independente e **espere o resultado** antes de entregar. Corrija o que ele achar. Nenhum revisor pode matar processos.
4. NÃO abra os vídeos.

## Saída
- **Pasta:** `C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\<NN>_<NOME>\`, com:
  - `SB-FR-<NOME>.mp4`
  - `_roteiro-fr.txt` (ES × FR e decisões)
  - `_texto-anuncio.txt`: Titre ≤40 / Texte principal / Version courte ≤125 / Bouton: LEARN_MORE "En savoir plus". Sem preço, chamando para a prière en direct. Notas internas só depois de uma linha "Notes:".
  - `_frames.jpg`
  - `PRONTO.txt`
- **Arquivos:** trabalhe só no seu `_trabalho\`. Não escreva nas pastas de origem. Apague os intermediários pesados ao final.
- **Painel:** `python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa sbfr2-<nome> "<título>" --texto "..."` (e também img/custo/fim).
- **Custos:** ElevenLabs custa centavos e o HeyGen speed usa os créditos do plano. Não meça saldo. Nada pago fora disso.
- **Relatório curto:** arquivo, duração, vozes, nº de jobs HeyGen e imperfeições com tempos.
