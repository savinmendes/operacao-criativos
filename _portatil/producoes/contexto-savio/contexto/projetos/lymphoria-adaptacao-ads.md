# Lymphoria: adaptação dos ADs Mayaverra (lote LHYMPORIA AD 01-20) + 5 Linfarele IT

> Lote em que os vídeos da marca Mayaverra (da própria pessoa) viraram Lymphoria (COD LATAM) e, em parte, Linfarele (Itália). Abra este arquivo ao refazer, corrigir ou ampliar esse lote, ou ao trocar a marca de qualquer AD longo no estilo Pixar/IA.

## Contexto de uso
- **Frente:** COD (Lymphoria) e e-commerce com cartão na Itália (Linfarele, sem COD).
- **Produto:** gotas de drenagem linfática com 4 ervas (galio, stillingia, trébol rojo, fresno espinoso). A fórmula é a mesma da Mayaverra, por isso o corpo dos vídeos pode ficar.
- **Origem:** 23 vídeos (AD 01–24; o AD 17 não existe na pasta) da marca **Mayaverra**, que é da pessoa (expansão de mercado). Os originais estão em 360p. A triagem de 03/10/2026 fica em `TRIAGEM-destinos-e-pendencias.md`.
- **Mercados (decisão de 03/10/2026):** Chile, Guatemala e Equador, com um **fim universal** em espanhol neutro e sem preço. As libras ficam (GT e EC usam). A versão em quilos só se for rodar só no Chile.
- **Oferta da loja Chile** (não vai no vídeo): Compre 1 reciba 2 $34.990 · 2→4 $54.990 · 3→6 $72.990 · despacho grátis · pagas al recibir · garantia de 90 dias. Página: chileverificada.com/products/lymphoria. A oferta foi atualizada depois no lote Vitaly (ver [vitaly-lymphoria-cl.md](vitaly-lymphoria-cl.md)).
- **Selo:** ENVÍO GRATIS · PAGO CONTRA ENTREGA · ¡PAGAS AL RECIBIR!
- **Frasco Lymphoria:** âmbar com conta-gotas, faixa verde "LYMPHORIA · drenaje linfático", "Sabe a Miel".
- **Promessas proibidas** que vinham do original: "hecho en EE.UU.", "probado por terceros", 60 dias, 50%, Cofepris (AD 20, registro sanitário do México).
- **Entregas:**
  - Piloto **AD 04** entregue em 03/10/2026 (custo ≈ US$ 6,52).
  - Lote 1 (AD 04, 06, 21, 23, 24) e Lotes 2+3 na noite de 03→04/10/2026: 19 vídeos Lymphoria em `LHYMPORIA AD 01-20\lymphoria\` (atalho `entregas-lymphoria/`), nomes `AD NN - LYMPHORIA-<TEMA>-ES-LATAM.mp4`.
  - 5 vídeos Linfarele IT (AD 03, 04, 05, 06, 10) em `linfarele\` (atalho `entregas-linfarele/`).
  - Textos dos anúncios: `lymphoria\TEXTOS-ANUNCIOS-LOTE1/2/3.txt` e `linfarele\TESTI-ANNUNCI-IT.txt`.
  - **v2 corrigidos** (05/10/2026): 13 vídeos (ADs 01, 02, 03, 04, 09, 10, 11, 12, 13, 14, 16, 19, 22) em `lymphoria\_v2_corrigidos\` com `RELATORIO-V2.md`, por causa do bug do rótulo branco no `encaixar_edit.py`. Os entregues originais não foram tocados.
- **Custos:** orçamento por AD em `lymphoria\orcamento_por_ad.md` (US$ 0,706 por take no Kling O1 Edit + ≈ US$ 0,06 por fim narrado). Noite dos lotes 2+3 + Linfarele: ≈ US$ 44 (Kling ~60 takes ≈ US$ 42, ElevenLabs ≈ US$ 2,1, Flora imagens ≈ US$ 0,14), dentro dos US$ 51 aprovados.
- **IDs úteis:** voz clonada do narrador `FNIhgYgEcJsdWbHRFiz6`; projeto Flora Lymphoria `prj_ns7cvmdqvtn37b53wfnywhr9q58fjte1` (frasco neutro = nó n59; frasco ref = nó n2); projeto Flora Linfarele `prj_ns7f6r91ft66e7jpk9d8mrapph8fn291` (frasco neutro = nó n6).
- **Validado no TikTok (08/10/2026):** o AD 23 SUPERMERCADO deste lote está em `Downloads\APROVADOS E VALIDADOS TIKTOK\`.
- **Pendências e revisão manual:**
  - restos do rótulo dentro da faixa da legenda nos ADs 03, 09, 22, 13 e 01 (um v3 grátis resolve a maior parte; teste em `_v2_trabalho\teste_v3\cmp_v2_v3.jpg`); AD 19 t2 com possível mancha;
  - AD 19 mantém o frasco Herbalia pequeno em 0:00–0:02 e 0:08–0:09 e tem antes/depois de celulite (risco Meta);
  - AD 11 em 5:10: o Kling trocou o fundo do close do frasco;
  - Linfarele: confirmar no site se o frete grátis vale para toda a Itália e se a garantia é de 90 dias;
  - AD 20 (Herbalia + Cofepris) ficou de fora; reservas 08, 15 e 18 são duplicatas de roteiro.

## Lógica de uso
1. **Triagem:** transcrever todos, marcar no nome do arquivo `EDITAR marca`, `EDITAR mercado` ou `OK`, e escolher 1 de cada grupo de roteiro duplicado (o mais denso em palavras por minuto, sem pendência de marca).
2. **Orçamento por AD** antes de produzir: contar os takes com frasco legível pela folha de contato (1 quadro a cada 3 s). Frasco pequeno, no fundo ou ilegível **não** é trocado.
3. **Upscale** com Real-ESRGAN `realesr-animevideov3` 3x (no ffmpeg 9 use `-fps_mode passthrough`, não `-vsync`).
4. **Corte + fim próprio:** manter gancho e corpo, cortar antes de "La marca que te da..." e colar o fim narrado com a **voz clonada do narrador original** (voz genérica quebra o padrão).
   - Fins prontos em `lymphoria\_trabalho\fim_A.txt` (com "La marca que te da esas cuatro hierbas..."), `fim_B.txt` (começa "Se llama Lymphoria: cuatro hierbas...", para quando a narração não citou as ervas) e `fim_C.txt` (só a oferta).
   - Montagem: `montar_fim_universal.py <pasta_ad> <parte1.mp4> <narr_fim.mp3> "<saida>" [--cauda original.wav]` (fotos do produto + legenda só no fim + selo + setas, finaliza pelo kit).
5. **Takes com o frasco antigo → Kling O1 Edit no Flora**, não remendo 2D:
   - cortar com `cortar_takes.py adNN ini:quadros ...` (estende com quadro congelado até ≥ 3,4 s; nunca `-frames:v`, que corta o padding);
   - referência do frasco **recortado sobre fundo cinza neutro** (com foto de catálogo o Kling troca o cenário inteiro);
   - prompt começando com "@Image1 is ONLY a reference for the bottle label design; do not use its background" + descrição da cena + "local edit only... every pixel outside the bottle identical";
   - upload em lote com `flora_upload.py --lote`; encaixe com `encaixar_edit.py` (realinha 24 fps e restaura a legenda queimada só na faixa 0,62–0,90 da altura); troca no vídeo com `substituir_trechos.py`.
6. **Pipeline por receita:** `lymphoria\_trabalho\processar_ad.py receita.json` (takes, extras, blur, textos, áudios, cauda; pula etapas já feitas). Linfarele: `linfarele\_trabalho\processar_it.py`.
7. **Falas e legendas com a marca antiga no meio:** trocar só a palavra com a voz clonada (centavos) e cobrir a legenda queimada.
8. **Telas de celular com o site antigo:** o Kling não troca texto de tela; cobrir com cena vizinha ou desfocar.
9. **Revisão:** whisper no idioma alvo + folha de contato + **zoom no rótulo** de cada take editado (a folha não mostra resto de rótulo).
- **O que deu errado e como evitar:**
  - Kling em clipe com corte no meio ou estendido em vai-e-volta reinventa personagem e fundo. Use clipe de cena única.
  - Kling pode trocar o rosto de personagem em plano médio e estraga rosto Pixar: use `trocar_rotulo_faixa.py` do kit (ex-`band_fix.py`), como no lote Drenagem.
  - O `encaixar_edit.py` antigo trazia de volta o texto branco do rótulo (corrigido em 05/10/2026).
  - Elisões italianas quebravam o nome ("L'INFARELE"): usar `legenda_hook.corrigir`.
- **Se a pessoa pedir mais:** rodar o v3 grátis nos 5 ADs com resto de rótulo; regerar o fim em quilos para uma versão só Chile; usar as reservas (08, 15, 18) só se precisar de volume, lembrando que competem com os irmãos de roteiro.

## Relacionados
- [../06-troca-de-marca.md](../06-troca-de-marca.md)
- [../04-fluxo-producao-criativos.md](../04-fluxo-producao-criativos.md)
- [../05-traducao-de-criativos.md](../05-traducao-de-criativos.md) (Linfarele IT)
- [drenagem-latam.md](drenagem-latam.md), [vitaly-lymphoria-cl.md](vitaly-lymphoria-cl.md), [linfarele-imagens-erlona.md](linfarele-imagens-erlona.md)
