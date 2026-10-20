# Troca de marca em criativo existente

> Como "virar" um AD próprio para outra marca, oferta ou mercado: corte antes da marca antiga, fim novo, rótulo trocado nas cenas, texto de tela, fala antiga e versão curta. Abra quando pedirem para adaptar/reaproveitar criativos de uma marca para outra.

## Contexto de uso

**Quando se aplica.** Criativos da **própria** operação (marca da pessoa) que vão rodar com outra marca/oferta com a mesma fórmula, ou em outro mercado. Concorrente nunca entra: dele só se aproveita a ideia de ângulo, sem imagem, texto ou voz. Fluxo de lote guiado pela skill `adaptar-marca`; montagem e revisão pelas skills `editar-criativo` e `revisar-criativo`.

**Lotes em que foi usado.**
- **Mayaverra → Lymphoria (COD Chile), pasta `Downloads\LHYMPORIA AD 01-20\`, iniciado 03/10/2026.**
  - 24 vídeos de gotas de drenagem linfática da marca Mayaverra, que é da pessoa.
  - Mesma fórmula de 4 ervas, então o corpo pode ficar.
  - Fim universal sem preço para Chile, Guatemala e Equador: frete grátis, pago contra entrega, 90 días de garantía.
  - Piloto AD 04 entregue em 03/10/2026 por ≈US$6,52.
  - Voz clonada do narrador: `FNIhgYgEcJsdWbHRFiz6`.
  - Projeto Flora `prj_ns7cvmdqvtn37b53wfnywhr9q58fjte1`: referência neutra do frasco = nó n59 (nó n2 também citado como ref do frasco).
- **Linfarele (Itália, cartão, sem COD).** Fim em IT. Referência neutra do frasco = nó n6 do projeto Flora `prj_ns7f6r91ft66e7jpk9d8mrapph8fn291`. Orquestrador `linfarele/_trabalho/processar_it.py`.
- **Drenagem LATAM, pasta `Downloads\DRENAGEM-LATAM\`, entregue 05/10/2026.**
  - 10 ADs (longo + CURTO), 5 UGC e 30 variações.
  - Custo real ≈US$24,75 (orçado US$35).
  - A pessoa aprovou tratar os vídeos 18 (Herbalia), 20 e 21 ("Lymphoria EUA") como dela.
- **Vitaly → Lymphoria CL, pasta `Downloads\ADLIB-VITALY-CL\`.**
  - 11 vídeos + 12 imagens + um lote enxuto.
  - V03/V11 bloqueados: fala nova em profissional de saúde.
  - Padrão adotado quando o filtro barra "manter tudo": suavizar com o mesmo sentido e o mesmo tempo, e registrar as trocas.

**Fatos e decisões técnicas.**
- Método validado no Lymphoria após o piloto: manter hook + corpo, **cortar antes de "La marca que te da…"** e colar um fim próprio narrado com a **voz clonada do narrador original**. Voz genérica quebra o padrão. O fim leva fotos do produto + selo COD + setas.
- Fim A (a narração já citou as ervas) × fim B, que começa com "Se llama Lymphoria: cuatro hierbas en las dosis correctas."
- Takes com o frasco antigo: refazer no Kling O1 Edit (Flora). O remendo 2D tinha ficado feio no piloto. Desde o lote Drenagem, a ordem é: `trocar_rotulo_faixa.py` primeiro (grátis), Kling só onde a faixa não resolve.
- Kling O1 Edit: ~US$0,706 por clipe no Flora.
  - Funciona bem em clipe de **cena única**.
  - Clipe estendido em vai-e-volta, ou com corte no meio, faz o modelo reinventar personagem e fundo.
  - Não troca texto de tela de celular.
  - Pode trocar rosto em plano médio.
  - Em cena Pixar/3D troca o rosto ou deixa fotorrealista. No Drenagem isso levou ao `band_fix.py`, hoje `trocar_rotulo_faixa.py` no kit.
- Referência do frasco para o Kling: foto **recortada sobre fundo cinza neutro** (Flora i2i-birefnet + composição, sem selos ao lado). Com a foto de catálogo (fundo jardim), o Kling trocou o cenário inteiro pelo jardim.
- Promessas da versão original que não podem ir para a marca nova: "hecho en EE.UU.", "probado por terceros", 60 dias, 50%. Também não podem ir garantia antiga, registro sanitário, claims fora da ficha nem remédio/doença como cura.
- Upscale prévio: origem 360p → Real-ESRGAN `realesr-animevideov3` (2x para entrega em 720; o piloto usou 3x).
- Ordem recomendada no fluxo de adaptação: remover legenda queimada (LaMa local) → upscale → troca de produto (Kling) → legenda nova padrão do kit. (Vmake removido em 14/10/2026.)
- Bug corrigido em 05/10/2026: o `encaixar_edit.py` copiava do original todo pixel branco do quadro, o que trazia de volta o texto branco do rótulo antigo. Agora a cópia fica limitada à faixa da legenda (0,62–0,90 da altura). As v2 do lote antigo estão em `lymphoria\_v2_corrigidos\`.
- Receitas por AD e orquestradores (`processar_ad.py`, `processar_it.py`, `_trabalho/cortar_takes.py`): em `Downloads\LHYMPORIA AD 01-20\*\_trabalho\`.

## Lógica de uso

### 1. Estudo e orçamento
1. Baixar ≥720p, deduplicar por md5, `originais/NN.mp4` + `indice-arquivos.csv`. Agentes em paralelo para transcrição (faster-whisper), folha de contato e OCR só onde precisar (em sequência, `cpu_threads=4`).
2. Classificar cada vídeo: marca própria adaptável · já com a marca nova (só fim/unidades) · concorrente (só referência de ângulo) · descartar.
3. Conferir duplicados contra lotes anteriores (mesmo roteiro já entregue).
4. Listar os melhores ganchos (com tempo) e os riscos de plataforma.
5. Orçar 3 caminhos, cada um com custo + tempo + opção mais rápida: (1) adaptar (cenas Kling × preço + voz), (2) refazer com avatar (créditos), (3) matriz gancho × corpo. Variantes mais baratas: versão curta e "desfocar em vez de Kling".
6. Perguntas de bloqueio: os vídeos são da pessoa? oferta e países? aprovação do gasto?

### 2. Preparação
- Upscale em **fila única de GPU** (um script de fila com log). Agentes não rodam upscale: esperam o `full_up720.mp4` e adiantam ponto de corte, mapa de cenas e voz no original.
  ```
  python ferramentas/upscale_video.py entrada.mp4 full_up720.mp4 --escala 2 [--ate 52.4]
  ```
- Briefing único `producao/_trabalho/BRIEFING-AGENTES.md`: oferta/CTA/garantia nova, lista do que tirar, textos do fim A/B/C, regra de voz, teto de Kling por AD (cenas orçadas + 2), CPU/GPU, revisão, relatório.

### 3. Por AD
1. **Ponto de corte.** Transcrição por palavra (`python ferramentas/palavras_trecho.py video.mp4 --de 40 --ate 80` imprime `tempo:palavra`). Cortar em fim de frase, antes do trecho em que o narrador apresenta a marca/oferta antiga.
2. **Fim universal.**
   - Fotos do produto novo + narração clonada + legenda + selo + setas.
   - Voz: reutilizar um clone existente (`VOZES-CLONADAS.md`, `voz.txt` dos lotes) ou `python ferramentas/clonar_voz.py video.mp4 --nome "AD04 narrador" --de 20 --ate 110` → `tts_elevenlabs.py` com alinhamento → `narr_fim.mp3`.
   - Montar com `montar_ad.py` em 720.
3. **Achar as cenas com a marca antiga.**
   - Folha de contato do `full_up720`: `python ferramentas/folhas_contato.py --cada 1 --de 0 --ate 60 --saida pasta video.mp4`.
   - Ou varredura por molde: `python ferramentas/varrer_produto.py --moldes m1.png m2.png --saida varredura.json video1.mp4 …`. Amostra 2 q/s, agrupa por cena, conta take >9 s como 2+ clipes e gera `<video>_achados.jpg`.
4. **Trocar o rótulo — ordem obrigatória.**
   1. `trocar_rotulo_faixa.py` (grátis, o personagem não muda nenhum pixel):
      ```
      python ferramentas/trocar_rotulo_faixa.py in.mp4 out.mp4 --auto --roi "0:x0,y0,x1,y1;60:…" --texto MARCA --de 143 --ate 145.6
      python ferramentas/trocar_rotulo_faixa.py in.mp4 out.mp4 --seguir --roi 290,840,452,940 --cor escuro --texto MARCA
      python ferramentas/trocar_rotulo_faixa.py in.mp4 out.mp4 --caixa "0:265,960,455,1010;60:270,965,460,1015" --texto MARCA
      … --prev 10   (salva só o quadro 10 tratado, para conferir)
      ```
      Modos:
      - `--auto` acha a faixa pela cor (bom para frasco em movimento; `--so-faixa` não alarga ao rótulo);
      - `--seguir` segue pelas linhas (faixa horizontal; `--cor escuro` quando não é colorida);
      - `--caixa` é marcada à mão, para plano parado.

      Parâmetros: `--cor verde|escuro|h0,s0,v0,h1,s1,v1`, `--cor-texto`, `--escala 0.55`, `--alfa`, `--fonte Poppins-Bold.ttf`. A saída sai em crf 14 com o áudio copiado.
   2. **Kling O1 Edit** só onde a faixa não resolve (rótulo em ângulo, ilustração, tampa) e **nunca em rosto Pixar/3D**:
      - take de cena única, cortado com `-ss ini -t dur` + `tpad=stop_mode=clone` até ≥3 s (ex.: 3,4 s). Nunca usar `-frames:v`, que corta o padding e faz o Kling recusar;
      - referência do frasco novo recortada sobre cinza neutro;
      - prompt começando com "@Image1 is ONLY a reference for the bottle label design; do not use its background" + descrição da cena original + "local edit only… every pixel outside the bottle identical";
      - subir com `flora_upload.py --lote lote.json` (ou `flora_up.py`);
      - teto por AD = cenas previstas + 2. Se falhar: cena vizinha, desfoque ou manter quando a marca é ilegível.
   3. Realinhar o take do Kling (24 fps, duração diferente) ao tempo original e restaurar a legenda queimada:
      ```
      python ferramentas/encaixar_edit.py take.mp4 take_edit.mp4 take_final.mp4 --dur 2.3 [--sem-legenda]
      ```
   4. Se o Kling mexeu no personagem/fundo, colar **só o produto** editado sobre o original:
      ```
      python ferramentas/colar_produto.py original.mp4 editado.mp4 saida.mp4 [--dur 1.33] [--debug quadro.jpg]
      ```
      A silhueta é calibrada para frasco âmbar com faixa verde e tampa preta. Para outro produto, precisa de revisão manual.
   5. Encaixar os takes no vídeo (quadro a quadro, áudio mantido):
      ```
      python ferramentas/substituir_trechos.py base.mp4 out.mp4 trechos.json
      ```
      `trechos.json = [{"clipe":"take1_final.mp4","inicio":7.367,"quadros":190}, …]`
5. **Texto na tela.**
   - Marca na legenda queimada: achar a caixa com `python ferramentas/caixa_legenda.py video.mp4 --t 2.9 [--faixa 0.45,0.92]` e trocar com
     ```
     python ferramentas/trocar_texto_tela.py in.mp4 out.mp4 --de 181.47 --ate 183.43 --caixa 312,1410,765,1467 --texto "Lymphoria, 4" [--px 58] [--ref t] [--fonte Poppins-Medium.ttf] [--maiusc]
     ```
   - Marca num cabeçalho que se move pouco (tela de celular): `remendo_rastreado.py entrada.mp4 saida.mp4 --caixa x0,y0,x1,y1 --texto LYMPHORIA [--ref 0.3]` (saída sem áudio).
   - Tela de celular/app/site com outra marca: `python ferramentas/desfocar_regioes.py in.mp4 out.mp4 --de 346.67 --ate 349.73 --caixas "230,110,560,215;150,660,370,705" [--forca 45]`.
6. **Falas** com marca, garantia ou plataforma antiga: fala nova na voz clonada e
   ```
   python ferramentas/trocar_trecho_audio.py in.mp4 fala.mp3 out.mp4 --de 179.8 --ate 182.3
   ```
   O ajuste de velocidade fica limitado a 0,8x–1,25x (avisa se precisar mais), com cruzamento de 40 ms nas bordas. O vídeo é copiado sem reencode.
7. Tudo numa receita `rNN.json` (`corte`, `takes`, `extras`, `blur`, `textos`, `audios`, `cauda`, `saida`), rodada por um pipeline do tipo `processar_ad.py` que pula etapas já feitas. O fim passa por `montar_ad.py` em 720.
8. **Versão CURTA (60–90 s):** gancho (~8–15 s) + 2–3 trechos fortes (problema, mecanismo, prova) + o mesmo fim. Cortar em fim de frase e montar **só com partes já tratadas**, para a marca antiga não voltar.
9. Revisão: `revisar_ad.py` + **zoom 3x em cada take trocado** (o resto do rótulo antigo só aparece ampliado).

### 4. UGC a partir de ângulo de concorrente
Só a ideia: roteiro novo, avatar próprio (skill `gerar-midia-ia`), cenas do produto novo. Medir créditos no 1º.

### Armadilhas
- Kling recusa vídeo <3 s; `-frames:v` corta o padding.
- Kling em Pixar/3D troca o rosto → `trocar_rotulo_faixa.py` ou colar só a região do frasco (`colar_produto.py`; no lote, `ad05/flora/comp_regiao.py`).
- Kling não troca texto de tela de celular → desfocar, cobrir ou usar a cena vizinha.
- A folha de contato não mostra rótulo branco antigo reaparecendo: conferir com zoom.
- Unidades (libras/kg): mudar só se a oferta pedir. Libras ficaram no Lymphoria porque Guatemala e Equador usam.
- Não inventar depoimento, número ou estudo.

### Checklist de saída
- [ ] Nenhum nome/grafia da marca antiga em áudio (Whisper) e tela (folha + zoom 3x).
- [ ] Fim com a oferta atual confirmada, voz igual à do narrador.
- [ ] Nenhum claim herdado fora da ficha nova.
- [ ] Versão curta emendada em fim de frase.
- [ ] `_trabalho/adNN/RELATORIO.md` (takes Kling e US$, caracteres TTS, clone usado, o que trocou, revisão, pendências) + `00-RELATORIO-PRODUCAO.md` com custo real × orçado e bugs do kit.

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [02-regras-gerais-e-seguranca.md](02-regras-gerais-e-seguranca.md)
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [04-fluxo-producao-criativos.md](04-fluxo-producao-criativos.md)
- [05-traducao-de-criativos.md](05-traducao-de-criativos.md)
- [07-variacoes-gancho-corpo.md](07-variacoes-gancho-corpo.md)
- [08-voz-e-dublagem.md](08-voz-e-dublagem.md)
- [10-limpeza-cor-e-qualidade-de-video.md](10-limpeza-cor-e-qualidade-de-video.md)
- [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)
- [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md)
- [13-analise-meta-ads-e-vencedores.md](13-analise-meta-ads-e-vencedores.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)
- [projetos/](projetos/)
