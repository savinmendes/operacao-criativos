# -*- coding: utf-8 -*-
"""Testes dos formatos de entrega (9:16, 4:5, 1:1) do kit.

Rodar (de dentro de kit-edicao-criativos/):
  python -m unittest tests.test_formatos -v

Os testes de ponta a ponta montam um corpo sintético de ~3 s (ffmpeg testsrc2 + seno) e rodam
montar_ad.py / revisar_ad.py / preparar_corpo_traducao.py em cada formato (720). Levam ~1–2 min.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
FER = KIT / "ferramentas"
sys.path.insert(0, str(FER))
import comum as C  # noqa: E402

FORMATOS = ["9:16", "4:5", "1:1"]
ESPERADO = {
    ("9:16", 720): (720, 1280), ("9:16", 1080): (1080, 1920),
    ("4:5", 720): (720, 900), ("4:5", 1080): (1080, 1350),
    ("1:1", 720): (720, 720), ("1:1", 1080): (1080, 1080),
}
SETA_PX, SELO_W, SELO_H = 194, 760, 360      # tamanhos dos PNGs em escala 1 (overlays.seta / overlays.selo)
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


# ------------------------------------------------------------------ mapeamento
class TestMapeamento(unittest.TestCase):
    def test_dimensoes(self):
        for (f, base), wh in ESPERADO.items():
            self.assertEqual(C.dimensoes(f, base), wh, (f, base))

    def test_dimensoes_padrao(self):
        self.assertEqual(C.dimensoes(), (1080, 1920))
        self.assertEqual(C.dimensoes("4:5"), (1080, 1350))

    def test_resolucao_seis_combinacoes(self):
        for (f, base), wh in ESPERADO.items():
            self.assertEqual(C.resolucao(str(base), f), wh)
            self.assertEqual(C.resolucao(base, f), wh)

    def test_resolucao_compativel(self):
        self.assertEqual(C.resolucao(), (1080, 1920))
        self.assertEqual(C.resolucao("720"), (720, 1280))
        self.assertEqual(C.resolucao("1080"), (1080, 1920))
        self.assertEqual(C.resolucao("720", None), (720, 1280))
        self.assertEqual((C.W, C.H, C.FPS), (1080, 1920, 30))

    def test_formato_invalido(self):
        with self.assertRaises(ValueError):
            C.dimensoes("16:9")
        with self.assertRaises(ValueError):
            C.resolucao("720", "2:3")

    def test_formato_de(self):
        for (f, _), (w, h) in ESPERADO.items():
            self.assertEqual(C.formato_de(w, h), f)
        self.assertIsNone(C.formato_de(640, 360))
        self.assertIsNone(C.formato_de(1080, 1080 + 2))

    def test_checar_resolucao(self):
        for (f, _), (w, h) in ESPERADO.items():
            self.assertTrue(C.checar_resolucao(w, h)[0], (w, h))
            self.assertTrue(C.checar_resolucao(w, h, f)[0], (w, h, f))
        ok, msg = C.checar_resolucao(1080, 1920, "1:1")
        self.assertFalse(ok)
        self.assertIn("1080x1080", msg)
        self.assertFalse(C.checar_resolucao(640, 360)[0])
        self.assertFalse(C.checar_resolucao(1080, 1352)[0])

    def test_vf_vertical_formato(self):
        self.assertEqual(C.vf_vertical(), "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,"
                                          "crop=1080:1920,fps=30,setsar=1")
        self.assertIn("crop=1080:1350", C.vf_vertical(*C.dimensoes("4:5")))


# ------------------------------------------------------------------ layout
class TestLayout(unittest.TestCase):
    def test_916_igual_ao_de_hoje(self):
        L = C.layout_padrao("9:16", "drop")
        self.assertEqual((L["W"], L["H"]), (1080, 1920))
        self.assertEqual(L["legenda_y"], 1060)
        self.assertEqual((L["selo_x"], L["selo_y"], L["selo_escala"]), (160, 1225, 1.0))
        self.assertEqual((L["cta_x"], L["cta_y"], L["cta_escala"]), ([300, 610], 1630, 1.0))
        self.assertEqual((L["manchete_y"], L["faixa_y"]), (140, 150))
        self.assertEqual(C.layout_padrao("9:16", "sb")["legenda_y"], 1480)

    def test_padroes_dentro_do_quadro(self):
        for f in FORMATOS:
            for estilo, px in (("drop", 107), ("sb", 116)):
                L = C.layout_padrao(f, estilo)
                W, H = L["W"], L["H"]
                self.assertEqual((W, H), C.dimensoes(f, 1080))
                # legenda: centro com meia altura de linha dentro do quadro, no meio/baixo da tela
                self.assertGreater(L["legenda_y"] - px * 0.7, H * 0.25, (f, estilo))
                self.assertLess(L["legenda_y"] + px * 0.7, H, (f, estilo))
                # setas: abaixo da metade (o revisor procura nela) e acima da margem de baixo
                s = L["cta_escala"]
                seta = SETA_PX * s
                self.assertGreaterEqual(L["cta_y"] - 20 * s, H * 0.5, f)
                self.assertLessEqual(L["cta_y"] + seta + 20 * s, H - 0.02 * H, f)
                for x in L["cta_x"]:
                    self.assertGreaterEqual(x, 0)
                    self.assertLessEqual(x + seta, W)
                # selo inteiro dentro do quadro e sem encostar nas setas
                e = L["selo_escala"]
                sy0, sy1 = L["selo_y"], L["selo_y"] + SELO_H * e
                self.assertGreaterEqual(sy0, 0)
                self.assertLessEqual(sy1, H)
                self.assertGreaterEqual(L["selo_x"], 0)
                self.assertLessEqual(L["selo_x"] + SELO_W * e, W)
                self.assertTrue(sy1 <= L["cta_y"] - 20 * s or sy0 >= L["cta_y"] + seta + 20 * s, f)
                # selo e legenda (drop) não se cobrem
                if estilo == "drop":
                    ly0, ly1 = L["legenda_y"] - px * 0.7, L["legenda_y"] + px * 0.7
                    self.assertTrue(sy1 <= ly0 or sy0 >= ly1, (f, sy0, sy1, ly0, ly1))
                # manchete/faixa no topo
                self.assertLess(L["manchete_y"], H * 0.15)
                self.assertLess(L["faixa_y"], H * 0.15)

    def test_resolver_y(self):
        self.assertEqual(C.resolver_y({"y": 1110}, "y", 1920, 1225), 1110)
        self.assertEqual(C.resolver_y({}, "y", 1920, 1225), 1225)
        self.assertEqual(C.resolver_y(None, "y", 1920, 1225), 1225)
        self.assertEqual(C.resolver_y({"y_rel": 0.5}, "y", 1350, 7), 675)
        self.assertEqual(C.resolver_y({"y": 10, "y_rel": 0.5}, "y", 1350, 7), 10)   # absoluto vence
        with self.assertRaises(ValueError):
            C.resolver_y({"y_rel": 1.5}, "y", 1350, 7)

    def test_legenda_ass_no_quadro(self):
        import legenda as LEG
        pal = [("hola", 0.1, 0.4), ("mundo", 0.5, 0.9)]
        with tempfile.TemporaryDirectory() as d:
            for f in FORMATOS:
                W, H = C.dimensoes(f, 1080)
                L = C.layout_padrao(f, "drop")
                ass = Path(d) / "l.ass"
                LEG.gera_ass(pal, str(ass), "drop", None, L["legenda_y"], 1.0, play_res=(W, H))
                t = ass.read_text(encoding="utf-8")
                self.assertIn(f"PlayResX: {W}", t)
                self.assertIn(f"PlayResY: {H}", t)
                self.assertIn(rf"\pos({W // 2},{L['legenda_y']})", t)
            LEG.gera_ass(pal, str(ass), "drop")       # assinatura antiga: 1080x1920 e y=1060
            t = ass.read_text(encoding="utf-8")
            self.assertIn("PlayResY: 1920", t)
            self.assertIn(r"\pos(540,1060)", t)

    def test_overlays_escala(self):
        import overlays as OV
        from PIL import Image

        def tam(p):
            with Image.open(p) as im:
                return im.size
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(tam(OV.seta(str(Path(d) / "s.png"))), (SETA_PX, SETA_PX))
            self.assertEqual(tam(OV.selo(["A", "B", "C", "D"], str(Path(d) / "x.png"))), (SELO_W, SELO_H))
            w, h = tam(OV.selo(["A", "B", "C", "D"], str(Path(d) / "y.png"), escala=0.75))
            self.assertEqual((w, h), (round(SELO_W * 0.75), round(SELO_H * 0.75)))
            w, h = tam(OV.seta(str(Path(d) / "z.png"), escala=0.75))
            self.assertEqual(w, round(SETA_PX * 0.75))


# ------------------------------------------------------------------ ponta a ponta
def _py(args, cwd=KIT):
    return subprocess.run([sys.executable, *map(str, args)], cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=ENV)


def _probe(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height",
                          "-of", "json", str(p)], capture_output=True, text=True).stdout
    st = json.loads(out)["streams"]
    v = next(s for s in st if s["codec_type"] == "video")
    return (int(v["width"]), int(v["height"])), any(s["codec_type"] == "audio" for s in st)


class TestPontaAPonta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="kit_formatos_")
        cls.d = Path(cls.tmp.name)
        # corpo horizontal (testa o recorte para preencher) com fala sintética
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=1280x720:rate=30:duration=3",
                        "-f", "lavfi", "-i", "sine=frequency=330:sample_rate=48000:duration=3",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
                        str(cls.d / "corpo.mp4")], check=True)
        (cls.d / "frases.txt").write_text("Toca el botón de abajo ahora\n", encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def _receita(self, formato, nome, **extra):
        rec = {"saida": nome, "corpo": "corpo.mp4", "resolucao": "720",
               "legenda": {"fonte": "texto:frases.txt"},
               "selo": {"linhas": ["ENVÍO GRATIS", "PAGO CONTRA", "ENTREGA", "¡PAGAS AL RECIBIR!"]},
               "cta": {"inicio": 1.0}, "limite_mb": 30}
        if formato:
            rec["formato"] = formato
        rec.update(extra)
        p = self.d / (Path(nome).stem + ".json")
        p.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
        return p

    def _monta_e_revisa(self, formato, classico=False, **extra):
        nome = f"ad_{(formato or 'pad').replace(':', 'x')}{'_cl' if classico else ''}.mp4"
        rec = self._receita(formato, nome, **extra)
        r = _py([FER / "montar_ad.py", rec, *(["--classico"] if classico else [])])
        self.assertEqual(r.returncode, 0, r.stdout[-1500:] + r.stderr[-1500:])
        self.assertIn("RESULTADO: OK", r.stdout, r.stdout[-1500:])
        self.assertNotIn("sai do quadro", r.stdout)       # padrões e exemplos cabem no quadro
        saida = self.d / nome
        (w, h), audio = _probe(saida)
        self.assertEqual((w, h), C.resolucao("720", formato or "9:16"))
        self.assertTrue(audio)
        rv = _py([FER / "revisar_ad.py", saida, "--sem-whisper", "--silencio-fim", "9",
                  *(["--formato", formato] if formato else [])])
        txt = rv.stdout
        self.assertNotIn("PROBLEMA: resolução", txt, txt[-2000:])
        self.assertIn("no último quadro: sim", txt, txt[-2000:])        # setas achadas no quadro novo
        self.assertNotIn("setas de CTA em cima", txt)
        self.assertEqual(rv.returncode, 0, txt[-2000:])
        return saida

    def test_916_padrao(self):
        self._monta_e_revisa(None)

    def test_916(self):
        self._monta_e_revisa("9:16")

    def test_4x5(self):
        self._monta_e_revisa("4:5")

    def test_1x1(self):
        self._monta_e_revisa("1:1")

    def test_1x1_y_rel(self):
        self._monta_e_revisa("1:1", selo={"linhas": ["A", "PAGO", "CONTRA", "B"], "y_rel": 0.15},
                             cta={"inicio": 1.0, "y_rel": 0.78})

    def test_1x1_escala_1_cabe(self):
        # selo/setas em tamanho cheio no 1:1 sem y: o padrão sobe para continuar dentro do quadro
        self._monta_e_revisa("1:1", selo={"linhas": ["A", "PAGO", "CONTRA", "B"], "escala": 1},
                             cta={"inicio": 1.0, "escala": 1})

    def test_4x5_classico(self):
        self._monta_e_revisa("4:5", classico=True)

    def test_revisar_formato_errado(self):
        saida = self._monta_e_revisa("1:1")
        rv = _py([FER / "revisar_ad.py", saida, "--sem-whisper", "--silencio-fim", "9", "--formato", "9:16"])
        self.assertIn("PROBLEMA: resolução", rv.stdout)
        self.assertEqual(rv.returncode, 1)

    def test_finalizar_so_revisar(self):
        saida = self._monta_e_revisa("4:5")
        r = _py([FER / "finalizar.py", saida, "--so-revisar"])
        self.assertIn("RESULTADO: OK", r.stdout, r.stdout + r.stderr)

    def test_preparar_corpo_traducao_formatos(self):
        # narração sintética + alinhamento por caractere (formato do ElevenLabs)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                        "sine=frequency=440:sample_rate=44100:duration=2", str(self.d / "narr.mp3")], check=True)
        txt = "Hola mundo."
        n = len(txt)
        al = {"characters": list(txt),
              "character_start_times_seconds": [round(1.8 * i / n, 3) for i in range(n)],
              "character_end_times_seconds": [round(1.8 * (i + 1) / n, 3) for i in range(n)]}
        (self.d / "narr.alinhamento.json").write_text(json.dumps(al), encoding="utf-8")
        for f in ("4:5", "1:1"):
            W, H = C.resolucao("720", f)
            prep = {"video": "corpo.mp4", "resolucao": "720", "formato": f, "fundo": None, "narr": "narr.mp3",
                    "faixas": [{"y_rel": [0.70, 0.78]}],
                    "titulos": [{"linhas": ["Título nuevo"], "px": 30, "cy_rel": 0.12, "de": 0, "ate": 1}],
                    "aviso": {"linhas": ["Solo con fines demostrativos."], "px": 19},
                    "saida": f"corpo_{f.replace(':', 'x')}.mp4"}
            p = self.d / f"prep_{f.replace(':', 'x')}.json"
            p.write_text(json.dumps(prep, ensure_ascii=False), encoding="utf-8")
            r = _py([FER / "preparar_corpo_traducao.py", p])
            self.assertEqual(r.returncode, 0, r.stdout[-1500:] + r.stderr[-1500:])
            (w, h), audio = _probe(self.d / prep["saida"])
            self.assertEqual((w, h), (W, H))
            self.assertTrue(audio)


if __name__ == "__main__":
    unittest.main()
