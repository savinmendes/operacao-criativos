---
name: clonar-loja-ecommerce
description: Reconstrói o design de uma página ou loja de e-commerce a partir de uma loja de referência, gerando as seções em código no tema do usuário, com tudo editável pelo editor visual. Use sempre que a pessoa pedir para clonar, copiar, replicar, recriar ou "fazer igual" o design de uma loja, página de produto ou landing de concorrente — mesmo em pedidos informais como "quero uma loja parecida com essa", "copia esse layout pra mim", "monta minha página igual a desse site", "refaz minha loja no estilo dessa". Também use quando pedirem para montar uma loja nova partindo de um site de referência, ou para reconstruir uma seção específica (hero, prova social, comparativo, garantia) vista em outro lugar. É genérica: funciona para qualquer plataforma, nicho, país e modelo de venda, e busca o contexto do negócio em tempo de execução.
---

# Clonar design de loja de e-commerce

Esta skill reconstrói o design de uma loja de referência dentro do tema do
usuário, em código, com cada elemento editável pelo editor visual — não como
bloco fixo que exige mexer no código a cada ajuste.

## Quando usar

Sempre que alguém quiser reproduzir o design de uma loja, página de produto ou
seção vista em outro site. Não é necessária para ajustar uma loja que já existe
sem referência externa — nesse caso um pedido direto resolve.

---

## Passo 0 — Parâmetros

Infira o que puder. **Só pergunte o que for essencial e não der para inferir.**

| Parâmetro | Como resolver |
|---|---|
| Loja de referência | URL que a pessoa indicar. Sem ela, pergunte — é o único item sem o qual não dá para começar |
| Escopo | Página inteira, só a página de produto, ou seções específicas |
| Plataforma e tema | Pergunte se não estiver claro. O código gerado depende disso |
| **Modelo de venda** | **Determine sempre.** Ver "Modelo de venda" abaixo — muda o que faz sentido construir |
| País, idioma e moeda | Definem formato de preço, prova social e texto |
| Contexto do negócio | Se o projeto tiver pasta de contexto (`contexto/`, `sops/` ou equivalente), leia antes de começar |

### Modelo de venda — determine antes de construir

Pergunte, ou infira do contexto do projeto, **como o dinheiro entra**:

| Modelo | Consequência para o que você constrói |
|---|---|
| **Pagamento antecipado** (cartão, Pix, checkout padrão) | Seções de upsell de checkout, order bump e one-click fazem sentido |
| **Pagamento na entrega / contra-entrega** | O checkout costuma ser substituído por formulário. **Não construa nada que dependa do checkout padrão** — é trabalho perdido |
| **Venda por conversa** (WhatsApp, closer, ligação) | A página serve de apoio, não fecha a venda. O destino do botão é o canal, não o carrinho |

Errar isso produz uma loja bonita com seções inúteis.

---

## O que esta skill gera, e o que não gera

| | |
|---|---|
| **Gera** | Design e código: seções, layout, estrutura, responsividade |
| **Não gera** | Conteúdo de venda: copy final, oferta, preço, imagens de produto, roteiros de anúncio |

São etapas diferentes. Construa a estrutura primeiro; conteúdo é outro trabalho.
Se a pessoa pedir os dois num disparo só, avise que o resultado degrada nos dois
e proponha separar.

---

## Expectativa realista

**A primeira tentativa pode não sair parecida.** Isso é comum e não indica que o
método falhou.

Trate a iteração como parte do processo. O protocolo de recuperação está abaixo
e deve ser usado sem constrangimento. Diga isso à pessoa **antes** de começar,
para ela não interpretar a primeira rodada como fracasso.

---

## Fluxo

### 1. Capturar a referência

Peça capturas de **página inteira**, e sempre em dois formatos:

- desktop
- **mobile**

O print mobile é o passo mais pulado, e é o que faz a página quebrar no celular.
Não prossiga sem ele em qualquer layout com colunas ou grade.

Se a referência bloquear clique direito, a captura pode ser feita pelo
inspetor do navegador.

### 2. Proteger o que já existe

**Antes de qualquer alteração, duplique o tema ativo para rascunho.**

Se a rodada sair ruim, o que está no ar continua intacto. Sem isso, uma
tentativa malsucedida derruba a loja publicada. Esta etapa não é opcional.

### 3. Construir

Monte o pedido com estes elementos:

