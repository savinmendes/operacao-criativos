import json, base64, re, os, glob

SRC = r"C:/Users/PICHAU/.claude/projects/c--Users-PICHAU-Downloads-Produtividade-com-ia/b1265e31-6073-4e56-bb4d-84393cd16696/tool-results/artifact-0406ff45-1790358812-bf31.html"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "banco-san-benito.html")
IDX = r"C:/Users/PICHAU/Downloads/SB-BANCO-BROLL/indice_geral.json"

USOS = [
    ("gancho", "Gancho e choque", "Abrir o vídeo e prender o olho nos primeiros segundos"),
    ("dor", "Dor e bloqueio", "Portas fechadas, solidão, vergonha, rezar sem resposta"),
    ("dinheiro", "Dinheiro e dívidas", "Contas na mesa, moedas, geladeira vazia, negócio parado"),
    ("ataque", "Ataque e inveja", "Energia pesada, inveja, proteção espiritual"),
    ("oracao", "Oração e fé", "Rezar, terço, velas, igreja, devoção do dia a dia"),
    ("autoridade", "San Benito e mosteiro", "Monges, abadia, medalha: prova de origem e autoridade"),
    ("mecanismo", "Forma correta", "Manuscrito, instruções, detalhe da medalha, o segredo"),
    ("virada", "Virada e sinal", "Luz entrando, porta abrindo, correntes quebrando"),
    ("alivio", "Alívio e prosperidade", "Família, fila de clientes, mesa farta, boa notícia"),
    ("urgencia", "Urgência e tempo", "Ampulheta, portal fechando, última vela, sino"),
    ("cta", "Live e chamada", "Celular, transmissão ao vivo, toque na tela, comentários"),
    ("respiro", "Natureza e respiro", "Paisagens para transição e pausa entre blocos"),
]

# Classificação dos clipes já existentes (uso principal primeiro)
EXIST = {
 "01":"virada","02":"urgencia dor","03":"virada alivio","04":"virada","05":"virada","06":"virada mecanismo",
 "07":"dor gancho","08":"dor","09":"urgencia","10":"oracao mecanismo","11":"cta","12":"dor","13":"mecanismo autoridade",
 "14":"autoridade mecanismo","15":"autoridade","16":"autoridade mecanismo","17":"ataque","18":"virada ataque","19":"cta",
 "20":"virada","21":"urgencia","22":"gancho virada","23":"virada","24":"virada","25":"virada dor","26":"oracao",
 "27":"urgencia dor","28":"mecanismo","29":"virada","30":"gancho cta","31":"autoridade","32":"autoridade",
 "33":"autoridade mecanismo","34":"mecanismo autoridade","35":"oracao autoridade","36":"oracao ataque","37":"dor",
 "38":"dor urgencia","39":"virada","40":"ataque dor","41":"dor","42":"ataque","43":"respiro oracao","44":"oracao virada",
 "45":"oracao","46":"alivio","47":"virada","48":"virada","49":"virada ataque","50":"cta","52":"urgencia gancho",
 "53":"urgencia","54":"virada","55":"oracao","56":"virada","57":"alivio","58":"mecanismo virada","59":"mecanismo",
 "60":"virada","61":"dor ataque","62":"mecanismo","63":"alivio","64":"urgencia","65":"alivio","66":"virada",
 "67":"ataque oracao","68":"mecanismo","69":"autoridade","70":"ataque virada","71":"virada dor","72":"virada",
 "73":"mecanismo oracao","75":"cta","76":"dor","77":"alivio","78":"gancho mecanismo","79":"urgencia","80":"cta",
 "81":"dor","82":"dor","83":"dor dinheiro","84":"oracao dor","85":"dor","86":"dor ataque","87":"dor","88":"cta",
 "89":"urgencia mecanismo","90":"cta","91":"dinheiro","92":"alivio","93":"alivio","94":"oracao","95":"dor urgencia",
 "96":"mecanismo","97":"mecanismo","98":"virada mecanismo","99":"alivio","100":"oracao",
}

