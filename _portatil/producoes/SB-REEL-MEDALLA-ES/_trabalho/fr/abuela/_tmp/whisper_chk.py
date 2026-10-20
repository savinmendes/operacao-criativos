import sys, json
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8")
for f in sys.argv[1:]:
    segs, info = m.transcribe(f, language="fr", word_timestamps=True)
    print("==", f.split("/fr/")[-1], " ".join(s.text.strip() for s in segs))
