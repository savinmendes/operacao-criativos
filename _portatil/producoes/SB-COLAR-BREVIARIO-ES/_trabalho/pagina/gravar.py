import asyncio, base64, os, shutil, json
from playwright.async_api import async_playwright
URL="https://pellorini.com/products/collar-san-benito-breviario"
D="C:/Users/PICHAU/Downloads/SB-COLAR-BREVIARIO-ES/_trabalho/pagina/"
FR=D+"_frames/"
CSS="""
html{scroll-behavior:auto!important;overflow-x:clip!important}
body{overflow-x:clip!important}
body .nx-main, body .nx-main *{min-width:0!important}
body .nx-main{max-width:100vw!important}
body .nx-th{max-width:100%!important;overflow:hidden!important}
body .price,body [class*=price],body [class*=Price],body [class*=compare],body .money,body .rapi-money,body .nx-pr,body .nx-stk>div:first-child{display:none!important}
body .rapi-cart-drawer,body [class*=rapi-cart-drawer],body [class*=popup],body [class*=Popup],body [class*=modal],body [class*=newsletter],body [class*=cookie],body [id*=cookie],body [class*=klaviyo],body [class*=scratch],body [class*=raspa],body [class*=wheel],body [id*=chat],body [class*=chat-],body iframe{display:none!important}
"""
HIDE_JS="""()=>{let n=0;document.querySelectorAll('body *').forEach(e=>{if(e.closest('[data-hid]'))return;
 const own=[...e.childNodes].filter(c=>c.nodeType===3).map(c=>c.textContent).join('');
 if(/[$]|CLP/.test(own)){e.style.setProperty('visibility','hidden','important');e.setAttribute('data-hid','1');n++}});return n}"""
CHECK_JS="""()=>{const t=document.body.innerText;const m=t.match(/.{0,30}([$]|CLP).{0,30}/g)||[];return m}"""
async def main():
    shutil.rmtree(FR,ignore_errors=True); os.makedirs(FR)
    async with async_playwright() as p:
        b=await p.chromium.launch(channel="chrome",headless=True)
        ctx=await b.new_context(viewport={"width":360,"height":640},device_scale_factor=3,is_mobile=True,has_touch=True,
          user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",locale="es-CL")
        pg=await ctx.new_page(); cdp=await ctx.new_cdp_session(pg)
        await pg.goto(URL,wait_until="networkidle",timeout=90000)
        await pg.wait_for_timeout(8000)   # deixa popups atrasados aparecerem
        await pg.keyboard.press("Escape")
        await pg.add_style_tag(content=CSS)
        print("ancestrais:",await pg.evaluate("""()=>{let e=document.querySelector('.nx-main'),r=[];while(e&&e!==document.body){const c=getComputedStyle(e);r.push([e.tagName,e.className.toString().slice(0,40),c.display,c.width]);e.style.setProperty('min-width','0','important');e.style.setProperty('max-width','100%','important');e=e.parentElement}return r}"""))
        # carrega lazy images
        h=await pg.evaluate("document.documentElement.scrollHeight")
        for y in range(0,h,400):
            await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(150)
        await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(1500)
        # esconder tudo que for fixo grande (popup) exceto barra de compra
        print("popups fixos:",await pg.evaluate("""()=>[...document.querySelectorAll('body *')].filter(e=>{const s=getComputedStyle(e);const r=e.getBoundingClientRect();return s.position=='fixed'&&r.height>0&&r.width>0&&!e.closest('.nx-stk')&&!e.classList.contains('nx-stk')}).map(e=>{e.style.setProperty('display','none','important');return e.className.toString().slice(0,50)})"""))
        print("escondidos por texto:",await pg.evaluate(HIDE_JS))
        chk=await pg.evaluate(CHECK_JS)
        print("CHECK $/CLP visivel:",chk)
        print("larguras:",await pg.evaluate("[innerWidth,document.documentElement.scrollWidth]"))
        info=await pg.evaluate("""()=>{const g=e=>e?Math.round(e.getBoundingClientRect().top+scrollY):null;
          return {h1:g(document.querySelector('h1')),lo:g([...document.querySelectorAll('h2')].find(e=>/encontrar/i.test(e.innerText))),
          med:g([...document.querySelectorAll('h2')].find(e=>/Medalla/i.test(e.innerText))),thumbs:document.querySelectorAll('.nx-th img').length,
          H:document.documentElement.scrollHeight}}""")
        print(info)
        n=[0]
        async def shot(rep=1):
            d=await cdp.send("Page.captureScreenshot",{"format":"jpeg","quality":95})
            raw=base64.b64decode(d["data"])
            for _ in range(rep):
                open(FR+f"f{n[0]:05d}.jpg","wb").write(raw); n[0]+=1
        async def hold(sec):
            await shot(round(sec*30))
        async def thumb(i,sec):
            await pg.evaluate(f"(()=>{{const t=document.querySelectorAll('.nx-th img')[{i}];t&&t.click()}})()")
            await pg.wait_for_timeout(900)
            await hold(sec)
        ease=lambda t: 4*t*t*t if t<.5 else 1-(-2*t+2)**3/2
        async def rolar(y0,y1,sec,fn=ease):
            N=round(sec*30)
            for k in range(1,N+1):
                y=y0+(y1-y0)*fn(k/N)
                await pg.evaluate(f"window.scrollTo(0,{y:.2f})"); await pg.wait_for_timeout(15)
                await shot()
        marks={}
        # 1) topo + galeria
        await hold(0.9)
        await thumb(1,1.2)   # maos + medalha
        await thumb(3,1.2)   # colar
        await thumb(0,0.4)   # volta ao breviario
        marks["topo"]=(0,n[0]/30)
        # 2) rolagem ate titulo
        y_tit=max(0,info["h1"]-150)
        t0=n[0]/30
        await rolar(0,y_tit,2.6)
        await hold(0.9)
        marks["meio"]=(t0,n[0]/30)
        # 3) rolagem lenta pela descricao e imagens
        t0=n[0]/30
        y_fim=min(info["med"]+150 if info["med"] else y_tit+2400, info["H"]-640)
        lin=lambda t: t*t*(3-2*t)*0.25+t*0.75
        await rolar(y_tit,y_fim,5.0,lin)
        marks["fim"]=(t0,n[0]/30)
        chk2=await pg.evaluate(CHECK_JS)
        print("CHECK final:",chk2)
        json.dump({"marks":marks,"frames":n[0],"check":chk,"check_final":chk2},open(D+"_marks.json","w"),indent=1)
        await b.close()
asyncio.run(main())
