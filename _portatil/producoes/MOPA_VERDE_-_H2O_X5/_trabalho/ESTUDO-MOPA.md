# Estudo de tradução: lote MOPA VERDE (H2O X5), EN → espanhol neutro LATAM (COD)

Data: 08/10/2026. Nenhuma API paga foi usada (ElevenLabs, Flora, HeyGen e Vmake não foram chamados). Os originais não foram alterados.

## Decisões da dona (aplicadas neste estudo)
- **A marca "H2O X5" fica em tudo**: na fala, no texto da tela, no aparelho, na caixa e no logo. Ela vende o próprio H2O X5 (página `h2oforyou.co.uk/products/h2o-x5-steam-cleaner-tvpr`). Por isso **não há troca de marca nem edição paga de logo**.
- Especificações oficiais usadas para conferir os claims:
  - 1300 W, 5 em 1, aquece em menos de 30 s, pesa menos de 5 lb (≈2,3 kg);
  - elimina 99% de bactérias, vírus e germes com 15 s de aplicação;
  - 30 dias de garantia de devolução do dinheiro e 2 anos de garantia.
- Os claims ficam como estão: "$55 OFF", "14 million sold", "kills 99%" e "making you sick".
- **Sai apenas o "USE CODE: FBX5"**.
- CTA: "Haz clic en Más información". Selo COD: "Pago contra entrega".

## Arquivos gerados (`_trabalho/`)
| Pasta/arquivo | Conteúdo |
|---|---|
| `transcricoes/<id>.json` | Transcrição palavra a palavra (faster-whisper medium, CPU, en). O 44 não tem faixa de áudio (registrado como erro). |
| `folhas/<id>_folha.jpg` | Folha de contato, 1 quadro/s, com o segundo marcado. `imagens_folha.jpg` mostra as 12 imagens. |
| `frames/<id>/` | Quadros a 1 fps em resolução cheia. |
| `ocr/<id>_ocr.json` | OCR dos vídeos (1 fps), com o texto, o intervalo `ini–fim` (s), a caixa `x0,y0,x1,y1` e a flag `marca_ou_alerta`. O `07_ocr_4fps.json` é uma passada extra a 4 fps. |
| `ocr/img_<id>_ocr.json` | OCR das imagens, com caixa, `marca_ou_alerta` e `remover` (FBX5). |
| `audio/<id>_no_vocals.wav` | Fundo sem voz (demucs htdemucs, `--two-stems=vocals`) para 07, 16, 17, 24, 25, 31, 32, 46 e 60. As faixas `vocals.wav` ficam em `audio/demucs/htdemucs/<id>_orig/`. |
| `audio/voz_<id>.wav` | Amostra só de voz, sem silêncios, mono, −18 LUFS, para clonar: uma por narração distinta. |
| `roteiros/<id>_es.txt` | Roteiros em espanhol neutro (07, 16, 24, 25 e 31). |
| `transcrever.py`, `ocr.py`, `folha.py` | Scripts usados, para refazer o processo. |

Observação técnica: o faster-whisper na GPU falhou (`cublas64_12.dll` ausente) e o torch está sem CUDA. Por isso whisper, OCR e demucs rodaram na CPU, em sequência.

---

## 1. Duplicatas
| Grupo | Versões | Como foi confirmado | Usar como base |
|---|---|---|---|
| A | **07** (720×1280) = **60** (720×900, 4:5) | Mesmo roteiro palavra por palavra, mesmos planos e textos, timbre quase idêntico (distância MFCC 12) | **07** (9:16) |
| B | **16** (720×900) = **32** (720×1280) | Mesmo roteiro e planos (MFCC 10) | **32** (9:16) |
| C | **31** (720×900) = **46** (720×1280) | Mesmo roteiro e planos (MFCC 4) | **46** (9:16) |
| D | **10** = **15** (720×900) | Quadros idênticos (diferença média 0,0). O áudio é música, com hash diferente (outra codificação ou trilha). Os textos dos anúncios mudam só no link (USA × UK). | **10** (um só) |
| E | **21** (720×900) = **54** (720×1280) | Mesmos planos e textos, versão 4:5 × 9:16, só música | **54** (9:16) |
| F | Vídeo **44** (720×720, 3,4 s) ≈ imagem **01** | O 44 é a imagem 01 animada (os itens 4 e 5 aparecem depois), sem áudio | Traduzir a 01 e reanimar |

