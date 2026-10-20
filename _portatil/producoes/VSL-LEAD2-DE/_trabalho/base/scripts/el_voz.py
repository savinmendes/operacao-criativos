import sys, json, requests
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
H = {"xi-api-key": chave()}
cmd = sys.argv[1]
if cmd == "contar":
    r = requests.get("https://api.elevenlabs.io/v2/voices", headers=H, params={"page_size": 100, "voice_type": "personal"}, timeout=60).json()
    nomes = [v["name"] for v in r.get("voices", [])]
    print("total_count", r.get("total_count"), "tem PADRE?", [n for n in nomes if "PADRE" in n.upper()])
    s = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers=H, timeout=60).json()
    print("voice_limit", s.get("voice_limit"), "voice_slots_used", s.get("voice_slots_used"), "chars", s.get("character_count"), "/", s.get("character_limit"))
elif cmd == "criar":
    r = requests.post("https://api.elevenlabs.io/v1/voices/add", headers=H,
        data={"name": "PADRE VSL LEAD2", "remove_background_noise": "false", "description": "Clone do padre (avatar da pessoa) da VSL Lead 2 San Benito; amostra demucs vocals 153 s"},
        files={"files": ("amostra_padre.mp3", open(sys.argv[2], "rb"), "audio/mpeg")}, timeout=300)
    print(r.status_code, r.text[:300])
elif cmd == "tts":
    vid, txt, out = sys.argv[2], sys.argv[3], sys.argv[4]
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}", headers=H, params={"output_format": "mp3_44100_128"},
        json={"text": txt, "model_id": "eleven_multilingual_v2", "language_code": "de",
              "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.0, "use_speaker_boost": True}}, timeout=120)
    if r.status_code != 200:
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}", headers=H, params={"output_format": "mp3_44100_128"},
            json={"text": txt, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.0, "use_speaker_boost": True}}, timeout=120)
    print(r.status_code, len(r.content)); open(out, "wb").write(r.content) if r.status_code == 200 else print(r.text[:300])
