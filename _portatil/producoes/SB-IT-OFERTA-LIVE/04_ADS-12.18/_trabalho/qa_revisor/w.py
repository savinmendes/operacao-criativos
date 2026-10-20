from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8",cpu_threads=4)
segs,info=m.transcribe("a16.wav",language=None,word_timestamps=True,vad_filter=False)
print(info.language,info.language_probability)
with open("whisper.txt","w",encoding="utf-8") as f:
  for s in segs:
    f.write(f"[{s.start:.2f}-{s.end:.2f}] {s.text}\n")
    for w in s.words: f.write(f"   {w.start:.2f}-{w.end:.2f} {w.word} {w.probability:.2f}\n")
