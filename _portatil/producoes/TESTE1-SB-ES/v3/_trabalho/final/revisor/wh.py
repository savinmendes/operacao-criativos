from faster_whisper import WhisperModel
import json
m=WhisperModel('medium',device='cpu',compute_type='int8')
segs,_=m.transcribe('a16.wav',language='es',word_timestamps=True,vad_filter=False,beam_size=5)
out=[]
for s in segs:
    out.append({'t0':s.start,'t1':s.end,'txt':s.text,'w':[(w.start,w.end,w.word) for w in s.words]})
    print(f'{s.start:7.2f}-{s.end:7.2f} {s.text}',flush=True)
json.dump(out,open('whisper.json','w',encoding='utf-8'),ensure_ascii=False)
