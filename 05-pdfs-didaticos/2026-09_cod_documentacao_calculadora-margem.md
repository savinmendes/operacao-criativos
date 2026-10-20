# Calculadora de Margem COD — especificação funcional

Documento de referência para um agente que precise entender, operar ou modificar a ferramenta.
Artefato publicado: https://claude.ai/artifact/8yBHU2JigWBRPEut9V3y2Q
Página única em HTML, sem dependências além de fontes do Google. Todo o estado vive no navegador.

---

## 1. Para que serve

Responde uma pergunta de gestão de tráfego pago em dropshipping COD (pagamento na entrega):
**até quanto posso pagar por compra no gerenciador de anúncios antes de o produto parar de dar lucro?**

O contexto é uma operação que vende sem estoque em vários países da América Latina, onde o
cliente paga só quando recebe. Isso muda a matemática em relação a e-commerce comum: uma parte
relevante dos pedidos nunca é paga, mas o frete de ida já foi gasto.

Substitui uma planilha ("Precificação Padrão CONTRA") que tinha células quebradas.

---

## 2. Modelo econômico

Três decisões de modelagem que não são óbvias e que devem ser preservadas:

1. **Tudo é diluído sobre ENTREGAS CONCRETIZADAS, não sobre pedidos enviados.** Erro comum:
   dividir por pedidos. O custo de quem não pagou precisa ser absorvido por quem pagou.
2. **A devolução custa o frete, não o produto.** O produto volta ao estoque. Em operações onde
   a transportadora cobra à parte pela volta, soma-se também essa taxa.
3. **CPA é o custo por compra do gerenciador (Meta/Kwai/TikTok), não uma porcentagem do preço.**
   A despesa real por entrega é maior que o CPA nominal, porque parte das compras não vira entrega.

### 2.1 Conversão de moeda

A cotação é **inversa**: quantas unidades da moeda local valem R$ 1.

```
conv        = 1 / cotacao
valor_em_R$ = valor_local * conv
```

Ou seja, com CLP 185,9, um produto de 34.885 pesos vale 34.885 / 185,9 = R$ 187,65.

### 2.2 Funil

```
enviados   = vendas * (1 - naoProcessadoPct/100)
entregas   = enviados * (1 - devolucaoPct/100)
devolvidos = enviados - entregas
```

`naoProcessadoPct` = pedidos cancelados antes de virar guia de envio.
`devolucaoPct` = devolução ou não pagamento, sobre os pedidos que chegaram a ser despachados.

### 2.3 Custo por entrega

```
perdaPorDevolucao = frete + freteDevolucao
custoDevolucao    = devolvidos * perdaPorDevolucao / entregas
taxaPlataforma    = (plataformaPct/100) * precoVenda
valorCusto        = custoProduto + frete + custoDevolucao + taxaPlataforma
margem            = precoVenda - valorCusto
```

A taxa da plataforma incide só sobre o que foi efetivamente cobrado do cliente, logo só nas entregas.

### 2.4 Resultado

```
despesaAnuncio = cpaRS * vendas / entregas
lucroBruto     = margem - despesaAnuncio
taxas          = lucroBruto > 0 ? lucroBruto * (taxasPct/100) : 0
lucroEntrega   = lucroBruto - taxas
lucroTotal     = lucroEntrega * entregas
```

As taxas sobre o lucro (saque + imposto) só incidem quando há lucro: prejuízo não é transferido
nem tributado. Esse condicional é intencional.

### 2.5 Os dois tetos de CPA

```
cpaMax   = margem * entregas / vendas
cpaIdeal = cpaMax - (metaLucro/100) / (1 - taxasPct/100)
```

- **cpaMax** é o ponto de equilíbrio: pagar mais que isso dá prejuízo.
- **cpaIdeal** é o CPA que ainda deixa a meta de lucro intacta. `metaLucro` é expresso em reais
  por 100 unidades, por isso a divisão por 100. A divisão por `(1 - taxasPct/100)` existe porque
  a meta é líquida: é preciso reservar o bruto que sobrevive às taxas.

**cpaMax é o número que se compara diretamente com o "custo por compra" do gerenciador.**

---

## 3. Entradas

