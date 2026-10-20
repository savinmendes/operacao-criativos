# Briefing — criativos "fora da caixa" da Podadora (08/10/2026)

A pessoa aprovou tudo. **Não pergunte nada.** **Nunca leia nem imprima arquivos .env.**

## Base comum
- Leia `PODADORA-CL\_vencedores\BRIEFING-VENCEDORES.md`, que é o mesmo contexto do produto, e `PODADORA-CL\VENCEDORES\RELATORIO-A.md` e `RELATORIO-B.md`, que mostram como o gancho foi colado no corpo.
- **Corpos vencedores**, que ficam intactos do ponto de corte até o fim, com o CTA original:
  - **Corpo A (DEVOLVER):** `PODADORA-CL\AD 04 - PODADORA-INALAMBRICA-DEVOLVER-ES-CL.mp4` a partir de 9,000 s. Script de referência: `_vencedores\A\montar_gancho.py`. Voz clonada do narrador: `BgvvJ0I0R4tg6uf8DolY`.
  - **Corpo B (ORILLA):** `PODADORA-CL\_vencedores\vencedor1.mp4` a partir de 2,100 s, escalado para 720x1280. Script de referência: `_vencedores\B\montar_ganchos.py`. Voz: "PODADORA venc-B narradora" `57OUoWWIdEbPrxk0T02A`, com tom mexicano mantido.
- **Produto:** a referência é `_vencedores\produto_kit.webp` (máquina verde-limão e preta com 2 rodas, cabo telescópico, 2 baterias de 21V, 2 discos de serra, 2 lâminas, protetor e carregador).
  - **Não invente** recurso.
  - Nas cenas geradas, a máquina tem que ser **igual à da foto**.
  - **Não mostre marca de terceiros.** A marca SEESE da foto pode aparecer pequena; não destaque.
- **Regras do Meta:**
  - sem preço, sem depoimento inventado como real, sem "notícia";
  - antes e depois de **gramado** pode;
  - CTA e selo: os do corpo.
- **Formato:** cada criativo = gancho novo (3–8 s, salvo indicação) + corpo vencedor, em 720x1280. Monte com os scripts do A e do B, que já resolvem a emenda, a legenda e o volume.
- **Revisão** de cada vídeo:
  - `revisar_ad.py` pelo PowerShell, com os proibidos num **.txt em UTF-8** (preço, garantia não confirmada, TikTok, "link");
  - folha de 1 em 1 quadro na emenda;
  - nenhuma frase cortada e nenhum quadro solto;
  - rosto falando só se for avatar com lipsync próprio.
- **Saída:** `PODADORA-CL\VENCEDORES\FORA\<código> - <NOME>-<A|B>-ES-CL.mp4` e um relatório `PODADORA-CL\VENCEDORES\FORA\RELATORIO-<agente>.md`.
- **Não abra os vídeos.**

## Gerações no Flora
- Projeto: crie um, "PODADORA CL - takes IA (2026-10-08)", no workspace `ws_qd750nr5tby8qpnr1kbqj7aft17v8ey8`. Se outro agente já tiver criado, reutilize.
- **Imagem base:** `i2i-gemini-3.1-flash-image` (Nano Banana 2, US$ 0,072), partindo da foto do kit, para a máquina sair fiel.
- **Vídeo:** `i2v-minimax-h3-max-gateway` (MiniMax H3 Max, ~US$ 0,48 por clipe), 9:16.
- Revise cada clipe a olho, pela folha de quadros: máquina fiel à foto, sem deformação, sem texto estranho e sem mão com 6 dedos. Refaça no máximo 1 vez.
- **Teto por agente** (indicado na tarefa). Registre o custo de cada geração.

## HeyGen
- Avatares por prompt (photo avatar). O áudio sai do `tts_elevenlabs.py` e vai para o lipsync do avatar (a integração ElevenLabs↔HeyGen está quebrada).
- ~15 créditos por ~50 s de avatar. Meça.
