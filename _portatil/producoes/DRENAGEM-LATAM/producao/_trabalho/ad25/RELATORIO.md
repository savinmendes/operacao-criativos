# AD 25 — Lymphoria "VECINO" (Maya Verra masculino, Pixar)

**Arquivos**
- Longo: `producao\AD 25 - LYMPHORIA-VECINO-ES-LATAM.mp4` — 4:59 (298,9 s), 720x1280, 36,1 MB (acima de 30 MB: o finalizar baixou para 900 kbps)
- Curto: `producao\AD 25 CURTO - LYMPHORIA-VECINO-ES-LATAM.mp4` — 1:12 (71,7 s), 24,4 MB

**Custos**
- Kling O1 Edit: 8 takes × US$ 0,706 = US$ 5,65 (teto = 6 + 2). Só 2 entraram no vídeo (t1 de 126,8 s e t4 de 168,2 s). t2, t3, t5 e t6 saíram fotorrealistas ou com outro rosto, e as 2 re-tentativas (t3 e t5 v2) mudaram o rosto.
- Os 4 takes reprovados foram resolvidos de graça com `ad25/band_fix.py`: ele acha a faixa verde do rótulo quadro a quadro, apaga "MAYA VERRA" e escreve "LYMPHORIA" no mesmo ângulo. O personagem não muda nenhum pixel.
- TTS (voz clonada `IUEkf483KpgC9tyWn70n`, "DRENAGEM AD25 narrador", clone novo porque nenhum clone existente passou de 0,75 de semelhança): 83 + 305 + 282 = 670 caracteres (~US$ 0,11)

**O que foi tirado ou trocado**
- Corte em 279,2 s, depois de "Esa acumulación no se quema, se drena". Saíram "Gotas de drenaje linfático mayaverra", "60 días de garantía" e "lotes pequeños".
- Longo com fim_A (as 4 ervas já tinham sido citadas). Curto com fim_B.
- Fala trocada em 167,9–173,75 s: "Se llama mayaverra… Tienes 60 días" virou "Se llama Lymphoria. Pruébalo. Si no te funciona, lo devuelves. Tienes noventa días."
  - Não havia legenda queimada nesse trecho.
- Rótulo Maya Verra trocado em 6 cenas: 126,8 / 143,1 / 149,6 / 168,2 / 174,1 / 175,5 s.
- Mantidos: libras (14 e 19), o ângulo de ciúme e "no me quita las manos de encima".

**Curto:** gancho 0–6,45 + trechos 36,8–46,6 / 48,4–59,05 / 83,2–89,0 / 112,2–116,2 / 198,1–206,35 / 231,5–235,25 + fim_B.

**Revisão**
- Whisper (es, vad off) nos 2 finais: nenhum "Maya Verra", "60 días", TikTok, Ozempic, preço ou link. Só aparece "90 días de garantía" no fim universal.
- Folhas de contato em `producao\_revisao\`: sem rótulo Maya Verra legível e fim com setas até o último quadro.

**Revisão manual**
- Restam relances de frasco pequeno e ilegível em 142,3 s (desfocado em primeiro plano), 146 s, 164 s e 179 s.
- Cenas de torso nu: em 3:24–3:28 ele aparece de cueca, de costas, e em 3:30 levanta a camiseta e mostra o abdômen. Isso coincide com a fala das libras: avaliar o risco de "antes/depois" no Meta.
- Fala anti-TRT ("No necesitas más hormonas") mantida.
- Semelhança da voz clonada: 0,86.

## Correção 05/10 (bug do encaixar_edit.py)
- t1 tinha uma mancha branca no fundo em 3 quadros (cerca de 128,2 s), sem letras do rótulo. No t4 a diferença era desprezível.
- Mesmo assim os dois foram re-encaixados com `encaixar_edit_faixa.py`, e o AD foi remontado com `processar_ad.py r25.json` e `curto.py`. Os band_fix (t2/t3/t5/t6) não dependem do encaixar e foram reaproveitados.
- O CURTO não contém os takes do Kling e ficou visualmente idêntico.
- Revisão: decodificação OK; duração igual (298,90 s e 71,69 s); áudio idêntico. Versões antigas em `ad25/_antes_fix_faixa/`.
