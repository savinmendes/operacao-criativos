# -*- coding: utf-8 -*-
"""Gera a narração ES de cada item de roteiros.json (por segmento, encaixado no tempo do original)
e junta num mp3 + alinhamento (formato ElevenLabs: characters / *_start_times / *_end_times).

  python gerar_voz.py roteiros.json [--so id1,id2] [--refazer]
Usa a chave do kit (tts_elevenlabs.chave), sem imprimi-la.
"""
from __future__ import annotations
import argparse, base64, json, subprocess, sys
from pathlib import Path
import requests

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
sys.path.insert(0, str(KIT))
from tts_elevenlabs import chave  # noqa

VOZ = Path(r"C:\Users\PICHAU\Downloads\DEWALT-ADS\enxuto\voz")
SEG = VOZ / "_trabalho" / "segmentos"
SEG.mkdir(parents=True, exist_ok=True)
SR = 44100


def tts(texto, voice_id, saida, prev="", nxt="", velocidade=1.0, estab=0.5, estilo=0.0):
    body = {"text": texto, "model_id": "eleven_multilingual_v2", "language_code": "es",
            "voice_settings": {"stability": estab, "similarity_boost": 0.8, "style": estilo,
                               "use_speaker_boost": True, "speed": velocidade}}
    if prev:
        body["previous_text"] = prev
    if nxt:
        body["next_text"] = nxt
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps",
                      params={"output_format": "mp3_44100_128"},
                      headers={"xi-api-key": chave(), "Content-Type": "application/json"}, json=body, timeout=300)
    if r.status_code != 200 and "language_code" in r.text:
        body.pop("language_code")
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps",
                          params={"output_format": "mp3_44100_128"},
                          headers={"xi-api-key": chave(), "Content-Type": "application/json"}, json=body, timeout=300)
    if r.status_code != 200:
        raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:400]}")
    d = r.json()
    Path(saida).write_bytes(base64.b64decode(d["audio_base64"]))
    al = d.get("alignment") or d.get("normalized_alignment")
    Path(str(saida) + ".json").write_text(json.dumps(al, ensure_ascii=False), encoding="utf-8")
    return al


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout.strip())


def fala_fim(al):
    """fim real da fala (último caractere não-espaço)."""
    for c, e in zip(reversed(al["characters"]), reversed(al["character_end_times_seconds"])):
        if c.strip():
            return e
    return 0.0


def processar(item, refazer=False):
    iid = item["id"]
    voice = item["voz_id"]
    vel = item.get("velocidade", 1.0)
    segs = item["segmentos"]
    textos = [s.get("tts") or s["texto"] for s in segs]
    pecas, chars, ini_t, fim_t = [], [], [], []
    cursor = 0.0
    rel = []
    for i, s in enumerate(segs):
        mp3 = SEG / f"{iid}_{i:02d}.mp3"
        v = s.get("velocidade", vel)
        if refazer or not mp3.exists():
            prev = " ".join(textos[max(0, i - 2):i])
            nxt = " ".join(textos[i + 1:i + 2])
            tts(textos[i], voice, mp3, prev, nxt, v, item.get("estabilidade", 0.5), item.get("estilo", 0.0))
        al = json.loads(Path(str(mp3) + ".json").read_text(encoding="utf-8"))
        # corta silêncio inicial do segmento
        primeiro = next((t for c, t in zip(al["characters"], al["character_start_times_seconds"]) if c.strip()), 0.0)
        lead = max(0.0, primeiro - 0.03)
        alvo = s.get("t")
        if alvo is None:
            inicio = cursor + (s.get("pausa", 0.25) if i else 0.0)
        else:
            inicio = max(alvo, cursor + 0.12 if i else alvo)
        fim_fala = fala_fim(al) - lead
        pecas.append((mp3, lead, inicio))
        if chars:
            chars.append(" "); ini_t.append(cursor); fim_t.append(inicio)
        for c, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
            chars.append(c); ini_t.append(round(max(0, a - lead) + inicio, 3)); fim_t.append(round(max(0, b - lead) + inicio, 3))
        cursor = inicio + fim_fala
        rel.append({"i": i, "texto": s["texto"], "inicio": round(inicio, 2), "fim": round(cursor, 2),
                    "dur": round(fim_fala, 2), "orig_ini": s.get("orig_ini"), "orig_fim": s.get("orig_fim")})
    total = cursor + item.get("cauda", 0.4)
    # mix: cada peça com atraso
    cmd = ["ffmpeg", "-v", "error", "-y"]
    filt = []
    for k, (mp3, lead, inicio) in enumerate(pecas):
        cmd += ["-ss", f"{lead:.3f}", "-i", str(mp3)]
        filt.append(f"[{k}:a]aresample={SR},adelay={int(inicio*1000)}:all=1[a{k}]")
    filt.append("".join(f"[a{k}]" for k in range(len(pecas))) + f"amix=inputs={len(pecas)}:normalize=0,apad,atrim=0:{total:.3f}[o]")
    out = VOZ / f"{iid}.mp3"
    cmd += ["-filter_complex", ";".join(filt), "-map", "[o]", "-ac", "1", "-b:a", "192k", str(out)]
    subprocess.run(cmd, check=True)
    (VOZ / f"{iid}.alinhamento.json").write_text(json.dumps(
        {"characters": chars, "character_start_times_seconds": ini_t, "character_end_times_seconds": fim_t},
        ensure_ascii=False), encoding="utf-8")
    return {"id": iid, "arquivo": str(out), "duracao": round(dur(out), 2), "fala_fim": round(cursor, 2), "segmentos": rel}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cfg")
    ap.add_argument("--so", default="")
    ap.add_argument("--refazer", default="", help="ids de segmentos p/ refazer: id:i,id:i")
    a = ap.parse_args()
    cfg = json.loads(Path(a.cfg).read_text(encoding="utf-8"))
    so = set(x for x in a.so.split(",") if x)
    for x in a.refazer.split(","):
        if x:
            iid, i = x.split(":")
            p = SEG / f"{iid}_{int(i):02d}.mp3"
            if p.exists():
                p.unlink()
    res = []
    for item in cfg["itens"]:
        if so and item["id"] not in so:
            continue
        r = processar(item)
        print(json.dumps({k: r[k] for k in ("id", "duracao", "fala_fim")}, ensure_ascii=False), flush=True)
        res.append(r)
    rp = VOZ / "_trabalho" / "relatorio_voz.json"
    old = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}
    for r in res:
        old[r["id"]] = r
    rp.write_text(json.dumps(old, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
