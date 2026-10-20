from playwright.sync_api import sync_playwright
for T in ("167234765056","167236436224"):
  with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome"); pg=b.new_page(viewport={"width":1440,"height":900}); errs=[]
    pg.on("pageerror", lambda e: errs.append((e.message[:60], (e.stack or '').split('\n')[1][:110] if e.stack and '\n' in e.stack else '')))
    pg.goto(f"https://chileverificada.com/collections/perfumes-arabes?preview_theme_id={T}",wait_until="domcontentloaded",timeout=90000)
    pg.wait_for_selector('#product-grid', state='attached', timeout=60000); pg.wait_for_timeout(4000)
    pg.evaluate("""fetch('/cart/clear.js',{method:'POST'}).then(()=>fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:[{id:50483876135168,quantity:1},{id:50570134913280,quantity:1}]})})).then(()=>window.__cvCart.open())""")
    pg.wait_for_timeout(3000); pg.click("#cv-cod"); pg.wait_for_timeout(6000)
    from collections import Counter
    print(T, Counter(errs).most_common())
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.wait_for_timeout(800); b.close()
