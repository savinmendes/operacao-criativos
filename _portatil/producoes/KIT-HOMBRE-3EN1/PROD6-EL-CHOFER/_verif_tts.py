import sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\ferramentas\transcritor-youtube")
from lib.whisper_local import _registrar_dlls_cuda
_registrar_dlls_cuda()
from faster_whisper import WhisperModel
import json, glob, os
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
out = {}
for f in sys.argv[1:]:
    segs, _ = m.transcribe(f, language="es", word_timestamps=True)
    ws = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]
    out[os.path.basename(f)] = ws
    print(os.path.basename(f), " ".join(w for w, _, _ in ws))
json.dump(out, open("_transcricao_" + os.path.basename(sys.argv[1]).split('.')[0] + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
