---
name: traduzir-criativo
description: Adapta um lote de criativos de vídeo de um idioma/mercado para outro (ex.: inglês → espanhol LATAM) — estudo do lote, briefing único para agentes em paralelo, narração nova sem rosto de terceiro falando, legenda queimada coberta, CTA e selo do mercado novo, revisão e entrega com relatório. Use quando pedirem para traduzir, dublar, "passar para espanhol" ou adaptar vídeos de outro país.
---

# Traduzir criativo

Fluxo de lote. Montagem, geração de mídia e revisão seguem `editar-criativo`, `gerar-midia-ia` e `revisar-criativo`; aqui só está o que é próprio da tradução. Leia antes o `CLAUDE.md` do kit (seção "Tradução de criativo de outro idioma" e as armadilhas). Nunca leia nem imprima `.env`.

## 1. Estudo do lote (antes de gastar qualquer coisa)
1. Baixe sempre na **maior qualidade disponível (≥720p)**: na Biblioteca do Meta, o `video_hd_url` dos dados da página, não o vídeo do player (360p); confira com `ffprobe` e deduplique por md5. Renomeie os originais para `originais/NN.mp4` e gere `indice-arquivos.csv` (nome original → NN).
2. Agentes em paralelo (1 por 3–6 vídeos), cada um com: transcrição faster-whisper (idioma automático, `cpu_threads=4`), folha de contato (1 quadro/s) e leitura dos quadros em tamanho cheio. Whisper e OCR em sequência, nunca juntos.
3. Para cada vídeo, listar o que **não serve** no mercado alvo: preço/moeda, país e bandeira, plataforma de origem (carrinho, "link abaixo"), cupom/desconto, data/estação/feriado, escassez não comprovável ("esgotou X vezes"), claims fora da ficha oficial, rosto de criador de terceiro, legenda queimada, dados pessoais em cena (rosto de terceiro, data/hora, número de casa, @perfil), medidas em unidade estrangeira.
4. **Produto certo:** compare o produto que aparece nos criativos com o link ou a ficha que a pessoa vende (modelo, cor, formato, potência). Se não bater, pare e pergunte antes de orçar. Um lote já ia sair com um modelo de outra cor e outra potência.
5. **Conflitos com a ficha oficial**, listados por vídeo: número vendido, garantia, peso, potência, "frete grátis", moeda. A ficha oficial vale mais que o criativo.
6. **Amostra de voz** de cada narrador (voz isolada pelo demucs, o máximo de fala limpa). Com menos de 30 s o clone sai pior: avise.
7. Marcar duplicados (mesmo roteiro ou o **mesmo vídeo em outro formato**, 9:16 × 4:5 × 1:1; compare quadros) e classificar: **A** sem rosto (só mãos/produto), **B** com rosto do criador, **C** outro produto, **D** sem narração (só música + texto na tela). Duplicado de formato: monte uma mestra 9:16 e gere o par no outro formato com o mesmo texto, a mesma voz e o mesmo tempo.
8. Entregar `ESTUDO-<lote>.md` com: tabela por vídeo, lista de alegações proibidas, classificação, orçamento (custo em US$ + tempo + opção paga mais rápida, lado a lado) e as **perguntas de bloqueio**: a marca é da pessoa ou revende a original? ficha técnica oficial (link)? oferta e países (COD, frete, garantia, preço)? quais vídeos excluir? **itens de compliance sensíveis (promessa de dinheiro/cura, ameaça, urgência, famoso, depoimento com resultado, cenas de hospital/remédio/dinheiro): manter ou suavizar?** (nunca suavizar sem a resposta) **criadores com rosto (grupo B): avatar próprio (B1, padrão) ou o mesmo criador (B2, só com autorização do criador)?** Sem essas respostas, não produzir.

## 2. Briefing único do lote
Escreva `producao/_trabalho/BRIEFING-AGENTES.md` e passe o mesmo arquivo a todos os agentes (1 agente por 1–2 vídeos). Conteúdo obrigatório:
- onde estão originais, transcrições, folhas, kit e o exemplo pronto de um lote anterior;
- **ficha oficial** (só o que pode ser dito) e a lista de trocas fixas ("funciona sem X" → frase segura; medida → unidade local);
- regra de marca: fica se a pessoa vende a original; senão desfocar/cobrir/Kling;
- **CTA** falado + palavra das setas; oferta só se confirmada (sem preço, país, frete ou garantia inventados);
- **voz**: narrador de terceiro → voz de catálogo (mesmo gênero e energia, a mesma em todos os vídeos do mesmo criador); clonar só no modo B2 (autorização do criador confirmada); marca própria → clone permitido (`clonar_voz.py`);
- fluxo A e B, limites de CPU/GPU (`-threads 4`, `PYTHONIOENCODING=utf-8`), teto de créditos por vídeo, revisão obrigatória e formato do relatório;
- **marca falada:** escreva no texto do TTS a pronúncia por extenso no idioma alvo (siglas e números soletrados) e use a mesma grafia em todos os vídeos. Senão, cada voz pronuncia de um jeito;
- "não pergunte nada; na dúvida escolha o lado seguro e registre a decisão".

