# -*- coding: utf-8 -*-
"""Abre posts do Facebook e captura URLs de vídeo (HD/SD), imagens e o texto do post."""
import json, re, sys, time
from playwright.sync_api import sync_playwright

BS = chr(92)
ids = sys.argv[1:]
res = {}


def limpa(u):
    return u.replace(BS + "/", "/")


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for pid in ids:
        a = {"hd": [], "sd": [], "img": [], "texto": []}

        def on_resp(r, a=a):
            try:
                if "facebook.com" not in r.url: return
                t = r.text()
            except Exception:
                return
            for k, pat in (("hd", r'"(?:browser_native_hd_url|playable_url_quality_hd|video_hd_url)":"(https:[^"]+)"'),
                           ("sd", r'"(?:browser_native_sd_url|playable_url|video_sd_url)":"(https:[^"]+)"')):
                for u in re.findall(pat, t):
                    u = limpa(u)
                    if u not in a[k]: a[k].append(u)
            for x in re.findall(r'"message":\{"text":"(.*?)(?<!' + BS + BS + r')"', t):
                try:
                    s = json.loads('"' + x + '"')
                except Exception:
                    s = x
                if s not in a["texto"]: a["texto"].append(s)

        pg = b.new_page(locale="es-CL", viewport={"width": 1200, "height": 1600})
        pg.on("response", on_resp)
        pg.goto(f"https://www.facebook.com/61592606590702/posts/{pid}/", wait_until="domcontentloaded", timeout=90000)
        time.sleep(7)
        html = pg.content()

        class R:
            url = "facebook.com"
            def text(self): return html
        on_resp(R())
        for u in re.findall(r'"uri":"(https:[^"]+?scontent[^"]+)"', html):
            u = limpa(u)
            if u not in a["img"]: a["img"].append(u)
        pg.screenshot(path=f"{pid}_tela.png")
        res[pid] = a
        pg.close()
        print(pid, "hd", len(a["hd"]), "sd", len(a["sd"]), "img", len(a["img"]), "txt", len(a["texto"]))
    b.close()
json.dump(res, open("posts.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
