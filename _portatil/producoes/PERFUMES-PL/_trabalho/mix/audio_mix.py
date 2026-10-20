import sys, json, numpy as np, soundfile as sf
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
T = r"C:\Users\PICHAU\Downloads\PERFUMES-PL\_trabalho"
mapa = json.load(open(T + r"\corpo\mapa.json")); D = mapa["D"]; FIM = mapa["fim"]
def sec(x, a, b): return x[int(round(a*SR)):int(round(b*SR))]
def fade(x, fi=0.0, fo=0.0):
    x = x.copy(); n = len(x)
    if fi: k = int(fi*SR); x[:k] *= np.linspace(0, 1, k)[:, None]
    if fo: k = int(fo*SR); x[n-k:] *= np.linspace(1, 0, k)[:, None]
    return x
# voz do corpo
vc = load(T + r"\audio\corpo_vera.mp3"); pwc = palavras(T + r"\audio\corpo_vera.alinhamento.json")
vc, mkc = limpar_voz(vc, pwc); vc = ganho_lufs(vc, -16.5)
# trilha do corpo: no_vocals do 17 a partir do corte + emenda com crossfade p/ cobrir o PL mais longo
nv = load(T + r"\demucs\sep\htdemucs\PFMascLatam17\no_vocals.wav")
a = sec(nv, 8.0667, 57.10); falta = FIM - len(a)/SR
xf = 1.0; b = sec(nv, 20.0, 20.0 + falta + xf + 0.2)
k = int(xf*SR); a2 = a.copy(); a2[-k:] = a[-k:]*np.linspace(1,0,k)[:,None] + b[:k]*np.linspace(0,1,k)[:,None]
bed = np.concatenate([a2, b[k:]])[:int(round(FIM*SR))]
bed = fade(limpar_trilha(bed), 0.02, 0.6)
bed = ganho_lufs(bed, -32)
# mascara da fala do corpo no tempo do corpo
mk_c = np.zeros(len(bed), bool); n0 = int(round(D*SR)); mm = mkc[:len(bed)-n0]; mk_c[n0:n0+len(mm)] = mm
bed = dip_pausas(bed, mk_c, 3)
corpo = bed.copy(); vv = vc[:len(corpo)-n0]; corpo[n0:n0+len(vv)] += vv
def montar(nome, hook_len, hook_voz=None, hook_alin=None, hook_bed=None, hook_orig=None, voz_ini=0.0):
    H = int(round(hook_len*SR)); h = np.zeros((H, 2), np.float32)
    if hook_orig is not None: h += sec(load(hook_orig), 0, hook_len)[:H]
    if hook_bed is not None:
        hb = fade(limpar_trilha(sec(load(hook_bed), 0, hook_len)), 0.0, 0.05); hb = ganho_lufs(hb, -32); h[:len(hb)] += hb
    if hook_voz:
        v = load(hook_voz); v, _ = limpar_voz(v, palavras(hook_alin)); v = ganho_lufs(v, -16.5)
        i0 = int(voz_ini*SR); v = v[:H-i0]; h[i0:i0+len(v)] += v
    mix = finalizar_mix(np.concatenate([h, corpo]))
    sf.write(f"mix_{nome}.wav", mix, SR, subtype="PCM_24"); print(nome, round(len(mix)/SR, 3), round(lufs(mix), 1))
A = T + r"\audio"; S = T + r"\demucs\sep\htdemucs"
montar("17", 8.0667, A + r"\hook17_cristina.mp3", A + r"\hook17_cristina.alinhamento.json")
montar("18", 8.0667, A + r"\hook18_jessica.mp3", A + r"\hook18_jessica.alinhamento.json", voz_ini=0.45)
montar("t1", 3.5667, A + r"\hook_danca_vera.mp3", A + r"\hook_danca_vera.alinhamento.json", hook_bed=S + r"\PFMasctesteLatam1\no_vocals.wav")
montar("t3", 3.5667, A + r"\hook_danca_vera.mp3", A + r"\hook_danca_vera.alinhamento.json", hook_bed=S + r"\PFMasctesteLatam3\no_vocals.wav")
montar("pf7", 7.8333)
