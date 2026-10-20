# -*- coding: utf-8 -*-
"""Testes do checar_lipsync.py.

Rodar (de dentro de kit-edicao-criativos/):
  python -m unittest tests.test_checar_lipsync -v

Casos reais (cópias; nunca rode em cima da pasta de trabalho de um AD em produção):
  LIPSYNC_CASOS/ad11  lote HeyGen do AD 11 (aprovado pela pessoa): 4 saídas em que a boca continuou o português
                      (ruins) e 6 com lipsync correto (bons).
  LIPSYNC_CASOS/ad01  AD 01, plano com DOIS rostos (mulher falando, Jesus calado atrás): a boca foi refeita em todos
                      os trechos, mas o revisor independente reprovou 9 de 13 (boca abre nas pausas do espanhol).
  LIPSYNC_CASOS/ad13  AD 13: trechos bons (revisor: "no nível do AD 11").
Se a pasta não existir, os testes de casos reais são pulados.
"""
from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

import numpy as np

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT / "ferramentas"))
import checar_lipsync as CL  # noqa: E402

BASE = Path(os.environ.get(
    "LIPSYNC_CASOS",
    r"C:\Users\PICHAU\AppData\Local\Temp\claude\c--Users-PICHAU-Downloads-Produtividade-com-ia"
    r"\fefd88e1-1970-4576-a429-cf0c1248f170\scratchpad\lipsync_casos"))
PASTA = BASE / "ad11"
P01 = BASE / "ad01"
P13 = BASE / "ad13"

# (saída, áudio novo, original, áudio original)  -- None = extrai do original; False = não usar
RUINS = {
    "ls_menina": ("ls_menina.mp4", "es_menina.mp3", "pt_menina.mp4", None),
    "ls_mulher_1": ("ls_mulher_1.mp4", "es_mulher_1.mp3", "pt_mulher_1.mp4", None),
    # não há pt_mulher_2: o original é a entrada do HeyGen (boca em pt, áudio es embutido) -> sem áudio original
    "ls_mulher_2": ("ls_mulher_2.mp4", None, "v_mulher_2.mp4", False),
    "ls_m3a": ("ls_m3a.mp4", "es_m3a.mp3", "pt_m3a.mp4", None),
}
# ls_m3b veio rotulado como ruim, mas as medições dizem que o HeyGen sincronizou: a boca mudou em 99% dos quadros
# em relação ao pt_m3b (corr. da abertura 0,12) e é quase igual à do v2_m3b, que é bom (corr. 0,92; dif. de
# pixels 2,4 contra 7,8 em relação ao original). Fica como caso à parte, esperado não reprovar.
CONTESTADOS = {
    "ls_m3b": ("ls_m3b.mp4", "es_m3b.mp3", "pt_m3b.mp4", None),
}
BONS = {
    "v2_menina": ("v2_menina.mp4", "es_menina.mp3", "pt_menina.mp4", None),
    "ls_teste_m1": ("ls_teste_m1.mp4", "es_mulher_1.mp3", "pt_mulher_1.mp4", None),
    "v2_m2a": ("v2_m2a.mp4", "es_m2a.mp3", "pt_m2a.mp4", None),
    "v2_m2b": ("v2_m2b.mp4", "es_m2b.mp3", "pt_m2b.mp4", None),
    "v2_m3a": ("v2_m3a.mp4", "es_m3a.mp3", "pt_m3a.mp4", None),
    "v2_m3b": ("v2_m3b.mp4", "es_m3b.mp3", "pt_m3b.mp4", None),
}

# AD 01 (REVISAO-01-13.md, tabela "Lipsync, trecho por trecho")
AD01_RUINS = ["s01", "s02", "s05", "s06", "s07", "s08", "s09", "s11", "s12"]
AD01_BONS = ["s03", "s04", "s10", "s13"]
# AD 13: todos aprovados pelo revisor, exceto w05 ("duvidoso": abre numa pausa de 0,5 s)
AD13_BONS = ["j1", "w01", "w02", "w03", "w04", "w06", "w07", "w08", "w09", "w10", "w11", "w12", "w13"]
# rosto da mulher no AD 01 (recorte usado pelo revisor: ffmpeg crop=400:440:320:280)
AD01_ROSTO_MULHER = (320, 280, 400, 440)


