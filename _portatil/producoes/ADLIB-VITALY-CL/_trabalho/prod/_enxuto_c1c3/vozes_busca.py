# -*- coding: utf-8 -*-
"""Lista info das vozes conhecidas e busca vozes femininas maduras em espanhol (sem imprimir chave)."""
import sys, json, urllib.request, urllib.parse
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import tts_elevenlabs as T
K = T.chave()
def get(url):
    r = urllib.request.Request(url, headers={"xi-api-key": K})
    return json.loads(urllib.request.urlopen(r, timeout=60).read())
for vid in ["uHo8F3FY11rc2LxCwDSB", "cIBxLwfshLYhRB9lCXEg"]:
    try:
        v = get(f"https://api.elevenlabs.io/v1/voices/{vid}")
        print(vid, v.get("name"), v.get("labels"), v.get("category"))
    except Exception as e:
        print(vid, "erro", e)
res = {}
for age in ["old", "middle_aged"]:
    for q in [dict(language="es", accent="chilean"), dict(language="es", accent="latin american"), dict(language="es")]:
        p = dict(page_size=60, gender="female", age=age, **q)
        try:
            d = get("https://api.elevenlabs.io/v1/shared-voices?" + urllib.parse.urlencode(p))
        except Exception as e:
            print("erro", e); continue
        for v in d.get("voices", []):
            res[v["voice_id"]] = (age, v.get("accent"), v.get("name"), v.get("descriptive"), v.get("use_case"), v.get("preview_url"), v.get("public_owner_id"), v.get("cloned_by_count"))
for k, v in sorted(res.items(), key=lambda x: -(x[1][7] or 0))[:40]:
    print(k, v[:5], v[7])
json.dump(res, open("vozes_maduras.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
