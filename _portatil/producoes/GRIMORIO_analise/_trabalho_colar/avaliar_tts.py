import os, sys, json
os.add_dll_directory(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Lib\site-packages\torch\lib")
os.environ["PATH"] = r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Lib\site-packages\torch\lib;" + os.environ["PATH"]
from faster_whisper import WhisperModel
from resemblyzer import VoiceEncoder, preprocess_wav
import librosa, numpy as np
enc = VoiceEncoder(verbose=False)
y, sr = librosa.load('demucs/htdemucs/audio_orig/vocals.wav', sr=16000, offset=100, duration=25)
ref = enc.embed_utterance(preprocess_wav(y, source_sr=16000))
f0r, _, _ = librosa.pyin(y, fmin=60, fmax=300, sr=16000); print('ref f0 med', np.nanmedian(f0r))
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
for f in sys.argv[1:]:
    y, _ = librosa.load(f, sr=16000)
    e = enc.embed_utterance(preprocess_wav(y, source_sr=16000))
    f0, _, _ = librosa.pyin(y, fmin=60, fmax=300, sr=16000)
    segs, _ = m.transcribe(f, language="pt", word_timestamps=True)
    ws = [w for s in segs for w in s.words]
    print(f, 'sim', round(float(e @ ref), 3), 'f0', round(float(np.nanmedian(f0)), 1), 'fala', round(ws[0].start, 2), '-', round(ws[-1].end, 2), '|', ''.join(w.word for w in ws))
