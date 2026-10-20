import sys
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
for lang in ("es", "en"):
    segs, info = m.transcribe(sys.argv[1], language=lang, vad_filter=False)
    print(f"--- {lang}")
    for s in segs:
        print(f"{s.start:6.2f}-{s.end:6.2f} {s.text}")
