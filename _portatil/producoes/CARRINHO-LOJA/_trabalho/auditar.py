"""Audita o fluxo de compra (produto + carrinho) na pre-visualizacao do tema."""
import json, sys
from playwright.sync_api import sync_playwright

TEMA = "167232798976"
BASE = "https://chileverificada.com"
HANDLE = sys.argv[1] if len(sys.argv) > 1 else "kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml"
PREF = sys.argv[2] if len(sys.argv) > 2 else "antes"
OUT = r"C:\Users\PICHAU\Downloads\CARRINHO-LOJA"

JS_BOTOES = r"""
() => {
  const vis = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const out = [];
  document.querySelectorAll('button, a.button, input[type=submit], [role=button], a[class*=btn], div[class*=_rsi]').forEach(el => {
    const t = (el.innerText || el.value || '').trim().replace(/\s+/g,' ').slice(0,80);
    if (!t) return;
    out.push({tag: el.tagName, txt: t, cls: (el.className||'').toString().slice(0,90), name: el.getAttribute('name'), vis: vis(el)});
  });
  return out;
}
"""

def run():
    res = {}
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, channel="chrome")
        for modo, vp in (("mobile", {"width": 390, "height": 844}), ("desktop", {"width": 1440, "height": 900})):
            ctx = b.new_context(viewport=vp, is_mobile=(modo == "mobile"), device_scale_factor=2 if modo == "mobile" else 1,
                                user_agent=None if modo == "desktop" else "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
            pg = ctx.new_page()
            logs = []
            pg.on("console", lambda m: logs.append(f"{m.type}: {m.text[:200]}"))
            pg.goto(f"{BASE}/products/{HANDLE}?preview_theme_id={TEMA}", wait_until="domcontentloaded", timeout=90000)
            pg.wait_for_timeout(7000)
            pg.screenshot(path=f"{OUT}\\{PREF}_produto_{modo}.png", full_page=False)
            pg.screenshot(path=f"{OUT}\\_trabalho\\{PREF}_produto_{modo}_full.png", full_page=True)
            botoes = pg.evaluate(JS_BOTOES)
            info = pg.evaluate("""() => ({
              forms: [...document.querySelectorAll('form[action*="/cart/add"]')].map(f => ({id: f.id, cls: f.className, btns: [...f.querySelectorAll('button')].map(b=>b.innerText.trim()+'|'+b.className+'|hidden='+(b.offsetParent===null))})),
              releasit: [...document.querySelectorAll('[id*=releasit],[class*=releasit],[id*=_rsi],[class*=_rsi]')].slice(0,15).map(e=>e.tagName+'#'+e.id+'.'+(e.className||'').toString().slice(0,60)),
              cartType: (window.theme && window.theme.settings) ? JSON.stringify(window.theme.settings).slice(0,200) : null,
              cartDrawer: !!document.querySelector('cart-drawer'),
              scripts: [...document.scripts].map(s=>s.src).filter(s=>/releasit|cod|rsi/i.test(s))
            })""")
            res[modo] = {"botoes": botoes, "info": info}
            # tenta adicionar ao carrinho via API e abrir /cart
            r = pg.evaluate("""async () => { const v = window.ShopifyAnalytics?.meta?.product?.variants?.[0]?.id;
                const r = await fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:[{id:v,quantity:2}]})});
                return {v, st: r.status, body: (await r.text()).slice(0,300)}; }""")
            res[modo]["add_js"] = r
            pg.goto(f"{BASE}/cart?preview_theme_id={TEMA}", wait_until="domcontentloaded", timeout=90000)
            pg.wait_for_timeout(6000)
            pg.screenshot(path=f"{OUT}\\{PREF}_carrinho-pagina_{modo}.png", full_page=True)
            res[modo]["cart_botoes"] = pg.evaluate(JS_BOTOES)
            res[modo]["cart_rsi"] = pg.evaluate("""() => [...document.querySelectorAll('[id*=releasit],[class*=releasit],[id*=_rsi],[class*=_rsi]')].slice(0,15).map(e=>e.tagName+'#'+e.id+'.'+(e.className||'').toString().slice(0,60))""")
            res[modo]["logs"] = [l for l in logs if "error" in l.lower()][:15]
            ctx.close()
        b.close()
    with open(f"{OUT}\\_trabalho\\{PREF}_auditoria.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1)[:12000])

run()
