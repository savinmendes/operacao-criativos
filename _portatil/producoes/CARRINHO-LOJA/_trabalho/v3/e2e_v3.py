import sys
from playwright.sync_api import sync_playwright
T="167236436224"; BASE="https://chileverificada.com"; OUT="C:/Users/PICHAU/Downloads/CARRINHO-LOJA/v3"
UA_M="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
def run(b, modo):
    mob=modo=="mobile"
    ctx=b.new_context(viewport={"width":390,"height":844} if mob else {"width":1440,"height":900},is_mobile=mob,has_touch=mob,device_scale_factor=2 if mob else 1,user_agent=UA_M if mob else None)
    pg=ctx.new_page()
    pg.goto(f"{BASE}/collections/perfumes-arabes?preview_theme_id={T}",wait_until="domcontentloaded",timeout=90000)
    pg.wait_for_selector('#product-grid', state='attached', timeout=60000)
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'}).then(()=>window.__cvCart.refresh())"); pg.wait_for_timeout(6000)
    print(modo,"flag no tema:", pg.evaluate("document.documentElement.innerHTML.indexOf('promo: true')>-1"))
    pg.evaluate("window.scrollTo({top: document.querySelector('#product-grid').getBoundingClientRect().top + window.scrollY - 70, behavior:'instant'})")
    pg.locator(".cv-qa-btn[data-cv-card='yara']").click()
    pg.wait_for_selector(".cvp.is-in", timeout=15000); pg.wait_for_timeout(600)
    pg.screenshot(path=f"{OUT}/1_promo-raspadita_{modo}.png")
    box=pg.locator(".cvp__card canvas").bounding_box()
    pg.mouse.move(box["x"]+10, box["y"]+10); pg.mouse.down()
    for r in range(8):
        y=box["y"]+box["height"]*(r+0.5)/8
        xs=[box["x"]+8, box["x"]+box["width"]-8] if r%2==0 else [box["x"]+box["width"]-8, box["x"]+8]
        pg.mouse.move(xs[0], y, steps=4); pg.mouse.move(xs[1], y, steps=14)
    pg.mouse.up(); pg.wait_for_timeout(900)
    pg.locator(".cvp__it").nth(1).click(); pg.wait_for_timeout(300)
    print(modo,"popup:", pg.evaluate("[document.querySelector('.cvp__nota').innerText, document.querySelector('.cvp__solo').innerText, document.querySelector('.cvp__btn').innerText]"))
    print(modo,"popup cabe (scrollW<=W):", pg.evaluate("[document.querySelector('.cvp').scrollWidth, innerWidth]"))
    pg.screenshot(path=f"{OUT}/2_promo-premio-texto-novo_{modo}.png")
    pg.click("[data-cvp-add]"); pg.wait_for_selector("#cv-cart.is-open", timeout=15000); pg.wait_for_timeout(3000)
    c=pg.evaluate("fetch('/cart.js').then(r=>r.json()).then(c=>({total:c.total_price,orig:c.original_total_price,desc:c.total_discount,items:c.items.map(i=>i.handle+' '+i.original_line_price+'->'+i.final_line_price+' '+JSON.stringify((i.discounts||[]).map(d=>d.title)))}))")
    print(modo,"carrinho:", c)
    print(modo,"gaveta:", pg.evaluate("document.querySelector('#cv-foot').innerText.split(String.fromCharCode(10)).join(' | ')"))
    pg.screenshot(path=f"{OUT}/3_gaveta-com-desconto_{modo}.png")
    pg.click("#cv-cod")
    pg.wait_for_selector("#_rsi-cod-form-modal._rsi-cod-form-modal-open", timeout=20000); pg.wait_for_timeout(3000)
    t=pg.evaluate("document.querySelector('#_rsi-cod-form-modal').innerText")
    import re
    linhas=[l for l in t.split("\n") if re.search(r'(?i)descuento|discount|total|subtotal|\$', l)]
    print(modo,"linhas releasit:", pg.evaluate("[...document.querySelectorAll('._rsi-modal-line-item')].map(f=>f.querySelector('._rsi-modal-line-item-title').textContent.slice(0,30)+' => '+f.querySelector('._rsi-modal-line-item-final-price').innerText.split(String.fromCharCode(10)).join(' / '))"))
    print(modo,"form releasit:", " | ".join(linhas[:20]))
    pg.screenshot(path=f"{OUT}/4_form-releasit-linha-com-desconto_{modo}.png")
    # rola o form até o resumo de totais
    pg.evaluate("""(()=>{const m=document.querySelector('#_rsi-cod-form-modal');const el=[...m.querySelectorAll('*')].filter(e=>/automatic|descuento|subtotal/i.test(e.textContent)&&e.children.length==0).pop();if(el)el.scrollIntoView({block:'center'})})()""")
    pg.wait_for_timeout(800); pg.screenshot(path=f"{OUT}/5_form-releasit-totais_{modo}.png")
    pg.keyboard.press("Escape"); pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.wait_for_timeout(800)
    ctx.close()
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome")
    for m in (sys.argv[1:] or ["mobile","desktop"]): run(b,m)
    b.close()
