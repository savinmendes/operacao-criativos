import os, requests, json, base64
from dotenv import load_dotenv
load_dotenv(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
k=os.environ["ELEVENLABS_API_KEY"]; V="BPwS5yO6aXvwg8auqNwS"
L={"L4_oferta":"Tres perfumes árabes al precio de uno.",
"L5_dia":"En el día, Armaf Club. Fresco, masculino y poderoso. Ahora me piden la carta solo pa' olerme.",
"L6_noche":"En la noche, Lattafa Asad. Intenso y seductor. Mi señora ya no me deja ni lavar la loza.",
"L7_finde":"Y el fin de semana, Afnan Nine PM. Elegante y moderno.",
"L8_cta":"Los tres te llegan a la casa y pagas cuando los recibes. ¡Pídelo ahora!"}
for n,t in L.items():
    r=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{V}/with-timestamps",headers={"xi-api-key":k},
      json={"text":t,"model_id":"eleven_multilingual_v2","language_code":"es","voice_settings":{"stability":0.45,"similarity_boost":0.8,"style":0.3}},timeout=120)
    if not r.ok: print(n,r.status_code,r.text[:300]); continue
    d=r.json(); open(f"audio/{n}.mp3","wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"],open(f"audio/{n}.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
    print(n,"ok",round(d["alignment"]["character_end_times_seconds"][-1],2), r.headers.get("x-character-count"))