Saem **10 peças de vídeo únicas** (07, 08, 10, 17, 24, 25, 32, 46, 54 e 44/01). Se a conta pedir 4:5, as versões 4:5 saem por recorte das 9:16 traduzidas, sem retrabalho.

## 2. Narradoras
Todas as narrações são **femininas**: F0 mediano entre 201 e 237 Hz, na voz isolada pelo demucs.

| Narração | Vídeos | F0 mediano | Faixa p10–p90 | Amostra p/ clonar | Duração da amostra |
|---|---|---|---|---|---|
| N1 | 07 / 60 | 214 Hz | 194–271 | `audio/voz_07.wav` | 26,0 s |
| N2 | 16 / 32 | 232 Hz | 189–304 | `audio/voz_16.wav` (tirada do 32) | 15,6 s |
| N3 | 24 | 201 Hz | 173–251 | `audio/voz_24.wav` | 19,1 s |
| N4 | 25 | 237 Hz | 193–304 | `audio/voz_25.wav` | 19,3 s |
| N5 | 31 / 46 | 219 Hz | 183–269 | `audio/voz_31.wav` (tirada do 46) | 23,7 s |

- **5 narrações distintas**, todas de mulher. Os timbres não batem entre roteiros diferentes (MFCC 35–60, contra 4–12 entre duplicatas). Por isso considero **5 vozes**, uma por roteiro.
- **Precisa de revisão manual (ouvido):** N2 e N4 têm pitch e faixa quase iguais e podem ser a mesma pessoa ou a mesma voz de TTS. Se forem, basta clonar uma.
- **Nenhuma narração chega a 30 s** (a maior tem 26 s): os vídeos são curtos. O ElevenLabs aceita, mas a qualidade do clone com ~15–26 s é menor que com 60 s. O caminho seguro é juntar N2+N4 se forem a mesma voz, ou usar uma voz feminina LATAM pronta da biblioteca (sem custo de clone).
- **17:** a faixa tem **voz contínua de 0 a 14 s** (vocal de −23 dB em todos os segundos), ou seja, é uma **música cantada** e não narração. O whisper pegou só "Check this out right here" (0–1,5 s, no_speech 0,48). Ver o tratamento do 17.

## 3. Tabela por vídeo
Legenda das colunas de marca: **Fala** = "H2O X5" falado; **Texto** = texto sobreposto; **Aparelho** = logo impresso no mop, na caixa ou na embalagem.

