# AD 01: MENOPAUSIA ("Fingí con mi esposo…"), relatório

## Entregas
- Longo: `producao\AD 01 - LYMPHORIA-MENOPAUSIA-ES-LATAM.mp4`. 7:19 (439 s), 720x1280, 53 MB. Passa de 30 MB por ser longo; o finalizar usou 900 kbps.
- Curto: `producao\AD 01 CURTO - LYMPHORIA-MENOPAUSIA-ES-LATAM.mp4`. 1:25 (85,3 s), 24 MB.

## Custos
- Kling O1 Edit: 6 takes × US$ 0,706 = **US$ 4,24**, sem re-tentativas. Ficou dentro da previsão de ~6 cenas e abaixo do teto de 8.
- TTS ElevenLabs: 623 caracteres, ~US$ 0,10. São três peças: fim A (305), a fala trocada (36) e o fim B do curto (282).
- Voz: clone novo **tfFP4rfamffIqrVeBdL6** ("DRENAGEM AD01 narradora"). Nenhum clone antigo bateu com essa narradora: a maior semelhança foi 0,78. Nenhuma voz foi apagada.

## O que foi trocado
- **Corte** em 416,7 s, logo depois de "completamente viva" e antes de "Las gotas se llaman…". Saíram junto "en seis semanas" e o fim emocional sem oferta.
- **Fim** com a versão A (as 4 ervas já tinham sido citadas), selo de pagamento contra entrega e setas.
- **Parte sexual** suavizada, mantendo o drama:
  - O plano de 0–1,5 s, com a mulher sentada sobre o marido na cama, foi coberto pelo plano seguinte (o rosto do marido). A legenda é a mesma nos dois.
  - A fala "No fingí el sexo, fingí desearlo" virou "No fingí quererlo… fingí desearlo", com a voz clonada. A legenda queimada foi trocada para "no fingí quererlo".
- **Frasco Maya Verra:**
  - 6 cenas no Kling: 5:19, 5:22, 5:27, 5:33, 5:36 e 5:53. Todas foram conferidas: rótulo LYMPHORIA e rosto da personagem preservados.
  - A cena de 5:43 (frasco pequeno no espelho) foi corrigida com o `band_fix.py` do ad25, de graça.
  - A cena de 5:29 (frasco cortado na borda de baixo) teve a faixa desfocada, porque o `band_fix` falhou nela.
- Não havia preço, link, 60 dias, "hecho en EE.UU.", Ozempic nem TikTok na parte mantida.

## Versão curta (gancho, mecanismo, uso, prova, fim B)
Trechos do original: 0–14,3 s (gancho), 243,8–271,5 s ("no era solo vanidad… es desecho"), 326,4–335 s ("unas gotas… lo que la menopausia dejó atrapado"), 342,5–347 s ("semana dos…") e 353,2–359,3 s ("me quedé sin aire… las bolsas de los ojos se fueron").
- Os trechos saem do `parte1.mp4` já tratado, então nenhum Maya Verra volta.
- O fim é o B ("Se llama Lymphoria: cuatro hierbas…").
- Cada corte cai em fim de frase, conferido com o whisper.

## Bug encontrado (vale para os outros agentes)
O `encaixar_edit.py` do kit, na última etapa, copia de volta do original **qualquer pixel quase branco do quadro inteiro**, não só a faixa da legenda. Nos rótulos com letra branca isso traz de volta "MAYA VERRA" / "Mayaverra" por cima do take do Kling.
- Corrigi com uma cópia local, `ad01\encaixar_edit_faixa.py`, que limita essa cópia à faixa da legenda (0,62–0,90 da altura).
- O arquivo do kit **não** foi alterado. Recomendo aplicar a mesma linha lá e conferir os ADs já entregues que têm rótulo com letra branca.

## Revisão
- **Whisper (es) nos dois vídeos:**
  - Nenhum termo proibido encontrado: Maya Verra, 60 días, hecho en EE.UU., Ozempic, TikTok, COFEPRIS, cáncer, preço, link, "sexo".
  - O único alerta foi "después de los cuarenta y cinco", que é a idade da personagem e não garantia.
  - Os dois terminam em "Toca el botón de abajo y pide el tuyo".
- **Folhas de contato** (1 quadro a cada 2 s; no curto, também 1 a cada 1 s no miolo):
  - Nenhum rótulo Maya Verra legível, nenhuma cena sexual explícita, nenhum antes/depois com kg.
  - O fim não fica em silêncio: o RMS dos últimos 2 s é 0,078.
- Transcrições salvas junto dos vídeos (`*_transcricao.txt`).

## Para revisão manual
- No curto, a legenda queimada do 2º trecho ainda mostra "de raíz no era solo vanidad", enquanto a fala é "No era solo vanidad". Tentei trocar, mas a troca deixou borrão no queixo, então mantive a original.
- No curto, há ~0,25 s de legenda da frase seguinte nas emendas: o respiro entre os trechos tem a imagem andando e o áudio em fade.
- A fala trocada (2,37 s) entrou num espaço de 3,58 s e ficou a 0,85x, com um pouco de pausa. Vale ouvir.
- No longo, o gancho segue "Fingí con mi esposo… en cuanto terminamos", que é implícito e foi mantido como drama. Se o Meta reprovar, troque o gancho.
