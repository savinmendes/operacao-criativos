# -*- coding: utf-8 -*-
"""Adaptador: export CSV do Helpship (Romênia) -> pedidos no formato do modelo.

Serve de referência para escrever outros adaptadores, inclusive o do MCP: o
trabalho de um adaptador é só traduzir campos e classificar status. Nenhuma
regra de negócio mora aqui.

Armadilha específica desta fonte: só `priceOriginal` está em RON. `totalPrice`,
`costProducts` e todas as colunas de custo já vêm em EURO, convertidos pela
própria plataforma a 5,4167 RON/EUR (spread de ~2,9% sobre o mercado). Ler custo
e frete como se fossem leus inflava o teto de CPA em até 4x.
"""
import csv
import io
from datetime import datetime

from lib.modelo import ABERTO, CANCELADO, DEVOLVIDO, ENTREGUE

MAPA_STATUS = {
    "DELIVERED": ENTREGUE,
    "RETURNED": DEVOLVIDO,
    "RETURNING": DEVOLVIDO,
    "CANCELLED": CANCELADO,
    "CANCELED": CANCELADO,
}

COLUNAS_FRETE = ("costCommission", "costCourier", "costWarehouse", "costPaymentMethod")
COLUNAS_FRETE_DEV = ("costCourierReturn", "costCommissionReturn", "costWarehouseReturn")


def _num(v):
    v = (v or "").strip()
    if v in ("", "null", "None"):
        return 0.0
    try:
        return float(v)
    except ValueError:
        return 0.0


def _data(v):
    v = (v or "").strip()[:10]
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(v, f)
        except ValueError:
            pass
    return None


def carregar(caminho, hoje=None, coluna_data="createdAt", coluna_movimento=None):
    """CSV do Helpship -> lista de pedidos prontos para `modelo.medir`."""
    hoje = hoje or datetime.now()
    pedidos = []
    # utf-8-sig: o export vem com BOM, e sem isso a primeira coluna nunca casa
    with io.open(caminho, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            classe = MAPA_STATUS.get((r.get("status") or "").strip().upper(), ABERTO)
            criado = _data(r.get(coluna_data))
            movimento = _data(r.get(coluna_movimento)) if coluna_movimento else None
            pedidos.append({
                "classe": classe,
                "data": criado,
                "movimento": movimento,
                "idade": (hoje - criado).days if criado else 0,
                "preco": _num(r.get("totalPrice")),          # EUR, não RON
                "custo": _num(r.get("costProducts")),        # EUR
                "frete": sum(_num(r.get(c)) for c in COLUNAS_FRETE),
                "frete_devolucao": sum(_num(r.get(c)) for c in COLUNAS_FRETE_DEV),
                "quantidade": 1,                             # export não traz quantidade
                "produto": None,                             # nem produto
                "preco_original_ron": _num(r.get("priceOriginal")),
                "loja": (r.get("storeName") or "").strip(),
            })
    return pedidos
