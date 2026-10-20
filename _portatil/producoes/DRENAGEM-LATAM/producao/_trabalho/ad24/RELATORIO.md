# AD 24 — Lymphoria "HOMBRE-40" (Maya Verra masculino, Pixar; = AD 18 antigo)

**Arquivos**
- Longo: `producao\AD 24 - LYMPHORIA-HOMBRE-40-ES-LATAM.mp4` — 6:48 (408,3 s), 720x1280, 48,6 MB. Passa de 30 MB: o finalizar usou 900 kbps, como no AD 25.
- Curto: `producao\AD 24 CURTO - LYMPHORIA-HOMBRE-40-ES-LATAM.mp4` — 1:28 (88,1 s), 23,8 MB
- Folhas de revisão: `producao\_revisao\ad24\`. Transcrições finais: `producao\AD 24*_transcricao.txt`

**Custos**
- Kling: 0 takes, US$ 0. Os 7 planos com o rótulo legível foram trocados de graça:
  - `band_fix3.py` é uma evolução do `ad25/band_fix.py`. A região de busca tem chaves por quadro. A faixa é preenchida na largura toda do rótulo, com a cor de fundo coluna a coluna. O ângulo é corrigido e o movimento suavizado no tempo.
  - `band_box.py` serve para os planos quase parados.
  - O personagem fica intacto.
- TTS com a voz clonada `jKbwZXxLCZofPlbZNKNw`, reaproveitada do AD 13 antigo. O narrador é o mesmo: semelhança de 0,92 com o original do AD 13; o fim gerado ficou entre 0,75 e 0,79. Nenhum clone novo.
  - Caracteres: fim_A com 305 + fim_B com 282 = 587 (~US$ 0,10).
- Transcrição: demucs (só a voz) + faster-whisper small. O trecho com música tinha derrubado a transcrição antiga depois de ~5 min.

**Corte do longo (12:56 → 6:48)**, segmentos do original, em segundos:
- 0–71,56: gancho, flagra, espelho, "20 años siendo el hombre…".
- 79,2–136,1: turnos dobles, 30 libras, invisible.
- 149,95–157,0: "fui a mi doctor… es la edad, tienes 47".
- 166,08–371,88: irmão Miguel, frasco, "no es grasa", 4 ervas, dose, "semana uno… el reloj".
- 440,25–444,88: "por primera vez en años volví a sentirme yo".
- 645,17–684,43: "yo pensé que me dejó porque estaba viejo… el hombre que ella debió haber tenido miedo de perder".
- Depois entra o fim_A (as 4 ervas já tinham sido citadas).

**Curto:** 0–22,63 (gancho) + 204,5–217,34 (frasco, "parecía miel") + 260,37–273,42 ("no tienes un problema de peso… desechos atrapados") + 284,48–300,15 (mecanismo: "eso no es grasa, es todo lo que has estado cargando") + fim_B.

**O que foi tirado ou trocado**
- Saíram:
  - "75 hard" e as pastilhas de testosterona;
  - "baja diez libras o empieza terapia de testosterona";
  - "14 libras menos" e "19 libras menos", e o torso transformado junto;
  - "las ganas de vuelta";
  - o casamento inteiro, com a tela do celular "MAYAVERRA" (9:40);
  - o pitch final original: escassez, "garantía de reembolso de 60 días" e loja no celular.
- Rótulo MAYAVERRA → LYMPHORIA em 7 planos: 209,23 / 213,3 / 244,1 / 302,97 / 342,3 / 664,27 / 677,93 s.
  - Os frascos pequenos ficaram como estavam: a marca não dá para ler, e vários já têm o rótulo "Lymphoria · lymphatic drainage" do próprio original.
- Legenda queimada ajustada nas emendas:
  - 166,0 s e 645,1 s: colada a caixa da frase correta;
  - 440–442,8 s: "las ganas de vuelta por primera vez en años" virou "por primera vez / en años".
- Mantidos: libras ("30 libras más pesado", "subí 30 libras"), traição/flagra (casal coberto na cama, sem cena explícita), "clínica brasileña de drenaje linfático".

**Revisão**
- Whisper (es, sem VAD) nos 2 finais: nada de Maya Verra, 60 días, hecho en EE.UU., Ozempic, TikTok, COFEPRIS, câncer, preço ou link. A fala vai até o último segundo, sem silêncio no fim (-22/-24 dB no último 1,5 s).
- Folhas a cada 2 s:
  - nenhum rótulo Maya Verra legível;
  - nenhum quadro solto nas emendas, que caem longe dos cortes de cena;
  - setas e selo até o fim.

**Para revisão manual**
- Corpo:
  - 1:24 (longo): protagonista sem camisa mostrando a barriga ("30 libras más pesado");
  - 3:20–3:22 (longo): homens musculosos sem camisa ("los veteranos del barrio").
  - Avaliar o risco de "corpo/antes-depois" no Meta.
- Emenda em 2:15 do longo: "tienes 47 | esa misma semana" sai sem pausa (as palavras estão inteiras; o whisper ouviu "claro" no meio). A legenda em 2:14 ainda mostra "tienes 47 baja".
- Curto: nos primeiros ~0,8 s do trecho do mecanismo a legenda queimada diz "de pie tu cuerpo se". No fim do corpo aparece "no lo puedes quemar" sem fala.
- Plano 302,97 s (frasco pequeno na mão, ~quadro 30): leve fantasma da faixa antiga por ~0,3 s.
