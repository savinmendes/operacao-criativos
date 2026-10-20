# -*- coding: utf-8 -*-
"""Site local para corrigir em massa videos recusados pela plataforma.

    python servidor.py

Abre no navegador. Por que local e nao hospedado: a pagina precisa ler uma
pasta com centenas de videos e reencodar cada um. Navegador nao alcanca disco,
e reencodar dentro do navegador (ffmpeg.wasm) e varias vezes mais lento e
estoura memoria em arquivo de 100 MB. Aqui o navegador e so a tela; quem
trabalha e o ffmpeg nativo que a maquina ja tem.

Os originais NUNCA sao tocados: o resultado vai para uma subpasta `corrigidos`.
"""
import json
import os
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import correcao, sonda

RAIZ = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(RAIZ, "web")
PORTA_PADRAO = 8750
SUBPASTA_SAIDA = "corrigidos"


class Fila(object):
    """Estado da conversao. Uma de cada vez, para nao brigar por CPU."""

    def __init__(self):
        self.trava = threading.Lock()
        self.itens = []
        self.indice = 0
        self.rodando = False
        self.cancelar = False
        self.log = []
        self.proc = None

    def estado(self):
        with self.trava:
            return {
                "rodando": self.rodando,
                "indice": self.indice,
                "total": len(self.itens),
                "atual": (self.itens[self.indice]["nome"]
                          if self.rodando and self.indice < len(self.itens) else None),
                "log": self.log[-200:],
            }

    def registrar(self, nome, situacao, detalhe=""):
        with self.trava:
            self.log.append({"nome": nome, "situacao": situacao,
                             "detalhe": detalhe, "quando": time.strftime("%H:%M:%S")})


FILA = Fila()


def _saida_para(entrada, pasta_base):
    pasta = os.path.join(pasta_base, SUBPASTA_SAIDA)
    os.makedirs(pasta, exist_ok=True)
    base, _ = os.path.splitext(os.path.basename(entrada))
    alvo = os.path.join(pasta, base + ".mp4")
    # Nunca sobrescreve: nem o original (que esta noutra pasta) nem uma
    # correcao anterior, que pode ter sido feita com outro perfil.
    n = 2
    while os.path.exists(alvo):
        alvo = os.path.join(pasta, "%s_%d.mp4" % (base, n))
        n += 1
    return alvo


