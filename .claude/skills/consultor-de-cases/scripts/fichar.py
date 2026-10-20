# -*- coding: utf-8 -*-
"""Extração automática da parte mecânica de uma ficha de case.

A ideia: tudo que dá para extrair sem julgamento sai daqui de graça e em
segundos — metadados, resumo de abertura, números declarados, menções, e um
mapa de fatias para leitura. O que exige julgamento (o que é tática replicável,
o que é anedota, o que não transfere entre frentes de negócio) fica para a
leitura guiada pela SKILL.md.

Uso:
    python fichar.py <transcricao.md> [--partes N] [--saida ficha.md]
    python fichar.py <pasta/> --lote            # esqueleto de todas de uma vez
"""
import argparse
import io
import os
import re
import sys
from collections import OrderedDict

# ---------------------------------------------------------------- tempo/parse

_RE_BLOCO = re.compile(r"^\*\*\[([0-9:]+)\]\*\*\s*(.*)$")


def tempo_para_segundos(t):
    """'01:15' -> 75 · '1:02:05' -> 3725 · lixo -> None."""
    if not t:
        return None
    partes = str(t).strip().split(":")
    if not all(p.isdigit() for p in partes) or not 2 <= len(partes) <= 3:
        return None
    partes = [int(p) for p in partes]
    if len(partes) == 2:
        return partes[0] * 60 + partes[1]
    return partes[0] * 3600 + partes[1] * 60 + partes[2]


def ler_metadados(texto):
    """Lê o título e a tabela de procedência do topo da transcrição."""
    m = {"titulo": None, "canal": None, "duracao": None, "publicado": None,
         "url": None, "origem": None}
    for linha in (texto or "").splitlines():
        if m["titulo"] is None and linha.startswith("# "):
            m["titulo"] = linha[2:].strip()
            continue
        if not linha.startswith("|"):
            continue
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        if len(celulas) < 2:
            continue
        chave, valor = celulas[0].lower(), celulas[1]
        if not valor or set(valor) <= set("-: "):
            continue
        if "canal" in chave:
            m["canal"] = valor
        elif "dura" in chave:
            m["duracao"] = valor
        elif "public" in chave:
            m["publicado"] = valor
        elif chave == "url":
            m["url"] = valor
        elif "origem" in chave:
            m["origem"] = valor
    return m


def blocos(texto):
    """Transcrição -> [{seg, tempo, texto}] na ordem do vídeo."""
    saida = []
    for linha in (texto or "").splitlines():
        m = _RE_BLOCO.match(linha.strip())
        if not m:
            continue
        seg = tempo_para_segundos(m.group(1))
        if seg is None:
            continue
        saida.append({"seg": seg, "tempo": m.group(1), "texto": m.group(2).strip()})
    return saida


# ------------------------------------------------------- resumo de abertura

# Praticamente todo episódio de podcast abre com o host resumindo o que o
# convidado vai cobrir, e só depois começa a conversa. Esse trecho é um resumo
# pronto, escrito por quem viu o episódio inteiro, e sai de graça.
_MARCAS_INICIO = [
    "vamos começar", "vamos começo", "bora pro podcast", "bora pro episódio",
    "chega de conversa", "com vocês,", "seja muito bem-vindo", "seja bem-vindo",
    "vamos para o podcast", "começar logo o podcast",
]


def resumo_de_abertura(bs, teto=12):
    """Blocos até a marca de 'começou a conversa', limitado a `teto`."""
    if not bs:
        return []
    for i, b in enumerate(bs[:teto]):
        baixo = (b.get("texto") or "").lower()
        if any(marca in baixo for marca in _MARCAS_INICIO):
            return bs[:i]
    return bs[:teto]


# ------------------------------------------------------- números declarados

# A legenda automática destrói termos técnicos. "ROAS" aparece como ruas, rost,
# RAS, Ross, rus. Sem cobrir isso, perde-se justamente a métrica mais citada.
_ROAS = r"(?:roas|roi|r[ou]as|rost|r[áa]s\b|ross|rus)"

