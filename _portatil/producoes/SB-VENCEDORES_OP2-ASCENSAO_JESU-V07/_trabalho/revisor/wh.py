import sys, json
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8')
for v, lang, out in [(a.split('|')[0], a.split('|')[1], a.split('|')[2]) for a in sys.argv[1:]]:
    segs, info = m.transcribe(v, language=lang, word_timestamps=True, beam_size=5, vad_filter=False)
    W=[]
    for s in segs:
        for w in s.words: W.append({'w':w.word.strip(),'s':round(w.start,2),'e':round(w.end,2),'p':round(w.probability,2)})
    json.dump(W, open(out,'w',encoding='utf-8'), ensure_ascii=False, indent=0)
    print('==', out); print(' '.join(f"{x['w']}[{x['s']}-{x['e']}|{x['p']}]" for x in W))
