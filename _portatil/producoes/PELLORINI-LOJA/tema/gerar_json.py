# -*- coding: utf-8 -*-
"""Gera os JSON do tema Pellorini (product.pelvini, header-group, footer-group, index) a partir do conteúdo original."""
import json

css_prod = "<style>.pvp__rate{display:none!important}.pvp__ccn{display:none!important}.pvp__ccc>div:nth-of-type(2){display:none!important}</style>"


def feat(icon, t, s):
    return {"type": "feature", "settings": {"icon": f"shopify://shop_images/{icon}", "title": t, "sub": s}}


def why(t, s):
    return {"type": "why", "settings": {"title": t, "sub": s}}


blocks = {
    "f0": feat("pv-f-steel.png", "316L Stainless Steel", "Surgical-grade alloy"),
    "f1": feat("pv-f-crystal.png", "Scratch-Resistant Face", "No anxiety wear"),
    "f2": feat("pv-f-quartz.png", "Quartz Movement", "Precision timekeeping"),
    "f3": feat("pv-f-water.png", "3ATM Waterproof", "Rain & splash safe"),
    "f4": feat("pv-f-bracelet.png", "Adjustable Bracelet", "Fits all wrists"),
    "f5": feat("pv-f-date.png", "Day/Date Display", "Dual function dial"),
    "w0": why("Affordable Luxury", "Premium materials, no luxury markup."),
    "w1": why("24-Month Warranty", "Full coverage on every component. We stand behind our craft."),
    "w2": why("90-Day Money Back", "No questions asked. Return for a full refund if it's not for you."),
    "w3": why("Buy 1 Get 1 Free", "Two watches for the price of one. Pick any two colors."),
}
for i in range(1, 7):
    blocks[f"l{i}"] = {"type": "life", "settings": {"image": f"shopify://shop_images/pv-life-{i}.png"}}
caps = [("Cheap look, loose fit", True), ("Clean Look, Fits Perfectly", False), ("Clean Look · Fits Perfectly", False),
        ("Alloy, lightweight, tarnishes easily", True), ("Adjustable · No Tarnish · Built to Last", False),
        ("Adjustable · No Tarnish · Built to Last", False), ("Mineral glass", True), ("Scratch-resistant", False),
        ("Scratch-resistant", False)]
for i, (cap, bad) in enumerate(caps):
    blocks[f"c{i}"] = {"type": "cmp", "settings": {"image": f"shopify://shop_images/pv-cmp-{i+1}.png", "caption": cap, "bad": bad}}
order = ["f0", "f1", "f2", "f3", "f4", "f5", "w0", "w1", "w2", "w3", "l1", "l2", "l3", "l4", "l5", "l6"] + [f"c{i}" for i in range(9)]


def it(mi, h, t, rev):
    return {"type": "pv-imgtext", "settings": {"media_index": mi, "heading": h, "text": t, "reverse": rev}}


def rv(d, n, h, t):
    return {"type": "review", "settings": {"date": d, "name": n, "heading": h, "text": t}}


prod = {"sections": {
    "announce": {"type": "pv-announce", "settings": {"bold": "Buy 1 Get 1 Free", "text": "- While Stock Lasts", "brand": "PELLORINI", "minutes": 45}},
    "main": {"type": "pv-product", "blocks": blocks, "block_order": order, "settings": {
        "collection_products": ["pelvini-maretti-1", "pelvini-opulent", "pelvini-milano", "pelvini-dominante", "pelvini-lucent", "pelvini-napoli"],
        "brand": "Pellorini", "rating_text": "", "tab2": "Why Pellorini", "cmp_title": "See how Pellorini compares"}},
    "must": {"type": "pv-must-have", "settings": {"title": "MUST HAVE", "products": ["pelvini-adjustment-tool", "pelvini-silk-cleaning-cloth"]}},
    "it1": it(2, "Become the Man", "Success isn’t claimed—it’s earned. Pellorini watches are crafted for men who command respect, exude confidence, and embrace their status. Wear your legacy. Pellorini is more than a timepiece—it's a statement.", False),
    "it2": it(3, "The $10K Look", "Made with quality materials and built to be worn for years. Pellorini gives you the unmistakable $10K look and feel, without the $10K price tag.", True),
    "it3": it(4, "Timeless Strength", "Every Pellorini timepiece is a statement of strength and refinement. Designed for the modern man, each watch features scratch-resistant faces, precision-engineered bracelets, and rigorous testing to ensure unmatched durability and timeless sophistication.", False),
    "it4": it(5, "Effortless Elegance", "The Pellorini man exudes effortless charisma and style. With water-resistant strength and refined elegance, his timepiece makes a statement—get ready for the compliments.", True),
    "reviews": {"type": "pv-reviews", "disabled": True, "blocks": {
        "r0": rv("01/12/2026", "Hakam Ktaish", "Beautiful Experience from Dubai ❤️", "Forget the price. Pelvini is just one of the finest watches you could ever buy. Amazing quality. Fancy watch on your wrist. Attention grabbing, especially the silver one. I bought the silver for me and the golden for my father in law, he is so happy with it. The way it shines, just magnificent."),
        "r1": rv("01/10/2026", "Joseph Smith", "They look great for the price.", "I bought them in December and they came in January because of all the delivery traffic. They look great for the price. Some other companies sell them $10 more for the same exact watch."),
        "r2": rv("01/20/2026", "Kevin Oliveira", "Muito lindo", "Muito lindo, super estiloso 🔥"),
        "r3": rv("03/23/2026", "Anonymous", "Muy bonitos", "Tardó dos semanas en llegar pero a ser sincera están muy bonitos, son de buena calidad y trae su propio desarmador para quitar piezas si queda grande.")},
        "block_order": ["r0", "r1", "r2", "r3"], "settings": {}},
    "footer": {"type": "pv-footer", "settings": {"brand": "Pellorini", "text1": "Each Pellorini timepiece is accompanied by a 2-year international warranty."}},
    "cart": {"type": "pv-cart-drawer", "settings": {"upsells": ["pelvini-parchment-gift-bag", "premium-pelvini-box"], "trust": "Secure checkout · 90-Day Money Back · 24-Month Warranty"}},
    "wheel": {"type": "pv-wheel", "settings": {"segments": "5% OFF,10% OFF,TRY AGAIN,15% OFF,20% OFF,NEXT TIME", "win_index": 2, "won_title": "You won an extra [prize]!", "won_text": "Your code has been applied to your cart and will show at checkout."}},
    "pell_fix": {"type": "custom-liquid", "settings": {"custom_liquid": css_prod, "color_scheme": "scheme-1", "padding_top": 0, "padding_bottom": 0}}},
    "order": ["announce", "main", "must", "it1", "it2", "it3", "it4", "reviews", "footer", "cart", "wheel", "pell_fix"]}

