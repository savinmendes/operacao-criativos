# -*- coding: utf-8 -*-
"""Testes do núcleo de unit economics do COD.

Estas contas decidem preço, CPA máximo e se um produto entra ou sai do catálogo.
Errar aqui em silêncio custa dinheiro real, e já custou: numa rodada anterior um
problema de encoding zerou a curva de desfecho, a projeção caiu na taxa dos
pedidos fechados e a efetividade da Colômbia apareceu inflada de 60,5% para
69,4% — com os tetos de CPA subindo junto. Os testes de curva existem por causa
disso.

Três decisões de modelagem que NÃO são bug e não devem ser "corrigidas":
  1. tudo se dilui sobre ENTREGAS CONCRETIZADAS, não sobre pedidos enviados;
  2. uma devolução custa frete (ida + taxa de retorno), não o produto;
  3. CPA é valor absoluto do gerenciador, não percentual do preço.
"""
import os
import sys
import unittest
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.modelo import (ABERTO, CANCELADO, DEVOLVIDO, ENTREGUE, classificar,
                        curva_desfecho, medir, projetar_entregas, teto_de_cpa)


def ped(classe, idade=30, mov_dias=3, preco=100.0, custo=30.0, frete=20.0,
        fdev=0.0, qtd=1, produto="X"):
    """Pedido sintético. `idade` = dias desde a criação; `mov_dias` = dias até fechar."""
    base = datetime(2026, 1, 1)
    return {
        "classe": classe, "idade": idade,
        "data": base,
        "movimento": None if classe == ABERTO else datetime(2026, 1, 1 + mov_dias),
        "preco": preco, "custo": custo, "frete": frete, "frete_devolucao": fdev,
        "quantidade": qtd, "produto": produto,
    }


class TestClassificar(unittest.TestCase):
    MAPA = {
        "ENTREGADO": ENTREGUE, "ENTREGUE": ENTREGUE,
        "DEVOLUCION": DEVOLVIDO, "RECHAZADO": DEVOLVIDO,
        "CANCELADO": CANCELADO,
    }

    def test_mapeia_conhecidos(self):
        self.assertEqual(classificar("ENTREGADO", self.MAPA), ENTREGUE)
        self.assertEqual(classificar("RECHAZADO", self.MAPA), DEVOLVIDO)
        self.assertEqual(classificar("CANCELADO", self.MAPA), CANCELADO)

    def test_ignora_caixa_e_espaco(self):
        self.assertEqual(classificar("  entregado  ", self.MAPA), ENTREGUE)

    def test_status_desconhecido_vira_aberto_e_nao_some(self):
        # tratar desconhecido como entregue ou devolvido enviesaria a conta;
        # aberto é o único default honesto — ele entra na projeção
        self.assertEqual(classificar("EM TRANSITO", self.MAPA), ABERTO)
        self.assertEqual(classificar("", self.MAPA), ABERTO)
        self.assertEqual(classificar(None, self.MAPA), ABERTO)


class TestCurvaDesfecho(unittest.TestCase):
    """A curva responde: um pedido ainda aberto no dia N acaba entregue em que %?
    Ela é medida só em coorte madura, onde quase tudo já fechou."""

    def coorte(self, n_entregues, n_devolvidos, dias_entrega=2, dias_devolucao=10):
        p = [ped(ENTREGUE, idade=60, mov_dias=dias_entrega) for _ in range(n_entregues)]
        p += [ped(DEVOLVIDO, idade=60, mov_dias=dias_devolucao) for _ in range(n_devolvidos)]
        return p

    def test_curva_cai_conforme_o_pedido_envelhece(self):
        # entrega resolve em 2 dias, devolução em 10: quanto mais velho o pedido
        # ainda aberto, menor a chance de virar entrega
        c = curva_desfecho(self.coorte(70, 30), corte_dias=13, minimo=10)
        self.assertTrue(c)
        self.assertGreater(c[0], c[max(c)])

    def test_dia_zero_bate_com_a_taxa_geral(self):
        c = curva_desfecho(self.coorte(70, 30), corte_dias=13, minimo=10)
        self.assertAlmostEqual(c[0], 0.70, places=2)

    def test_amostra_pequena_devolve_curva_vazia(self):
        # vazia é o resultado certo: melhor o chamador saber que não dá para
        # projetar do que receber uma curva inventada com 3 pedidos
        self.assertEqual(curva_desfecho(self.coorte(2, 1), corte_dias=13, minimo=10), {})

    def test_ignora_coorte_verde(self):
        # pedidos recentes ainda não fecharam; entram na curva e a inflam
        verdes = [ped(ENTREGUE, idade=2, mov_dias=1) for _ in range(50)]
        self.assertEqual(curva_desfecho(verdes, corte_dias=13, minimo=10), {})

    def test_sem_data_de_movimento_nao_entra(self):
        p = self.coorte(40, 20)
        for x in p:
            x["movimento"] = None
        self.assertEqual(curva_desfecho(p, corte_dias=13, minimo=10), {})