def _existe(casos, pasta=None) -> bool:
    pasta = pasta or PASTA
    return pasta.is_dir() and all((pasta / c[0]).exists() and (pasta / c[2]).exists()
                                  and (c[1] is None or (pasta / c[1]).exists()) for c in casos.values())


def _caso_ad(pasta, nomes):
    return {n: (f"ls_{n}.mp4", f"es_{n}.mp3", f"pt_{n}.mp4", None) for n in nomes}


def _rodar(caso, pasta=None, **kw):
    pasta = pasta or PASTA
    s, an, o, ao = caso
    return CL.checar(pasta / s, audio_novo=pasta / an if an else None, original=pasta / o,
                     audio_original=ao, **kw)


class TestSinais(unittest.TestCase):
    """Partes puras (sem vídeo)."""

    def test_corr_lag_acha_atraso(self):
        rng = np.random.default_rng(1)
        a = rng.standard_normal(300)
        b = np.roll(a, 4)                      # b atrasado 4 quadros
        c, lag = CL.corr_lag(a, b, max_lag=6)
        self.assertGreater(c, 0.95)
        self.assertEqual(abs(lag), 4)

    def test_corr_lag_respeita_tolerancia(self):
        rng = np.random.default_rng(2)
        a = rng.standard_normal(300)
        b = np.roll(a, 15)                     # fora da janela de ±6
        c, _ = CL.corr_lag(a, b, max_lag=6)
        self.assertLess(c, 0.3)

    def test_corr_lag_ignora_nan(self):
        a = np.sin(np.linspace(0, 20, 200))
        b = a.copy()
        a[10:20] = np.nan
        c, lag = CL.corr_lag(a, b, max_lag=3)
        self.assertGreater(c, 0.99)
        self.assertEqual(lag, 0)

    def test_envelope_tamanho_e_fala(self):
        sr, fps = 16000, 30
        x = np.zeros(sr * 2, dtype=np.float32)
        x[sr // 2: sr] = 0.5 * np.sin(np.arange(sr // 2) * 2 * np.pi * 200 / sr)   # fala em 0,5-1,0 s
        env = CL.envelope(x, sr, fps, n=60)
        self.assertEqual(len(env), 60)
        self.assertGreater(env[22], env[5] + 1)   # mais energia onde há som
        self.assertGreater(env[22], env[45] + 1)

    def test_veredito_boca_igual_reprova(self):
        st, motivo = CL.veredito({"mudou": 0.05, "indice_pausa": 0.3, "corr_novo": 0.6, "corr_original": 0.2})
        self.assertEqual(st, "REPROVADO")
        self.assertIn("boca", motivo.lower())

    def test_veredito_boca_abre_igual_ao_original_reprova(self):
        st, _ = CL.veredito({"mudou": 0.9, "corr_boca_original": 0.95, "indice_pausa": 0.3, "corr_novo": 0.5})
        self.assertEqual(st, "REPROVADO")

    def test_veredito_pausa_alta_reprova_mesmo_com_boca_mudada(self):
        # AD 01: a boca mudou (foi refeita), mas abre nas pausas do áudio novo
        st, motivo = CL.veredito({"mudou": 0.98, "indice_pausa": 0.86, "corr_novo": 0.30, "corr_original": 0.1})
        self.assertEqual(st, "REPROVADO")
        self.assertIn("pausa", motivo.lower())

    def test_veredito_pixels_iguais_mas_abertura_diferente_e_aviso(self):
        # AD 13 j1 (barba): dif. de pixels na boca no nível do ruído, mas a abertura não segue a do original
        st, motivo = CL.veredito({"mudou": 0.19, "corr_boca_original": -0.08, "indice_pausa": 0.5, "n_pausa": 40,
                                  "corr_novo": 0.3})
        self.assertEqual(st, "AVISO")
        self.assertIn("confira", motivo.lower())

    def test_veredito_poucas_pausas_tolera_mais(self):
        # < 20 quadros de pausa: amostra pequena, só reprova acima de 0,90
        st, _ = CL.veredito({"mudou": 0.9, "indice_pausa": 0.79, "n_pausa": 14, "corr_novo": 0.2})
        self.assertEqual(st, "AVISO")
        st, _ = CL.veredito({"mudou": 0.9, "indice_pausa": 1.15, "n_pausa": 13, "corr_novo": 0.04})
        self.assertEqual(st, "REPROVADO")
        st, _ = CL.veredito({"mudou": 0.9, "indice_pausa": 0.79, "n_pausa": 29, "corr_novo": 0.1})
        self.assertEqual(st, "REPROVADO")

    def test_veredito_sem_pausa_margem_original(self):
        # AD 01 s08 (ruim): corr. novo 0,15 x original 0,30; ls_teste_m1 (bom): 0,22 x 0,30
        st, _ = CL.veredito({"mudou": 0.99, "indice_pausa": None, "corr_novo": 0.15, "corr_original": 0.30})
        self.assertEqual(st, "REPROVADO")
        st, _ = CL.veredito({"mudou": 0.98, "indice_pausa": None, "corr_novo": 0.22, "corr_original": 0.30})
        self.assertEqual(st, "AVISO")

    def test_veredito_pausa_intermediaria_e_aviso(self):
        st, _ = CL.veredito({"mudou": 0.9, "indice_pausa": 0.70, "corr_novo": 0.3, "corr_original": 0.1})
        self.assertEqual(st, "AVISO")

    def test_veredito_pausa_baixa_aprova(self):
        st, _ = CL.veredito({"mudou": 0.9, "indice_pausa": 0.38, "corr_novo": 0.05, "corr_original": 0.1})
        self.assertEqual(st, "APROVADO")

    def test_veredito_sem_pausa_usa_correlacao(self):
        st, _ = CL.veredito({"mudou": 0.9, "indice_pausa": None, "corr_novo": 0.02, "corr_original": None})
        self.assertEqual(st, "REPROVADO")
        st, motivo = CL.veredito({"mudou": 0.9, "indice_pausa": None, "corr_novo": 0.5, "corr_original": 0.1})
        self.assertEqual(st, "AVISO")             # sem pausa o teste principal não roda: confira a olho
        self.assertIn("pausa", motivo.lower())

    def test_veredito_sem_pausa_mais_parecido_com_original_reprova(self):
        st, motivo = CL.veredito({"mudou": 0.9, "indice_pausa": None, "corr_novo": 0.35, "corr_original": 0.55})
        self.assertEqual(st, "REPROVADO")
        self.assertIn("original", motivo.lower())

    def test_veredito_sem_original_usa_so_audio(self):
        st, _ = CL.veredito({"mudou": None, "indice_pausa": 0.4, "corr_novo": 0.5, "corr_original": None})
        self.assertEqual(st, "APROVADO")

    def test_ler_especificacao_lipsync(self):
        e = CL.ler_especificacao(r"C:\a\s1.mp4:C:\a\es1.mp3:C:\a\pt1.mp4, s2.mp4::pt2.mp4 ,s3.mp4")
        self.assertEqual(e, [(r"C:\a\s1.mp4", r"C:\a\es1.mp3", r"C:\a\pt1.mp4", None),
                             ("s2.mp4", None, "pt2.mp4", None),
                             ("s3.mp4", None, None, None)])

    def test_ler_especificacao_com_rosto(self):
        e = CL.ler_especificacao(r"C:\a\s1.mp4:C:\a\es1.mp3:C:\a\pt1.mp4:320;280;400;440, s2.mp4")
        self.assertEqual(e, [(r"C:\a\s1.mp4", r"C:\a\es1.mp3", r"C:\a\pt1.mp4", "320;280;400;440"),
                             ("s2.mp4", None, None, None)])


class TestPausa(unittest.TestCase):
    """Índice de pausa: abertura média da boca nas pausas da voz nova / abertura média na fala."""

    def test_mascara_fala_relativa_ao_pico(self):
        env = np.array([-20.0, -25, -55, -60, -21])
        np.testing.assert_array_equal(CL.mascara_fala(env, faixa_db=30), [True, True, False, False, True])

    def test_mascara_pausas_so_corridas_longas_e_sem_bordas(self):
        fala = np.array([True] * 5 + [False] * 10 + [True] * 5 + [False] * 4 + [True] * 3)
        p = CL.mascara_pausas(fala, min_q=8, borda=2)
        self.assertEqual(int(p.sum()), 6)            # 10 quadros de pausa menos 2 de cada borda
        self.assertTrue(p[7:13].all())
        self.assertFalse(p[20:24].any())             # pausa de 4 quadros é curta demais

    def _sinais(self, boca_fecha: bool, seed=3):
        rng = np.random.default_rng(seed)
        n = 300
        fala = np.ones(n, bool)
        for a in (40, 120, 200, 260):
            fala[a:a + 15] = False
        env = np.where(fala, -20.0, -70.0) + rng.normal(0, 1, n)
        ab = 0.06 + 0.03 * rng.random(n)
        if boca_fecha:
            ab[~fala] = 0.01 * rng.random(int((~fala).sum()))
        return ab, env

    def test_indice_baixo_quando_boca_fecha_nas_pausas(self):
        ab, env = self._sinais(True)
        idx, nq = CL.indice_pausa(ab, env)
        self.assertLess(idx, 0.3)
        self.assertGreater(nq, 30)

    def test_indice_perto_de_1_quando_boca_ignora_as_pausas(self):
        ab, env = self._sinais(False)
        idx, _ = CL.indice_pausa(ab, env)
        self.assertGreater(idx, 0.85)

    def test_indice_none_sem_pausa_suficiente(self):
        ab = np.full(100, 0.05)
        env = np.full(100, -20.0)
        idx, nq = CL.indice_pausa(ab, env)
        self.assertIsNone(idx)
        self.assertEqual(nq, 0)

    def test_indice_ignora_nan(self):
        ab, env = self._sinais(True)
        ab[::7] = np.nan
        idx, _ = CL.indice_pausa(ab, env)
        self.assertLess(idx, 0.3)

    def test_classificar_pausa_limiares(self):
        self.assertEqual(CL.classificar_pausa(0.38), "APROVADO")
        self.assertEqual(CL.classificar_pausa(0.60), "APROVADO")
        self.assertEqual(CL.classificar_pausa(0.70), "AVISO")
        self.assertEqual(CL.classificar_pausa(0.75), "AVISO")
        self.assertEqual(CL.classificar_pausa(0.86), "REPROVADO")

    def test_indice_agregado_soma_os_trechos(self):
        # o índice do AD inteiro junta os quadros de todos os trechos (como o revisor fez)
        a = {"soma_ab_pausa": 1.0, "n_pausa": 20, "soma_ab_fala": 10.0, "n_fala": 100}
        b = {"soma_ab_pausa": 3.0, "n_pausa": 20, "soma_ab_fala": 10.0, "n_fala": 100}
        self.assertAlmostEqual(CL.indice_agregado([a, b]), (4.0 / 40) / (20.0 / 200))
        self.assertIsNone(CL.indice_agregado([{"n_pausa": 0, "soma_ab_pausa": 0, "n_fala": 5, "soma_ab_fala": 1}]))


class TestRosto(unittest.TestCase):
    def test_ler_rosto(self):
        self.assertEqual(CL.ler_rosto("320,280,400,440"), (320, 280, 400, 440))
        self.assertEqual(CL.ler_rosto("320;280;400;440"), (320, 280, 400, 440))
        for ruim in ("1,2,3", "a,b,c,d", "0,0,0,10", "-1,0,10,10"):
            with self.assertRaises(ValueError):
                CL.ler_rosto(ruim)

    def test_agrupar_rostos_junta_o_mesmo_rosto_em_quadros_diferentes(self):
        # 3 quadros, 2 rostos (um grande atrás, um menor na frente), caixas (x, y, w, h)
        dets = [[(100, 100, 300, 300), (450, 500, 200, 200)],
                [(105, 98, 300, 300), (455, 505, 200, 200)],
                [(110, 102, 300, 300)]]
        g = CL.agrupar_rostos(dets)
        self.assertEqual(len(g), 2)
        self.assertEqual(sorted(c["n"] for c in g), [2, 3])

    def test_escolher_rosto_com_original_usa_quem_mudou(self):
        cands = [{"mudanca": 1.1, "corr_audio": 0.30, "atividade": 0.02},   # calado, nada mudou
                 {"mudanca": 8.0, "corr_audio": -0.10, "atividade": 0.03}]  # quem fala (lipsync ruim)
        self.assertEqual(CL.escolher_rosto(cands), 1)

    def test_escolher_rosto_sem_mudanca_usa_audio(self):
        cands = [{"mudanca": None, "corr_audio": 0.05, "atividade": 0.004},
                 {"mudanca": None, "corr_audio": 0.35, "atividade": 0.030}]
        self.assertEqual(CL.escolher_rosto(cands), 1)
        # boca devolvida igual nos dois (nenhum mudou): decide pelo áudio também
        cands = [{"mudanca": 1.0, "corr_audio": 0.40, "atividade": 0.03},
                 {"mudanca": 1.2, "corr_audio": 0.02, "atividade": 0.01}]
        self.assertEqual(CL.escolher_rosto(cands), 0)


@unittest.skipUnless(_existe(RUINS), f"casos reais não encontrados em {PASTA}")
class TestCasosRuins(unittest.TestCase):
    def test_ruins_reprovam(self):
        for nome, caso in RUINS.items():
            with self.subTest(nome):
                r = _rodar(caso)
                self.assertEqual(r["status"], "REPROVADO", f"{nome}: {r}")


@unittest.skipUnless(_existe(BONS), f"casos reais não encontrados em {PASTA}")
class TestCasosBons(unittest.TestCase):
    def test_bons_nao_reprovam(self):
        for nome, caso in BONS.items():
            with self.subTest(nome):
                r = _rodar(caso)
                self.assertTrue(r["aprovado"], f"{nome}: {r}")
                self.assertNotEqual(r["status"], "REPROVADO")


@unittest.skipUnless(_existe(CONTESTADOS) and (PASTA / "v2_m3b.mp4").exists(),
                     f"casos reais não encontrados em {PASTA}")
class TestCasoContestado(unittest.TestCase):
    def test_ls_m3b_sincronizou(self):
        r = _rodar(CONTESTADOS["ls_m3b"])
        self.assertTrue(r["aprovado"], r)
        # a boca do ls_m3b é praticamente a mesma do v2_m3b (bom)
        r2 = CL.checar(PASTA / "ls_m3b.mp4", audio_novo=PASTA / "es_m3b.mp3", original=PASTA / "v2_m3b.mp4",
                       audio_original=False)
        self.assertGreater(r2["corr_boca_original"], 0.8)


@unittest.skipUnless(_existe(_caso_ad(P01, AD01_RUINS + AD01_BONS), P01), f"casos do AD 01 não encontrados em {P01}")
class TestAD01DoisRostos(unittest.TestCase):
    """Plano com dois rostos: o maior é o Jesus calado. A ferramenta tem de medir a mulher que fala."""

    @classmethod
    def setUpClass(cls):
        cls.r = {n: _rodar(c, P01) for n, c in _caso_ad(P01, AD01_RUINS + AD01_BONS).items()}

    def test_escolhe_o_rosto_de_quem_fala(self):
        x, y, w, h = AD01_ROSTO_MULHER
        for n, r in self.r.items():
            with self.subTest(n):
                rx, ry, rw, rh = r["rosto_caixa"]
                cx, cy = rx + rw / 2, ry + rh / 2
                self.assertTrue(x <= cx <= x + w and y <= cy <= y + h, f"{n}: {r['rosto_caixa']}")

    def test_boca_mudou_em_todos(self):
        for n, r in self.r.items():
            with self.subTest(n):
                self.assertGreater(r["mudou"], 0.8, f"{n}: {r}")

    def test_ruins_reprovam(self):
        for n in AD01_RUINS:
            with self.subTest(n):
                self.assertEqual(self.r[n]["status"], "REPROVADO", f"{n}: {self.r[n]}")

    def test_bons_nao_reprovam(self):
        for n in AD01_BONS:
            with self.subTest(n):
                self.assertNotEqual(self.r[n]["status"], "REPROVADO", f"{n}: {self.r[n]}")

    def test_ad_inteiro_reprova_pelo_indice_agregado(self):
        idx = CL.indice_agregado(list(self.r.values()))
        self.assertEqual(CL.classificar_pausa(idx), "REPROVADO", idx)

    def test_rosto_forcado(self):
        r = _rodar(_caso_ad(P01, ["s05"])["s05"], P01, rosto=AD01_ROSTO_MULHER)
        self.assertEqual(r["rosto_caixa"], AD01_ROSTO_MULHER)
        self.assertEqual(r["status"], "REPROVADO", r)


@unittest.skipUnless(_existe(_caso_ad(P13, AD13_BONS), P13), f"casos do AD 13 não encontrados em {P13}")
class TestAD13(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = {n: _rodar(c, P13) for n, c in _caso_ad(P13, AD13_BONS).items()}

    def test_ad_inteiro_passa_pelo_indice_agregado(self):
        idx = CL.indice_agregado(list(self.r.values()))
        self.assertNotEqual(CL.classificar_pausa(idx), "REPROVADO", idx)

    def test_maioria_dos_trechos_nao_reprova(self):
        # índice por trecho é ruidoso (poucas pausas, corte de câmera): exige >= 75% dos bons sem reprovação
        ok = [n for n, r in self.r.items() if r["status"] != "REPROVADO"]
        self.assertGreaterEqual(len(ok), 0.75 * len(self.r), {n: (r["status"], r.get("indice_pausa"))
                                                              for n, r in self.r.items()})


@unittest.skipUnless(_existe(RUINS), f"casos reais não encontrados em {PASTA}")
class TestSemOriginal(unittest.TestCase):
    """Sem o original só sobram os testes de áudio: pegam os ruins grosseiros e não reprovam nenhum bom."""

    def test_bons_nao_reprovam_sem_original(self):
        for nome, (s, an, _, _) in BONS.items():
            with self.subTest(nome):
                r = CL.checar(PASTA / s, audio_novo=PASTA / an if an else None)
                self.assertTrue(r["aprovado"], f"{nome}: {r}")

    def test_ruins_grosseiros_reprovam_sem_original(self):
        for nome in ("ls_menina", "ls_mulher_2"):
            with self.subTest(nome):
                s, an, _, _ = RUINS[nome]
                r = CL.checar(PASTA / s, audio_novo=PASTA / an if an else None)
                self.assertFalse(r["aprovado"], f"{nome}: {r}")


@unittest.skipUnless(_existe(RUINS) and _existe(BONS), f"casos reais não encontrados em {PASTA}")
class TestCLI(unittest.TestCase):
    def _cli(self, *args):
        return subprocess.run([sys.executable, str(KIT / "ferramentas" / "checar_lipsync.py"), *map(str, args)],
                              capture_output=True, text=True, encoding="utf-8", errors="replace",
                              env={**os.environ, "PYTHONIOENCODING": "utf-8"})

    def test_cli_reprova_com_codigo_1(self):
        p = self._cli(PASTA / "ls_mulher_1.mp4", "--audio-novo", PASTA / "es_mulher_1.mp3",
                      "--original", PASTA / "pt_mulher_1.mp4")
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        self.assertIn("REPROVADO", p.stdout)

    def test_cli_aprova_com_codigo_0(self):
        p = self._cli(PASTA / "v2_m2a.mp4", "--audio-novo", PASTA / "es_m2a.mp3",
                      "--original", PASTA / "pt_m2a.mp4")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("APROVADO", p.stdout)
        self.assertIn("pausa", p.stdout)

    @unittest.skipUnless((P01 / "ls_s05.mp4").exists(), "AD 01 ausente")
    def test_cli_rosto_forcado(self):
        p = self._cli(P01 / "ls_s05.mp4", "--audio-novo", P01 / "es_s05.mp3", "--original", P01 / "pt_s05.mp4",
                      "--rosto", "320,280,400,440")
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        self.assertIn("320,280,400,440", p.stdout)


if __name__ == "__main__":
    unittest.main()
