import json, sys
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8")
out = {}
for f in ["takes/T1_gancho_v2_vz.wav","takes/T3_yara_vz.wav","takes/T4_yara_close_vz.wav","takes/T5_moi_vz.wav","takes/T7_elixir_vz.wav","takes/T10_cta_vz.wav","voz/N_yara.mp3","voz/N_moi_v2.mp3","voz/N_elixir.mp3"]:
    segs,_ = m.transcribe(f, language="es", word_timestamps=True, vad_filter=False)
    ws = [(w.word.strip(), round(w.start,3), round(w.end,3)) for s in segs for w in (s.words or [])]
    out[f] = ws
    print(f, " ".join(f"{w}@{a:.2f}" for w,a,b in ws), flush=True)
json.dump(out, open("edicao/_legenda_sinc/wh_medium_fontes.json","w",encoding="utf-8"), ensure_ascii=False, indent=0)
