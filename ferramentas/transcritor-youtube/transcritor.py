# -*- coding: utf-8 -*-
"""Transcritor de vídeos do YouTube em massa.

Fluxo: você vai salvando links com `add` ao longo da semana e roda `rodar` quando
quiser. Para cada vídeo pendente tenta primeiro a legenda que o YouTube já tem
(segundos, custo zero) e só cai para o Whisper local na GPU quando não existe
legenda alguma.

    python transcritor.py add https://youtu.be/xxxx
    python transcritor.py add --arquivo links.txt
    python transcritor.py lista
    python transcritor.py rodar
    python transcritor.py limpar

Veja o README.md para as opções de cada comando.
"""
import argparse
import io
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import legendas, whisper_local
from lib.fila import Fila
from lib.texto import (agrupar_blocos, e_lista, extrair_id, formatar_tempo,
                       nome_arquivo_seguro)

AQUI = os.path.dirname(os.path.abspath(__file__))
FILA = os.path.join(AQUI, "fila.json")
SAIDA = os.path.join(AQUI, "transcricoes")


# ----------------------------------------------------------------- utilidades

def _p(texto=""):
    """Print que não quebra em terminal com codepage antiga."""
    try:
        print(texto)
    except UnicodeEncodeError:
        print(texto.encode("utf-8", "replace").decode("ascii", "replace"))


def _duracao(segundos):
    return formatar_tempo(segundos) if segundos else "?"


def escrever_transcricao(info, blocos, motor, pasta, janela):
    """Grava um .md por vídeo: cabeçalho com a procedência + transcrição."""
    os.makedirs(pasta, exist_ok=True)
    vid = info.get("id") or "sem-id"
    titulo = info.get("title") or vid
    nome = "%s__%s.md" % (nome_arquivo_seguro(titulo, 100), vid)
    caminho = os.path.join(pasta, nome)

    linhas = [
        "# %s" % titulo,
        "",
        "| | |",
        "|---|---|",
        "| Canal | %s |" % (info.get("uploader") or info.get("channel") or "?"),
        "| Duração | %s |" % _duracao(info.get("duration")),
        "| Publicado | %s |" % _formatar_data(info.get("upload_date")),
        "| URL | https://www.youtube.com/watch?v=%s |" % vid,
        "| Origem da transcrição | %s |" % motor,
        "| Transcrito em | %s |" % datetime.now().strftime("%d/%m/%Y %H:%M"),
        "| Blocos | %d (janela de %ds) |" % (len(blocos), janela),
        "",
        "---",
        "",
    ]
    for b in blocos:
        linhas.append("**[%s]** %s" % (formatar_tempo(b["inicio"]), b["texto"]))
        linhas.append("")

    with io.open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    return caminho


def escrever_txt(info, blocos, pasta):
    """Versão em texto corrido, sem timestamp nem marcação.

    Serve para colar em prompt, importar em outra ferramenta ou ler de ponta a
    ponta — casos em que a marcação do .md atrapalha mais do que ajuda.
    """
    os.makedirs(pasta, exist_ok=True)
    vid = info.get("id") or "sem-id"
    titulo = info.get("title") or vid
    caminho = os.path.join(pasta, "%s__%s.txt" % (nome_arquivo_seguro(titulo, 100), vid))

    linhas = [
        titulo,
        "%s · %s · https://www.youtube.com/watch?v=%s" % (
            info.get("uploader") or info.get("channel") or "?",
            _duracao(info.get("duration")), vid),
        "",
    ]
    linhas.extend(b["texto"] for b in blocos)

    with io.open(caminho, "w", encoding="utf-8") as f:
        f.write("\n\n".join(linhas))
    return caminho


def _formatar_data(aaaammdd):
    if not aaaammdd or len(str(aaaammdd)) != 8:
        return "?"
    s = str(aaaammdd)
    return "%s/%s/%s" % (s[6:8], s[4:6], s[0:4])


# -------------------------------------------------------------------- comandos

