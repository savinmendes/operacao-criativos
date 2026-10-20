# Briefing do lote — 14 vídeos restantes (PT → espanhol neutro LATAM), noite de 07→08/10/2026

A pessoa está dormindo e mandou terminar todos os criativos. **Não pergunte nada.** Na dúvida, escolha o lado seguro e anote no relatório. **Nunca leia nem imprima arquivos .env.**

## Base (leia antes, nesta ordem)
1. `BRIEFING-PILOTO.md`: contexto, propriedade confirmada (os criativos e os personagens de IA são da pessoa; clonar vozes e fazer lipsync é permitido), regras de roteiro e fluxo.
2. **`LICOES-LIPSYNC.md`** (se existir; o agente do AD 01 vai atualizando): qual variação de lipsync funciona em planos com 2 rostos. **Siga o que estiver lá.**
3. As revisões `revisao\REVISAO-01-13.md` e `revisao\REVISAO-05.md`: os defeitos que o revisor reprova.
4. Os relatórios do AD 01, 05 e 13 (`adNN\RELATORIO.md`) e os scripts deles. Reaproveite.

**Formato aprovado pela pessoa:** **cortes + lipsync mantendo o plano original**. Ela preferiu a versão com o Jesus atrás ao avatar completo. **Não use avatar completo.**

## Fluxo por vídeo (com tudo o que já aprendemos)
1. **Fonte:** `UNICOS_HD\NN.mp4` (720x1280). Muitos originais terminam com uma **tela parada sem fala** (cruz, "CLIQUE E RECEBA" etc.): corte essa parte (~0,7 s depois da última fala, fade de 0,3 s).
2. **Roteiro em espanhol neutro:** mantém fé, personagens, gancho, urgência suave, a "oración de nueve palabras" e o CTA "Toca el botón de abajo". Tira promessa de **dinheiro**, de **cura**, **ameaça**, **contagem regressiva** ("pocos segundos", "30 segundos", "puede salir del aire"), **depoimento com resultado** e **pessoa real/famosa**. Na imagem: tire moeda, marca ou famoso do Brasil (troque a cena).
3. **Vozes:**
   - Reutilize os clones se for a mesma personagem (meça a semelhança):
     - "ORACAO-11 mulher" `UNDKAyEJ2rTv99l7gCy5` (Desatadora dos ADs 11/01/05);
     - "ORACAO-11 menina" `VtWz85Bf8UfJlJLifFE3`;
     - "ORACAO-13 mulher" `ZsipxX9wNYg2lJhEScWc`;
     - "ORACAO-13 jesus" `lRnvtIq1W0SQIeABr1I4`;
     - "ORACAO-05 Clara (esposa)" `84WxgdFrdm1LAdwbQFZR`;
     - "ORACAO-05 marido" `Fn4faHoDwi31tC6L06Fl`.
   - Clone novo só para personagem nova ("ORACAO-NN <personagem>"). Nunca apague vozes.
   - Voz ≤ 1,1x.
4. **Legenda em português:** remova com o **LaMa na GPU** (`producao\_trabalho\_vg\Scripts\python`, veja `ad01\_tmp\lama_worker.py`), com **máscara justa** (só as letras e o contorno, dilatados ~9 px), longe da boca. Tire também ícones ou textos PT na tela.
5. **Lipsync (HeyGen):**
   - **Vídeo de entrada com o áudio ORIGINAL em PT**; o espanhol vai separado, como `audio`.
   - Trechos **≤ 12 s**, sem atravessar corte de câmera.
   - **Com 2 ou mais rostos no plano: recorte a entrada só no rosto de quem fala** e cole de volta, ou siga o que o `LICOES-LIPSYNC.md` disser.
   - Parâmetros: `precision`, `enableDynamicDuration=false`, `keepTheSameFormat=true`, `fpsMode cfr`, sem marca d'água.
6. **Checagem de cada trecho:** `python ferramentas\checar_lipsync.py saida.mp4 --audio-novo es.mp3 --original pt.mp4 [--rosto x,y,w,h]` (kit em `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos`).
   - **REPROVADO:** refaça, no máximo 2 vezes, com recorte mais justo ou trecho mais curto.
   - Se continuar reprovado, **cubra a boca** com outro enquadramento do próprio vídeo (reação, mãos, detalhe), sem mudar o áudio.
   - **Nenhum quadro final pode ter boca falando português.**
7. **Recolocação:**
   - descarte o 1º quadro da saída se ele for de outra tomada;
   - se a saída vier com quadros a menos, **reamostre no tempo** em vez de congelar;
   - suavize os saltos de boca nas emendas da mesma tomada;
   - mesmos metadados de cor (bt709/tv).
8. **Montagem:** `montar_ad.py` com legenda em espanhol pelo alinhamento, na altura da legenda antiga e fora da boca, setas no 1º "Toca", `resolucao` "720", **sem selo**.
   - Saída: `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD NN - ORACION-<TEMA>-ES-LATAM.mp4`.
9. **Revisão própria:** `revisar_ad.py "<final>" --idioma es --idioma-residual pt --proibidos "real,reales,dinero,depósito,cantidad,riqueza,cura,curada,enfermedad,cáncer,horas,segundos,aire,borrada" --lipsync "<trecho1>:<es1>:<pt1>[:x;y;w;h],..."`, **pelo PowerShell** (o Git Bash quebra os `:`).
   - O conjunto do vídeo precisa dar índice de pausa **≤ 0,6**.
   - Faça também uma folha de 1 em 1 quadro em volta de cada corte.
10. **Não abra o vídeo** (o revisor independente vem depois). Escreva `adNN\RELATORIO.md`.

## Limites
- HeyGen: com `mode speed` o custo é **~1 crédito por segundo de rosto falando** (a cobrança aparece com até ~1 h de atraso). Teto: **até 170 créditos por vídeo**. Meça com `get_current_user` antes e depois, e não dispare lote sem considerar o atraso da cobrança. Saldo em 07/10 à noite: ~8.800, que zeram em 30/10.
- ElevenLabs: o mínimo necessário.
- GPU compartilhada entre agentes: use LaMa com lotes moderados e `-threads 4` no ffmpeg.

## Relatório (a sua resposta), por vídeo
- O arquivo e a duração.
- O roteiro.
- As vozes.
- Os caracteres de TTS e os créditos.
- Os trechos de lipsync com o índice de pausa de cada um e o do conjunto.
- O que saiu ou foi trocado.
- O resultado da revisão.
- Os pontos para a pessoa olhar.