| ID | Duração | Resolução | Áudio | Duplicata de | Narr. | Texto na tela (resumo) | Marca na fala (s) | Marca no texto (s, região) | Logo no aparelho/caixa legível (s) | Tratamento proposto |
|---|---|---|---|---|---|---|---|---|---|---|
| **07** | 28,7 | 720×1280 | Narrado + trilha | = 60 | N1 | 0–4 artigo científico de fundo + caixa "Did you know bacteria on your kitchen counters is making you sick?" (y≈586–727); 4–7 "BEFORE ❌/AFTER ✅"; 4–9 "This is your sign to sanitize your kitchen using H2O X5!" (y≈639–714); 9–17 "Uses 1300 watts of superheated steam which kills 99%…" (y≈773–931); 17–18 "Lab certified ✅"; 19–20 "Just steam and a wipe!"; 20–23 "Look how clean this is! No more germs"; 23–25 "Very impressed with this!"; 25–29 cards de avaliação em inglês + "Get Yours Now 4000+ ★ REVIEWS" | ~5,5 s e ~7 s ("using H2O X5", "The H2O X5 uses…") | 4–9 (caixa central); 25–29 "H2O X5" no 1º card (topo esq., y≈143) | ≈0–1 s (só o corpo verde; sem logo legível) | Tradução completa: narração clonada N1 + `07_no_vocals.wav`; caixas brancas novas em ES nas mesmas posições (estilo caixa branca arredondada); "ANTES/DESPUÉS"; nos 25–29 s cobrir os cards em inglês com cards em espanhol (ou recortar para o mop + selo); CTA com setas; selo COD. O artigo científico de fundo pode ficar (é textura, ilegível no celular). |
| **60** | 28,7 | 720×900 | idem | **dup. 07** | N1 | Igual ao 07, em 4:5 | idem | 4–9; 25–29 | idem | Não refazer: recortar do 07 traduzido, se precisar de 4:5. |
| **08** | 24,6 | 720×720 | Só música | — | — | Comercial de TV antigo (marca **THANE**): 0–2 "Introducing THANE ❤ H2OX5™" (topo); 2–4 "5-in-1 STEAM CLEANING SYSTEM"; 4–6 "WITH VARIABLE STEAM"; **6–8 coração "12 Million SOLD WORLDWIDE"** (topo esq.); 8–10 "1. POWERFUL FLOOR CLEANER"; 10–12 "2. VERSATILE HAND HELD STEAMER"; 12–13 "3. WINDOW CLEANER"; 14–15 "4. CARPET CLEANER"; 15–17 "5. GARMENT CLEANER"; 17–19 "CHANGE THE WAY YOU CLEAN" (mop **vermelho** nessa cena); 19–21 "WITH THE POWER OF STEAM"; 22–24 logo "THANE H2OX5" | — | 0–2 e 22–24 (logo grande, topo/centro) | 8–10, 19–21, 21–24 (adesivo "H2O MOP X5" na base); 13 (lateral). ≈8 s | Textos animados em inglês: cobrir cada letreiro com caixa sólida + texto ES (≈10 letreiros, 1–2 s cada). **Atualizar "12 Million" para "14 millones"** (decisão da dona). Formato 1:1 antigo: para 9:16, montar em tela com faixa de título em cima e selo/CTA embaixo. O logo THANE pode ficar (é o fabricante da linha H2O, só por revisão manual). **Precisa de revisão manual:** a cena 17–19 s mostra um mop **vermelho** (outra cor/modelo); cortar se a oferta for só o verde. |
| **10** | 9,0 | 720×900 | Só música | = 15 | — | Faixa fixa "H2O X5 STEAM CLEANER" (y≈368–400, faixa branca no meio) + mosaico de 6 mini-vídeos embaixo | — | 0–8 (faixa central) | 0–1 "H2OX5" grande na base do mop (x≈306–456, y≈178–258); 6 lateral. ≈2 s | Traduzir só a faixa ("LIMPIADOR A VAPOR H2O X5"): troca de texto barata (`trocar_texto_tela.py`) ou faixa nova. Para 9:16: 4:5 sobre fundo + título no topo + CTA/selo embaixo. Trilha: manter ou trocar. |
| **15** | 9,0 | 720×900 | Só música | **dup. 10** | — | Igual ao 10 | — | idem | idem | Não refazer. |
| **16** | 16,3 | 720×900 | Narrado + trilha | = 32 | N2 | 0–6 "Five cleaning tools in one lightweight, powerful steamer" (centro); legenda palavra a palavra (y≈715–770) | 1–2 s ("I love the H2O X5") | 1–2 legenda "the H2O X5" | 12–16 adesivo grande "H2O MOP X5" na base (close); 1–2 pequeno. ≈4–5 s | Base no 32. |
| **32** | 16,3 | 720×1280 | Narrado + trilha | **dup. 16** | N2 | Igual ao 16, em 9:16 (título y≈498–657; legenda y≈1017–1086) | 1–2 s | 1–2 legenda | 12–16 adesivo "H2O MOP X5" (close). ≈4–5 s | Narração N2 clonada + `32_no_vocals.wav`; cobrir o título (caixa transparente sobre vídeo, então usar faixa/caixa opaca nova) e trocar a legenda queimada (faixa opaca alpha ≥250 em y≈1000–1100, ou Vmake se a dona aprovar o custo). Estender o fim ~2 s (quadro congelado) para o CTA. |
| **17** | 14,0 | 720×1280 | **Música cantada** (vocal 0–14 s) | — | — (cantor) | 0–3 "A cleaner that cleans every surface in your home"; 3–4 "Carpets"; 4–6 "Floors"; 6–7 "Handheld steamer"; 7–9 "Air fryer"; 9–12 "Oven"; 12–14 "Microwave and more" (todos no centro, y≈560–650, texto branco fino sem caixa) | — | — | 0–1 caixa "H2O X5" (topo esq.); 1–3 "H2OX5" na base; 4–6 lateral da base. ≈4–5 s | Trocar os 7 rótulos curtos por ES (faixa/caixa nova). **Trocar a música** por trilha livre: é uma canção em inglês, com risco de direitos e de não fazer sentido no mercado. Opcional: narração ES curta (ex.: N3/N5) virando um vídeo narrado. |
| **21** | 9,6 | 720×900 | Só música | = 54 | — | 0–5 "Floors, counters, windows, carpets, clothes — clean them all with ONE steamer!"; 5–10 "H2O X5 Steam Cleaner" | — | 5–10 (centro) | 0 e 6–7 lateral da base (pequeno). ≈2 s | Base no 54. |
| **54** | 9,6 | 720×1280 | Só música | **dup. 21** | — | Igual ao 21, em 9:16 (y≈351–526) | — | 5–10 | ≈2 s | Trocar os 2 textos (texto branco fino sobre vídeo: caixa/faixa nova); CTA e selo. Vídeo curto, bom para teste barato. |
| **24** | 19,5 | 720×1280 | Narrado + trilha | — | N3 | 0–6 "Protect your family from 99% of germs with this one item" (y≈374–525); legenda palavra a palavra (y≈970–1025); 13–19 "H2O X5 Steam Cleaner" (y≈368–420) | ~3–4 s ("with the H2O X5 Steam Cleaner") | 3–5 legenda; 13–19 título | 3–7 base; 9–11 base; 13–15 caixa "H2O X5" + base; ≈7–8 s | Narração N3 + `24_no_vocals.wav`; título e legenda novos; estender o fim para o CTA. **Precisa de revisão manual:** "safe around kids and pets" não está nas especificações enviadas. |
| **25** | 19,5 | 720×1280 | Narrado + trilha (depoimento) | — | N4 | 0–7 caixa verde "Deep clean your home *in minutes*, not hours!" (y≈537–667); legenda palavra a palavra (y≈1087–1150) | ~1–2 s ("get the H2O X5 sooner") | 1–3 legenda | ≈1 s (mop em movimento, logo pequeno) | Narração N4 (1ª pessoa feminina: "encantada") + `25_no_vocals.wav`; caixa verde nova (mesmo estilo); legenda nova. |
| **31** | 24,0 | 720×900 | Narrado + trilha | = 46 | N5 | 0–3 caixa verde "Fast, effective cleaning that actually makes life easier"; legenda palavra a palavra | ~4 s e ~18,5 s | 3–5 "The H2O X5"; 18–20 "The H2O / X5 saves time" | 3–5 caixa grande "H2O X5" (unboxing); 6–8 caixa ao fundo; 9–10 e 22–24 base "H2OX5". ≈7 s | Base no 46. |
| **46** | 23,9 | 720×1280 | Narrado + trilha | **dup. 31** | N5 | Igual ao 31, em 9:16 (caixa verde y≈200–260; legenda y≈1000–1046) | ~4 s e ~18,5 s | 3–5; 18–20 | ≈7 s | Narração N5 + `46_no_vocals.wav`; caixa verde nova e legenda nova; estender o fim para o CTA. |
| **44** | 3,4 | 720×720 | **Sem áudio** | ≈ imagem 01 | — | "14 MILLION SOLD WORLDWIDE", "H2O X5 5-IN-1 STEAM CLEANER", 5 itens, "SHOP NOW", "★★★★★ (3026+ Reviews)" | — | 0–3 (título esq.) | Mop pequeno, logo ilegível | Refazer a partir da imagem 01 traduzida, com a mesma animação (itens entrando). Trocar "SHOP NOW" por "Pago contra entrega" ou pelo CTA. |