def cmd_add(args):
    fila = Fila(args.fila)
    entradas = list(args.urls or [])

    if args.arquivo:
        if not os.path.exists(args.arquivo):
            _p("Arquivo não encontrado: %s" % args.arquivo)
            return 1
        with io.open(args.arquivo, encoding="utf-8-sig") as f:
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith("#"):
                    entradas.append(linha)

    if not entradas:
        _p("Nada para adicionar. Passe uma URL ou use --arquivo.")
        return 1

    novos = repetidos = invalidos = 0
    for entrada in entradas:
        if e_lista(entrada):
            _p("Expandindo lista: %s" % entrada)
            try:
                urls = legendas.expandir(entrada)
            except legendas.ErroYoutube as e:
                _p("   falhou: %s" % e)
                invalidos += 1
                continue
            _p("   %d vídeos encontrados" % len(urls))
            for u in urls:
                if fila.adicionar(u):
                    novos += 1
                else:
                    repetidos += 1
            continue

        if not extrair_id(entrada):
            _p("Ignorado (não é link de vídeo do YouTube): %s" % entrada)
            invalidos += 1
            continue
        if fila.adicionar(entrada):
            novos += 1
        else:
            repetidos += 1

    fila.salvar()
    _p("")
    _p("Adicionados: %d · já estavam na fila: %d · ignorados: %d"
       % (novos, repetidos, invalidos))
    _p("Fila agora: %s" % _resumo(fila))
    return 0


def _resumo(fila):
    r = fila.resumo()
    if not r:
        return "vazia"
    return " · ".join("%s: %d" % (k, v) for k, v in sorted(r.items()))


def cmd_lista(args):
    fila = Fila(args.fila)
    if not fila.itens:
        _p("Fila vazia. Use: python transcritor.py add <url>")
        return 0

    _p("%-13s %-11s %-9s %s" % ("VIDEO ID", "STATUS", "MOTOR", "TÍTULO"))
    _p("-" * 100)
    for it in fila.itens:
        if args.status and it.get("status") != args.status:
            continue
        motor = (it.get("motor") or "-")
        motor = motor.split("/")[0][:9]
        _p("%-13s %-11s %-9s %s" % (
            it.get("video_id", "?"), it.get("status", "?"), motor,
            (it.get("titulo") or it.get("url") or "")[:58]))
        if it.get("erro"):
            _p("%-13s   ↳ %s" % ("", str(it["erro"])[:80]))
    _p("-" * 100)
    _p(_resumo(fila))
    return 0


def cmd_local(args):
    """Transcreve um arquivo de vídeo ou áudio que já está no disco."""
    caminho = os.path.abspath(args.arquivo)
    if not os.path.isfile(caminho):
        _p("Arquivo não encontrado: %s" % caminho)
        return 1
    if not whisper_local.disponivel():
        _p("faster-whisper não está instalado. Rode: pip install faster-whisper")
        return 1

    nome = os.path.splitext(os.path.basename(caminho))[0]
    _p("%s · %.1f MB" % (nome, os.path.getsize(caminho) / 1048576.0))
    _p("transcrevendo (arquivo local, sempre pelo Whisper — não há legenda pronta)...")

    try:
        segmentos, motor, info = whisper_local.transcrever_arquivo(
            caminho, tamanho=args.modelo, idioma=args.idioma_whisper,
            dispositivo=args.dispositivo, avisar=lambda m: _p("   AVISO: %s" % m))
    except whisper_local.ErroWhisper as e:
        _p("falhou: %s" % e)
        return 1

    if not segmentos:
        _p("nenhuma fala detectada — o arquivo tem áudio?")
        return 1

    dur = getattr(info, "duration", None)
    meta = {"id": "local", "title": nome, "uploader": "arquivo local",
            "duration": dur, "upload_date": None}
    blocos = agrupar_blocos(segmentos, janela=args.janela)
    caminho_md = escrever_transcricao(meta, blocos, motor, args.saida, args.janela)
    _p("   %s · %d segmentos · %d blocos" % (motor, len(segmentos), len(blocos)))
    _p("   salvo: %s" % os.path.basename(caminho_md))
    if args.txt:
        _p("   txt:   %s" % os.path.basename(escrever_txt(meta, blocos, args.saida)))
    _p("Saída: %s" % args.saida)
    return 0


