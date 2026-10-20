---
name: project-lymphoria-adaptacao-ads
description: "Lote \"LHYMPORIA AD 01-20\" = criativos da marca Mayaverra (do próprio usuário) sendo adaptados para a marca Lymphoria (COD Chile); método e dados da oferta"
metadata:
  node_type: memory
  type: project
  originSessionId: fefd88e1-1970-4576-a429-cf0c1248f170
  modified: 2026-10-04T05:24:24.141Z
---

Pasta `C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20` (triagem em TRIAGEM-destinos-e-pendencias.md) tem 24 vídeos da marca **Mayaverra** (do próprio usuário, expansão de mercado) (gotas de drenagem linfática). Objetivo (03/10/2026): trocar marca/mercado para **Lymphoria** (https://chileverificada.com/products/lymphoria), COD Chile.

- Mesma fórmula das 4 ervas (galio, stillingia, trébol rojo, fresno espinoso) → corpo dos vídeos pode ficar.
- MERCADOS (decisão 03/10/2026): os vídeos servem para Chile, Guatemala e Equador → fim UNIVERSAL sem preço/promo, espanhol neutro: "...se llama Lymphoria. Unas gotas bajo la lengua cada mañana, y sabe a miel. Pides ahora, te llega con envío gratis y pagas al recibir en tu casa. Y tienes noventa días de garantía o te devolvemos tu dinero. Toca el botón de abajo y pide el tuyo." Selo: ENVÍO GRATIS · PAGO CONTRA ENTREGA · ¡PAGAS AL RECIBIR! (frete grátis, COD e "90 días de garantía o te devolvemos tu dinero" são padrão nos 3 países — política oficial). Versão B do fim (quando a narração não citou as 4 ervas antes): começa "Se llama Lymphoria: cuatro hierbas en las dosis correctas.". Libras: manter (GT/EC usam); versão kilos só se for rodar no Chile. AD 04 precisa regerar o fim nesse padrão.
- Oferta (loja Chile, NÃO vai no vídeo): Compre 1 reciba 2 $34.990 · 2→4 $54.990 · 3→6 $72.990 · despacho grátis · pagas al recibir · garantia 90 dias.
- Frasco Lymphoria: âmbar conta-gotas, faixa verde "LYMPHORIA · drenaje linfático", "Sabe a Miel".
- Método (revisado após feedback do piloto): manter hook+corpo, cortar antes de "La marca que te da..." e colar fim próprio narrado com a VOZ CLONADA do narrador original (não voz genérica — quebra o padrão) + fotos do produto + selo COD + setas. Takes com o frasco Mayaverra (AD 04: 7 takes, ex. 0:07–0:16, 0:21–0:27, 0:37, 0:48–0:50) → refazer no Flora com Kling O1 Edit (vídeo + foto do frasco Lymphoria), não remendo 2D (ficou feio). Qualidade: upscale IA local Real-ESRGAN `realesr-animevideov3` 3x (usuário autorizou; ffmpeg 9 usa `-fps_mode passthrough`, não `-vsync`).
- Promessas da versão original ("hecho en EE.UU.", "probado por terceros", 60 dias, 50%) não podem ir para os vídeos.
- REFERÊNCIA DO FRASCO PARA KLING: usar foto do frasco RECORTADO sobre fundo cinza neutro (Flora i2i-birefnet + composição; sem selos ao lado). Com a foto de catálogo (fundo jardim) o Kling troca o cenário inteiro pelo jardim. Lymphoria neutra = nó n59 do projeto prj_ns7cvmdqvtn37b53wfnywhr9q58fjte1. Prompt começar com "@Image1 is ONLY a reference for the bottle label design; do not use its background" + descrever a cena original.
- Kling NÃO troca texto de tela de celular (página do site) e pode trocar rosto de personagem em plano médio → nesses casos cobrir com cena vizinha (vai-e-volta) ou manter original se a marca não for legível.
- Lições do Kling O1 Edit (Flora, US$0,706/clipe): funciona bem em clipe de CENA ÚNICA; clipe curto estendido em vai-e-volta ou com corte no meio faz o modelo reinventar personagem/fundo. Estender com quadro congelado (`tpad=stop_mode=clone`) + prompt "local edit only... every pixel outside the bottle identical". Saída vem 24 fps/duração diferente → `ferramentas/encaixar_edit.py` (realinha e restaura legenda queimada). Fluxo de upload: `flora_upload.py --lote`. Trocar trechos: `substituir_trechos.py`.
- Kling exige vídeo ≥3,0 s: cortar take com `-ss ini -t dur` + `tpad=stop_mode=clone` até 3,4 s (NÃO usar `-frames:v`, corta o padding). Script: `_trabalho/cortar_takes.py ad NN ini:quadros ...`; pipeline completo por receita JSON: `lymphoria/_trabalho/processar_ad.py` e `linfarele/_trabalho/processar_it.py`.
- Linfarele (IT, Itália, cartão — sem COD): ref neutra do frasco = nó n6 do projeto Flora prj_ns7f6r91ft66e7jpk9d8mrapph8fn291. Fim IT: "Si chiama Linfarele... spedizione gratuita... novanta giorni di garanzia: soddisfatti o rimborsati" (confirmar política no site).
- Piloto: AD 04 ENTREGUE 03/10/2026 (lymphoria\AD 04 - LYMPHORIA-ESQUELETO-CERVEZA-ES-CL.mp4), custo ≈ US$6,52. Voz clonada do narrador: voice_id FNIhgYgEcJsdWbHRFiz6. Projeto Flora: prj_ns7cvmdqvtn37b53wfnywhr9q58fjte1 (frasco ref = nó n2; foto kit 3 frascos limpa gerada lá). Relacionado: [[reference-unit-economics-cod]]