### Marca: resumo e esforço
Como a marca fica, **nenhuma ocorrência exige edição paga** (Kling/Flora). Fala e textos em inglês são refeitos de qualquer forma na tradução, e o "H2O X5" continua em ES.

O logo no aparelho só foi medido para registro, caso um dia a marca mude. Ele aparece legível em cerca de **38 s** nos vídeos únicos:

| Vídeo | Logo legível |
|---|---|
| 08 | ≈8 s |
| 24 | ≈8 s |
| 46 | ≈7 s |
| 32 | ≈5 s |
| 17 | ≈5 s |
| 10 | ≈2 s |
| 54 | ≈2 s |
| 25 | ≈1 s |

Isso dá cerca de 8 takes de 5 s, ou US$1,2–2,4 a US$0,15–0,30 por take, mais as re-tentativas. **Custo atual: US$0** com edição de logo.

## 4. Claims e referências que conflitam com as especificações ou com a LATAM
| Onde | O que diz | Problema | Ação proposta |
|---|---|---|---|
| Vídeo 08, 6–8 s | "12 Million SOLD WORLDWIDE" | A dona usa "14 million" (imagem 01 e vídeo 44) | Trocar por "14 MILLONES VENDIDOS" |
| Imagem 45 (rodapé) | "1-YEAR FREE WARRANTY" | Especificação: **2 anos** de garantia | "2 AÑOS DE GARANTÍA" |
| Imagem 45 (rodapé) | "FREE SHIPPING*" | Condição dos EUA, com asterisco | Trocar por "PAGO CONTRA ENTREGA" ou confirmar se há frete grátis (**precisa de revisão manual**) |
| Imagens 45, 59 e 61 | "$55 OFF", "SAVE $55", "Claim My $55 Savings" | Mantido por decisão da dona. **Atenção:** em CL/CO/MX "$" lê-se como **peso local** (US$55 ≠ $55 CLP/COP/MXN) | Escrever "US$55" ou converter por país (**precisa de revisão manual**) |
| Imagem 61 (rodapé) | "*Based on controlled lab tests. Efficacy varies by treatment time and surface." | Tem que acompanhar o "99%" | Traduzir e manter: "*Según pruebas de laboratorio controladas. La eficacia varía según el tiempo de aplicación y la superficie." |
| Vídeo 07/60, 17–18 s | "Lab certified" | Não consta das especificações enviadas | Mantido como claim do original; **precisa de revisão manual** |
| Vídeo 24 | "safe around kids and pets" | Não consta das especificações | **Precisa de revisão manual** |
| Vídeo 07/60 | "1300 watts" | Bate com a especificação (1300 W) | OK |
| Vídeo 07/60, gancho | "…is making you sick?" | Mantido (decisão da dona). Risco de compliance Meta (afirma condição de quem vê) | Mantido na pergunta "¿Sabías que…?" e sinalizado |
| Vídeo 07/60, 25–29 s | Cards de avaliação em inglês, de clientes do Reino Unido | Prova social em inglês na LATAM | Trocar por cards em ES ou cobrir (não inventar depoimentos: usar avaliações reais traduzidas ou só "4000+ reseñas") |
| Vídeo 08, 17–19 s | Mop **vermelho** | Outra cor | Cortar a cena se a oferta for só o verde |
| Textos (TEXTOS/) | "Ships from USA in 1-2 Business Days", "Same day dispatch from the UK", "Ships from Canada…" | Referência a EUA/Reino Unido/Canadá | Remover; usar "Pago contra entrega · Envío a todo el país" (prazo real: **precisa de revisão manual**) |
| Texto 28 | "3 Easy Payments of $43 + Free Shipping" | Oferta parcelada dos EUA | Remover |
| Textos (todos) | Links x5mop.com, h2oforyou.co.uk/.com/.ca, tinyurl | Lojas de outros países | Trocar pelo link da loja COD |
| Textos 07/10/11/… | "weighing under 5lbs" | Unidade imperial | "pesa menos de 2,3 kg" (bate com a especificação) |
| Imagens 36 e 62 | **"USE CODE: FBX5"** | Removido por decisão da dona | Ocupar o mesmo botão com "PAGO CONTRA ENTREGA" |

