# Calculadora COD — núcleo de cálculo

Toda a modelagem de unit economics do COD mora em `lib/modelo.py`. Adaptadores
traduzem uma fonte de dados para o formato de entrada; a conta não muda por fonte.

```
adaptadores/        traduzem uma fonte → lista de pedidos
  helpship_csv.py   export CSV do Helpship (Romênia) — serve de modelo
lib/modelo.py       a conta (curva de desfecho, projeção, margem, teto de CPA)
tests/              27 testes da conta
```

## Como rodar os testes

```bash
python -m unittest discover -s tests
```

## Contrato de entrada

Um adaptador devolve uma lista de dicts. É só isto que o modelo precisa:

| Campo | Tipo | O que é |
|---|---|---|
| `classe` | str | `entregue` · `devolvido` · `cancelado` · `aberto` |
| `data` | date | criação do pedido |
| `movimento` | date/None | último movimento; `None` enquanto aberto |
| `idade` | int | dias desde a criação |
| `preco` | float | valor pago pelo cliente, moeda local |
| `custo` | float | custo do fornecedor **já multiplicado pela quantidade** |
| `frete` | float | frete de ida |
| `frete_devolucao` | float | taxa extra na devolução (0 onde não existe) |
| `quantidade` | int | unidades no pedido |
| `produto` | str/None | nome do produto |

**Cancelado não é venda.** Pedido que nunca foi despachado vira taxa de não
processado e sai da base — contá-lo como venda perdida afunda a efetividade
artificialmente.

## As três decisões de modelagem

Parecem erro à primeira leitura. Não são, e não devem ser "corrigidas":

1. **Tudo se dilui sobre entregas concretizadas, não sobre pedidos enviados.**
   No COD o dinheiro só entra quando o produto chega e é pago. Diluir despesa de
   anúncio sobre pedidos enviados infla o CPA máximo na exata proporção da
   taxa de devolução.

2. **Uma devolução custa frete, não produto.** O produto volta para o estoque do
   fornecedor. Perde-se o frete de ida mais, em alguns países, uma taxa de
   retorno cobrada à parte (`frete_devolucao`).

3. **CPA é valor absoluto**, o custo por compra do gerenciador — não percentual
   do preço.

## Projeção dos pedidos em aberto

Descartar pedidos em trânsito enviesa o resultado para cima: entrega resolve em
poucos dias e devolução demora bem mais, então os abertos são
desproporcionalmente futuras devoluções.

Duas formas, e a escolha fica registrada em `metodo_projecao` na saída:

- **`medir(..., curva=None)`** (padrão) — projeta pela taxa de fechados do
  próprio grupo. Correto quando a cobertura é alta (quase tudo já fechou).
- **`medir(..., curva=curva_desfecho(...))`** — curva medida em coorte madura,
  que responde "um pedido ainda aberto no dia N acaba entregue em que %".
  Necessária quando há muitos pedidos em trânsito.

Passar uma curva global para um produto que entrega pior que a média infla o
resultado dele **em silêncio**. Por isso o padrão é a taxa do próprio grupo, e
por isso a saída sempre diz qual método usou.

> Já aconteceu de valer caro: numa rodada anterior, um problema de encoding zerou
> a curva, a projeção caiu na taxa dos fechados e a efetividade da Colômbia
> apareceu como 69,4% em vez de 60,5% — com os tetos de CPA subindo junto.

## Verificação

O adaptador do Helpship reproduz exatamente os números da versão 46 publicada
da calculadora:

| Produto | Pedidos | Entrega | Teto de CPA |
|---|---|---|---|
| Smartwatch Y68 | 156 | 67,3% | R$ 63,59 |
| Caixa de som | 89 | 39,5% | R$ 51,16 |
| Perfumes 239 | 72 | 43,5% | R$ 28,59 |

Qualquer adaptador novo deve passar por essa mesma prova antes de virar fonte
de presets: rodar contra dados cuja saída já é conhecida e bater.

## Escrevendo um adaptador novo

Copie `adaptadores/helpship_csv.py`. O trabalho é só traduzir campos e mapear
status — nenhuma regra de negócio ali dentro.

Três coisas que já morderam e valem conferir em qualquer fonte nova:

- **Moeda por coluna.** No Helpship só o preço original está em RON; custo e
  fretes já vêm em euro. Ler tudo como a mesma moeda inflou o teto em até 4x.
- **Encoding.** Use `utf-8-sig`. BOM não tratado quebra o casamento da primeira
  coluna em silêncio, e o resultado é uma conta que roda e dá errado.
- **Custo por quantidade.** Confirme se o custo da fonte já vem multiplicado
  pelas unidades ou se é unitário.

## Pendente

Adaptador do MCP `chegou-operacoes`
(`https://operacoes-api.chegouhub.com.br/mcp`), para substituir o ciclo de
export manual. Bloqueado na autorização OAuth, que exige navegador. Antes de
escrever o adaptador é preciso confirmar se o conector expõe, por pedido:
status, custo de fornecedor, frete e custo de devolução. Se só expuser agregado,
ele complementa o export mas não o substitui.
