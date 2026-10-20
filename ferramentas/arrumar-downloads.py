# -*- coding: utf-8 -*-
r"""Mantém a pasta Downloads navegável em UM salto, sem esconder nada.

O problema que ele resolve: quem só olha a pasta Downloads não quer descer por
`_organizado/videos/projeto/subpasta` para achar um arquivo. Quer abrir
Downloads, entrar em UMA pasta e já ver o que precisa.

Por isso este script é deliberadamente burro:

- Cria pastas de categoria na RAIZ de Downloads, numeradas para ficarem no topo
  do Explorer: ``1-VIDEOS``, ``2-IMAGENS``, ``3-AUDIO``, ...
- Move os arquivos soltos para dentro delas, **sem subpastas**. Um salto, e o
  arquivo está lá. Para achar, ordene a pasta por data no Explorer.
- **Não renomeia nada.** O nome que você deu (ou que o site deu) é o que você
  lembra na hora de procurar; renomear quebraria exatamente isso.
- **Não toca em pasta nenhuma.** Só mexe em arquivo solto na raiz. Suas pastas
  de projeto continuam onde estão, intactas.

Período de carência
-------------------
Arquivo recém-baixado é o que você mais precisa achar rápido, e o lugar onde
você vai procurar é a raiz. Então os arquivos mais novos que ``--dias`` ficam
soltos de propósito. O padrão é 1: o que você baixou hoje continua à vista.

Desfazer
--------
Toda execução grava um log CSV com origem e destino de cada arquivo. Se algo
sair errado, ``--desfazer <log.csv>`` devolve tudo para onde estava.

Uso
---
    python ferramentas/arrumar-downloads.py                    # simula, não move
    python ferramentas/arrumar-downloads.py --executar         # move de verdade
    python ferramentas/arrumar-downloads.py --executar --dias 3
    python ferramentas/arrumar-downloads.py --desfazer <log.csv>

Simular é o padrão de propósito: mover arquivo em massa é fácil de pedir e
chato de reverter, então o script só move quando alguém escreve ``--executar``.
"""
import argparse
import csv
import os
import shutil
import sys
import time

PASTA_PADRAO = os.path.join(os.path.expanduser("~"), "Downloads")

# Categoria -> extensões. A ordem numérica é o que coloca as pastas no topo do
# Explorer, acima das pastas de projeto, que começam com letra.
CATEGORIAS = [
    ("1-VIDEOS", {"mp4", "webm", "mov", "mpeg", "mpg", "avi", "mkv", "m4v", "wmv", "flv", "ts"}),
    ("2-IMAGENS", {"png", "jpg", "jpeg", "jfif", "webp", "gif", "bmp", "tiff", "tif", "svg", "heic", "avif"}),
    ("3-AUDIO", {"mp3", "wav", "m4a", "aac", "ogg", "flac", "wma", "opus"}),
    ("4-DOCUMENTOS", {"pdf", "md", "txt", "doc", "docx", "odt", "rtf", "html", "htm", "epub", "pptx", "ppt"}),
    ("5-PLANILHAS", {"csv", "xlsx", "xls", "ods", "tsv"}),
    ("6-PACOTES", {"zip", "rar", "7z", "tar", "gz", "exe", "msi", "dmg", "apk", "iso"}),
]
OUTROS = "7-OUTROS"

NOMES_CATEGORIAS = [c for c, _ in CATEGORIAS] + [OUTROS]

# Nunca movidos, mesmo estando soltos na raiz: são do sistema ou do próprio
# gerenciador de download, e sumir com eles causa confusão sem ganho nenhum.
IGNORAR_NOMES = {"desktop.ini", "thumbs.db", ".ds_store"}
# Download ainda em andamento. Mover agora corrompe o arquivo.
IGNORAR_SUFIXOS = (".crdownload", ".part", ".partial", ".tmp", ".download", ".!ut")
# Arquivos do próprio arrumador. Sem isto o log de desfazer, que é um .csv,
# seria varrido para a pasta de planilhas na execução seguinte — justo o
# arquivo que alguém procura na raiz quando quer reverter alguma coisa.
IGNORAR_PREFIXOS = ("_arrum",)


def categoria_de(nome):
    ext = nome.rsplit(".", 1)[-1].lower() if "." in nome else ""
    for categoria, exts in CATEGORIAS:
        if ext in exts:
            return categoria
    return OUTROS


def nome_livre(destino, nome):
    """Nome que não colide no destino. Nunca sobrescreve nada."""
    alvo = os.path.join(destino, nome)
    if not os.path.exists(alvo):
        return alvo
    base, ext = os.path.splitext(nome)
    n = 2
    while True:
        alvo = os.path.join(destino, "%s_%d%s" % (base, n, ext))
        if not os.path.exists(alvo):
            return alvo
        n += 1