## 5. Tabela por imagem
| ID | Tamanho | Textos (OCR) | Marca (texto / aparelho) | FBX5 | Tratamento |
|---|---|---|---|---|---|
| 01 | 1080×1080 | "14 MILLION SOLD WORLDWIDE" (topo dir. 445,36–1051,72); "H2O X5" (58,197–422,285); "5-IN-1 STEAM CLEANER"; 5 itens (Floor cleaner, Carpet cleaner, Garment steamer, Handheld steamer, Glass cleaner); "SHOP NOW"; "★★★★★ (3026+ Reviews)" | Texto "H2O X5"; logo pequeno na base do mop | — | Troca local de texto sobre fundo liso (PIL): "14 MILLONES VENDIDOS", "LIMPIADOR A VAPOR 5 EN 1", itens em ES, "PAGO CONTRA ENTREGA", "(3026+ reseñas)". Base do vídeo 44. |
| 11 | 1638×2048 | Pop-up do iOS "Copy / Select All / Look Up"; texto selecionado "Now you can clean every surface in your home with just one device"; "H2O X5 5-in-1 Steam Cleaner" (rodapé 354,1610–1289,1899) | Texto rodapé; aparelho sem logo legível | — | Trocar o pop-up por "Copiar / Seleccionar todo / Buscar", a frase selecionada (fundo azul de seleção) e o rodapé "Limpiador a vapor H2O X5 5 en 1". Fundo fotográfico atrás do texto: pede cuidado (camada nova sobre área desfocada). |
| 13 | 1254×1254 | "JUST ADD WATER. LET STEAM DO THE CLEANING." (caixa verde); "★★★★★ 4,000+ 5-STAR REVIEWS" | Logo "H2OX5" na base do mop (719,942–855,998) | — | Caixa verde lisa: reescrever "SOLO AGREGA AGUA. DEJA QUE EL VAPOR LIMPIE."; rodapé "4.000+ RESEÑAS DE 5 ESTRELLAS". |
| 28 | 1080×1080 | "H2O X5 STEAM MOP"; "SALE NOW ON!"; "LIMITED STOCK ONLY!"; "SHOP NOW" | Texto "H2O X5"; logo pequeno na base | — | "TRAPEADOR A VAPOR H2O X5", "¡OFERTA!", "¡STOCK LIMITADO!", botão → "PAGO CONTRA ENTREGA". |
| 33 | 1254×1254 | "ONE MOP. WHOLE-HOME CLEAN."; "5 cleaning modes. Powerful steam. No added cleaning chemicals."; "★★★★ 4,000+ 5-STAR REVIEWS" | Aparelho sem logo legível | — | "UN SOLO TRAPEADOR. TODA LA CASA LIMPIA." etc. Fundo é foto: caixa/área clara no topo esq. ajuda. |
| 36 | 1080×1080 | "H2O X5 STEAM CLEANER"; "SALE NOW ON!"; "LIMITED STOCK ONLY!"; **"USE CODE: FBX5"** (612,895–985,934) | Texto "H2O X5"; logo pequeno na base | **REMOVER** | Trocar o botão do código por "PAGO CONTRA ENTREGA"; demais textos em ES. |
| 45 | 1254×1254 | Logo "H2OX5™"; "LIMITED TIME OFFER"; **"$55 OFF"**; "POWERFUL STEAM A HEALTHIER HOME"; ícones "KILLS 99% OF BACTERIA, VIRUSES & GERMS*", "CHEMICAL FREE", "5-IN-1 MULTI-SURFACE VERSATILITY"; faixa "FLOORS / KITCHEN / BATHROOM / CARPETS / WINDOWS"; rodapé "4,000+ 5 STAR REVIEWS", "FREE SHIPPING*", "30 DAY MONEY BACK GUARANTEE**", **"1-YEAR FREE WARRANTY"** | Logo texto topo; aparelho pequeno | — | ~25 blocos de texto pequenos. Trocar a garantia para **2 años**; "ENVÍO GRATIS" só se confirmado. A mais trabalhosa das imagens. |
| 47 | 2000×2000 | "ONE DEVICE… 5 CLEANING SOLUTIONS FOR EVERY CORNER OF YOUR HOME!"; cards "Handheld Steamer / Comes with many attachments", "Floor Cleaner / and carpet steamer"; balão "Must-have for every home"; "H2O X5 5-in-1 Steam Cleaner" | Texto rodapé dir. | — | Fundo liso claro: troca local simples. |
| 58 | 1254×1254 | "LIGHTWEIGHT. EASY TO MOVE."; "Clean upstairs, downstairs and everywhere between."; "★★★★★ 4,000+ 5-STAR REVIEWS" | Logo "H2OX5" na base (827,887–889,947), legível | — | Caixa verde lisa: "LIVIANO. FÁCIL DE MOVER." etc. |
| 59 | 1254×1254 | Logo "H2OX5™"; "LIMITED TIME OFFER"; **"$55 OFF"**; "A CLEANER HOME NATURALLY"; "POWERFUL STEAM. REAL RESULTS. NO HARSH CHEMICALS."; ícones (kills 99%…, chemical free, 5-in-1); faixa "FLOORS…WINDOWS" | Logo texto topo | — | Igual à 45, sem rodapé de garantia. |
| 61 | 1254×1254 | Logo "H2OX5™"; "EXCLUSIVE LIMITED-TIME OFFER"; "A Healthier Home, Powered by Steam"; **"SAVE $55 On the H2O X5 Steam Cleaner"**; ícones; "4,000+ Reviews"; "30-Day Money-Back Guarantee"; botão "Claim My $55 Savings"; nota "*Based on controlled lab tests…" | Texto e logo topo | — | ~20 blocos; manter a nota de rodapé traduzida (sustenta o 99%). |
| 62 | 1080×1080 | "H2O X5 STEAM CLEANER"; "SALE"; "LIMITED TIME ONLY"; **"USE CODE: FBX5"** (139,802–491,838) | Texto; logo "H2O X5" pequeno na base | **REMOVER** | Botão → "PAGO CONTRA ENTREGA"; "OFERTA / POR TIEMPO LIMITADO". |

