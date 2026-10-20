import sys, requests; sys.path.insert(0,"ferramentas"); import tts_elevenlabs as T
H={"xi-api-key":T.chave()}
r=requests.get("https://api.elevenlabs.io/v2/voices",headers=H,params={"page_size":100,"include_total_count":True}).json()
vs=r["voices"]; tok=r.get("next_page_token")
while r.get("has_more"):
    r=requests.get("https://api.elevenlabs.io/v2/voices",headers=H,params={"page_size":100,"next_page_token":r["next_page_token"]}).json(); vs+=r["voices"]
print(len(vs))
for v in vs:
    l=v.get("labels") or {}
    print(v["voice_id"], v["category"], "|", v["name"], "|", l.get("gender"), l.get("accent"), l.get("language"), l.get("age"))
