# Estudo rápido: banner principal (hero) de Black Friday nos grandes varejistas

Data: 09/10/2026 · Frente: COD Chile · Objetivo: refazer o banner da home de chileverificada.com como imagem.

## Como foi feito

Abri as páginas com navegador (Chrome headless, celular 390 px e computador 1440 px) e medi as imagens do topo (tamanho real do arquivo e tamanho exibido). Prints em `scratchpad/estudo` (não copiados para cá, só serviram de base).

| Loja | Página vista | O que deu para ver |
|---|---|---|
| Falabella | https://www.falabella.com/falabella-cl/page/Black-Friday | Hero BF 2026: desktop **1920×480 (4:1)**, mobile **720×576 (5:4)**. Fundo preto/grafite, wordmark "black friday" gigante em branco com 1 acento verde-limão (o ponto do "i"), botão "VER OFERTAS" branco, produtos recortados (console, câmera, celular) à direita. Sem data, sem contador, sem % no hero. |
| Falabella (home) | https://www.falabella.com/falabella-cl | Carrossel 1920×480 desktop / 720×589 mobile. Cada slide 1 promessa ("Vestuario mujer 40% dcto.") + 1 botão + nota "Productos seleccionados". |
| Paris (Cencosud) | https://www.paris.cl/black-friday/ | Hero "BLACK paris": desktop **3360×990 (~3,4:1)**, mobile **1200×800 (3:2)**. Fundo azul-escuro quase preto com feixes de luz, só tipografia (wordmark gigante), "Black Friday 2026" pequeno. Logo abaixo, 4 cartões de confiança: **"Despacho gratis"**, "Compra antes de las 17:00 y recibe el mismo día", retiro grátis, tarjeta. |
| Mercado Libre Chile | https://www.mercadolibre.cl/ | (Evento atual "Fechas dobles 10/10", não BF.) Desktop **1920×500 (~3,8:1)**, mobile **1200×410 (~3:1)**. Promessa enorme ("10/10", "50% OFF", "12 cuotas"), pessoa + produtos, e logo abaixo fileira de cartões "Envío gratis", "Medios de pago". |
| Nike Chile | https://www.nike.com/cl/ | Desktop **1620×788 (~2:1)**, mobile **828×1240 (2:3, vertical)**: foto de produto grande, faixa "HASTA 60% OFF · 12 cuotas sin interés · COMPRAR". |
| Amazon | https://www.amazon.com/blackfriday | Faixa **1500×150 / 750×200** "Gracias por comprar Black Friday" (pós-evento), o resto é grade de ofertas com selo "-27% Oferta Relámpago". |
| Ripley, Lider (Walmart), Hites | ripley.cl, lider.cl, hites.com | **Não deu para ver**: bloqueio anti-robô (Cloudflare / "Robot or human?"). Precisa de revisão manual se quiser incluir. |

## Padrões encontrados

1. **Proporção:** desktop largo e baixo, entre **3:1 e 4:1** (1920×480 a 3360×990), para não empurrar os produtos para baixo da dobra. No celular, **imagem própria** e mais alta: de 3:2 (Paris) e 5:4 (Falabella) até 2:3 (Nike). Todos usam arquivos separados para celular e computador (nada de recortar a mesma imagem).
2. **Hierarquia (3 níveis só):** 1) wordmark "BLACK FRIDAY" gigante (ou "BLACK paris"), 2) uma promessa curta, 3) um botão. Texto de apoio é pequeno ou fica fora da imagem.
3. **Cor:** fundo preto/azul-noite + **um único acento** (verde-limão Falabella, azul elétrico Paris). Ninguém usa várias cores fortes juntas. Para nós, **preto + dourado** cumpre o mesmo papel e já é a cor da barra/faixa do tema.
4. **Produto x tipografia:** os varejistas de catálogo misto (Falabella) usam 2-3 produtos recortados com sombra; quem tem marca forte (Paris) vai só de tipografia. Catálogo misto como o nosso → tipografia forte + produtos **genéricos** (sem marca de terceiros) no lado.
5. **Datas/contador:** nenhum hero visto usa contador regressivo; no máximo "Black Friday 2026" pequeno. As **condições de confiança** (despacho grátis, mesmo dia, cuotas) ficam em **selos/cartões logo abaixo** ou numa faixa, não competindo com o título.
6. **Quantidade de mensagens:** 1 promessa + 1 CTA por banner. Rodapé legal quando há % ("Productos seleccionados", "compras sobre $19.990").

## Recomendação aplicada ao nosso banner

- Desktop ~**3:1** (gerado em 2K e entregue em largura total) e celular **1:1**, mesmo conceito.
- Preto + dourado; "BLACK FRIDAY" gigante; promessa "LIQUIDACIÓN DE STOCK"; apoio "Stock limitado"; **1 botão** ("VER OFERTAS").
- Os 3 selos verdadeiros (Despacho gratis a todo Chile · Pagas al recibir · Entrega en 24-72h) numa linha discreta, como os cartões da Paris/Mercado Libre.
- Sem %, sem preço "antes/agora", sem contador, sem data (não temos dados reais para isso), sem marcas de terceiros.

## Fontes

- https://www.falabella.com/falabella-cl/page/Black-Friday
- https://www.falabella.com/falabella-cl
- https://www.paris.cl/black-friday/
- https://www.mercadolibre.cl/
- https://www.nike.com/cl/
- https://www.amazon.com/blackfriday
- Tamanhos recomendados para Shopify (referência secundária): https://section.store/blogs/store-design-optimisation/shopify-hero-banner-sizes-examples-best-practices-2025 , https://pagefly.io/blogs/shopify/shopify-banner-size