As imagens se agrupam em 3 famílias:
- **SALE:** 28, 36 e 62.
- **$55 OFF:** 45, 59 e 61.
- **Benefício:** 01, 11, 13, 33, 47 e 58.

Todas dá para fazer **sem custo**, com troca local de texto (PIL: caixa da cor do fundo + fonte parecida). A alternativa paga é a Flora i2i, a ~US$0,073 por imagem (~US$0,88 pelas 12), útil só para 11 e 33 (texto sobre foto).

## 6. Roteiros em espanhol (`roteiros/`)
| Arquivo | Base | Palavras faladas EN → ES | Observação |
|---|---|---|---|
| `07_es.txt` | 07 / 60 | 66 → 58 (−12%) | Gancho "making you sick" mantido; "save big today" virou CTA (sem "hoy") |
| `16_es.txt` | 32 / 16 | 54 → 44 (−19%) | CTA acrescentado (o original não tem): estender ~2 s |
| `24_es.txt` | 24 | 56 → 51 (−9%) | "seguro con niños y mascotas" sinalizado |
| `25_es.txt` | 25 | 64 → 57 (−11%) | Depoimento feminino em 1ª pessoa |
| `31_es.txt` | 46 / 31 | 76 → 70 (−8%) | Mais longo; se estourar o tempo, cortar "y más" / "con un solo aparato" |

