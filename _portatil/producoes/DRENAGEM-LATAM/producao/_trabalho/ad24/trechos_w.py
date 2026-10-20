import json,subprocess,sys
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8",cpu_threads=4)
out={}
for de,ate in [(60,170),(425,450),(575,610),(615,700)]:
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(de),"-to",str(ate),"-i","aud/voc16.wav","x.wav"],check=True)
    segs,_=m.transcribe("x.wav",language="es",word_timestamps=True,condition_on_previous_text=False,vad_filter=False)
    for s in segs:
        print(" ".join(f"{w.word.strip()}[{w.start+de:.2f}-{w.end+de:.2f}]" for w in s.words),flush=True)
    print("-----")
