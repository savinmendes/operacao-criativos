import sys,urllib.request
# uso: python _baixar.py destino url [destino url ...]
a=sys.argv[1:]
for d,u in zip(a[::2],a[1::2]):
    urllib.request.urlretrieve(u,d); print('ok',d)
