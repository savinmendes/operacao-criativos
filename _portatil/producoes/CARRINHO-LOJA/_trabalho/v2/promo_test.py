"""Teste do popup «¡Fuiste seleccionado!» com cv_promo_kit forçado a true SÓ no navegador (simulação; nada gravado)."""
import sys
from playwright.sync_api import sync_playwright
T="167234765056"; BASE="https://chileverificada.com"
OUT="C:/Users/PICHAU/Downloads/CARRINHO-LOJA/v2"
UA_M="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
def cartjs(pg): return pg.evaluate("fetch('/cart.js').then(r=>r.json()).then(c=>({n:c.item_count,t:c.total_price,desc:c.total_discount,items:c.items.map(i=>i.handle+' x'+i.quantity+' '+i.final_line_price)}))")
def run(b, modo):
    mob=modo=="mobile"
    ctx=b.new_context(viewport={"width":390,"height":844} if mob else {"width":1440,"height":900},is_mobile=mob,has_touch=mob,device_scale_factor=2 if mob else 1,user_agent=UA_M if mob else None)
    pg=ctx.new_page(); errs=[]
    pg.on("pageerror", lambda e: errs.append(str(e)[:120]))
    def troca(route):
        r=route.fetch(); body=r.text().replace("promo: false,","promo: true,"); route.fulfill(response=r, body=body)
    pg.route("**/collections/**", lambda route: troca(route) if route.request.resource_type=="document" else route.continue_())
    pg.goto(f"{BASE}/collections/perfumes-arabes?preview_theme_id={T}",wait_until="domcontentloaded",timeout=90000)
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.reload(wait_until="domcontentloaded"); pg.wait_for_timeout(6000)
    print(modo,"promo flag:",pg.evaluate("document.documentElement.innerHTML.indexOf('promo: true')>-1"))
    pg.evaluate("window.scrollTo({top: document.querySelector('#product-grid').getBoundingClientRect().top + window.scrollY - 70, behavior:'instant'})")
    pg.locator(".cv-qa-btn[data-cv-card='yara']").click()
    pg.wait_for_selector(".cvp.is-in", timeout=15000); pg.wait_for_timeout(600)
    pg.screenshot(path=f"{OUT}/10_promo-raspadita_{modo}.png")
    box=pg.locator(".cvp__card canvas").bounding_box()
    # raspa em zigue-zague
    if mob:
        pass
    pg.mouse.move(box["x"]+10, box["y"]+10); pg.mouse.down()
    rows=8
    for r in range(rows):
        y=box["y"]+box["height"]*(r+0.5)/rows
        xs=[box["x"]+8, box["x"]+box["width"]-8] if r%2==0 else [box["x"]+box["width"]-8, box["x"]+8]
        pg.mouse.move(xs[0], y, steps=4); pg.mouse.move(xs[1], y, steps=14)
        if r==2:
            pg.mouse.up(); pg.screenshot(path=f"{OUT}/11_promo-raspando_{modo}.png"); pg.mouse.down()
    pg.mouse.up(); pg.wait_for_timeout(900)
    print(modo,"revelou:", pg.evaluate("document.querySelector('.cvp').classList.contains('is-won')"))
    pg.screenshot(path=f"{OUT}/12_promo-premio-para-mi_{modo}.png")
    print(modo,"para mi:", pg.evaluate("[...document.querySelectorAll('.cvp__it span')].map(e=>e.textContent)"))
    pg.click(".cvp__opt[data-cvp-g='regalo']"); pg.wait_for_timeout(400)
    print(modo,"para regalar:", pg.evaluate("[...document.querySelectorAll('.cvp__it span')].map(e=>e.textContent)"))
    pg.locator(".cvp__it").nth(1).click(); pg.wait_for_timeout(300)
    pg.screenshot(path=f"{OUT}/13_promo-para-regalar_{modo}.png")
    pg.click("[data-cvp-add]")
    pg.wait_for_selector("#cv-cart.is-open", timeout=15000); pg.wait_for_timeout(2500)
    print(modo,"carrinho apos promo:", cartjs(pg))
    pg.screenshot(path=f"{OUT}/14_SIMULACAO-gaveta-apos-promo-sem-desconto_{modo}.png")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    # já tem unitario: outro kit não deve abrir popup
    pg.locator(".cv-qa-btn[data-cv-card='lattafa']").click(); pg.wait_for_timeout(2500)
    print(modo,"2o kit abriu popup?", pg.evaluate("!!document.querySelector('.cvp.is-in')"), "gaveta?", pg.evaluate("document.querySelector('#cv-cart').classList.contains('is-open')"))
    pg.keyboard.press("Escape")
    # formulario Releasit em modo carrinho (não envia)
    pg.evaluate("window.__cvCart.open()"); pg.wait_for_timeout(1500)
    pg.click("#cv-cod")
    try:
        pg.wait_for_selector("#_rsi-cod-form-modal._rsi-cod-form-modal-open", timeout=20000); pg.wait_for_timeout(2500)
        print(modo,"form COD:", pg.evaluate("document.querySelector('#_rsi-cod-form-modal').innerText.slice(0,400)").replace("\n"," | "))
        pg.screenshot(path=f"{OUT}/15_SIMULACAO-form-cod-carrinho_{modo}.png")
    except Exception as e: print("form nao abriu", e)
    # "No, gracias" com carrinho novo (nova sessão)
    ctx2=b.new_context(viewport={"width":390,"height":844} if mob else {"width":1440,"height":900},is_mobile=mob,has_touch=mob,device_scale_factor=2 if mob else 1,user_agent=UA_M if mob else None)
    pg2=ctx2.new_page(); pg2.route("**/collections/**", lambda route: troca(route) if route.request.resource_type=="document" else route.continue_())
    pg2.goto(f"{BASE}/collections/perfumes-arabes?preview_theme_id={T}",wait_until="domcontentloaded",timeout=90000); pg2.wait_for_timeout(6000)
    pg2.evaluate("window.scrollTo({top: document.querySelector('#product-grid').getBoundingClientRect().top + window.scrollY - 70, behavior:'instant'})")
    pg2.locator(".cv-qa-btn[data-cv-card='lattafa']").click(); pg2.wait_for_selector(".cvp.is-in", timeout=15000); pg2.wait_for_timeout(500)
    print(modo,"kit hombre para mi (sem raspar):", pg2.evaluate("[...document.querySelectorAll('.cvp__it span')].map(e=>e.textContent)"))
    pg2.click(".cvp__no"); pg2.wait_for_timeout(2000)
    print(modo,"no gracias -> gaveta:", pg2.evaluate("document.querySelector('#cv-cart').classList.contains('is-open')"), "popup fechado:", pg2.evaluate("!document.querySelector('.cvp')"))
    pg2.keyboard.press("Escape"); pg2.wait_for_timeout(300)
    pg2.reload(wait_until="domcontentloaded"); pg2.wait_for_timeout(5000)
    pg2.evaluate("window.scrollTo({top: document.querySelector('#product-grid').getBoundingClientRect().top + window.scrollY - 70, behavior:'instant'})")
    pg2.locator(".cv-qa-btn[data-cv-card='yara']").click(); pg2.wait_for_timeout(2500)
    print(modo,"mesma sessao/carrinho, popup de novo?", pg2.evaluate("!!document.querySelector('.cvp.is-in')"))
    pg2.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg2.wait_for_timeout(600)
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.wait_for_timeout(600)
    print(modo,"erros:", [e for e in errs if 'innerHTML' not in e and '_0x' not in e and "'}'" not in e and 'closest' not in e and 'Failed to fetch' not in e])
    ctx.close(); ctx2.close()
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome")
    for m in (sys.argv[1:] or ["mobile","desktop"]): run(b,m)
    b.close()
