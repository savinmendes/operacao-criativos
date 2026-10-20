import sys,json,base64,requests
sys.path.insert(0,r'C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas')
from tts_elevenlabs import chave
VID='AkQxVSf1kENGmX9WjeDE'
H={"xi-api-key":chave()}
if sys.argv[1]=='vozes':
    v=requests.get('https://api.elevenlabs.io/v1/voices',headers=H,timeout=60).json()['voices']
    print('total vozes',len(v))
    for x in v:
        if x['voice_id']==VID: print('escolhida:',x['name'],x.get('category'),x.get('labels'))
    s=requests.get('https://api.elevenlabs.io/v1/user/subscription',headers=H,timeout=30).json()
    print('chars usados',s.get('character_count'),'/',s.get('character_limit')); sys.exit()
nome,txt=sys.argv[1],sys.argv[2]; spd=float(sys.argv[3]) if len(sys.argv)>3 else 0.95
prev=sys.argv[4] if len(sys.argv)>4 else None; nxt=sys.argv[5] if len(sys.argv)>5 else None
MODEL=sys.argv[6] if len(sys.argv)>6 else 'eleven_multilingual_v2'
body={"text":txt,"model_id":MODEL,"voice_settings":{"stability":0.5,"similarity_boost":0.75,"style":0.0,"use_speaker_boost":True,"speed":spd}}
if MODEL!='eleven_multilingual_v2' and MODEL!='eleven_v3': body['language_code']='it'
if prev and prev!='-': body['previous_text']=prev
if nxt and nxt!='-': body['next_text']=nxt
r=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VID}/with-timestamps",params={"output_format":"mp3_44100_128"},headers={**H,"Content-Type":"application/json"},json=body,timeout=300)
assert r.status_code==200, r.text[:300]
d=r.json(); open(f'audio/{nome}.mp3','wb').write(base64.b64decode(d['audio_base64']))
json.dump(d.get('normalized_alignment') or d.get('alignment'),open(f'audio/{nome}.alinhamento.json','w',encoding='utf-8'),ensure_ascii=False)
open(f'audio/{nome}.txt','w',encoding='utf-8').write(txt)
print(nome,len(txt),'chars')