def cmd_limpar(args):
    fila = Fila(args.fila)
    n = fila.remover_concluidos()
    fila.salvar()
    _p("Removidos da fila: %d concluídos. Os arquivos de transcrição continuam em %s"
       % (n, SAIDA))
    return 0


def cmd_rodar(args):
    fila = Fila(args.fila)
    pendentes = fila.pendentes(incluir_erros=args.repetir_erros)
    if args.limite:
        pendentes = pendentes[:args.limite]

    if not pendentes:
        _p("Nada pendente. %s" % _resumo(fila))
        return 0

    usar_whisper = args.motor in ("hibrido", "whisper")
    usar_legenda = args.motor in ("hibrido", "legenda")

    if usar_whisper and not whisper_local.disponivel():
        if args.motor == "whisper":
            _p("faster-whisper não está instalado. Rode: pip install faster-whisper")
            return 1
        _p("Aviso: faster-whisper não instalado — vídeos sem legenda serão pulados.")
        usar_whisper = False

    _p("Pendentes: %d · motor: %s · janela: %ds" % (len(pendentes), args.motor, args.janela))
    _p("")

    feitos = falhas = sem = 0
    for i, it in enumerate(pendentes, 1):
        vid = it["video_id"]
        url = it["url"]
        _p("[%d/%d] %s" % (i, len(pendentes), it.get("titulo") or url))

        try:
            info = legendas.info_video(url)
        except legendas.ErroYoutube as e:
            _p("   erro ao ler o vídeo: %s" % e)
            fila.marcar(vid, "erro", erro=str(e))
            fila.salvar()
            falhas += 1
            continue

        titulo = info.get("title") or vid
        canal = info.get("uploader") or info.get("channel")
        duracao = info.get("duration")
        _p("   %s · %s · %s" % (titulo[:58], canal or "?", _duracao(duracao)))

        segmentos, motor = None, None

        if usar_legenda:
            try:
                segmentos, lang, tipo = legendas.buscar(info, args.idiomas)
                if segmentos:
                    motor = "%s (%s)" % (tipo, lang)
                    _p("   legenda encontrada: %s em %s · %d segmentos"
                       % (tipo, lang, len(segmentos)))
            except Exception as e:
                _p("   legenda falhou (%s), seguindo" % str(e)[:60])

        if not segmentos and usar_whisper:
            _p("   sem legenda — transcrevendo o áudio...")
            try:
                segmentos, motor = whisper_local.transcrever(
                    url, tamanho=args.modelo, idioma=args.idioma_whisper,
                    dispositivo=args.dispositivo,
                    avisar=lambda m: _p("   AVISO: %s" % m))
                _p("   %s · %d segmentos" % (motor, len(segmentos)))
            except whisper_local.ErroWhisper as e:
                _p("   whisper falhou: %s" % e)
                fila.marcar(vid, "erro", erro=str(e), titulo=titulo,
                            canal=canal, duracao=duracao)
                fila.salvar()
                falhas += 1
                continue

        if not segmentos:
            _p("   sem legenda e sem whisper — pulado")
            fila.marcar(vid, "sem-legenda", titulo=titulo, canal=canal, duracao=duracao,
                        erro="vídeo não tem legenda e o Whisper não foi usado")
            fila.salvar()
            sem += 1
            continue

        blocos = agrupar_blocos(segmentos, janela=args.janela)
        caminho = escrever_transcricao(info, blocos, motor, args.saida, args.janela)
        if args.txt:
            txt = escrever_txt(info, blocos, args.saida)
            _p("   txt: %s" % os.path.basename(txt))
        fila.marcar(vid, "feito", arquivo=caminho, motor=motor, titulo=titulo,
                    canal=canal, duracao=duracao, erro=None)
        fila.salvar()
        feitos += 1
        _p("   salvo: %s" % os.path.basename(caminho))
        _p("")

    _p("=" * 60)
    _p("Transcritos: %d · sem legenda: %d · erros: %d" % (feitos, sem, falhas))
    _p("Saída: %s" % args.saida)
    _p("Fila: %s" % _resumo(fila))
    return 0


