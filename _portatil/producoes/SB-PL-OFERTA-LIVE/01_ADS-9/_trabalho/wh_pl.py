import sys
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, info = m.transcribe(sys.argv[1], language=None, beam_size=5)
print("idioma", info.language, round(info.language_probability, 3))
for s in segs: print(f"{s.start:6.2f} {s.text}")
