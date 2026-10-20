# UGC 01–05 Lymphoria (HeyGen) — relatório

## Arquivos
Todos em 720x1280, prontos e revisados, em `DRENAGEM-LATAM\producao\`:
- UGC 01 - LYMPHORIA-CARRITO-ES-LATAM.mp4 (52,6 s)
- UGC 02 - LYMPHORIA-PIRATAS-ES-LATAM.mp4 (52,0 s)
- UGC 03 - LYMPHORIA-DISCULPA-ES-LATAM.mp4 (51,2 s)
- UGC 04 - LYMPHORIA-HINCHAMOS-ES-LATAM.mp4 (53,7 s)
- UGC 05 - LYMPHORIA-PAGAS-AL-RECIBIR-ES-LATAM.mp4 (47,2 s)

## Avatar e voz
- **Avatar:** "Lymphoria UGC Latina 48" (look/grupo `571dd78eac576678691f4f2b2287a72e`). É um photo avatar novo, gerado por prompt no HeyGen: mulher latina de ~48 anos, selfie caseira na cozinha. Motor Avatar IV, expressividade alta, saída em 720p.
- **Voz:** ElevenLabs "Carolina - Conversational, Balanced" (`cIBxLwfshLYhRB9lCXEg`, feminina, meia-idade, espanhol latino). O áudio foi gerado com `tts_elevenlabs.py` (que salva o alinhamento) e enviado ao HeyGen como áudio para o lipsync.
- **Por que não usei uma voz do HeyGen:** as vozes clonadas privadas do HeyGen falham. A integração ElevenLabs da conta HeyGen está com o *key ID* salvo no lugar da chave `sk_...` (erro VOICE_CONFIG_ERROR). A 1ª tentativa do UGC 01 falhou por isso, sem custo.

## Custos
| Item | Custo |
|---|---|
| Criação do avatar | 1 crédito |
| HeyGen, por vídeo | 15 créditos (UGC 01 medido sozinho; os 5 juntos deram 75) |
| **HeyGen, total** | **76 créditos** (9.148 → 9.072) |
| TTS ElevenLabs | 4.239 caracteres ≈ US$ 0,70 |

## Tempo de render no HeyGen
| Vídeo | Tempo |
|---|---|
| UGC 01 | 123 s |
| UGC 02 | 107 s |
| UGC 03 | 104 s |
| UGC 04 | 122 s |
| UGC 05 | 262 s |

## Pós-produção
- Script: `ugc\posprod.py NN`.
- Cada vídeo tem 3 cortes de produto de 2,2 a 2,8 s, encaixados na palavra-âncora (ver `cfg.json`). Os cortes trocam só a imagem; a fala dela continua.
- Material dos cortes, em `prod\`:
  - `P1_kit3` e `P2_frasco_miel`: fotos com zoom lento. O rótulo foi descido para não ficar sob a legenda. O P2 corta os painéis de claims do `prod_1.jpg`.
  - `V1_gotero_hierbas` (`ad13/t4`), `V2_frasco_cocina` (`ad12/t2`) e `V3_frasco_mesa` (`ad14/t3`): takes do lote antigo recortados na parte de cima, para tirar a legenda queimada antiga.
- Legenda pelo alinhamento do ElevenLabs, com o texto do roteiro. A marca aparece como "Lymphoria", embora o TTS fale "Linforia".
- Selo "ENVÍO GRATIS A DOMICILIO / PAGO CONTRA ENTREGA / ¡PAGAS AL RECIBIR!" a partir da 1ª menção a envío/gratis. Setas de CTA no "Toca".
- Montagem com `montar_ad.py`, resolução 720.

## Revisão (`ugc\revisar.py NN` e `solto.py`)
- **Whisper es:** o texto bate com o roteiro nos 5 vídeos. Nenhuma palavra proibida (Maya Verra, 60/45 días, EE.UU., Ozempic, TikTok, COFEPRIS, preço, link, kg/libras).
- **Folha de contato** (1 quadro a cada 2 s): sem problemas.
- **Bordas dos insertos:** um único corte limpo em cada uma, sem quadro solto.
- **Silêncio no fim:** nenhum.

## Pendências e revisão manual
- **Setas de CTA:** ficam só os ~2–3 s finais na tela, porque o "Toca" está no fim da fala. Se quiser mais tempo de seta, dá para estender o último quadro em ~1,5 s.
- **Tamanho:** ~26 MB cada, abaixo do limite de 30 MB.
- **UGC 05:** no inserto P2 (~33 s), o selo cobre a parte de baixo do rótulo.
- **Estilo dos takes:** os takes V1–V3 têm estética de render 3D/IA. Contrastam um pouco com o avatar realista. Vale conferir se agrada.
- **Pronúncia:** "stillingia" saiu como "estilingia". É a pronúncia natural em espanhol, aceitável.
- **Para o dono da conta:** corrigir a chave ElevenLabs na integração do HeyGen, para as vozes clonadas privadas voltarem a funcionar.
- **Texto do anúncio (.txt):** não foi gerado.
