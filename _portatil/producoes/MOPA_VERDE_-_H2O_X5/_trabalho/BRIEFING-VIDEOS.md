# Briefing: vídeos H2O X5 → espanhol neutro LATAM (08/10/2026)

A pessoa aprovou o orçamento (~US$ 4–5 no total; as imagens já gastaram US$ 1,40).
- **Não pergunte nada.** Na dúvida, escolha o lado seguro e registre a decisão.
- **Nunca leia nem imprima arquivos `.env`.**
- **Não abra os vídeos** em players.

## Contexto
- **A loja e o produto são da pessoa.** A marca **"H2O X5" fica** em tudo: fala, texto e logo. Clonar a voz da narradora original é **permitido**.
- **Ficha oficial:** https://h2oforyou.co.uk/products/h2o-x5-steam-cleaner-tvpr
  - 1300W, 5 en 1, calienta en menos de 30 s, menos de 2,3 kg;
  - elimina el 99 % de bacterias, virus y gérmenes (aplicado 15 s);
  - 30 días de devolución, 2 años de garantía;
  - 14 millones vendidas.
- **Mercado:** LATAM em geral, espanhol neutro com "tú", sem regionalismos.
- **Decisões da pessoa:**
  - **manter todas as alegações**, só traduzidas: "$55", "14 millones", "99 %", "lab certified", "seguro con niños y mascotas", cards de avaliação traduzidos sem inventar;
  - **tirar "USE CODE FBX5"**;
  - tirar qualquer referência a envio do Reino Unido, dos EUA ou do Canadá e a parcelamento.
- **CTA falado e escrito:** "Haz clic en Más información". As setas apontam para baixo na palavra "Más información".
- **Selo:** "Pago contra entrega".
- **Decisões já tomadas:**
  - **08:** "12 Million sold" vira "14 millones vendidas", que é o número da ficha. A mopa vermelha em 17–19 s fica e vai anotada.
  - **17:** a música (com letra em inglês) **fica**; não há narração. Traduza só o texto da tela.
  - **Formato:** cada arquivo sai no **mesmo formato do original** (9:16 = 720x1280, 4:5 = 720x900, 1:1 = 720x720).
  - **Duplicados:** a mestra é a 9:16. Gere o par 4:5 a partir da mesma montagem, com o mesmo texto e a mesma voz.

## Material pronto (`_trabalho\`)
- `ESTUDO-MOPA.md`: tabela por vídeo, onde está cada texto e cada marca, e conflitos.
- `transcricoes\<id>.json`: transcrição palavra por palavra.
- `ocr\<id>_ocr.json`: texto da tela com tempo e caixa.
- `folhas\`: folhas de contato.
- `audio\<id>_no_vocals.wav`: fundo sem a voz.
- `audio\voz_<id>.wav`: amostras da narradora.
- `roteiros\<id>_es.txt`: roteiros em espanhol.

Revise o roteiro contra a ficha e as decisões acima antes de gerar a voz.

## Ferramentas
Kit em `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\`.
- Leia o `CLAUDE.md` do kit e o do projeto, na seção "Tradução de criativo" e nas armadilhas.
- Rode com o diretório de trabalho no kit e `PYTHONIOENCODING=utf-8`.
- Whisper e OCR em sequência, nunca em paralelo.
- `-threads 4`.
- **GPU sem CUDA** nesta máquina: CPU.

**Voz:**
- `clonar_voz.py` a partir de `audio\voz_<id>.wav`, nome "MOPA X5 narradora <id>". Um clone por narradora; se 16/32 e 25 soarem iguais, use o mesmo.
- Depois `tts_elevenlabs.py --arquivo roteiro` (modelo multilíngue). A velocidade fica ≤1,1x.
- A fala tem que caber no tempo do vídeo. Se não couber, enxugue o texto ou congele um quadro curto no fim.
- **Teto: 6.000 caracteres** de TTS somando todos os agentes; você tem a sua parte.

**Corpo:**
- `preparar_corpo_traducao.py prep.json`, com o modelo em `exemplos/traducao_exemplo.json`.
- **Cobrir o texto em inglês:** use faixa ou caixa opaca (alpha ≥ 250) redesenhada no mesmo estilo e posição, com o texto em espanhol. O texto em inglês não pode aparecer por baixo.
- **Áudio:** fundo `no_vocals.wav` + narração nova.

**Montagem:**
- `montar_ad.py` na resolução do original (720 de largura), com legenda pelo alinhamento, selo "Pago contra entrega" e setas no CTA.
- Na 9:16 com faixa no rodapé, use selo y≈1110 e cta.y≈1490.

**Revisão:**
- `revisar_ad.py` **pelo PowerShell**, com os termos proibidos num `.txt` em UTF-8: FBX5, USA, UK, Canada, "Shop now", "código", "cuotas", "envío desde".
- Whisper em espanhol: o texto tem que bater com o roteiro.
- Whisper em inglês: nenhuma fala antiga por baixo.
- Folha 1 quadro/s: nenhuma palavra em inglês na tela, exceto a marca "H2O X5" e textos impressos no produto ou na caixa; nenhum quadro solto; nenhum silêncio no fim; setas fora da faixa.
- RESULTADO precisa sair OK.

## Saída
- **Vídeos:** `C:\Users\PICHAU\Downloads\MOPA VERDE - H2O X5\ES-LATAM\VIDEOS\NN AD - ES.mp4`, com o mesmo NN do original.
- **Trabalho:** `_trabalho\videos\NN\`.
- **Relatório:** `_trabalho\videos\RELATORIO-<agente>.md`, com o seguinte por vídeo:
  - roteiro final;
  - voz (id);
  - caracteres;
  - duração;
  - resultado da revisão;
  - pendências.
