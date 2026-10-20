import sys,requests
sys.path.insert(0,'ferramentas')
from tts_elevenlabs import chave
r=requests.get('https://api.elevenlabs.io/v1/user/subscription',headers={'xi-api-key':chave()},timeout=30).json()
print('usado',r.get('character_count'),'limite',r.get('character_limit'),'tier',r.get('tier'))
v=requests.get('https://api.elevenlabs.io/v1/voices/AkQxVSf1kENGmX9WjeDE',headers={'xi-api-key':chave()},timeout=30).json()
print(v.get('name'),v.get('category'),v.get('fine_tuning',{}).get('language'), v.get('labels'))
