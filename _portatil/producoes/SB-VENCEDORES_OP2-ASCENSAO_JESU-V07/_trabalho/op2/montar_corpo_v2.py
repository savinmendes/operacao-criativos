import soundfile as sf, numpy as np, json
old,sr=sf.read("audio/corpo_fr.wav"); new,sr2=sf.read("audio/s67_fr_v1.wav"); assert sr==sr2
oal=json.load(open("audio/corpo_fr.alinhamento.json",encoding="utf-8")); nal=json.load(open("audio/s67_fr_v1.alinhamento.json",encoding="utf-8"))
C1, NS, GAP67, NE, GAP78, C2 = 14.30, 2.215, 0.70, 4.36, 0.30, 20.30
z=lambda d: np.zeros(int(round(d*sr)))
parts=[old[:int(C1*sr)], new[:int(NS*sr)], z(GAP67), new[int(NS*sr):int(NE*sr)], z(GAP78), old[int(C2*sr):]]
y=np.concatenate(parts); sf.write("audio/corpo_fr_v2.wav",y,sr)
ch=[];st=[];en=[]
def add(al,lo,hi,shift):
    for c,a,b in zip(al["characters"],al["character_start_times_seconds"],al["character_end_times_seconds"]):
        if lo<=a<hi: ch.append(c); st.append(round(a+shift,3)); en.append(round(b+shift,3))
add(oal,0,C1,0)
add(nal,0,NS,C1)
add(nal,NS,99,C1+GAP67)
off2=C1+NE+GAP67+GAP78-C2
add(oal,C2,99,off2)
# separadores de espaço entre trechos
json.dump({"characters":ch,"character_start_times_seconds":st,"character_end_times_seconds":en},open("audio/corpo_fr_v2.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
print("dur",len(y)/sr,"off2",off2)