Em todos:
- a marca é "H2O X5";
- o CTA é "Haz clic en Más información";
- o espanhol é neutro: "piso", "alfombra", "liviano", "trapeador", "aparato", "mugre";
- não há hora do dia;
- as marcações de tempo dos planos vão em linhas `#`.

Espanhol fala ~10–15% mais sílabas que inglês. Se a narração clonada passar do tempo do vídeo, use `--vel` ou corte frases de apoio, nunca os claims.

## 7. Plano de produção sugerido (próxima etapa, sem custo até o item 3)
1. Base 9:16: 07, 32, 24, 25, 46 (narrados), 54, 17 e 10 (música). 08 e 44/01 entram por último (precisam de recomposição de formato).
2. Para cada narrado, montar o `prep.json` do `preparar_corpo_traducao.py`:
   - caixas/faixas opacas sobre o título e a legenda queimada (alpha ≥250);
   - títulos novos em ES no mesmo estilo (caixa branca ou verde);
   - fundo = `audio/<id>_no_vocals.wav`;
   - fim congelado (~2 s) para o CTA.
   Depois `montar_ad.py` com receita 720, selo "PAGO CONTRA ENTREGA" e setas no "Más información".
3. Revisão local: `revisar_ad.py --idioma es --idioma-residual en`, com proibidos = "FBX5", "USA", "UK", "12 million", "1-year".
4. **Paga (pedir aprovação):** clonar as vozes N1–N5 (ou 4, se N2 = N4) e gerar ~5 narrações ES (~300–400 caracteres cada, total ≈1.850 caracteres ≈ US$0,31 no ElevenLabs a US$0,165/1.000). Tempo: ~10 min de geração + montagem.
5. Opcional pago: Vmake para remover a legenda queimada sem faixa (cota Vmake), se a faixa opaca ficar pesada visualmente.

## 8. Pendências e limitações
- **N2 × N4**: confirmar de ouvido se é a mesma voz.
- **Amostras de voz curtas** (15–26 s): clone com qualidade limitada (seção 2).
- **17 é música cantada**: precisa de trilha nova (sem custo, banco livre).
- **"$" × peso local**, **frete grátis**, **"Lab certified"**, **"safe around kids and pets"**, **prazo de entrega**: revisão manual da dona.
- **Mop vermelho no 08 (17–19 s)**: cortar ou manter?
- **Cards de avaliação do 07**: decidir entre traduzir avaliações reais ou só "4000+ reseñas" (não inventar depoimentos).
- O OCR do 07/60 entre 0 e 4 s lê o artigo científico de fundo (texto de textura). Esses blocos foram ignorados na análise e estão nos JSON só como registro.
- A GPU não serviu para whisper/demucs (falta cuBLAS 12 e torch sem CUDA). Tudo rodou em CPU, sem impacto no resultado.
