# Briefing comum — Wyze Solar Cam Pan 2K: inglês → espanhol LATAM (05/10/2026)

A pessoa vende a **Wyze original** em toda a LATAM. Por isso a marca **Wyze PODE ficar**: no relevo da câmera, na caixa, no app e na marca d'água.

**Não pergunte nada à pessoa.** Quando houver dúvida, escolha o lado seguro e registre a decisão no relatório.

**Nunca leia nem imprima arquivos `.env`.** Os scripts do kit carregam as chaves sozinhos.

## Onde estão as coisas
- **Originais:** `C:\Users\PICHAU\Downloads\WYZ-CAMARA-LATAM\originais\NN.mp4` (720x1280).
- **Estudo:** `..\ESTUDO-WYZE-LATAM.md`. Leia a linha do seu vídeo: ela lista o que precisa sair.
- **Transcrição:** `_analise\fala\NN.json`, com idioma e segmentos.
- **Folha de contato:** `_analise\folhas\NN.jpg`.
- **Kit:** `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\`. Leia o `CLAUDE.md` dele e a seção "Tradução de criativo de outro idioma" do `C:\Users\PICHAU\Downloads\Produtividade com ia\CLAUDE.md`.
- **Exemplo pronto do mesmo fluxo (inglês → espanhol do Chile):** `C:\Users\PICHAU\Downloads\PODADORA-CL\`. Use como base os scripts e as receitas de `_analise\` e `_trabalho\`, e o `preparar_corpo.py`.
- **Trabalho:** `C:\Users\PICHAU\Downloads\WYZ-CAMARA-LATAM\producao\_trabalho\adNN\`.
- **Saída:** `C:\Users\PICHAU\Downloads\WYZ-CAMARA-LATAM\producao\AD NN - WYZE-SOLAR-CAM-PAN-<TEMA>-ES-LATAM.mp4`, em 720x1280.

## Especificações oficiais (wyze.com, Solar Cam Pan 2K) — use SÓ estas
- Video 2K (3MP).
- Giro 360° horizontal e 70° vertical. Seguimiento de personas con IA. Detección de movimiento.
- Visión nocturna a color. Reflector (2 LED). Sirena de 105 dB. Audio bidireccional (hablar por el celular).
- IP65, resistente a la intemperie (lluvia y polvo).
- Panel solar: **1 hora de sol directo al día** basta para funcionar continuo. Cable largo (3 metros) para poner el panel donde da más sol. Batería de 6400 mAh.
- Graba en tarjeta microSD. **No necesita suscripción** (la suscripción es opcional).
- Se ve y se controla desde el celular con la app Wyze, desde cualquier lugar.

**Não traduza nem invente o que não estiver acima:**
- "funciona sin sol" e "semanas sin sol": troque por "y la batería la mantiene funcionando de noche y en días nublados";
- "nunca la cargué en X meses": troque por "no tienes que cargarla";
- "#1 en América", "agotada 8 veces", "volvió al stock después de 6 meses", "la más vendida en TikTok", "bajó el precio", "descuento", "año nuevo", "regalo de Navidad", "link abajo", "carrito naranja", "wyze.com", "HOA";
- medidas em pés: troque por metros ou tire.

## Oferta / CTA (universal LATAM)
- **Sem preço, sem país e sem promessa de frete ou garantia**: a pessoa não confirmou para este produto.
- **CTA falado:** "Toca el botón de abajo y pide la tuya." Pode abrir com uma frase de urgência neutra, sem dado falso, como "Pídela hoy".
- **Setas de CTA:** no "Toca".
- **Selo:** NÃO coloque selo de oferta. Deixe a receita pronta para incluir depois (campo `selo` comentado ou num `receita_com_selo.json` com "PAGO CONTRA ENTREGA").

## Voz (IMPORTANTE)
Os narradores são criadores reais de terceiros. **NÃO clone a voz deles.**
- Use uma voz de catálogo do ElevenLabs em espanhol latino neutro, do mesmo gênero e com energia parecida com a do original.
- Liste as vozes com as ferramentas do kit ou o MCP do ElevenLabs.
- Use `tts_elevenlabs.py` com alinhamento.
- Mantenha a mesma voz em todos os vídeos de um mesmo criador.

## Fluxo — Grupo A (só mãos ou produto)
1. Separe a música e o fundo com `python -m demucs --two-stems=vocals` e use só o `no_vocals.wav`.
2. Escreva o roteiro em espanhol neutro LATAM com a mesma estrutura do original (gancho, benefícios, CTA), corrigido pelas regras acima.
   - Duração parecida com a do original. O espanhol fica ~15% mais longo, então enxugue o texto.
   - Salve em `adNN\roteiro_es.txt`.
3. Gere o TTS com alinhamento. Se não couber, ajuste o tempo das cenas: corte sobras, estique os takes com congelamento curto ou repita um take de produto. **Não acelere a voz acima de 1,1x.**
4. Cubra a legenda em inglês com faixa ou caixa opaca, com alpha ≥ 250 (ver as armadilhas no CLAUDE.md), e o título em inglês do topo com uma caixa nova em espanhol.
5. Corte ou cubra os trechos visuais proibidos que o estudo lista para o seu vídeo: Halloween, FedEx, rostos de terceiros nítidos nas gravações (desfoque), data, número de casa.
6. Monte com `montar_ad.py` com `resolucao: "720"`: legenda nova pelo alinhamento e setas no "toca".

## Fluxo — Grupo B (rosto do criador)
**NÃO faça lipsync nem coloque fala nova na boca do criador real**, porque seria fazê-lo dizer o que não disse. Reconstrua assim:
1. Aproveite só os takes **sem o rosto do criador**: produto, instalação, mãos, gravações da câmera e app. Aproveite também o gancho visual, se não tiver rosto.
2. Faça a parte "falada" com **um avatar HeyGen próprio** (MCP do HeyGen):
   - O saldo é ~9.000 créditos; um UGC de ~50 s custou ~15 créditos.
   - O avatar "Lymphoria UGC Latina 48" (id `571dd78eac576678691f4f2b2287a72e`) existe, mas é de outro nicho. Se preferir, crie um photo avatar novo coerente com o criador original (por exemplo, homem latino de 30 a 40 anos, estilo garagem ou quintal).
   - A integração ElevenLabs do HeyGen está quebrada: gere o áudio com `tts_elevenlabs.py` e envie o áudio para o HeyGen fazer o lipsync **do avatar**.
   - Teto: 200 créditos por vídeo.
3. Intercale o avatar (~40–60%) com os takes de produto, mais a legenda, as setas e o CTA.

## CPU / GPU
- Outros agentes estão rodando ao mesmo tempo. Use `cpu_threads=4` no Whisper e `-threads 4` no ffmpeg.
- O demucs pode usar a GPU (`-d cuda`), já que é rápido.
- No Bash, use `PYTHONIOENCODING=utf-8`.

## Revisão obrigatória (cada vídeo final)
- **Whisper (es) no final:** nenhum preço, país, TikTok, "link", Navidad/año nuevo ou alegação proibida. O texto tem que bater com o roteiro.
- **Whisper (en)** só para garantir que não sobrou fala em inglês, nem por baixo.
- **Folha de contato** (1 quadro a cada 1 s): nenhuma legenda em inglês aparecendo, nenhum quadro solto nos cortes, nenhum silêncio no fim e setas fora da legenda.

## Relatório final (a sua resposta)
Por vídeo:
- o arquivo e a duração;
- a voz usada (nome e id);
- os caracteres de TTS;
- os créditos HeyGen (grupo B);
- o que foi cortado ou trocado;
- o resultado da revisão;
- as pendências.

Salve também em `adNN\RELATORIO.md`.
