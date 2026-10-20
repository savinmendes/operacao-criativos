from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome"); pg=b.new_page()
    r=pg.goto("https://chileverificada.com/collections/perfumes-arabes?preview_theme_id=167234765056",wait_until="domcontentloaded",timeout=90000)
    t=r.text().split("\n"); print(len(t))
    for i in range(992,1002): print(i+1, t[i][:300])
    b.close()
