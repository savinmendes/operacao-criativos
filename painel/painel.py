"""Painel ao vivo: grava o andamento das tarefas em status.json (lido pelo index.html).

Uso (qualquer agente, de qualquer pasta):
  python painel/painel.py etapa kit1 "Kit 1 Yara" --texto "gerando bloco Yara Moi" --k 3 --n 6
  ... img kit1 <url-ou-arquivo-local> --legenda "Yara Moi"
  ... custo kit1 0.11            (soma ao custo da tarefa, em US$)
  ... link kit1 "Rascunho Shopify" https://admin.shopify.com/...
  ... fim kit1 [--erro "motivo"] [--aguardando "o que falta decidir"]
  ... limpar                      (remove tarefas prontas há mais de 24 h)
  ... pedido "texto"              (nome do pedido mais recente da pessoa: vira o título da aba e o topo do painel)
"""
import argparse, json, os, shutil, sys, time, hashlib
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
ARQ = RAIZ / "status.json"
IMG = RAIZ / "img"


def ler():
    try:
        return json.loads(ARQ.read_text(encoding="utf-8"))
    except Exception:
        return {"tarefas": {}}


def gravar(d):
    d["atualizado"] = time.time()
    tmp = ARQ.with_suffix(".tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, ARQ)


def tarefa(d, tid, titulo=None):
    t = d["tarefas"].setdefault(tid, {"titulo": titulo or tid, "estado": "rodando", "inicio": time.time(),
                                      "etapa": "", "k": 0, "n": 0, "custo": 0.0, "imagens": [], "links": [], "log": []})
    if titulo:
        t["titulo"] = titulo
    return t


def logar(t, msg):
    t["log"] = (t.get("log", []) + [[time.time(), msg]])[-10:]


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("etapa"); e.add_argument("id"); e.add_argument("titulo", nargs="?")
    e.add_argument("--texto", default=""); e.add_argument("--k", type=int); e.add_argument("--n", type=int)
    i = sub.add_parser("img"); i.add_argument("id"); i.add_argument("src"); i.add_argument("--legenda", default="")
    c = sub.add_parser("custo"); c.add_argument("id"); c.add_argument("valor", type=float)
    l = sub.add_parser("link"); l.add_argument("id"); l.add_argument("rotulo"); l.add_argument("url")
    f = sub.add_parser("fim"); f.add_argument("id"); f.add_argument("--erro"); f.add_argument("--aguardando")
    sub.add_parser("limpar")
    pd = sub.add_parser("pedido"); pd.add_argument("texto")
    a = ap.parse_args()
    d = ler()

    if a.cmd == "pedido":
        d["pedido"] = {"texto": a.texto, "desde": time.time()}
        gravar(d); return

    if a.cmd == "limpar":
        agora = time.time()
        d["tarefas"] = {k: v for k, v in d["tarefas"].items()
                        if not (v.get("estado") == "pronto" and agora - v.get("fim", agora) > 86400)}
        gravar(d); return

    t = tarefa(d, a.id, getattr(a, "titulo", None))
    if a.cmd == "etapa":
        t["estado"] = "rodando"
        t["etapa"] = a.texto
        if a.k is not None: t["k"] = a.k
        if a.n is not None: t["n"] = a.n
        logar(t, a.texto)
    elif a.cmd == "img":
        src = a.src
        if not src.startswith("http"):
            p = Path(src)
            if p.exists():
                IMG.mkdir(exist_ok=True)
                nome = hashlib.md5(str(p.resolve()).encode()).hexdigest()[:10] + p.suffix.lower()
                shutil.copy2(p, IMG / nome)
                src = "img/" + nome
        t["imagens"] = (t.get("imagens", []) + [{"src": src, "legenda": a.legenda}])[-24:]
        logar(t, "imagem: " + (a.legenda or "nova"))
    elif a.cmd == "custo":
        t["custo"] = round(t.get("custo", 0) + a.valor, 4)
    elif a.cmd == "link":
        t["links"] = [x for x in t.get("links", []) if x["rotulo"] != a.rotulo] + [{"rotulo": a.rotulo, "url": a.url}]
    elif a.cmd == "fim":
        t["fim"] = time.time()
        if a.erro:
            t["estado"], t["etapa"] = "erro", a.erro
        elif a.aguardando:
            t["estado"], t["etapa"] = "aguardando", a.aguardando
        else:
            t["estado"] = "pronto"
            if t.get("n"): t["k"] = t["n"]
        logar(t, t["estado"] + (": " + t["etapa"] if t["estado"] != "pronto" else ""))
    gravar(d)


if __name__ == "__main__":
    sys.exit(main())
