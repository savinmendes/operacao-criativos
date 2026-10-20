import json,subprocess
TL=json.load(open('timeline.json')); sc={n:(s,e) for n,s,e in TL['scenes']}
W={'hook':('src_soldados_v2.mp4',0.0,0.0,sc['hook'][1]+0.4),
   'crown1':('src_corpo_cta.mp4',0.0,sc['crown1'][0]-0.3,sc['crown1'][1]+0.3),
   'crown2':('src_corpo_cta.mp4',4.0,sc['crown2'][0]-0.3,sc['crown2'][1]+0.3),
   'crown3':('src_corpo_cta.mp4',19.16,sc['crown3'][0]-0.3,sc['crown3'][1]+0.3)}
org={}
for n,(src,ss,a,b) in W.items():
    d=b-a; org[n]=[a,ss,round(d,3)]
    subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-ss',f'{ss:.3f}','-t',f'{d:.3f}','-c:v','libx264','-crf','12','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',f'ls/in_{n}.mp4'],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i','audio/voz_en_full.wav','-ss',f'{a:.3f}','-t',f'{d:.3f}','-c:a','libmp3lame','-b:a','192k',f'ls/au_{n}.mp3'],check=True)
    print(n,src,ss,'-> T',round(a,3),'dur',round(d,3))
json.dump(org,open('ls/org.json','w'),indent=1)
