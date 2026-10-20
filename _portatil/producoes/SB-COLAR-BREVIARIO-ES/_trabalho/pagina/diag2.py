import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel="chrome",headless=True)
        ctx=await b.new_context(viewport={"width":360,"height":640},device_scale_factor=1,is_mobile=True)
        pg=await ctx.new_page()
        await pg.goto("https://pellorini.com/products/collar-san-benito-breviario",wait_until="networkidle",timeout=90000)
        print(await pg.evaluate("[document.documentElement.className,document.body.className,document.body.id]"))
        print(await pg.evaluate("""()=>{const m=getComputedStyle(document.querySelector('.nx-main'));const th=getComputedStyle(document.querySelector('.nx-th'));return [m.display,m.gridTemplateColumns,m.width,th.display,th.gridTemplateColumns,th.width, document.querySelector('.nx-main').parentElement.className, getComputedStyle(document.querySelector('.nx-main').parentElement).display]}"""))
        await b.close()
asyncio.run(main())
