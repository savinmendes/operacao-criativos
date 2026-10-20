# AD 09 — Instalador na escada (misto → fluxo Grupo A) — relatório

**Arquivo:** `producao\AD 09 - WYZE-SOLAR-CAM-PAN-INSTALADOR-ES-LATAM.mp4`
- 33,5 s, 720x1280, 30 fps, 24,0 MB, decodifica sem erro.

## O que foi feito
- **Cortado o início (0–3,6 s):**
  - rosto do criador;
  - título "How I make $400 in 15 minutes";
  - número da casa "55" (só aparece nesse trecho);
  - "Let me go get paid".
- O vídeo usa o original de 3,6 a 37,1 s, só com mãos e produto, na ordem original.
- **Legenda em inglês:** removida ao cortar o quadro em y 0–960 (540x960, ampliado 1,33x para 720x1280). Não foi preciso faixa.
- **"55":** conferido na folha de 1 s. Não sobrou em nenhum quadro, então não houve desfoque.
- **Áudio:**
  - Fundo: `no_vocals` do demucs. O original não tem música, só ambiente.
  - Narração nova no lugar da original.
- **Gancho:** caixa no topo (0–3,4 s) com "¡ASÍ DE FÁCIL SE INSTALA! 😱".
- **Legenda:** nova, pelo alinhamento.
- **Setas de CTA:** no "Toca" (30,6 s) até o fim.
- **Selo:** não tem. A versão com selo está pronta em `receita_com_selo.json`.

## O que saiu ou foi trocado no texto
- "sold out multiple times", "link down below", "restocked" e "don't sleep on these": removidos. No lugar, entrou "Pídela hoy. Toca el botón de abajo y pide la tuya."
- "prescription": virou "suscripción".
- "keep charged day and night": virou "con solo una hora de sol directo al día… y la batería la mantiene funcionando de noche y en días nublados".
- "take the panel off and mount it somewhere else": virou "el panel tiene un cable largo para ponerlo donde sí le dé".
- "widescreen / full night vision": virou "Graba en 2K, gira 360 grados y de noche ve a color".

## Voz e TTS
- **Voz:** ElevenLabs "Richard – Social Media" (`Cpm6N9BNC1M75bYS7kO1`), do catálogo. É masculina, latina neutra e dinâmica, sem clone.
- **Caracteres:** 589 (≈ US$ 0,10).
- **Velocidade:** 1,0x, sem atempo. A narração tem 32,7 s.
- **HeyGen:** não usado.

## Revisão
- **Whisper (es):** bate com o roteiro (`roteiro_es.txt`). Não aparece preço, país, TikTok, "link", Natal/ano-novo nem "sold out".
- **Whisper (en):** só a tradução do espanhol. Não sobrou fala em inglês.
- **Folha 1/s** (`rev_folha.jpg`):
  - nenhuma legenda em inglês;
  - nenhum rosto;
  - nenhum "55";
  - as setas ficam abaixo da legenda.
  - Há um quadro com chicote de câmera (~25,5 s) que já existe no original e funciona como transição.
- **Fim:** a narração termina em ~32,8 s; a cauda é de 0,7 s com as setas. Não há silêncio maior que 0,5 s.
- **Áudio:** conferidos os pacotes, sem buracos.

## Pendências
- O `finalizar.py --so-revisar` marca "VERIFICAR" só por esperar 1080x1920. O arquivo é 720 por especificação.
- "2K" é falado como "dos K". Confirmar se é esse o padrão dos demais ADs.
