# Relatório: criativos "fora da caixa" F1 (ASMR) e F4a/F4b/F4c ("respondiendo al comentario"), Podadora COD Chile (08/10/2026)

**Regra seguida:** só tomadas que já existem (`original_03.mp4`, `original_04.mp4` e `vencedor1.mp4`). Nenhuma imagem ou vídeo foi gerado por IA, e não houve gasto em Flora nem em HeyGen.
**Corpos:** entram intactos do ponto de corte até o fim, com o CTA original. A única mudança é a recodificação final para caber em 30 MB.
- **Corpo A:** AD 04 a partir de 9,000 s.
- **Corpo B:** `vencedor1.mp4` a partir de 2,100 s, escalado de 576x1024 para 720x1280 sem recorte.

**Script:** `PODADORA-CL\_vencedores\FORA\F1F4\montar_F1F4.py`. Reproduz cada vídeo com `python montar_F1F4.py F4b`.
**Som do F1:** `PODADORA-CL\_vencedores\FORA\F1F4\som_corte.py`.

## Entregas (`PODADORA-CL\VENCEDORES\FORA\`)

| Arquivo | Gancho (fala / texto na tela) | Cenas do gancho | Gancho | Total | MB |
|---|---|---|---|---|---|
| `F1 - ASMR-B-ES-CL.mp4` | **Sem narração.** Só som de corte. Caixa "ANTES 😩" (0–2,4 s) → "10 MIN DESPUÉS 😮‍💨" (5,5 s até o fim do gancho) | corredor tomado de mato (vencedor1 0,00–1,00) → máquina entrando no mato alto, close (original_03 13,55–14,95) → POV cortando mato alto (vencedor1 16,45–17,45) → close no mato alto (original_03 18,05–19,15) → faixa sendo aberta no gramado alto (vencedor1 19,40–20,40) → **POV da faixa listrada em câmera lenta 0,5x** (vencedor1 22,33–23,20, que vira 1,73 s) | 7,23 s | 42,1 s | 26,8 |
| `F4a - COMENTARIO-PASTO-ALTO-B-ES-CL.mp4` | Balão: **"¿Sirve para pasto alto?"** / fala (voz B): "¿Que si sirve para pasto alto? Esto estaba altísimo… y así quedó." | POV cortando mato alto (vencedor1 16,36–18,19) → faixas abertas no gramado alto (18,40–20,07) → POV da faixa listrada pronta (22,31–23,21) | 4,40 s | 39,3 s | 26,8 |
| `F4b - COMENTARIO-BATERIA-A-ES-CL.mp4` | Balão: **"¿Cuánto dura la batería?"** / fala (voz A): "¿Cuánto dura la batería? Trae dos baterías… si una se acaba, pones la otra y sigues." | máquina com rodas cortando junto às plantas, só pernas (original_04 24,45–26,05) → mesa com as 2 baterias 21V, só a mão (35,75–37,25), entrando em "Trae dos baterías" → close das rodas cortando o mato na calçada (27,47–29,07) → câmera da porta cortando o mato (7,40–9,00, emenda contínua no corpo) | 6,30 s | 53,4 s | 26,4 |
| `F4c - COMENTARIO-PESADA-A-ES-CL.mp4` | Balão: **"¿Es pesada?"** / fala (voz A): "¿Que si es pesada? Tiene ruedas… la guías sin cargar el peso." | máquina rodando no gramado junto à escada, só pernas (original_04 14,00–15,23) → close das rodas, entrando em "Tiene ruedas" (28,80–29,80) → guiando a máquina com uma mão junto às plantas, só pernas (24,45–26,88) | 4,67 s | 51,8 s | 26,1 |

**Formato:** todos em 720x1280, 30 fps, H.264 high, AAC 48 kHz estéreo e abaixo de 30 MB.

**Distribuição pedida:** F1 → corpo B. F4a → corpo B. F4b e F4c → corpo A. Cada gancho usa a voz do corpo em que entra:
- **B:** "PODADORA venc-B narradora", `57OUoWWIdEbPrxk0T02A`.
- **A:** `BgvvJ0I0R4tg6uf8DolY`.

### Como cada formato foi feito
- **F1, o som:** as tomadas não têm som de corte aproveitável. Para conferir, passei um classificador de áudio local (AST/AudioSet, gratuito) no `no_vocals` do demucs dos 4 originais e do vencedor1. Só apareceu música, resíduo de voz e ruído abaixo de −50 dB; nenhum trecho foi classificado como motor, cortador ou ferramenta.
  - Por isso o som foi **gerado localmente, sem custo**:
    - zumbido de motor elétrico, feito com ruído em filtro pente na rotação do disco, que cai de tom quando "pega" o mato;
    - grama sendo cortada (grãos curtos de ruído agudo);
    - arranque do motor sob o "ANTES";
    - na câmera lenta, rotação pela metade com "whoosh" grave.
  - O mesmo classificador reconhece o trecho de corte como "Power tool / Tools / Sawing".
  - O gancho ficou em −16,3 LUFS, contra −14,0 LUFS no corpo. Ele tem fade de 0,2 s e emenda direto em "Mira, dos baterías…".
- **F1, a câmera lenta:** 0,5x por interpolação de movimento (`minterpolate` mci). Conferi na folha 1:1 e não há deformação visível.
- **F1, o aviso em inglês:** as duas tomadas do `original_03` levam um zoom de 1,10 ancorado no topo, que tira o aviso em inglês queimado no rodapé. O corpo B não tem faixa.
- **F1, os emojis:** vêm em PNG do Twemoji (licença CC-BY 4.0). O Pillow local não junta a sequência ZWJ de 😮‍💨.
- **F4, o balão:** é um balão branco de comentário com avatar cinza genérico, o nome "Usuario" e **só a pergunta**: sem curtidas, sem estrelas, sem avaliação. Ele fica no topo (centro em y=330) durante todo o gancho.
  - A legenda da resposta segue o estilo drop do kit, com 1 palavra amarela.
  - No corpo A entra também a faixa do aviso em espanhol do AD 04, igual às variações A1–A6.
