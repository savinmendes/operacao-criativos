import os, sys
os.add_dll_directory(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Lib\site-packages\torch\lib")
os.environ["PATH"] = r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Lib\site-packages\torch\lib;" + os.environ["PATH"]
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
segs,_ = m.transcribe(sys.argv[1], language="es", word_timestamps=True)
for s in segs:
    for w in s.words: print(round(w.start,2), round(w.end,2), w.word)