## 3. Grupo A (sem rosto)
1. `python -m demucs --two-stems=vocals` → usar só o `no_vocals.wav` (GPU liberada: `-d cuda`). Se a voz original ainda vazar no fundo, entregar sem trilha e anotar.
2. Roteiro no idioma alvo com a **mesma estrutura** (gancho, benefícios, CTA), ~15% mais curto que o original, sem o que o estudo listou. Salvar `adNN/roteiro_<idioma>.txt`.
3. `tts_elevenlabs.py --arquivo roteiro.txt` (gera o alinhamento). Não cabe? Enxugue o texto ou estique cenas com congelamento curto; velocidade da voz ≤ 1,1x; frase a frase no tempo das cenas.
4. `preparar_corpo_traducao.py prep.json` (modelo em `exemplos/traducao_exemplo.json`): corta a capa, cobre a legenda queimada com faixa opaca (alpha ≥ 250) e o título do gancho com caixa nova, troca o áudio (fundo + narração), gera o alinhamento deslocado. Cenas proibidas: cortar ou `desfocar_regioes.py`.
5. `montar_ad.py` em `"resolucao": "720"` com legenda pelo alinhamento e setas na palavra do CTA; `revisar_ad.py` no final.

## 4. Grupo B (rosto do criador) — a pessoa escolhe o modo por lote ou por vídeo
**B2 — mesmo criador** (só quando a pessoa confirma que o criador autorizou o uso de imagem e voz para fala nova/tradução: contrato, licença de UGC ou permissão direta):
- Registre no estudo e no `RELATORIO.md`: "uso do criador autorizado pela pessoa em DD/MM/AAAA" e quais vídeos.
- Voz: procure antes em `VOZES-CLONADAS.md` do kit (reutilize; depois de clonar, acrescente a linha). `clonar_voz.py` a partir de um trecho limpo do criador (1 clone por criador, reutilizado em todos os vídeos dele) → `tts_elevenlabs.py` com o roteiro traduzido.
- Rosto: lipsync do HeyGen sobre o vídeo original (ou tradução de vídeo do HeyGen com o roteiro revisado), medindo créditos no 1º. Cubra a legenda queimada e siga o grupo A no resto.
  - **Método do lipsync.** A receita completa está nas armadilhas do `CLAUDE.md`. Em resumo:
    - `mode speed`;
    - entrada recortada só no rosto de quem fala, com o áudio original;
    - o áudio novo vai separado;
    - trechos de até 12 s;
    - colar de volta com elipse na boca e no queixo;
    - leitura e gravação com cor exata.
  - **Aceite:** `checar_lipsync.py` com índice de pausa ≤ 0,6.
  - **Plano B sem custo:** boca fechada colada nas pausas.
- **Piloto antes do lote:** produza 1 vídeo completo e mostre à pessoa. Só rode o lote depois que ela aprovar o piloto. No lote Oración o 1º piloto saiu com o lipsync errado e o método foi refeito antes de gastar com os outros 17.
- **Mantenha o plano original.** Com o criador da própria pessoa, um avatar completo gerado (imagem parecida no Flora + avatar HeyGen) foi **rejeitado**: ela preferiu o vídeo original com lipsync. Ofereça avatar só como alternativa.
- Sem autorização confirmada, **não** use B2: vá de B1.

**B1 — avatar próprio** (padrão):
- Nada de lipsync nem fala nova sobre o rosto real.
- Reaproveite só takes sem o rosto (produto, mãos, app, gravações); recorte 9:16 abaixo do rosto quando preciso.
- Parte falada com **avatar próprio** (HeyGen, via `gerar-midia-ia`): áudio do `tts_elevenlabs.py` enviado para o lipsync do avatar. Meça os créditos no 1º vídeo e fixe o teto antes de rodar os outros.
- `montar_corpo_avatar.py plano.json`: intercala avatar (~40–60%) com os takes sem rosto (tela cheia ou dividida), depois `montar_ad.py` + `revisar_ad.py`.

