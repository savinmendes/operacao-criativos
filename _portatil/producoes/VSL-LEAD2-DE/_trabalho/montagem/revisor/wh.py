import sys,json,subprocess,os
from faster_whisper import WhisperModel
V=r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\VSL-LEAD2-DE.mp4"
chunks=[(0,75),(270,350),(600,660),(960,1020),(1200,1260),(1500,1560),(1860,1990),(2100,2160),(2235,2300)]
m=WhisperModel("small",device="cpu",compute_type="int8",cpu_threads=4)
out=[]
for a,b in chunks:
    wav=f"c_{a}.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-t",str(b-a),"-i",V,"-ac","1","-ar","16000",wav],check=True)
    segs,info=m.transcribe(wav,language="de",word_timestamps=True,vad_filter=False)
    segs=list(segs)
    # language detection residual
    from faster_whisper.audio import decode_audio
    au=decode_audio(wav)
    try:
        lang,prob,allp=m.detect_language(au)
    except Exception as e:
        lang,prob=str(e),0
    class I: pass
    info2=I(); info2.language=lang; info2.language_probability=prob
    rec={"a":a,"b":b,"lang_detect":info2.language,"prob":info2.language_probability,"segs":[{"s":round(a+s.start,2),"e":round(a+s.end,2),"t":s.text,"words":[(round(a+w.start,2),w.word,round(w.probability,2)) for w in s.words]} for s in segs]}
    out.append(rec); print(a,info2.language,round(info2.language_probability,2),flush=True)
    for s in rec["segs"]: print(f"  {s['s']:.1f}-{s['e']:.1f} {s['t']}",flush=True)
json.dump(out,open("whisper.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("DONE")
