import json
from faster_whisper import WhisperModel
m=WhisperModel('medium',device='cpu',compute_type='int8',cpu_threads=8)
seg,info=m.transcribe('a16.wav',language='es',word_timestamps=True,beam_size=5,vad_filter=False,condition_on_previous_text=False)
out=[]
for s in seg:
    out.append({'s':s.start,'e':s.end,'t':s.text,'w':[(w.start,w.end,w.word,w.probability) for w in s.words]})
json.dump(out,open('whisper.json','w',encoding='utf8'),ensure_ascii=False,indent=0)
print('done')
