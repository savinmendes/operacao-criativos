# Relatório: F3 (vizinha fofoqueira, corpo A) e F5 (presente para o pai, corpo B). Podadora COD Chile, 08/10/2026

## Entregas (`PODADORA-CL\VENCEDORES\FORA\`)

| Arquivo | Gancho | Cenas do gancho | Gancho | Total | MB |
|---|---|---|---|---|---|
| `F3 - VECINA-SAPA-A-ES-CL.mp4` | Vizinha: "¿Contrataste jardinero? ¡Te debe haber salido carísimo!" / Dono: "No po… lo hice yo, en diez minutos." | Avatar da vizinha na cerca (HeyGen, 0–3,93 s) → avatar do dono com a máquina (HeyGen, 3,93–6,67 s) → close da máquina cortando o mato alto (original_04 27,6–28,8 s, só pernas) → câmera da porta cortando (original_04 8,0–9,0 s, emenda contínua no corpo) | 8,87 s | 56,0 s | 25,8 |
| `F5 - REGALO-PAPA-B-ES-CL.mp4` | Senhor: "Pensé que no iba a poder… es liviana y tiene ruedas." / caixa fixa "EL REGALO PARA PAPÁ 🎁" | Avatar do senhor erguendo a máquina com uma mão (HeyGen, 0–3,83 s) → máquina com rodas vindo para a câmera (vencedor1 21,45–22,25 s) → corredor com mato alto (vencedor1 0,0–2,1 s, emenda contínua no corpo) | 6,77 s | 41,6 s | 26,2 |

- **Corpo A:** AD 04 de 9,000 s até o fim, sem alteração.
- **Corpo B:** vencedor1 de 2,100 s até o fim, escalado para 720x1280, sem outra alteração.
- **CTA e selo:** os do próprio corpo.
- **Legenda da fala:** no estilo drop do kit, com 1 palavra amarela ("carísimo", "diez", "liviana", "ruedas").
- **Faixa do aviso em espanhol do AD 04:** só nos takes do original_04, que têm o aviso em inglês queimado.
- **Música e fundo:**
  - F3 usa o áudio do AD 04 nos 8,87 s antes do corte (só música).
  - F5 usa o `no_vocals` do vencedor1 nos takes reais (o original não tem música). Por isso a emenda não dá pulo.
