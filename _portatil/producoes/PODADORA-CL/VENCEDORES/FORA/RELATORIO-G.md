# Relatório G: ganchos com takes IA (Flora) + corpo A "DEVOLVER", Podadora COD Chile (08/10/2026)

**Corpo:** `AD 04 - PODADORA-INALAMBRICA-DEVOLVER-ES-CL.mp4` a partir de 9,000 s, sem nenhuma alteração (imagem, legenda, selo, setas, CTA e áudio). A única mudança é a recodificação final para ficar abaixo de 30 MB.
**Voz dos ganchos:** clone do narrador do corpo A, `BgvvJ0I0R4tg6uf8DolY`, modelo `eleven_multilingual_v2`. O volume foi igualado ao LUFS da voz do corpo.
**Música do gancho:** o próprio áudio do AD 04 nos segundos anteriores a 9,0 s (só tem música ali), então a trilha emenda sem pulo.
**Visual do gancho:**
- takes gerados no Flora: imagem base com Nano Banana 2 a partir de `produto_kit.webp` e vídeo com MiniMax H3 Max i2v, 768P, 5 s, 24 fps, convertido para 30 fps e recortado para 720x1280;
- a mesma faixa do aviso em espanhol do AD 04;
- caixa branca grande (Poppins Bold 46, cy 470);
- legenda drop com 1 palavra amarela.
**Script:** `_vencedores\G\montar_gancho_ia.py`. Reproduz qualquer um com `python montar_gancho_ia.py G3`.
**Flora:** projeto "PODADORA CL - takes IA (2026-10-08)" (`prj_ns79qnwxfbn177wryzt64c8q698fxkg7`). Ele já existia, criado por outro agente, e foi reaproveitado. Imagens e takes baixados em `_vencedores\G\flora\` e `_vencedores\G\takes\`.

## Entregas (`PODADORA-CL\VENCEDORES\FORA\`)

| Arquivo | Narração / texto na tela | Takes do gancho | Gancho | Total | MB |
|---|---|---|---|---|---|
| `G1 - SELVA-A-ES-CL.mp4` | "Mi patio parecía una selva… hasta que llegó esto." / DE SELVA A JARDÍN 🌿 | G1a: câmera entrando no quintal com mato alto, casa de telha ao fundo (0,3–2,0) → G1b: máquina empurrada sobre as rodas abrindo caminho no mato, só pernas (0,4–2,7) | 4,00 s | 51,1 s | 25,0 |
| `G2 - DOMINGO-LIBRE-A-ES-CL.mp4` | "Antes perdía el domingo entero en el patio… ahora no." / DOMINGO LIBRE ☕ | Homem de costas/perfil na cadeira tomando mate, gramado perfeito, máquina encostada na cadeira (0–4,0). Ele não fala | 4,00 s | 51,1 s | 25,9 |
| `G3 - UNA-MANO-A-ES-CL.mp4` | "Fíjate bien… esto se maneja con una sola mano. Así de fácil." / CON UNA MANO ✋ | Uma mão guiando a máquina sobre as rodas no gramado, câmera acompanhando, sem rosto (0–4,97) | 4,97 s | 52,1 s | 25,8 |
| `G4 - LLUVIA-DE-PASTO-A-ES-CL.mp4` | "Mira cómo corta… hasta el pasto más alto cae en segundos." / MIRA CÓMO CORTA | Close no chão do disco girando no pasto, pedaços voando contra o pôr do sol (0,2–4,2), sem pessoas | 4,00 s | 51,1 s | 26,0 |
| `G5 - CAJA-EN-LA-PUERTA-A-ES-CL.mp4` | "Pedí esto por internet… y lo pagué cuando llegó a mi casa." / PAGAS AL RECIBIR 📦 | G5a: caixa lisa, sem marca, no capacho da porta, push-in (0,2–2,0) → G5b: caixa aberta com a máquina montada, as 2 baterias 21V e o carregador (0,3–2,5) | 4,00 s | 51,1 s | 26,2 |

Todos saem em 720x1280, 30 fps, H.264 high e AAC 48 kHz.

**Ajustes nas ideias de partida:**
- **G4:** o texto da tela virou "MIRA CÓMO CORTA" em vez de "CORTA TODO", para não prometer um recurso que não foi confirmado.
- **G5:** "Pagas al recibir" é a mesma oferta que o corpo diz em "Despacho gratis, pagas al recibir".

## Custos

| Gancho | Flora: imagens (US$ 0,072 cada) | Flora: vídeos (US$ 0,48 cada) | Flora total | TTS (caracteres ≈ US$) |
|---|---|---|---|---|
| G1 | 2 (G1a, G1b) | 2 | **US$ 1,104** | 49 ≈ 0,008 |
| G2 | 1 | 1 | **US$ 0,552** | 53 ≈ 0,009 |
| G3 | 1 | 1 | **US$ 0,552** | 39 + 60 ≈ 0,016 (refeito) |
| G4 | 1 | 1 | **US$ 0,552** | 52 + 57 ≈ 0,018 (refeito) |
| G5 | 3 (G5a, G5b descartada, G5b v2) | 2 | **US$ 1,176** | 58 ≈ 0,010 |
| **Total** | 8 = US$ 0,576 | 7 = US$ 3,36 | **US$ 3,936** (teto US$ 9) | 368 ≈ **US$ 0,061** |

HeyGen: US$ 0, porque nenhum gancho tem rosto falando.

**Refeitos:**
- **G5b (imagem):** a 1ª versão punha na caixa 3 protetores (o kit tem 1), então foi refeita mostrando só a máquina montada, as baterias e o carregador. A descartada é `flora\G5b.png`.
- **G3 (TTS):** a 1ª fala tinha só 2,2 s.
- **G4 (TTS):** o whisper ouviu "**y** el pasto más alto se le resiste" no lugar de "ni…", o que inverte o sentido. A frase foi trocada.
- Os áudios descartados estão em `_vencedores\G\voz\v1\`.
- Nenhum clipe de vídeo foi refeito.

## Revisão
- **Fidelidade da máquina** (folha de quadros de cada clipe, `_vencedores\G\folhas\`, com zoom na mão do G3 e no disco do G1b):
  - a máquina segue a foto em todos os clipes: verde-limão e preta, 2 rodas, cabo telescópico prateado com travas pretas, alça em D e disco metálico;
  - nenhuma deformação, nenhuma mão com dedos a mais e nenhum texto estranho;
  - "SEESE" aparece pequeno só nas baterias do G5b.
- **`revisar_ad.py`:** rodado pelo PowerShell nos 5 vídeos, com `--idioma es --idioma-residual en --passo 1` e os proibidos em `_vencedores\G\proibidos.txt` (UTF-8, mesma lista do A).
  - **Resultado:** os 5 deram **OK** (exit 0). Nenhum termo proibido, nenhum par de cortes a menos de 0,3 s, nenhum salto de áudio e as setas ficam fora da faixa.
  - O whisper transcreve o gancho inteiro e emenda em "Quien inventó esto merece un aumento.": nenhuma frase cortada.
  - Relatórios em `_vencedores\G\revisao\`.
- **Folha de 1 em 1 quadro** na emenda gancho→corpo (`revisao\G1..G5_emenda_1a1.jpg`, consolidada em `emendas_todas.jpg`) e no corte interno de G1 e G5 (`*_corte_interno_1a1.jpg`):
  - os cortes são limpos, sem quadro solto ou repetido;
  - a caixa e a legenda do gancho somem exatamente no corte e o corpo entra em "QUIEN INVENTÓ".

## Pontos de atenção (revisão manual opcional)
- **Pulo de estética na emenda:** os takes IA são "limpos/cinematográficos" e o corpo começa na câmera de porta caseira, então a emenda é um corte seco de estilo. Não existe tomada contínua entre os dois, como havia em A1/A3.
- **G1b:** a máquina avança no mato, mas o corte da grama é discreto (limite de física do modelo de vídeo). Lê como "abrindo caminho", não como antes/depois.
- **G2:** o rosto do homem aparece de perfil enquanto toma mate. Ele não fala, então não há lipsync envolvido.
- **G5b:** as abas da caixa se mexem um pouco durante o push-in. O produto não muda.
- **Silêncio no fim:** os 0,8 s finais de silêncio vêm do AD 04 original e foram mantidos, pela regra do corpo intacto.
- **Projeto duplicado no Flora:** existem 2 projetos com o mesmo nome no workspace, criados ao mesmo tempo por agentes paralelos. Este lote está no `prj_ns79…`.
