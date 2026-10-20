"""Teste ponta a ponta na pre-visualizacao (sem enviar pedido)."""
import json, sys
from playwright.sync_api import sync_playwright

TEMA = "167232798976"
BASE = "https://chileverificada.com"
KIT = "kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml"
OUT = r"C:\Users\PICHAU\Downloads\CARRINHO-LOJA"
UA_M = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
ADDON_TESTE = "--addon" in sys.argv
log = []

def shot(pg, nome, full=False):
    p = f"{OUT}\\{nome}.png"
    pg.screenshot(path=p, full_page=full)
    log.append(p)

def run_modo(b, modo):
    mob = modo == "mobile"
    ctx = b.new_context(viewport={"width": 390, "height": 844} if mob else {"width": 1440, "height": 900},
                        is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1, user_agent=UA_M if mob else None)
    pg = ctx.new_page()
    erros = []
    pg.on("pageerror", lambda e: erros.append(str(e)[:200]))
    if ADDON_TESTE:
        def troca(route):
            r = route.fetch()
            body = r.text().replace("addon: 0,", "addon: 19900,")
            route.fulfill(response=r, body=body)
        pg.route("**/products/**", lambda route: troca(route) if route.request.resource_type == "document" else route.continue_())
    pg.goto(f"{BASE}/products/{KIT}?preview_theme_id={TEMA}", wait_until="domcontentloaded", timeout=90000)
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})")
    pg.reload(wait_until="domcontentloaded")
    pg.wait_for_selector("#cv-atc:not([hidden])", timeout=20000)
    pg.wait_for_timeout(2500)
    pre = "addon_" if ADDON_TESTE else ""
    if not ADDON_TESTE:
        pg.locator("#_rsi-buy-now-button").first.scroll_into_view_if_needed()
        pg.evaluate("window.scrollBy(0, -260)")
        pg.wait_for_timeout(600)
        shot(pg, f"depois_1_produto-botoes_{modo}")
    # quantidade 2 + agregar
    pg.click("#cv-atc [data-cv-q='1']")
    pg.click("#cv-atc-btn")
    pg.wait_for_selector("#cv-cart.is-open", timeout=15000)
    try:
        pg.wait_for_selector("#cv-ups .cv-up", timeout=15000)
    except Exception:
        log.append(f"{modo}: upsell NAO apareceu")
    pg.wait_for_timeout(1500)
    shot(pg, f"depois_2_{pre}carrinho-2kits_{modo}")
    c = pg.evaluate("fetch('/cart.js').then(r=>r.json()).then(c=>({n:c.item_count,t:c.total_price,items:c.items.map(i=>i.handle+' x'+i.quantity)}))")
    log.append(f"{modo} carrinho apos ATC: {c}")
    ups = pg.evaluate("[...document.querySelectorAll('#cv-ups .cv-up__t')].map(e=>e.textContent)")
    log.append(f"{modo} upsell: {ups}")
    if ADDON_TESTE:
        opts = pg.evaluate("[...document.querySelectorAll('#cv-addon-sel option')].map(e=>e.textContent)")
        log.append(f"{modo} addon opcoes: {opts}")
        ctx.close(); return erros
    # adiciona 1 do upsell
    pg.click("#cv-ups [data-cv-add] >> nth=0")
    pg.wait_for_timeout(3500)
    shot(pg, f"depois_3_carrinho-com-upsell_{modo}")
    c = pg.evaluate("fetch('/cart.js').then(r=>r.json()).then(c=>({n:c.item_count,t:c.total_price,items:c.items.map(i=>i.handle+' x'+i.quantity)}))")
    log.append(f"{modo} carrinho apos upsell: {c}")
    # abre o formulario contra entrega (NAO envia)
    pg.click("#cv-cod")
    pg.wait_for_selector("#_rsi-cod-form-modal._rsi-cod-form-modal-open", timeout=20000)
    pg.wait_for_timeout(3000)
    shot(pg, f"depois_4_formulario-cod_{modo}")
    txt = pg.evaluate("document.querySelector('#_rsi-cod-form-modal').innerText.slice(0,500)")
    log.append(f"{modo} form COD: {txt!r}")
    # fecha form, botão flutuante
    pg.keyboard.press("Escape")
    pg.goto(f"{BASE}/products/{KIT}?preview_theme_id={TEMA}", wait_until="domcontentloaded")
    pg.wait_for_timeout(5000)
    pg.evaluate("window.scrollTo(0, 1600)")
    pg.wait_for_timeout(2000)
    shot(pg, f"depois_5_botao-carrinho-flutuante_{modo}")
    if not mob:
        # conflito de fornecedor: produto sem etiqueta forn- no carrinho
        vid = pg.evaluate("fetch('/products/mopah2o.js').then(r=>r.ok?r.json():null).then(p=>p&&p.variants[0].id)")
        if vid:
            pg.evaluate(f"fetch('/cart/clear.js',{{method:'POST'}}).then(()=>fetch('/cart/add.js',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{items:[{{id:{vid},quantity:1}}]}})}}))")
            pg.reload(wait_until="domcontentloaded")
            pg.wait_for_selector("#cv-atc:not([hidden])", timeout=20000)
            pg.wait_for_timeout(2000)
            pg.click("#cv-atc-btn")
            pg.wait_for_selector("#cv-atc-msg.is-on", timeout=10000)
            pg.locator("#cv-atc").scroll_into_view_if_needed()
            shot(pg, f"depois_6_aviso-outro-fornecedor_{modo}")
            c = pg.evaluate("fetch('/cart.js').then(r=>r.json()).then(c=>c.items.map(i=>i.handle))")
            log.append(f"conflito: carrinho continua {c}")
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})")
    pg.wait_for_timeout(800)
    ctx.close()
    return erros

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel="chrome")
    for modo in ("mobile", "desktop"):
        e = run_modo(b, modo)
        cv = [x for x in e if 'cv' in x.lower()]
        log.append(f"{modo} erros JS (todos={len(e)}): {cv or e[:3]}")
    b.close()
print("\n".join(log))
