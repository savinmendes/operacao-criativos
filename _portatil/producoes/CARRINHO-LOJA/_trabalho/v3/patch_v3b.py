p = r"C:\Users\PICHAU\Downloads\CARRINHO-LOJA\novos-v3\snippets__cv-carrito.liquid"
s = open(p, encoding="utf-8").read()
a = s[s.index("  if (CFG.rsiLinea && window.MutationObserver) {"):s.index("  window.__cvCart = {")]
b = """  if (CFG.rsiLinea && window.MutationObserver) {
    new MutationObserver(function (ms) {
      var li = document.querySelector('._rsi-modal-line-item');
      if (!li) return;
      var caja = li.closest('#_rsi-cod-form-modal, form') || li.parentNode.parentNode || document.body;
      for (var i = 0; i < ms.length; i++) {
        var t = ms[i].target;
        if (t.nodeType !== 1) t = t.parentNode;
        if (!t || (t.closest && t.closest('._rsi-modal-line-item-final-price'))) continue;
        if (caja.contains(t) || t.contains(caja)) { clearTimeout(rsiT); rsiT = setTimeout(rsiPatch, 120); return; }
      }
    }).observe(document.body, { childList: true, subtree: true, characterData: true });
  }

"""
s = s.replace(a, b)
s = s.replace("""    if (!filas.length || rsiBusy) return;
    rsiBusy = true;""", """    if (!filas.length) return;
    if (rsiBusy) { rsiOtra = true; return; }
    rsiBusy = true; rsiOtra = false;""")
s = s.replace("var rsiT = null, rsiBusy = false;", "var rsiT = null, rsiBusy = false, rsiOtra = false;")
s = s.replace("}).catch(function () {}).then(function () { rsiBusy = false; });", "}).catch(function () {}).then(function () { rsiBusy = false; if (rsiOtra) rsiPatch(); });")
open(p, "w", encoding="utf-8", newline="").write(s)
