from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4)
seg,info=m.transcribe(r'..\..\SB-PL-JESU-V07.mp4',language='pl',word_timestamps=True)
for s in seg:
    print(f'{s.start:.2f}-{s.end:.2f} {s.text}')
    print('   ',' '.join(f'{w.word.strip()}@{w.start:.2f}({w.probability:.2f})' for w in s.words))
