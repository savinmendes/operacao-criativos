import sys,json,subprocess
from pathlib import Path
sys.path.insert(0,r"C:\Users\PICHAU\Downloads\Produtividade com ia\ferramentas\transcritor-youtube")
from lib.whisper_local import _registrar_dlls_cuda; _registrar_dlls_cuda()
from faster_whisper import WhisperModel
m=WhisperModel('large-v3',device='cuda',compute_type='float16')
src=Path('TODOS'); out=Path('_analise')
for f in sorted(src.glob('*.mp4')):
    j=out/(f.stem+'.json')
    if j.exists(): continue
    segs,info=m.transcribe(str(f),language=None,vad_filter=True)
    txt=' '.join(s.text.strip() for s in segs)
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(f)],capture_output=True,text=True).stdout or 0)
    json.dump({'arquivo':f.name,'idioma':info.language,'duracao':round(dur,1),'texto':txt},open(j,'w',encoding='utf-8'),ensure_ascii=False)
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-vf',f"fps={min(1,12/max(dur,1)):.3f},scale=160:284,tile=6x2",'-frames:v','1',str(out/(f.stem+'_folha.jpg'))])
    print(f.name,round(dur,1),info.language,flush=True)
print('FIM')
