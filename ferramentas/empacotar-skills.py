# -*- coding: utf-8 -*-
r"""Empacota as skills do projeto em .zip prontos para upload no claude.ai.

Existe porque a skill vive em dois lugares: a pasta local (fonte de verdade) e
a cópia enviada para a nuvem. Sem um comando único, as duas divergem em
silêncio — edita-se a local, esquece-se de subir, e a da nuvem passa a ser uma
versão antiga que ninguém lembra de qual é.

    python ferramentas/empacotar-skills.py

Antes de gerar qualquer zip o script confere duas coisas que já causaram
problema de verdade:

1. O ``name:`` do frontmatter tem de ser igual ao nome da pasta. O upload
   rejeita quando divergem, e a mensagem de erro não diz qual dos dois está
   errado.
2. Nenhum arquivo pode conter caminho da máquina local. Uma skill com
   ``C:\Users\<alguem>\...`` embutido quebra em qualquer outro ambiente, e o
   caminho ainda carrega o nome de usuário para fora do computador.

Se qualquer uma das duas falhar o script PARA sem gerar zip: subir uma skill
quebrada custa mais do que não subir nada.
"""
import argparse
import os
import re
import sys
import zipfile

# A pasta que contém as skills, relativa à raiz do projeto (pai de ferramentas/).
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(RAIZ, ".claude", "skills")
DESTINO_PADRAO = os.path.join(os.path.expanduser("~"), "Downloads")

# Não vão para a nuvem: teste é ferramenta de desenvolvimento, e o resto é lixo
# de build que só engorda o pacote.
PASTAS_EXCLUIDAS = {"tests", "test", "__pycache__", ".git", "evals"}
SUFIXOS_EXCLUIDOS = (".pyc", ".pyo", ".bak")

EXTENSOES_VARRIDAS = (".md", ".py", ".ps1")

# Marcas de caminho local. A lista é de padrões genéricos de propósito: serve
# para qualquer máquina, não só para a de quem escreveu o script.
PADROES_LOCAIS = [
    (r"[A-Za-z]:\\Users\\", "caminho Windows absoluto"),
    (r"/[a-zA-Z]/Users/", "caminho Windows em formato POSIX"),
    (r"/home/[^/\s]+/", "caminho Linux de usuário"),
    (r"(?<!\w)/Users/[^/\s]+/", "caminho macOS de usuário"),
    (r"python\.exe", "executável Python da máquina local"),
    (r"[A-Za-z]:\\", "raiz de disco Windows"),
]


def _ignorar(caminho_rel):
    partes = caminho_rel.replace("\\", "/").split("/")
    if any(p in PASTAS_EXCLUIDAS for p in partes[:-1]):
        return True
    return partes[-1].endswith(SUFIXOS_EXCLUIDOS)


def listar_skills():
    if not os.path.isdir(SKILLS):
        return []
    achadas = []
    for nome in sorted(os.listdir(SKILLS)):
        pasta = os.path.join(SKILLS, nome)
        if os.path.isdir(pasta) and os.path.exists(os.path.join(pasta, "SKILL.md")):
            achadas.append(nome)
    return achadas


def arquivos_da_skill(nome):
    """Caminhos (absoluto, relativo) que entram no zip, já filtrados."""
    pasta = os.path.join(SKILLS, nome)
    saida = []
    for raiz, dirs, arqs in os.walk(pasta):
        dirs[:] = [d for d in dirs if d not in PASTAS_EXCLUIDAS]
        for a in sorted(arqs):
            absoluto = os.path.join(raiz, a)
            rel = os.path.relpath(absoluto, pasta)
            if _ignorar(rel):
                continue
            saida.append((absoluto, rel.replace("\\", "/")))
    return sorted(saida, key=lambda x: x[1])


def conferir_nome(nome):
    """(ok, valor_encontrado). O name: do frontmatter tem de bater com a pasta."""
    caminho = os.path.join(SKILLS, nome, "SKILL.md")
    try:
        with open(caminho, encoding="utf-8-sig") as f:
            texto = f.read()
    except OSError as e:
        return False, "erro ao ler: %s" % e
    m = re.search(r"^name:\s*(.+?)\s*$", texto, re.M)
    if not m:
        return False, "(sem campo name: no frontmatter)"
    return m.group(1) == nome, m.group(1)