# Classificação dos clipes novos (Lote 5) por número dentro do tema
NOVO = {
 "oracion": {"05":"oracao virada","13":"oracao dor","16":"oracao dor","17":"oracao dor","22":"oracao autoridade",
             "23":"oracao autoridade","24":"oracao ataque","25":"oracao ataque","28":"oracao virada","*":"oracao"},
 "problema": {"01":"dinheiro","02":"dinheiro","03":"dinheiro","04":"dinheiro","07":"dinheiro dor","08":"dinheiro dor",
              "09":"dinheiro dor","10":"dinheiro dor","15":"dor urgencia","18":"dinheiro","19":"dinheiro",
              "22":"dinheiro dor","24":"dinheiro","26":"dinheiro dor","27":"dinheiro","30":"dor dinheiro","*":"dor"},
 "alivio": {"01":"virada alivio","02":"virada alivio","25":"virada alivio","26":"virada alivio","27":"respiro virada",
            "28":"respiro virada","29":"virada respiro","30":"virada respiro","*":"alivio"},
 "sagrado": {"05":"autoridade oracao","06":"autoridade oracao","07":"mecanismo autoridade","08":"mecanismo autoridade",
             "09":"mecanismo autoridade","10":"mecanismo autoridade","11":"respiro autoridade","12":"respiro autoridade",
             "13":"urgencia autoridade","14":"urgencia autoridade","15":"oracao autoridade","16":"oracao autoridade",
             "17":"virada autoridade","18":"virada autoridade","21":"autoridade mecanismo","22":"autoridade mecanismo",
             "25":"respiro virada","26":"respiro ataque","27":"oracao autoridade","28":"oracao autoridade",
             "29":"respiro virada","30":"respiro virada","31":"cta","32":"cta","33":"cta","34":"cta","35":"cta","*":"autoridade"},
}
TEMA_PT = {"oracion":"Oração","problema":"Problema","alivio":"Alívio","sagrado":"Sagrado"}

h = open(SRC, encoding="utf-8").read()
lines = h.split("\n")
items = json.loads(lines[106][len("const ITEMS = "):].rstrip().rstrip(";"))

for it in items:
    if it["id"].startswith("SB-NAT"):
        it["usos"] = ["respiro", "oracao"] if it["id"] == "SB-NAT-13" else ["respiro"]
    else:
        k = it["id"].split("-")[-1].lstrip("0") or "0"
        k = k.zfill(2) if len(k) < 2 else k
        it["usos"] = EXIST[k].split()

# Novos
ids = {}
for f in glob.glob(os.path.join(HERE, "map*.txt")):
    for ln in open(f, encoding="utf-8"):
        if ln.strip():
            a, b = ln.split(); ids[a] = b
idx = {d["arquivo"][:-4]: d for d in json.load(open(IDX, encoding="utf-8"))}

def g(d, *ks):
    for k in ks:
        v = d.get(k)
        if v not in (None, ""): return v
    return None

novos = []
n = 101
for tema in ["oracion", "problema", "alivio", "sagrado"]:
    for name in sorted(k for k in ids if k.startswith(tema + "_")):
        d = idx[name]
        num = name.split("_")[1]
        usos = (NOVO[tema].get(num) or NOVO[tema]["*"]).split()
        scene = " ".join(w.capitalize() for w in name.split("_", 2)[2].split("-"))
        ini = g(d, "util_in", "in", "in_s") or 0
        fim = g(d, "util_out", "out", "out_s")
        obs = (g(d, "obs") or "").strip()
        uso_txt = f"usar {float(ini):.1f}–{float(fim):.1f} s" if fim else ""
        poster = base64.b64encode(open(os.path.join(HERE, "poster", name + ".jpg"), "rb").read()).decode()
        novos.append({"id": f"SB-BRV-{n}", "n": n, "file": name, "scene": scene, "lote": 5,
                      "tag": TEMA_PT[tema] + (" · " + uso_txt if uso_txt else ""),
                      "desc": d["descricao"] + (f" — {obs}" if obs else ""),
                      "poster": "data:image/jpeg;base64," + poster,
                      "url": "/_blob/" + ids[name], "usos": usos})
        n += 1

allitems = items + novos
lines[106] = "const ITEMS = " + json.dumps(allitems, ensure_ascii=False) + ";"

# ---- HTML da seção de b-rolls ----
html = "\n".join(lines)
old_tools = html[html.index('  <div class="tools">\n    <div class="seg lote"'):html.index('  <div class="grid" id="grid"></div>')]
new_tools = '''  <div class="usebar" role="group" aria-label="Momento do roteiro">
    <button class="use" data-u="all" aria-pressed="true"><span class="un">Todos os momentos</span><span class="uc" id="uc-all"></span></button>
''' + "".join(f'''    <button class="use" data-u="{k}" aria-pressed="false"><span class="un">{nm}</span><span class="uc" id="uc-{k}"></span></button>
''' for k, nm, _ in USOS) + '''  </div>
  <p class="usehint" id="usehint">Escolha o momento do roteiro: cada clipe aparece em todos os momentos em que funciona, com o uso principal primeiro.</p>
  <div class="tools">
    <select id="lot" aria-label="Lote">
      <option value="all">Todos os lotes</option>
      <option value="1">Lote 1 · 01–50</option>
      <option value="2">Lote 2 · Pediste una señal</option>
      <option value="3">Lote 3 · UGC + Rezar mucho</option>
      <option value="4">Lote 4 · Belezas naturais</option>
      <option value="5">Lote 5 · Banco IA (oração, problema, alívio, sagrado)</option>
    </select>
    <input id="q" type="search" placeholder="Buscar cena, frase ou ID" aria-label="Buscar">
    <span class="count" id="count"></span>
  </div>

'''
html = html.replace(old_tools, new_tools)
html = html.replace('<span><b id="total">0</b> clipes</span>', '<span><b id="total">0</b> clipes</span><span><b id="totalu">12</b> momentos</span>')
html = html.replace('<p class="sub">B-rolls aprovados e imagens-base dos avatares dos criativos de San Benito. O nome de cada item bate com o arquivo usado na produção.</p>',
                    '<p class="sub">B-rolls aprovados e imagens-base dos avatares dos criativos de San Benito, organizados pelo momento do roteiro em que cada clipe funciona. O nome de cada item bate com o arquivo usado na produção.</p>')

