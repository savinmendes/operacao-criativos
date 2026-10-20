import os, sys
os.add_dll_directory(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Lib\site-packages\torch\lib")
os.environ["PATH"] = r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Lib\site-packages\torch\lib;" + os.environ["PATH"]
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
f, lang = sys.argv[1], sys.argv[2]
segs,_ = m.transcribe(f, language=lang, vad_filter=True)
for s in segs: print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}")
