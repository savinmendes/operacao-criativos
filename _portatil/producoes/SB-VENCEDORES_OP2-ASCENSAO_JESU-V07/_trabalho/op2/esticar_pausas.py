import soundfile as sf, numpy as np, json
a,sr=sf.read("audio/corpo_fr_v2.wav")
ins=[(2.655,0.65),(3.73,0.60),(6.73,0.15),(15.85,0.50)]
tail=0.40
al=json.load(open("audio/corpo_fr_v2.alinhamento.json",encoding="utf-8"))
out=[]; prev=0
for t,d in ins:
    i=int(t*sr); out+= [a[prev:i], np.zeros(int(d*sr))]; prev=i
out+=[a[prev:], np.zeros(int(tail*sr))]
y=np.concatenate(out); sf.write("audio/corpo_fr.wav",y,sr)
def sh(x):
    return round(x+sum(d for t,d in ins if x>=t),3)
al2={"characters":al["characters"],
     "character_start_times_seconds":[sh(x) for x in al["character_start_times_seconds"]],
     "character_end_times_seconds":[sh(x) for x in al["character_end_times_seconds"]]}
json.dump(al2,open("audio/corpo_fr.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
print("dur",len(y)/sr)
