import json
from playwright.sync_api import sync_playwright
T="167234765056"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome")
    ctx=b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,device_scale_factor=2)
    pg=ctx.new_page()
    pg.goto(f"https://chileverificada.com/collections/perfumes-arabes?preview_theme_id={T}",wait_until="domcontentloaded",timeout=90000)
    pg.wait_for_timeout(6000)
    pg.screenshot(path=r"C:\Users\PICHAU\Downloads\CARRINHO-LOJA\_trabalho\v2\antes_col_mobile.png")
    info=pg.evaluate("""()=>{
      const out={};
      const hg=document.querySelector('.shopify-section-group-header-group')||document.querySelector('[class*=header-group]');
      out.headerSections=[...document.querySelectorAll('.shopify-section-group-header-group')].map(s=>({id:s.id,cls:s.className,h:s.getBoundingClientRect().height,html:s.outerHTML.slice(0,1500)}));
      out.bodyFirst=[...document.body.children].slice(0,8).map(e=>e.tagName+'#'+e.id+'.'+e.className+' h='+e.getBoundingClientRect().height);
      const card=document.querySelector('#product-grid .grid__item');
      out.card=card?card.outerHTML.slice(0,6000):null;
      out.sticky=[...document.querySelectorAll('*')].filter(e=>{const s=getComputedStyle(e);return (s.position=='sticky'||s.position=='fixed')&&e.getBoundingClientRect().height>0}).map(e=>e.tagName+'#'+e.id+'.'+String(e.className).slice(0,60)+' top='+e.getBoundingClientRect().top+' h='+e.getBoundingClientRect().height+' z='+getComputedStyle(e).zIndex);
      return out;}""")
    open(r"C:\Users\PICHAU\Downloads\CARRINHO-LOJA\_trabalho\v2\inspect.json","w",encoding="utf-8").write(json.dumps(info,ensure_ascii=False,indent=1))
    b.close()
