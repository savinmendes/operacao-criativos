# Trocas na loja essiora.com: marca Pellorini (levantamento de 10/10/2026, pelo site público)

Decisões da pessoa: devolução de **90 dias**; venda para o **mundo todo**; marca **Pellorini**; trocar tudo.

## Produtos (Admin API: produto, sem mexer no tema)
- 49 produtos com "Pelvini®" no título e no fornecedor ("vendor"). Exemplo: "Pelvini® Vittorio" → "Pellorini Vittorio".
  - Ficam "Pelvini® - Abito ( Limited Edition )" → "Pellorini Abito (Limited Edition)" e "Pelvini® – Silk Cleaning Cloth" → "Pellorini – Silk Cleaning Cloth".
- 1 descrição ("Signature Pelvini design") → "Signature Pellorini design".
- O handle (URL) **não muda**: mudar quebra os links de anúncios já no ar.
- Backup antes de mudar: `produtos_antes.json`.

## Tema (cópia do tema publicado; a pessoa publica)
| Texto atual | Onde aparece | Texto novo |
|---|---|---|
| Free tracked UK delivery · 90-day money-back guarantee | faixa do topo, todas as páginas | Free tracked worldwide shipping · 90-day money-back guarantee |
| Ships From the UK | selos (rodapé/produto) | Ships Worldwide |
| Free Tracked UK Delivery | selos do rodapé | Free Tracked Worldwide Shipping |
| Shipping to US | produto | (remover ou "Free worldwide shipping") |
| Secure checkout · 30-Day Money Back · 24-Month Warranty | card de produto na coleção | Secure checkout · 90-Day Money Back · 24-Month Warranty |
| New arrivals, home cleaning tips and members-only offers, straight to your inbox. | newsletter do rodapé | New arrivals, early access to limited drops and members-only offers, straight to your inbox. |
| Smart, reliable home essentials that make everyday cleaning easier. Shipped from the UK and backed by our 90-day money-back guarantee. | texto do rodapé | Timeless watches built to last, without the luxury markup. Free tracked worldwide shipping and a 90-day money-back guarantee. |
| Orders ship from the UK with tracked delivery... | FAQ | Orders ship worldwide with tracked delivery... |
| 4.8/5 – 13,066 reviews · 100,000+ customers worldwide | página de produto | remover (números da Pelvini) |
| 5,900+ Verified Reviews | coleção best-sellers | remover |
| Shipping/refund policy | Configurações → Políticas | conferir se cita UK, 30 dias ou Pelvini |

## Fora do pedido (só avisar)
- A **página inicial inteira é de aspirador** ("Cordless Vacuum Cleaner", "Clean your whole home without a cord").
  Também há os produtos "Digestive Enzymes" e "Cordless Vacuum Cleaner". Não foi mexido.
- As **fotos** dos relógios mostram o logo PELVINI no mostrador e na caixa. A troca de texto não resolve isso.
- O app de avaliações (320 reviews no produto) pode ter avaliações importadas da Pelvini: conferir.
