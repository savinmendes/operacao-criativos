# Guia operacional — montar loja Shopify seção por seção com IA

**Para quem lê este documento:** você é um assistente que vai conduzir a
construção de uma loja Shopify, passo a passo, junto com o operador. Este
documento é o procedimento; não é um resumo para ele ler sozinho.

Método derivado de três vídeos que ensinam a mesma tarefa por caminhos
diferentes, confrontados entre si (ver seção de confronto no fim), adaptado ao
contexto da operação.
Transcrição completa e ficha crítica em `01-arquivos-organizados/transcricoes-youtube/`.

---

## Contexto da operação — leia antes de começar

Ele opera **dropshipping COD (pagamento na entrega)** em Chile, Colômbia,
Guatemala, México e Romênia, além de infoprodutos e uma frente de venda 1-a-1
por WhatsApp. Isso muda três coisas em relação a qualquer tutorial genérico de
Shopify:

1. **No COD o checkout do Shopify é substituído por um formulário de
   contra-entrega.** Toda seção de upsell de checkout, order bump ou one-click
   é inútil nessas lojas. Não sugira.
2. **O dinheiro entra na entrega paga, não na compra.** Métrica de conversão da
   página é só o primeiro passo; ele já tem uma calculadora própria que dilui
   custo sobre entregas concretizadas.
3. **Público Latam, em espanhol.** Prova social, formato de preço e moeda
   precisam bater com o país.

Pergunte de qual frente e de qual país é a loja antes de começar. A resposta
muda o que faz sentido construir.

---

## A regra que governa tudo

**Uma seção por vez. Nunca a loja inteira.**

Pedir "monte minha loja com este layout" produz código com bug, link quebrado e
estrutura impossível de editar. Isso não é cautela: é o erro que o autor do
método sinaliza explicitamente como o mais comum.

Se ele pedir a loja inteira de uma vez, recuse e explique o porquê.

---

## Pré-requisitos

| Item | Observação |
|---|---|
| Conta Shopify | — |
| Tema **Dawn** publicado | Gratuito, na Theme Store. Adicionar como cópia nova para começar limpo |
| Loja de referência aberta | A que serve de inspiração de layout |
| App de formulário COD | Se for loja COD. O mercado usa Releasit; confirmar com ele o que já usa |

---

## O ciclo, por seção

Repita este ciclo inteiro para **cada** seção. Não adiante etapas.

### 1. Identificar

Peça a ele a lista de seções que quer reproduzir da loja de referência.
Exemplos comuns: barra de anúncio, hero, prova social com foto, garantia,
FAQ, comparativo.

Trate uma por vez, na ordem em que aparecem na página.

### 2. Capturar

Peça **dois prints** da seção:

- desktop
- **mobile** — este é o passo que as pessoas pulam e que faz a seção quebrar no
  celular. Não prossiga sem ele em qualquer seção com layout dinâmico.

Se a loja de referência bloquear clique direito, ele pode inspecionar a página
pelo navegador e capturar a partir dali.

### 3. Descrever

Monte o pedido com estes três elementos, sempre:

```
Crie uma seção Shopify para o tema Dawn.

O que é: <descrição objetiva do que aparece no print>
Onde vai: <home | página de produto | página de coleção>
Idioma/moeda: <espanhol MX | espanhol CO | português BR | ...>

Requisitos:
- arquivo .liquid completo, pronto para colar em sections/
- schema com settings editáveis: textos, cores e imagens ajustáveis
  pelo editor visual do Shopify (nada fixo no código)
- responsivo, conforme o print mobile anexo
- sem dependência de app pago nem de biblioteca externa
```

Anexe os dois prints.

**Por que exigir schema editável:** sem isso a seção vira bloco morto e qualquer
ajuste de cor ou texto exige mexer no código de novo. Com schema, ele muda tudo
pelo editor visual.

### 4. Instalar

1. Shopify → Loja online → Temas
2. Nos três pontos do tema → **Editar código**
3. Pasta `sections` → ícone **+**
4. Nome do arquivo com extensão: `nome-da-secao.liquid`
5. Colar o código → Salvar

### 5. Tratar o erro — isto é etapa, não exceção

É normal o Shopify recusar o primeiro salvamento. Quando acontecer:

- peça a ele o **texto exato** da mensagem de erro
- devolva o erro junto com o código atual e peça a correção
- repita até salvar

Não trate isso como falha do método. O autor mostra o erro acontecendo no
próprio tutorial e trata o ciclo como parte do processo.

### 6. Posicionar e conferir

1. Personalizar tema → **Adicionar seção** → escolher a nova
2. Arrastar para a posição certa
3. **Conferir no modo mobile do próprio editor**
4. Ajustar cores e textos pelo painel lateral, não no código

Só então passe para a próxima seção.

---

## Imagens de produto

Se ele gostar de uma foto da loja de referência, o caminho é **gerar uma
própria a partir dela como referência de composição**, não reutilizar o arquivo.

Ao gerar, mude o que separa o público dele do público da referência:
idade do modelo, ambiente, iluminação, tom de pele, vestuário. No caso dele,
isso importa de verdade: a frente de WhatsApp vende para 50+, e o COD Latam tem
públicos distintos por país.

Nunca reutilize foto, logo, nome de marca ou texto de copy de terceiro.
Estrutura de layout é referência; identidade de marca não é.

