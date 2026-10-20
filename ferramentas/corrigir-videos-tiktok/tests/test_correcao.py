# -*- coding: utf-8 -*-
"""Testes da logica de diagnostico e plano.

Os casos nao sao inventados: as resolucoes e bitrates abaixo foram medidos nos
441 videos da pasta do usuario. 360x640 e o reprovado mais comum (29 videos),
576x1024 e o caso traicoeiro que passa na resolucao e cai no bitrate, e
720x900 e 286x242 sao os formatos estranhos que apareceram no acervo.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.correcao import (Medida, avaliar, escala_alvo, bitrate_alvo, planejar,
                          comando_ffmpeg, perfil, _par_acima)

TT = perfil("tiktok")


class TestAvaliar(unittest.TestCase):
    def test_vertical_grande_passa(self):
        self.assertEqual(avaliar(Medida(1080, 1920, 2500), TT), [])

    def test_720x1280_passa(self):
        self.assertEqual(avaliar(Medida(720, 1280, 821), TT), [])

    def test_no_limite_exato_passa(self):
        self.assertEqual(avaliar(Medida(540, 960, 350.0), TT), [])

    def test_360x640_reprova_resolucao(self):
        self.assertIn("resolucao", avaliar(Medida(360, 640, 1200), TT))

    def test_bitrate_baixo_reprova(self):
        self.assertEqual(avaliar(Medida(1080, 1920, 271), TT), ["bitrate"])

    def test_576x1024_passa_resolucao_e_cai_no_bitrate(self):
        # caso real do acervo: resolucao suficiente, bitrate 271 kbps
        p = avaliar(Medida(576, 1024, 271), TT)
        self.assertEqual(p, ["bitrate"])

    def test_pode_reprovar_nos_dois(self):
        self.assertEqual(sorted(avaliar(Medida(360, 480, 184), TT)),
                         ["bitrate", "resolucao"])

    def test_deitado_nao_e_reprovado_por_estar_deitado(self):
        # 1024x576: lado curto 576 >= 540, lado longo 1024 >= 960
        self.assertEqual(avaliar(Medida(1024, 576, 1500), TT), [])

    def test_720x900_reprova_porque_o_lado_longo_e_curto_demais(self):
        self.assertEqual(avaliar(Medida(720, 900, 1500), TT), ["resolucao"])

    def test_bitrate_desconhecido_nao_inventa_reprovacao(self):
        self.assertEqual(avaliar(Medida(1080, 1920, None), TT), [])


class TestEscala(unittest.TestCase):
    def test_nao_reduz_quem_ja_e_grande(self):
        self.assertIsNone(escala_alvo(Medida(1080, 1920), TT))

    def test_360x640_vira_540x960(self):
        self.assertEqual(escala_alvo(Medida(360, 640), TT), (540, 960))

    def test_mantem_proporcao(self):
        larg, alt = escala_alvo(Medida(360, 480), TT)
        orig = 360 / 480.0
        self.assertAlmostEqual(larg / float(alt), orig, places=2)

    def test_resultado_sempre_par(self):
        for w, h in [(360, 640), (360, 480), (270, 360), (286, 242), (720, 900),
                     (576, 720), (333, 777)]:
            larg, alt = escala_alvo(Medida(w, h), TT)
            self.assertEqual(larg % 2, 0, "%dx%d -> largura impar" % (w, h))
            self.assertEqual(alt % 2, 0, "%dx%d -> altura impar" % (w, h))

    def test_resultado_sempre_cumpre_o_minimo(self):
        for w, h in [(360, 640), (360, 480), (270, 360), (286, 242), (720, 900),
                     (576, 720), (100, 100), (1, 2)]:
            larg, alt = escala_alvo(Medida(w, h), TT)
            self.assertGreaterEqual(min(larg, alt), 540, "%dx%d" % (w, h))
            self.assertGreaterEqual(max(larg, alt), 960, "%dx%d" % (w, h))

    def test_deitado_tambem_sobe_certo(self):
        larg, alt = escala_alvo(Medida(640, 360), TT)
        self.assertEqual((larg, alt), (960, 540))

    def test_par_acima(self):
        self.assertEqual(_par_acima(539.1), 540)
        self.assertEqual(_par_acima(540), 540)
        self.assertEqual(_par_acima(540.1), 542)


class TestBitrate(unittest.TestCase):
    def test_respeita_o_piso(self):
        self.assertGreaterEqual(bitrate_alvo(540, 960, 30), 600)

    def test_fica_bem_acima_do_minimo_da_plataforma(self):
        self.assertGreater(bitrate_alvo(540, 960, 30), 350 * 1.5)

    def test_quadro_maior_pede_mais(self):
        self.assertGreater(bitrate_alvo(1080, 1920, 30),
                           bitrate_alvo(540, 960, 30))

    def test_nunca_abaixa_o_que_ja_existia(self):
        # video de 1080p a 4000 kbps nao pode sair com menos
        self.assertGreaterEqual(bitrate_alvo(1080, 1920, 30, kbps_atual=4000), 4000)

    def test_fps_ausente_nao_quebra(self):
        self.assertGreater(bitrate_alvo(540, 960, None), 0)


class TestPlanejar(unittest.TestCase):
    def test_video_bom_nao_gera_trabalho(self):
        pl = planejar(Medida(1080, 1920, 2500, 30), TT)
        self.assertFalse(pl.precisa)
        self.assertIsNone(pl.escala)

    def test_so_bitrate_nao_mexe_na_resolucao(self):
        pl = planejar(Medida(576, 1024, 271, 30), TT)
        self.assertTrue(pl.precisa)
        self.assertIsNone(pl.escala)
        self.assertGreater(pl.kbps, 350)

    def test_so_resolucao_ainda_assim_define_bitrate(self):
        # reencodar exige escolher um bitrate de qualquer forma
        pl = planejar(Medida(360, 640, 1200, 30), TT)
        self.assertEqual(pl.escala, (540, 960))
        self.assertGreaterEqual(pl.kbps, 1200)

    def test_audio_aac_e_copiado(self):
        pl = planejar(Medida(360, 640, 200, 30, codec_audio="aac"), TT)
        self.assertTrue(pl.copiar_audio)

    def test_audio_de_outro_formato_e_reencodado(self):
        pl = planejar(Medida(360, 640, 200, 30, codec_audio="opus"), TT)
        self.assertFalse(pl.copiar_audio)


class TestComando(unittest.TestCase):
    def _cmd(self, m):
        return comando_ffmpeg("e.mp4", "s.mp4", planejar(m, TT))

    def test_recusa_sobrescrever_a_entrada(self):
        pl = planejar(Medida(360, 640, 200, 30), TT)
        with self.assertRaises(ValueError):
            comando_ffmpeg("v.mp4", "v.mp4", pl)

    def test_fixa_o_bitrate_nos_tres_parametros(self):
        # e isso que garante o piso; com CRF o ffmpeg cairia abaixo
        c = self._cmd(Medida(360, 640, 200, 30))
        for flag in ("-b:v", "-minrate", "-maxrate"):
            self.assertIn(flag, c)
        i = c.index("-b:v")
        self.assertEqual(c[c.index("-minrate") + 1], c[i + 1])
        self.assertEqual(c[c.index("-maxrate") + 1], c[i + 1])

    def test_escala_entra_quando_precisa(self):
        c = self._cmd(Medida(360, 640, 1200, 30))
        self.assertIn("-vf", c)
        self.assertIn("scale=540:960:flags=lanczos", c)

    def test_sem_escala_quando_a_resolucao_ja_serve(self):
        c = self._cmd(Medida(576, 1024, 271, 30))
        self.assertNotIn("-vf", c)

    def test_sempre_yuv420p(self):
        # sem isso o arquivo nao abre em parte dos players e gerenciadores
        c = self._cmd(Medida(360, 640, 200, 30))
        self.assertEqual(c[c.index("-pix_fmt") + 1], "yuv420p")

    def test_faststart(self):
        c = self._cmd(Medida(360, 640, 200, 30))
        self.assertIn("+faststart", c)


class TestOResultadoPassaNaPropriaRegra(unittest.TestCase):
    """O teste que importa: o plano produz um video que seria aprovado?"""

    def test_todo_reprovado_vira_aprovado(self):
        casos = [(360, 640, 193), (360, 480, 184), (270, 360, 500),
                 (286, 242, 241), (720, 900, 1500), (576, 720, 800),
                 (576, 1024, 271), (1080, 1920, 150)]
        for w, h, k in casos:
            m = Medida(w, h, k, 30)
            pl = planejar(m, TT)
            self.assertTrue(pl.precisa, "%dx%d@%s deveria precisar" % (w, h, k))
            nw, nh = pl.escala if pl.escala else (w, h)
            depois = Medida(nw, nh, pl.kbps, 30)
            self.assertEqual(avaliar(depois, TT), [],
                             "%dx%d@%s continuou reprovado" % (w, h, k))


if __name__ == "__main__":
    unittest.main(verbosity=2)
