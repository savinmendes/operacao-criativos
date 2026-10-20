import json, os, re, hashlib, subprocess, urllib.request, datetime, csv
BASE = r"C:/Users/PICHAU/Downloads/ADLIB-VITALY-CL"
ads = json.load(open("ads_raw.json", encoding="utf-8")); ordem = json.load(open("raw/ordem_tela.json"))["ids"][:30]
def get(u, dst):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dst, "wb") as f: f.write(r.read())
def md5(p): return hashlib.md5(open(p, "rb").read()).hexdigest()
def probe(p):
    o = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height:format=duration","-of","json",p],capture_output=True,text=True).stdout
    j = json.loads(o); s = j["streams"][0]; return s["width"], s["height"], float(j["format"]["duration"])
def short(n): return re.sub(r'[^\w\- ]', '', n)[:28].strip()
seen = {}; rows = []; log = []
for i, aid in enumerate(ordem, 1):
    a = ads[aid]; s = a["snapshot"]; nn = f"{i:02d}"; pg = short(a["page_name"])
    files = []; res = []; dur = ""; dup = []; tipo = s["display_format"]
    medias = []
    for v in s["videos"]: medias.append(("v", v.get("video_hd_url") or v.get("video_sd_url"), bool(v.get("video_hd_url"))))
    for im in s["images"]: medias.append(("i", im.get("original_image_url") or im.get("resized_image_url"), True))
    for c in s.get("cards") or []:
        if c.get("video_hd_url") or c.get("video_sd_url"): medias.append(("v", c.get("video_hd_url") or c.get("video_sd_url"), bool(c.get("video_hd_url"))))
        elif c.get("original_image_url") or c.get("resized_image_url"): medias.append(("i", c.get("original_image_url") or c.get("resized_image_url"), True))
    multi = len(medias) > 1
    for k, (t, u, hd) in enumerate(medias, 1):
        suf = f"-{k}" if multi else ""
        if t == "v": dst = f"{BASE}/VIDEOS/{nn} - {pg} - {aid}{suf}.mp4"
        else: dst = f"{BASE}/IMAGENS/{nn} - {pg} - {aid}{suf}.jpg"
        get(u, dst); h = md5(dst)
        if h in seen:
            os.remove(dst); dup.append(seen[h]); files.append(f"(= {seen[h]})")
        else:
            seen[h] = os.path.basename(dst); files.append(os.path.basename(dst))
        if t == "v":
            p = dst if os.path.exists(dst) else f"{BASE}/VIDEOS/{seen[h]}"
            w, hh, d = probe(p); res.append(f"{w}x{hh}" + ("" if min(w,hh) >= 720 else " FONTE BAIXA") + ("" if hd else " (sem HD)")); dur = f"{d:.1f}"
        else:
            p = dst if os.path.exists(dst) else f"{BASE}/IMAGENS/{seen[h]}"
            w, hh, _ = probe(p) if False else (0,0,0)
            o = subprocess.run(["ffprobe","-v","error","-show_entries","stream=width,height","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip()
            res.append(o.replace(",","x"))
    body = ((s.get("body") or {}).get("text") or "").replace("\n"," ")
    rows.append([i, aid, f"https://www.facebook.com/ads/library/?id={aid}", a["page_name"],
        datetime.datetime.utcfromtimestamp(a["start_date"]).strftime("%Y-%m-%d"), ", ".join(a["publisher_platform"]),
        tipo, " | ".join(files), " | ".join(res), dur, body[:150], s.get("title") or "", s.get("cta_text") or "", s.get("link_url") or "",
        " | ".join(dup), a.get("collation_count") or 1])
    print(f"[{i}/30] {tipo} {files} {res}", flush=True)
with open(f"{BASE}/00-indice.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["n","ad_id","link_biblioteca","pagina","inicio","plataformas","tipo_midia","arquivos","resolucao","duracao_s","texto_150","titulo","cta","url_destino","duplicata_de","versoes_agrupadas"])
    w.writerows(rows)
