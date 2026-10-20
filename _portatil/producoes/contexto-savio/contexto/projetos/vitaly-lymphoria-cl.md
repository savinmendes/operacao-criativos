# Vitaly → Lymphoria Chile (vídeos, imagens e lote enxuto Andromeda)

> Conversão dos criativos da marca Vitaly (da pessoa) para Lymphoria COD Chile, com suavização de claims, CTA "clean" e um lote enxuto por conceito. Abra ao continuar Lymphoria Chile ou ao definir o padrão de fim/CTA de COD.

## Contexto de uso
- **Frente:** COD Chile. **Produto:** Lymphoria (gotas de drenagem, 4 ervas), página chileverificada.com/products/lymphoria.
- **Oferta (texto do anúncio; nunca preço no vídeo/imagem):** Compre 1, Reciba 2 $34.990 · Compre 2, Reciba 4 $59.990 · Compre 3, Reciba 6 $79.990 · envío gratis · pagas al recibir · 90 días de garantía.
- **Marca Vitaly é da pessoa:** clonar voz e lipsync permitidos; a criadora do V09 autorizou o uso.
- **Pasta:** `Downloads\ADLIB-VITALY-CL\` — estudo por vídeo em `_estudo\VNN.md`; briefings em `_trabalho\BRIEFING-ESTUDO/PRODUCAO/ENXUTO-LYMPHORIA.md`; plano em `Produtividade com ia\02-relatorios\2026-10_cod_plano_andromeda-lymphoria-chile.md`.
- **Entregas:**
  - `LYMPHORIA-ES-CL\` (09–10/10/2026): 11 vídeos (V01, 05, 09, 10, 12, 14, 19, 22, 25, 26, 30); `SUAVIZADOS\` (V10, V19, V26) com `00-TROCAS.md`; `IMAGENS\` com 12 de 14 imagens (`RELATORIO.md`, `TROCAS.md`, `00-TEXTOS-LYMPHORIA.txt`; a 20 e a 29 não foram produzidas). Versão com CTA antigo guardada em `_versao-cta-antigo\`.
  - `LYMPHORIA-ENXUTO\` (10/10/2026): 8 vídeos — C1 trabalhadora em pé (avatar UGC + POV voz off), C2 drama (gancho × AD 30 e × AD 23 do lote Drenagem), C3 jubilada 60+ (avatar UGC + testemunho off), C5 desconfiada online / pago na porta (avatar UGC + montagem) — + 4 estáticos + `00-TEXTOS.txt` (botão SHOP_NOW, nome no Meta = nome do arquivo).
- **Fora do lote:** V17/V23/V24 (clorofila) apagados; **V03/V11** (nutricionista/médica com voz clonada) **bloqueados pelo filtro de segurança** — não produzir fala nova em profissional de saúde.
- **CTA padrão definido pela pessoa (10/10/2026):** sem preço, sem card colorido; 3 takes Lymphoria variados + legenda normal + selo amarelo pequeno "PAGO CONTRA ENTREGA" a partir de "pagas" + setas vermelhas a partir de "Toca" até o último quadro. Estudo em `_trabalho\prod\_cta_v2\ESTUDO-CTA.md` (baseado nos vencedores validados no TikTok).
- **Custos registrados:** imagens US$ 1,116 (Nano Banana 2; teto US$ 3,20); C1/C3: ElevenLabs ~US$ 0,70 + até 103 créditos HeyGen. Custo total do projeto: precisa de revisão manual.
- **Pendências:**
  - avatares C1-A/C3-A reprovados pelo `checar_lipsync.py` (1,25 / 1,57) — falso positivo (o Avatar IV sorri com dentes nas pausas; a UGC 01 aprovada do Drenagem também dá 1,01): conferir a olho;
  - C2-B (corpo do AD 23) tem claims fora do compliance;
  - V19: flash preto em ~19 s; antes/depois visual do corpo mantido (risco Meta);
  - verba diária de mídia não informada.

## Lógica de uso
1. **Estudo por vídeo:** whisper + OCR + folha; listar marca, oferta, claims e tempos de cada trecho a trocar.
2. **Troca de marca:** toda aparição de Vitaly (falada, escrita, rótulo) vira Lymphoria; frascos de outra marca viram Lymphoria ou são cortados/desfocados; URL vira "Toca el botón de abajo"; "2x1", "70% OFF", Cyber Day viram "Compre 1, Reciba 2"; garantias de 45/60 dias viram 90; cortar a camiseta política (V01 6–7 s, V25 10 s).
3. **Suavização (padrão adotado após o filtro bloquear "manter tudo"):** frase nova com o **mesmo sentido e o mesmo tempo** (±0,2 s), voz clonada de quem fala no mesmo LUFS, lipsync `mode speed` se o rosto fala; texto na tela por caixa opaca no mesmo estilo. Ex.: "Bajé 7 kilos" → "Me deshinché y bajé tallas"; "114 KG"/"84 KG" → "ANTES"/"DESPUÉS". Registrar cada troca em `00-TROCAS.md`.
4. **Fim/CTA:** padrão ESTUDO-CTA v2 acima; fala final "Se llama Lymphoria. Compre uno y reciba dos, con envío gratis, y pagas al recibir en tu casa. Toca el botón de abajo y pide el tuyo."; música a −32 LUFS sob a voz (−16); legenda pelo roteiro (alinhamento do ElevenLabs); troca de plano a cada 1,1–4 s.
5. **Lote enxuto (Andromeda):** 1 conceito = persona × ângulo, 2 execuções diferentes de verdade (ex.: avatar UGC × POV sem rosto). Avatares por prompt no HeyGen + B-rolls HeyGen Video 1 (créditos do plano), takes reais do lote Lymphoria conferidos contra texto queimado.
6. **Imagens:** Nano Banana 2 só para rótulo/elementos; textos redesenhados localmente (PIL/OpenCV), sem custo.
- **Se a pessoa pedir mais:** ler resultado por conceito (skill andromeda) e produzir a 2ª execução do conceito vencedor; nunca dar fala nova a profissional de saúde.

## Relacionados
- [../06-troca-de-marca.md](../06-troca-de-marca.md)
- [../09-lipsync-e-avatar-heygen.md](../09-lipsync-e-avatar-heygen.md)
- [../07-variacoes-gancho-corpo.md](../07-variacoes-gancho-corpo.md)
- [drenagem-latam.md](drenagem-latam.md), [lymphoria-adaptacao-ads.md](lymphoria-adaptacao-ads.md)