_PADROES = [
    # dinheiro
    re.compile(r"R?\$?\s?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?\s*(?:mil|milh[õo]es|milh[ãa]o|k|bi|bilh[õo]es)\b", re.I),
    re.compile(r"R\$\s?\d[\d.,]*", re.I),
    # volume por período
    re.compile(r"\d[\d.,]*\s*k?\s*(?:por|no|ao|\/)\s*(?:dia|m[êe]s|ano|semana)", re.I),
    re.compile(r"\d[\d.,]*\s*k\s*(?:dia|m[êe]s)\b", re.I),
    # percentual
    re.compile(r"\d[\d.,]*\s*%", re.I),
    # dígitos (sete dígitos, nove dígitos)
    re.compile(r"(?:m[úu]ltiplos\s+)?(?:seis|sete|oito|nove)\s+d[íi]gitos", re.I),
    # métricas com nome
    # o número nem sempre encosta na métrica: "o ROAS caiu para 1.2"
    re.compile(_ROAS + r"[^.!?\n]{0,25}?\d[\d.,]*", re.I),
    re.compile(r"\d[\d.,]*\s*(?:de\s*)?" + _ROAS, re.I),
    re.compile(_ROAS + r"\s+(?:um|dois|tr[êe]s|quatro|cinco)\b", re.I),
    re.compile(r"(?:ticket|cpm|cpc|cpa|ctr|connect\s*rate|play\s*rate|convers[ãa]o|reten[çc][ãa]o)"
               r"[^.!?\n]{0,25}?\d[\d.,]*\s*%?", re.I),
    re.compile(r"\d[\d.,]*\s*%?[^.!?\n]{0,12}?(?:de\s+)?(?:convers[ãa]o|reten[çc][ãa]o|ticket|margem)", re.I),
]

# "3 filhos", "2 cachorros" e afins não são declaração de resultado.
_RUIDO = re.compile(r"^\d{1,2}\s*(?:filhos?|cachorros?|anos?|horas?|dias?|meses|pessoas?|vezes)$", re.I)


def numeros_declarados(bs):
    """Acha declarações de resultado, cada uma com o timestamp de origem.

    Vários padrões casam o mesmo pedaço de texto — "100k" e "100k por dia" saem
    dos dois. Por isso a resolução é por sobreposição de posição, e não por
    igualdade de string: o match mais longo ganha e engole os menores. Sem isso
    a tabela de números sai com a mesma declaração repetida em três formatos.
    """
    saida = []
    for b in bs or []:
        texto = b.get("texto") or ""
        achados = []
        for p in _PADROES:
            for m in p.finditer(texto):
                achados.append((m.start(), m.end()))
        achados.sort(key=lambda x: (-(x[1] - x[0]), x[0]))   # mais longo primeiro

        aceitos = []
        for ini, fim in achados:
            if any(ini < f and fim > i for i, f in aceitos):
                continue
            trecho = re.sub(r"\s+", " ", texto[ini:fim]).strip(" ,.;:")
            if not trecho or _RUIDO.match(trecho):
                continue
            aceitos.append((ini, fim))

        # o host costuma repetir de volta o número que o convidado acabou de
        # dizer; dentro do mesmo bloco isso é uma declaração só, não duas
        ja_no_bloco = set()
        for ini, fim in sorted(aceitos):                      # volta à ordem de leitura
            trecho = re.sub(r"\s+", " ", texto[ini:fim]).strip(" ,.;:")
            if trecho.lower() in ja_no_bloco:
                continue
            ja_no_bloco.add(trecho.lower())
            c0, c1 = max(0, ini - 70), min(len(texto), fim + 70)
            saida.append({
                "tempo": b.get("tempo"), "seg": b.get("seg"),
                "trecho": trecho,
                "contexto": re.sub(r"\s+", " ", texto[c0:c1]).strip(),
            })
    return saida


# ------------------------------------------------------------------ menções

