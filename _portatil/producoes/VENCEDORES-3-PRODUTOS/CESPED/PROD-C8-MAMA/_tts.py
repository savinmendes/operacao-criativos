# -*- coding: utf-8 -*-
import json,base64,sys,requests
from dotenv import dotenv_values
K=dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
V="dQafQNlqLLJDepKplzjl"
L={"L3_antes":"Hasta que probé esta.",
 "L4_mecanismo":"Es cortapasto, orilladora y bordeadora en uno. Tiene ruedas, así que la usas con una sola mano. Cuchilla de metal reforzada: olvídate de los hilos que se cortan. Y es inalámbrica, con dos baterías.",
 "L6_cta":"Despacho gratis a todo Chile, pagas al recibir y tienes noventa días de garantía. Toca el botón y pídela."}
for n,t in L.items():
    if len(sys.argv)>1 and n not in sys.argv[1:]: continue
    r=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{V}/with-timestamps",headers={"xi-api-key":K},
      json={"text":t,"model_id":"eleven_multilingual_v2","language_code":"es","voice_settings":{"stability":0.5,"similarity_boost":0.8,"style":0.2,"speed":1.12}})
    r.raise_for_status(); d=r.json()
    open(f"audio/{n}.mp3","wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"],open(f"audio/{n}.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
    print(n,d["alignment"]["character_end_times_seconds"][-1])