## 4b. Mesmo idioma, outro país (localização)
Quando o idioma já serve e só o país muda (ex.: inglês dos EUA → Reino Unido), **não refaça o vídeo**: troque só as frases que não servem.
1. **Mapa de troca:** transcrição palavra a palavra + leitura da tela, com a lista do kit `exemplos/termos-por-pais.md`. Procure país, moeda, plataforma de venda (nome do app, "carrinho laranja", "on here"), redes de loja e pratos de rede local, unidades e grafia local. Proponha a troca frase a frase (original → nova) e aprove com a pessoa.
2. **Emendas em pausa natural**, medidas no envelope da voz isolada (demucs). Se a frase não tem pausa antes, comece a troca na frase anterior e regrave as mesmas palavras.
3. **Voz clonada** da própria pessoa que fala, a partir da voz isolada. A fala nova cabe no tempo da original (±0,3 s, velocidade 0,9–1,1x) e fica no mesmo LUFS. Fora da troca o áudio fica original.
4. **Rosto:** lipsync só no trecho (método B2). Antes de mandar, veja se a boca aparece: com a boca coberta (produto na frente, mão, desfoque), o HeyGen devolve a boca intacta e gasta crédito. Nesse caso troque só o áudio. Com 2 pessoas no plano, descubra quem diz a frase pela abertura da boca.
5. **Tela:** apague a interface da plataforma de origem e o país nas capturas (avaliações, comentários). Prefira trocar a captura inteira quando a interface aparece demais.
6. **Fala contínua, sem pausa:** o índice de pausa não dá número. Aprove a olho, quadro a quadro, e avise a pessoa para conferir.

## 4c. Imagens (estáticos e carrossel)
- Gere a imagem traduzida por **edição de imagem com IA** (`gerar-midia-ia`), com a lista exata de textos original → novo e "nada mais muda". Em geral passa na 1ª tentativa; refaça no máximo 1 vez; se falhar, cubra e reescreva o texto localmente.
- Confira com zoom: grafia, acentos, produto igual, nada a mais ou a menos. Entregue uma folha com original e tradução lado a lado.
- Liste na entrega o que a arte afirma e a ficha não confirma (garantia, frete, moeda).

## 5. Selo de oferta
Só com oferta confirmada pela pessoa. Sem confirmação, deixe `adNN/receita_com_selo.json` pronta (selo "pago contra entrega" ou o da oferta) e registre no relatório que falta renderizar.

## 6. Revisão (por vídeo final)
`revisar_ad.py` + Whisper no idioma alvo (texto bate com o roteiro; nenhum item proibido) + Whisper no idioma original (nenhuma fala antiga por baixo) + folha de contato 1 quadro/s (nenhuma legenda antiga, quadro solto no corte, silêncio no fim, seta sobre a faixa). Depois `revisar-criativo`.

Em lote com lipsync, divida em lotes A/B/C para um **revisor independente**. Ele mede o índice de pausa no rosto de quem fala e manda refazer o que reprovar; repita até passar. No lote Oración, 10 de 18 vídeos voltaram pelo menos 1 vez.

## 6b. Lições de lotes anteriores
- **CTA na forma nativa, não literal:** traduzir "Toca «Más información»" ao pé da letra deu "Touche « En savoir plus »", que soa como tradução. O revisor trocou para "Appuie sur « En savoir plus »". Peça ao revisor que confira o CTA e os verbos de ação com um nativo em mente.
- **Nome próprio na forma local** (santo, cidade, instituição): use a grafia que o público do idioma usa (ex.: San Benito → "saint Benoît" em francês) e mantenha a mesma na fala, na legenda e no texto do anúncio.
- **Lipsync deixa o rosto mais mole** que o original: cole só boca e queixo sobre o take original (ver `gerar-midia-ia`, Avatar falando) e compare a nitidez.
- **Trecho reprovado se refaz sozinho:** com um trecho de lipsync acima do limite, gere de novo só esse trecho (mais curto, cortado nas pausas), sem refazer o vídeo inteiro.
- **True peak:** confira ≤ −1 dBTP depois da mixagem; já saiu −0,3 e precisou de limitador.

## 7. Entrega
- Pasta numerada: `producao/AD NN - <PRODUTO>-<TEMA>-<IDIOMA>-<MERCADO>.mp4`, trabalho em `producao/_trabalho/adNN/` com `RELATORIO.md` (voz usada, caracteres TTS, créditos, o que saiu/trocou, revisão, pendências).
- `producao/00-RELATORIO-PRODUCAO.md`: custo real × orçado, decisões aplicadas a todos, tabela de ADs, lista "para você olhar" (revisão manual), bugs do kit encontrados.
- Textos de anúncio por AD: título (≤ 40 caracteres), descrição, texto principal e versão TikTok ≤ 100 caracteres, com compliance. Confira os limites e os termos proibidos por script. Use só dados da ficha e escreva na grafia do país (ex.: inglês britânico).
- **Formatos 4:5 e 1:1:** o kit monta e revisa direto. Na receita do `montar_ad.py` e no `prep.json` do `preparar_corpo_traducao.py`, ponha `"formato": "4:5"` (ou `"1:1"`) junto de `"resolucao"` (720 → 720×900 / 720×720). Posições em px do quadro base de 1080 de largura do formato (1080×1350 / 1080×1080) ou `y_rel` (0–1 da altura); sem posição, o kit usa o padrão do formato. Revise com `revisar_ad.py --formato 4:5`. Não escreva compositor próprio do lote para isso. Par de formato: mesma narração/alinhamento, só troca `formato` (e as posições, se precisar).
- Atualize a memória do projeto (lote, método, pendências) para o próximo lote partir daqui.
