import sys, json, urllib.request, urllib.parse
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import tts_elevenlabs as T
K = T.chave()
def get(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"xi-api-key": K}), timeout=60).read())
for v in get("https://api.elevenlabs.io/v1/voices")["voices"]:
    l = v.get("labels") or {}
    print("CONTA", v["voice_id"], v["name"], l.get("gender"), l.get("age"), l.get("accent"))
for acc in ["chilean", "chile"]:
    d = get("https://api.elevenlabs.io/v1/shared-voices?" + urllib.parse.urlencode(dict(page_size=100, language="es", accent=acc)))
    for v in d.get("voices", []):
        print("SHARED", acc, v["voice_id"], v["name"], v.get("gender"), v.get("age"), v.get("accent"), v.get("public_owner_id"), v.get("use_case"))
