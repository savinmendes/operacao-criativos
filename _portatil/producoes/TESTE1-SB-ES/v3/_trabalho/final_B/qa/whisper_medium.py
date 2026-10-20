import json, sys
from faster_whisper import WhisperModel
m = WhisperModel('medium', device='cpu', compute_type='int8')
s, _ = m.transcribe(sys.argv[1], language='es', word_timestamps=True)
out = []
for x in s:
    for w in x.words: out.append(dict(w=w.word.strip(), ini=round(w.start, 2), fim=round(w.end, 2)))
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False)
print(' '.join(w['w'] for w in out))
