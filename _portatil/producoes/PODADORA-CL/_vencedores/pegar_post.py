# -*- coding: utf-8 -*-
import sys, json, re, time
from playwright.sync_api import sync_playwright
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for i, url in enumerate(sys.argv[1:], 1):
        pg = b.new_page(locale="es-CL", viewport={"width": 1280, "height": 1400})
        vids = []
        def on_resp(r):
            u = r.url
            if ".mp4" in u or "video" in (r.headers.get("content-type") or ""):
                vids.append(u)
        pg.on("response", on_resp)
        pg.goto(url, wait_until="domcontentloaded", timeout=90000); time.sleep(8)
        for btn in ["Permitir todos los cookies", "Allow all cookies", "Rechazar cookies opcionales", "Decline optional cookies"]:
            try: pg.get_by_role("button", name=btn).first.click(timeout=1500); break
            except Exception: pass
        try: pg.keyboard.press("Escape")
        except Exception: pass
        time.sleep(3)
        html = pg.content()
        hd = [u.replace("\/", "/") for u in re.findall(r'"(?:browser_native_hd_url|playable_url_quality_hd|hd_src)":"(https:[^"]+)"', html)]
        sd = [u.replace("\/", "/") for u in re.findall(r'"(?:browser_native_sd_url|playable_url|sd_src)":"(https:[^"]+)"', html)]
        og = dict(re.findall(r'<meta property="og:(title|description|video|image)" content="([^"]*)"', html))
        texto = pg.inner_text("body")[:1500]
        pg.screenshot(path=f"post{i}.png")
        out[url] = {"hd": hd[:3], "sd": sd[:3], "og": og, "rede": vids[:5], "texto": texto}
        pg.close()
    b.close()
json.dump(out, open("posts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for u, v in out.items(): print(u, "| hd", len(v["hd"]), "| sd", len(v["sd"]), "| rede", len(v["rede"]), "|", v["og"].get("title","")[:80])
