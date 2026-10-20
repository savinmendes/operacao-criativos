# -*- coding: utf-8 -*-
"""Testes da extração automática de fichas.

O que se testa aqui é só a parte mecânica: parsear a transcrição, achar os
números declarados, isolar o resumo de abertura e fatiar o material para leitura.
O julgamento (o que é tática replicável, o que é anedota) é feito pelo modelo
seguindo a SKILL.md e não tem teste automático.

A legenda automática do YouTube destrói termos técnicos — "ROAS" vira "ruas",
"rost", "RAS", "Ross". Boa parte destes testes existe por causa disso.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from fichar import (blocos, fatiar, ler_metadados, mencoes, numeros_declarados,
                    resumo_de_abertura, tempo_para_segundos)


CABECALHO = """# Um título qualquer

| | |
|---|---|
| Canal | CanalX |
| Duração | 3:55:38 |
| Publicado | 22/09/2026 |
| URL | https://www.youtube.com/watch?v=ABC |
| Origem da transcrição | auto-legenda (pt-orig) |
| Blocos | 453 (janela de 30s) |

---

"""


class TestTempo(unittest.TestCase):
    def test_mm_ss_e_h_mm_ss(self):
        self.assertEqual(tempo_para_segundos("00:00"), 0)
        self.assertEqual(tempo_para_segundos("01:15"), 75)
        self.assertEqual(tempo_para_segundos("1:02:05"), 3725)

    def test_invalido(self):
        self.assertIsNone(tempo_para_segundos("abc"))
        self.assertIsNone(tempo_para_segundos(""))


class TestMetadados(unittest.TestCase):
    def test_le_a_tabela(self):
        m = ler_metadados(CABECALHO)
        self.assertEqual(m["titulo"], "Um título qualquer")
        self.assertEqual(m["canal"], "CanalX")
        self.assertEqual(m["url"], "https://www.youtube.com/watch?v=ABC")
        self.assertEqual(m["duracao"], "3:55:38")
        self.assertIn("auto-legenda", m["origem"])

    def test_arquivo_sem_tabela_nao_quebra(self):
        m = ler_metadados("# Só um título\n\ntexto solto\n")
        self.assertEqual(m["titulo"], "Só um título")
        self.assertEqual(m.get("canal"), None)


class TestBlocos(unittest.TestCase):
    def test_parseia(self):
        t = CABECALHO + "**[00:00]** primeiro\n\n**[01:15]** segundo\n\n**[1:02:05]** terceiro\n"
        b = blocos(t)
        self.assertEqual(len(b), 3)
        self.assertEqual(b[0]["seg"], 0)
        self.assertEqual(b[0]["texto"], "primeiro")
        self.assertEqual(b[1]["seg"], 75)
        self.assertEqual(b[2]["seg"], 3725)
        self.assertEqual(b[2]["tempo"], "1:02:05")

    def test_texto_sem_blocos(self):
        self.assertEqual(blocos("nada aqui"), [])


class TestResumoDeAbertura(unittest.TestCase):
    """Todo episódio abre com o host resumindo o que o convidado vai cobrir.
    É um abstract pronto e de graça — vale isolar antes de qualquer leitura."""

    def bs(self, *textos):
        return [{"seg": i * 30, "tempo": "%02d:%02d" % (i // 2, (i % 2) * 30),
                 "texto": t} for i, t in enumerate(textos)]

    def test_corta_na_marca_de_inicio(self):
        b = self.bs("o convidado fez X", "e vai contar Y",
                    "chega de conversa, vamos começar o podcast",
                    "seja muito bem-vindo", "aí começa o papo de verdade")
        r = resumo_de_abertura(b)
        self.assertEqual(len(r), 2)
        self.assertIn("fez X", r[0]["texto"])

    def test_aceita_outras_marcas(self):
        for marca in ("bora pro podcast", "vamos começar aqui o podcast",
                      "com vocês, Fulano", "seja muito bem-vindo"):
            b = self.bs("resumo", marca + " e tal", "depois")
            self.assertEqual(len(resumo_de_abertura(b)), 1, marca)

    def test_sem_marca_usa_teto(self):
        b = self.bs(*["bloco %d" % i for i in range(40)])
        r = resumo_de_abertura(b, teto=12)
        self.assertEqual(len(r), 12)

    def test_vazio(self):
        self.assertEqual(resumo_de_abertura([]), [])


class TestNumerosDeclarados(unittest.TestCase):
    def achar(self, texto):
        return [n["trecho"] for n in numeros_declarados(
            [{"seg": 0, "tempo": "00:00", "texto": texto}])]

    def test_dinheiro(self):
        self.assertTrue(self.achar("faturou R$ 40 milhões no ano"))
        self.assertTrue(self.achar("o ticket é 997"))
        self.assertTrue(self.achar("custa R$ 100.000"))

    def test_volume_por_dia(self):
        for t in ("fazia 100.000 por dia", "20k dia", "100k no dia",
                  "20 mil por dia", "fez 5 milhões no mês"):
            self.assertTrue(self.achar(t), t)

    def test_percentual(self):
        self.assertTrue(self.achar("converte 25% direto"))
        self.assertTrue(self.achar("1% de conversão de VSL"))

    def test_digitos(self):
        self.assertTrue(self.achar("lucra múltiplos sete dígitos"))
        self.assertTrue(self.achar("uma VSL de nove dígitos"))

    def test_roas_mesmo_destruido_pela_legenda(self):
        # a auto-legenda escreve ROAS como ruas / rost / RAS / Ross / ROI
        for t in ("um ruas de 1.5", "tinha rost três", "o RAS caiu para 1.2",
                  "Ross 2.1 ainda é tranquilo", "meu ROAS 3 na escala alta"):
            self.assertTrue(self.achar(t), t)

    def test_metrica_sem_numero_nao_conta_como_declaracao(self):
        # "o RAS diminuiu" diz que caiu, mas não declara valor nenhum —
        # não pode virar linha na tabela de números declarados
        self.assertFalse(self.achar("o RAS diminuiu bastante"))
        self.assertFalse(self.achar("a conversão caiu"))

    def test_carrega_o_timestamp(self):
        b = [{"seg": 75, "tempo": "01:15", "texto": "fez 100k por dia"}]
        n = numeros_declarados(b)
        self.assertEqual(n[0]["tempo"], "01:15")

    def test_nao_pega_numero_solto_irrelevante(self):
        self.assertFalse(self.achar("a gente tem 3 filhos e 2 cachorros"))

    def test_nao_duplica_o_mesmo_trecho(self):
        b = [{"seg": 0, "tempo": "00:00", "texto": "100k por dia, isso, 100k por dia"}]
        self.assertEqual(len(numeros_declarados(b)), 1)


class TestMencoes(unittest.TestCase):
    def test_livro(self):
        b = [{"seg": 0, "tempo": "00:00",
              "texto": 'tem um livro chamado A Meta que é muito bom'}]
        m = mencoes(b)
        self.assertTrue(any("A Meta" in x["nome"] for x in m["livros"]))

    def test_ferramenta_conhecida(self):
        b = [{"seg": 0, "tempo": "00:00", "texto": "a gente usa Meta Ads e o checkout"}]
        self.assertTrue(mencoes(b)["ferramentas"])

    def test_vazio_nao_quebra(self):
        m = mencoes([])
        self.assertEqual(m["livros"], [])
        self.assertEqual(m["ferramentas"], [])


class TestFatiar(unittest.TestCase):
    def test_divide_em_n_partes_com_faixa_de_tempo(self):
        b = [{"seg": i * 30, "tempo": "x", "texto": "t%d" % i} for i in range(100)]
        f = fatiar(b, 4)
        self.assertEqual(len(f), 4)
        self.assertEqual(sum(len(p["blocos"]) for p in f), 100)
        self.assertEqual(f[0]["inicio_seg"], 0)
        self.assertEqual(f[-1]["fim_seg"], 99 * 30)

    def test_menos_blocos_que_partes(self):
        b = [{"seg": 0, "tempo": "x", "texto": "t"}]
        f = fatiar(b, 5)
        self.assertEqual(len(f), 1)

    def test_vazio(self):
        self.assertEqual(fatiar([], 3), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
