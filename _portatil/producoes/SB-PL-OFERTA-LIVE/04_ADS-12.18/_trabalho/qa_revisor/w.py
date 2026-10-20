from faster_whisper import WhisperModel
import sys
m=WhisperModel("medium",device="cuda",compute_type="float16") if len(sys.argv)<2 else WhisperModel("medium",device="cpu",compute_type="int8")
segs,_=m.transcribe("a.wav",language="pl",word_timestamps=True,beam_size=5,vad_filter=False)
for s in segs:
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}")
    for w in s.words: print(f"   {w.start:.2f}-{w.end:.2f} {w.word} p={w.probability:.2f}")
