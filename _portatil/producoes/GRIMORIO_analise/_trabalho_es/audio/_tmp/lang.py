import os, sys
os.add_dll_directory(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Lib\site-packages\torch\lib")
os.environ["PATH"] = r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Lib\site-packages\torch\lib;" + os.environ["PATH"]
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
for f in sys.argv[1:]:
    a = decode_audio(f)
    lang, p, allp = m.detect_language(a)
    d = dict(allp)
    segs,_ = m.transcribe(f, language="es")
    print(f, "lang", lang, round(p,3), "es", round(d.get("es",0),3), "pt", round(d.get("pt",0),3), "dur", round(len(a)/16000,2), "|", "".join(s.text for s in segs))
