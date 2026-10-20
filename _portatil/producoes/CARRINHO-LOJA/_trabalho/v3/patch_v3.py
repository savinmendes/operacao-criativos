p = r"C:\Users\PICHAU\Downloads\CARRINHO-LOJA\novos-v3\snippets__cv-carrito.liquid"
s = open(p, encoding="utf-8").read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)

# 1) ajuste no topo
rep("""  - cv_fab ............... true = vuelve""",
"""  - cv_rsi_precio_linea .. true = dentro del formulario de Releasit (modo carrito) cada línea con descuento automático
                           muestra el precio original tachado + el precio con descuento (lee /cart.js final_line_price).
                           Releasit 455 siempre pinta original_line_price en la línea y no tiene ajuste para eso (v3).
  - cv_fab ............... true = vuelve""")
rep("""  assign cv_promo_forn = 'forn-82275'
""", """  assign cv_promo_forn = 'forn-82275'
  assign cv_rsi_precio_linea = true
""")
rep("""    promoForn: {{ cv_promo_forn | json }}
  };""", """    promoForn: {{ cv_promo_forn | json }},
    rsiLinea: {{ cv_rsi_precio_linea | json }}
  };""")

# 2) CSS: linea del popup + "Solo 1 por pedido" + precio tachado en Releasit
rep("""  .cvp__fine{margin:8px 0 0;""",
"""  .cvp__nota{margin:0 0 12px;padding:9px 12px;border:1px solid rgba(226,194,122,.4);border-radius:12px;background:rgba(226,194,122,.1);color:#f3e6c8;font-size:13.5px;line-height:1.4;text-align:center}
  .cvp__nota b{color:#fff}
  .cvp__solo{display:flex;justify-content:center;margin-top:12px}
  .cvp__solo span{display:inline-block;padding:4px 12px;border-radius:999px;background:#16110c;border:1px solid #e2c27a;color:#e2c27a;font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}
  .cvp__solo + .cvp__btn{margin-top:8px}
  ._rsi-modal-line-item-final-price .cv-rsi-s{display:block;color:#8a8a8a;font-size:.85em;font-weight:400;text-decoration:line-through}
  ._rsi-modal-line-item-final-price .cv-rsi-f{display:block;color:#c0392b;font-weight:700}
  .cvp__fine{margin:8px 0 0;""")

# 3) HTML del popup
rep("""      '<div class="cvp__step2"><div class="cvp__opts">' +""",
"""      '<div class="cvp__step2"><p class="cvp__nota">Oferta válida solo para <b>1 perfume adicional</b> por pedido: el 50% lo asumimos nosotros 🖤</p><div class="cvp__opts">' +""")
rep("""      '<button type="button" class="cvp__btn" data-cvp-add>""",
"""      '<div class="cvp__solo"><span>Solo 1 por pedido</span></div>' +
      '<button type="button" class="cvp__btn" data-cvp-add>""")

# 4) Precio con descuento por línea dentro del formulario de Releasit
rep("""  window.__cvCart = {""",
"""  // Releasit (v455) pinta cada línea con original_line_price, aunque el carrito tenga descuento automático
  // (el descuento solo aparece en el resumen). Acá se reescribe el precio de la línea: original tachado + final.
  // Solo actúa si las líneas del formulario coinciden 1 a 1 con /cart.js (mismo orden, variante y cantidad).
  function rsiFmt(c) {
    try { if (window._rsi && _rsi.u && _rsi.u.formatMoney) return _rsi.u.formatMoney(c, 'amount_with_comma_separator'); } catch (e) {}
    return '$' + Math.round(c / 100).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  }
  var rsiT = null, rsiBusy = false;
  function rsiPatch() {
    var filas = [].slice.call(document.querySelectorAll('._rsi-modal-line-item'));
    if (!filas.length || rsiBusy) return;
    rsiBusy = true;
    j('/cart.js?t=' + Date.now()).then(function (c) {
      var its = c.items || [];
      filas = [].slice.call(document.querySelectorAll('._rsi-modal-line-item'));
      filas.forEach(function (f) {
        var vin = f.querySelector('input[name^="item_variant_id["]'), qin = f.querySelector('input[name^="item_quantity["]');
        var pr = f.querySelector('._rsi-modal-line-item-final-price');
        if (!vin || !pr) return;
        var idx = Number((vin.name.match(/\[(\d+)\]/) || [])[1]);
        var it = its[idx];
        var ok = filas.length === its.length && it && String(it.variant_id) === String(vin.value) && (!qin || Number(qin.value) === it.quantity);
        var firma = ok ? it.original_line_price + '>' + it.final_line_price : '';
        if (pr.getAttribute('data-cv-firma') === firma && (firma || !pr.querySelector('.cv-rsi-f'))) return;
        if (ok && it.final_line_price < it.original_line_price) {
          pr.innerHTML = '<s class="cv-rsi-s">' + rsiFmt(it.original_line_price) + '</s><span class="cv-rsi-f">' + rsiFmt(it.final_line_price) + '</span>';
          pr.setAttribute('aria-label', 'Antes ' + rsiFmt(it.original_line_price) + ', ahora ' + rsiFmt(it.final_line_price));
        } else if (pr.querySelector('.cv-rsi-f')) {
          pr.textContent = ok ? rsiFmt(it.original_line_price) : pr.querySelector('.cv-rsi-s').textContent;
          pr.removeAttribute('aria-label');
        }
        pr.setAttribute('data-cv-firma', firma);
      });
    }).catch(function () {}).then(function () { rsiBusy = false; });
  }
  if (CFG.rsiLinea && window.MutationObserver) {
    new MutationObserver(function (ms) {
      for (var i = 0; i < ms.length; i++) {
        var t = ms[i].target;
        if (t.nodeType === 1 && t.closest && t.closest('._rsi-modal-line-item-final-price')) continue;
        if (t.nodeType === 1 && (t.querySelector && t.querySelector('._rsi-modal-line-item') || t.closest && t.closest('#_rsi-cod-form-modal, ._rsi-cod-form'))) {
          clearTimeout(rsiT); rsiT = setTimeout(rsiPatch, 120); return;
        }
      }
    }).observe(document.body, { childList: true, subtree: true });
    document.addEventListener('cv:rsi', rsiPatch);
  }

  window.__cvCart = {""")
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok", len(s.encode()))
