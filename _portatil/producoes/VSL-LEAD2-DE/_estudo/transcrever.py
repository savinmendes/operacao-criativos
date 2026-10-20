import json, sys
from faster_whisper import WhisperModel
m = WhisperModel('small', device='cpu', compute_type='int8')
segs, info = m.transcribe(sys.argv[1], language='es', word_timestamps=True, vad_filter=True)
out = []
with open('transcricao_es.txt', 'w', encoding='utf-8') as f:
    for s in segs:
        out.append({'ini': s.start, 'fim': s.end, 'texto': s.text.strip(), 'palavras': [[w.start, w.end, w.word] for w in s.words]})
        f.write(f"[{int(s.start//60):02d}:{s.start%60:05.2f}] {s.text.strip()}\n"); f.flush()
json.dump(out, open('transcricao_es.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('ok', len(out))