css = '''
.usebar{display:flex;flex-wrap:wrap;gap:8px}
.use{display:inline-flex;align-items:baseline;gap:7px;border:1px solid var(--line);background:var(--surface);color:var(--ink);font:500 13px "IBM Plex Sans",sans-serif;padding:7px 12px;border-radius:999px;cursor:pointer}
.use .uc{font:500 11px "IBM Plex Mono",monospace;color:var(--muted);font-variant-numeric:tabular-nums}
.use[aria-pressed="true"]{background:var(--gold-soft);border-color:var(--gold);color:var(--ink)}
.use[aria-pressed="true"] .uc{color:var(--gold)}
.use:focus-visible,#lot:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.usehint{margin:-6px 0 0;color:var(--muted);font-size:13.5px;max-width:70ch}
#lot{background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:9px 10px;font:inherit;max-width:100%}
.grp{display:flex;flex-direction:column;gap:14px}
.grp + .grp{margin-top:18px;padding-top:22px;border-top:1px solid var(--line)}
.grp-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px}
.grp-h h2{font-family:Marcellus,"Times New Roman",serif;font-weight:400;font-size:22px;margin:0;text-wrap:balance}
.grp-h p{margin:0;color:var(--muted);font-size:13.5px}
.grp-h .n{font:500 12px "IBM Plex Mono",monospace;color:var(--gold)}
.usos{display:flex;flex-wrap:wrap;gap:4px}
.usos span{font-size:11px;line-height:1.3;padding:2px 7px;border-radius:5px;background:var(--chip);color:var(--muted)}
.usos span.p{background:var(--gold-soft);color:var(--ink)}
'''
html = html.replace("@media (prefers-reduced-motion: reduce)", css.strip() + "\n@media (prefers-reduced-motion: reduce)", 1)