class TestProjetarEntregas(unittest.TestCase):
    def test_sem_abertos_entregas_sao_os_entregues(self):
        p = [ped(ENTREGUE) for _ in range(8)] + [ped(DEVOLVIDO) for _ in range(2)]
        self.assertAlmostEqual(projetar_entregas(p, {0: 0.5}), 8.0)

    def test_abertos_entram_pela_curva(self):
        p = [ped(ENTREGUE) for _ in range(8)] + [ped(ABERTO, idade=0) for _ in range(10)]
        # 8 fechados entregues + 10 abertos × 30% = 11
        self.assertAlmostEqual(projetar_entregas(p, {0: 0.3}), 11.0)

    def test_usa_o_dia_mais_proximo_disponivel_na_curva(self):
        p = [ped(ABERTO, idade=99) for _ in range(10)]
        # a curva só vai até o dia 5; pedido de 99 dias usa o dia 5
        self.assertAlmostEqual(projetar_entregas(p, {0: 0.9, 5: 0.1}), 1.0)

    def test_curva_vazia_nao_projeta_e_avisa(self):
        p = [ped(ENTREGUE) for _ in range(5)] + [ped(ABERTO) for _ in range(5)]
        with self.assertRaises(ValueError):
            projetar_entregas(p, {})


class TestTetoDeCpa(unittest.TestCase):
    def test_formula(self):
        # margem 40 por entrega, 50 entregas em 100 vendas -> teto 20 por venda
        self.assertAlmostEqual(teto_de_cpa(margem=40.0, entregas=50.0, vendas=100), 20.0)

    def test_entrega_total_teto_igual_a_margem(self):
        self.assertAlmostEqual(teto_de_cpa(margem=40.0, entregas=100.0, vendas=100), 40.0)

    def test_sem_vendas_ou_sem_entregas(self):
        self.assertEqual(teto_de_cpa(40.0, 0.0, 100), 0.0)
        self.assertEqual(teto_de_cpa(40.0, 50.0, 0), 0.0)

    def test_margem_negativa_passa_adiante(self):
        # não é papel desta função esconder prejuízo
        self.assertLess(teto_de_cpa(margem=-10.0, entregas=50.0, vendas=100), 0)


