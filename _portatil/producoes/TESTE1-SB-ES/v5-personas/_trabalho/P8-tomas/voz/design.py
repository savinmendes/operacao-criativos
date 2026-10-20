import sys, json, requests, base64
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
H={"xi-api-key":chave(),"Content-Type":"application/json"}
def sub(): return requests.get("https://api.elevenlabs.io/v1/user/subscription",headers=H,timeout=60).json().get("character_count")
a=sub()
desc=("A 65-year-old humble man from Bogotá, Colombia, with a natural Andean Colombian (rolo / cundiboyacense) Spanish accent. "
      "Elderly, slightly hoarse and worn voice, warm, gentle and a bit tired, speaking slowly and sincerely, like a poor street candy vendor "
      "telling his story to a TV reporter. Clear studio recording, no background noise.")
txt=("Esa noche conté las monedas, y no alcanzaba ni para el pasaje de vuelta. Me sentí un viejo que ya no le sirve a nadie. "
     "Mi hijo me mandó la transmisión del padre Juan Méndez, y la hice esa misma noche, como él enseña.")
r=requests.post("https://api.elevenlabs.io/v1/text-to-voice/design",headers=H,json=dict(voice_description=desc,text=txt,model_id="eleven_multilingual_ttv_v2",guidance_scale=5),timeout=300)
print(r.status_code, r.text[:300] if r.status_code!=200 else "")
d=r.json(); out=[]
for k,p in enumerate(d.get("previews",[])):
    open(f"voz/prev{k}.mp3","wb").write(base64.b64decode(p["audio_base_64"])); out.append(dict(k=k,gid=p["generated_voice_id"],dur=p.get("duration_secs")))
json.dump(dict(desc=desc,txt=txt,previews=out),open("voz/design.json","w"),indent=1)
print(out, "creditos", (sub() or 0)-(a or 0))