_RE_LIVRO = re.compile(
    r"livro\s+(?:chamado|que\s+se\s+chama|do|da)?\s*([A-ZÀ-Ú][\wÀ-ú'’]*(?:\s+(?:de|do|da|dos|das|e|of|the|to|for)?\s*[A-ZÀ-Ú0-9][\wÀ-ú'’]*){0,5})")

_FERRAMENTAS = [
    "meta ads", "facebook ads", "google ads", "tiktok ads", "kwai", "youtube ads",
    "hotmart", "kiwify", "eduzz", "digistore", "stripe", "braip", "monetizze",
    "shopify", "clickfunnels", "notion", "typeform", "manychat", "whatsapp",
    "instagram", "zapier", "make", "n8n",
]


def mencoes(bs):
    """Livros e ferramentas citados, com timestamp — bom rastro de repertório."""
    livros, ferramentas = OrderedDict(), OrderedDict()
    for b in bs or []:
        texto = b.get("texto") or ""
        for m in _RE_LIVRO.finditer(texto):
            nome = m.group(1).strip(" ,.;:")
            if len(nome) > 2 and nome.lower() not in livros:
                livros[nome.lower()] = {"nome": nome, "tempo": b.get("tempo")}
        baixo = texto.lower()
        for f in _FERRAMENTAS:
            if f in baixo and f not in ferramentas:
                ferramentas[f] = {"nome": f, "tempo": b.get("tempo")}
    return {"livros": list(livros.values()), "ferramentas": list(ferramentas.values())}


# ------------------------------------------------------------------- fatias