hdr = {"name": "t:sections.header.name", "type": "header", "sections": {
    "announcement-bar": {"type": "announcement-bar", "blocks": {
        "a1": {"type": "announcement", "disabled": True, "settings": {"text": "NEW: Silk Peptide EGF Toner. Shop now!", "link": "shopify://products/silk-peptide-egf-toner-duo"}},
        "a2": {"type": "announcement", "settings": {"text": "Free tracked worldwide shipping · 90-day money-back guarantee", "link": ""}}},
        "block_order": ["a1", "a2"], "settings": {"auto_rotate": True, "change_slides_speed": 4, "color_scheme": "scheme-5", "show_line_separator": False, "show_social": False, "enable_country_selector": False, "enable_language_selector": False}},
    "header": {"type": "header", "settings": {"logo_position": "middle-left", "mobile_logo_position": "left", "menu": "main-menu", "menu_type_desktop": "dropdown", "sticky_header_type": "on-scroll-up", "show_line_separator": False, "color_scheme": "scheme-1", "menu_color_scheme": "scheme-1", "enable_country_selector": False, "enable_language_selector": False, "margin_bottom": 0, "padding_top": 8, "padding_bottom": 8}}},
    "order": ["announcement-bar", "header"]}


def tr(icon, text):
    return {"type": "trust", "settings": {"icon": icon, "text": text, "link": ""}}


ftr = {"type": "footer", "name": "t:sections.footer.name", "sections": {
    "ppfooter": {"type": "pp-footer", "blocks": {
        "about": {"type": "text", "settings": {"title": "About Essiora", "text": "<p>Timeless watches built to last, without the luxury markup. Free tracked worldwide shipping and a 90-day money-back guarantee.</p>"}},
        "shop": {"type": "menu", "settings": {"title": "Shop", "menu": "main-menu"}},
        "help": {"type": "menu", "settings": {"title": "Customer Care", "menu": "footer"}},
        "t1": tr("shield", "90-Day Money-Back Guarantee"), "t2": tr("truck", "Free Tracked Worldwide Shipping"),
        "t3": tr("lock", "Secure Checkout"), "t4": tr("star", "Ships Worldwide")},
        "block_order": ["about", "shop", "help", "t1", "t2", "t3", "t4"],
        "settings": {"bg": "#121212", "text": "#FFFFFF", "btn_bg": "#5B2BD8", "btn_text": "#FFFFFF", "pad_top": 44, "news_title": "Join the", "news_title2": "Essiora Club",
                     "news_text": "New arrivals, early access to limited drops and members-only offers, straight to your inbox.", "news_placeholder": "Enter your email",
                     "news_button": "Subscribe", "news_success": "Thank you! You're on the list.", "show_payment": True, "copyright": "All rights reserved."}},
    "scratch": {"type": "pp-scratch-popup", "settings": {"enabled": True, "delay": 5, "days": 7, "bg": "shopify://shop_images/f3962fc4-bcbc-4d2e-a1f7-da8a6ec3ce1d.jpg", "dim": 55, "overlay": "#1c1530", "accent": "#5B2BD8", "title": "Try your luck", "subtitle": "Scratch below to see what you win", "prize_big": "10% OFF", "prize_small": "your first order", "won_text": "You won 10% off! Enter your email to claim it.", "email_placeholder": "Enter your email", "claim_button": "Claim my 10% off", "code": "LUCKY10", "shop_button": "Shop now", "fine_print": "Your discount is applied automatically at checkout.", "no_thanks": "No thanks"}}},
    "order": ["ppfooter", "scratch"]}

for nome, obj in [("product.pelvini.json", prod), ("header-group.json", hdr), ("footer-group.json", ftr)]:
    json.dump(obj, open(nome, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# index.json: só os 2 textos de envio (o resto da home não foi mexido)
idx_trust_old, idx_trust_new = "Ships From the UK", "Ships Worldwide"
idx_faq_old = "Orders ship from the UK with tracked delivery."
idx_faq_new = "Orders ship worldwide with free tracked delivery."
print("ok")
