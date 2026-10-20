# -*- coding: utf-8 -*-
"""Parte B do v2 (ADs 12, 13, 19, 22). Cópia adaptada de encaixar_v2.py + montar_v2.py (não mexe nos arquivos
da parte A: tudo que este script grava leva o sufixo _v2b / _b).

  python parteb_v2_b.py encaixar ad12 [ad13 ...]   -> flora/tN_final_b.mp4 (encaixar_edit corrigido, mesmos args)
  python parteb_v2_b.py montar   ad12 [ad13 ...]   -> _v2_corrigidos/<nome entregue> v2.mp4

Takes refeitos = só os da auditoria. AD 19 t2 NÃO é refeito (é um flash do original, não é defeito): entra o
mesmo t2_final.mp4 do AD entregue. Takes/extras fora da lista entram com o arquivo do AD entregue (_trabalho).
Caminho de montagem = o do AD entregue (processar_ad.py, log_rNN.txt): substituir_trechos -> blur -> textos ->
(áudios: só mexem no áudio, -c:v copy) -> montar_fim_universal (receita_final.json -> montar_ad.py).
O áudio da parte 1 é copiado sem reencode da parte1.mp4 entregue.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config_v2 import OLD, V2, KIT, SAIDA, _receita, _etapas_receita, _dur  # noqa: E402

ENV = dict(os.environ, PYTHONIOENCODING="utf-8")

# AD 12: o 1º quadro do flora/cobre_tela.mp4 (extra que cobre a tela do celular em 218.87s) NÃO está coberto:
# mostra o site "MAYAVERRA" por 1 quadro. No entregue o encode a 900 kbps borrou esse quadro; no v2 ele saía nítido.
# cobre_tela_b.mp4 = mesmo clipe com o 1º quadro trocado pelo 2º (gerado com ffmpeg, ver RELATORIO-V2 Parte B).
PATCH = {"ad12": {"flora/cobre_tela.mp4"}}

FIX = {"ad12": {"t1", "t2"}, "ad13": {"t1", "t2", "t4", "t5"}, "ad19": {"t1", "t3", "t4"}, "ad22": {"t2"}}


def cfg(ad):
    r = _receita(ad[2:])
    ref = {}
    for t in r["takes"]:
        nome = Path(t["orig"]).stem
        if nome in FIX[ad]:
            ref[f"flora/{nome}_final.mp4"] = (t["orig"], f"flora/{nome}_edit.mp4", _dur(t["quadros"]))
    return dict(saida=r["saida"], base="base.mp4", hook_old="parte1.mp4", refazer=ref, etapas=_etapas_receita(r))


def b_name(clip):
    p = Path(clip)
    return (p.parent / (p.stem + "_b.mp4")).as_posix()


def run(*a):
    a = [str(x) for x in a]
    print(">>", " ".join(Path(x).name if "\\" in x else x for x in a[1:6]), flush=True)
    subprocess.run(a, check=True, env=ENV)


def py(tool, *a):
    run(sys.executable, KIT / tool, *a)


def nq(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-count_packets", "-show_entries",
                        "stream=nb_read_packets", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return int(r.stdout.strip())


def pts_idx(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "frame=pts_time",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return sorted(int(round(float(x.split(",")[0]) * 30)) for x in r.stdout.split() if x.split(",")[0])


def copiar(ad):
    """Igual ao encaixar_v2.copiar: só copia o que ainda não existe."""
    src, dst = OLD / ad, V2 / ad
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        if f.is_file() and not (f.suffix.lower() == ".mp4" and f.name not in {"base.mp4", "parte2.mp4"}):
            if not (dst / f.name).exists():
                shutil.copy2(f, dst / f.name)
    for sub in ("flora", "flora2"):
        if (src / sub).is_dir():
            (dst / sub).mkdir(exist_ok=True)
            for f in (src / sub).iterdir():
                if f.is_file() and not (dst / sub / f.name).exists():
                    shutil.copy2(f, dst / sub / f.name)


def encaixar(ad):
    c = cfg(ad)
    P = V2 / ad
    copiar(ad)
    for clip, (orig, edit, dur) in c["refazer"].items():
        for f in (orig, edit):           # entradas têm de ser as mesmas do lote antigo
            assert (P / f).stat().st_size == (OLD / ad / f).stat().st_size, f
        py("encaixar_edit.py", P / orig, P / edit, P / b_name(clip), "--dur", dur)


def montar(ad):
    c = cfg(ad)
    P = V2 / ad
    etapa = 0

    def prox():
        nonlocal etapa
        etapa += 1
        return P / f"v2b_b{etapa}.mp4"

    tre = json.load(open(OLD / ad / "trechos.json", encoding="utf-8-sig"))
    for t in tre:
        rel = Path(t["clipe"]).relative_to(OLD / ad).as_posix()
        t["clipe"] = str(P / b_name(rel)) if rel in c["refazer"] else str(OLD / ad / rel)
        if rel in PATCH.get(ad, ()):           # extra com defeito próprio (ver PATCH)
            t["clipe"] = str(P / b_name(rel))
        assert Path(t["clipe"]).exists(), t["clipe"]
        print("  trecho", rel, "->", "REFEITO" if rel in c["refazer"] else "igual ao entregue", flush=True)
    (P / "trechos_v2b.json").write_text(json.dumps(tre, ensure_ascii=False), encoding="utf-8")
    cur = prox()
    py("substituir_trechos.py", P / c["base"], cur, P / "trechos_v2b.json")
    for tipo, e in c["etapas"]:
        o = prox()
        if tipo == "blur":
            py("desfocar_regioes.py", cur, o, "--de", e["de"], "--ate", e["ate"], "--caixas", e["caixas"])
        else:
            a = ["--de", e["de"], "--ate", e["ate"], "--caixa", e["caixa"], "--texto", e["texto"]]
            for k in ("ref", "px", "contorno", "fonte"):
                if k in e:
                    a += [f"--{k}", e[k]]
            if e.get("maiusc"):
                a.append("--maiusc")
            py("trocar_texto_tela.py", cur, o, *a)
        cur = o
    hook = P / "parte1_v2b.mp4"
    # No lote antigo o "-shortest" das passadas cortou quadros do FIM da parte 1 em alguns ADs (AD 12: 1, AD 19: 2,
    # AD 22: 3). A cópia do kit em _v2_trabalho/kit não tem "-shortest", então aqui a parte 1 é cortada no mesmo
    # nº de quadros da parte1.mp4 entregue (corte no fim; o início fica alinhado quadro a quadro).
    n_old = nq(OLD / ad / c["hook_old"])
    if nq(cur) == n_old:
        run("ffmpeg", "-v", "error", "-y", "-i", cur, "-i", OLD / ad / c["hook_old"], "-map", "0:v", "-map", "1:a",
            "-c", "copy", hook)
    else:
        print(f"  parte 1: {nq(cur)} quadros -> cortando para {n_old} (igual à entregue)", flush=True)
        so_v = P / "parte1_v2b_video.mp4"     # 1º só o vídeo (-frames:v também cortaria o áudio)
        idx = pts_idx(OLD / ad / c["hook_old"])
        falta = sorted(set(range(idx[-1] + 1)) - set(idx))
        if not falta:                          # entregue = primeiros N quadros, contínuos
            run("ffmpeg", "-v", "error", "-y", "-i", cur, "-map", "0:v", "-frames:v", n_old, "-c:v", "libx264",
                "-threads", "4", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", so_v)
        else:                                  # entregue tem buraco no PTS (quadro descartado no meio): igual
            print(f"  parte 1 entregue sem os quadros {falta} (PTS com buraco): reproduzindo", flush=True)
            expr = f"lte(n\\,{idx[-1]})" + "".join(f"*not(eq(n\\,{k}))" for k in falta)
            run("ffmpeg", "-v", "error", "-y", "-i", cur, "-map", "0:v", "-vf", f"select={expr}",
                "-fps_mode", "passthrough", "-c:v", "libx264", "-threads", "4", "-crf", "15", "-preset", "medium",
                "-pix_fmt", "yuv420p", so_v)
            assert pts_idx(so_v) == idx, "PTS da parte 1 v2 diferente da entregue"
        run("ffmpeg", "-v", "error", "-y", "-i", so_v, "-i", OLD / ad / c["hook_old"], "-map", "0:v", "-map", "1:a",
            "-c", "copy", hook)
    assert nq(hook) == n_old, (nq(hook), n_old)
    md5 = lambda p: subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-map", "0:a", "-c", "copy", "-f", "md5",  # noqa: E731
                                    "-"], capture_output=True, text=True).stdout.strip()
    assert md5(hook) == md5(OLD / ad / c["hook_old"]), "áudio da parte 1 diferente"
    rec = json.load(open(OLD / ad / "receita_final.json", encoding="utf-8-sig"))
    rec["hook"]["video"] = str(hook)
    rec["legenda"]["fonte"] = rec["legenda"]["fonte"].replace(str(OLD / ad), str(P))
    assert Path(rec["legenda"]["fonte"].split(":", 1)[1]).exists()
    assert (P / rec["corpo"]).stat().st_size == (OLD / ad / rec["corpo"]).stat().st_size
    saida = SAIDA / (Path(c["saida"]).stem + " v2.mp4")
    rec["saida"] = str(saida)
    (P / "receita_final_v2b.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    run(sys.executable, KIT / "montar_ad.py", P / "receita_final_v2b.json")
    print("PRONTO", saida, flush=True)


if __name__ == "__main__":
    acao = sys.argv[1]
    for ad in sys.argv[2:]:
        {"encaixar": encaixar, "montar": montar}[acao](ad)
