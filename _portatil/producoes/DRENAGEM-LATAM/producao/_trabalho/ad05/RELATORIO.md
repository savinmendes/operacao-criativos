# AD 05 — Lymphoria "Esposo no me miraba" (origem: originais/05.mp4, Maya Verra Pixar, 5:18)

## Entregas
- Longo: `producao/AD 05 - LYMPHORIA-ESPOSO-NO-ME-MIRABA-ES-LATAM.mp4`: 4:58 (298,4 s), 720x1280, 35,7 MB (o vídeo de 5 min não cabe em 30 MB sem perder qualidade).
- Curto: `producao/AD 05 CURTO - LYMPHORIA-ESPOSO-NO-ME-MIRABA-ES-LATAM.mp4`: 88 s, 720x1280, 24,6 MB.

## Gancho novo (o sexual saiu)
- O trecho 0:00–0:42 do original saiu inteiro: sexo, lingerie, "no pudo", "camisa puesta".
- O gancho novo dura 15 s, no mesmo ângulo (marido perdeu o interesse / traição). A narração usa a voz clonada:
  > "Vi a mi esposo almorzando con una compañera de trabajo... y por fin entendí por qué ya no me miraba. Veintidós años casados. Llegaba tarde, el teléfono siempre boca abajo... y apagaba la luz antes de que yo entrara al cuarto."
- As cenas são todas do próprio vídeo: restaurante com a colega, rosto dela, casamento, ele saindo, celular virado e abajur.
- A legenda antiga foi apagada por inpaint, e entrou legenda nova no estilo drop. A manchete "¿POR QUÉ MI ESPOSO YA NO ME MIRABA? 💔" fica nos primeiros 4,2 s.
- Depois do gancho, o vídeo segue do original em "Nunca dije una palabra" (42,26 s). A legenda "puesta. Nunca dije..." foi trocada por "Nunca dije una palabra".

## O que foi trocado no corpo
- Fala "El líquido parecía miel, MayaVerra" → "…miel. Lymphoria." (voz clonada + legenda).
- "Le dije: MayaVerra" → "Le dije: «Lymphoria»" (voz + legenda). A legenda "Berra». Ella sacó su teléfono" foi corrigida.
- "No dejes que te vendan Ozempic" → "No es tu culpa, no es falta de voluntad" (voz + 2 legendas).
- Corte antes de "Sabe a miel / 70% de descuento / 30 días de garantía / se agotan": o vídeo é cortado em 300,4 s do original. Depois entra o fim universal **A**, porque a narração acabou de citar as 4 ervas.
- Mantidos: "diecinueve libras" (conforme o briefing) e o drama de traição.

## Kling (Flora, isv2v-kling-o1-edit, ref. n59)
7 takes × US$ 0,706 = **US$ 4,94** (teto = 7):
| Take | Trecho (original) | Resultado |
|---|---|---|
| t1 | 96,8 s, mão pondo o frasco | O Kling trocou a estampa da manga. Só a região do frasco foi colada sobre o original (caixa que acompanha o frasco). Em 0,3 s de movimento borrado entrou desfoque do rótulo. |
| t2 | 99,2 s, frasco no balcão | OK |
| t3, t4 | 119,9 s e 120,7 s, frasco no mármore | OK |
| t5 | 121,7 s, ela segurando o frasco/conta-gotas | O Kling deixou o rosto fotorrealista. Só a região do frasco foi colada sobre o original: rosto Pixar intacto, rótulo Lymphoria. |
| t6 | 124,7 s | **Desperdiçado:** cena errada (espelho, sem frasco), descartado. US$ 0,706 perdidos. |
| t7 | 249,2 s, frasco ao sol | OK |

Frasco pequeno e ilegível em 1:41–1:44 e 1:58 do original: mantido.

## Voz (ElevenLabs)
- Clone novo: `BCCHRwYb332ahRN0gT7H` ("DRENAGEM AD05 narradora").
  - Nenhum clone antigo passou de 0,76 de semelhança. O clone novo ficou em 0,82.
- TTS: gancho 225 + fim A 305 + falas 94 + fim B do curto 282 = **906 caracteres (~US$ 0,15)**.

## Curto (88 s)
Gancho novo, depois:
- "Así que culpé a mi cuerpo… mandíbula";
- irmã + frasco + mecanismo ("no estás gorda… tienes que drenarla");
- "Semana cinco… vestido… perfecto";
- fim universal **B** ("Se llama Lymphoria: cuatro hierbas…"), porque o curto não cita as ervas.

A legenda da emenda foi corrigida para "Entonces mi hermana".

## Revisão
- Whisper (es) no longo e no curto: nenhum Maya Verra, Ozempic, 60/30 días, sexo, TikTok, preço ou link. O nome sai transcrito como "linforia".
- Folhas de contato (1 quadro a cada 2 s):
  - nenhum rótulo Maya Verra legível;
  - nenhuma cena sexual;
  - o fim termina em fala, com no máximo 0,7 s de silêncio.

## Revisão manual
- Vestígios leves da legenda antiga apagada sob a legenda nova do gancho, em quadros claros (vestido de noiva).
- A frase original "el teléfono, las luces, la camisa" (2:39 no longo) ficou: é só uma referência, sem conteúdo sexual.
- Libras mantidas. Se for rodar no Chile, pode valer uma versão em kg.
- Arquivo do gancho: `ad05/hook_final.mp4`, reaproveitável na matriz de ganchos.

## Correção 05/10 (bug do encaixar_edit.py: branco copiado fora da faixa da legenda)
- Afetados: t1, t3, t4, t5, t7. Apareciam letras do rótulo antigo ("LYMPHERRA", restos de "MAYA" e "VERRA") por cima do Kling. O t2 tinha só um filete na borda e foi refeito junto.
- Takes re-encaixados com `ad01/encaixar_edit_faixa.py`. O t1 passou de novo por `comp_movel` + `blur_movel` (b1.json) e o t5 por `comp_regiao`, com os mesmos argumentos. Depois rodaram `orq.py r05.json --so-parte1`, `fix_puesta.json` e `montar_fim_universal`.
- CURTO: `curto2.py` com os trechos finais 47.95-54.75 88.05-123.40 146.35-155.30, depois `fix.json`.
- Revisão: decodificação OK; duração igual (298,20 s e 87,80 s); áudio idêntico ao entregue (md5 do PCM); fora dos takes a imagem é igual. Zoom 3x conferido: rótulo limpo.
- Versões anteriores em `ad05/_antes_fix_faixa/`. Script: `_trabalho/refazer_faixa.sh ad05`.
- Revisão manual: no t1 o próprio Kling escreveu "LYMFIORIA". Isso vem do `_edit` e não desse bug.