def planejar(pasta, dias):
    """Lista de (origem, categoria, nome) a mover, e a contagem do que ficou."""
    agora = time.time()
    limite = dias * 86400
    plano, recentes, ignorados = [], 0, 0

    for nome in sorted(os.listdir(pasta)):
        caminho = os.path.join(pasta, nome)
        if not os.path.isfile(caminho):
            continue  # pastas nunca são tocadas
        baixo = nome.lower()
        if (baixo in IGNORAR_NOMES
                or baixo.endswith(IGNORAR_SUFIXOS)
                or baixo.startswith(IGNORAR_PREFIXOS)):
            ignorados += 1
            continue
        try:
            idade = agora - os.path.getmtime(caminho)
        except OSError:
            ignorados += 1
            continue
        if idade < limite:
            recentes += 1  # recém-baixado fica à vista de propósito
            continue
        plano.append((caminho, categoria_de(nome), nome))

    return plano, recentes, ignorados


def tamanho_legivel(b):
    for unidade in ("B", "KB", "MB", "GB"):
        if b < 1024 or unidade == "GB":
            return "%.1f %s" % (b, unidade)
        b /= 1024.0


def executar(pasta, plano, log_path):
    movidos, erros = 0, []
    with open(log_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["origem", "destino", "quando"])
        for origem, categoria, nome in plano:
            destino_dir = os.path.join(pasta, categoria)
            os.makedirs(destino_dir, exist_ok=True)
            alvo = nome_livre(destino_dir, nome)
            try:
                shutil.move(origem, alvo)
            except OSError as e:
                erros.append((nome, str(e)))
                continue
            w.writerow([origem, alvo, time.strftime("%Y-%m-%d %H:%M:%S")])
            movidos += 1
    return movidos, erros


def desfazer(log_path):
    if not os.path.exists(log_path):
        print("Log não encontrado: %s" % log_path)
        return 1
    voltaram, falharam = 0, []
    with open(log_path, encoding="utf-8-sig") as f:
        linhas = list(csv.DictReader(f))
    for linha in reversed(linhas):
        origem, destino = linha["origem"], linha["destino"]
        if not os.path.exists(destino):
            falharam.append((destino, "não está mais lá"))
            continue
        if os.path.exists(origem):
            falharam.append((destino, "já existe um arquivo no lugar original"))
            continue
        try:
            shutil.move(destino, origem)
            voltaram += 1
        except OSError as e:
            falharam.append((destino, str(e)))
    print("Devolvidos: %d de %d" % (voltaram, len(linhas)))
    for d, motivo in falharam:
        print("   nao voltou: %s  (%s)" % (os.path.basename(d), motivo))
    return 0


def main():
    p = argparse.ArgumentParser(description="Arruma a pasta Downloads em um nivel so.")
    p.add_argument("--pasta", default=PASTA_PADRAO, help="padrão: %(default)s")
    p.add_argument("--dias", type=int, default=1,
                   help="arquivos mais novos que isso ficam soltos (padrão: %(default)s)")
    p.add_argument("--executar", action="store_true",
                   help="move de verdade; sem isso o script apenas simula")
    p.add_argument("--desfazer", metavar="LOG.CSV",
                   help="devolve os arquivos de um log anterior para a raiz")
    args = p.parse_args()

    if args.desfazer:
        return desfazer(args.desfazer)

    if not os.path.isdir(args.pasta):
        print("Pasta não encontrada: %s" % args.pasta)
        return 1

    plano, recentes, ignorados = planejar(args.pasta, args.dias)

    # Resumo por categoria antes de qualquer coisa: é o que permite perceber
    # que algo foi parar na categoria errada ANTES de mover.
    por_cat = {}
    for origem, categoria, nome in plano:
        try:
            tam = os.path.getsize(origem)
        except OSError:
            tam = 0
        d = por_cat.setdefault(categoria, {"n": 0, "bytes": 0, "exemplos": []})
        d["n"] += 1
        d["bytes"] += tam
        if len(d["exemplos"]) < 3:
            d["exemplos"].append(nome)

    modo = "EXECUTANDO" if args.executar else "SIMULACAO (nada foi movido)"
    print("== %s ==" % modo)
    print("Pasta: %s" % args.pasta)
    print("Carencia: arquivos com menos de %d dia(s) ficam soltos" % args.dias)
    print()

    if not plano:
        print("Nada a mover.")
    else:
        for categoria in NOMES_CATEGORIAS:
            if categoria not in por_cat:
                continue
            d = por_cat[categoria]
            print("   %-14s %4d arquivo(s)  %10s" % (categoria, d["n"], tamanho_legivel(d["bytes"])))
            for ex in d["exemplos"]:
                print("        %s" % ex[:72])
            if d["n"] > 3:
                print("        ... e mais %d" % (d["n"] - 3))
        print()

    print("   ficam soltos (recentes): %d" % recentes)
    print("   ignorados (sistema / download em andamento): %d" % ignorados)
    print()

    if not args.executar:
        if plano:
            print("Para mover de verdade, repita com --executar")
        return 0

    if not plano:
        # Rodando todo dia, o caso comum é não ter nada a mover. Gravar um log
        # vazio nessa hora encheria a raiz de CSV inútil — exatamente a bagunça
        # que este script existe para evitar.
        return 0

    log_path = os.path.join(args.pasta, "_arrumacao-%s.csv" % time.strftime("%Y%m%d-%H%M%S"))
    movidos, erros = executar(args.pasta, plano, log_path)
    print("Movidos: %d" % movidos)
    for nome, e in erros:
        print("   FALHOU: %s  (%s)" % (nome, e))
    print("Log (para desfazer): %s" % log_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
