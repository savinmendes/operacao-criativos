# AD 06 — Esquete de vizinhos (Grupo B) — relatório

**Arquivo:** `producao\AD 06 - WYZE-SOLAR-CAM-PAN-VECINOS-ES-LATAM.mp4`
- 41,6 s, 720x1280, 30 fps, H.264 + AAC 48 kHz, 13,5 MB, decodifica sem erro.

## Como foi reconstruído
- Os dois atores originais **não aparecem**. O diálogo virou uma conversa entre dois avatares HeyGen próprios, intercalados com takes sem rosto do original.
  - **Vecina:** "Lymphoria UGC Latina 48" (`571dd78eac576678691f4f2b2287a72e`).
  - **Vecino:** "WYZE Review Latino 35" (`430f346689b68545f1adbea9f186bd83`), criado pelo agente dos ADs 01/12.
- O avatar ocupa 24,8 s (59%); os takes de produto e app, 17 s.
- **Takes do original usados (s):**
  - celular com a gravação: 12,8–15,5;
  - câmera na grade: 16,0–18,5, 29,8–32,2 e 41,3–43,3;
  - app: 25,8–28,8;
  - mão apontando e luz: 33,8–36,0;
  - grade: 39,7–41,2.
- **Ajustes nos takes:**
  - Cada take foi cortado em y 0–1020 e ampliado ~1,25x. Isso tirou a legenda roxa em inglês sem precisar de faixa.
  - Os rostos dos atores na tela do celular (12,8–15,5) foram desfocados.
  - Dois takes saíram levemente desacelerados (0,89–0,93x) para cobrir a fala.
- **Áudio:**
  - Falas geradas no ElevenLabs. O HeyGen fez só o lipsync, a partir do áudio enviado.
  - Fundo: `no_vocals` do demucs (volume 0,45).
  - Normalização: loudnorm −15 LUFS.
- **Gancho:** caixa no topo (0–3,9 s) com "Mi vecina pensó que la estaba grabando 😳", no lugar do título "I called the HOA on her".
- **Legenda:** nova, pelo alinhamento, em y=1400 (escala 1080). Fica no peito do avatar, sem cobrir o rosto.
- **Setas de CTA:** no "Toca" (39,2 s) até o fim.
- **Selo:** não tem. A versão com selo está pronta em `receita_com_selo.json` ("PAGO CONTRA ENTREGA").

## Roteiro
Está em `roteiro_es.txt`. Em resumo:
1. Vecina: "¿Me estás grabando?"
2. Vecino:
   - segue o movimento;
   - grava em 2K;
   - não tem mensalidade (microSD);
   - não tem cabos e carrega com o sol;
   - app de qualquer lugar;
   - visão noturna a cores;
   - fala pelo celular;
   - refletor contra o gato.
3. Vecina: "¿Y si llueve?" Vecino: resiste à chuva e ao pó.
4. Vecina: "¿y dónde la consigo?" Vecino: "Toca el botón de abajo y pide la tuya."

## O que saiu
- O título "HOA".
- "Hey pervert".
- "deal… by Wyze".
- "I can show you a link".
- "prescription" (virou "mensualidad/suscripción").
- "completely waterproof" (virou "resistente a la lluvia y al polvo", conforme IP65).

## Voz, TTS e HeyGen
- **Vecina:** ElevenLabs "Nathalia – Neutral, Sweet and Friendly" (`tTQzD8U9VSnJgfwC6HbY`), do catálogo, latina neutra.
- **Vecino:** "WYZE 01-12 Mario animado" (`tomkxGQGz4b1kE0EM722`). É a mesma voz já pareada com esse avatar nos ADs 01/12.
- **Caracteres de TTS:** 652 (149 da vecina + 503 do vecino), ≈ US$ 0,11.
- **HeyGen:**
  - Foram 2 vídeos de avatar com áudio próprio: vecina com 12,0 s (`9a2ecdf2de778478bda923106c17f581`) e vecino com 15,2 s (`59e9f00b77c9a62dc257fee2b12e4538`).
  - Pela tabela, isso dá ~8–10 créditos.
  - O saldo foi de 9.071 para 9.009 no período, mas é compartilhado com os outros agentes.

## Revisão
- **Whisper (es):** o texto bate com o roteiro. Não aparece preço, país, TikTok, "link", Natal/ano-novo nem alegação proibida.
- **Whisper (en):** só a tradução do espanhol. Não sobrou fala em inglês.
- **Folha de contato 1/s** (`rev_folha.jpg`):
  - nenhuma legenda em inglês;
  - nenhum rosto dos atores;
  - nenhum quadro solto;
  - as setas aparecem no "Toca" e ficam fora da legenda.
- **Silêncio:** só 0,5 s no fim.
- **Defeito pego na revisão e corrigido:**
  - A saída do `montar_ad.py` (caminho rápido) veio com um **buraco de 3 s no áudio** (8,49→11,49 s), o que dessincronizou a fala.
  - A mesma saída veio **sem as setas**.
  - Correção: o vídeo do montar foi remontado com o áudio do `corpo.mp4` (loudnorm + aresample async) e as setas foram sobrepostas à mão no "Toca".
  - O arquivo final foi conferido de novo: sem buracos, Whisper ok e setas visíveis.

## Pendências e decisões para revisão manual
- A fala "No te graba a ti: sigue cualquier movimiento" é tom de humor. A câmera grava, sim, pessoas em movimento. Se quiser zero ambiguidade, troque por "Tranquila, vecina: solo sigue el movimiento" (exige refazer o TTS do M1 e o HeyGen do vecino).
- O avatar da vecina é de outro nicho (cozinha, selfie). Funciona como vizinha em casa, mas um avatar novo "na porta" seria mais fiel ao esquete.
- **Bug do kit para corrigir:** `montar_ad_rapido.py` gerou um buraco de áudio e perdeu as setas nesta receita (legenda com `y`, manchete com `px`). Ainda não diagnosticado.
- O `finalizar.py --so-revisar` marca "VERIFICAR" só porque espera 1080x1920. O arquivo é 720 por especificação.
