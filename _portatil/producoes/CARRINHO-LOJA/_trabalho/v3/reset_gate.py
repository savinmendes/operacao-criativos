import sys, json
from playwright.sync_api import sync_playwright
T="167236436224"; OUT="C:/Users/PICHAU/Downloads/CARRINHO-LOJA/v3"
UA_M="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
def raspar(pg):
    box=pg.locator(".cvp__card canvas").bounding_box()
    pg.mouse.move(box["x"]+10, box["y"]+10); pg.mouse.down()
    for r in range(8):
        y=box["y"]+box["height"]*(r+0.5)/8
        xs=[box["x"]+8, box["x"]+box["width"]-8] if r%2==0 else [box["x"]+box["width"]-8, box["x"]+8]
        pg.mouse.move(xs[0], y, steps=4); pg.mouse.move(xs[1], y, steps=14)
    pg.mouse.up(); pg.wait_for_timeout(900)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome")
    ctx=b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,device_scale_factor=2,user_agent=UA_M)
    pg=ctx.new_page(); errs=[]; pg.on("pageerror", lambda e: errs.append(e.message[:80]))
    URL=f"https://chileverificada.com/collections/perfumes-arabes?preview_theme_id={T}"
    pg.goto(URL,wait_until="domcontentloaded",timeout=90000); pg.wait_for_selector('#product-grid', state='attached', timeout=60000)
    # simula visitante da v2: marca antiga na sessão
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'}); sessionStorage.setItem('cvPromo:abc','1'); localStorage.setItem('cvPromo:xyz','1')")
    pg.reload(wait_until="domcontentloaded"); pg.wait_for_selector('#product-grid', state='attached', timeout=60000); pg.wait_for_timeout(5000)
    print("marcas v2 apos carregar:", pg.evaluate("[sessionStorage.getItem('cvPromo:abc'), localStorage.getItem('cvPromo:xyz')]"))
    print("botoes nos cards:", pg.evaluate("document.querySelectorAll('.cv-qa-btn').length"), "cards:", pg.evaluate("document.querySelectorAll('#product-grid .card-wrapper').length"))
    pg.evaluate("window.scrollTo({top: document.querySelector('#product-grid').getBoundingClientRect().top + window.scrollY - 70, behavior:'instant'})")
    for rodada in (1,2,3):
        pg.locator(".cv-qa-btn[data-cv-card='yara']").click()
        pg.wait_for_selector(".cvp.is-in", timeout=15000); pg.wait_for_timeout(600)
        st=pg.evaluate("({won:document.querySelector('.cvp').classList.contains('is-won'), canvasOpacity:getComputedStyle(document.querySelector('.cvp__card canvas')).opacity})")
        print(f"rodada {rodada}: popup abriu", st)
        if rodada==2: pg.screenshot(path=f"{OUT}/6_promo-reabre-sem-raspar_mobile.png")
        raspar(pg)
        print(f"rodada {rodada}: raspado ->", pg.evaluate("document.querySelector('.cvp').classList.contains('is-won')"))
        pg.click(".cvp__no"); pg.wait_for_selector("#cv-cart.is-open", timeout=15000); pg.wait_for_timeout(1200)
        # remove o kit (esvazia) e fecha a gaveta
        pg.evaluate("fetch('/cart/clear.js',{method:'POST'}).then(()=>window.__cvCart.refresh()).then(()=>window.__cvCart.close())"); pg.wait_for_timeout(1500)
    # com unitário no carrinho, NÃO deve abrir
    pg.evaluate("fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:[{id:50570134913280,quantity:1}]})})"); pg.wait_for_timeout(1500)
    pg.locator(".cv-qa-btn[data-cv-card='yara']").click(); pg.wait_for_timeout(4000)
    print("com unitario no carrinho, popup abriu?", pg.evaluate("!!document.querySelector('.cvp.is-in')"))
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.wait_for_timeout(800)
    # outra coleção / página fora de perfume: botão só em produtos com perfumes-arabes
    pg.goto(f"https://chileverificada.com/collections/all?preview_theme_id={T}",wait_until="domcontentloaded",timeout=90000); pg.wait_for_timeout(6000)
    r=pg.evaluate("""()=>{const m=JSON.parse((document.querySelector('#cv-card-map')||{}).textContent||'{}');
      const btn=[...document.querySelectorAll('.cv-qa-btn')].map(b=>b.dataset.cvCard);
      return {cards:Object.keys(m).length, comForn:Object.entries(m).filter(([h,v])=>v.f).map(([h])=>h), botoes:btn}}""")
    print("collections/all:", json.dumps(r, ensure_ascii=False))
    print("erros js:", errs)
    b.close()