def fatiar(bs, partes):
    """Divide os blocos em N fatias com faixa de tempo — mapa para leitura."""
    if not bs:
        return []
    partes = max(1, min(partes, len(bs)))
    tam = -(-len(bs) // partes)          # teto da divisão
    saida = []
    for i in range(0, len(bs), tam):
        pedaco = bs[i:i + tam]
        saida.append({
            "n": len(saida) + 1,
            "inicio": pedaco[0]["tempo"], "fim": pedaco[-1]["tempo"],
            "inicio_seg": pedaco[0]["seg"], "fim_seg": pedaco[-1]["seg"],
            "linha_inicio": i + 1, "linha_fim": i + len(pedaco),
            "blocos": pedaco,
        })
    return saida


# -------------------------------------------------------------- esqueleto md

def esqueleto(caminho, partes=6):
    texto = io.open(caminho, encoding="utf-8").read()
    meta = ler_metadados(texto)
    bs = blocos(texto)
    abertura = resumo_de_abertura(bs)
    nums = numeros_declarados(bs)
    men = mencoes(bs)
    fatias = fatiar(bs, partes)

    L = []
    L.append("---")
    L.append("fonte: %s" % (meta["canal"] or "?"))
    L.append("titulo: %s" % (meta["titulo"] or os.path.basename(caminho)))
    L.append("url: %s" % (meta["url"] or "?"))
    L.append("publicado: %s" % (meta["publicado"] or "?"))
    L.append("duracao: %s" % (meta["duracao"] or "?"))
    L.append("origem_transcricao: %s" % (meta["origem"] or "?"))
    L.append("transcricao: %s" % os.path.basename(caminho))
    L.append("confiabilidade: declarado-nao-verificado")
    L.append("status: ESQUELETO — precisa do passe de leitura")
    L.append("---")
    L.append("")
    L.append("# Ficha: %s" % (meta["titulo"] or "?"))
    L.append("")
    L.append("> Gerado automaticamente por `fichar.py`. As seções marcadas com")
    L.append("> `[PREENCHER]` exigem leitura e julgamento — veja a SKILL.md.")
    L.append("")

    L.append("## Resumo de abertura (palavras do próprio host)")
    L.append("")
    if abertura:
        for b in abertura:
            L.append("**[%s]** %s" % (b["tempo"], b["texto"]))
            L.append("")
    else:
        L.append("_não identificado_")
        L.append("")

    L.append("## Quem é / contexto")
    L.append("")
    L.append("[PREENCHER]")
    L.append("")
    L.append("## Modelo de negócio")
    L.append("")
    L.append("[PREENCHER]")
    L.append("")
    L.append("## Frentes a que se aplica")
    L.append("")
    L.append("[PREENCHER — marque só as que de fato transferem, e diga por quê]")
    L.append("")

    L.append("## Números declarados (extraídos automaticamente)")
    L.append("")
    L.append("> Declarações do entrevistado, sem verificação independente.")
    L.append("")
    if nums:
        L.append("| Tempo | Trecho | Contexto |")
        L.append("|---|---|---|")
        for n in nums[:120]:
            ctx = n["contexto"].replace("|", "/")[:150]
            L.append("| %s | %s | %s |" % (n["tempo"], n["trecho"].replace("|", "/"), ctx))
        if len(nums) > 120:
            L.append("")
            L.append("_(%d ocorrências no total; listadas as 120 primeiras)_" % len(nums))
    else:
        L.append("_nenhum número detectado_")
    L.append("")

    L.append("## Táticas replicáveis")
    L.append("")
    L.append("[PREENCHER — tabela: tática | quando usar | timestamp]")
    L.append("")
    L.append("## Erros, fracassos e contra-exemplos")
    L.append("")
    L.append("[PREENCHER — o que deu errado, o que ele admite ter feito mal,")
    L.append("onde contradiz outro case. Esta seção é obrigatória: sem ela a")
    L.append("base vira máquina de confirmar o que já se pensava.]")
    L.append("")
    L.append("## Limites — onde NÃO se aplica")
    L.append("")
    L.append("[PREENCHER — pressupostos do case que podem não valer em outra frente]")
    L.append("")

    L.append("## Menções")
    L.append("")
    if men["livros"]:
        L.append("**Livros:** " + " · ".join("%s [%s]" % (x["nome"], x["tempo"]) for x in men["livros"]))
        L.append("")
    if men["ferramentas"]:
        L.append("**Ferramentas:** " + " · ".join(x["nome"] for x in men["ferramentas"]))
        L.append("")
    if not men["livros"] and not men["ferramentas"]:
        L.append("_nenhuma_")
        L.append("")

    L.append("## Mapa de leitura")
    L.append("")
    L.append("| Fatia | De | Até | Linhas |")
    L.append("|---|---|---|---|")
    for f in fatias:
        L.append("| %d | %s | %s | %d-%d |" % (f["n"], f["inicio"], f["fim"],
                                               f["linha_inicio"], f["linha_fim"]))
    L.append("")
    L.append("## Citações-chave")
    L.append("")
    L.append("[PREENCHER — curtas, sempre com timestamp]")
    L.append("")
    return "\n".join(L)


def main():
    p = argparse.ArgumentParser(description="Gera o esqueleto da ficha de um case.")
    p.add_argument("caminho", help="arquivo .md de transcrição, ou pasta com --lote")
    p.add_argument("--partes", type=int, default=6, help="fatias do mapa de leitura")
    p.add_argument("--saida", help="arquivo de saída (padrão: _fichas/<nome>.md)")
    p.add_argument("--lote", action="store_true", help="processa a pasta inteira")
    a = p.parse_args()

    alvos = []
    if a.lote:
        if not os.path.isdir(a.caminho):
            print("--lote exige uma pasta"); return 1
        for n in sorted(os.listdir(a.caminho)):
            if n.lower().endswith(".md") and not n.startswith("_"):
                alvos.append(os.path.join(a.caminho, n))
    else:
        alvos = [a.caminho]

    base = a.caminho if a.lote else os.path.dirname(os.path.abspath(a.caminho))
    destino = os.path.join(base, "_fichas")
    os.makedirs(destino, exist_ok=True)

    for c in alvos:
        saida = a.saida if (a.saida and not a.lote) else \
            os.path.join(destino, os.path.splitext(os.path.basename(c))[0] + ".ficha.md")
        if os.path.exists(saida):
            print("PULADO (já existe): %s" % os.path.basename(saida))
            continue
        io.open(saida, "w", encoding="utf-8").write(esqueleto(c, a.partes))
        print("OK: %s" % saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
