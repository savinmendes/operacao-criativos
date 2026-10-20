# -*- coding: utf-8 -*-
"""Biblioteca de Anúncios do Meta -> baixa em HD os vídeos dos anúncios SEM o selo «Número de impresiones bajo»,
deduplica por md5 e grava uma cópia sem metadados.
Uso: python baixar_adlib.py "<url da biblioteca>" <pasta_saida>"""
import json, re, sys, time, hashlib, subprocess, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

URL, OUT = sys.argv[1], Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
raw = []


def on_resp(r):
    try:
        if "graphql" in r.url or "ads/library" in r.url:
            raw.append(r.text())
    except Exception:
        pass


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(locale="es-ES", viewport={"width": 1400, "height": 1000})
    pg.on("response", on_resp)
    pg.goto(URL, wait_until="domcontentloaded", timeout=90000); time.sleep(8)
    ult, parado = 0, 0
    for k in range(120):  # rola até parar de crescer
        pg.mouse.wheel(0, 5000); time.sleep(2)
        n = pg.inner_text("body").count("Identificador de la biblioteca")
        parado = parado + 1 if n == ult else 0
        ult = n
        if parado >= 6:
            break
    texto = pg.inner_text("body"); raw.append(pg.content())
    b.close()

# 1) quais cards têm o selo de poucas impressões
blocos = re.split(r"Identificador de la biblioteca:\s*", texto)[1:]
cards = {}
for bl in blocos:
    m = re.match(r"(\d+)", bl)
    if m:
        cards[m.group(1)] = ("impresiones bajo" in bl.split("Identificador de la biblioteca")[0])

# 2) URLs de vídeo por ad_archive_id (no JSON das respostas)
tudo = "\n".join(raw)
urls = {}
for m in re.finditer(r'"ad_archive_id":"(\d+)"(.{0,30000}?)(?="ad_archive_id"|$)', tudo, re.S):
    aid, bl = m.group(1), m.group(2)
    hd = [u.replace("\\/", "/") for u in re.findall(r'"video_hd_url":"(https:[^"]+)"', bl)]
    sd = [u.replace("\\/", "/") for u in re.findall(r'"video_sd_url":"(https:[^"]+)"', bl)]
    if hd or sd:
        d = urls.setdefault(aid, {"hd": [], "sd": []})
        for u in hd:
            if u not in d["hd"]: d["hd"].append(u)
        for u in sd:
            if u not in d["sd"]: d["sd"].append(u)

rel = {"cards": len(cards), "baixo": sum(cards.values()), "baixados": [], "pulados_baixo": [], "sem_video": [], "duplicados": []}
vistos = {}
for aid, baixo in cards.items():
    if baixo:
        rel["pulados_baixo"].append(aid); continue
    if aid not in urls:
        rel["sem_video"].append(aid); continue
    fontes = [("hd", u) for u in urls[aid]["hd"]] + [("sd", u) for u in urls[aid]["sd"]]
    for i, (q, u) in enumerate(fontes):
        if q == "sd" and any(x == "hd" for x, _ in fontes[:i]):
            break  # já tem HD desse anúncio
        tmp = OUT / f"_tmp_{aid}_{i}.mp4"
        try:
            urllib.request.urlretrieve(u, tmp)
        except Exception as e:
            continue
        md5 = hashlib.md5(tmp.read_bytes()).hexdigest()
        if md5 in vistos:
            rel["duplicados"].append([aid, vistos[md5]]); tmp.unlink(); continue
        nome = OUT / f"{aid}{'' if i == 0 else '_'+str(i)}.mp4"
        # cópia sem metadados (sem recodificar)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-map", "0", "-map_metadata", "-1",
                        "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact",
                        "-metadata", "creation_time=", "-metadata", "encoder=", "-c", "copy", str(nome)], check=True)
        tmp.unlink()
        vistos[md5] = aid
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                            "-of", "csv=p=0", str(nome)], capture_output=True, text=True).stdout.strip()
        rel["baixados"].append({"id": aid, "arquivo": nome.name, "qualidade": q, "res": r})
json.dump(rel, open(OUT / "_relatorio.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"cards {rel['cards']} | poucas impressões (pulados) {rel['baixo']} | baixados {len(rel['baixados'])} | "
      f"sem vídeo {len(rel['sem_video'])} | duplicados {len(rel['duplicados'])}")
print("abaixo de 720p:", [b['arquivo'] for b in rel['baixados'] if b['res'] and min(map(int, b['res'].split(','))) < 720])
