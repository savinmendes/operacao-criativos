# -*- coding: utf-8 -*-
"""Abre a Ad Library, rola, salva respostas brutas (HTML + graphql) e a ordem dos IDs na tela."""
import json, re, sys, time, os
from playwright.sync_api import sync_playwright
URL = sys.argv[1]; RAW = sys.argv[2]; N = int(sys.argv[3])
os.makedirs(RAW, exist_ok=True)
cnt = [0]
def on_resp(r):
    try:
        if "graphql" not in r.url: return
        t = r.text()
    except Exception: return
    if "ad_archive_id" in t:
        cnt[0] += 1
        open(os.path.join(RAW, f"gql_{cnt[0]:03d}.txt"), "w", encoding="utf-8").write(t)
JS = r"""() => { const t = document.body.innerText; const ids=[]; const re=/(?:Library ID|ID da biblioteca|Identificador de la biblioteca|Identificação da biblioteca)[:：]\s*(\d+)/g; let m; while((m=re.exec(t))) if(!ids.includes(m[1])) ids.push(m[1]); 
 const tot = (t.match(/[~≈]?\s*[\d.,]+\s*(results|resultados)/i)||[''])[0]; return {ids, tot}; }"""
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(locale="pt-BR", viewport={"width": 1400, "height": 1000})
    pg.on("response", on_resp)
    pg.goto(URL, wait_until="domcontentloaded", timeout=90000); time.sleep(8)
    for btn in ["Permitir todos os cookies", "Allow all cookies", "Aceitar tudo"]:
        try: pg.get_by_role("button", name=btn).first.click(timeout=1500); break
        except Exception: pass
    open(os.path.join(RAW, "html.txt"), "w", encoding="utf-8").write(pg.content())
    st = {}
    same = 0; last = 0
    for k in range(80):
        st = pg.evaluate(JS)
        print(f"[rolagem {k+1}] ids {len(st['ids'])} | {st['tot']}", flush=True)
        if len(st["ids"]) >= N: break
        if len(st["ids"]) == last: same += 1
        else: same = 0
        if same >= 6: break
        last = len(st["ids"])
        pg.mouse.wheel(0, 4000); time.sleep(2.5)
    pg.screenshot(path=os.path.join(RAW, "tela.png"))
    json.dump(st, open(os.path.join(RAW, "ordem_tela.json"), "w", encoding="utf-8"), indent=1)
    b.close()
print("graphql salvos:", cnt[0])
