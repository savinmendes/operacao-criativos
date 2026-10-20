import subprocess, tempfile, numpy as np
from pathlib import Path
from resemblyzer import VoiceEncoder, preprocess_wav
enc = VoiceEncoder(verbose=False); tmp = Path(tempfile.mkdtemp())
def emb(src, de=None, ate=None, n="x"):
    o = tmp / f"{n}.wav"; c = ["-ss", str(de), "-to", str(ate)] if de is not None else []
    subprocess.run(["ffmpeg","-v","error","-y",*c,"-i",str(src),"-ac","1","-ar","16000",str(o)],check=True)
    return enc.embed_utterance(preprocess_wav(o))
A = r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\_trabalho\ad30\curto_p1c.mp4"
B = r"C:\Users\PICHAU\Downloads\APROVADOS E VALIDADOS TIKTOK\AD 23 - LYMPHORIA-SUPERMERCADO-ES-LATAM.mp4"
oa = emb(A, 29, 57.5, "oa"); ob = emb(B, 200, 260, "ob")
for n, o, g in [("A_gancho", oa, "voz/A_gancho.mp3"), ("B_gancho", ob, "voz/B_gancho.mp3"), ("B_fim", ob, "voz/B_fim.mp3")]:
    print(n, round(float(np.dot(o, emb(g, n=n))), 3))
print("ref B×A (vozes diferentes)", round(float(np.dot(oa, ob)), 3))
