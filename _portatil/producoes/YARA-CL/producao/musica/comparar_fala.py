import difflib,re,unicodedata,json
from faster_whisper import WhisperModel
E=r"C:\Users\PICHAU\Downloads\YARA-CL\entregas\AD-C_yara-kit3_bf_es-cl"
m=WhisperModel("small",device="cpu",compute_type="int8")
norm=lambda s:[w for w in re.sub(r"[^a-z0-9 ]"," ",unicodedata.normalize("NFKD",s.lower()).encode("ascii","ignore").decode()).split()]
def tr(f):
    seg,_=m.transcribe(f,language="es",beam_size=5,vad_filter=False,condition_on_previous_text=False)
    return " ".join(s.text.strip() for s in seg)
ref=tr(E+".mp4"); R=norm(ref); out={"original":ref}
for n in "ABC":
    t=tr(E+f"_musica-{n}.mp4"); W=norm(t); out[n]=t
    sm=difflib.SequenceMatcher(None,R,W); diffs=[(" ".join(R[a:b])," ".join(W[c:d])) for op,a,b,c,d in sm.get_opcodes() if op!="equal"]
    print(n,f"similaridade palavras {sm.ratio():.3f}",len(R),len(W),"difs:",diffs)
json.dump(out,open("_revisao/transcricoes_comparadas.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("ORIG:",ref)
