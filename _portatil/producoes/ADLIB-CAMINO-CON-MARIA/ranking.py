import re,sys,time,json
from playwright.sync_api import sync_playwright
URLS={'busca':'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&q=%22Camino%20con%20Mar%C3%ADa%22&search_type=keyword_exact_phrase&sort_data[direction]=desc&sort_data[mode]=total_impressions',
'pagina':'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id=1330311366834121'}
out={}
with sync_playwright() as p:
    b=p.chromium.launch(channel='chrome',headless=True)
    for k,u in URLS.items():
        pg=b.new_page(locale='es-ES',viewport={'width':1400,'height':1000}); pg.goto(u,wait_until='domcontentloaded',timeout=90000); time.sleep(8)
        ult=0;par=0
        for i in range(120):
            pg.mouse.wheel(0,5000); time.sleep(2)
            n=pg.inner_text('body').count('Identificador de la biblioteca'); par=par+1 if n==ult else 0; ult=n
            if par>=6: break
        t=pg.inner_text('body'); pg.close()
        for pos,bl in enumerate(re.split(r'Identificador de la biblioteca:\s*',t)[1:],1):
            m=re.match(r'(\d+)',bl); d=re.search(r'En circulación desde el ([^\n]+)',bl)
            if m: out.setdefault(m.group(1),{})[k]={'pos':pos,'desde':d.group(1).strip() if d else ''}
    b.close()
json.dump(out,open('_analise/ranking.json','w',encoding='utf-8'),ensure_ascii=False,indent=1); print(len(out))
