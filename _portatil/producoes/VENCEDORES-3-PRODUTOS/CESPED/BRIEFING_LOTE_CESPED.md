# Lote CÉSPED: podadora inalámbrica con ruedas (COD Chile), RASCUNHO 15/10/2026

> Rascunho do agente de estudo. **Não gerar nada pago** antes de a pessoa responder os itens [PENDENTE].
> Estudo completo (raio-x, matriz C01–C12, compliance e perguntas): `C:\Users\PICHAU\Downloads\VENCEDORES-3-PRODUTOS\CESPED\ESTUDO_CESPED.md`

## Decisões da pessoa (não reabrir)
- **Os anúncios vencedores são da pessoa.** Pode reaproveitar takes, cenas e vozes e clonar a voz dos narradores.
- **Mercado e preço:** COD Chile, **sem preço** no vídeo.
- **Oferta:** [PENDENTE] Unidade ou kit? Confirmar «despacho gratis», «pagas al recibir», prazo de entrega e «90 días de garantía».
- **Especificações** que podem ser faladas: [PENDENTE] ~4,5 kg, 2 baterias de 21 V, 4 cabezales, cabeça ajustável, lâmina de metal. Até confirmar, só o que o vídeo **mostra**.
- **Marca:** [PENDENTE] Nome do produto na página. A marca «SEESE» da bateria fica ou é borrada? Letreiro/marca d'água da loja?
- **Compliance:** [PENDENTE] Manter × suavizar:
  - câmera de segurança encenada + uniforme estilo UPS;
  - aviso «video acelerado» no V1;
  - «pícale» → «toca el botón de abajo».
  - Não suavizar sozinho.
- **Volume:** 12–14 criativos [PENDENTE: orçamento diário de mídia]. **Teto total:** US$ 15 no Flora (Seedance/Kling/GPT Image) + créditos HeyGen do plano + ElevenLabs.
- **Formato:** 9:16, 720×1280 ou maior, 30 fps [PENDENTE: 4:5?].
- **Selo fixo:** «PAGO CONTRA ENTREGA · DESPACHO GRATIS» no topo [PENDENTE: texto final].
- **CTA único:** bloco amarelo «PAGO CONTRA ENTREGA / ¡PAGAS AL RECIBIR!» + setas, como no V2, sem nada depois.

## Produto
Cortador de grama/roçadeira sem fio com rodas, 3 em 1 (cortapasto, orilladora, bordeadora), lâmina de metal, 2 baterias, verde-limão.

**Página de destino:** [PENDENTE]. Nunca mostrar domínio nem preço no vídeo.

