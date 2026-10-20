import json, sys
sys.path.insert(0, "..")
import alinhar_roteiro as ar
from pathlib import Path
T = json.load(open("../textos_legenda.json", encoding="utf-8"))
import torch
torch_, proc, mod = ar._modelo()
for f in ["T1_gancho_v2_vz","T3_yara_vz","T4_yara_close_vz","T5_moi_vz","T7_elixir_vz","T10_cta_vz"]:
    p = Path("../../takes")/(f+".wav")
    x = ar._pcm16(p)
    with torch.no_grad():
        lg = mod(proc(x, sampling_rate=16000, return_tensors="pt").input_values).logits[0]
    print(f, "| greedy:", proc.batch_decode(lg.argmax(-1)[None])[0])
    r = ar.palavras_fonte(p, T[f], "ctc")
    print("   ", " ".join(f"{w}@{a:.2f}" for w,a,b in r))
for f in ["N_yara","N_moi_v2","N_elixir"]:
    p = Path("../../voz")/(f+".mp3"); t = ar.texto_de(p, T)
    e = ar.palavras_fonte(p, t, "auto"); c = ar.palavras_fonte(p, t, "ctc")
    print(f, " ".join(f"{w}:{a:.2f}/{c2[1]:.2f}" for (w,a,b),c2 in zip(e,c)))
