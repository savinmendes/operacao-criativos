# Briefing técnico CÉSPED no ElevenLabs (aprovado pela pessoa em 15/10/2026)

**Roteiro:** a sua seção em `C:\Users\PICHAU\Downloads\VENCEDORES-3-PRODUTOS\CESPED\PERSONAS_CESPED_C1-C10.md`. Siga à risca, sem suavizar nada. A pessoa decidiu que tudo passa no Facebook.

**Pipeline técnico (MCP do ElevenLabs, imagens, vídeos, voz, QA, montagem, revisão):** é o mesmo dos perfumes, em `C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\BRIEFING_PERSONAS_ELEVEN.md`. Leia inteiro, incluindo as "Lições da 1ª onda". **Diferenças em relação aos perfumes:**

## Material compartilhado (só leitura, não altere)
Pasta: `C:\Users\PICHAU\Downloads\VENCEDORES-3-PRODUTOS\CESPED\BANCO\`

`V1_720.mp4` (720×1280, 37 s; demonstração com a criadora de corpo inteiro, uso liberado pela pessoa):

| Trecho | Conteúdo |
|---|---|
| 0–5,5 s | **antes/depois** (corredor com mato → faixa limpa) |
| 6–10 s | rodas |
| 11–15 s | borda da calçada |
| 16–17 s | POV do gatilho |
| 18–22 s | faixas no mato alto |
| 24–33 s | gramado lateral |

**Não use 34–37 s** (close no rosto da criadora).

`V2_limpo_13-46.mp4` (720×1280, 33 s, sem legenda nem rodapé; o tempo 0 equivale a 13 s do original):

| Trecho | Conteúdo |
|---|---|
| 0–7 s | deck e horta («cortapasto pesado / desbrozadoras que se traban») |
| 7–16 s | corredor de brita, rodas, uma mão |
| 17–23 s | corredor lateral com mato |
| 23–25,5 s | **kit na mesa** (lâminas, rodas, 2 baterias, carregador) |
| 26–33 s | mato alto perto do galpão |

`ref/`: quadros do **produto original**, para usar como referência nas imagens de IA:

| Arquivo | Conteúdo |
|---|---|
| `v2_9.png` | produto inteiro em uso |
| `v1_35.png` | criadora segurando o produto |
| `v2_23.png` | kit na mesa |
| `v2_27.png` | uso no mato alto |

Escolha os takes reais de modo que o vídeo não repita nenhum trecho. Para diversificar o lote, comece o bloco 4 por um trecho diferente conforme o seu número de C (ex.: C ímpar começa pelo V2, C par pelo V1).

## Produto nas imagens de IA
- Sempre parta da referência real (`ref/v2_9.png` ou `ref/v1_35.png`, ligada ao nó de imagem) com o pedido «keep the exact same cordless trimmer from the reference: lime-green and black motor head, silver telescopic pole, two black wheels with lime-green hubs, trigger handle; do not change its design».
- Confira com zoom. Se não ficar idêntico, gere a cena **sem o produto** ou com o produto fora de foco. Nunca invente um produto.
- A IA nunca mostra a máquina cortando.

## Telas de celular (WhatsApp, Facebook, mensagens)
- Faça por código, com PIL: retângulo arredondado no estilo do app (verde do WhatsApp ou azul do Facebook), fonte Arial/Segoe, nomes e textos exatamente como no roteiro.
- Sobreponha a tela na cena da persona olhando o celular, ou em tela cheia por 2–3 s com um leve zoom.
- A IA não gera texto de tela.
- Sem logo oficial de app e sem nomes de pessoas reais.

## Voz
- **Narração** (blocos 3–6, incluindo o mecanismo comum e o CTA): a voz definida para a sua persona.
- **Falas de outros personagens:** as nativas do Seedance.
- O personagem principal, quando fala no Seedance (gancho ou persona), passa por STS para a voz dele, como nos perfumes.
- No CTA, diga «noventa días».
- **Selo no topo das cenas de IA:** use o overlay do CÉSPED em `BANCO\overlay_selo_cesped.png`, se existir. Se não existir, crie na sua pasta, no mesmo estilo do selo dos perfumes (`LOTE-15-10\_trabalho\A\overlay_selo.png`), com o texto «PAGO CONTRA ENTREGA · DESPACHO GRATIS».

## Pasta, painel e saída
- Pasta: `C:\Users\PICHAU\Downloads\VENCEDORES-3-PRODUTOS\CESPED\PROD-C<N>-<NOME>\`
- Painel: `c<N>`
- Saída: `CESPED-CL_C<N>_<NOME>.mp4` + `_narracion.txt`. O texto do anúncio vai em ES-CL, com título ≤ 40 caracteres e o texto principal com:
  - gancho da história;
  - 3 en 1, ruedas, cuchilla de metal, inalámbrica;
  - 🚚 Despacho gratis a todo Chile;
  - 💳 Pagas al recibir;
  - 🛡️ 90 días de garantía;
  - sem preço.
- Teto: 35 mil créditos.
- Revisão: `revisar_ad.py --idioma es --proibidos "pícale,dólares"`. Precisa dar OK. Olhe a folha inteira e abra o vídeo.
