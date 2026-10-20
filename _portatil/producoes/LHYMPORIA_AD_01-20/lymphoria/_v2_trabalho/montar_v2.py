# -*- coding: utf-8 -*-
"""Passo 2 do v2: refaz a parte 1 com os takes re-encaixados (mesmos passos e mesma ordem do AD entregue)
e remonta o AD final com a mesma receita_final.json (só os caminhos trocados para _v2_trabalho/_v2_corrigidos).

  python montar_v2.py ad01 [ad09 ...]
- Etapas de vídeo refeitas: substituir_trechos -> desfocar_regioes -> trocar_texto_tela -> (remendo).
- Áudio da parte 1: copiado sem reencode da parte 1 do AD entregue (as etapas de áudio só mexiam no áudio
  e copiavam o vídeo), então o áudio fica idêntico.
- parte2.mp4 (fim universal): a mesma do AD entregue (copiada).
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config_v2 import ADS, OLD, V2, KIT, SAIDA  # noqa: E402

ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def run(*a):
    a = [str(x) for x in a]
    print(">>", " ".join(Path(x).name if "\\" in x else x for x in a[1:6]), flush=True)
    subprocess.run(a, check=True, env=ENV)


def py(tool, *a):
    o = Path(str(a[1]))
    if REUSAR and o.exists():          # retomada: reaproveita a etapa já feita
        print("(reaproveitado)", o.name, flush=True)
        return
    run(sys.executable, KIT / tool, *a)


REUSAR = bool(os.environ.get("V2_REUSAR"))


def n_quadros(p):
    return int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-count_packets", "-show_entries",
                               "stream=nb_read_packets", "-of", "csv=p=0", str(p)], capture_output=True,
                              text=True).stdout.strip())


def v2_path(ad, p):
    rel = Path(p).relative_to(OLD / ad)
    return V2 / ad / rel


def processar(ad):
    cfg = ADS[ad]
    P = V2 / ad
    etapa = 0

    def prox():
        nonlocal etapa
        etapa += 1
        return P / f"v2_b{etapa}.mp4"

    # 1) encaixe dos takes na base (mesmo trechos.json, takes com defeito trocados pelos re-encaixados)
    tre = json.load(open(OLD / ad / "trechos.json", encoding="utf-8-sig"))
    for t in tre:
        t["clipe"] = str(v2_path(ad, t["clipe"]))
        assert Path(t["clipe"]).exists(), t["clipe"]
    (P / "trechos_v2.json").write_text(json.dumps(tre, ensure_ascii=False), encoding="utf-8")
    cur = prox()
    py("substituir_trechos.py", P / cfg["base"], cur, P / "trechos_v2.json")
    # 2) etapas de vídeo, na ordem original
    for tipo, e in cfg["etapas"]:
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
    # 3) remendo feito depois na parte 1 pronta (remendar_ad.py)
    if cfg.get("remendo"):
        r = cfg["remendo"]
        (P / "trechos_remendo_v2.json").write_text(json.dumps(
            [{"clipe": str(P / r["clipe"]), "inicio": r["inicio"], "quadros": r["quadros"]}]), encoding="utf-8")
        o = prox()
        py("substituir_trechos.py", cur, o, P / "trechos_remendo_v2.json")
        cur = o
    # 4) parte 1 v2 = vídeo novo + áudio da parte 1 entregue (sem reencode)
    hook = P / cfg["hook_old"]
    # no lote original o "-shortest" das etapas cortava quadros do fim quando o áudio ficava mais curto;
    # aqui o vídeo é cortado no mesmo nº de quadros da parte 1 entregue (cópia, sem reencode)
    nq = n_quadros(OLD / ad / cfg["hook_old"])
    assert n_quadros(cur) >= nq, (n_quadros(cur), nq)
    vid = cur
    if n_quadros(cur) != nq:
        # corte só do vídeo, recodificação SEM PERDA (qp 0): copiar pacotes com quadros B não corta no quadro exato,
        # e -frames:v junto com o áudio cortaria o áudio também
        vid = P / "v2_parte1_so_video.mp4"
        run("ffmpeg", "-v", "error", "-y", "-i", cur, "-map", "0:v", "-frames:v", nq, "-c:v", "libx264", "-threads",
            "4", "-qp", "0", "-preset", "veryfast", "-pix_fmt", "yuv420p", vid)
    run("ffmpeg", "-v", "error", "-y", "-i", vid, "-i", OLD / ad / cfg["hook_old"], "-map", "0:v", "-map", "1:a",
        "-c", "copy", hook)
    md5 = lambda x: subprocess.run(["ffmpeg", "-v", "error", "-i", str(x), "-map", "0:a", "-c", "copy", "-f", "md5", "-"],  # noqa: E731
                                   capture_output=True, text=True).stdout.strip()
    assert md5(hook) == md5(OLD / ad / cfg["hook_old"]), "áudio da parte 1 diferente do entregue"
    assert n_quadros(hook) == nq
    # 5) remonta com a mesma receita final
    rec = json.load(open(OLD / ad / "receita_final.json", encoding="utf-8-sig"))
    old_dir, new_dir = str(OLD / ad), str(V2 / ad)
    rec["hook"]["video"] = rec["hook"]["video"].replace(old_dir, new_dir)
    rec["legenda"]["fonte"] = rec["legenda"]["fonte"].replace(old_dir, new_dir)
    if not Path(rec["hook"]["video"]).is_absolute():
        rec["hook"]["video"] = str(P / rec["hook"]["video"])
    assert Path(rec["hook"]["video"]) == hook, rec["hook"]["video"]
    saida = SAIDA / (Path(cfg["saida"]).stem + " v2.mp4")
    rec["saida"] = str(saida)
    (P / "receita_final_v2.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    a = [KIT / "montar_ad.py", P / "receita_final_v2.json"]
    if cfg.get("classico"):
        a.append("--classico")
    run(sys.executable, *a)
    print("PRONTO", saida, flush=True)


if __name__ == "__main__":
    # divisão de trabalho (05/10): ADs listados em _pular_lote_agente1.txt ficam com outro agente; o lote em
    # andamento deste agente sai com erro para não rodar o revisar_v2 nem sobrescrever nada desses ADs.
    pular = V2 / "_pular_lote_agente1.txt"
    skip = set(pular.read_text(encoding="utf-8").split()) if pular.exists() and not os.environ.get("V2_IGNORAR_PULAR") else set()
    for ad in sys.argv[1:]:
        if ad in skip:
            print("PULADO (outro agente):", ad)
            sys.exit(3)
        processar(ad)
