import sys
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=8)
for spec in sys.argv[2:]:
    a, b = map(float, spec.split("-"))
    import subprocess, numpy as np
    r = subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-t",str(b-a),"-i",sys.argv[1],"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True)
    x = np.frombuffer(r.stdout, np.float32)
    segs, _ = m.transcribe(x, language="en", word_timestamps=True)
    print(spec, " ".join(f"{w.word.strip()}[{a+w.start:.2f}]" for s in segs for w in s.words))
