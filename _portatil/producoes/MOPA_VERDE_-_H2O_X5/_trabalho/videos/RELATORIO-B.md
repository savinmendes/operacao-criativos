# Relatório do agente B: vídeos 24, 46 (mestra 9:16) e 31 (par 4:5)

Data: 08/10/2026. Entregas em `ES-LATAM\VIDEOS\`. Trabalho em `_trabalho\videos\24\`, `46\` e `31\`.

## Resumo
| Arquivo | Formato | Duração | Tamanho | Voz (voice_id) | Caracteres TTS | Revisão |
|---|---|---|---|---|---|---|
| `24 AD - ES.mp4` | 720x1280 | 21,70 s | 12,1 MB | `GnAzF1UybYKv51msoOSw` ("MOPA X5 narradora 24") | 285 | OK |
| `46 AD - ES.mp4` | 720x1280 | 25,10 s | 16,4 MB | `gm4qx4lkjb5aDUefAhv1` ("MOPA X5 narradora 31") | 385 | OK |
| `31 AD - ES.mp4` | 720x900 | 25,10 s | 9,1 MB | mesma do 46 (mesma narração, sem TTS extra) | 0 | OK em tudo; o único "PROBLEMA" é a resolução 720x900, exigida pelo briefing (ver abaixo) |

**Total de TTS: 670 caracteres** (limite da parte B: 2.000), ≈ US$0,11, mais 2 clones de voz.

## Roteiros finais (narração)
**24**: "Protege a tu familia del 99 % de los gérmenes con el H2O X5. Así de fácil. Úsalo en pisos, superficies y alfombras: todo queda impecable en minutos. Sin químicos, seguro con niños y mascotas. Un solo aparato para tener tu casa realmente limpia, sin estrés. Haz clic en Más información."

**46 / 31**: "Una limpieza rápida y eficaz que de verdad te facilita la vida. El H2O X5 es un potente limpiador a vapor 5 en 1 para toda tu casa, con un solo aparato. Pisos, alfombras, ventanas, azulejos y más: el vapor quita la mugre sin químicos agresivos. Liviano y fácil de manejar, te ahorra tiempo y limpia más a fondo. Menos tiempo limpiando, más tiempo viviendo. Haz clic en Más información."

Os roteiros de `roteiros\24_es.txt` e `31_es.txt` foram conferidos contra a ficha e as decisões e usados sem mudar o texto. Velocidade 1,0x (nenhum ajuste de atempo).

## Texto da tela
- **24:** o título "Protect your family from 99% of germs with this one item" (0–5,6 s) foi coberto por uma caixa branca opaca com "Protege a tu familia / del 99 % de los gérmenes / con un solo aparato". O título "H2O X5 Steam Cleaner" (13,4 s até o fim) virou "Limpiador a vapor H2O X5". O original tem texto branco sem caixa, que não dá para cobrir no mesmo estilo; usei a caixa branca padrão do kit.
- **46/31:** a caixa verde "Fast, effective cleaning that actually makes life easier" (0–3,36 s) foi redesenhada opaca, na mesma cor (33,168,12) e na mesma posição, com texto branco: "Una limpieza rápida / y eficaz que de verdad / te facilita la vida".
- **Legenda queimada em inglês:** coberta por uma faixa preta opaca (24: y 955–1075; 46: y 980–1075). A legenda nova em espanhol fica em cima da faixa e vem do alinhamento do ElevenLabs. "H2O X5", "99%" e "5 en 1" ficam inteiros no mesmo bloco, com espaço não separável.
- Ficaram só textos impressos: "H2O X5" no aparelho e na caixa, "5 in 1 Steam Cleaning System", "IMPORTANT", "OPEN THIS SIDE" na caixa de papelão e "BOSCH" no micro-ondas.
- **Selo** "PAGO CONTRA ENTREGA": no 24, no topo (y=60 na escala de 1920); no 46/31, em y=300. **Setas** fora da faixa: no 24, cta.y=1190; no 46, 1210. A faixa aqui fica no meio-baixo da tela, e não no rodapé. Por isso não usei o y≈1110/1490 do briefing, que poria as setas em cima da faixa.
- **Áudio:** `<id>_no_vocals.wav` (volume 1,0) + narração clonada. O fim foi congelado para caber o CTA: 2,14 s no 24 e 1,07 s no 46/31.

## Par 4:5 (31)
O 31 é um recorte 720x900 (y 190–1090) do `46 AD - ES.mp4` final: mesma montagem, mesmo texto e mesma voz. O selo, a caixa verde, as setas e a legenda foram posicionados no 46 para caber nessa janela, e todos aparecem inteiros no 31 (conferido na folha `31\31 AD - ES_revisao.jpg`).

## Revisão (`revisar_ad.py` pelo PowerShell, `--idioma es --idioma-residual en`, proibidos em `_trabalho\videos\proibidos.txt`)
- **24: RESULTADO OK.** Decodificação OK, sem salto de pts, sem silêncio, sem quadro solto, setas no último quadro e fora da faixa. Termos proibidos: nenhum. O whisper es bate com o roteiro. O whisper en só traduziu a fala em espanhol: nenhuma fala antiga.
- **46: RESULTADO OK.** Mesmos itens. O whisper es bate com o roteiro, com erros de grafia do modelo small: "XC5", "Pizos", "Libiano". O whisper en transcreveu o próprio espanhol (sem fala inglesa residual).
- **31:** os mesmos itens passaram. O único PROBLEMA apontado é "resolução 720x900 (esperado 720x1280 ou 1080x1920)": o revisor só aceita 9:16, e o 720x900 é exigido pelo briefing. Fora isso, o resultado é igual ao do 46, que saiu OK.
- Folhas de 1 quadro/s conferidas a olho (`*_revisao.jpg`): nenhum inglês na tela além da marca e de textos impressos no produto ou na caixa.

## Pendências e decisões registradas
- **"Seguro con niños y mascotas" (24)** não está na ficha. Foi mantido por decisão da pessoa ("manter todas as alegações"), mas ainda precisa de revisão manual para compliance.
- **31:** o revisor marca a resolução 4:5 como problema, mas é o formato pedido. Não é defeito.
- **Pronúncia de "H2O X5":** a voz clonada lê a marca em espanhol. Vale ouvir para confirmar.
- **Clone com amostras curtas** (19 s e 24 s): a qualidade fica limitada. Vale ouvir.
