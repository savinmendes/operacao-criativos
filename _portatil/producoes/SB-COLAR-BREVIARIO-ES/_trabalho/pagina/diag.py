import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel="chrome",headless=True)
        ctx=await b.new_context(viewport={"width":360,"height":640},device_scale_factor=3,is_mobile=True,has_touch=True,
          user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",locale="es-CL")
        pg=await ctx.new_page()
        await pg.goto("https://pellorini.com/products/collar-san-benito-breviario",wait_until="networkidle",timeout=90000)
        await pg.wait_for_timeout(4000)
        print(await pg.evaluate("[innerWidth,document.documentElement.clientWidth,document.documentElement.scrollWidth,visualViewport.width,visualViewport.scale,document.querySelector('meta[name=viewport]')&&document.querySelector('meta[name=viewport]').content]"))
        print(await pg.evaluate("""()=>[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>365&&e.offsetWidth>0).slice(0,15).map(e=>[e.tagName,e.id,e.className.toString().slice(0,60),Math.round(e.getBoundingClientRect().right)])"""))
        print(await pg.evaluate("""()=>[...document.querySelectorAll('[class*=price],[class*=Price],.money,[class*=compare]')].map(e=>[e.tagName,e.className.toString().slice(0,60),(e.innerText||'').slice(0,30)])"""))
        print(await pg.evaluate("""()=>{const s=document.querySelector('.nx-stk');return s?s.outerHTML.slice(0,1500):null}"""))
        print(await pg.evaluate("""()=>[...document.querySelectorAll('button,a')].filter(e=>/QUIERO|Comprar|Pagar/i.test(e.innerText)).map(e=>[e.tagName,e.className.toString().slice(0,60),e.innerText.slice(0,60)])"""))
        await b.close()
asyncio.run(main())
