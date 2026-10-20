# Clonar loja Shopify em disparo único — guia operacional

**Para quem lê este documento:** você é um assistente que vai clonar uma loja
Shopify inteira de uma vez, conduzindo o operador. Este é o procedimento
completo, não um resumo para ele ler sozinho.

Método consolidado a partir de três tutoriais confrontados entre si, mais o
prompt "AI Ecom Engine", adaptado à operação dele. Transcrições e fichas em
`01-arquivos-organizados/transcricoes-youtube/`.

---

## Contexto da operação — leia antes de qualquer coisa

Ele opera **dropshipping COD (pagamento na entrega)** em Chile, Colômbia,
Guatemala, México e Romênia, além de infoprodutos e venda 1-a-1 por WhatsApp.

Três consequências que mudam tudo:

1. **No COD o checkout do Shopify é substituído por formulário de
   contra-entrega.** Não construa seção de upsell de checkout, order bump ou
   one-click. É trabalho jogado fora.
2. **O dinheiro entra na entrega paga, não na compra.** Qualquer cálculo de
   lucro por pedido superestima. Ele tem calculadora própria que dilui sobre
   entregas concretizadas — mande os números para lá.
3. **Público Latam, em espanhol, variando por país.** Moeda, formato de preço e
   prova social precisam bater com o país da loja.

**Pergunte de qual país e qual oferta é a loja antes de começar.**

---

## Duas coisas diferentes que costumam ser confundidas

| O que se gera | Onde |
|---|---|
| **Design e código** da loja — seções, layout, Liquid | Este guia |
| **Conteúdo** — copy, oferta, prompts de imagem, roteiros de anúncio | Prompt "AI Ecom Engine", que ele já tem |

São etapas complementares, não concorrentes. Rode este guia primeiro para ter a
estrutura, depois o AI Ecom Engine para preencher. Misturar os dois num pedido
só degrada os dois resultados.

---

## O que esperar de verdade

**A primeira tentativa provavelmente não vai ficar parecida.** Isso não é falha
sua nem dele.

O autor do método mais automatizado mostrou exatamente isso acontecendo na
própria gravação: pediu o clone, recebeu algo genérico, disse ao assistente que
não parecia com o original, e só na segunda rodada obteve resultado aceitável.

Trate a iteração como parte do método. O protocolo está na seção "Quando não
ficar parecido", e deve ser usado sem constrangimento.

---

## Caminho A — via conector Shopify

Permite escrever direto na loja, sem copiar e colar. É o que torna o disparo
único viável de verdade.

### Setup, uma vez só

1. **Criar a loja** no Shopify e remover a senha de acesso (exige endereço cadastrado)
2. **Publicar o tema Dawn** (gratuito, na Theme Store)
3. **Criar app customizado:** Configurações → Apps → Desenvolver apps → Criar app
4. **Habilitar escopos** — sem estes o assistente não consegue escrever:
   - `read_themes`, `write_themes`
   - `read_theme_code`, `write_theme_code`
   - `read_products`, `write_products`
   - `read_product_listings`, `write_product_listings`
   - `read_files`, `write_files`
   - `read_content`, `write_content`
5. **Salvar escopos → Release versão 1 → Instalar o app** na loja
6. **Conectar no Claude:** Personalizar → Conectar apps → Shopify → autorizar
7. **Liberar as permissões** do conector, para não pedir confirmação a cada passo
8. **Verificar:** peça "traga as informações da minha loja Shopify". Se voltarem
   os dados, está conectado

### Captura

Use extensão de captura de página inteira. Capture **quatro imagens**:

- página de produto, desktop **e** mobile
- home, desktop **e** mobile

A página de produto é a mais importante. O print mobile é o passo mais pulado e
é o que faz a loja quebrar no celular.

### O disparo

Envie numa mensagem só:

```
Clone esta página de produto na minha loja Shopify, no tema Dawn.

URL de referência: <url>
Anexos: print desktop e print mobile

País e idioma da loja: <ex.: Colômbia, espanhol, COP>
Modelo de venda: COD — o checkout é substituído por formulário de
contra-entrega. NÃO crie nenhuma seção que dependa do checkout padrão
(upsell de checkout, order bump, one-click).

Requisitos:
- duplique o tema ativo para rascunho antes de qualquer alteração
- reconstrua a página em Liquid, seção por seção, dentro de sections/
- TODA imagem, headline, cor e botão editável pelo editor visual
  (schema com settings, nada fixo no código)
- responsivo conforme o print mobile
- sem dependência de app pago
- não copie o texto do concorrente: iguale o ângulo, escreva original
- não use logo, foto, fonte ou nome de marca de terceiro

Ao terminar, liste o que criou e o que NÃO conseguiu reproduzir.
```

