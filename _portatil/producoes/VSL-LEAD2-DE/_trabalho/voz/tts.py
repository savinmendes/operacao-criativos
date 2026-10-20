import requests, json, base64, sys, el
URL = "https://api.elevenlabs.io/v1/text-to-speech/{}/with-timestamps?output_format=mp3_44100_192"
def tts(voice_id, text, out_mp3, settings=None, prev=None, nxt=None, lang="de", model="eleven_multilingual_v2", seed=None):
    body = {"text": text, "model_id": model,
            "voice_settings": settings or {"stability": 0.5, "similarity_boost": 0.8, "style": 0.0, "use_speaker_boost": True}}
    if lang: body["language_code"] = lang
    if prev: body["previous_text"] = prev
    if nxt: body["next_text"] = nxt
    if seed is not None: body["seed"] = seed
    r = requests.post(URL.format(voice_id), headers={**el.H(), "Content-Type": "application/json"}, json=body, timeout=300)
    if r.status_code != 200 and lang and "language" in r.text.lower():
        body.pop("language_code"); r = requests.post(URL.format(voice_id), headers={**el.H(), "Content-Type": "application/json"}, json=body, timeout=300)
        print("language_code recusado; sem ele", file=sys.stderr)
    if r.status_code != 200: raise RuntimeError(f"{r.status_code} {r.text[:300]}")
    j = r.json()
    open(out_mp3, "wb").write(base64.b64decode(j["audio_base64"]))
    al = j.get("alignment")
    json.dump(al, open(out_mp3[:-4] + ".alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
    return al, r.headers.get("character-cost") or r.headers.get("x-character-count")
