# Podadora inalámbrica (COD Chile)

> Lote da podadora/desbrozadora sem fio com rodas: traduções EN→ES-CL, matriz gancho × corpo, estáticos e, depois, variações sobre os 2 vencedores. Abra ao continuar esse produto ou como exemplo-base do fluxo de tradução e de variação.

## Contexto de uso
- **Frente:** COD Chile. **Produto:** "Podadora Inalambrica Cesped Ruedas" (desbrozadora 3 en 1 com rodas, 2 baterias de 21V; marca **SEESE** impressa nas baterias e na máquina).
- **Oferta confirmada pela pessoa:** pago contra entrega, despacho gratis, 90 días de garantía. **Sem preço** no criativo.
- **Pasta:** `Downloads\PODADORA-CL\` (atalho `entregas-podadora/`). Textos em `TEXTOS-ANUNCIOS-PODADORA-CL.txt` e `PARA-O-DRIVE\`.
- **Fase 1 — entregue em 04/10/2026:**
  - AD 01–04: tradução dos originais em inglês (voz clonada do narrador A = 01/02, B = 03/04; música separada com demucs local);
  - AD 05–12: matriz de 4 ganchos (JARDINERO, PERRO, AUMENTO, DEVOLVER) × corpos (A FUNCIONES, B CUCHILLA, C KIT);
  - estáticos em `estaticos\`: feed 4:5 01–07 + carrossel 1:1 1–4;
  - `SELECAO-C1-C4-C10\`: seleção com os ADs 01, 04 e 10.
- **Fase 2 — vencedores, 08/10/2026** (`VENCEDORES\`):
  - **Vencedor A "DEVOLVER"** = AD 04 (corte em 9,000 s). A0 (1080p sem mudança) + A1–A6 (ganchos novos). Voz clone do narrador B `BgvvJ0I0R4tg6uf8DolY`. Relatório `RELATORIO-A.md`.
  - **Vencedor B "ORILLA"** = `_vencedores\vencedor1.mp4` (vídeo da operação, narradora com tom mexicano, 576x1024; corte em 2,100 s). B0 (1080p) + B1–B6. Voz "PODADORA venc-B narradora" `57OUoWWIdEbPrxk0T02A`. Relatório `RELATORIO-B.md`.
  - **"Fora da caixa"** (`VENCEDORES\FORA\`): F1 ASMR, F2 duelo com roçadeira a bencina (tela dividida), F3 vizinha fofoqueira (avatares HeyGen), F4a/b/c "respondiendo al comentario", F5 presente para o pai, F6 kit explodido, G1–G5 (ganchos com takes IA sobre o corpo A), H1–H5 (ganchos sobre o corpo B). Relatórios `RELATORIO-F1-F4.md`, `-F2F6.md`, `-F3-F5.md`, `-G.md`, `-B-H.md`; briefings em `_vencedores\BRIEFING-VENCEDORES.md` e `BRIEFING-FORA-DA-CAIXA.md`.
  - Takes IA: projeto Flora "PODADORA CL - takes IA (2026-10-08)" `prj_ns7fv2n485kqy6kr5pm6xbtxzd8fwy0w` (Nano Banana 2 a partir de `produto_kit.webp` + MiniMax H3 Max i2v). Gasto do agente F2/F6 no Flora: US$ 1,20; F1/F4 sem custo de IA.
- **Custo total do projeto:** precisa de revisão manual (cada relatório traz o seu; não há soma única).
- **Pendências:**
  - marca SEESE visível nas baterias/máquina: a pessoa ainda não disse se é problema;
  - vencedor B tem 4,25 s de silêncio no fim (moça sorrindo), mantido pela regra do corpo intacto; decidir se corta (~3,6 s) nas próximas versões;
  - textos do anúncio das variações de vencedor não foram feitos (o briefing não pediu).

## Lógica de uso
- **Tradução (AD 01–04):** transcrever (faster-whisper) e ler a tela (RapidOCR) → reescrever o roteiro para o Chile sem preço estrangeiro → voz clonada do narrador → demucs `--two-stems=vocals` e usar só `no_vocals.wav` → cobrir texto queimado com faixa quase opaca (alpha ≥ 250) e aviso em espanhol no rodapé → `montar_ad.py`. Era o `preparar_corpo.py` daqui; hoje é `preparar_corpo_traducao.py` do kit.
- **Matriz gancho × corpo (AD 05–12):** `_variacoes\gerar_variacao.py NN Hx X` sobre o banco de tomadas `_variacoes\banco.json` (margem nas bordas de cada tomada, grupos de cena contínua, sem repetir pedaço da mesma cena; a mesa espelhada da v2 ficou excluída). Hoje o equivalente é `gerar_variacao.py banco/fundo/montar` do kit.
- **Estáticos:** quadros reais do vídeo via `_variacoes\est\gerar_estaticos.py`.
- **Variações de vencedor (regra fixa): corpo e CTA ficam exatamente como estão.**
  1. Achar o corte no fim do gancho original, em fim de frase pela transcrição por palavra, dentro de uma tomada contínua.
  2. Gancho novo de 3–6 s: narração com a voz clonada do próprio narrador (volume igualado ao LUFS do corpo), visual de cenas do próprio vencedor ou da foto do kit (zoom lento), **sem rosto falando** (só avatar com lipsync próprio), caixa branca grande do kit (Poppins Bold, cy≈240 em 1280).
  3. Música do gancho = o próprio áudio do vencedor antes do corte (só música) ou o `no_vocals` do demucs, para emendar sem pulo.
  4. Scripts: `_vencedores\A\montar_gancho.py A3`, `_vencedores\B\montar_ganchos.py`, `_vencedores\B\fora\montar_fora.py`, `_vencedores\FORA\F1F4\montar_F1F4.py F4b`.
  5. Versão 1080p do vencedor original com `upscale_video.py` (Real-ESRGAN, GPU local). As variações ficam em 720x1280 (não subir resolução do corpo).
  6. Revisão: `revisar_ad.py` pelo PowerShell com proibidos em `.txt` UTF-8 (preço, "gratis" fora do selo, garantia não confirmada, TikTok, "link") + folha de 1 em 1 quadro na emenda.
- **Regras de conteúdo:** não inventar recurso que não está na foto `produto_kit.webp` ou no vídeo; máquina gerada por IA igual à foto; antes/depois de gramado pode; sem depoimento inventado como real; sem preço.
- **Se a pessoa pedir mais:** ler os resultados dos A/B/F/G/H no Meta e seguir com o gancho vencedor; pacote de ângulos ainda não feito: sênior, economia, comparação, lista; ganchos IA só se os atuais cansarem.

## Relacionados
- [../05-traducao-de-criativos.md](../05-traducao-de-criativos.md)
- [../07-variacoes-gancho-corpo.md](../07-variacoes-gancho-corpo.md)
- [../04-fluxo-producao-criativos.md](../04-fluxo-producao-criativos.md)
- [wyze-solar-cam-latam.md](wyze-solar-cam-latam.md) (mesmo fluxo EN→ES), [mopa-h2o-x5-es.md](mopa-h2o-x5-es.md)
