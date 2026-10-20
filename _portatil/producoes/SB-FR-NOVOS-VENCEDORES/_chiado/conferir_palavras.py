# whisper fr no audio antigo x novo, comparado com o texto do roteiro (alinhamento): % de palavras reconhecidas
# uso: python conferir_palavras.py ref1.alinhamento.json[,ref2...] antigo.(wav|mp4) novo.(wav|mp4)
import sys, json, re, unicodedata, difflib
from faster_whisper import WhisperModel
def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z0-9]+", s.replace("'", " ").replace("’", " "))
ref = []
for p in sys.argv[1].split(","): ref += norm("".join(json.load(open(p, encoding="utf-8"))["characters"]))
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=8)
res = {}
for f in sys.argv[2:]:
    segs, _ = m.transcribe(f, language="fr", beam_size=5, vad_filter=False, condition_on_previous_text=False)
    hyp = norm(" ".join(s.text for s in segs))
    sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
    ok = sum(b.size for b in sm.get_matching_blocks()); miss = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("delete", "replace"): miss.append(" ".join(ref[i1:i2]) + (" -> " + " ".join(hyp[j1:j2]) if tag == "replace" else " -> (nada)"))
    res[f] = (ok, len(ref), miss)
    print(f"{f.split(chr(92))[-1].split('/')[-1]}: {ok}/{len(ref)} palavras do roteiro = {100*ok/len(ref):.1f}%")
    for x in miss: print("   dif:", x)
