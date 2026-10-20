import json, sys
from playwright.sync_api import sync_playwright
OUT=r"C:/Users/PICHAU/Downloads/CARRINHO-LOJA/v2/ref-linfarele"
UA_M="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
def overlays(pg):
    return pg.evaluate("""()=>[...document.querySelectorAll('body *')].filter(e=>{const s=getComputedStyle(e);const r=e.getBoundingClientRect();return (s.position=='fixed')&&r.width>200&&r.height>150&&s.visibility!='hidden'&&s.display!='none'&&+s.opacity>0.1}).map(e=>e.tagName+'#'+e.id+'.'+String(e.className).slice(0,80)+' '+Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height)+' z='+getComputedStyle(e).zIndex)""")
modo=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome")
    mob=modo=="mobile"
    ctx=b.new_context(viewport={"width":390,"height":844} if mob else {"width":1440,"height":900},is_mobile=mob,has_touch=mob,device_scale_factor=2 if mob else 1,user_agent=UA_M if mob else None)
    pg=ctx.new_page()
    pg.goto("https://linfarele.com/products/drenante-linfatico",wait_until="domcontentloaded",timeout=90000); pg.wait_for_timeout(8000)
    print("overlays inicio", overlays(pg))
    pg.screenshot(path=f"{OUT}/02_produto_{modo}.png")
    pg.mouse.wheel(0,1500); pg.wait_for_timeout(6000)
    print("overlays apos rolar", overlays(pg))
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500)
    btns=pg.evaluate("[...document.querySelectorAll('button, a')].filter(e=>/carrello|aggiungi|acquista|compra|ordina/i.test(e.innerText)&&e.getBoundingClientRect().height>0).map(e=>e.tagName+'#'+e.id+'.'+String(e.className).slice(0,60)+' :: '+e.innerText.trim().slice(0,40))")
    print("botoes", btns)
    sel=pg.locator("form[action*='/cart/add'] [type=submit], [name=add]").first
    sel.scroll_into_view_if_needed(); sel.click(); pg.wait_for_timeout(3500)
    print("overlays apos add", overlays(pg))
    pg.screenshot(path=f"{OUT}/03_apos-add_{modo}.png")
    pg.wait_for_timeout(4000)
    pg.screenshot(path=f"{OUT}/04_apos-add-7s_{modo}.png")
    html=pg.evaluate("""()=>{const o=[...document.querySelectorAll('body *')].filter(e=>{const s=getComputedStyle(e);const r=e.getBoundingClientRect();return s.position=='fixed'&&r.width>200&&r.height>150&&s.display!='none'&&+s.opacity>0.1});return o.map(e=>e.outerHTML.slice(0,3000)).join('\n=====\n')}""")
    open(f"{OUT}/overlay_{modo}.html","w",encoding="utf-8").write(html)
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.wait_for_timeout(500)
    b.close()
