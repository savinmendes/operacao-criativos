# Relatório: criativos fora da caixa F2 e F6, Podadora COD Chile (08/10/2026)

Briefing: `_vencedores\BRIEFING-FORA-DA-CAIXA.md`. Teto Flora deste agente: US$ 6. **Gasto real no Flora: US$ 1,200.**

## Entregas (`PODADORA-CL\VENCEDORES\FORA\`)

| Arquivo | Gancho | Visual do gancho | Gancho | Total | MB |
|---|---|---|---|---|---|
| `F2 - DUELO-BENCINA-A-ES-CL.mp4` | Narração: "Mi vecino con la de bencina… y yo con esta." Texto: ¿CUÁL PREFIERES? 👇 | Tela dividida 720x640 + 720x640 com uma linha branca no meio. **Em cima:** take IA de um homem num quintal puxando a cordinha de uma roçadeira a gasolina vermelha, sem marca. Ela não pega e solta fumaça. **Embaixo:** tomadas reais do `original_04` com a nossa máquina cortando: 27,6–29,9 s (close do mato alto), 24,6–26,9 s (ao lado do canteiro) e 21,0–22,4 s (faixa de mato no cascalho). Só aparecem pernas e máquina. | 6,00 s | 53,1 s | 25,3 |
| `F6 - KIT-EXPLODIDO-B-ES-CL.mp4` | Narração: "Mira todo lo que trae la caja…" (voz da narradora B, tom mexicano). Texto: TODO ESTO / EN LA CAJA 📦 | Take IA: a máquina montada fiel à foto, com as peças do kit ao redor em vista "explodida", fundo cinza neutro e push-in lento com paralaxe. | 4,00 s | 38,9 s | 25,7 |

Os dois saem em 720x1280, 30 fps, H.264 high e AAC 48 kHz, abaixo de 30 MB.

## Como foram montados
- **F2 (corpo A):** script `_vencedores\FORA_F2F6\montar_F2.py`, adaptado do `A\montar_gancho.py`.
  - Usa a mesma emenda do A: o AD 04 entra de 9,000 s até o fim sem alteração.
  - A música do gancho é o próprio AD 04 de 3,0 a 9,0 s, então emenda sem pulo.
  - A fala foi ajustada ao LUFS da voz do corpo (+0,8 dB).
  - A narração foi dividida na pausa real (silêncio de 1,90 a 2,04 s): "Mi vecino con la de bencina…" entra em 0,30 s e "y yo con esta." entra em 3,30 s, quando o painel de baixo mostra a máquina cortando.
  - A legenda usa o estilo drop do kit, em y≈887 px, com "BENCINA" e "ESTA" em amarelo. A caixa fica sobre a linha divisória.
  - O recorte do painel de baixo (y 520–1160) deixa fora o aviso em inglês do rodapé do original.
- **F6 (corpo B):** script `_vencedores\FORA_F2F6\montar_F6.py`. Segue o mesmo caminho do `B\montar_ganchos.py` (`gerar_variacao.py montar`, modo A).
  - O vencedor1 entra de 2,100 s até o fim sem alteração.
  - O fundo vem do `B\bed.wav` e a voz foi ajustada para −14,3 LUFS (+1,6 dB).
  - O clipe IA (768x1344, 4:7) foi escalado e cortado para 720x1280: perde só 5 px de cada lado.
- O áudio gerado pelo MiniMax **não foi usado**: os clipes entram sem som.

## Gerações (Flora)
Projeto: **"PODADORA CL - takes IA (2026-10-08)"** (`prj_ns7fv2n485kqy6kr5pm6xbtxzd8fwy0w`) — https://app.flora.ai/projects/ns7fv2n485kqy6kr5pm6xbtxzd8fwy0w

| Peça | Modelo | Run | Custo |
|---|---|---|---|
| F2, imagem base (vizinho com roçadeira a gasolina genérica, 1:1) | `t2i-gemini-3.1-flash-image` (Nano Banana 2). Não vem da foto do kit, porque a máquina é a de gasolina, não a nossa | run_m17fd13g7tkg0ayxt7q9c9cceh8fx3c8 | US$ 0,072 |
| F6, imagem base 9:16 (kit em vista explodida a partir da foto) | `i2i-gemini-3.1-flash-image` + `produto_kit` | run_m174rx3egv2sstsc0ry77c7t698fxyc8 | US$ 0,072 |
| F2, vídeo de 6 s (768x768) | `i2v-minimax-h3-max-gateway` | run_m17217c7f66x8pm6xw0hgc9dfd8fw6z1 | US$ 0,576 |
| F6, vídeo de 5 s (768x1344) | `i2v-minimax-h3-max-gateway` | run_m1769hfnvg7dcvv85xmqjq5ceh8fwzj6 | US$ 0,480 |
| **Total Flora** | | | **US$ 1,200** (nenhuma geração refeita) |

- **TTS ElevenLabs** (`eleven_multilingual_v2`):
  - F2: 43 caracteres, voz `BgvvJ0I0R4tg6uf8DolY`;
  - F6: 30 caracteres, voz `57OUoWWIdEbPrxk0T02A`;
  - total de 73 caracteres ≈ **US$ 0,012**.
