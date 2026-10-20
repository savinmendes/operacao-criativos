# -*- coding: utf-8 -*-
"""Núcleo de unit economics do COD (pagamento na entrega).

Este módulo é o único lugar onde a conta mora. Adaptadores (export em xlsx/csv,
MCP, API de plataforma) só precisam entregar uma lista de pedidos no formato
descrito em `CONTRATO` — a modelagem não muda por fonte de dados.

Três decisões de modelagem que parecem erro e não são:

1. **Tudo se dilui sobre entregas concretizadas, não sobre pedidos enviados.**
   No COD o dinheiro só entra quando o produto chega e é pago. Diluir despesa de
   anúncio sobre pedidos enviados faz o CPA máximo parecer maior do que é, na
   exata proporção da taxa de devolução.

2. **Uma devolução custa frete, não produto.** O produto volta para o estoque do
   fornecedor. O que se perde é o frete de ida mais, em alguns países, uma taxa
   de retorno cobrada à parte.

3. **CPA é valor absoluto**, o custo por compra do gerenciador de anúncios — não
   um percentual do preço de venda.
"""
from collections import defaultdict

ENTREGUE = "entregue"
DEVOLVIDO = "devolvido"
CANCELADO = "cancelado"
ABERTO = "aberto"

CONTRATO = """
Cada pedido é um dict com:

  classe            str   um de: entregue | devolvido | cancelado | aberto
  idade             int   dias desde a criação do pedido até hoje
  data              date  criação (opcional se `idade` vier pronta)
  movimento         date  último movimento; None enquanto aberto
  preco             float valor pago pelo cliente, moeda local
  custo             float custo do fornecedor JÁ multiplicado pela quantidade
  frete             float frete de ida
  frete_devolucao   float taxa extra cobrada quando devolve (0 onde não há)
  quantidade        int   unidades no pedido
  produto           str   nome do produto (None quando a fonte não traz)

Cancelado é pedido que nunca chegou a ser despachado: vira taxa de não
processado e NÃO entra na base de vendas válidas.
"""


# ------------------------------------------------------------- classificação

def classificar(status, mapa):
    """Status bruto da plataforma -> classe interna.

    Status desconhecido vira `aberto` de propósito. Chutar entregue infla a
    efetividade; chutar devolvido a afunda. Aberto é o único default honesto —
    e ainda participa da projeção pela curva.
    """
    if not status:
        return ABERTO
    return mapa.get(str(status).strip().upper(), ABERTO)


# ---------------------------------------------------------- curva de desfecho

def curva_desfecho(pedidos, corte_dias=13, minimo=10, ate_dia=25):
    """Probabilidade de um pedido ainda aberto no dia N acabar entregue.

    Medida só sobre coorte madura (idade >= corte_dias), onde praticamente tudo
    já fechou. Serve para projetar os pedidos em trânsito em vez de descartá-los.

    Descartar os abertos inflaria o resultado, porque entrega resolve em poucos
    dias e devolução demora bem mais — os abertos são desproporcionalmente
    futuras devoluções.

    Devolve {} quando não há amostra suficiente. Vazio é resposta legítima: o
    chamador precisa saber que não dá para projetar, em vez de receber uma
    curva inventada a partir de três pedidos.
    """
    ref = []
    for p in pedidos or []:
        if p.get("idade", 0) < corte_dias:
            continue
        if p.get("classe") not in (ENTREGUE, DEVOLVIDO):
            continue
        if not p.get("movimento") or not p.get("data"):
            continue
        ref.append((max(0, (p["movimento"] - p["data"]).days), p["classe"]))

    if len(ref) < minimo:
        return {}

    curva = {}
    for n in range(0, ate_dia + 1):
        abertos_no_dia = [c for dias, c in ref if dias > n]
        if n == 0:
            abertos_no_dia = [c for _, c in ref]     # dia 0 = a taxa geral
        if len(abertos_no_dia) < minimo:
            break
        curva[n] = sum(1 for c in abertos_no_dia if c == ENTREGUE) / len(abertos_no_dia)
    return curva


def taxa_fechados(pedidos):
    """Taxa de entrega entre os pedidos já fechados. 0.0 se não houver nenhum.

    Só é uma projeção honesta quando quase tudo já fechou (cobertura alta). Com
    muitos pedidos em trânsito ela infla, porque entrega resolve rápido e
    devolução demora — aí o certo é `curva_desfecho`.
    """
    fechados = [p for p in pedidos or [] if p.get("classe") in (ENTREGUE, DEVOLVIDO)]
    if not fechados:
        return 0.0
    return sum(1 for p in fechados if p.get("classe") == ENTREGUE) / len(fechados)


def projetar_entregas(pedidos, curva):
    """Entregues confirmados + projeção dos abertos pela curva."""
    entregues = [p for p in pedidos if p.get("classe") == ENTREGUE]
    abertos = [p for p in pedidos if p.get("classe") == ABERTO]
    if abertos and not curva:
        raise ValueError(
            "há pedidos em aberto mas a curva de desfecho está vazia — sem ela a "
            "projeção cairia na taxa dos fechados, que infla a efetividade")
    total = float(len(entregues))
    if curva:
        teto = max(curva)
        for p in abertos:
            total += curva[min(max(p.get("idade", 0), 0), teto)]
    return total