def trabalhar(perfil_nome):
    p = correcao.perfil(perfil_nome)
    with FILA.trava:
        FILA.rodando = True
        FILA.cancelar = False
        FILA.indice = 0

    while True:
        with FILA.trava:
            if FILA.cancelar or FILA.indice >= len(FILA.itens):
                break
            item = FILA.itens[FILA.indice]
        entrada = item["caminho"]
        nome = item["nome"]
        try:
            m = sonda.medir(entrada)
            plano = correcao.planejar(m, p)
            if not plano.precisa:
                FILA.registrar(nome, "pulado", "ja cumpre o minimo")
            else:
                saida = _saida_para(entrada, item["pasta_base"])
                cmd = correcao.comando_ffmpeg(entrada, saida, plano)
                proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                                        stderr=subprocess.PIPE)
                with FILA.trava:
                    FILA.proc = proc
                _, err = proc.communicate()
                with FILA.trava:
                    FILA.proc = None
                if proc.returncode != 0:
                    msg = err.decode("utf-8", "replace").strip().splitlines()
                    FILA.registrar(nome, "erro", msg[-1][:200] if msg else "ffmpeg falhou")
                    if os.path.exists(saida):
                        os.remove(saida)      # arquivo pela metade engana mais do que ajuda
                else:
                    # Confere o resultado em vez de confiar no codigo de saida:
                    # ffmpeg retorna 0 em casos onde o arquivo sai fora do alvo.
                    try:
                        depois = sonda.medir(saida)
                        restante = correcao.avaliar(depois, p)
                        if restante:
                            FILA.registrar(nome, "atencao",
                                           "saiu %dx%d @ %s kbps e ainda reprova em %s" % (
                                               depois.largura, depois.altura,
                                               ("%.0f" % depois.kbps) if depois.kbps else "?",
                                               ", ".join(restante)))
                        else:
                            FILA.registrar(nome, "ok", "%dx%d @ %.0f kbps" % (
                                depois.largura, depois.altura, depois.kbps or 0))
                    except sonda.ErroSonda as e:
                        FILA.registrar(nome, "atencao", "convertido mas ilegivel: %s" % e)
        except Exception as e:
            FILA.registrar(nome, "erro", str(e)[:200])
        with FILA.trava:
            FILA.indice += 1

    with FILA.trava:
        FILA.rodando = False


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass                                    # o console e do usuario, nao do servidor

    def _json(self, obj, codigo=200):
        corpo = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def _corpo(self):
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8"))
        except ValueError:
            return {}

    def do_GET(self):
        caminho = urlparse(self.path).path
        if caminho in ("/", "/index.html"):
            try:
                with open(os.path.join(WEB, "index.html"), "rb") as f:
                    corpo = f.read()
            except OSError:
                self.send_error(500, "index.html nao encontrado")
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)
        elif caminho == "/api/progresso":
            self._json(FILA.estado())
        else:
            self.send_error(404)

    def do_POST(self):
        caminho = urlparse(self.path).path
        dados = self._corpo()
        if caminho == "/api/escanear":
            self._escanear(dados)
        elif caminho == "/api/corrigir":
            self._corrigir(dados)
        elif caminho == "/api/parar":
            with FILA.trava:
                FILA.cancelar = True
                if FILA.proc:
                    try:
                        FILA.proc.kill()
                    except OSError:
                        pass
            self._json({"ok": True})
        elif caminho == "/api/abrir-pasta":
            alvo = dados.get("pasta") or ""
            if os.path.isdir(alvo):
                os.startfile(alvo)              # noqa  (so existe no Windows)
                self._json({"ok": True})
            else:
                self._json({"erro": "pasta inexistente"}, 400)
        else:
            self.send_error(404)

    def _escanear(self, dados):
        pasta = (dados.get("pasta") or "").strip().strip('"')
        if not pasta or not os.path.isdir(pasta):
            self._json({"erro": "pasta nao encontrada: %s" % pasta}, 400)
            return
        p = correcao.perfil(dados.get("perfil") or "tiktok")
        recursivo = bool(dados.get("recursivo", True))

        linhas = []
        for caminho in sonda.listar_videos(pasta, recursivo):
            linha = {"caminho": caminho,
                     "nome": os.path.relpath(caminho, pasta),
                     "tamanho": os.path.getsize(caminho)}
            try:
                m = sonda.medir(caminho)
            except sonda.ErroSonda as e:
                linha.update({"situacao": "ilegivel", "detalhe": str(e)[:120]})
                linhas.append(linha)
                continue
            problemas = correcao.avaliar(m, p)
            plano = correcao.planejar(m, p)
            linha.update({
                "largura": m.largura, "altura": m.altura,
                "kbps": round(m.kbps, 1) if m.kbps else None,
                "duracao": round(m.duracao, 1) if m.duracao else None,
                "codec": m.codec_video,
                "problemas": problemas,
                "situacao": "reprovado" if problemas else "ok",
                "plano": plano.resumo() if plano.precisa else "",
            })
            linhas.append(linha)

        self._json({"pasta": pasta, "perfil": p["nome"],
                    "minimos": {"curto": p["lado_curto_min"],
                                "longo": p["lado_longo_min"],
                                "kbps": p["kbps_min"]},
                    "videos": linhas,
                    "saida": os.path.join(pasta, SUBPASTA_SAIDA)})

    def _corrigir(self, dados):
        with FILA.trava:
            if FILA.rodando:
                self._json({"erro": "ja existe uma fila rodando"}, 409)
                return
        pasta = (dados.get("pasta") or "").strip()
        caminhos = dados.get("arquivos") or []
        if not caminhos:
            self._json({"erro": "nenhum video selecionado"}, 400)
            return
        itens = [{"caminho": c, "nome": os.path.basename(c), "pasta_base": pasta}
                 for c in caminhos if os.path.isfile(c)]
        with FILA.trava:
            FILA.itens = itens
            FILA.indice = 0
            FILA.log = []
        t = threading.Thread(target=trabalhar,
                             args=(dados.get("perfil") or "tiktok",), daemon=True)
        t.start()
        self._json({"ok": True, "total": len(itens),
                    "saida": os.path.join(pasta, SUBPASTA_SAIDA)})


def checar_ffmpeg():
    for prog in ("ffmpeg", "ffprobe"):
        try:
            subprocess.run([prog, "-version"], capture_output=True, timeout=20)
        except (OSError, subprocess.TimeoutExpired):
            return prog
    return None


def main():
    faltando = checar_ffmpeg()
    if faltando:
        print("ERRO: '%s' nao foi encontrado no PATH." % faltando)
        print("A ferramenta inteira depende dele. Instale o ffmpeg e rode de novo.")
        return 1

    porta = PORTA_PADRAO
    abrir = True
    for arg in sys.argv[1:]:
        if arg in ("--sem-navegador", "-s"):
            abrir = False          # usado nos testes e em maquina sem interface
        else:
            try:
                porta = int(arg)
            except ValueError:
                pass

    endereco = "http://127.0.0.1:%d/" % porta
    # 127.0.0.1 e nao 0.0.0.0 de proposito: o servidor le e escreve arquivos da
    # maquina, entao nao tem por que estar acessivel pela rede.
    srv = ThreadingHTTPServer(("127.0.0.1", porta), Handler)
    print("Corretor de video rodando em %s" % endereco)
    print("Deixe esta janela aberta. Ctrl+C encerra.")
    if abrir:
        try:
            webbrowser.open(endereco)
        except Exception:
            pass
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nencerrado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
