# Relatório: ganchos "fora da caixa" H1–H5 + corpo B (ORILLA), 08/10/2026

**Corpo:** `_vencedores/vencedor1.mp4` de 2,100 s até o fim, intacto (narradora, CTA falado "Pícale aquí abajo"), escalado de 576x1024 para 720x1280 sem corte, igual ao lote B1–B6.
**Montagem:** `_vencedores/B/fora/montar_fora.py`. Ele segue o `montar_ganchos.py` do B e usa `gerar_variacao.py montar` com o mesmo corte, o mesmo fundo (`bed.wav`), a voz ajustada para −14,3 LUFS e a caixa branca do kit (64 px, cy=240).
**Takes IA (Flora):** projeto "PODADORA CL - takes IA (2026-10-08)" `prj_ns7fv2n485kqy6kr5pm6xbtxzd8fwy0w`. As imagens base foram feitas com Nano Banana 2 (i2i, a partir de `produto_kit.webp`) e os vídeos com MiniMax H3 Max (i2v, 5 s, 768P, 9:16). Os vídeos saem em 24 fps e a montagem converte para 30 fps.
**Voz:** clone "PODADORA venc-B narradora" `57OUoWWIdEbPrxk0T02A`, com `eleven_multilingual_v2` e tom mexicano.

## Entregas

| Arquivo | Narração / texto na tela | Takes do gancho | Gancho | Total | MB |
|---|---|---|---|---|---|
| `H1 - LA-ORILLA-IMPOSIBLE-B-ES-CL.mp4` | "La orilla que nadie quería limpiar… quedó perfecta." / ORILLA PERFECTA | H1a 0–4,2 s: close baixo da máquina rodando rente à guia de concreto, aparando o mato da beira (a câmera acompanha) | 4,20 s | 39,07 s | 24,5 |
| `H2 - VISTA-DE-DRON-B-ES-CL.mp4` | "Así se ve el patio desde arriba… antes y después." / LA DIFERENCIA 😮 | H2a 0–4,2 s: vista de drone de cima, metade do quintal com mato alto e metade cortada, mulher de chapéu empurrando a máquina na linha de corte, drone subindo | 4,20 s | 39,07 s | 23,5 |
| `H3 - SIN-CABLES-B-ES-CL.mp4` | "Sin cables, sin bencina… y llegas a todo el patio." / SIN CABLES | H3b 0–4,3 s: gramado enorme com a casa lá no fundo, mulher (de costas/corpo) cortando, faixa cortada atrás e nenhum fio | 4,30 s | 39,13 s | 23,4 |
| `H4 - CAMBIO-DE-BATERIA-B-ES-CL.mp4` | "Se acaba una batería… pones la otra y sigues." / 2 BATERÍAS 🔋 | H4a 0–2,8 s: mãos encaixando a bateria 21V embaixo da empunhadura, com a 2ª bateria na grama → H1a 1,0–2,5 s: a máquina volta a cortar na beira ("y sigues") | 4,30 s | 39,13 s | 24,7 |
| `H5 - MAMA-TAMBIEN-PUEDE-B-ES-CL.mp4` | "Con ruedas y liviana… hasta tu mamá la usa sola." / LIVIANA Y CON RUEDAS | H5a 0–4,2 s: mulher de ~50 anos sorrindo de boca fechada, sem falar, empurrando a máquina sobre as rodas num quintal simples | 4,20 s | 39,07 s | 24,2 |

Todos saem em 720x1280, 30 fps, H.264 + AAC, abaixo de 30 MB e decodificando sem erro. Nenhum gancho tem rosto falando: a mulher do H5 aparece sorrindo, sem fala e sem lipsync.

## Custos

| Gancho | Flora: imagens | Flora: vídeos | Flora total | TTS (caracteres) |
|---|---|---|---|---|
| H1 | 1 × 0,108 (2K) | 1 × 0,48 | **US$ 0,588** | 51 |
| H2 | 0,108 (reprovada) + 0,072 (1K) | 1 × 0,48 | **US$ 0,660** | 35 + 49 (refeita mais longa) |
| H3 | 0,108 (reprovada) + 0,072 (1K) | 2 × 0,48 (1º reprovado) | **US$ 1,140** | 50 |
| H4 | 1 × 0,108 | 1 × 0,48 (+ 1,5 s reaproveitados do H1a) | **US$ 0,588** | 45 |
| H5 | 1 × 0,108 | 1 × 0,48 | **US$ 0,588** | 48 |
| **Total** | 7 imagens, US$ 0,684 | 6 vídeos, US$ 2,88 | **US$ 3,564** (teto US$ 9) | 278 car. ≈ **US$ 0,046** |

Obs.: o Nano Banana 2 em 2K cobrou **US$ 0,108**, e não os US$ 0,072 do briefing, que é o preço em 1K. As 2 refações já foram feitas em 1K. Não usei crédito do HeyGen.

