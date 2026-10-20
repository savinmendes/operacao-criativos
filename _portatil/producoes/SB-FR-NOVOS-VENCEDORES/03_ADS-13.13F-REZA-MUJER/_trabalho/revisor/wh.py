from faster_whisper import WhisperModel
import json,sys
m=WhisperModel('medium',device='cpu',compute_type='int8')
out={}
for lang in ['fr','es']:
    seg,info=m.transcribe('audio16.wav',language=lang,word_timestamps=True,beam_size=5,vad_filter=False)
    ws=[];txt=[]
    for s in seg:
        txt.append(s.text)
        for w in s.words: ws.append((round(w.start,2),round(w.end,2),w.word,round(w.probability,2)))
    out[lang]={'text':''.join(txt),'words':ws}
    print(lang,info.language_probability if lang=='fr' else '', ''.join(txt))
seg,info=m.transcribe('audio16.wav')
print('auto',info.language,round(info.language_probability,3))
json.dump(out,open('whisper.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
for w in out['fr']['words']: print(*w)
