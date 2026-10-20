import gpu, json, subprocess, sys
from faster_whisper import WhisperModel
A = json.load(open("alinhamento_de.json", encoding="utf-8"))["palavras"]
m = WhisperModel("medium", device="cuda", compute_type="float16")
for t in [165.3, 316.3, 435.8, 485.4, 617.5, 642.6, 672.2, 1362.6, 2027.3, 2171.3, 2194.4, 2382.3, 2435.9, 2462.0]:
    ws = [a for a in A if abs(a["ini"] - t) < 0.6]
    w0 = ws[0] if ws else None
    blk = [a for a in A if a["bloco"] == w0["bloco"]] if w0 else []
    a, b = t - 4, t + 4
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b - a), "-i", "narracao_de_completa.wav", "-ar", "16000", "-ac", "1", "_j.wav"])
    s, _ = m.transcribe("_j.wav", language="de", beam_size=5, condition_on_previous_text=False)
    ref = " ".join(x["palavra"] for x in A if a + 0.3 < x["ini"] < b - 0.3)
    fim_bloco = blk and abs(blk[-1]["ini"] - t) < 0.6
    print(t, w0["bloco"] if w0 else "", "FIM_BLOCO" if fim_bloco else "", "\n  REF:", ref, "\n  WH :", " ".join(x.text for x in s))
