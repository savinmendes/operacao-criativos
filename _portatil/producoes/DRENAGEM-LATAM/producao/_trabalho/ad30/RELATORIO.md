# AD 30 — Lymphoria "Exesposo en la fila" (origem: vídeo 30, Maya Verra Pixar, 6:33)

## Entregas
- Longo: `producao\AD 30 - LYMPHORIA-EXESPOSO-FILA-ES-LATAM.mp4` — 327,0 s (5:27), 720x1280, 39,5 MB (acima de 30 MB: o kit avisa que 5,4 min não cabe em 30 MB com qualidade e usou 900 kbps)
- Curto: `producao\AD 30 CURTO - LYMPHORIA-EXESPOSO-FILA-ES-LATAM.mp4` — 81,7 s, 720x1280, 23,6 MB

## O que foi feito
- Corte em 308,1 s, depois de "…lo que años de estrés dejaron atrapado" e antes de "Pero antes de probarlo tengo que advertirte algo" (conferido com whisper por palavra). Saiu: empresa pequeña/se agota, "hasta un 70% de descuento", "haz clic", "Emporio" (= Mayaverra falado), garantia de 30 dias.
- Fim (voz clonada da narradora): fim_A sem a frase "Unas gotas bajo la lengua cada mañana, y sabe a miel", que a narradora já tinha dito logo antes: "La marca que te da esas cuatro hierbas en las dosis correctas se llama Lymphoria. Pides ahora, te llega con envío gratis y pagas al recibir en tu casa. Y tienes noventa días de garantía o te devolvemos tu dinero. Toca el botón de abajo y pide el tuyo."
- 0 falas trocadas (a única menção à marca ficava depois do corte).
- Kling O1 Edit (nós n226, n232, n235, n227, n233, n236):
  - aproveitados: t1 packshot na mesa (4:27–4:32), t2 frasco com raízes (4:36–4:38), t5 fileira de frascos (5:01–5:04) e t6 mulher de blusa magenta com frascos no balcão (5:04–5:07). Em t5 e t6 o Kling refez o fundo e o enquadramento, mas cada take cobre a cena inteira, então não aparece emenda.
  - reprovados: t3 (roupão rosa, 4:43–4:48) e t4 (camiseta menta, 4:48–4:51), porque o Kling deixou a personagem fotorrealista. Nessas duas cenas a faixa "MAYA VERRA" foi trocada por "LYMPHORIA" com o `ad25\band_fix.py`, sem custo. O resultado ficou limpo.
- A legenda em caixa verde que o Kling apagou foi restaurada com `_trabalho\colar_caixa_verde.py`, que acha o texto verde no original e cola a caixa. O `encaixar_edit.py` padrão gerava artefatos brancos nessa legenda.
- 5:07–5:08 (frasco na mão, Maya Verra legível): coberto com o último quadro congelado do t6 (0,57 s).
- Curto: gancho 0–29,0 s ("…por fin entendí") + mecanismo 143,4–170,0 s ("Verás, cuando pasas años bajo estrés… Eso no es grasa, son residuos") + 187,5–189,6 s ("Sólo puedes drenarlos") + fim_B ("Se llama Lymphoria: cuatro hierbas…", porque no curto as ervas não são citadas). Nas junções, a legenda queimada da frase anterior ficava 0,1–0,4 s na tela; foi coberta com a legenda seguinte.
- Voz: clone novo "DRENAGEM AD30 narradora" `x7Q3zqDG9jz6G8aiQCio`. É a mesma atriz do AD 08/21/22 antigos (semelhança 0,93–0,96), mas não havia clone dela tirado de amostra deste vídeo. Ficaram cerca de 33 vagas livres de 160, e nenhuma voz foi apagada.

## Custos
- Kling: 6 takes × US$0,706 = US$4,236 (teto do AD: 7)
- TTS: 251 (fim longo) + 282 (fim curto) = 533 caracteres (≈ US$0,09)

## Revisão
- Whisper (es) no longo e no curto: nenhum termo proibido (Maya Verra, Emporio, 70%, 30 días, link, preço…).
- Folha de contato 1 quadro/2 s: rótulos Lymphoria em todas as cenas de produto, sem cena sexual e sem antes/depois com kg (a balança em 1:00 não mostra número). Fim com selo COD e setas até o último quadro.

## Para revisão manual
- Tamanho do longo: 39,5 MB, acima do limite de 30 MB do kit.
- Frascos pequenos ao fundo (4:25 cozinha, 4:35 na mão, 4:54 balcão, 4:57–5:00 mesa do parque) ficaram com o rótulo original: a faixa da marca não é legível nesse tamanho.
- Mantidos do original: "diez años más joven", antes/depois de semanas 1/3/6 (sem kg), vestidos decotados (4:00–4:24) e "decenas de miles de mujeres como yo". Risco Meta médio-alto, já apontado na análise G6.