# ---------------------------------------------------------------- resultado

def teto_de_cpa(margem, entregas, vendas):
    """CPA máximo por venda para a operação empatar.

    A margem existe só na entrega, mas o anúncio é pago em toda venda — por isso
    a margem é multiplicada pela taxa de entrega.
    """
    if not vendas or not entregas:
        return 0.0
    return margem * entregas / float(vendas)


def _media(valores):
    valores = [v for v in valores if v is not None]
    return sum(valores) / len(valores) if valores else 0.0


def medir(pedidos, cotacao, curva=None, minimo=15, frete_devolucao_fixo=None):
    """Mede um grupo de pedidos (um produto, um país, a operação inteira).

    `cotacao` é inversa: quantas unidades da moeda local valem R$ 1.

    `curva=None` projeta os pedidos em aberto pela taxa de fechados DESTE grupo.
    É o padrão porque passar uma curva global para um produto que entrega pior
    que a média infla o resultado dele em silêncio — erro fácil de cometer e
    impossível de notar olhando só o número final. O resultado sempre registra
    em `metodo_projecao` como a projeção foi feita, para a origem ficar rastreável.

    Devolve None quando a amostra é pequena demais ou não há entrega alguma —
    sem entrega não há sobre o que diluir, e a conta simplesmente não existe.
    """
    pedidos = list(pedidos or [])
    entregues = [p for p in pedidos if p.get("classe") == ENTREGUE]
    devolvidos = [p for p in pedidos if p.get("classe") == DEVOLVIDO]
    cancelados = [p for p in pedidos if p.get("classe") == CANCELADO]
    abertos = [p for p in pedidos if p.get("classe") == ABERTO]

    base = entregues + devolvidos + abertos          # vendas válidas
    fechados = entregues + devolvidos
    if len(fechados) < minimo or not entregues:
        return None

    if curva is None:
        curva = {0: taxa_fechados(base)}
        metodo = "taxa-fechados-do-grupo"
    else:
        metodo = "curva-de-desfecho"
    if not abertos:
        metodo = "nenhum aberto — projeção não usada"

    entregas = projetar_entregas(base, curva)
    if entregas <= 0:
        return None

    preco = _media([p.get("preco") for p in entregues])
    custo = _media([p.get("custo") for p in entregues])
    frete = _media([p.get("frete") for p in base])

    if frete_devolucao_fixo is not None:
        fdev = frete_devolucao_fixo
    else:
        # só parte das devoluções tem taxa de retorno lançada; o custo esperado
        # por devolução é a média das que cobram, ponderada pela fração que cobra
        com_taxa = [p.get("frete_devolucao") or 0.0 for p in devolvidos
                    if p.get("frete_devolucao")]
        fdev = (_media(com_taxa) * len(com_taxa) / len(devolvidos)) if (com_taxa and devolvidos) else 0.0

    perdidas = len(base) - entregas
    custo_dev_por_entrega = perdidas * (frete + fdev) / entregas
    margem = preco - custo - frete - custo_dev_por_entrega

    cot = cotacao or 1.0
    return {
        "pedidos": len(base),
        "entregues": len(entregues),
        "devolvidos": len(devolvidos),
        "abertos": len(abertos),
        "cancelados": len(cancelados),
        "cobertura_pct": round(len(fechados) / len(base) * 100, 1),
        "unidades_por_pedido": round(_media([p.get("quantidade", 1) for p in entregues]), 2),
        "entregas": round(entregas, 2),
        "entrega_pct": round(entregas / len(base) * 100, 1),
        "devolucao_pct": round((1 - entregas / len(base)) * 100, 1),
        "nao_processado_pct": round(
            len(cancelados) / (len(cancelados) + len(base)) * 100, 1) if base else 0.0,
        "preco": round(preco, 2),
        "custo": round(custo, 2),
        "frete": round(frete, 2),
        "frete_devolucao": round(fdev, 2),
        "custo_devolucao_por_entrega": round(custo_dev_por_entrega, 2),
        "margem": round(margem, 2),
        "teto_cpa": round(teto_de_cpa(margem, entregas, len(base)) / cot, 2),
        "metodo_projecao": metodo,
    }


def medir_por_produto(pedidos, cotacao, curva, minimo=15, frete_devolucao_fixo=None):
    """Aplica `medir` produto a produto, do maior volume para o menor."""
    grupos = defaultdict(list)
    for p in pedidos or []:
        grupos[p.get("produto") or "(sem produto)"].append(p)

    saida = []
    for nome, gg in sorted(grupos.items(), key=lambda x: -len(x[1])):
        m = medir(gg, cotacao, curva, minimo, frete_devolucao_fixo)
        if m:
            m["produto"] = nome
            saida.append(m)
    return saida
