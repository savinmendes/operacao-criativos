from playwright.sync_api import sync_playwright
T="167234765056"; OUT="C:/Users/PICHAU/Downloads/CARRINHO-LOJA/v2"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome"); pg=b.new_page(viewport={"width":1440,"height":900})
    pg.goto(f"https://chileverificada.com/collections/perfumes-arabes?preview_theme_id={T}",wait_until="domcontentloaded",timeout=90000)
    pg.wait_for_selector('#product-grid', state='attached', timeout=60000); pg.wait_for_timeout(4000)
    pg.evaluate("""fetch('/cart/clear.js',{method:'POST'}).then(()=>fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:[{id:50483876135168,quantity:1},{id:50570134913280,quantity:1}]})})).then(()=>window.__cvCart.open())""")
    pg.wait_for_timeout(3000); pg.click("#cv-cod")
    pg.wait_for_selector("#_rsi-cod-form-modal._rsi-cod-form-modal-open", timeout=20000); pg.wait_for_timeout(3000)
    info=pg.evaluate("""()=>{const m=document.querySelector('#_rsi-cod-form-modal');
      const els=[...m.querySelectorAll('*')].filter(e=>e.children.length==0&&/67\.350|17\.450|descuento|discount|subtotal|total/i.test(e.textContent));
      const last=els[els.length-1]; let box=last; for(let i=0;i<3&&box.parentElement;i++) box=box.parentElement;
      box.scrollIntoView({block:'center'}); return {leaf:els.map(e=>e.textContent.trim()).slice(0,20), bloco: box.innerText}}""")
    print(info); pg.wait_for_timeout(800)
    pg.screenshot(path=f"{OUT}/24_REAL-form-releasit-totais_desktop.png")
    pg.keyboard.press("Escape"); pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.wait_for_timeout(800); b.close()