- **HeyGen:** US$ 0.
- **Total geral ≈ US$ 1,21.**

**QA dos clipes** (folhas em `_vencedores\FORA_F2F6\takes\*_folha.jpg` e `*_zoom.jpg`):
- **F2:** puxadas de cordinha cômicas (0–1,8 s), fumaça cinza-azulada e cara de frustração. A roçadeira não tem marca, logo nem texto. As mãos estão normais e não há deformação. Aprovado.
- **F6:** a máquina está fiel à foto em todos os quadros: verde-limão e preta, cabo telescópico, 2 rodas e disco sob o protetor. As peças são só as do kit: 2 discos, protetor, 2 lâminas, 2 baterias 21V, carregador, arruelas, chave, chave de fenda, fios e as 2 rodas avulsas da foto. Não há texto gerado, só a marca SEESE pequena nas baterias e no cabo, como na foto. Aprovado.
- **Desvio no F6:** o MiniMax entregou um push-in com as peças quase paradas ao redor, e não as peças "se juntando" para formar a máquina. O briefing aceitava a alternativa de máquina montada com as peças ao redor, então não refiz. O modelo `f2v` (primeiro e último quadro) não aparece para o MiniMax H3 neste catálogo.

## Revisão
- **`revisar_ad.py`:** rodado pelo PowerShell com `--idioma es --idioma-residual en --passo 1 --proibidos proibidos.txt` (UTF-8, a mesma lista do A: preço/moeda, "gratis" fora do despacho, garantia além dos 90 días, TikTok, link/enlace).
  - **F2:** OK, nenhum problema (exit 0).
    - Nenhum termo proibido.
    - Não há quadro solto: 10 cortes, nenhum par a menos de 0,3 s.
    - Não há salto de áudio.
    - As setas estão no último quadro e não ficam sobre a faixa.
  - **F6:** 1 "PROBLEMA": **silêncio de 4,25 s no fim**. Esse silêncio vem do próprio vencedor1 e aparece igual no B0–B6. Foi mantido pela regra do corpo intacto.
    - O aviso "sem setas" também é esperado, porque o vencedor B não tem setas e o CTA é falado.
    - Nenhum termo proibido, nenhum quadro solto e nenhum salto de áudio.
- **Frases (whisper es):**
  - **F2:** "Mi vecino con la de vecina y yo con ésta." → "¿Quién inventó esto? Merece un aumento." Nenhuma frase cortada.
    - No mix com a música, o whisper small ouviu "vecina". Na fala isolada, o small e o medium transcrevem "Benzina/benzina", ou seja, a pronúncia está certa.
  - **F6:** "Mira todo lo que trae la caja." → "Mira, dos baterías…". Nenhuma frase cortada.
- **Folha de 1 em 1 quadro na emenda:** `_vencedores\FORA_F2F6\revisao\F2_emenda_1a1.jpg` e `F6_emenda_1a1.jpg`.
  - Os cortes são limpos, sem quadro solto nem repetido.
  - A caixa e a tela dividida somem exatamente no corte. No F2, a legenda do corpo ("QUIEN INVENTÓ") entra 2 quadros depois.
- **Rostos:** ninguém fala na tela. O homem do F2 só faz careta de esforço, não fala, e a narração é do narrador em off. O F6 não tem pessoas.
- **Relatórios e folhas de contato:** `_vencedores\FORA_F2F6\revisao\*_revisao.txt/.jpg`.

## Pontos de atenção
- **F6, repetição do "Mira":** o gancho "Mira todo lo que trae la caja…" é seguido pela 1ª frase do corpo, "Mira, dos baterías…". Isso é consequência da regra do corpo intacto, igual ao B1/B6.
- **F6, "cuatro cabezales":** o corpo B continua dizendo "cuatro cabezales", que é a fala original e já estava apontada no RELATORIO-B.
- **F2, take IA:** a fumaça aparece desde o 1º quadro. A cabeça do carretel da roçadeira IA é um pouco simplificada, mas não dá para notar no painel de 720x640.
- **Projeto Flora duplicado:** outro agente e eu criamos o projeto com o mesmo nome ao mesmo tempo, com 0,7 s de diferença. Usei o primeiro (`prj_ns7fv2n…`). O meu (`prj_ns79qnwxfbn177wryzt64c8q698fxkg7`) ficou **vazio** e pode ser apagado à mão. Não apaguei porque não há ferramenta para isso e apagar exige autorização.
- O texto do anúncio (título e texto principal) não foi feito, porque o briefing não pediu.

## Arquivos de trabalho
`_vencedores\FORA_F2F6\`:
- `montar_F2.py`, `montar_F6.py`;
- `img\` (imagens base);
- `takes\` (clipes IA + folhas de QA);
- `voz\` (F2/F6 .mp3 + alinhamento);
- `trab\F2`, `trab\F6` (intermediários, `info.json`, config do F6);
- `proibidos.txt`;
- `revisao\`.
