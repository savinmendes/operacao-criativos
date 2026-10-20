# VSL DE: lipsync por lote (vozes aprovadas pela pessoa em 19/10/2026)

**Entradas:**
- `_trabalho\voz\lotes.json`: cada trecho tem id, falante, cena, ini/fim no original, ini/fim na timeline nova, fator e texto.
- `_trabalho\voz\narracao_de_completa.wav`: áudio DE na timeline nova.
- `_trabalho\voz\timeline_de.json`.
- Fonte: `C:\Users\PICHAU\Downloads\Lead 2.mp4`, só leitura.

## Para cada trecho do seu lote
1. **Vídeo de entrada:**
   - Recorte o trecho do ORIGINAL (ini/fim original) **com o áudio original em espanhol**.
   - Aplique o MESMO fator de tempo no vídeo e no áudio ES (setpts + atempo), para casar com a duração DE.
   - Se o vídeo foi remapeado no tempo e o áudio original não, o HeyGen devolve a boca intacta.
   - Trecho com menos de 3 s: junte com o vizinho da mesma cena ou faça padding com quadro congelado (`tpad=stop_mode=clone`) e descarte o excesso depois.
2. **Áudio novo:** recorte de `narracao_de_completa.wav` nos tempos da timeline nova.
3. **HeyGen `create_lipsync`:**
   - Mode **speed**.
   - Envie em lote (`create_lipsync_batch`) quando possível.
   - Trechos de até 12 s.
   - Job parado há mais de 45 min: reenvie igual, nunca antes.
   - Rosto pequeno no quadro: recorte o rosto e amplie 2x antes de enviar; depois cole só boca e queixo de volta (elipse suave).
4. **Aceite:**
   - Rode `checar_lipsync.py` do kit (`C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas\`).
   - Índice de pausa ≤ 0,6.
   - Se reprovar: corte na fronteira da palavra e marque o trecho para b-roll ou jump cut na montagem. **Não retoque a boca.**
   - Cor bt601 fixa.
5. **Saída:**
   - `_trabalho\lipsync\LOTE_N\<id>.mp4`: só vídeo, já na duração da timeline nova.
   - `_trabalho\lipsync\LOTE_N\relatorio.json`: id, job_id, índice e status (ok / aviso / usar_broll).

## Regras
- Trabalhe só na sua pasta `LOTE_N`.
- Não mexa em `_trabalho\base`, `voz` nem `roteiro`.
- Não mate processos.
- Os outros 3 lotes rodam em paralelo na mesma conta HeyGen. Não meça saldo; o coordenador mede.
- Créditos do plano: cerca de 90 por lote. Não gaste fora disso.
- **Painel:** `python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa vsl-de-lip<N> "Lipsync lote N" --texto "[k/N] ..."`.
- **Relatório curto:** quantos trechos ok, em aviso e para b-roll, nº de jobs e reenvios.