# ---- script da seção de b-rolls (linhas 108–159 originais) ----
s_start = html.index("const grid = document.getElementById('grid');")
s_end = html.index("render();\n", s_start) + len("render();\n")
USOS_JS = json.dumps([{"k": k, "n": nm, "d": d} for k, nm, d in USOS], ensure_ascii=False)
new_script = '''const USOS = ''' + USOS_JS + ''';
const UN = Object.fromEntries(USOS.map(u => [u.k, u.n]));
const grid = document.getElementById('grid');
let F = 'all', U = 'all', Q = '';
try { F = localStorage.getItem('sb-lote') || 'all'; U = localStorage.getItem('sb-uso') || 'all'; } catch(e) {}
if (U !== 'all' && !UN[U]) U = 'all';
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function card(it){
  const tag = it.lote === 5 ? `${esc(it.desc)} <i>· ${esc(it.tag)}</i>` : it.lote === 4 ? `${esc(it.desc)} <i>· ${esc(it.tag)}</i>` : (it.lote >= 2 ? `<i>“${esc(it.tag)}”</i>` : esc(it.desc));
  const usos = (it.usos||[]).map((u,i) => `<span class="${i===0?'p':''}">${esc(UN[u]||u)}</span>`).join('');
  return `<article class="card" data-id="${it.id}">
    <div class="frame" tabindex="0" role="button" aria-label="Assistir ${esc(it.id)}">
      <img src="${it.poster}" alt="${esc(it.scene)}" loading="lazy">
      <span class="lote">L${it.lote}</span>
      <span class="play" aria-hidden="true"><svg viewBox="0 0 10 12"><path d="M0 0l10 6-10 6z"/></svg></span>
    </div>
    <div class="info">
      <div class="row"><span class="id">${esc(it.id)}</span><button class="copy" data-copy="${esc(it.file)}">Copiar nome</button></div>
      <span class="scene">${esc(it.scene)}</span>
      <div class="usos">${usos}</div>
      <span class="tag" title="${esc(it.lote>=2 && it.lote<4 ? it.tag+' — '+it.desc : it.desc+' · '+it.tag)}">${tag}</span>
    </div>
  </article>`;
}
function base(){
  const q = Q.trim().toLowerCase();
  return ITEMS.filter(it => (F==='all' || String(it.lote)===F) &&
    (!q || (it.id+' '+it.scene+' '+it.tag+' '+it.desc+' '+it.file+' '+(it.usos||[]).map(u=>UN[u]).join(' ')).toLowerCase().includes(q)));
}
function render(){
  const pool = base();
  document.getElementById('uc-all').textContent = pool.length;
  USOS.forEach(u => { document.getElementById('uc-'+u.k).textContent = pool.filter(it => (it.usos||[]).includes(u.k)).length; });
  let html = '', shown = 0;
  if (U === 'all') {
    USOS.forEach(u => {
      const g = pool.filter(it => (it.usos||[])[0] === u.k);
      if (!g.length) return;
      shown += g.length;
      html += `<section class="grp"><div class="grp-h"><h2>${esc(u.n)}</h2><span class="n">${g.length}</span><p>${esc(u.d)}</p></div><div class="grid">${g.map(card).join('')}</div></section>`;
    });
  } else {
    const u = USOS.find(x => x.k === U);
    const g = pool.filter(it => (it.usos||[]).includes(U)).sort((a,b) => (a.usos.indexOf(U)) - (b.usos.indexOf(U)));
    shown = g.length;
    if (g.length) html = `<section class="grp"><div class="grp-h"><h2>${esc(u.n)}</h2><span class="n">${g.length}</span><p>${esc(u.d)}</p></div><div class="grid">${g.map(card).join('')}</div></section>`;
  }
  grid.innerHTML = html || '<p class="empty">Nenhum clipe com esse filtro.</p>';
  document.getElementById('count').textContent = shown + ' de ' + ITEMS.length;
  document.querySelectorAll('.use').forEach(b => b.setAttribute('aria-pressed', b.dataset.u===U));
  document.getElementById('lot').value = F;
  const h = document.getElementById('usehint');
  h.textContent = U==='all' ? 'Escolha o momento do roteiro: cada clipe aparece em todos os momentos em que funciona, com o uso principal primeiro.' : (USOS.find(x=>x.k===U).d + '. Os de uso principal vêm primeiro.');
}
function play(frame){
  const it = ITEMS.find(x => x.id === frame.closest('.card').dataset.id);
  if (!it || !it.url || frame.querySelector('video')) return;
  document.querySelectorAll('.frame video').forEach(v => { const f=v.parentElement; v.remove(); f.querySelector('img').hidden=false; f.querySelector('.play').hidden=false; });
  const v = document.createElement('video');
  v.src = it.url; v.muted = true; v.loop = true; v.playsInline = true; v.autoplay = true; v.controls = true;
  frame.querySelector('img').hidden = true; frame.querySelector('.play').hidden = true;
  frame.appendChild(v); v.play().catch(()=>{});
}
grid.addEventListener('click', e => {
  const c = e.target.closest('.copy');
  if (c){
    const txt = c.dataset.copy;
    const done = () => { c.textContent='Copiado'; c.classList.add('ok'); setTimeout(()=>{c.textContent='Copiar nome'; c.classList.remove('ok');},1400); };
    navigator.clipboard && navigator.clipboard.writeText(txt).then(done).catch(()=>{ c.textContent = txt; });
    return;
  }
  const f = e.target.closest('.frame'); if (f) play(f);
});
grid.addEventListener('keydown', e => { if ((e.key==='Enter'||e.key===' ') && e.target.classList.contains('frame')) { e.preventDefault(); play(e.target); } });
document.querySelectorAll('.use').forEach(b => b.addEventListener('click', () => { U=b.dataset.u; try{localStorage.setItem('sb-uso',U);}catch(e){} render(); }));
document.getElementById('lot').addEventListener('change', e => { F=e.target.value; try{localStorage.setItem('sb-lote',F);}catch(e){} render(); });
document.getElementById('q').addEventListener('input', e => { Q = e.target.value; render(); });
document.getElementById('total').textContent = ITEMS.length;
render();
'''
html = html[:s_start] + new_script + html[s_end:]

# a grade passa a conter seções: remove o grid do contêiner externo
html = html.replace('<div class="grid" id="grid"></div>', '<div id="grid" class="groups"></div>')
html = html.replace(".grid{display:grid;", ".groups{display:flex;flex-direction:column}\n.grid{display:grid;", 1)

# remove o esqueleto adicionado pela publicação (a ferramenta envolve de novo)
pre = '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>'
if html.startswith(pre):
    html = html[html.index("</head><body>") + len("</head><body>"):]
html = html.replace("</body></html>", "").rstrip() + "\n"
open(OUT, "w", encoding="utf-8").write(html)
print("itens:", len(allitems), "novos:", len(novos), "tamanho MB:", round(len(html.encode())/1e6, 2))
from collections import Counter
print(Counter(i["usos"][0] for i in allitems))
