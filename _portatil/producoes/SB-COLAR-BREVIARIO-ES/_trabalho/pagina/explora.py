import asyncio, json
from playwright.async_api import async_playwright
URL="https://pellorini.com/products/collar-san-benito-breviario"
OUT="C:/Users/PICHAU/Downloads/SB-COLAR-BREVIARIO-ES/_trabalho/pagina/_explora/"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel="chrome",headless=True)
        ctx=await b.new_context(viewport={"width":360,"height":640},device_scale_factor=1,is_mobile=True,has_touch=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",locale="es-CL")
        pg=await ctx.new_page()
        cdp=await ctx.new_cdp_session(pg)
        import base64
        await pg.goto(URL,wait_until="networkidle",timeout=90000)
        await pg.wait_for_timeout(6000)
        h=await pg.evaluate("document.documentElement.scrollHeight")
        print("height",h)
        for i,y in enumerate(range(0,min(h,9000),640)):
            await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(600)
            d=await cdp.send("Page.captureScreenshot",{"format":"png"}); open(OUT+f"s{i:02d}.png","wb").write(base64.b64decode(d["data"]))
        info=await pg.evaluate("""()=>{
          const r=[];document.querySelectorAll('body *').forEach(e=>{
            if(e.children.length===0||e.tagName==='BUTTON'){const t=(e.innerText||'').trim();
             if(/[$]|CLP/.test(t)&&t.length<120){const b=e.getBoundingClientRect();r.push([e.tagName,e.className.toString().slice(0,80),t.slice(0,80),Math.round(b.top+scrollY)])}}});
          return r}""")
        for x in info: print(x)
        fixed=await pg.evaluate("""()=>[...document.querySelectorAll('body *')].filter(e=>{const s=getComputedStyle(e);return (s.position=='fixed'||s.position=='sticky')&&e.offsetHeight>0}).map(e=>[e.tagName,e.id,e.className.toString().slice(0,80),(e.innerText||'').slice(0,60)])""")
        print("FIXED"); [print(f) for f in fixed]
        imgs=await pg.evaluate("""()=>[...document.querySelectorAll('h1,h2,h3')].map(e=>[e.tagName,e.innerText.slice(0,80),Math.round(e.getBoundingClientRect().top+scrollY)])""")
        print("HEADS");[print(f) for f in imgs]
        await b.close()
asyncio.run(main())
