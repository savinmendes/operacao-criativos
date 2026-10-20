import json,sys
from faster_whisper import WhisperModel
v=r"C:\Users\PICHAU\Downloads\SB-EN-NOVOS-VENCEDORES\01_AVATAR-REST\_trabalho\SB-EN-AVATAR-REST_v2.mp4"
m=WhisperModel("medium",device="cpu",compute_type="int8")
segs,info=m.transcribe(v,language="en",word_timestamps=True,beam_size=5,condition_on_previous_text=False)
out=[]
for s in segs:
    ws=[[w.word,round(w.start,2),round(w.end,2),round(w.probability,2)] for w in s.words]
    out.append({"ini":round(s.start,2),"fim":round(s.end,2),"txt":s.text,"words":ws})
    print(f"{s.start:6.2f}-{s.end:6.2f} {s.text}",flush=True)
json.dump(out,open("whisper_medium_en.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
# deteccao de idioma em janelas (residuo de espanhol)
segs2,info2=m.transcribe(v,word_timestamps=False,beam_size=5)
print("IDIOMA auto:",info2.language,info2.language_probability)
for s in segs2: print(f"AUTO {s.start:6.2f}-{s.end:6.2f} {s.text}")
