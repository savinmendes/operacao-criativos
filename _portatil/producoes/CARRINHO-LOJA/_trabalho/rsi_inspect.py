import json
from playwright.sync_api import sync_playwright
URL = "https://chileverificada.com/products/kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml?preview_theme_id=167232798976"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel="chrome")
    pg = b.new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(8000)
    r = pg.evaluate("""() => {
      const s = window._rsi && _rsi.s;
      const pick = o => o ? JSON.stringify(o).slice(0,1500) : null;
      return {
        keys: window._rsi ? Object.keys(_rsi).join(',') : null,
        cartPage: s ? pick(s.cartPage) : null,
        productPage: s ? pick(s.productPage) : null,
        upsells: s ? pick(s.general) : null, fdisc: s && s.form ? pick(s.form.discounts) : null, codFee: s ? pick(s.codFee) : null,
        discounts: s ? pick(s.discounts || s.discount || s.quantityOffers) : null,
        skeys: s ? Object.keys(s).join(',') : null,
        formKeys: window._rsi && _rsi.form ? Object.keys(_rsi.form).join(',') : null,
        bnKeys: window._rsi && _rsi.buyNowButton ? Object.keys(_rsi.buyNowButton).join(',') : null,
      };
    }""")
    print(json.dumps(r, indent=1, ensure_ascii=False))
    b.close()
