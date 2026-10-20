import sys,json,base64,requests
sys.path.insert(0,'ferramentas')
from tts_elevenlabs import chave
D='C:/Users/PICHAU/Downloads/SB-VENCEDORES_OP2-ASCENSAO_JESU-V07/_trabalho/v07/audio/'
txt="Appuie sur « En savoir plus » maintenant."
r=requests.post("https://api.elevenlabs.io/v1/text-to-speech/AkQxVSf1kENGmX9WjeDE/with-timestamps",params={"output_format":"mp3_44100_128"},
 headers={"xi-api-key":chave(),"Content-Type":"application/json"},
 json={"text":txt,"model_id":"eleven_multilingual_v2","previous_text":"Mais seulement si tu ne la refuses pas une nouvelle fois.","next_text":"Reçois ton miracle avant que la porte ne se ferme pour toujours.",
 "voice_settings":{"stability":0.5,"similarity_boost":0.75,"style":0.0,"use_speaker_boost":True,"speed":0.9}},timeout=300)
assert r.status_code==200, r.text[:300]
d=r.json(); open(D+'cta_fr09.mp3','wb').write(base64.b64decode(d['audio_base64']))
json.dump(d.get('normalized_alignment') or d.get('alignment'),open(D+'cta_fr09.alinhamento.json','w',encoding='utf-8'),ensure_ascii=False)
print(len(txt),'chars')
