import sys
from playwright.sync_api import sync_playwright
T="167236436224"; OUT="C:/Users/PICHAU/Downloads/CARRINHO-LOJA/v3"
UA_M="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
LIN="[...document.querySelectorAll('._rsi-modal-line-item')].map(f=>f.querySelector('._rsi-modal-line-item-title').textContent.slice(0,22)+' => '+f.querySelector('._rsi-modal-line-item-final-price').innerText.split(String.fromCharCode(10)).join(' / '))"
def run(b,modo):
    mob=modo=="mobile"
    ctx=b.new_context(viewport={"width":390,"height":844} if mob else {"width":1440,"height":900},is_mobile=mob,has_touch=mob,device_scale_factor=2 if mob else 1,user_agent=UA_M if mob else None)
    pg=ctx.new_page(); errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)[:100]))
    pg.goto(f"https://chileverificada.com/collections/perfumes-arabes?preview_theme_id={T}",wait_until="domcontentloaded",timeout=90000)
    pg.wait_for_selector('#product-grid', state='attached', timeout=60000); pg.wait_for_timeout(4000)
    pg.evaluate("""fetch('/cart/clear.js',{method:'POST'}).then(()=>fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:[{id:50483876135168,quantity:1},{id:50570134913280,quantity:1}]})})).then(()=>window.__cvCart.open())""")
    pg.wait_for_timeout(3000); pg.click("#cv-cod")
    pg.wait_for_selector("#_rsi-cod-form-modal._rsi-cod-form-modal-open", timeout=20000); pg.wait_for_timeout(3000)
    print(modo,"linhas:",pg.evaluate(LIN))
    pg.evaluate("""(()=>{const m=document.querySelector('#_rsi-cod-form-modal');const b=[...m.querySelectorAll('button')].filter(x=>/pedido/i.test(x.innerText)).pop();(b||m).scrollIntoView({block:'end'})})()""")
    pg.wait_for_timeout(800); pg.screenshot(path=f"{OUT}/5_form-releasit-totais_{modo}.png")
    print(modo,"botao:",pg.evaluate("""[...document.querySelectorAll('#_rsi-cod-form-modal button')].map(x=>x.innerText.trim()).filter(t=>/pedido/i.test(t)).join(' | ')"""))
    # robustez: remover o kit dentro do form -> desconto some -> perfume volta a $34.900 sem riscado
    pg.evaluate("""[...document.querySelectorAll('._rsi-modal-line-item')].find(f=>/Pack/.test(f.innerText)).querySelector('._rsi-modal-line-item-remove-button').click()""")
    pg.wait_for_timeout(5000)
    print(modo,"apos remover kit:",pg.evaluate(LIN), pg.evaluate("fetch('/cart.js').then(r=>r.json()).then(c=>c.total_price)"))
    pg.keyboard.press("Escape"); pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.wait_for_timeout(800)
    print(modo,"erros js:",errs); ctx.close()
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome")
    for m in (sys.argv[1:] or ["mobile","desktop"]): run(b,m)
    b.close()
