p = r'C:/Users/PICHAU/Downloads/CARRINHO-LOJA/novos-v2/snippets__cv-carrito.liquid'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)

# 1. settings
rep("""  - cv_fab ............... true""", """  - cv_promo_kit ......... true = al agregar un KIT (etiquetas kit + cv_promo_forn) desde una tarjeta, abre el
                           "rasca y gana" «¡Fuiste seleccionado!» con +1 perfume unitario a mitad de precio.
                           SOLO prender DESPUÉS de crear el descuento automático "Black Friday +1 perfume 50%"
                           (sin él, el carrito cobra el precio completo). Reemplaza al bloque bf_addon_precio.
  - cv_promo_forn ........ proveedor de la promo (kits y unitarios con la misma etiqueta).
  - cv_fab ............... true""")
rep("""  assign cv_atc_producto = false
""", """  assign cv_atc_producto = false
  assign cv_promo_kit = false
  assign cv_promo_forn = 'forn-82275'
""")
# 2. card map with kit / gender / image
rep(""","a":{{ p.available | json }},"t":{{ p.title | json }}}""",
    ""","a":{{ p.available | json }},"t":{{ p.title | json }},"k":{%- if p.tags contains 'kit' -%}true{%- else -%}false{%- endif -%},"g":{%- if p.tags contains 'mujer' -%}"mujer"{%- elsif p.tags contains 'hombre' -%}"hombre"{%- else -%}""{%- endif -%},"img":{{ p.featured_image | image_url: width: 700 | json }}}""")
rep("""      return (cardMap[handle] = { id: p.id, f: fornOf(tags), v: v ? v.id : null, a: !!p.available, t: p.title });""",
    """      return (cardMap[handle] = { id: p.id, f: fornOf(tags), v: v ? v.id : null, a: !!p.available, t: p.title, k: tags.indexOf('kit') > -1,
        g: tags.indexOf('mujer') > -1 ? 'mujer' : (tags.indexOf('hombre') > -1 ? 'hombre' : ''), img: p.featured_image ? img(p.featured_image, 700) : '' });""")
# 3. CFG
rep("""    tarjetas: {{ cv_atc_tarjetas | json }}
  };""", """    tarjetas: {{ cv_atc_tarjetas | json }},
    promo: {{ cv_promo_kit | json }},
    promoForn: {{ cv_promo_forn | json }}
  };""")
# 4. hook
rep("""          open();
          flash('Agregado al carrito');""", """          return promoKit(inf).then(function (mostro) { if (!mostro) { open(); flash('Agregado al carrito'); } });""")

CSS = open(r'C:/Users/PICHAU/Downloads/CARRINHO-LOJA/_trabalho/v2/promo.css', encoding='utf-8').read()
JS = open(r'C:/Users/PICHAU/Downloads/CARRINHO-LOJA/_trabalho/v2/promo.js', encoding='utf-8').read()
rep("""
</style>""", "\n" + CSS + "</style>")
rep("""  window.__cvCart = { open: open, close: close, refresh: refresh, openCOD: openCOD, toast: toast };""",
    JS + """
  window.__cvCart = { open: open, close: close, refresh: refresh, openCOD: openCOD, toast: toast };""")
open(p, 'w', encoding='utf-8').write(s)
print("ok")
