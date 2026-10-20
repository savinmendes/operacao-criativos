# -*- coding: utf-8 -*-
import io, os, shutil, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from importar_fichas import importar, video_id


class T(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(); self.base = os.path.join(self.t, "base"); self.dl = os.path.join(self.t, "dl")
        f = os.path.join(self.base, "transcricoes", "vturb", "_fichas"); os.makedirs(f); os.makedirs(self.dl)
        io.open(os.path.join(f, "Ep #171__iHl26ShFJJ4.ficha.md"), "w", encoding="utf-8").write("[PREENCHER]")
        self.f = f

    def tearDown(self): shutil.rmtree(self.t)

    def test_id(self): self.assertEqual(video_id("X Escala 171__iHl26ShFJJ4.ficha.md"), "iHl26ShFJJ4")

    def test_importa_por_id_e_guarda_esqueleto(self):
        io.open(os.path.join(self.dl, "Ep 171__iHl26ShFJJ4.ficha.md"), "w", encoding="utf-8").write("ficha pronta")
        feitos, _ = importar(self.dl, self.base)
        self.assertEqual(len(feitos), 1)
        self.assertEqual(io.open(os.path.join(self.f, "Ep #171__iHl26ShFJJ4.ficha.md"), encoding="utf-8").read(), "ficha pronta")
        self.assertTrue(os.path.exists(os.path.join(self.f, "_esqueletos", "Ep #171__iHl26ShFJJ4.ficha.md")))

    def test_ignora_ficha_incompleta(self):
        io.open(os.path.join(self.dl, "Ep 171__iHl26ShFJJ4.ficha.md"), "w", encoding="utf-8").write("[PREENCHER]x")
        feitos, pulados = importar(self.dl, self.base)
        self.assertEqual((len(feitos), len(pulados)), (0, 1))


if __name__ == "__main__": unittest.main()
