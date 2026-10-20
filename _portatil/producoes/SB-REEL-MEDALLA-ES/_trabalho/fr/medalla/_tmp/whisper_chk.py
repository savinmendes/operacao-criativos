import sys, json
from faster_whisper import WhisperModel
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\voz"); import montar_vozes as mv
m = WhisperModel("medium", device="cpu", compute_type="int8")
for f in sys.argv[1:]:
    segs, _ = m.transcribe(f, language="fr", beam_size=5)
    print("==", f.split("_trabalho")[-1], "|", " ".join(s.text.strip() for s in segs))
    ws = mv.palavras(f[:-4] + ".alinhamento.json")
    gaps = [(round(a["fim"],2), round(b["ini"],2), round(b["ini"]-a["fim"],2), a["w"]) for a,b in zip(ws,ws[1:]) if b["ini"]-a["fim"]>0.15]
    print("   dur_fala", round(ws[-1]["fim"],2), "gaps", gaps)
