# Gera cada segmento PL com a voz Jesus The Chosen (mesma do EN); contexto anterior/seguinte p/ prosodia continua
# uso: python tts_segs_it.py [modelo] [idx...]   velocidades em velocidades_pl.json
import sys, json, base64, requests
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
VOZ = "AkQxVSf1kENGmX9WjeDE"
S = json.load(open("segmentos_pl.json", encoding="utf-8"))
MOD = sys.argv[1] if len(sys.argv) > 1 else "eleven_multilingual_v2"
so = [int(a) for a in sys.argv[2:]] or range(len(S))
try: vel = json.load(open("velocidades_pl.json"))
except Exception: vel = {}
tot = 0
for i in so:
    a, b, t = S[i]
    body = {"text": t, "model_id": MOD,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.0, "use_speaker_boost": True,
                               "speed": vel.get(str(i), 1.0)}}
    if MOD != "eleven_multilingual_v2": body["language_code"] = "pl"
    if i > 0: body["previous_text"] = S[i-1][2]
    if i + 1 < len(S): body["next_text"] = S[i+1][2]
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps", params={"output_format": "mp3_44100_128"},
                      headers={"xi-api-key": chave()}, json=body, timeout=300)
    if not r.ok: print(i, r.status_code, r.text[:300]); continue
    d = r.json()
    open(f"audio/s{i:02d}.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(f"audio/s{i:02d}.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
    tot += len(t)
    e = d["alignment"]["character_end_times_seconds"][-1]
    print(i, f"slot {b-a:.2f}s  it {e:.2f}s  {'ESTOURA' if e > b-a else 'ok'}", flush=True)
print("chars", tot)