class TestMedir(unittest.TestCase):
    def cenario(self):
        """60 entregues, 40 devolvidos, nada aberto — conta fechada e verificável."""
        return ([ped(ENTREGUE, preco=100.0, custo=30.0, frete=20.0) for _ in range(60)]
                + [ped(DEVOLVIDO, preco=100.0, custo=30.0, frete=20.0, fdev=10.0)
                   for _ in range(40)])

    def test_taxas_basicas(self):
        m = medir(self.cenario(), cotacao=1.0, curva={0: 0.6})
        self.assertEqual(m["pedidos"], 100)
        self.assertAlmostEqual(m["entregas"], 60.0)
        self.assertAlmostEqual(m["entrega_pct"], 60.0)
        self.assertAlmostEqual(m["devolucao_pct"], 40.0)

    def test_devolucao_custa_frete_e_nao_produto(self):
        """40 devoluções × (20 ida + 10 retorno) = 1200, diluído em 60 entregas = 20."""
        m = medir(self.cenario(), cotacao=1.0, curva={0: 0.6})
        self.assertAlmostEqual(m["custo_devolucao_por_entrega"], 20.0)
        # margem = 100 - 30 - 20 - 20 = 30
        self.assertAlmostEqual(m["margem"], 30.0)

    def test_teto_dilui_sobre_entregas_nao_sobre_pedidos(self):
        m = medir(self.cenario(), cotacao=1.0, curva={0: 0.6})
        # 30 de margem × 60 entregas / 100 vendas = 18
        self.assertAlmostEqual(m["teto_cpa"], 18.0)

    def test_cotacao_converte_para_real(self):
        # cotação inversa: quantas unidades locais valem R$ 1
        m = medir(self.cenario(), cotacao=2.0, curva={0: 0.6})
        self.assertAlmostEqual(m["teto_cpa"], 9.0)

    def test_cancelados_viram_taxa_de_nao_processado_e_saem_da_base(self):
        p = self.cenario() + [ped(CANCELADO) for _ in range(25)]
        m = medir(p, cotacao=1.0, curva={0: 0.6})
        self.assertEqual(m["pedidos"], 100)              # cancelado não é venda válida
        self.assertAlmostEqual(m["nao_processado_pct"], 20.0)   # 25 de 125

    def test_amostra_pequena_devolve_none(self):
        self.assertIsNone(medir([ped(ENTREGUE)] * 3, cotacao=1.0,
                                curva={0: 0.6}, minimo=15))

    def test_sem_entrega_nenhuma_devolve_none(self):
        # sem entrega não há sobre o que diluir; a conta não existe
        self.assertIsNone(medir([ped(DEVOLVIDO) for _ in range(30)],
                                cotacao=1.0, curva={0: 0.6}))

    def test_padrao_projeta_pela_taxa_do_proprio_grupo(self):
        """Curva global aplicada a produto que entrega pior que a média infla o
        resultado dele em silêncio. O padrão tem que ser a taxa do grupo."""
        p = self.cenario() + [ped(ABERTO, idade=0) for _ in range(20)]
        sozinho = medir(p, cotacao=1.0)                      # 60/100 = 60%
        global_ = medir(p, cotacao=1.0, curva={0: 0.95})     # curva otimista de fora
        self.assertAlmostEqual(sozinho["entregas"], 60 + 20 * 0.6)
        self.assertAlmostEqual(global_["entregas"], 60 + 20 * 0.95)
        self.assertLess(sozinho["teto_cpa"], global_["teto_cpa"])

    def test_registra_como_projetou(self):
        com_abertos = self.cenario() + [ped(ABERTO) for _ in range(10)]
        self.assertEqual(medir(com_abertos, 1.0)["metodo_projecao"],
                         "taxa-fechados-do-grupo")
        self.assertEqual(medir(com_abertos, 1.0, curva={0: 0.5})["metodo_projecao"],
                         "curva-de-desfecho")
        # sem pedido em aberto a projeção não influencia nada, e isso fica dito
        self.assertIn("nenhum aberto", medir(self.cenario(), 1.0)["metodo_projecao"])

    def test_taxa_fechados(self):
        from lib.modelo import taxa_fechados
        self.assertAlmostEqual(taxa_fechados(self.cenario()), 0.6)
        self.assertEqual(taxa_fechados([ped(ABERTO)]), 0.0)
        self.assertEqual(taxa_fechados([]), 0.0)

    def test_cobertura_mostra_quanto_ja_fechou(self):
        p = self.cenario() + [ped(ABERTO, idade=1) for _ in range(20)]
        m = medir(p, cotacao=1.0, curva={0: 0.6})
        self.assertEqual(m["pedidos"], 120)
        self.assertAlmostEqual(m["cobertura_pct"], 100 / 120 * 100, places=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