def procurar_caminhos_locais(nome):
    """Ocorrências de caminho da máquina local. Lista vazia = limpo."""
    achados = []
    for absoluto, rel in arquivos_da_skill(nome):
        if not rel.endswith(EXTENSOES_VARRIDAS):
            continue
        try:
            with open(absoluto, encoding="utf-8-sig") as f:
                linhas = f.readlines()
        except (OSError, UnicodeDecodeError):
            continue
        for n, linha in enumerate(linhas, 1):
            for padrao, rotulo in PADROES_LOCAIS:
                if re.search(padrao, linha):
                    achados.append((rel, n, rotulo, linha.strip()[:100]))
                    break
    return achados


def empacotar(nome, destino):
    saida = os.path.join(destino, "skill-%s.zip" % nome)
    arquivos = arquivos_da_skill(nome)
    # A pasta da skill vai DENTRO do zip: é o formato que o upload espera, e o
    # nome dela precisa ser igual ao name: do frontmatter (já conferido acima).
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as z:
        for absoluto, rel in arquivos:
            z.write(absoluto, "%s/%s" % (nome, rel))
    return saida, ["%s/%s" % (nome, rel) for _, rel in arquivos]


def main():
    p = argparse.ArgumentParser(description="Empacota as skills do projeto em .zip.")
    p.add_argument("skills", nargs="*", help="nomes a empacotar (padrão: todas)")
    p.add_argument("--destino", default=DESTINO_PADRAO,
                   help="pasta onde salvar os zips (padrão: %(default)s)")
    args = p.parse_args()

    todas = listar_skills()
    if not todas:
        print("Nenhuma skill encontrada em %s" % SKILLS)
        return 1

    alvos = args.skills or todas
    desconhecidas = [s for s in alvos if s not in todas]
    if desconhecidas:
        print("Skill(s) inexistente(s): %s" % ", ".join(desconhecidas))
        print("Disponíveis: %s" % ", ".join(todas))
        return 1

    print("== 1. frontmatter name: x nome da pasta ==")
    falhas_nome = []
    for s in alvos:
        ok, valor = conferir_nome(s)
        print("   %-28s name: %-28s %s" % (s, valor, "ok" if ok else "<<< DIVERGE"))
        if not ok:
            falhas_nome.append(s)

    print()
    print("== 2. caminhos da máquina local ==")
    falhas_caminho = {}
    for s in alvos:
        achados = procurar_caminhos_locais(s)
        if achados:
            falhas_caminho[s] = achados
            print("   %-28s %d ocorrência(s)" % (s, len(achados)))
            for rel, linha, rotulo, trecho in achados:
                print("      %s:%d  [%s]" % (rel, linha, rotulo))
                print("         %s" % trecho)
        else:
            print("   %-28s limpo" % s)

    if falhas_nome or falhas_caminho:
        print()
        print("PAROU - nenhum zip foi gerado.")
        if falhas_nome:
            print("  Corrija o name: do frontmatter (ou renomeie a pasta): %s"
                  % ", ".join(falhas_nome))
        if falhas_caminho:
            print("  Troque os caminhos locais por caminho relativo ou por uma")
            print("  instrucao generica (ex.: \"a pasta que o usuario indicar\") em: %s"
                  % ", ".join(falhas_caminho))
        return 1

    if not os.path.isdir(args.destino):
        os.makedirs(args.destino)

    print()
    print("== 3. zips gerados em %s ==" % args.destino)
    for s in alvos:
        saida, itens = empacotar(s, args.destino)
        kb = os.path.getsize(saida) / 1024.0
        print()
        print("   %s  (%.1f KB, %d arquivo(s))" % (os.path.basename(saida), kb, len(itens)))
        for i in itens:
            print("      %s" % i)

    print()
    print("Pronto. Subir em: Personalizar > Skills > + > Criar skill > Enviar uma skill.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