| Campo (id) | Unidade | O que é |
|---|---|---|
| `cpaRS` / `cpaLocal` / `cpaSlider` | R$ / moeda local | CPA do gerenciador. Os três são espelhos do mesmo valor |
| `devolucaoPct` / `devPctManual` | % | Devolução ou não pagamento. Slider e campo digitável espelhados |
| `moeda` | — | CLP, COP, MXN, GTQ, RON ou BRL |
| `cotacao` | local por R$ 1 | Preenchida automaticamente ao trocar de moeda |
| `precoVenda` | moeda local | Preço cobrado do cliente |
| `custoProduto` | moeda local | Custo do fornecedor |
| `frete` | moeda local | Frete de ida |
| `freteDevolucao` | moeda local | Taxa extra de retorno. Zero onde a transportadora não cobra |
| `plataformaPct` | % do preço | Dropi, Ecomhub etc. |
| `taxasPct` | % do lucro | Saque + imposto |
| `vendasTotais` | unidades | Base do período. Padrão 100 |
| `naoProcessadoPct` | % | Cancelados antes do envio |
| `metaLucro` | R$ por 100 un | Meta usada no cpaIdeal |

---

## 4. Saídas

- **Lucro por entrega concretizada** — número principal.
- **CPA atual / CPA ideal / CPA máximo / Lucro total** — quatro indicadores.
- **Régua horizontal** — zona verde até o cpaMax, vermelha depois, com marcas do CPA atual,
  do cpaIdeal e do cpaMax.
- **Funil** — vendas → enviados → entregas.
- **Cascata** — preço − custos = margem − anúncio = lucro bruto − taxas = lucro por entrega.
- **Mapa de calor** — matriz de 9 faixas de CPA × 6 faixas de devolução (20% a 70%), alternável
  entre lucro total e lucro por entrega. Escala de cor HSL de três paradas ancorada no zero:
  vermelho → laranja/amarelo no equilíbrio → verde. A interpolação é em HSL porque em RGB o
  trecho laranja→verde passa por um cáqui ilegível.
- **Ranking** — ver seção 6.

---

## 5. Alertas

Três banners, mutuamente coordenados:

| Alerta | Gatilho | Mensagem |
|---|---|---|
| 🛑 vermelho | `lucroEntrega < 0` | "Produto dando prejuízo — pare os anúncios agora ou realinhe a oferta" |
| ⚠️ âmbar | não está em prejuízo **e** lucro por 100 ≤ R$ 1.000 **e** gasto por 100 ≥ R$ 3.000 | "Avaliar se ainda vale a pena rodar esse produto" |
| 👀 verde | `cpaIdeal - cpaAtual ≥ R$ 10` | "Vamos escalar" |

O alerta âmbar é suprimido quando o vermelho está ativo, para não empilhar dois avisos
contraditórios. Existe ainda um quarto banner que avisa quando a cotação em uso tem mais de
7 dias.

---

## 6. Presets de dados reais

Dois conjuntos, selecionáveis por operação. Carregar um preset preenche preço, custo, frete,
frete de devolução, não processados e (quando medida) a devolução.

### 6.1 Chile — Dropi

13 produtos + linha de referência "Operação inteira". Medidos em 2.660 pedidos até 12/09/2026.
Cada produto tem duas bases alternáveis:

- **Mix real** — todas as ofertas juntas (1, 2 e 3 unidades). Preço e custo são a média por
  pedido entregue. Como o export já traz o custo multiplicado pela quantidade, a oferta de 2
  unidades entra com o preço dela e o custo dobrado automaticamente.
- **Só 1 unidade** — isola a oferta unitária, para desenhar preço de uma oferta nova.

**Metodologia de efetividade (importante, é onde se erra):**

- Entregue, Devolução e Cancelado entram pelo desfecho real.
- Pedidos ainda em trânsito **não são descartados nem contados como entrega**. Entram pela curva
  de desfecho da própria operação, medida numa coorte antiga já totalmente resolvida: um pedido
  ainda aberto no 7º dia entrega em 6,1% dos casos, no 9º em 2,7%, no 13º em 0,6%. Isso porque
  entrega resolve em 3 dias na mediana e devolução em 10.
