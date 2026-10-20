# Briefing — piloto de 3 vídeos (PT → espanhol neutro LATAM), 07/10/2026

A pessoa aprovou o AD 11 como referência e pediu 3 vídeos para aprovação. **Não pergunte nada.** **Nunca leia nem imprima arquivos .env.**

## Contexto fixo
- **Propriedade confirmada pela pessoa em 07/10/2026:** a página da Biblioteca (id 104060992792639, "Keiko Tanaka") e todos os criativos são dela, com personagens gerados por IA. Os originais se perderam e as cópias HD da Biblioteca são a única fonte. Clonar as vozes dos personagens e fazer lipsync neles é **permitido** (modo B2).
- **Fonte:** `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\UNICOS_HD\NN.mp4` (720x1280). **Não faça upscale.**
- **Estudo:** transcrições em `_analise\fala\NN.json` e folhas de contato em `_analise\folhas\NN.jpg`.
- **Mercado:** hispânicos nos EUA e América Latina, em **espanhol neutro latino**. O produto novo ainda não foi definido, então o CTA fica genérico ("Toca el botón de abajo…") e **sem selo**.
- **Referência aprovada:** o AD 11, em `producao\AD 11 - ORACION-DESATADORA-ES-LATAM.mp4`. Todo o trabalho dele está em `producao\_trabalho\ad11\` e os scripts podem ser reaproveitados:
  - `_audio\montar_narracao.py`: monta a narração na linha do tempo;
  - `_tmp\tirar_legenda_v2.py` e `_tmp\cobertura.py`: tiram a legenda com fundo mediano onde a câmera é fixa e com LaMa local onde há movimento;
  - `_tmp\cortar_segmentos.py`;
  - `lipsync\recolocar.py`: recoloca os trechos quadro a quadro, com cor bt709;
  - `receita_ad11.json`.
  - Leia o `BRIEFING-TESTE-11.md` e os relatórios desse trabalho.
- **Kit:** `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\`. Leia o `CLAUDE.md` dele e o `CLAUDE.md` raiz, inclusive as armadilhas.

## Regras de roteiro (iguais às do AD 11)
- **Mantém:** o tom de fé, a personagem (a "Desatadora de Nudos" e as outras), o gancho, a urgência, a "oración de nueve palabras" e o CTA.
- **Tira ou suaviza:**
  - promessa de **dinheiro** concreto: valor, prazo, depósito, "quantia inesperada", "riqueza imediata";
  - promessa de **cura** ou saúde: "dor curada em X horas", doença;
  - **ameaça** ("se pular, a bênção some", "está pecando");
  - **depoimento com resultado** financeiro ou de saúde (pode virar "sintió paz y esperanza");
  - moeda ou referência do Brasil (real, Banco Central, nomes de lojas brasileiras): na imagem, troque a cena; na fala, tire.
- A duração do espanhol cabe na duração do original. Voz ≤ 1,1x.

## Passos (o fluxo do AD 11, com as correções)
1. **Áudio:**
   - Separe a voz com demucs e clone **um personagem por voz** (`clonar_voz.py`).
   - **Antes de clonar, reutilize os clones que já existem** se for o mesmo personagem ou a mesma voz: "ORACAO-11 mulher" `UNDKAyEJ2rTv99l7gCy5`, "ORACAO-11 menina" `VtWz85Bf8UfJlJLifFE3`. Compare a semelhança.
   - Nomes dos clones novos: "ORACAO-NN <personagem>". Nunca apague vozes.
   - Gere com `tts_elevenlabs.py` e alinhamento. Monte `narracao_es.wav` (mesma duração do vídeo) e um wav por personagem, com silêncio fora da fala de cada um.
   - Não use o fundo do demucs se ele sair mudo.
2. **Vídeo base:**
   - Tire a legenda queimada em português sem tocar boca e queixo.
   - Troque cenas com moeda ou marca do Brasil.
   - Corte os **trechos de rosto falando** para o lipsync.
3. **Lipsync (HeyGen MCP), com as duas armadilhas corrigidas:**
   - **O vídeo de entrada leva o ÁUDIO ORIGINAL EM PORTUGUÊS** daquele trecho. O espanhol vai **separado**, como `audio`. Se o espanhol for embutido no vídeo, a boca não muda.
   - **Trechos de até ~12 s.** Divida os maiores.
   - Parâmetros: `mode precision`, `enableDynamicDuration=false`, `keepTheSameFormat=true`, `fpsMode cfr`, sem marca d'água.
   - **Meça os créditos** (`get_current_user` antes e depois). Teto: 120 créditos por vídeo.
   - **Confira cada saída:** compare a região da boca entre o original e o lipsync. Se a diferença ficar só no nível de ruído (~2/255), o lipsync não aconteceu: refaça.
4. **Montagem:**
   - `recolocar.py`, depois o corpo com `narracao_es.wav` (cortado ~0,7 s depois da última fala, com fade de 0,3 s), depois `montar_ad.py` com legenda pelo alinhamento na altura da legenda antiga, setas no "Toca", `resolucao` "720", sem selo.
   - Saída: `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD NN - ORACION-<TEMA>-ES-LATAM.mp4`.
5. **Revisão própria:**
   - `revisar_ad.py --idioma es --idioma-residual pt --proibidos "real,reales,dinero inesperado,depósito,cantidad inesperada,borrada para siempre,curada,cura,horas"`.
   - Folha de contato com zoom na boca durante a fala.
   - **Não abra o vídeo:** um revisor independente vai checar antes de entregar à pessoa.

## Relatório (a sua resposta)
- O arquivo final e a duração.
- O roteiro em espanhol.
- As vozes (reaproveitadas ou novas, com os ids).
- Os caracteres de TTS.
- Os créditos HeyGen medidos.
- O que saiu ou foi trocado.
- O resultado da revisão.
- Os pontos para a pessoa olhar.
- Salve também em `producao\_trabalho\adNN\RELATORIO.md`.
