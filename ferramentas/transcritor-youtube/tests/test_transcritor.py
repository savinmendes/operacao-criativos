# -*- coding: utf-8 -*-
"""Testes da lógica pura do transcritor.

Nada aqui toca a rede nem a GPU de propósito: o que é testável sem depender do
YouTube é justamente o que costuma quebrar em silêncio (IDs mal extraídos,
timestamps errados, fila duplicando link). O caminho de rede é verificado no
smoke test manual descrito no README.
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.fila import Fila
from lib.texto import (agrupar_blocos, extrair_id, formatar_tempo,
                       nome_arquivo_seguro, parse_json3, parse_vtt)


class TestExtrairId(unittest.TestCase):
    def test_formatos_de_url(self):
        casos = [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtube.com/watch?v=dQw4w9WgXcQ&t=42s", "dQw4w9WgXcQ"),
            ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtu.be/dQw4w9WgXcQ?si=abc", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://m.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ]
        for url, esperado in casos:
            self.assertEqual(extrair_id(url), esperado, url)

    def test_playlist_e_canal_nao_tem_id_de_video(self):
        # precisam ser expandidos pelo yt-dlp antes, não viram item sozinhos
        for url in ["https://www.youtube.com/playlist?list=PL123",
                    "https://www.youtube.com/@canal",
                    "https://www.youtube.com/c/canal/videos"]:
            self.assertIsNone(extrair_id(url), url)

    def test_lixo_nao_vira_id(self):
        for url in ["", "   ", "https://vimeo.com/12345", "não é url"]:
            self.assertIsNone(extrair_id(url), repr(url))

    def test_watch_com_lista_pega_o_video(self):
        # link de vídeo dentro de playlist: o vídeo é o que importa
        self.assertEqual(
            extrair_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL123"),
            "dQw4w9WgXcQ")


class TestFormatarTempo(unittest.TestCase):
    def test_abaixo_de_uma_hora(self):
        self.assertEqual(formatar_tempo(0), "00:00")
        self.assertEqual(formatar_tempo(9.4), "00:09")
        self.assertEqual(formatar_tempo(75), "01:15")
        self.assertEqual(formatar_tempo(3599), "59:59")

    def test_uma_hora_ou_mais_ganha_campo_de_hora(self):
        self.assertEqual(formatar_tempo(3600), "1:00:00")
        self.assertEqual(formatar_tempo(3725), "1:02:05")

    def test_negativo_vira_zero(self):
        self.assertEqual(formatar_tempo(-5), "00:00")


class TestNomeArquivo(unittest.TestCase):
    def test_remove_caracteres_proibidos_no_windows(self):
        n = nome_arquivo_seguro('Oferta: "CartiCuri" <novo> | 2026?/*\\')
        for c in '<>:"/\\|?*':
            self.assertNotIn(c, n)

    def test_nao_fica_vazio(self):
        self.assertTrue(nome_arquivo_seguro("???").strip())
        self.assertTrue(nome_arquivo_seguro("").strip())

    def test_preserva_acento_e_corta_tamanho(self):
        n = nome_arquivo_seguro("Ação de vovó com açaí " * 20)
        self.assertIn("ção", n)
        self.assertLessEqual(len(n), 120)

    def test_nao_termina_em_ponto_ou_espaco(self):
        # o Windows recusa silenciosamente nomes assim
        self.assertFalse(nome_arquivo_seguro("nome.").endswith("."))
        self.assertFalse(nome_arquivo_seguro("nome ").endswith(" "))


class TestAgruparBlocos(unittest.TestCase):
    def segs(self):
        return [
            {"inicio": 0.0, "texto": "Olá, tudo bem?"},
            {"inicio": 2.0, "texto": "Hoje eu vou falar"},
            {"inicio": 4.0, "texto": "sobre dor no joelho."},
            {"inicio": 40.0, "texto": "Segundo bloco começa aqui."},
        ]

    def test_junta_dentro_da_janela(self):
        b = agrupar_blocos(self.segs(), janela=30)
        self.assertEqual(len(b), 2)
        self.assertEqual(b[0]["inicio"], 0.0)
        self.assertEqual(b[0]["texto"], "Olá, tudo bem? Hoje eu vou falar sobre dor no joelho.")
        self.assertEqual(b[1]["inicio"], 40.0)

    def test_janela_menor_quebra_mais(self):
        self.assertEqual(len(agrupar_blocos(self.segs(), janela=3)), 3)

    def test_lista_vazia(self):
        self.assertEqual(agrupar_blocos([], janela=30), [])

    def test_ignora_segmento_em_branco(self):
        s = [{"inicio": 0.0, "texto": "  "}, {"inicio": 1.0, "texto": "vale"}]
        b = agrupar_blocos(s, janela=30)
        self.assertEqual(len(b), 1)
        self.assertEqual(b[0]["texto"], "vale")
        # o bloco herda o tempo do primeiro segmento que de fato tem texto
        self.assertEqual(b[0]["inicio"], 1.0)


class TestParseJson3(unittest.TestCase):
    def test_extrai_segmentos(self):
        bruto = json.dumps({"events": [
            {"tStartMs": 0, "segs": [{"utf8": "Olá"}, {"utf8": " mundo"}]},
            {"tStartMs": 2500, "segs": [{"utf8": "segundo"}]},
            {"tStartMs": 5000, "segs": [{"utf8": "\n"}]},      # só quebra de linha
            {"tStartMs": 6000},                                 # evento sem segs
        ]})
        s = parse_json3(bruto)
        self.assertEqual(len(s), 2)
        self.assertEqual(s[0], {"inicio": 0.0, "texto": "Olá mundo"})
        self.assertEqual(s[1], {"inicio": 2.5, "texto": "segundo"})

    def test_json_invalido_devolve_vazio(self):
        self.assertEqual(parse_json3("não é json"), [])


class TestParseVtt(unittest.TestCase):
    def test_extrai_segmentos(self):
        vtt = (
            "WEBVTT\n"
            "Kind: captions\n"
            "Language: pt\n"
            "\n"
            "00:00:00.000 --> 00:00:02.500\n"
            "Olá, tudo bem?\n"
            "\n"
            "00:00:02.500 --> 00:00:05.000 align:start position:0%\n"
            "Hoje eu vou falar\n"
            "\n"
            "01:00:01.250 --> 01:00:03.000\n"
            "Depois de uma hora\n"
        )
        s = parse_vtt(vtt)
        self.assertEqual(len(s), 3)
        self.assertEqual(s[0], {"inicio": 0.0, "texto": "Olá, tudo bem?"})
        self.assertEqual(s[1]["inicio"], 2.5)
        self.assertEqual(s[2]["inicio"], 3601.25)

    def test_remove_tags_de_karaoke(self):
        vtt = ("WEBVTT\n\n00:00:01.000 --> 00:00:02.000\n"
               "<c.colorE5E5E5>oi</c> <00:00:01.500>tudo bem\n")
        s = parse_vtt(vtt)
        self.assertEqual(s[0]["texto"], "oi tudo bem")

    def test_vazio(self):
        self.assertEqual(parse_vtt("WEBVTT\n"), [])

    def test_legenda_rolante_nao_duplica_e_mantem_o_tempo_de_inicio(self):
        # A legenda automática reescreve a linha anterior em cada cue para dar
        # efeito de rolagem. Ao fundir, o texto que vale é o mais completo, mas
        # o tempo que vale é o do primeiro cue: é quando a fala começou, e é isso
        # que serve para achar o trecho no vídeo.
        vtt = (
            "WEBVTT\n\n"
            "00:00:10.000 --> 00:00:12.000\ndoutor eu sentia\n\n"
            "00:00:12.000 --> 00:00:14.000\ndoutor eu sentia dor no joelho\n\n"
            "00:00:14.000 --> 00:00:16.000\ndoutor eu sentia dor no joelho toda noite\n\n"
            "00:00:20.000 --> 00:00:22.000\nagora eu durmo\n"
        )
        s = parse_vtt(vtt)
        self.assertEqual(len(s), 2)
        self.assertEqual(s[0]["texto"], "doutor eu sentia dor no joelho toda noite")
        self.assertEqual(s[0]["inicio"], 10.0)
        self.assertEqual(s[1]["inicio"], 20.0)


class TestOrdemDeIdioma(unittest.TestCase):
    """A escolha da faixa de legenda tem que priorizar idioma antes de manual/auto."""

    def ranque(self, lang, original=None):
        from lib.legendas import IDIOMAS, _ranque_idioma
        return _ranque_idioma(lang, IDIOMAS, original)

    def test_idioma_original_do_video_vem_na_frente_de_tudo(self):
        # caso real: canal brasileiro com legenda manual só em inglês
        self.assertLess(self.ranque("pt", "pt-BR"), self.ranque("en-US", "pt-BR"))
        self.assertEqual(self.ranque("pt", "pt-BR"), -1)

    def test_variante_regional_conta_como_o_mesmo_idioma(self):
        self.assertEqual(self.ranque("pt-BR", "pt"), -1)
        self.assertEqual(self.ranque("en-GB", "en-US"), -1)

    def test_sem_idioma_original_segue_a_lista_de_preferencia(self):
        self.assertLess(self.ranque("pt", None), self.ranque("es", None))
        self.assertLess(self.ranque("es", None), self.ranque("en", None))

    def test_idioma_fora_da_lista_fica_por_ultimo(self):
        self.assertGreater(self.ranque("ja", None), self.ranque("en", None))

    def test_dentro_do_mesmo_idioma_a_manual_ganha(self):
        # o desempate por peso (manual=0, auto=1) é feito no sorted de buscar();
        # aqui garanto que o ranque de idioma empata, deixando o peso decidir
        self.assertEqual(self.ranque("pt", "pt-BR"), self.ranque("pt-BR", "pt-BR"))


class TestFila(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.caminho = os.path.join(self.tmp, "fila.json")

    def test_adiciona_e_persiste(self):
        f = Fila(self.caminho)
        self.assertEqual(f.adicionar("https://youtu.be/aaaaaaaaaaa"), 1)
        f.salvar()
        self.assertEqual(len(Fila(self.caminho).itens), 1)

    def test_nao_duplica_mesmo_video_em_url_diferente(self):
        f = Fila(self.caminho)
        f.adicionar("https://youtu.be/aaaaaaaaaaa")
        self.assertEqual(f.adicionar("https://www.youtube.com/watch?v=aaaaaaaaaaa"), 0)
        self.assertEqual(len(f.itens), 1)

    def test_pendentes_e_marcar(self):
        f = Fila(self.caminho)
        f.adicionar("https://youtu.be/aaaaaaaaaaa")
        f.adicionar("https://youtu.be/bbbbbbbbbbb")
        self.assertEqual(len(f.pendentes()), 2)
        f.marcar("aaaaaaaaaaa", "feito", arquivo="x.md", motor="legenda")
        self.assertEqual(len(f.pendentes()), 1)
        it = f.buscar("aaaaaaaaaaa")
        self.assertEqual(it["status"], "feito")
        self.assertEqual(it["motor"], "legenda")
        self.assertTrue(it["processado_em"])

    def test_erro_volta_a_ser_pendente_quando_pedido(self):
        f = Fila(self.caminho)
        f.adicionar("https://youtu.be/aaaaaaaaaaa")
        f.marcar("aaaaaaaaaaa", "erro", erro="sem legenda")
        self.assertEqual(len(f.pendentes()), 0)
        self.assertEqual(len(f.pendentes(incluir_erros=True)), 1)

    def test_arquivo_corrompido_nao_derruba(self):
        with open(self.caminho, "w", encoding="utf-8") as fh:
            fh.write("{lixo")
        self.assertEqual(Fila(self.caminho).itens, [])

    def test_remover_concluidos(self):
        f = Fila(self.caminho)
        f.adicionar("https://youtu.be/aaaaaaaaaaa")
        f.adicionar("https://youtu.be/bbbbbbbbbbb")
        f.marcar("aaaaaaaaaaa", "feito")
        self.assertEqual(f.remover_concluidos(), 1)
        self.assertEqual(len(f.itens), 1)


class TestTetoDeTentativas(unittest.TestCase):
    """O YouTube oferece ~157 idiomas de auto-legenda por vídeo. Sem teto, um vídeo
    cujo download esteja falhando faz o código tentar centenas de URLs em sequência —
    foi o que provocou bloqueio por volume numa sessão real de pesquisa."""

    def info_com(self, n_idiomas):
        return {"language": "en",
                "automatic_captions": {("l%03d" % i): [{"ext": "json3", "url": "u"}]
                                       for i in range(n_idiomas)}}

    def test_para_no_teto_quando_tudo_falha(self):
        from lib.legendas import buscar
        chamadas = []
        def falha(formatos):
            chamadas.append(1); return None
        segs, _, _ = buscar(self.info_com(157), max_tentativas=6, baixar=falha)
        self.assertIsNone(segs)
        self.assertEqual(len(chamadas), 6)

    def test_para_assim_que_uma_funciona(self):
        from lib.legendas import buscar
        chamadas = []
        def so_a_terceira(formatos):
            chamadas.append(1)
            return [{"inicio": 0.0, "texto": "oi"}] if len(chamadas) == 3 else None
        segs, _, _ = buscar(self.info_com(157), max_tentativas=6, baixar=so_a_terceira)
        self.assertTrue(segs)
        self.assertEqual(len(chamadas), 3)

    def test_poucos_idiomas_nao_e_afetado(self):
        from lib.legendas import buscar
        chamadas = []
        def falha(formatos):
            chamadas.append(1); return None
        buscar(self.info_com(2), max_tentativas=6, baixar=falha)
        self.assertEqual(len(chamadas), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
