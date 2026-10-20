# Briefing: lote enxuto Lymphoria (COD Chile), versão barata, 09/10/2026

A pessoa aprovou o lote: **4 conceitos × 2 execuções = 8 vídeos + 4 estáticos**, com teto total de **~US$ 5** (máx. US$ 8).
- **Não pergunte nada.**
- **Nunca leia `.env`.**
- **Não abra players.**
- **Não use Seedance nem Kling** (caros). Use o que já existe + avatar HeyGen (créditos já pagos, que zeram dia 30) + ElevenLabs (centavos) + Nano Banana 2 nos estáticos.

**Escopo:** só estes criativos. Não mexa em loja, tema nem produtos.

## Oferta e regras (iguais às do lote Vitaly → Lymphoria)
- **Oferta:**
  - Compre 1, Reciba 2: $34.990;
  - Compre 2, Reciba 4: $59.990;
  - Compre 3, Reciba 6: $79.990.

  Com **Pagas al recibir**, envio grátis e garantia de **90 días**. CTA: "Toca el botón de abajo".
- **Compliance:**
  - Sem kg nem perda de peso. Use "deshincharse", "bajar tallas" ou "adiós hinchazón".
  - Sem cura, sem doença e sem médico.
  - Antes/depois só ilustrativo.
  - Ingredientes e claims só da página da Lymphoria (https://chileverificada.com/products/lymphoria): 4 hierbas (galio, trébol rojo, raíz de stillingia, fresno espinoso), "Sabe a miel", 100% natural.
- **Dose:** "unas gotas" sem número.
- **Espanhol do Chile**, com sotaque e tom chilenos.

## Material (tudo grátis)
- **Takes Lymphoria:**
  - `C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\` e `_trabalho\`, inclusive `ugc\prod\` (V1_gotero_hierbas, V2_frasco_cocina, V3_frasco_mesa, P2_frasco_miel etc.);
  - `C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\`.
- **Vencedores e corpos:**
  - AD 30 e AD 23 em `C:\Users\PICHAU\Downloads\APROVADOS E VALIDADOS TIKTOK\`;
  - corpos e receitas em `DRENAGEM-LATAM\producao\_trabalho\`.
- **Lote convertido** (cenas de banco): `C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\LYMPHORIA-ES-CL\` e os originais em `ADLIB-VITALY-CL\VIDEOS\`.
- **Fim/CTA (decisão da pessoa, 10/10):**
  - **sem preço** na tela ou na fala;
  - **sem card de texto colorido**;
  - fim clean com takes Lymphoria variados, legenda normal, selo pequeno "Pago contra entrega" e **setas vermelhas** no CTA, como nos vencedores do TikTok.

  Use o padrão definido em `ADLIB-VITALY-CL\_trabalho\prod\_cta_v2\ESTUDO-CTA.md`, assim que existir.
- **Avatar HeyGen:** `mcp__claude_ai_Heygen__*`.
  - Fluxo validado: avatar por prompt (`create_prompt_avatar`) ou por foto (`create_photo_avatar`).
  - O áudio sai do `tts_elevenlabs.py` e vai para `create_video_from_avatar` com o áudio enviado.
  - A integração de voz ElevenLabs↔HeyGen está quebrada, então mande o mp3.
  - Custo: ~15 créditos por ~50 s. Meça o saldo antes e depois.
- **Kit:** `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\`. Leia o `CLAUDE.md` e as skills `editar-criativo`, `gerar-midia-ia` e `revisar-criativo`.
  - Ferramentas: `gerar_variacao.py` (banco, fundo, montar), `montar_corpo_avatar.py`, `montar_ad.py` e `revisar_ad.py`.
  - Use `PYTHONIOENCODING=utf-8` e `-threads 3`.
- **Regras de produção:** `C:\Users\PICHAU\Downloads\Produtividade com ia\contexto\estrategias-criativos.md`.
  - Música a -32 LUFS sob a fala.
  - Legenda pelo roteiro, com alinhamento forçado.
  - Troca de plano a cada 1,5–4 s.
  - Gancho visual no quadro 1.

## Os 4 conceitos (Andromeda): cada execução precisa de abertura visual diferente
| ID | Persona / ângulo | Execução A | Execução B |
|---|---|---|---|
| **C1** | Mulher que trabalha o dia todo em pé (caixa, garçonete, enfermeira) e chega com tornozelos inchados. Dor/alívio | Avatar HeyGen chilena 30–45 de uniforme falando + B-roll de takes Lymphoria (gotas, frasco, pernas) | POV sem rosto: cenas do banco (pés, sapato saindo, sofá) + narração em off chilena |
| **C2** | Drama 2 ("¿estás embarazada?" no almoço de família, amiga ou sogra). Identidade | Gancho novo + corpo AD 30, com abertura de **cena diferente** do banco (`gerar_variacao.py`, modo A) | Gancho novo + corpo AD 23, também com abertura diferente |
| **C3** | Jubilada 60+, "ya puedo usar mis anillos / mis zapatos de nuevo". Prova social etária | Avatar HeyGen chilena 60+, voz calma | Depoimento em off de voz madura + mãos e frasco (takes) |
| **C5** | Desconfiada de comprar online. Remoção de risco: "lo pagas cuando llega a tu casa" + 90 días | Avatar HeyGen 35–50 explicando como funciona o pagamento na entrega | Montagem só com takes de caixa, frasco e card + narração e texto grande "PAGAS AL RECIBIR" |

**Estáticos (4, Nano Banana 2 i2i com a foto do frasco Lymphoria, ~US$ 0,07–0,11 cada):** um por conceito, no estilo dos 12 já feitos em `LYMPHORIA-ES-CL\IMAGENS\`. Para C1: "¿Llegas con los tobillos hinchados?".

## Revisão e saída
- **Revisão de cada vídeo:**
  - `revisar_ad.py` pelo PowerShell, com proibidos em `.txt` UTF-8: Vitaly, kilos, kg, cura, cáncer;
  - folha nas emendas;
  - avatar com lipsync ok (índice ≤ 0,6 no `checar_lipsync.py`, se aplicável).
- **Saída:**
  - `C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\LYMPHORIA-ENXUTO\LYM-CL_<C>_<persona>_<formato>_<a|b>.mp4` (nome Andromeda);
  - `...\LYMPHORIA-ENXUTO\IMAGENS\`;
  - `00-TEXTOS.txt` com título e texto principal por peça;
  - `RELATORIO.md` com custo real (US$ + créditos HeyGen), voz e revisão.
- **Painel:** python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa <id> ... ; fim <id>.
