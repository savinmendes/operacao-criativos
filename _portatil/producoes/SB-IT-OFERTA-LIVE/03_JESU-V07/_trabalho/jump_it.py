# Jump cut na pausa "Tocca ... «Scopri di più»" (boca entreaberta no HeyGen): tira C1-C0 s da voz e dos quadros do crown3,
# e corta crown3 -> porta logo depois de "diretta." (a pausa final fica na porta, não no rosto).
# Rode depois de timeline_it.py. Usa a timeline original (timeline_pre.json) para o crown3 já sincronizado (ls/pt_crown3.mp4).
import json,subprocess,shutil,numpy as np,os
SR=48000; C0,C1=23.48,23.74; D=C1-C0
if not os.path.exists('timeline_pre.json'): shutil.copy('timeline.json','timeline_pre.json')
TL=json.load(open('timeline_pre.json'))
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i','audio/voz_it_full.wav','-f','f32le','-'],capture_output=True).stdout,np.float32)
a=np.concatenate([a[:int(C0*SR)],a[int(C1*SR):]])
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar','48000','-ac','1','-i','-','-c:a','pcm_s16le','audio/voz_it_cut.wav'],input=a.tobytes(),check=True)
W=json.load(open('audio/voz_it_words.json',encoding='utf-8'))
for w in W:
    if w[0].startswith('<<Scopri'): w[1]=23.80   # alinhamento punha o '«' no silêncio
    if w[1]>=C1-0.1: w[1]=round(w[1]-D,3); w[2]=round(w[2]-D,3)
json.dump(W,open('audio/voz_it_words_cut.json','w',encoding='utf-8'),ensure_ascii=False)
fim_diretta=[w for w in W if w[0]=='diretta.'][0][2]
sc=[]
for n,s,e in TL['scenes']:
    s2=s-D if s>C0 else s; e2=e-D if e>C0 else e
    sc.append([n,round(s2,3),round(e2,3)])
for i,(n,s,e) in enumerate(sc):
    if n=='crown3': sc[i][2]=round(fim_diretta+0.06,3); sc[i+1][1]=sc[i][2]
total=round(len(a)/SR,4); sc[-1][2]=total
json.dump({'total':total,'scenes':sc,'arrow':TL['arrow'],'jump':[C0,D]},open('timeline.json','w'),indent=1)
for s in sc: print(s,round(s[2]-s[1],2))
print('total',total)
