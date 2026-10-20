import os, sys, json
os.add_dll_directory(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Lib\site-packages\torch\lib")
os.environ["PATH"] = r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Lib\site-packages\torch\lib;" + os.environ["PATH"]
from faster_whisper import WhisperModel
arq, off, saida = sys.argv[1], float(sys.argv[2]), sys.argv[3]
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
segs, _ = m.transcribe(arq, language="pt", word_timestamps=True)
out = []
for s in segs:
    for w in s.words:
        out.append((round(w.start + off, 2), round(w.end + off, 2), w.word)); print(out[-1])
json.dump(out, open(saida, "w", encoding="utf-8"), ensure_ascii=False)
