import subprocess, sys, re, json
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
TERMOS = r"maya|verra|mayaverra|sesenta|60 d|cuarenta y cinco|hecho en|estados unidos|ozempic|tiktok|cofepris|c[áa]ncer|precio|\$|link|enlace|pesos|d[óo]lares|sexo|kilo|libra"
for v in sys.argv[1:]:
    subprocess.run(["ffmpeg","-v","error","-y","-i",v,"-vn","-ac","1","-ar","16000","rev.wav"],check=True)
    segs,_ = m.transcribe("rev.wav", language="es")
    txt = [(s.start, s.end, s.text.strip()) for s in segs]
    out = v.rsplit(".",1)[0] + "_transcricao.txt"
    open(out,"w",encoding="utf-8").write("\n".join(f"{a:7.2f}-{b:7.2f} {t}" for a,b,t in txt))
    print("==", v)
    for a,b,t in txt:
        if re.search(TERMOS, t, re.I): print("  ACHADO", f"{a:.1f}", t)
    print("  fim da fala:", f"{txt[-1][1]:.2f}", "| últimas:", txt[-1][2])
