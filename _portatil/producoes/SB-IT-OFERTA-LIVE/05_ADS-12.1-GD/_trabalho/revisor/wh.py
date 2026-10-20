from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
s,_=m.transcribe(r"C:\Users\PICHAU\Downloads\SB-IT-OFERTA-LIVE\05_ADS-12.1-GD\SB-IT-ADS-12.1-GD.mp4",language="it",word_timestamps=True)
for seg in s:
  print("%.2f-%.2f %s"%(seg.start,seg.end,seg.text))
  print("   "+" ".join("%s@%.2f-%.2f"%(w.word.strip(),w.start,w.end) for w in seg.words))