- Descartar os abertos marcaria 65,0% de efetividade. Contando-os pela curva dá **54,4%**.
- Existe corte de maturidade: as semanas mais recentes têm pouca coisa fechada e o que fechou é
  quase só entrega, o que produz miragens de 100% de efetividade.
- Produtos com menos de 85% da base já fechada são sinalizados em laranja na interface.

### 6.2 Guatemala — DropLatam

7 ofertas, medidas em 101 pedidos de 16 a 21/09/2026. O mapeamento de colunas foi validado pela
identidade `preço − custo fornecedor − frete = ganancia`, que fecha em todos os pedidos entregues.

**Diferença estrutural em relação ao Chile:** a devolução custa o frete de ida **mais** uma taxa
de retorno (~20,7 GTQ na capital, ~28,3 no interior). Por isso existe o campo `freteDevolucao`.

**Limitação declarada:** a taxa de devolução da Guatemala **não foi medida**. O export tem poucos
dias e quase nenhuma devolução fechada. Os presets dessa operação deixam `dev = null`, o que faz
o preset **não mexer** no controle de devolução — o número é premissa do usuário, e a interface
marca isso com a etiqueta "premissa sua" em vez de "medida". Referências disponíveis: 1% de
cancelamento e 21,9% dos despachados em novedad.

---

## 7. Ranking com o CPA atual

Roda o mesmo modelo para todas as ofertas da operação selecionada, mantendo fixos o CPA, a taxa
da plataforma e as taxas sobre o lucro que estão na tela, e variando apenas os dados do produto.
Responde: *"se eu pagasse este mesmo CPA em todos, a cada 100 pedidos gerados, quanto cada um
devolveria?"*

- Ordenável por **lucro por 100** ou por **folga de CPA** (quanto ainda cabe subir).
- Cada linha traz etiqueta: bate a meta / no lucro / prejuízo.
- Clicar numa linha carrega aquele produto na calculadora inteira.
- A linha "Operação inteira" fica fora da disputa, exibida como régua no rodapé da lista.
- Quando a operação não tem devolução medida, todas as ofertas rodam com a devolução da tela e a
  interface avisa que a ordem compara margem, não efetividade.

---

## 8. Cotações

Cinco moedas com valor e data de verificação. Regra aprendida na prática: **puxar todas da mesma
fonte**. Misturar Wise, XE e Investing produziu erro de 6% num caso real. Fontes divergem muito
entre si no mesmo dia.

Uma cotação digitada pelo usuário fica salva no navegador e **passa por cima do valor de mercado
embutido no código**, inclusive após republicação. Por isso existe um botão de restaurar que
devolve as taxas ao padrão — sem ele não haveria como voltar atrás a não ser digitando tudo.

---

## 9. Persistência

`localStorage`, em duas chaves: uma para as cotações, outra para o restante do estado. Toda
leitura e escrita é envolvida em try/catch e a página funciona sem elas.

**Armadilha a conhecer:** mudar um valor padrão no HTML não chega a um navegador que já tem
estado salvo, porque o carregamento restaura por cima. Uma chave nova, ao contrário, mantém o
padrão do HTML porque não existe no armazenamento.

Há ainda uma flag `editando` que impede que o `render()` sobrescreva o campo em que o usuário
está digitando — necessária porque os campos de CPA e de devolução são espelhados entre si.

---

## 10. Limitações a declarar sempre

- Os presets são retratos de um período e não se atualizam sozinhos.
- Tetos de CPA mostrados nas análises são anteriores à taxa da plataforma; na calculadora, com
  ela ligada, caem alguns reais.
- Produtos com amostra pequena (menos de ~30 pedidos) são teste, não conclusão.
- A curva de desfecho assume que o período atual se comporta como o anterior. Mudança de
  transportadora invalida a projeção.
- A devolução da Guatemala segue sem medição.

---

## 11. Regra de ouro

Nunca preencher um campo com número inventado. Quando o dado não existe, o comportamento correto
é deixar o controle sob responsabilidade do usuário e **dizer na tela que aquilo é premissa, não
medição**. Um preset que silenciosamente não muda um campo parece defeito; um preset que diz por
que não mudou é informação.
