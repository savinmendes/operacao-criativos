# -*- coding: utf-8 -*-
"""Testes do Fluxo 0: levar transcrições novas para a base e manter o índice."""
import io
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from alimentar import alimentar, montar_indice, slug  # noqa: E402


def transcricao(titulo, canal, publicado="10/10/2026", duracao="1:02:03"):
    return (f"# {titulo}\n\n| | |\n|---|---|\n| Canal | {canal} |\n| Duração | {duracao} |\n"
            f"| Publicado | {publicado} |\n| URL | https://www.youtube.com/watch?v=X |\n\n---\n\n"
            "**[00:00]** Hoje vamos falar de VSL e escala.\n")


class TestAlimentar(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.origem = os.path.join(self.tmp, "origem")
        self.base = os.path.join(self.tmp, "base")
        os.makedirs(self.origem)
        for nome, canal in [("ep1__AAA.md", "VTurb"), ("ep2__BBB.md", "VTurb"), ("outro__CCC.md", "Outro Canal")]:
            with io.open(os.path.join(self.origem, nome), "w", encoding="utf-8") as f:
                f.write(transcricao(nome[:-3], canal))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_slug(self):
        self.assertEqual(slug("VTurb Oficial!"), "vturb-oficial")
        self.assertEqual(slug("Canal Ação"), "canal-acao")

    def test_copia_so_o_canal_pedido_e_por_pasta_de_canal(self):
        r = alimentar(self.origem, self.base, canal="vturb")
        self.assertEqual(r["copiados"], 2)
        self.assertTrue(os.path.exists(os.path.join(self.base, "transcricoes", "vturb", "ep1__AAA.md")))
        self.assertFalse(os.path.exists(os.path.join(self.base, "transcricoes", "outro-canal", "outro__CCC.md")))

    def test_nao_copia_duas_vezes(self):
        alimentar(self.origem, self.base)
        r = alimentar(self.origem, self.base)
        self.assertEqual(r["copiados"], 0)
        self.assertEqual(r["ja_estavam"], 3)

    def test_gera_esqueleto_de_ficha_e_indice(self):
        alimentar(self.origem, self.base, canal="VTurb")
        fichas = os.path.join(self.base, "transcricoes", "vturb", "_fichas")
        self.assertTrue(os.path.isdir(fichas))
        self.assertEqual(len([f for f in os.listdir(fichas) if f.endswith(".md")]), 2)
        indice = io.open(os.path.join(self.base, "INDICE.md"), encoding="utf-8").read()
        self.assertIn("ep1__AAA", indice)
        self.assertIn("VTurb", indice)
        self.assertIn("esqueleto", indice)  # ficha ainda não preenchida

    def test_indice_marca_ficha_preenchida(self):
        alimentar(self.origem, self.base, canal="VTurb")
        fichas = os.path.join(self.base, "transcricoes", "vturb", "_fichas")
        f = os.path.join(fichas, sorted(os.listdir(fichas))[0])
        texto = io.open(f, encoding="utf-8").read().replace("[PREENCHER]", "ok")
        io.open(f, "w", encoding="utf-8").write(texto)
        indice = montar_indice(self.base)
        self.assertIn("preenchida", indice)


if __name__ == "__main__":
    unittest.main()
