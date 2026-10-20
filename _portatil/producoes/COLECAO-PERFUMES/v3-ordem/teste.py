import asyncio, json
from playwright.async_api import async_playwright
URL="https://arabesperfume.cl/collections/p-arabes"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel="chrome")
        for nome,vp,mob in [("mobile",{"width":390,"height":844},True),("desktop",{"width":1366,"height":900},False)]:
            c=await b.new_context(viewport=vp,is_mobile=mob,locale="es-CL",user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148" if mob else None)
            pg=await c.new_page()
            await pg.goto(URL,wait_until="networkidle",timeout=90000); await pg.wait_for_timeout(4000)
            info=await pg.evaluate("""()=>[...document.querySelectorAll('#product-grid .grid__item')].map(li=>{
              const t=(li.querySelector('.card__heading a')||{}).innerText||'';
              const vis=[...li.querySelectorAll('*')].filter(e=>e.children.length==0 && /agotad|sold out/i.test(e.innerText||'') && e.offsetParent!==null).map(e=>e.className+':'+e.innerText.trim());
              const btn=li.querySelector('._rsi-buy-now-button, .quick-add__submit');
              return {t:t.replace(/\\s+/g,' ').slice(0,60),agotado_visivel:vis,botao:btn?(btn.innerText.trim().slice(0,40)+' disabled='+btn.disabled):null, preco:(li.querySelector('.price')||{}).innerText?.replace(/\\s+/g,' ')}
            })""")
            print("==",nome); [print(json.dumps(i,ensure_ascii=False)) for i in info]
            await pg.screenshot(path=f"live_{nome}_full.png",full_page=True)
            await c.close()
        # página do Kit 1: tenta abrir formulario COD e add ao carrinho (sem enviar pedido)
        c=await b.new_context(viewport={"width":390,"height":844},is_mobile=True,locale="es-CL")
        pg=await c.new_page()
        await pg.goto("https://arabesperfume.cl/products/kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml",wait_until="networkidle",timeout=90000); await pg.wait_for_timeout(4000)
        txt=await pg.evaluate("()=>[...document.querySelectorAll('button, ._rsi-buy-now-button')].filter(e=>e.offsetParent).map(e=>e.innerText.trim().replace(/\\s+/g,' ')+' |disabled='+e.disabled).filter(s=>s.length>8).slice(0,12)")
        print("== produto botoes:",txt)
        await pg.screenshot(path="live_produto_kit1.png")
        r=await pg.evaluate("""async()=>{const j=await (await fetch('/products/kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml.js')).json();
          const a=await fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:[{id:j.variants[0].id,quantity:1}]})});
          const cart=await (await fetch('/cart.js')).json(); return {available:j.available, add_status:a.status, itens:cart.item_count, total:cart.total_price}}""")
        print("== add carrinho:",r)
        rsi=pg.locator('._rsi-buy-now-button').first
        if await rsi.count():
            await rsi.click(); await pg.wait_for_timeout(4000)
            await pg.screenshot(path="live_produto_kit1_formulario.png")
            print("== form aberto:", await pg.evaluate("()=>!!document.querySelector('[class*=_rsi-modal], [id*=_rsi], form[class*=rsi]')"))
        await b.close()
asyncio.run(main())
