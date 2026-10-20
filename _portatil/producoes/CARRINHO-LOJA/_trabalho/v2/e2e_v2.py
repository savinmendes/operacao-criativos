"""Teste v2 na pre-visualizacao (sem enviar pedido)."""
import json, sys
from playwright.sync_api import sync_playwright
T = "167234765056"; BASE = "https://chileverificada.com"
OUT = r"C:\Users\PICHAU\Downloads\CARRINHO-LOJA\v2"
UA_M = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
KIT = "kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml"
log = []
def L(*a): log.append(" ".join(str(x) for x in a)); print(*a, flush=True)
def U(path): return f"{BASE}{path}{'&' if '?' in path else '?'}preview_theme_id={T}"
def cartjs(pg): return pg.evaluate("fetch('/cart.js').then(r=>r.json()).then(c=>({n:c.item_count,t:c.total_price,items:c.items.map(i=>i.handle+' x'+i.quantity)}))")

def run(b, modo):
    mob = modo == "mobile"
    ctx = b.new_context(viewport={"width":390,"height":844} if mob else {"width":1440,"height":900}, is_mobile=mob, has_touch=mob,
                        device_scale_factor=2 if mob else 1, user_agent=UA_M if mob else None)
    pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
    pg.goto(U("/collections/perfumes-arabes"), wait_until="domcontentloaded", timeout=90000)
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})")
    pg.reload(wait_until="domcontentloaded"); pg.wait_for_timeout(6000)
    st = pg.evaluate("""()=>{const hc=document.querySelector('#cv-hc');const r=hc.getBoundingClientRect();
      const btns=[...document.querySelectorAll('.cv-qa-btn')];const cards=document.querySelectorAll('#product-grid .grid__item').length;
      const rsi=document.querySelectorAll('#product-grid ._rsi-buy-now-button').length;
      const b0=btns[0]&&btns[0].getBoundingClientRect(); const r0=document.querySelector('#product-grid ._rsi-buy-now-button'); const rr=r0&&r0.getBoundingClientRect();
      return {hc:[r.x,r.y,r.width,r.height], hcFloat:hc.classList.contains('is-float'), cards, btns:btns.length, rsi, btn0:b0&&[b0.x,b0.y,b0.width,b0.height], rsi0:rr&&[rr.x,rr.y,rr.width,rr.height], docW:document.documentElement.scrollWidth,
        rsiText: r0 && r0.innerText, overflow:[...document.querySelectorAll('#product-grid ._rsi-buy-now-button > span')].some(s=>s.scrollWidth>s.clientWidth+1)}}""")
    L(modo, "colecao:", json.dumps(st))
    pg.screenshot(path=f"{OUT}/1_colecao-topo_{modo}.png")
    # rola até a grade
    pg.evaluate("window.scrollTo({top: document.querySelector('#product-grid').getBoundingClientRect().top + window.scrollY - 70, behavior:'instant'})")
    pg.wait_for_timeout(1200)
    L(modo, "hc float apos rolar:", pg.evaluate("document.querySelector('#cv-hc').classList.contains('is-float')"))
    pg.screenshot(path=f"{OUT}/2_colecao-cards_{modo}.png")
    # adiciona do card (primeiro botão)
    first = pg.locator(".cv-qa-btn").first
    h = first.get_attribute("data-cv-card"); L(modo, "card add handle:", h)
    first.click()
    pg.wait_for_selector("#cv-cart.is-open", timeout=15000)
    pg.wait_for_timeout(700)
    pg.screenshot(path=f"{OUT}/3_add-card-gaveta-toast_{modo}.png")
    pg.wait_for_timeout(2500)
    L(modo, "carrinho apos add card:", cartjs(pg))
    pg.screenshot(path=f"{OUT}/4_gaveta-completa_{modo}.png")
    try:
        pg.wait_for_selector("#cv-ups [data-cv-add]", timeout=10000)
        pg.click("#cv-ups [data-cv-add] >> nth=0"); pg.wait_for_timeout(3000)
        L(modo, "upsell da gaveta adicionou:", cartjs(pg))
        pg.screenshot(path=f"{OUT}/4b_gaveta-upsell-adicionado_{modo}.png")
        it = pg.evaluate("fetch('/cart.js').then(r=>r.json()).then(c=>c.items[0].key)")
        pg.evaluate(f"fetch('/cart/change.js',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:'{it}',quantity:0}})}})"); pg.wait_for_timeout(1200)
    except Exception as e:
        L(modo, "upsell nao apareceu", e)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(600)
    pg.evaluate("window.__cvCart.refresh()"); pg.wait_for_timeout(1000)
    L(modo, "badge:", pg.evaluate("document.querySelector('#cv-hc-n').textContent+' hidden='+document.querySelector('#cv-hc-n').hidden"))
    pg.screenshot(path=f"{OUT}/5_icone-com-contador_{modo}.png")
    # segundo card (outro produto, mesmo fornecedor)
    pg.locator(".cv-qa-btn").nth(1).click()
    pg.wait_for_selector("#cv-cart.is-open", timeout=15000); pg.wait_for_timeout(2500)
    L(modo, "carrinho apos 2o card:", cartjs(pg))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    # Releasit do card continua abrindo
    pg.evaluate("window.scrollTo({top:0,behavior:'instant'})"); pg.wait_for_timeout(400); pg.evaluate("document.querySelectorAll('#product-grid ._rsi-buy-now-button')[2].click()")
    try:
        pg.wait_for_selector("#_rsi-cod-form-modal._rsi-cod-form-modal-open", timeout=20000); pg.wait_for_timeout(2500)
        L(modo, "releasit card abriu:", pg.evaluate("document.querySelector('#_rsi-cod-form-modal').innerText.slice(0,160)"))
        pg.screenshot(path=f"{OUT}/6_releasit-card-abre_{modo}.png")
    except Exception as e:
        L(modo, "releasit NAO abriu", e); pg.screenshot(path=f"{OUT}/6_releasit-card-FALHOU_{modo}.png")
    # topo: ícone abre a gaveta
    pg.goto(U("/collections/perfumes-arabes"), wait_until="domcontentloaded"); pg.wait_for_timeout(5000)
    pg.click("#cv-hc"); pg.wait_for_selector("#cv-cart.is-open", timeout=10000); pg.wait_for_timeout(1500)
    L(modo, "icone abre gaveta: ok")
    pg.keyboard.press("Escape")
    # trava de fornecedor: põe um produto sem etiqueta e tenta pelo card
    vid = pg.evaluate("fetch('/products/mopah2o.js').then(r=>r.ok?r.json():null).then(p=>p&&p.variants.find(v=>v.available)?.id)")
    if vid:
        pg.evaluate(f"fetch('/cart/clear.js',{{method:'POST'}}).then(()=>fetch('/cart/add.js',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{items:[{{id:{vid},quantity:1}}]}})}}))")
        pg.wait_for_timeout(1500)
        pg.evaluate("window.scrollTo({top: document.querySelector('#product-grid').getBoundingClientRect().top + window.scrollY - 70, behavior:'instant'})"); pg.wait_for_timeout(800)
        pg.locator(".cv-qa-btn").first.click(); pg.wait_for_timeout(1800)
        L(modo, "trava:", pg.evaluate("document.querySelector('#cv-toast').className+' | '+document.querySelector('#cv-toast').innerText"), cartjs(pg))
        pg.screenshot(path=f"{OUT}/7_trava-fornecedor_{modo}.png")
    # página de produto
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})")
    pg.goto(U(f"/products/{KIT}"), wait_until="domcontentloaded"); pg.wait_for_timeout(6000)
    L(modo, "produto: cv-atc visivel", pg.evaluate("!!document.querySelector('#cv-atc:not([hidden])')"), "fab visivel", pg.evaluate("getComputedStyle(document.querySelector('#cv-fab')).display"))
    pg.screenshot(path=f"{OUT}/8_produto-topo_{modo}.png")
    pg.locator("#_rsi-buy-now-button").first.scroll_into_view_if_needed(); pg.evaluate("window.scrollBy(0,-260)"); pg.wait_for_timeout(800)
    pg.screenshot(path=f"{OUT}/9_produto-botoes_{modo}.png")
    # packs antigos: botão no card? (coleção) já coberto; produto lattafa mostra Agregar?
    pg.goto(U("/products/lattafa"), wait_until="domcontentloaded"); pg.wait_for_timeout(6000)
    L(modo, "pack lattafa cv-atc:", pg.evaluate("!!document.querySelector('#cv-atc:not([hidden])')"))
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})")
    L(modo, "erros JS:", errs)
    ctx.close()

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel="chrome")
    for m in (sys.argv[1:] or ["mobile", "desktop"]): run(b, m)
    b.close()
open(OUT + "/teste_log.txt", "w", encoding="utf-8").write("\n".join(log))
