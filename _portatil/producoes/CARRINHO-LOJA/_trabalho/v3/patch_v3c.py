p = r"C:\Users\PICHAU\Downloads\CARRINHO-LOJA\novos-v3\snippets__cv-carrito.liquid"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:70])
    s = s.replace(a, b)
# comentario de ajustes
rep("""  Proveedor: etiqueta del producto "forn-<id del proveedor en Dropi>" (ej: forn-82275).""",
"""  Proveedor: etiqueta del producto "forn-<id del proveedor en Dropi>" (ej: forn-82275).
  v3 (regla de la dueña): todo esto (botón en tarjetas, "Completa tu pedido", rasca y gana, traba de proveedor)
  SOLO vale para productos que tengan TAMBIÉN la etiqueta cv_cat ('perfumes-arabes'). Un producto con forn- pero sin
  perfumes-arabes se trata como si no tuviera proveedor (no recibe botón ni sugerencias ni promo).""")
rep("""  assign cv_rsi_precio_linea = true
""", """  assign cv_rsi_precio_linea = true
  assign cv_cat = 'perfumes-arabes'
""")
# Liquid: pagina de producto
rep("""  if template.name == 'product' and product
    assign cv_es_producto = true
    for t in product.tags""", """  if template.name == 'product' and product
    assign cv_es_producto = true
    for t in product.tags
      unless product.tags contains cv_cat
        break
      endunless""")
# Liquid: mapa de tarjetas
rep("""    {%- for t in p.tags -%}{%- assign cv_pre = t | slice: 0, 5 -%}""",
"""    {%- for t in p.tags -%}{%- unless p.tags contains cv_cat -%}{%- break -%}{%- endunless -%}{%- assign cv_pre = t | slice: 0, 5 -%}""")
# JS: config + fornOf + buscarForn
rep("""    rsiLinea: {{ cv_rsi_precio_linea | json }}
  };""", """    rsiLinea: {{ cv_rsi_precio_linea | json }},
    cat: {{ cv_cat | json }}
  };""")
rep("""  function fornOf(tags) { for (var i = 0; i < tags.length; i++) if (tags[i].indexOf('forn-') === 0) return tags[i]; return ''; }""",
"""  // v3: el proveedor solo cuenta si el producto también es de la categoría (perfumes-arabes). Si no, '' (= sin proveedor).
  function fornOf(tags) { if (!tags || tags.indexOf(CFG.cat) < 0) return ''; for (var i = 0; i < tags.length; i++) if (tags[i].indexOf('forn-') === 0) return tags[i]; return ''; }""")
rep("""      return ps.filter(function (p) { p._tags = p.tags || []; return p._tags.indexOf(forn) > -1 && p.variant; });""",
"""      return ps.filter(function (p) { p._tags = (p.tags || []).map(function (x) { return String(x).toLowerCase(); }); return p._tags.indexOf(forn) > -1 && p._tags.indexOf(CFG.cat) > -1 && p.variant; });""")
# JS: promo sin memoria
rep("""  // Una vez por sesión y por carrito, solo si el carrito no tiene unitario. El precio lo pone el descuento automático de Shopify.
  function ssGet(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function ssSet(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  function promoKit(inf) {
    if (!CFG.promo || !inf || !inf.k || inf.f !== CFG.promoForn) return Promise.resolve(false);
    return getCart().then(function (c) {
      var key = 'cvPromo:' + (c.token || '');
      if (ssGet(key)) return false;
      return cartForn(c)""",
"""  // v3: SIN memoria. Abre (sin raspar) cada vez que se agrega un kit desde una tarjeta y el carrito todavía no tiene
  // unitario, aunque el cliente ya haya raspado o dicho "No, gracias" antes. El límite de 1 por pedido lo pone el descuento.
  // Limpia las marcas que dejó la v2 (sessionStorage 'cvPromo:<token>') para que quien ya lo vio lo vea de nuevo.
  (function limpiarPromoV2() {
    [function () { return window.sessionStorage; }, function () { return window.localStorage; }].forEach(function (g) {
      try { var st = g(); for (var i = st.length - 1; i >= 0; i--) { var k = st.key(i); if (k && k.indexOf('cvPromo') === 0) st.removeItem(k); } } catch (e) {}
    });
  })();
  function promoKit(inf) {
    if (!CFG.promo || !inf || !inf.k || inf.f !== CFG.promoForn) return Promise.resolve(false);
    return getCart().then(function (c) {
      return cartForn(c)""")
rep("""          if (!singles.length) return false;
          ssSet(key, '1');
""", """          if (!singles.length) return false;
""")
assert "ssGet" not in s and "ssSet" not in s
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
