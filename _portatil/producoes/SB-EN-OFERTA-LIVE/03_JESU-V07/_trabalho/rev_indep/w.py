from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
s,_=m.transcribe(r"C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\03_JESU-V07\SB-EN-JESU-V07.mp4",language="en",word_timestamps=True)
for x in s:
  print(f"{x.start:.2f}-{x.end:.2f} {x.text}")
  print("   "," ".join(f"{w.word.strip()}@{w.start:.2f}-{w.end:.2f}" for w in x.words))