## Revisão dos takes (folha de quadros de cada clipe, em `_vencedores/B/fora/takes/*_folha.jpg`)
- **H1a: aprovado.** Máquina fiel à foto: cabeça verde-limão, protetor preto, disco de serra dentado, 2 rodas de cubo verde e haste telescópica. No fim do clipe entram pernas de uma pessoa (sem rosto). O disco aparece liso em alguns quadros por causa do borrão de rotação.
- **H2 imagem 1: reprovada**, porque o gramado parecia um canteiro de madeira artificial. **H2b + H2a: aprovados.** A máquina é pequena no quadro, mas a cor e a forma batem. A linha de corte quase não avança; o efeito "antes e depois" vem do contraste das duas metades.
- **H3 imagem 1: reprovada**, porque a mulher segurava uma segunda empunhadura solta, como se a máquina estivesse partida em duas. **H3b imagem: aprovada.** **1º vídeo: reprovado**, porque aparecia uma linha escura parecida com um fio saindo da saia/mão, o que contradiz "SIN CABLES". **Refação (H3b, seed 4242): aprovada**, sem nenhum fio e com a máquina inteira e consistente.
- **H4a: aprovado no trecho 0–2,8 s.** As mãos aparecem normais (5 dedos) e as baterias "21V SEESE" ficam iguais à foto. Os últimos ~0,8 s do clipe foram descartados, porque o texto SEESE vira garrancho e a máquina levanta.
- **H5a: aprovado.** Máquina fiel, rodas carregando o peso e sorriso sem fala.

## Revisão dos vídeos (`revisar_ad.py` pelo PowerShell, `--proibidos _vencedores/B/proibidos.txt` em UTF-8, `--passo 1`)
- **Termos proibidos** (precio, pesos, lucas, dólares, $+número, gratis, garantía, tiktok, link): **nenhum**, em H1–H5.
- **Whisper (es) do gancho:** H1 "La orilla que nadie quería limpiar, quedó perfecta."; H2 "Así se ve el patio desde arriba, antes y después."; H3 "Sin cables, sin vencina [bencina], y llegas a todo el patio."; H4 "Se acaba una batería, pones la otra y sigues."; H5 "con ruedas y liviana hasta tu mamá la usa sola". **Nenhuma frase foi cortada.** Cada fala termina pelo menos 0,4 s antes da emenda.
- **Decodificação:** OK. **Saltos de pts no áudio:** nenhum. **Quadro solto** (cortes a menos de 0,3 s): nenhum.
- **Emenda quadro a quadro** (6 antes e 6 depois): `_vencedores/B/fora/revisao/emendas_quadro_a_quadro.jpg`. O corte interno do H4 (2,8 s) está em `H4_corte_interno.jpg`. Todos os cortes estão limpos, e a caixa de texto some junto com o gancho.
- **"PROBLEMA: silêncio de 4,25 s no fim"** aparece em todos. Vem do próprio vencedor (moça sorrindo em silêncio), igual no B0–B6, e foi mantido porque o corpo não pode ser alterado. O aviso "sem setas" também é esperado, porque o original não tem setas.
- Relatórios e folhas de cada vídeo: `_vencedores/B/fora/revisao/*_revisao.txt` e `VENCEDORES/FORA/*_revisao.jpg|_frames.jpg`.

## Decisões e pontos para revisar
- **Textos ajustados em relação às ideias de partida:**
  - H2: "Mira la diferencia desde arriba" virou "Así se ve el patio desde arriba… antes y después", para não emendar "Mira… / Mira, dos baterías".
  - H1: "quedó perfecta" no lugar de "mira cómo quedó", pelo mesmo motivo.
  - H5: "Mi mamá la usa sola…" virou "Con ruedas y liviana… hasta tu mamá la usa sola", para não soar como depoimento real inventado (regra do Meta).
- **"Liviana"**, no H5, e **"llegas a todo el patio"**, no H3, são afirmações das ideias aprovadas. O peso e a autonomia **não aparecem na foto do kit** e precisam de revisão manual.
- **Encaixe da bateria (H4):** a IA colocou a bateria embaixo da empunhadura traseira. A foto do kit não mostra a bateria montada, então **confira com o produto real**.
- **Marca SEESE:** aparece legível nas baterias e na empunhadura do H4 (close). Nos outros takes ela é pequena ou nem aparece.
- **Reaproveitamento:** 1,5 s do H1a entra também no H4 ("y sigues").
- **Projeto duplicado no Flora:** o outro agente (corpo A) criou um projeto com o mesmo nome no mesmo segundo (`prj_ns79qnwxfbn177wryzt64c8q698fxkg7`). Os takes do B estão em `prj_ns7fv2n485kqy6kr5pm6xbtxzd8fwy0w`. Nenhum foi apagado.
- **Repetição na emenda:** o corpo começa com "Mira, dos baterías…". No H4, que já falou de bateria, a palavra "batería(s)" se repete logo em seguida.

## Arquivos de trabalho
`_vencedores/B/fora/`: `montar_fora.py`, `img/` (imagens base + `lote*.jpg`), `takes/` (clipes + folhas), `voz/H1–H5.mp3|.txt|.alinhamento.json`, `trab/H*/` (visual e config de cada gancho) e `revisao/`.
