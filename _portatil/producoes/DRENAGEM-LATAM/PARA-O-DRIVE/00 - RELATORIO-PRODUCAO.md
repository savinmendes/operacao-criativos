# Produção noturna Drenagem LATAM (Lymphoria): 04 → 05/10/2026

**55 criativos entregues: 20 ADs adaptados (10 longos e 10 curtos), 5 UGC e 30 variações de gancho.**
- Todos em 720x1280 e todos revisados (Whisper es + folha de contato).
- Oferta universal para CL, GT e EC: envío gratis, pagas al recibir, 90 días de garantía. Sem preço. As libras foram mantidas.

## Custo real

| Bloco | Kling | Voz (ElevenLabs) | Total |
|---|---|---|---|
| AD 01 | 4,24 | 0,10 | 4,34 |
| AD 03 | 0 (script `band_fix`) | 0,10 | 0,10 |
| AD 04 | 1,41 (2 takes descartados) | 0,07 | 1,48 |
| AD 05 + AD 20 | 4,94 | 0,20 | 5,14 |
| AD 18 + AD 30 | 6,35 | 0,13 | 6,48 |
| AD 21 + AD 25 | 5,65 | 0,17 | 5,82 |
| AD 24 | 0 (script `band_fix`) | 0,10 | 0,10 |
| 5 UGC (HeyGen) | — | 0,70 | 0,70 + 76 créditos HeyGen |
| 30 variações | — | 0,59 | 0,59 |
| **Total** | **22,59** | **2,16** | **≈ US$ 24,75**, abaixo dos US$ 35 orçados |

O custo ficou menor porque o Kling estragava o rosto dos personagens Pixar. Por isso foi criado o `band_fix.py`, que reescreve o rótulo de graça. Ele foi usado nos ADs 01, 03, 04, 24, 25 e 30.

## Arquivos

| AD | Longo | Curto |
|---|---|---|
| 01 MENOPAUSIA | 7:19 | 1:25 |
| 03 MEJOR-AMIGA | 7:24 (era 13:37) | 1:29 |
| 04 MUJER-28 | 6:13 | 1:27 |
| 05 ESPOSO-NO-ME-MIRABA (gancho novo, sem cena sexual) | 4:58 | 1:28 |
| 18 GOTITAS-DIA-A-DIA (era Herbalia) | 1:36 | 0:58 |
| 20 PANZA-HOMBRE (era Lymphoria EUA) | 4:56 | 1:24 |
| 21 EX-TARGET (era Lymphoria EUA, menção ao TikTok trocada) | 5:18 | 1:19 |
| 24 HOMBRE-40 (era 12:56) | 6:48 | 1:28 |
| 25 VECINO | 4:59 | 1:12 |
| 30 EXESPOSO-FILA | 5:27 | 1:22 |

- **UGC 01–05** (avatar HeyGen, ~50 s cada): CARRITO, PIRATAS, DISCULPA, HINCHAMOS e PAGAS-AL-RECIBIR.
- **VARIACOES:**
  - **VAR 01–10:** os 10 ganchos sobre o corpo do AD 20 (masculino; os ganchos foram adaptados para homem).
  - **VAR 11–20:** os 10 ganchos sobre o corpo do AD 05.
  - **VAR 21–30:** os 10 ganchos sobre o corpo do AD 30.
- **Tamanho:** os longos e as variações têm de 35 a 54 MB, acima do limite de 30 MB do kit. O Meta aceita até 4 GB, então não há problema para subir.

## Bug encontrado e corrigido durante a noite
O `encaixar_edit.py` do kit copiava todo pixel branco do quadro original de volta por cima do take do Kling. Com isso, o "MAYA VERRA" branco do rótulo reaparecia, e só era visível com zoom.
- **Nesta produção:** os ADs 05, 18 e 25 e as variações 11–20 foram refeitos de graça.
- **Kit:** corrigido, com a armadilha anotada no CLAUDE.md.
- **Lote antigo LHYMPORIA:** vários ADs entregues têm o defeito. O pior é o AD 01, com uma faixa branca no rosto. Foram geradas **13 versões v2 corrigidas** (ADs 01, 02, 03, 04, 09, 10, 11, 12, 13, 14, 16, 19 e 22) em `LHYMPORIA AD 01-20\lymphoria\_v2_corrigidos\`, com o relatório em `RELATORIO-V2.md`.
  - O áudio é idêntico ao entregue, e os arquivos entregues não foram tocados.
  - Ainda sobram restos do rótulo dentro da faixa da legenda nos ADs 03, 09, 22, 13 e 01. Um v3 grátis resolve a maior parte (teste em `_v2_trabalho\teste_v3\cmp_v2_v3.jpg`).
  - Vale olhar o AD 19 t2: foi mantido como estava, mas parece ter mancha.

## Para você olhar (revisão manual)
- **Risco no Meta:**
  - corpo e antes/depois: AD 25 (cueca/abdômen, 3:24), AD 24 (sem camisa, 1:24 e 3:20), AD 21 (moletom → vestido), AD 30 (semanas 1/3/6 e decote);
  - gancho "fingí" no AD 01 (implícito).
- **AD 20:** o trecho do TRT/hormônios foi removido por segurança. Também foi removido no AD 24, mas no AD 25 a fala "no necesitas más hormonas" ficou.
- **AD 21:** o rótulo do frasco está em inglês, "lymphatic drainage".
- **Legendas queimadas:** sobram restos de 0,3–0,8 s em algumas emendas dos curtos e nos longos encurtados (03 e 24). Um vestígio leve também aparece no gancho do AD 05.
- **Variações:** ouça a emenda das VAR 15, 17 e 19 (gancho de produto → "Así que culpé a mi cuerpo").
- **UGC:**
  - as cenas de produto são 3D e contrastam um pouco com o avatar realista;
  - no UGC 05, aos 33 s, o selo cobre parte do rótulo.
- **HeyGen:** a integração ElevenLabs está com o "key ID" salvo no lugar da chave `sk_…` (VOICE_CONFIG_ERROR). Corrija nas configurações do HeyGen.
- **Textos do anúncio** (título e texto principal) ainda não foram gerados.

Detalhes de cada AD: `producao\_trabalho\adNN\RELATORIO.md`.