**Por que exigir tema rascunho:** se a rodada sair ruim, o tema publicado
continua intacto. Sem isso, uma tentativa malsucedida derruba a loja no ar.

**Por que exigir a lista do que não conseguiu:** há elementos que não
transferem, e saber quais evita procurar defeito onde não há.

**Por que "seção por seção dentro do disparo":** o pedido é único, mas a
construção interna em seções separadas é o que evita o código monolítico que
não dá para editar depois.

---

## Caminho B — sem conector

Se o setup travar, o fluxo é o mesmo, mas o código volta como texto e ele cola
à mão:

Shopify → Temas → Editar código → pasta `sections` → **+** → nome do arquivo com
extensão `.liquid` → colar → Salvar.

Se o Shopify recusar o salvamento, peça o **texto exato do erro**, devolva junto
com o código e peça a correção. Repita até salvar. Isso é rotina, não falha.

---

## Quando não ficar parecido — protocolo de recuperação

Não recomece do zero. Nesta ordem:

**1. Diga que não ficou, com especificidade.** "Não parece com o original"
produz outra tentativa genérica. Aponte o quê: *"o hero está com a imagem à
esquerda, no original está à direita; a paleta está azul, no original é
terracota; falta a faixa de garantia abaixo do botão."*

**2. Reenvie o print.** A referência visual se perde entre rodadas.

**3. Se a segunda rodada também falhar, quebre em blocos.** Peça seção por
seção — hero, depois prova social, depois garantia. O disparo único funciona bem
em página simples e degrada em página densa. Não insista contra a evidência.

**4. Congele o que deu certo.** Se uma seção saiu boa, peça para preservá-la e
trabalhar só nas outras.

---

## O que não transfere — avise antes, não depois

| Elemento | Por quê |
|---|---|
| Avaliações | Vêm de app instalado, não do tema |
| Vídeo e GIF embutidos | Mídia hospedada por terceiro |
| Fontes proprietárias | Licenciadas pela marca original |
| Seções de app pago | Dependem do app, não do código |
| Imagens de produto | Precisam ser geradas ou fotografadas |

Para as imagens, o prompt "AI Ecom Engine" traz um sistema de 6 a 7 prompts com
dicionário de paleta por vibe, incluindo **arquétipo demográfico** — quem aparece
nas fotos de lifestyle e prova social. Essa é a parte mais aproveitável dele, e
é diretamente relevante: o público 50+ da frente de WhatsApp e os públicos Latam
do COD pedem pessoas diferentes nas imagens.

---

## Preço e oferta — cuidado sério

Se ele usar o `STATE 3` do AI Ecom Engine, saiba que aquela lógica pressupõe
**pagamento antecipado por cartão, em dólar**:

- escada de preços fixa terminando em `.95`, de `$24.95` a `$89.95`
- piso de lucro de `+$20 por pedido`
- cálculo de breakeven ROAS

**Nada disso vale no COD dele.** Lucro por pedido superestima quando só 54% a
60% dos pedidos viram entrega paga, e aquela lógica não considera custo de
devolução em lugar nenhum.

Aproveite a **estrutura de oferta** (BOGO, brinde, frete grátis em dois ou mais)
e **descarte os números**. Preço, custo, frete e devolução vão para a calculadora
de margem dele, que é a única que dilui sobre entregas concretizadas.

---

## Checklist antes de publicar

- [ ] Trabalhou em tema **rascunho**, não no publicado
- [ ] Todas as seções aparecem em Adicionar seção e estão posicionadas
- [ ] Testado no modo mobile do editor
- [ ] Textos, cores e imagens editáveis pelo painel, sem tocar no código
- [ ] Idioma, moeda e formato de preço corretos para o país
- [ ] Nenhuma imagem, logo, fonte ou texto de terceiro foi reaproveitado
- [ ] Nenhuma seção depende do checkout padrão (loja COD)
- [ ] Formulário de contra-entrega instalado e testado ponta a ponta
- [ ] Preço validado na calculadora de margem, não na escada em dólar
- [ ] Recebeu a lista do que não foi possível reproduzir

---

## Um limite a declarar

Este método reproduz a **aparência** de uma loja que vende bem. Nenhum dos
materiais de origem apresenta teste A/B, antes e depois, ou qualquer evidência
de que a aparência seja a causa da venda.

Os cases de operadores que ele já tem fichados apontam **ângulo de mercado,
oferta e ticket médio** como o que move a conta. Se a oferta for fraca, uma
página idêntica à do concorrente continua fraca.

Diga isso se a conversa derivar para "cloneei a loja e não vende".
