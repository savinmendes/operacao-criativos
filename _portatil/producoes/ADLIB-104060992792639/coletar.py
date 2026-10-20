# -*- coding: utf-8 -*-
"""Abre a Biblioteca de Anúncios (ordem por impressões), rola até achar N anúncios com vídeo e salva a lista em ordem."""
import json, sys, time, re
from playwright.sync_api import sync_playwright
URL = sys.argv[1]; N = int(sys.argv[2]); OUT = sys.argv[3]
JS = r"""
() => {
  const out = [];
  const seen = new Set();
  // cada card tem o texto "ID da biblioteca:" / "Library ID:"
  const nodes = Array.from(document.querySelectorAll('div')).filter(d => /(Library ID|Identificação da biblioteca|ID da biblioteca|Identificador de la biblioteca|Identificatore della libreria)[:：]\s*\d+/.test(d.innerText||'') && d.innerText.length < 4000);
  // menor div que contém um único ID = o card
  const cards = nodes.filter(d => (d.innerText.match(/(Library ID|Identificação da biblioteca|ID da biblioteca|Identificador de la biblioteca|Identificatore della libreria)/g)||[]).length === 1)
                     .filter(d => !Array.from(d.querySelectorAll('div')).some(c => c !== d && (c.innerText.match(/(Library ID|Identificação da biblioteca|ID da biblioteca)/g)||[]).length===1 && c.querySelector('video')===d.querySelector('video') && c.innerText.length > d.innerText.length*0.95 && false));
  for (const c of cards) {
    const m = c.innerText.match(/(?:Library ID|Identificação da biblioteca|ID da biblioteca|Identificador de la biblioteca|Identificatore della libreria)[:：]\s*(\d+)/);
    if (!m || seen.has(m[1])) continue;
    // sobe até o card conter mídia
    let card = c; for (let i=0;i<8 && card && !card.querySelector('video, img[src*="scontent"]'); i++) card = card.parentElement;
    const v = card ? card.querySelector('video') : null;
    seen.add(m[1]);
    out.push({id: m[1], video: v ? (v.currentSrc || v.src || (v.querySelector('source')||{}).src || null) : null,
              poster: v ? v.poster : null, texto: (card||c).innerText.slice(0, 600)});
  }
  return out;
}
"""
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(locale="pt-BR", viewport={"width": 1400, "height": 1000})
    pg.goto(URL, wait_until="domcontentloaded", timeout=90000)
    time.sleep(8)
    for btn in ["Permitir todos os cookies", "Allow all cookies", "Aceitar tudo", "Only allow essential cookies", "Recusar cookies opcionais"]:
        try: pg.get_by_role("button", name=btn).first.click(timeout=1500); break
        except Exception: pass
    ads = []
    for k in range(60):
        ads = pg.evaluate(JS)
        nv = sum(1 for a in ads if a["video"])
        print(f"[rolagem {k+1}] anúncios {len(ads)} | com vídeo {nv}", flush=True)
        if nv >= N: break
        pg.mouse.wheel(0, 4000); time.sleep(2.5)
    pg.screenshot(path=OUT.replace(".json", "_tela.png"), full_page=False)
    json.dump(ads, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    b.close()