```
Reconstrua <escopo> no tema <tema> da minha loja.

Referência: <url>
Anexos: print desktop e print mobile

País, idioma e moeda: <...>
Modelo de venda: <...>
  → se for pagamento na entrega: NÃO crie nada que dependa do
    checkout padrão (upsell de checkout, order bump, one-click)

Requisitos:
- duplique o tema ativo para rascunho antes de alterar qualquer coisa
- construa em seções separadas, uma por arquivo
- TODO texto, cor, imagem e botão editável pelo editor visual
  (schema com settings; nada fixo no código)
- responsivo conforme o print mobile
- sem dependência de app pago
- não copie o texto da referência: iguale a estrutura e o ângulo,
  escreva original
- não use logo, foto, fonte ou nome de marca de terceiro

Ao terminar, liste o que criou e o que NÃO conseguiu reproduzir.
```

**Por que seções separadas mesmo num pedido único:** evita o código monolítico
que não dá para editar depois. Mantém a velocidade sem herdar o defeito.

**Por que exigir schema com settings:** sem isso cada ajuste de cor ou texto
exige voltar ao código. Com schema, a pessoa muda tudo pelo painel.

**Por que exigir a lista do que não conseguiu:** há elementos que não transferem,
e saber quais evita procurar defeito onde não há.

### 4. Instalar e conferir

Se houver conector entre o assistente e a plataforma, o código vai direto.
Senão, a pessoa cola à mão no editor de código do tema, em arquivos separados
dentro da pasta de seções.

Erro ao salvar é rotina, não falha. Peça o **texto exato do erro**, devolva junto
com o código, peça a correção, repita até salvar.

Depois: posicionar a seção, conferir no modo mobile do editor, ajustar cores e
textos pelo painel — nunca no código.

---

## Quando não ficar parecido

Não recomece do zero. Nesta ordem:

**1. Aponte o que está diferente, com especificidade.** "Não parece com o
original" produz outra tentativa genérica. Nomeie: posição invertida, paleta
errada, seção faltando, proporção da imagem.

**2. Reenvie a captura.** A referência visual se perde entre rodadas.

**3. Se a segunda rodada falhar, quebre em blocos.** Peça uma seção por vez. O
disparo único funciona bem em página simples e degrada em página densa. Não
insista contra a evidência.

**4. Congele o que deu certo.** Peça para preservar as seções aprovadas e
trabalhar só nas pendentes.

---

## O que normalmente não transfere

Avise **antes**, não depois:

| Elemento | Por quê |
|---|---|
| Avaliações e depoimentos | Costumam vir de app instalado, não do tema |
| Vídeo e GIF embutidos | Mídia hospedada por terceiro |
| Fontes proprietárias | Licenciadas pela marca original |
| Seções de app pago | Dependem do app, não do código |
| Imagens de produto | Precisam ser geradas ou fotografadas |

---

## Limites — declare, não esconda

**Estrutura e layout são referência legítima. Identidade não é.** Logo, nome de
marca, fotos originais, fontes licenciadas e texto de copy pertencem a quem os
fez. Iguale o ângulo e a estrutura; escreva o texto do zero.

Se a pessoa pedir para copiar identidade de marca, recuse essa parte
especificamente, explique por quê em uma frase, e siga com o resto.

**Aparência não é causa de venda.** Esta skill reproduz o visual de uma loja que
vende bem. Isso não transfere o resultado dela: oferta, ângulo, preço e tráfego
continuam sendo o que decide. Se a conversa derivar para "cloneei e não vende",
diga isso com clareza em vez de sugerir mais ajustes de design.

**Cuidado com regra de preço importada.** Fórmulas de precificação de tutoriais
quase sempre pressupõem pagamento antecipado e moeda forte. Em venda com
pagamento na entrega, lucro calculado por pedido superestima, porque parte dos
pedidos não vira entrega paga e a devolução tem custo próprio. Se o projeto tiver
uma ferramenta própria de margem, use-a; se não, sinalize a limitação em vez de
aplicar a fórmula do tutorial.

---

## Checklist antes de publicar

- [ ] Trabalhou em tema rascunho, não no publicado
- [ ] Todas as seções aparecem no editor e estão posicionadas
- [ ] Testado em largura mobile
- [ ] Texto, cor e imagem editáveis pelo painel, sem tocar no código
- [ ] Idioma, moeda e formato de preço corretos
- [ ] Nada dependente de checkout padrão, se o modelo for pagamento na entrega
- [ ] Nenhuma imagem, logo, fonte ou texto de terceiro reaproveitado
- [ ] Preço validado pela conta do próprio negócio, não por fórmula de tutorial
- [ ] Recebeu a lista do que não foi possível reproduzir

---

## Referências

- [`references/conector-plataforma.md`](references/conector-plataforma.md) —
  como ligar o assistente direto à plataforma para escrever sem copiar e colar,
  e quando isso vale a pena
