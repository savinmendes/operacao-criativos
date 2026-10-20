import json,os
L=json.load(open('lotes/L6_acessorios.json',encoding='utf-8'))
obs={'pellorini-silk-cleaning-cloth_2':'assinatura saiu em script mais legivel/regular que a original (ainda manuscrita); grafia correta',
'premium-pellorini-box_0':'tom do verde da caixa levemente mais claro; grafia correta',
'pellorini-parchment-gift-bag_1':'ultimo i passa por tras da corda, como no original'}
base=r'C:\Users\PICHAU\Downloads\PELLORINI-LOJA\fotos-pellorini'
out=[]
for x in L:
  k=f"{x['handle']}_{x['pos']}"
  out.append(dict(handle=x['handle'],pos=x['pos'],tipo=x['tipo'],url_original=x['url'],arquivo=os.path.join(base,k+'.jpg'),status='aprovada',tentativas=1,custo=0.108,observacao=obs.get(k,'grafia correta, enquadramento 1:1 mantido')))
json.dump(out,open('resultado_L6.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out))
