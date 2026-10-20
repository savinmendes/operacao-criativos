from faster_whisper import WhisperModel
import json,sys
m=WhisperModel('medium',device='cpu',compute_type='int8')
segs,_=m.transcribe(sys.argv[1],language='fr',word_timestamps=True,beam_size=5)
W=[]
for s in segs:
    print(f'[{s.start:.2f}-{s.end:.2f}] {s.text}')
    for w in s.words: W.append([round(w.start,2),round(w.end,2),w.word])
json.dump(W,open(sys.argv[2],'w',encoding='utf-8'),ensure_ascii=False)
