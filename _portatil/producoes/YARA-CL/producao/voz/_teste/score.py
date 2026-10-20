import numpy as np, ctranslate2
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
m = WhisperModel("medium", device="cpu", compute_type="int8")
tok = m.hf_tokenizer
audio = decode_audio("gancho.wav", 16000)[:int(16000*3.0)]
feat = m.feature_extractor(audio)
feat = np.pad(feat, ((0,0),(0,3000-feat.shape[1])))[None].astype(np.float32)
enc = m.model.encode(ctranslate2.StorageView.from_array(feat))
def logp_seq(ids, cont):
    # sum log-probs of forcing cont tokens one by one
    g = m.model.generate(enc, [ids + cont], max_length=len(ids)+len(cont)+8, beam_size=1, return_logits_vocab=True)
    L = g[0].logits[0]; tot = 0.0
    for i, c in enumerate(cont):
        lg = np.asarray(L[i], dtype=np.float64); lp = lg - lg.max() - np.log(np.exp(lg-lg.max()).sum())
        tot += lp[c]
    return tot
for lang in ["es","pt"]:
    ids = [tok.token_to_id(t) for t in ["<|startoftranscript|>", f"<|{lang}|>", "<|transcribe|>", "<|notimestamps|>"]]
    pref = tok.encode(" Liquidación de", add_special_tokens=False).ids
    for w in [" stock", " estoque", " estok", " stok"]:
        cont = tok.encode(w + " por Black Friday", add_special_tokens=False).ids
        print(lang, repr(w), round(logp_seq(ids, pref+cont), 2))