- **F4b, a resposta:** usa só o que o produto tem e o que já foi dito. São 2 baterias, e o original em inglês diz "so you've got a backup ready to go". **Não cito autonomia nem tempo de carga.**
- **F4c, a resposta:** usa a frase pedida. Ela bate com o original ("because it has wheels, you're not holding all that weight… you basically just guide it") e com o corpo A ("tiene ruedas").
- **Música e fundo dos F4:**
  - **Corpo A:** os segundos do próprio AD 04 imediatamente antes de 9,0 s, que são só música. A voz foi igualada ao LUFS da voz do corpo.
  - **Corpo B:** o fundo do original (`bed.wav`), quase silencioso porque o vencedor não tem trilha. A voz foi ajustada para −14,3 LUFS, o nível da narradora.

## Custos
| Item | Caracteres | US$ |
|---|---|---|
| TTS F4a (voz B) | 65 | 0,011 |
| TTS F4b (voz A) | 84 | 0,014 |
| TTS F4c (voz A) | 61 | 0,010 |
| **Total ElevenLabs** (1 geração por fala, nenhuma refeita) | **210** | **≈ 0,035** |

Flora, HeyGen e geração de imagem ou vídeo: **US$ 0**. O som do F1 e o classificador de áudio rodaram localmente.

## Revisão
- **`revisar_ad.py` pelo PowerShell:** rodado nos 4 vídeos com `--idioma es --idioma-residual en --passo 1 --proibidos _vencedores\A\proibidos.txt`. O arquivo de proibidos está em UTF-8 e cobre preço/moeda, "gratis" fora de "despacho gratis", garantia além dos 90 días, TikTok e link/enlace.
  - **F4b e F4c:** OK, nenhum problema.
  - **F1 e F4a:** 1 "problema", o **silêncio de 4,25 s no fim**. Ele já existe no vencedor B original e aparece igual em B0–B6. Foi mantido pela regra do corpo intacto.
  - Aviso esperado: o corpo B não tem setas, porque o CTA é falado ("Pícale aquí abajo").
  - **Termos proibidos:** nenhum nos 4.
  - **Saltos de pts no áudio:** nenhum.
  - **Cortes a menos de 0,3 s (quadro solto):** nenhum.
- **Transcrição do gancho (whisper):**
  - **F4a:** "que si sirve para pasto alto esto estaba altísimo y así quedó" → "mira dos baterías…".
  - **F4b:** "¿Cuánto dura la batería? Trae dos baterías. Si una se acaba, pones la otra y sigues." → "Quien inventó esto merece un aumento".
  - **F4c:** "que si es pesada, tiene ruedas, la guías sin cargar el peso" → "Quien inventó…".
  - **F1:** nenhuma fala no gancho.
  - **Nenhuma frase cortada.**
- **Folha de 1 em 1 quadro na emenda** (12 quadros antes e 12 depois do corte): `_vencedores\FORA\F1F4\revisao\F1|F4a|F4b|F4c_emenda_1a1.jpg`.
  - Os cortes são limpos, sem quadro solto ou repetido.
  - O balão, a caixa e a legenda somem exatamente no corte.
  - No F4b a câmera da porta continua sem pulo para o corpo.
- **Folha 1:1 de todos os cortes do F1:** `F1_cortes_1a1.jpg`. Os 5 cortes caem nos quadros previstos (1,00, 2,40, 3,40, 4,50 e 5,50 s) e não há quadro solto.
- **Rosto falando:** nenhum. Os ganchos têm só pernas, mãos, a moça de longe cortando (vencedor1) e a câmera da porta. Não há avatar nem lipsync.
- Os relatórios e as folhas de contato de cada vídeo estão em `_vencedores\FORA\F1F4\revisao\`.

## Pontos de atenção (revisão manual opcional)
- **F1, o som é sintético.** Ele soa como motor elétrico e grama, mas não é uma gravação real. Se houver um take com o som real da máquina, troque o `som_F1.wav`.
- **F1, "ANTES":** a caixa fica sobre a 1ª tomada (o corredor de mato) e sobre o começo da 2ª, quando a máquina já entra no mato. Depois o corpo volta ao mesmo corredor, ainda cortando, em 2,1 s do vencedor. É a mesma lógica do B4.
- **F1, "10 MIN":** veio do briefing. Não é um tempo medido no vídeo.
- **F4b, marca SEESE:** aparece nas baterias da mesa (1,5 s), como no corpo e na variação A4. Não há zoom nem destaque.
- **F4a, repetição de "mira":** o gancho não usa "mira", mas o corpo B começa com "Mira, dos baterías…" e depois repete a narração inteira, como no original.
- **Cenas repetidas:** as tomadas do gancho reaparecem mais adiante no corpo (vencedor1 16–23 s, original_04 24–29 s). Isso não tem como evitar sem material novo.

## Arquivos de trabalho
- **`_vencedores\FORA\F1F4\`:**
  - `montar_F1F4.py`;
  - `som_corte.py`, `som_F1_raw.wav` e `som_F1.wav`;
  - os PNGs do Twemoji;
  - `trab\<código>\`: tomadas, balão, caixas, legenda, `gancho.mov` e `info.json`;
  - `revisao\`.
- **`_vencedores\FORA\voz\F4a|F4b|F4c.mp3`:** as falas, cada uma com o seu `.alinhamento.json`.
