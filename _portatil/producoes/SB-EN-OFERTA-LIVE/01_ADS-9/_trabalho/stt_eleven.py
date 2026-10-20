import sys, json, requests
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
src, lang, out = sys.argv[1], sys.argv[2], sys.argv[3]
r = requests.post("https://api.elevenlabs.io/v1/speech-to-text", headers={"xi-api-key": chave()},
    data={"model_id": "scribe_v1", "language_code": lang, "timestamps_granularity": "word"},
    files={"file": open(src, "rb")}, timeout=600)
r.raise_for_status(); d = r.json()
ws = [{"w": w["text"], "s": w["start"], "e": w["end"]} for w in d["words"] if w.get("type") == "word"]
json.dump(ws, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(d["text"])
