# -*- coding: utf-8 -*-
"""Top N vídeos (ordem da página = maiores impressões) da Biblioteca de Anúncios, em HD, sem repetidos (md5)."""
import json, re, sys, time, hashlib, os, subprocess
import requests
from playwright.sync_api import sync_playwright
URL = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 30
ordem, ads = [], {}
def achar(o):
    if isinstance(o, dict):
        if "ad_archive_id" in o and "snapshot" in o: yield o
        for v in o.values(): yield from achar(v)
    elif isinstance(o, list):
        for v in o: yield from achar(v)
def processar(t):
    for linha in t.splitlines():
        if "ad_archive_id" not in linha: continue
        cands = [linha.strip()] if linha.strip().startswith("{") else re.findall(r'<script type="application/json"[^>]*>(.*?)</script>', linha, re.S)
        for c in cands:
            if "ad_archive_id" not in c: continue
            try: o = json.loads(c)
            except Exception: continue
            for a in achar(o):
                aid = a["ad_archive_id"]; s = a.get("snapshot") or {}
                vids = [(v.get("video_hd_url"), v.get("video_sd_url")) for v in (s.get("videos") or [])]
                vids += [(c.get("video_hd_url"), c.get("video_sd_url")) for c in (s.get("cards") or []) if c.get("video_hd_url") or c.get("video_sd_url")]
                if aid not in ads:
                    ordem.append(aid)
                    body = (s.get("body") or {}).get("text") if isinstance(s.get("body"), dict) else s.get("body")
                    ads[aid] = {"id": aid, "inicio": a.get("start_date"), "variacoes": a.get("collation_count"), "texto": body,
                                "titulo": s.get("title"), "link": s.get("link_url"), "videos": vids, "formato": s.get("display_format")}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(locale="en-US", viewport={"width": 1400, "height": 1000})
    pg.on("response", lambda r: ("graphql" in r.url) and processar(r.text()) if r.ok else None)
    pg.goto(URL, wait_until="domcontentloaded", timeout=90000); time.sleep(8)
    processar(pg.content())
    for k in range(40):
        if sum(1 for a in ordem if ads[a]["videos"]) >= N * 3: break
        pg.mouse.wheel(0, 5000); time.sleep(2)
    b.close()
print("anúncios lidos:", len(ordem), "| com vídeo:", sum(1 for a in ordem if ads[a]["videos"]))
os.makedirs("videos", exist_ok=True)
vistos, lista, S = set(), [], requests.Session()
for aid in ordem:
    if len(lista) >= N: break
    for hd, sd in ads[aid]["videos"]:
        u = hd or sd
        if not u: continue
        r = S.get(u, timeout=180); r.raise_for_status()
        h = hashlib.md5(r.content).hexdigest()
        if h in vistos: continue
        vistos.add(h)
        n = len(lista) + 1
        fn = f"videos/{n:02d}_{aid}.mp4"
        open(fn, "wb").write(r.content)
        try:
            pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", fn], capture_output=True, text=True)
            j = json.loads(pr.stdout); res = f"{j['streams'][0]['width']}x{j['streams'][0]['height']}"; dur = round(float(j['format']['duration']), 1)
        except Exception: res, dur = "?", 0
        a = ads[aid]
        lista.append({"n": n, "arquivo": fn, "id": aid, "hd": bool(hd), "resolucao": res, "duracao_s": dur,
                      "inicio": time.strftime("%d/%m/%Y", time.localtime(a["inicio"])) if a["inicio"] else "", "variacoes": a["variacoes"],
                      "titulo": a["titulo"], "texto": a["texto"], "link": a["link"], "biblioteca": f"https://www.facebook.com/ads/library/?id={aid}"})
        print(f"[{n}/{N}] {fn} {res} {dur}s {'HD' if hd else 'SD!'}")
        if len(lista) >= N: break
json.dump(lista, open("indice.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
