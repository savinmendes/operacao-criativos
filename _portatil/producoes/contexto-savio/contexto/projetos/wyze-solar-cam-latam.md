# Wyze Solar Cam Pan 2K: EN → ES LATAM

> Tradução de 16 vídeos de criadores (inglês) da câmera solar Wyze para espanhol LATAM, com avatar HeyGen no lugar do rosto dos criadores. Abra ao continuar esse lote ou ao traduzir vídeo de criador terceiro.

## Contexto de uso
- **Frente:** COD/e-commerce LATAM (oferta ainda não confirmada). A pessoa vende a **Wyze original** (wyze.com/products/wyze-solar-cam-pan-2k) em toda a LATAM, então **a marca Wyze fica** na fala, no app, na caixa, nas marcas d'água e no relevo da câmera.
- **Pasta:** `Downloads\WYZ-CAMARA-LATAM\` (atalho `entregas-wyze/`). Estudo em `ESTUDO-WYZE-LATAM.md` (05/10/2026); produção em `producao\` com `00-RELATORIO-PRODUCAO.md`; briefing em `producao\_trabalho\BRIEFING-AGENTES.md`; por AD em `producao\_trabalho\adNN\RELATORIO.md` + `roteiro_es.txt`.
- **Entregue em 05/10/2026:** 16 ADs em 720x1280 (`AD NN - WYZE-SOLAR-CAM-PAN-<TEMA>-ES-LATAM.mp4`), revisados com whisper es + whisper en + folha de contato. O vídeo 17 (Bulb Cam, outro produto) foi excluído pela pessoa. 08, 10 e 13 usam o mesmo roteiro com filmagens diferentes.
- **Specs oficiais usadas (só estas):** 2K, 360°/70°, visão noturna a cor, refletor, sirene 105 dB, áudio bidirecional, IP65, 1 h de sol/dia, cabo de 10 ft (3 m), microSD, sem assinatura obrigatória.
- **Saíram de todos:** preço, desconto, cupom, "link abaixo", carrinho do TikTok, datas comemorativas (Natal, Halloween), HOA, FedEx, medidas em pés, e claims fora da ficha ("#1 na América", "funciona sem sol", "detecta pacotes", "Alexa" etc.).
- **CTA:** "Pídela hoy. Toca el botón de abajo y pide la tuya." Sem selo de oferta. Cada `_trabalho\adNN\` tem `receita_com_selo.json` pronta com "PAGO CONTRA ENTREGA / ¡PAGAS AL RECIBIR!".
- **Vozes:** nenhum criador clonado (são terceiros) — modo B1: voz de catálogo ElevenLabs em espanhol latino + avatar HeyGen nos vídeos com rosto (01, 06, 12, 14, 16). Avatar criado: "WYZE Review Latino 35" id `430f346689b68545f1adbea9f186bd83`. No 06, diálogo entre dois avatares (esse + "Lymphoria UGC Latina 48").
- **Custo real:** ~US$ 2,40 (ElevenLabs) + ~115 créditos HeyGen (saldo 9.072 → ~9.009). Kling: US$ 0.
- **Pendências / revisão manual:**
  - confirmar a oferta (COD/frete/garantia) para renderizar o selo nos 16 (sem custo, ~20 min);
  - AD 02 saiu com voz feminina; AD 04 sem música (o fundo ainda tinha voz em inglês); AD 07 com decoração de Halloween discreta e van da Amazon ao fundo; AD 11 casal com rosto pequeno sem desfoque; AD 12 logo YETI espelhado na camiseta; ADs 14/16 com o mesmo avatar e voz diferente da do 01/12/06; fala ambígua no 06;
  - pronúncia de "Wyze" (sai "uaiz");
  - textos do anúncio não gerados.

## Lógica de uso
1. **Estudo:** transcrever (whisper) + folhas de contato + leitura de tela por agentes; tabela por vídeo do que precisa sair (fala e tela) e se há rosto.
2. **Roteiro ES:** só specs oficiais; cortar tudo de outro mercado; CTA padrão.
3. **Sem rosto do criador:** narração com voz de catálogo, legenda queimada em inglês coberta por faixa com legenda nova, `preparar_corpo_traducao.py` + `montar_ad.py` (base: scripts do lote Podadora).
4. **Com rosto do criador terceiro:** o criador real não aparece nem ganha fala nova. Corpo com `montar_corpo_avatar.py plano.json` (avatar HeyGen intercalado com takes de produto recortados abaixo do rosto). Desde 06/10/2026 a pessoa pode escolher por lote o modo B2 (mesmo criador com clone + lipsync), **só com autorização do criador confirmada**.
5. Revisão com whisper no idioma alvo + residual em inglês + folha.
- **Bug encontrado aqui (corrigido em 05/10/2026 no kit):** no AD 06 o caminho rápido do `montar_ad.py` abriu um buraco de 3 s no áudio (8,5–11,5 s) e não desenhou as setas. Causa: concat `-c copy` de takes com metadados de cor diferentes (HeyGen × original) reconfigurava o filtergraph. Hoje o corpo entra com `-reinit_filter 0`. Conferir com `ffprobe -select_streams a -show_entries packet=pts_time` (o `silencedetect` não pega).
- **Se a pessoa pedir mais:** renderizar os 16 com selo quando a oferta for confirmada; trocar voz do AD 02 (~US$ 0,05); refazer 14/16 com a voz Mario (~US$ 0,13 + ~25 créditos cada); desfocar YETI; gerar textos.

## Relacionados
- [../05-traducao-de-criativos.md](../05-traducao-de-criativos.md)
- [../09-lipsync-e-avatar-heygen.md](../09-lipsync-e-avatar-heygen.md)
- [podadora-chile.md](podadora-chile.md) (mesmo fluxo EN→ES), [mopa-h2o-x5-es.md](mopa-h2o-x5-es.md)
