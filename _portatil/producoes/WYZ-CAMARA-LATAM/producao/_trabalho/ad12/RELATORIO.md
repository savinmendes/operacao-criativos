# AD 12 — Grupo B (criador falando para a câmera) — relatório

- **Arquivo:** `producao\AD 12 - WYZE-SOLAR-CAM-PAN-LA-QUE-QUIERO-ES-LATAM.mp4`. Tem 41,8 s (o original tem 47 s), 720x1280 e 26,2 MB, e decodifica sem erro.
- **Voz:** a mesma do AD 01, "WYZE 01-12 Mario animado" (`tomkxGQGz4b1kE0EM722`). É uma voz de catálogo latina masculina, **não clonada**, com eleven_multilingual_v2 na velocidade 1,0.
- **TTS:** 726 caracteres (~US$ 0,12).
- **HeyGen:**
  - Avatar "WYZE Review Latino 35" (`430f346689b68545f1adbea9f186bd83`), o mesmo do AD 01.
  - Vídeo `6392d81ce31938081a0ab94aed52387b`.
  - **12 créditos** (o saldo foi de 9.021 para 9.009, medido logo antes e logo depois).
- **Roteiro:** está em `roteiro_es.txt`.

## O que foi trocado ou cortado
- **Rosto do criador:** saiu do vídeo inteiro. A montagem tem três tipos de trecho:
  - **Gancho (0 a 1,8 s):** close do painel solar e da câmera, recortado à direita do criador (sem rosto nem boné), em câmera lenta de 0,56x.
  - **Tela dividida (~56%):** o avatar em cima (720x840) e, embaixo, o recorte do original **entre o queixo e a legenda** (y 530–950): câmera, painel, cabo e mãos.
  - **Avatar em tela cheia (~37%):** "Esta es la cámara…", "panel solar", 2K e o CTA.
  - Somando os dois formatos, o avatar aparece em ~94% do tempo.
- **Boné com possível bandeira:** o recorte nunca sobe acima de y = 530, então o boné não aparece em nenhum quadro.
- **"Hard time keeping these in stock" (escassez):** removido.
- **"I'll drop that link down below":** removido.
- Também saíram:
  - "it's from Wyze so you know it's high quality", trocado pelo spec "Graba en 2K";
  - "hands down the best", que virou "una cámara que vale la pena";
  - "no more batteries", que virou "no tienes que cargarla";
  - "quick connect mount": a montagem rápida não está nos specs oficiais, então ficou só "se instala muy fácil".
- **CTA:** "Pídela hoy. Toca el botón de abajo y pide la tuya." Não há preço, país, frete nem garantia.
- **Legenda em inglês:** não entra no quadro. O recorte de baixo termina em y = 950, acima da legenda original, e o gancho termina em y = 900. A legenda nova em espanhol, pelo alinhamento, fica no ponto padrão do kit, sem cobrir o rosto do avatar.
- **Título do gancho:** "LA CÁMARA QUE YO QUIERO 👀" (manchete, de 0 a 3 s).
- **Setas de CTA:** entram no "Toca" (39,3 s) e ficam até o fim.
- **Selo:** não foi colocado. A receita pronta para incluir depois é `receita_com_selo.json`.

## Revisão
- **Whisper (es):** bate com o roteiro. Não há preço, país, TikTok, "link", escassez nem alegação proibida.
- **Whisper (en):** só devolve a tradução do espanhol. Idioma detectado: es (0,999).
- **Folha de contato** (1 quadro/s):
  - Nenhuma legenda em inglês aparece.
  - O rosto e o boné do criador não aparecem em nenhum quadro; o último quadro do gancho foi conferido.
  - As setas ficam abaixo da legenda.
- **Cortes (scdet):** nenhum quadro solto; o menor trecho tem 0,57 s, por causa de um corte interno do original.
- **Fim:** o silêncio final tem 0,52 s.

## Pendências e observações
- **Camiseta "YETI":** o original é espelhado, e a camiseta do criador mostra a logo YETI (outra marca) espelhada e camuflada nos recortes de baixo. É pouco legível, mas, se incomodar, dá para desfocar (é grátis, com `desfocar_regioes.py`, só que a logo se move com o corpo).
- **Produto espelhado:** como o original é espelhado, o produto também aparece invertido. Não há texto legível no produto nos recortes.
- O original não tinha trilha, então o AD saiu sem música.
