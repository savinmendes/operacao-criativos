import json, sys
from playwright.sync_api import sync_playwright
T=sys.argv[1] if len(sys.argv)>1 else "167234765056"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome"); pg=b.new_page(viewport={"width":1440,"height":900})
    pg.goto(f"https://chileverificada.com/collections/perfumes-arabes?preview_theme_id={T}",wait_until="domcontentloaded",timeout=90000)
    pg.wait_for_selector('#product-grid', state='attached', timeout=60000); pg.wait_for_timeout(4000)
    print("theme", pg.evaluate("Shopify.theme.id"))
    pg.evaluate("""fetch('/cart/clear.js',{method:'POST'}).then(()=>fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:[{id:50483876135168,quantity:1},{id:50570134913280,quantity:1}]})})).then(()=>window.__cvCart.open())""")
    pg.wait_for_timeout(3000); pg.click("#cv-cod")
    pg.wait_for_selector("#_rsi-cod-form-modal._rsi-cod-form-modal-open", timeout=20000); pg.wait_for_timeout(3000)
    r=pg.evaluate("""()=>{const m=document.querySelector('#_rsi-cod-form-modal');
      const li=[...m.querySelectorAll('._rsi-modal-line-item')].map(e=>e.outerHTML.replace(/<svg.*?<\/svg>/g,'').slice(0,1500));
      const s=window._rsi&&_rsi.s; const keys=[];
      (function walk(o,p,d){ if(!o||d>6) return; for(const k in o){ try{const v=o[k]; if(/price|discount|line/i.test(k)) keys.push(p+k+'='+JSON.stringify(v).slice(0,80)); if(v&&typeof v=='object') walk(v,p+k+'.',d+1);}catch(e){} } })(s,'',0);
      return {li, keys:keys.slice(0,80), ver: _rsi.version||null, scripts:[...document.scripts].map(x=>x.src).filter(x=>/releasit|rsi/i.test(x))}}""")
    print(json.dumps(r,indent=1,ensure_ascii=False))
    pg.keyboard.press("Escape"); pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.wait_for_timeout(800); b.close()
