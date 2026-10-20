import sys, json, urllib.request, urllib.parse
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import tts_elevenlabs as T
K = T.chave()
for g in ["female"]:
    p = dict(page_size=100, gender=g, language="es", accent="chilean")
    r = urllib.request.Request("https://api.elevenlabs.io/v1/shared-voices?" + urllib.parse.urlencode(p), headers={"xi-api-key": K})
    d = json.loads(urllib.request.urlopen(r, timeout=60).read())
    for v in d["voices"]: print(v["voice_id"], v.get("age"), v.get("name"), v.get("descriptive"), v.get("use_case"), v.get("cloned_by_count"), v.get("free_users_allowed"))