---

## Limites que você deve declarar a ele

**Este método resolve execução e custo, não conversão.** Ele reproduz a
aparência de uma loja que vende bem. Não há nenhuma evidência, no material de
origem, de que a aparência seja a causa das vendas — nenhum teste A/B, nenhum
antes e depois.

Os cases de operadores que ele já tem fichados apontam **ângulo de mercado,
oferta e ticket médio** como o que move a conta. Se a oferta for fraca, uma
página idêntica à do concorrente continua fraca.

Diga isso a ele se a conversa derivar para "clonei a loja, por que não vende".

---

---

## Confronto com outros dois métodos — leia antes de mudar de abordagem

Este guia segue o método **seção por seção**. Dois outros vídeos ensinam a mesma
tarefa por caminhos diferentes, e o confronto entre os três é o que sustenta a
escolha feita aqui. Transcrições completas dos três em
`01-arquivos-organizados/transcricoes-youtube/`.

| | **Seção por seção** (base deste guia) | **Prompt único** | **MCP direto** |
|---|---|---|---|
| Fonte | Ricky Amador, 05/07/2026 | Anthony Eclipse, 08/05/2026 | Grant Zuco, 14/06/2026 |
| Instalação | Nenhuma — navegador e Shopify | VS Code, Node.js, Git, Python, extensão | Claude Desktop, app customizado no Shopify, escopos, skill |
| Como o código chega na loja | Colar em `sections/` à mão | Arquivo de export, copiar à mão | Escrito direto na loja pelo conector |
| Granularidade | Uma seção por vez | Loja inteira num disparo | Página inteira num disparo |
| Print mobile | **Sim, exigido** | Não menciona | Não menciona |
| Resultado mostrado | Funciona, com ciclo de erro | Funciona | **Falhou na primeira tentativa** |

### O que os três concordam

Isso é o núcleo confiável, porque vem de três criadores independentes:

1. **Screenshot é a entrada.** Nenhum descreve a loja por texto; todos capturam.
2. **Parte-se de uma loja de referência que já vende.**
3. **O produto final é código Liquid** com seções instaladas no tema.
4. **Imagem se resolve fora**, gerando por IA a partir de referência.
5. **Os três vendem algo no fim** — curso, comunidade, mentoria ou ferramenta de
   afiliado. Trate toda recomendação de ferramenta específica como comissionada.

### A divergência que decide o método

**Fazer a loja inteira de uma vez, ou uma seção por vez?**

O autor do método seção por seção alerta explicitamente contra o disparo único:
produz código com bug, link quebrado e estrutura difícil de editar.

Os outros dois fazem o disparo único. E o vídeo do MCP **mostra o resultado
falhando na própria gravação**: a página gerada não se parecia com a original, e
ele precisou pedir de novo para obter algo aceitável. Ele narra isso abertamente.

Ou seja: a evidência contra o disparo único aparece dentro do material que o
defende. Por isso este guia mantém seção por seção. **Não mude para o disparo
único só porque parece mais rápido.**

### O que vale aproveitar dos outros dois

**Do método MCP — conexão direta com a loja.** Conectar o Shopify ao Claude por
app customizado permite escrever na loja sem copiar e colar. É uma capacidade
real, não só conveniência. O custo é o setup: criar app no Shopify, configurar
escopos de leitura e escrita de tema, produto e conteúdo, e conectar. O próprio
autor admite que não é amigável para iniciante.

**Quando sugerir isso a ele:** só depois de a primeira loja estar de pé pelo
método manual. Quem ainda não viu uma seção funcionar não deve começar
depurando conexão de MCP.

**Do método de prompt único — encadear a oferta.** A ideia de gerar, no mesmo
fluxo, a oferta, os prompts de imagem e os roteiros de anúncio é boa. Mas
depende de um prompt proprietário vendido por assinatura, e ele já tem processo
próprio de criativo. Aproveite a ideia da sequência, não a ferramenta.

### Limites que nenhum dos três resolve

- **Vídeo, GIF e avaliações não são clonáveis.** O autor do método MCP mostra
  isso: reviews normalmente vêm de app, e mídia embutida não transfere.
- **Nenhum mede conversão.** Os três provam que dá para reproduzir a aparência.
  Nenhum apresenta teste A/B, antes e depois, ou qualquer evidência de que a
  aparência cause a venda.

## Checklist antes de dar uma seção por pronta

- [ ] Salvou sem erro no Shopify
- [ ] Aparece em Adicionar seção e está posicionada
- [ ] Testada no modo mobile
- [ ] Textos, cores e imagens editáveis pelo painel, sem tocar no código
- [ ] Idioma e moeda corretos para o país da loja
- [ ] Nenhuma imagem, logo ou texto de terceiro foi reaproveitado
- [ ] Se for loja COD: não foi criada nenhuma seção que dependa do checkout padrão

---

## Se algo sair do previsto

| Sintoma | Causa provável |
|---|---|
| Erro ao salvar o `.liquid` | Sintaxe — devolva a mensagem exata e peça correção |
| Seção não aparece em Adicionar seção | Falta o bloco `schema` no fim do arquivo |
| Quebra no celular | Não foi enviado o print mobile |
| Não dá para editar cor/texto pelo painel | Valores fixos no código em vez de `settings` |
| Conflita com o tema | Tema não é o Dawn — confirme antes |
