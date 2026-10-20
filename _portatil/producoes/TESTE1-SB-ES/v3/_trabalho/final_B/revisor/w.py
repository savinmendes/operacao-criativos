from faster_whisper import WhisperModel
import json
m=WhisperModel('medium',device='cpu',compute_type='int8')
segs,_=m.transcribe(r'C:/Users/PICHAU/Downloads/TESTE1-SB-ES/v4/SB-ES_NOTICIA-AURELIO_B-ORACION-COMPLETA_FICTICIO.mp4',language='es',word_timestamps=True,vad_filter=False)
out=[]
for s in segs:
    out.append({'s':s.start,'e':s.end,'t':s.text,'w':[(w.start,w.end,w.word,w.probability) for w in s.words]})
    print(f"{s.start:7.2f}-{s.end:7.2f} {s.text}",flush=True)
json.dump(out,open('whisper.json','w',encoding='utf-8'),ensure_ascii=False)
