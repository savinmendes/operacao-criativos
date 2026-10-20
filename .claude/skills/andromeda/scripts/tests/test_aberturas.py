"""Testes do comparador de aberturas. Rodar dentro de scripts/: python -m unittest discover -s tests -v"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import aberturas  # noqa: E402


def _video(caminho, fonte, dur=3):
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"{fonte}=s=360x640:d={dur}:r=24",
         "-pix_fmt", "yuv420p", caminho],
        check=True,
    )


class TestAberturas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp()
        cls.a = os.path.join(cls.dir, "C01_a.mp4")
        cls.b = os.path.join(cls.dir, "C01_b.mp4")  # mesma abertura que a
        cls.c = os.path.join(cls.dir, "C02_c.mp4")  # abertura diferente
        _video(cls.a, "testsrc")
        _video(cls.b, "testsrc")
        _video(cls.c, "smptebars")

    def test_assinatura_tem_64_bits_por_quadro(self):
        sig = aberturas.assinatura(self.a, tempos=(0.2, 1.0))
        self.assertEqual(len(sig), 2)
        self.assertTrue(all(len(h) == 64 for h in sig))

    def test_videos_iguais_tem_similaridade_alta(self):
        s = aberturas.similaridade(aberturas.assinatura(self.a), aberturas.assinatura(self.b))
        self.assertGreaterEqual(s, 0.95)

    def test_videos_diferentes_tem_similaridade_baixa(self):
        s = aberturas.similaridade(aberturas.assinatura(self.a), aberturas.assinatura(self.c))
        self.assertLess(s, 0.75)

    def test_comparar_lote_marca_so_o_par_parecido(self):
        res = aberturas.comparar([self.a, self.b, self.c], limiar=0.85)
        pares = {(p["a"], p["b"]) for p in res["parecidos"]}
        self.assertEqual(pares, {("C01_a.mp4", "C01_b.mp4")})
        self.assertEqual(len(res["matriz"]), 3)

    def test_video_curto_nao_quebra(self):
        curto = os.path.join(self.dir, "curto.mp4")
        _video(curto, "testsrc", dur=0.5)
        sig = aberturas.assinatura(curto, tempos=(0.2, 1.0, 2.0))
        self.assertEqual(len(sig), 3)

    def test_cli_gera_json_e_grade(self):
        saida = os.path.join(self.dir, "out")
        r = subprocess.run(
            [sys.executable, aberturas.__file__, self.dir, "--saida", saida, "--limiar", "0.85"],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(r.returncode, 1, r.stderr)  # 1 = achou par parecido
        with open(os.path.join(saida, "aberturas.json"), encoding="utf-8") as f:
            dados = json.load(f)
        self.assertTrue(dados["parecidos"])
        self.assertTrue(os.path.exists(os.path.join(saida, "aberturas_grade.jpg")))


if __name__ == "__main__":
    unittest.main()
