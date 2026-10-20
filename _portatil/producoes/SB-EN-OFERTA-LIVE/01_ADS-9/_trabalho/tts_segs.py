# Gera cada segmento EN com a voz Jesus The Chosen (contexto de texto anterior/seguinte p/ prosodia continua)
import sys, json, base64, requests
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
VOZ = "AkQxVSf1kENGmX9WjeDE"
S = json.load(open("segmentos_en.json", encoding="utf-8"))
so = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else range(len(S))
vel = json.load(open("velocidades.json")) if len(sys.argv) > 1 else {}
tot = 0
for i in so:
    a, b, t = S[i]
    body = {"text": t, "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.0, "use_speaker_boost": True,
                               "speed": vel.get(str(i), 1.0)}}
    if i > 0: body["previous_text"] = S[i-1][2]
    if i + 1 < len(S): body["next_text"] = S[i+1][2]
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps", params={"output_format": "mp3_44100_128"},
                      headers={"xi-api-key": chave()}, json=body, timeout=300)
    r.raise_for_status(); d = r.json()
    open(f"audio/s{i:02d}.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(f"audio/s{i:02d}.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
    tot += len(t)
    e = d["alignment"]["character_end_times_seconds"][-1]
    print(i, f"slot {b-a:.2f}s  en {e:.2f}s", flush=True)
print("chars", tot, "US$~", round(tot / 1000 * 0.165, 3))
