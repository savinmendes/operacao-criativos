import subprocess,sys
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8",cpu_threads=4)
for arg in sys.argv[1:]:
    a,b=map(float,arg.split(":"))
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-to",str(b),"-i","aud/voc16.wav","-af","apad=pad_dur=0.5","x.wav"],check=True)
    s,_=m.transcribe("x.wav",language="es",condition_on_previous_text=False,vad_filter=False)
    print(arg," | "," ".join(x.text.strip() for x in s),flush=True)