- **Volume das falas:** igualado à voz do corpo (A: LUFS do corpo −0,5; B: −14,3 LUFS).
- **Script:** `_vencedores\FORA\montar_fora.py F3|F5` reproduz tudo. Os arquivos de trabalho estão em `_vencedores\FORA\` (`img/`, `av/`, `voz/`, `trab/`, `revisao/`, `emenda/`).

## Avatares e vozes
- **Imagens base:** Flora, Nano Banana 2 (`i2i-gemini-3.1-flash-image`), 9:16. Projeto "PODADORA CL - takes IA (2026-10-08)", `prj_ns7fv2n485kqy6kr5pm6xbtxzd8fwy0w` (havia 2 projetos com o mesmo nome criados ao mesmo tempo; usei o mais antigo). A foto do kit foi enviada como referência nas cenas com a máquina.
  - **Vizinha** (~55 anos, cerca de madeira, limoeiro, casas de telha): aprovada na 1ª tentativa.
  - **Dono** (~40 anos, de pé no gramado cortado, segurando a máquina com as rodas no chão): aprovado. A máquina está fiel (verde-limão e preta, 2 rodas, disco de serra, cabo telescópico).
  - **Senhor:** refeito 1 vez.
    - A 1ª saiu de boca aberta, com expressão exagerada e barba cheia, e foi reprovada.
    - A 2ª foi aprovada: ~68 anos, bigode branco, ergue a máquina com uma mão (reforça o "es liviana"). A máquina está fiel à foto, com o "SEESE" pequeno no cabo.
- **Lipsync:** HeyGen `create_video_from_image` (photo avatar), 9:16 720p, expressiveness high. O áudio veio do `tts_elevenlabs.py`, com 0,15 s de silêncio antes e 0,45 s depois.
- **Vozes de catálogo do ElevenLabs** (es-chilean, `eleven_multilingual_v2`):
  - vizinha: "Isa Pro" `lLsDvdl6OjtZfLJPM2HA` (feminina, meia-idade);
  - dono: "Luis - voz natural latina Chile" `ZuuXsIgssLuaZ8Slz3yX` (masculina, meia-idade);
  - senhor: "IVÁN_OLIVARES" `aI9919Z6KR2NIkiqeIWg` (masculina, idosa).

## Custos (medidos)

| Item | Antes | Depois | Gasto |
|---|---|---|---|
| **HeyGen** (créditos premium) | 8814 | 8808 | **6 créditos** (de 80): vizinha 4 s = 2; dono + senhor = 4 |
| **Flora** | — | — | **US$ 0,288** (de US$ 1): 4 imagens Nano Banana 2 × US$ 0,072 (3 + 1 refação do senhor). Nenhum vídeo gerado |
| **ElevenLabs TTS** | — | — | **≈ US$ 0,030**: 178 caracteres. Inclui 1 teste de "¡No po!" (36 caracteres, US$ 0,006) que não foi usado |

Sobre a medição:
- O saldo do Flora é compartilhado com os outros agentes, que estavam rodando ao mesmo tempo. Por isso o custo do Flora é a soma do `charged_cost` de cada geração, e não a diferença de saldo.
- Os créditos do HeyGen foram lidos logo antes e logo depois de cada vídeo.

## Revisão
- **`revisar_ad.py`** rodou pelo PowerShell, com `--passo 1`, `--proibidos _vencedores\FORA\proibidos.txt` (UTF-8, mesma lista do vencedor A) e `--lipsync` em cada clipe de avatar.
  - **F3: OK, nenhum problema.**
    - Decodificação OK, sem salto de pts e sem quadro solto.
    - Termos proibidos: nenhum.
    - Lipsync APROVADO: índice de pausa 0,02 na vizinha e 0,04 no dono.
  - **F5: 1 "PROBLEMA" herdado do corpo.**
    - É o silêncio de 4,25 s no fim, que vem do próprio vencedor (igual ao B0–B6) e foi mantido porque o corpo e o CTA não podem ser alterados.
    - Decodificação OK, sem salto de pts e sem quadro solto.
    - Termos proibidos: nenhum.
    - Lipsync APROVADO: índice de pausa 0,22.
    - Avisos esperados: o vencedor não tem setas (o CTA é falado, "Pícale aquí abajo").
- **Correções feitas durante a revisão:**
  - **F5:** o take das rodas cruzava um corte de cena do original e deixava um quadro solto (167 ms). Encurtei o take para 0,8 s, terminando antes do corte.
  - **F3:** a faixa do aviso entrava 1 quadro atrasada no 1º take do original_04 e o aviso em inglês aparecia nesse quadro. Agora entra 1 quadro antes.
  - **F5:** a caixa do texto quebrava o 🎁 numa 2ª linha. Ficou em uma linha.
- **Folha de 1 em 1 quadro** em cada emenda (5 quadros antes e 5 depois): `_vencedores\FORA\emenda\F3_emendas.jpg` e `F5_emendas.jpg`. Os cortes estão limpos, a emenda gancho→corpo é contínua (mesma tomada) e as rodas e o disco da máquina aparecem sem deformação nos clipes HeyGen.
- **Transcrição do gancho** (whisper es):
  - F3: "¿Contrataste jardinero? Te debe haber salido carísimo." / "No puedo, lo hice yo en 10 minutos."
  - F5: "Pensé que no iba a poder, es liviana y tiene ruedas."
  - Nenhuma frase foi cortada: as falas terminam 0,4–0,6 s antes do corte.

## Pontos de atenção (precisa de revisão manual)
- **"No po…" (F3):** o whisper transcreve como "No puedo". O modelo não conhece o "po" chileno; testei uma 2ª versão ("¡No po!") e deu o mesmo. A legenda na tela mostra "NO PO… LO HICE YO", o que desambigua. Vale ouvir; se soar como "no puedo", basta trocar a fala, e refazer o lipsync custa ~2 créditos.
- **"carísimo":** fala de custo do jardineiro, sem preço nem moeda. Não está na lista de proibidos.
- **Nome do arquivo:** "SAPA" é a gíria chilena para fofoqueira. Renomeie se preferir.
- **Legenda na troca de avatar (F3):** a última palavra da vizinha ("CARÍSIMO!") fica 1 quadro sobre o 1º quadro do dono. É imperceptível.
- **Texto do anúncio** (título + texto principal): não foi feito, porque o briefing não pediu.
