# SB Reel Medalla ES: San Benito no esqueleto do reel "Sagrado Verso"

> Criativo de ~2 min em espanhol para San Benito, com a sequência de blocos do reel de referência "Sagrado Verso" e roteiro próprio (comerciante + sacerdote fictícios, oração da medalha de São Bento). Em produção em 13/10/2026. Abra para continuar este lote ou repetir o formato.

## Contexto de uso
- **Frente:** Infoproduto, Oração de San Benito, espanhol (LATAM/neutro).
- **Origem:** destrinche do reel `DeKy6u6xSr0` (perfil Sagrado Verso) em 13/10/2026. Método e riscos em [../19-destrinchar-e-adaptar-referencias.md](../19-destrinchar-e-adaptar-referencias.md).
- **Pasta:** `Downloads\SB-REEL-MEDALLA-ES\`.
  - `roteiro.txt`: narração final, ~1:55, com marcação de tempo.
  - `_trabalho\imagens\`: imagens base (`comerciante_retrato`, `salao_vazio`, `salao_cheio`, `sacerdote_live`, `medalla_san_benito`).
  - `_trabalho\voz\`: narração. `takes\` e `graficos\` ainda vazios em 13/10/2026.
- **Roteiro (estrutura):**
  1. comerciante 55+ ajoelhado no salão vazio, recitando as palavras da medalha (0:00);
  2. selfie: "casi seis meses sin clientes", aprendeu numa transmissão com um sacerdote (0:12);
  3. sacerdote em moldura "EN VIVO": "Repite conmigo" + as 6 linhas latinas da medalha de São Bento com tradução (*Crux sancta sit mihi lux… Ipse venena bibas*) (0:31–1:06);
  4. explicação: os monges a rezam há séculos; "no basta con repetirla una vez" → "Camino de Fe con San Benito" (1:06–1:32);
  5. compromisso de 7 dias + compartilhar (1:32);
  6. CTA: "Ahora mismo está ocurriendo una transmisión en vivo con San Benito. Toca el botón «Ver más»" (1:42).
- **Diferenças para a 1ª adaptação** (`REELS-REFERENCIA\sagrado-verso_adaptacao-san-benito-ES.md`, Doña Rosa): personagem masculino comerciante; oração **pública** da medalha no lugar das 7 palavras inventadas; destino "transmisión en vivo"/"Camino de Fe" no lugar de "el video aquí abajo"; botão "Ver más".
- **Personagens fictícios**, sem nome real. Selo **"VIDEO FICTICIO"** no topo à direita durante o vídeo todo.
- **Voz (ElevenLabs):**
  - amostras testadas em `voz\amostras\`: comerciante = `com_fabo` e `com_santiago`; sacerdote = `sac_adan` e `sac_gabriel`. Qual voice_id ficou: **precisa de revisão manual** (`voz\partes\`);
  - montado: `comerciante.mp3` (35,58 s) e `sacerdote.mp3` (82,68 s, entra em 36,03 s); `narracao_completa.mp3` com 118,72 s (`timeline.json`).
- **Compliance a confirmar:** o roteiro mantém "Sácame de esta escasez" e "seis meses sin clientes" (dor financeira) e a urgência de "transmisión en vivo". A destrinche recomendava evitar promessa de resultado financeiro. Se a pessoa decidiu manter: **precisa de revisão manual** (registrar a decisão aqui).
- **Pendências:** takes de vídeo (imagem → vídeo/avatar), gráficos (arte das 6 linhas latinas sublinhadas, moldura EN VIVO, setas), montagem, revisão, versão curta de ~33 s, texto do anúncio. Oferta/página do "Camino de Fe": **precisa de revisão manual**.

## Lógica de uso
1. **Voz:** gere as falas por parte no ElevenLabs e monte com `_trabalho\voz\montar_vozes.py`. O script:
   - junta as partes;
   - insere pausas depois de cada linha latina (tempo para o "repite conmigo");
   - grava o alinhamento por palavra com a grafia **correta**.
2. **Latim no TTS:** mande ao TTS a grafia fonética e corrija na legenda (`CORRIGE` no script: "míki"→"mihi", "Sátana"→"Satana", "Númcuam"→"Numquam", "cue"→"quae", "líbas"→"libas", "bíbas"→"bibas"). Assim a pronúncia sai certa e a legenda fica com o texto real. Confira com whisper.
3. **Imagens → takes:** a partir das imagens base, gere os takes (Flora/Kling/Seedance para cenas; HeyGen para selfie e sacerdote falando), mantendo a mesma persona/roupa em todas as cenas. Orce antes (custo + tempo + opção mais rápida). Teste 1 cena se o método for novo.
4. **Montagem:** estilo dos SB-JESU (legenda caixa alta branco + amarelo palavra a palavra, setas amarelas no CTA), selo "VIDEO FICTICIO" fixo, moldura "EN VIVO" fictícia sem @ real. A legenda vem do alinhamento do roteiro, nunca do whisper do vídeo montado.
5. **Revisão:** `revisar_ad.py` + whisper es + folha de contato + checagem de que nenhum nome, rosto ou print real de terceiro entrou.
6. **Se a pessoa pedir mais:** versão curta (gancho + 1 frase da selfie + 3 linhas latinas + CTA), outras personas de gancho (mulher na cozinha com contas, homem no ponto de ônibus, avó com neta) e versão FR (saint Benoît) com o mesmo esqueleto.

## Relacionados
- [../19-destrinchar-e-adaptar-referencias.md](../19-destrinchar-e-adaptar-referencias.md)
- [san-benito-es-vencedores.md](san-benito-es-vencedores.md), [san-benito-fr.md](san-benito-fr.md)
- [../08-voz-e-dublagem.md](../08-voz-e-dublagem.md), [../09-lipsync-e-avatar-heygen.md](../09-lipsync-e-avatar-heygen.md)

## Atualização 14/10/2026 (estado final)
- **Contexto:** a série saiu em 2 versões. A 1ª tem 11 vídeos com o selo "VIDEO FICTICIO" (`Downloads/SB-MEDALLA-SERIE-ES/`). A 2ª, a **COMPLETA**, foi feita depois do raio-x `completar-criativo` e aprovada pela pessoa (`Downloads/SB-MEDALLA-COMPLETA-ES/`). O taxista foi cancelado pela pessoa, que também não quis marca Uber. Cada persona tem voz própria e todas usam o mesmo padre, com o mecanismo das letras da medalha e o CTA único da transmissão 24 h (confirmada pela pessoa). Ainda não há dado de performance.
- **Lógica:** para repetir o formato com uma persona nova, siga `personas/BRIEFING_COMPLETA.md` na pasta do lote e as regras de [../22-licoes-producao-video.md](../22-licoes-producao-video.md). O script de montagem por persona é uma cópia de `montar_completa2.py` com um `config.json`.
