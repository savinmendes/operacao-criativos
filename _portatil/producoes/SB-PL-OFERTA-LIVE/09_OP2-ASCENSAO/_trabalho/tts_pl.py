import sys, json, base64, requests
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
VOZ="AkQxVSf1kENGmX9WjeDE"  # Jesus The Chosen (mesma do EN)
MOD=sys.argv[1]; vel=float(sys.argv[2]); suf=sys.argv[3]; nomes=sys.argv[4:] or ["hook","corpo"]
for n in nomes:
    t=open(f"audio/{n}_pl.txt",encoding="utf-8").read().strip()
    body={"text":t,"model_id":MOD,"voice_settings":{"stability":0.5,"similarity_boost":0.8,"style":0.0,"use_speaker_boost":True,"speed":vel}}
    if MOD!="eleven_multilingual_v2": body["language_code"]="pl"
    r=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps",params={"output_format":"mp3_44100_128"},headers={"xi-api-key":chave()},json=body,timeout=300)
    if not r.ok: print(n,r.status_code,r.text[:300]); continue
    d=r.json()
    open(f"audio/{n}_pl{suf}.mp3","wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"],open(f"audio/{n}_pl{suf}.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
    print(n,len(t),"chars", d["alignment"]["character_end_times_seconds"][-1],"s")