# ----------------------------------------------------------------------- main

def montar_parser():
    p = argparse.ArgumentParser(
        prog="transcritor",
        description="Transcreve vídeos do YouTube em massa, a partir de uma fila de links.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""exemplos:
  python transcritor.py add https://youtu.be/xxxx https://youtu.be/yyyy
  python transcritor.py add "https://www.youtube.com/@umcanal/videos"
  python transcritor.py add --arquivo links.txt
  python transcritor.py lista --status pendente
  python transcritor.py rodar --limite 20
  python transcritor.py rodar --motor legenda
  python transcritor.py limpar
""")
    p.add_argument("--fila", default=FILA, help="caminho do arquivo de fila")
    sub = p.add_subparsers(dest="comando")

    a = sub.add_parser("add", help="salva link(s) na fila (vídeo, playlist ou canal)")
    a.add_argument("urls", nargs="*", help="uma ou mais URLs")
    a.add_argument("--arquivo", help="arquivo .txt com uma URL por linha")
    a.set_defaults(func=cmd_add)

    l = sub.add_parser("lista", help="mostra a fila")
    l.add_argument("--status", choices=["pendente", "feito", "erro", "sem-legenda"])
    l.set_defaults(func=cmd_lista)

    r = sub.add_parser("rodar", help="transcreve os pendentes")
    r.add_argument("--limite", type=int, help="processa no máximo N vídeos")
    r.add_argument("--motor", choices=["hibrido", "legenda", "whisper"], default="hibrido",
                   help="hibrido (padrão): legenda e, na falta dela, Whisper local")
    r.add_argument("--janela", type=int, default=30,
                   help="segundos por bloco de timestamp (padrão 30)")
    r.add_argument("--modelo", default="large-v3",
                   help="modelo do Whisper: tiny, base, small, medium, large-v3")
    r.add_argument("--idioma-whisper", dest="idioma_whisper", default=None,
                   help="força o idioma no Whisper (ex.: pt). Padrão: detecta sozinho")
    r.add_argument("--dispositivo", choices=["auto", "cuda", "cpu"], default="auto",
                   help="auto (padrão): usa a GPU e avisa se cair para CPU")
    r.add_argument("--idiomas", nargs="+", default=None,
                   help="ordem de preferência de idioma da legenda")
    r.add_argument("--repetir-erros", action="store_true",
                   help="tenta de novo os itens marcados como erro ou sem-legenda")
    r.add_argument("--txt", action="store_true",
                   help="gera também um .txt de texto corrido, sem timestamps")
    r.add_argument("--saida", default=SAIDA, help="pasta das transcrições")
    r.set_defaults(func=cmd_rodar)

    lo = sub.add_parser("local", help="transcreve um arquivo de vídeo/áudio do disco")
    lo.add_argument("arquivo", help="caminho do .mp4, .mov, .mp3, .wav ...")
    lo.add_argument("--janela", type=int, default=30)
    lo.add_argument("--modelo", default="large-v3")
    lo.add_argument("--idioma-whisper", dest="idioma_whisper", default=None,
                    help="força o idioma (ex.: pt). Padrão: detecta sozinho")
    lo.add_argument("--dispositivo", choices=["auto", "cuda", "cpu"], default="auto")
    lo.add_argument("--txt", action="store_true", help="gera também o texto corrido")
    lo.add_argument("--saida", default=SAIDA)
    lo.set_defaults(func=cmd_local)

    c = sub.add_parser("limpar", help="tira os concluídos da fila")
    c.set_defaults(func=cmd_limpar)
    return p


def main():
    p = montar_parser()
    args = p.parse_args()
    if not getattr(args, "func", None):
        p.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
