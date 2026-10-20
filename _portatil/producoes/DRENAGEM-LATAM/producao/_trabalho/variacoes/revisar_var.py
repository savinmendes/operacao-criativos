# -*- coding: utf-8 -*-
"""Revisão de variações: python revisar_var.py <VAR_NN> [<VAR_NN> ...]   (ou 'todas')
- decodifica o arquivo inteiro (erros), confere 720x1280 / áudio / duração / tamanho
- whisper (es) do início até gancho+40 s: palavras proibidas, emenda gancho→corpo (frase cortada)
- scdet no gancho+3 s: corte fora do planejado ou dois cortes a <0,3 s (quadro solto)
- silencedetect no vídeo inteiro (silêncio > 0,8 s, principalmente na emenda e no fim)
- folha de contato do gancho (a cada 0,5 s) em trab/NN/rev_folha.jpg
Grava trab/NN/revisao.json e imprime um resumo.
"""
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

V = Path(__file__).resolve().parent
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
PROIB = ["maya verra", "mayaverra", "maya", "verra", "sesenta dias", "60 dias", "hecho en estados unidos", "ozempic", "tiktok",
         "cofepris", "cancer", "link", "pesos", "dolares", "precio", "probado por terceros", "45 dias", "cuarenta y cinco dias"]
_modelo = None


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def modelo():
    global _modelo
    if _modelo is None:
        from faster_whisper import WhisperModel
        _modelo = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
    return _modelo


def revisar(nn):
    T = V / "trab" / nn
    info = json.load(open(T / "info.json", encoding="utf-8"))
    f = Path(info["saida"])
    Hd = info["Hd"]
    rep = {"arquivo": f.name, "problemas": []}
    # 1) decodificação e formato
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-f", "null", "-"], capture_output=True, text=True)
    if r.stderr.strip():
        rep["problemas"].append("erro de decodificação: " + r.stderr.strip()[:200])
    p = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,sample_rate:format=duration,size",
                                   "-of", "json", str(f)], capture_output=True, text=True).stdout)
    vs = [s for s in p["streams"] if s["codec_type"] == "video"][0]
    rep["res"] = f"{vs['width']}x{vs['height']}"
    rep["dur"] = round(float(p["format"]["duration"]), 2)
    rep["mb"] = round(int(p["format"]["size"]) / 1e6, 1)
    if rep["res"] != "720x1280":
        rep["problemas"].append("resolução " + rep["res"])
    if not any(s["codec_type"] == "audio" for s in p["streams"]):
        rep["problemas"].append("sem áudio")
    # 2) whisper do começo
    wav = T / "rev.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-t", f"{Hd + 40:.2f}", "-i", str(f), "-ac", "1", "-ar", "16000", str(wav)], check=True)
    segs, _ = modelo().transcribe(str(wav), language="es", word_timestamps=True, vad_filter=False)
    pal = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]
    txt = " ".join(w for w, _, _ in pal)
    rep["whisper_gancho"] = " ".join(w for w, a, _ in pal if a < Hd)
    rep["whisper_emenda"] = " ".join(w for w, a, _ in pal if Hd - 3 <= a < Hd + 6)
    nt = " " + re.sub(r"[^a-z0-9 ]", " ", norm(txt)) + " "
    for x in PROIB:
        if f" {x} " in nt:
            rep["problemas"].append(f"palavra proibida no começo: {x}")
    # palavra atravessando a emenda (frase cortada)
    for w, a, b in pal:
        if a < Hd - 0.05 < b - 0.05 and b - Hd > 0.15:
            rep["problemas"].append(f"palavra atravessa a emenda: '{w}' {a}-{b}")
    # o gancho foi falado inteiro? (cobertura de palavras do roteiro)
    alvo = set(re.sub(r"[^a-z ]", " ", norm(info["texto"])).split())
    ouv = set(re.sub(r"[^a-z ]", " ", norm(rep["whisper_gancho"])).split())
    cob = len(alvo & ouv) / max(1, len(alvo))
    rep["cobertura_gancho"] = round(cob, 2)
    if cob < 0.75:
        rep["problemas"].append(f"whisper reconheceu só {cob:.0%} do texto do gancho")
    # 3) cortes no gancho
    r = subprocess.run(["ffmpeg", "-hide_banner", "-t", f"{Hd + 3:.2f}", "-i", str(f), "-an", "-vf",
                        "scdet=threshold=10,metadata=print", "-f", "null", "-"], capture_output=True, text=True)
    cortes = [float(l.split("lavfi.scd.time:")[1]) for l in r.stderr.splitlines() if "lavfi.scd.time:" in l]
    plan, acc = [], 0.0
    for s in info["tomadas"]:
        acc += s["dur"]; plan.append(round(acc, 3))
    rep["cortes"] = cortes
    rep["cortes_plan"] = plan
    for a, b in zip(cortes, cortes[1:]):
        if b - a < 0.3:
            rep["problemas"].append(f"cortes a {b - a:.2f}s um do outro em {a:.2f}s (quadro solto?)")
    for c in cortes:
        if c < Hd + 0.05 and min(abs(c - x) for x in plan) > 0.07:
            rep["problemas"].append(f"corte não planejado dentro do gancho em {c:.2f}s")
    # 4) silêncio
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(f), "-vn", "-af", "silencedetect=noise=-45dB:d=0.8", "-f", "null", "-"],
                       capture_output=True, text=True)
    sil = []
    ini = None
    for l in r.stderr.splitlines():
        if "silence_start" in l:
            ini = float(l.split("silence_start:")[1])
        if "silence_end" in l and ini is not None:
            fim = float(l.split("silence_end:")[1].split("|")[0]); sil.append((round(ini, 2), round(fim, 2))); ini = None
    if ini is not None:
        sil.append((round(ini, 2), rep["dur"]))
    rep["silencios"] = sil
    for a, b in sil:
        if a < Hd + 2 or b > rep["dur"] - 1.5:
            rep["problemas"].append(f"silêncio {a}-{b}s")
    # 5) folha do gancho
    subprocess.run([sys.executable, str(KIT / "folhas_contato.py"), "--cada", "0.5", "--de", "0", "--ate", f"{Hd + 2:.2f}",
                    "--colunas", "8", "--largura", "160", "--saida", str(T / "rev_folha"), str(f)], capture_output=True)
    rep["ok"] = not rep["problemas"]
    json.dump(rep, open(T / "revisao.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[{nn}] {'OK' if rep['ok'] else 'PROBLEMAS'} | {rep['res']} {rep['dur']}s {rep['mb']}MB | cobertura {rep['cobertura_gancho']}"
          f"\n   gancho: {rep['whisper_gancho']}\n   emenda: {rep['whisper_emenda']}" +
          "".join(f"\n   !! {x}" for x in rep["problemas"]), flush=True)
    return rep


if __name__ == "__main__":
    alvos = sys.argv[1:]
    if alvos == ["todas"]:
        alvos = sorted(p.name for p in (V / "trab").iterdir() if (p / "info.json").exists())
    for i, nn in enumerate(alvos, 1):
        print(f"--- [{i}/{len(alvos)}]", flush=True)
        revisar(nn)
