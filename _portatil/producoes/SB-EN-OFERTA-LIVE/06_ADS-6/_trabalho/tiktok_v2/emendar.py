# Emenda a frase nova na narração original (corte nas pausas), gera voz_emendada.wav + alinhamento combinado
import sys, json, numpy as np, soundfile as sf
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import load, SR
o=load("audio/narracao_en.mp3"); n=load("audio/frase01_nova.mp3")
def env(x):
    m=np.abs(x.mean(1)); h=int(0.005*SR); k=len(m)//h
    return 20*np.log10(np.sqrt((m[:k*h].reshape(k,h)**2).mean(1))+1e-12), h
def on_off(x, a, b, thr=-50):
    e,h=env(x); i0,i1=int(a*SR/h),int(b*SR/h); idx=np.where(e[i0:i1]>thr)[0]+i0
    return idx[0]*h/SR, (idx[-1]+1)*h/SR
o_on,_=on_off(o,2.10,2.60)          # início de "Not" original
_,o_off=on_off(o,4.50,5.40)         # fim de "warning."
o_no,_=on_off(o,5.30,5.80)          # início de "No"
n_on,n_off=on_off(n,0,len(n)/SR)
print("orig Not",o_on,"warning fim",o_off,"No",o_no,"| nova",n_on,n_off)
M=0.03
A=o[:int((o_on-M)*SR)]
B=n[int(max(0,n_on-M)*SR):int(min(len(n)/SR,n_off+M)*SR)]
gap=(o_no-M)-(o_off+M)               # mesma pausa original entre a frase e "No"
G=np.zeros((int(gap*SR),2),np.float32)
C=o[int((o_off+M)*SR)+len(G)*0:][:0]  # placeholder
C=o[int((o_no-M)*SR):]
# o trecho A termina em silencio e C começa em silencio (pausas TTS ~ -95 dB): emenda direta, fades de 5 ms por segurança
f=int(0.005*SR); r=np.linspace(0,1,f)[:,None]
B=B.copy(); B[:f]*=r; B[-f:]*=r[::-1]
v=np.concatenate([A,B,G,C]).astype(np.float32)
sf.write("audio/voz_emendada.wav",v,SR,subtype="FLOAT")
off_new=(o_on-M)-max(0,n_on-M)                     # deslocamento da frase nova
D=(len(A)+len(B)+len(G))/SR-(o_no-M)               # deslocamento do resto
print("frase nova em",round(off_new,3),"; resto deslocado",round(D,3),"s; dur",len(v)/SR)
# alinhamento combinado
ao=json.load(open("audio/narracao_en_ORIGINAL.alinhamento.json",encoding="utf-8")); an=json.load(open("audio/frase01_nova.alinhamento.json",encoding="utf-8"))
ch,s,e=[],[],[]
txt="".join(ao["characters"]); i_not=txt.index("Not by chance"); i_no=txt.index("No other message")
for i in range(i_not): ch.append(ao["characters"][i]); s.append(ao["character_start_times_seconds"][i]); e.append(ao["character_end_times_seconds"][i])
for c,a,b in zip(an["characters"],an["character_start_times_seconds"],an["character_end_times_seconds"]):
    ch.append(c); s.append(a+off_new); e.append(min(b+off_new,(len(A)+len(B))/SR))
ch.append(" "); s.append(e[-1]); e.append(e[-1])
for i in range(i_no,len(ao["characters"])): ch.append(ao["characters"][i]); s.append(ao["character_start_times_seconds"][i]+D); e.append(ao["character_end_times_seconds"][i]+D)
json.dump({"characters":ch,"character_start_times_seconds":s,"character_end_times_seconds":e},open("audio/narracao_en.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
json.dump({"off_new":off_new,"D":D,"o_on":o_on,"o_off":o_off,"o_no":o_no,"n_on":n_on,"n_off":n_off,"dur":len(v)/SR},open("emenda.json","w"),indent=1)
open("audio/narracao_en.txt","w",encoding="utf-8").write("".join(ch))