## Material existente
**Vencedores** (`C:\Users\PICHAU\Downloads\VENCEDORES-3-PRODUTOS\CESPED\`):
- **V1** `CESPED_122119371195415302.mp4`:
  - 576×1024, 37 s, **sem texto na tela**, narração masculina.
  - Melhor abertura de antes/depois em 0–5 s.
  - **Upscale obrigatório** com `kit-edicao-criativos\ferramentas\upscale_video.py` (Real-ESRGAN, local) para 720×1280. Feito **1 vez pelo agente A**, que salva em `_trabalho\_base\V1_720.mp4` para os outros usarem.
- **V2** `CESPED_122145821439352607.mp4`:
  - 720×1280, 56 s, narração feminina.
  - Legenda queimada no centro (9–56 s), rodapé fixo «video acelerado», carimbo de câmera 0–14 s, bloco COD 46–56 s.
  - Versão limpa (centro sem legenda, LaMa local `ADLIB-104060992792639\producao\_trabalho\_vg` + `_lote\lama_base.py`) feita **1 vez pelo agente A** em `_trabalho\_base\V2_limpo.mp4`.

**Apoio:**
- Transcrições, OCR e folhas de contato: arquivos `_*` na mesma pasta.
- Banco de takes com tempos: §4 do estudo. Gerar o banco com `gerar_variacao.py banco` sobre `V1_720.mp4` e `V2_limpo.mp4`.
- Referência do produto para o GPT Image: quadro do V2 em 36,5 s (kit na mesa) e quadro do V1 em 35 s (produto inteiro em pé).

**Pipeline validado** (`Contexto\estrategias-criativos.md`):
1. GPT Image 2 **1k** com o produto de referência («não invente peças; rodas pretas com aro verde, cabeça redonda com protetor preto, haste prateada»).
2. Seedance 2.0 i2v com fala nativa ≤ 20 palavras / 8 s.
3. Clone da voz + STS do ElevenLabs para 1 voz por personagem.
4. Legenda pelo roteiro (`montar.py` modo roteiro); música a −32 LUFS.

**Regras deste produto:**
- **A pessoa de IA nunca corta pasto em cena.** Ela fala ou segura o produto parada; a ação de corte vem sempre do banco real (o modelo deforma roda e cabeça).
- Repartidor sem logo, sem porta abrindo nem pessoa entrando em veículo; personagem com ~25% da altura no plano de câmera de segurança.
- Transcrever cada take do Seedance antes de usar.
- Confirmar a olho os alarmes do QA de IA.

## Divisão (definida antes de gerar; cada agente usa só a sua subpasta)

Saída: `C:\Users\PICHAU\Downloads\VENCEDORES-3-PRODUTOS\CESPED\LOTE\<NN>_<CODIGO>.mp4` + `_narracion.txt` (roteiro + texto do anúncio ES-CL: título ≤ 40 caracteres e texto principal, sem preço). Trabalho em `LOTE\_trabalho\<agente>\`; bases compartilhadas em `LOTE\_trabalho\_base\` (só o agente A escreve; os outros esperam o `PRONTO.txt` dela).

| Agente | Criativos (conceitos do estudo) | Teto Flora |
|---|---|---|
| **A: fiéis + bases (roda primeiro)** | Bases: `V1_720.mp4` (upscale) e `V2_limpo.mp4` (LaMa) + banco de takes → `PRONTO.txt`. Depois: 01 **C01** V1 fiel em HD (legenda + selo + CTA COD; troca «pícale» só se aprovado); 02 **C02** V2 fiel curto de 30 s; 03 **C10** sensorial sem fala; 04 **C08** primavera (TTS com clone do narrador do V1) | US$ 0 |
| **B: história** | 05 **C03** câmera de segurança chilena (repartidor genérico; 1 imagem + 2 takes Kling sem fala); 06 variação de gancho do 05 com outra abertura do banco; 07 **C11** objeção «maleza gruesa» (TTS) | US$ 3 |
| **C: talking heads** | 08 **C04** vizinho (homem de 50); 09 **C05** «lo hice yo sola» (mulher de 40, selfie); 10 **C06** jubilado de 67 anos «la cuerda de la bencina». 1 imagem + 1 Seedance de 8 s cada | US$ 6,50 |
| **D: risco + comparativo** | 11 **C09** paga al recibir (repartidor entregando na reja; Seedance de 8 s); 12 **C07** bencina × botão em tela dividida (Kling sem fala de 5 s); 13 **C12** «3 lugares» (TTS + abertura estática opcional); 14 estático/carrossel do antes/depois (quadros do V1, custo zero) | US$ 4 |

Custo previsto ~US$ 11 (estimativas do estudo). A soma dos tetos por agente é US$ 13,50, e sobra ~US$ 1,50 de reserva até o teto total de **US$ 15**, liberada só com o ok da pessoa. A conta do Kling não foi medida neste projeto: o agente cota antes e para se passar do teto dele.

Cada agente:
- personagens novos de IA só por texto (chilenos de 35–70 anos, casa chilena com reja, pandereta e antejardín), **1 imagem por personagem aprovada antes do vídeo**;
- registra as vozes em `LOTE\_trabalho\_vozes.json` antes de gerar (1 voz por personagem; narradores = clone do V1 masculino / V2 feminino);
- revisa com `revisar_ad.py --idioma es` (termos proibidos: «pícale» se trocado, «aumento» só se mantido, preço, domínio), faz zoom nos takes de IA (rodas e cabeça do produto) e abre os vídeos no fim;
- no fim, roda `aberturas.py` da skill `andromeda` sobre `LOTE\` (agente A, depois que todos marcarem `PRONTO.txt`).

**Painel:** `python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa cesped-<letra> "..." --k <k> --n <n>` e `fim cesped-<letra>`.
