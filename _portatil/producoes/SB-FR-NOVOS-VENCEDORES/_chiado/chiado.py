# Ferramentas para medir e limpar chiado (hiss) de TTS/trilha demucs. Uso como modulo.
import json, subprocess, numpy as np
SR = 48000
def load(p, sr=SR, ch=2, af=None):
    cmd = ["ffmpeg", "-v", "error", "-i", p] + (["-af", af] if af else []) + ["-ac", str(ch), "-ar", str(sr), "-f", "f32le", "-"]
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32)
    return x.reshape(-1, ch).copy() if ch > 1 else x.copy()
def palavras(p, off=0.0):
    a = json.load(open(p, encoding="utf-8")); out = []; cur = ""; cs = ce = None
    for c, a0, a1 in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
        if c.isspace():
            if cur: out.append([cur, cs + off, ce + off]); cur = ""
        else:
            if not cur: cs = a0
            cur += c; ce = a1
    if cur: out.append([cur, cs + off, ce + off])
    return out
def pausas(pw, minimo=0.25, margem=0.08, total=None):
    """intervalos entre palavras com gap >= minimo, encolhidos pela margem (so 'silencio')"""
    r = []
    for a, b in zip(pw, pw[1:]):
        s, e = a[2] + margem, b[1] - margem
        if e - s >= minimo - 2 * margem and e > s: r.append((s, e))
    if total is not None and total - (pw[-1][2] + margem) > 0.15: r.append((pw[-1][2] + margem, total - 0.02))
    return r
def bandas(x, sr, ints, nfft=2048):
    """dBFS RMS da banda (soma da potencia dos bins) nas bandas 7-14k e 100-1000 Hz, dentro dos intervalos"""
    m = x.mean(1) if x.ndim > 1 else x
    f = np.fft.rfftfreq(nfft, 1 / sr); hi = (f >= 7000) & (f <= 14000); lo = (f >= 100) & (f <= 1000)
    w = np.hanning(nfft); ph = []; pl = []
    for s, e in ints:
        a, b = int(s * sr), int(e * sr)
        for k in range(a, b - nfft, nfft // 2):
            S = np.abs(np.fft.rfft(m[k:k + nfft] * w)) ** 2 / (w ** 2).sum() * 2 / nfft
            ph.append(S[hi].sum()); pl.append(S[lo].sum())
    if not ph: return None
    db = lambda v: 10 * np.log10(np.mean(v) + 1e-20)
    return round(db(ph), 1), round(db(pl), 1), round(db(ph) - db(pl), 1), len(ph)
def fala(pw, margem=0.0):
    return [(w[1] - margem, w[2] + margem) for w in pw]

from scipy.signal import stft, istft
def metricas(x, sr=SR):
    """H = chiado: mediana da banda 7-14k nos quadros sem voz sonora (150-4k < -65 dB) mas ativos;
       S = p95 da banda 7-14k (sibilantes); L = mediana 150-4k nos quadros com voz"""
    m = x.mean(1) if x.ndim > 1 else x
    f, t, Z = stft(m, sr, nperseg=1024, noverlap=512); P = np.abs(Z) ** 2
    lo = 10 * np.log10(P[(f > 150) & (f < 4000)].mean(0) + 1e-20); hi = 10 * np.log10(P[(f > 7000) & (f < 14000)].mean(0) + 1e-20)
    voz = lo > -55
    return dict(H=round(float(np.percentile(hi[voz], 25)), 1), Hmed=round(float(np.median(hi[voz])), 1),
                S=round(float(np.percentile(hi[voz], 97)), 1), L=round(float(np.median(lo[voz])), 1))
def perfil_ruido(x, sr=SR, nfft=2048, q=25):
    """perfil de ruido por bin: mediana dos quadros 'so chiado' (sem voz sonora, ativos)"""
    m = x.mean(1) if x.ndim > 1 else x
    f, t, Z = stft(m, sr, nperseg=nfft, noverlap=nfft * 3 // 4); P = np.abs(Z) ** 2
    lo = 10 * np.log10(P[(f > 150) & (f < 4000)].mean(0) + 1e-20); hi = 10 * np.log10(P[(f > 7000) & (f < 14000)].mean(0) + 1e-20)
    voz = lo > -55
    return np.sqrt(np.percentile(P[:, voz], q, axis=1)), int(voz.sum())
def portao_espectral(x, N, sr=SR, nfft=2048, k=1.5, piso_db=-14, fmin=4000, suav_t=3, suav_f=5):
    """subtracao/gate espectral com perfil N (magnitude por bin). So atua acima de fmin (com rampa de 1 kHz),
       atenuacao maxima piso_db; ganho suavizado no tempo e na frequencia (evita 'musical noise'). Mantem o comprimento."""
    from scipy.ndimage import uniform_filter
    chans = [x[:, c] for c in range(x.shape[1])] if x.ndim > 1 else [x]
    out = []
    for c in chans:
        f, t, Z = stft(c, sr, nperseg=nfft, noverlap=nfft * 3 // 4)
        A = np.abs(Z) + 1e-12
        g = np.clip(1 - (k * N[:, None] / A) ** 2, 0, 1) ** 0.5
        g = uniform_filter(g, size=(suav_f, suav_t))
        fl = 10 ** (piso_db / 20); g = np.maximum(g, fl)
        w = np.clip((f - fmin) / 1000, 0, 1)[:, None]          # abaixo de fmin nao mexe
        g = 1 - w * (1 - g)
        _, y = istft(Z * g, sr, nperseg=nfft, noverlap=nfft * 3 // 4)
        y = y[:len(c)]; y = np.pad(y, (0, len(c) - len(y)))
        out.append(y.astype(np.float32))
    return np.stack(out, 1) if x.ndim > 1 else out[0]

def mascara_fala(x, pw, sr=SR, pre=0.05, pos=0.10, rel_db=40, abs_db=-62, min_gap=0.06, dil=0.03):
    """1 = fala. Uniao de (palavras do alinhamento com margem) e (quadros de 10 ms com energia > max(abs_db, mediana_fala - rel_db)).
       Buracos menores que min_gap ficam como fala. Retorna mascara por amostra (float 0/1)."""
    m = x.mean(1) if x.ndim > 1 else x
    hop = int(0.01 * sr); nfr = len(m) // hop + 1
    fr = np.zeros(nfr, bool)
    for w in pw:
        a = max(0, int((w[1] - pre) / 0.01)); b = min(nfr, int((w[2] + pos) / 0.01) + 1); fr[a:b] = True
    mm = np.pad(m, (0, nfr * hop - len(m))); e = np.sqrt((mm.reshape(nfr, hop) ** 2).mean(1) + 1e-20); edb = 20 * np.log10(e)
    thr = max(abs_db, np.median(edb[fr]) - rel_db)
    fr |= edb > thr
    d = int(dil / 0.01)
    if d: fr = np.convolve(fr.astype(float), np.ones(2 * d + 1), "same") > 0
    # fecha buracos curtos
    i = 0
    while i < nfr:
        if not fr[i]:
            j = i
            while j < nfr and not fr[j]: j += 1
            if (j - i) * 0.01 < min_gap and i > 0 and j < nfr: fr[i:j] = True
            i = j
        else: i += 1
    s = np.repeat(fr.astype(np.float32), hop)[:len(m)]
    return np.pad(s, (0, len(m) - len(s)), constant_values=s[-1] if len(s) else 0), thr
def portao_tempo(x, mask, sr=SR, fade=0.015, atn_db=-60):
    """aplica a mascara com rampas de 'fade' s (sem deslocar nada no tempo); fora da fala atenua atn_db"""
    n = int(fade * sr); k = np.ones(n) / n
    g = np.convolve(mask, k, "same"); g = np.clip(g, 0, 1)
    fl = 10 ** (atn_db / 20); g = fl + (1 - fl) * g
    return (x * g[:, None]).astype(np.float32) if x.ndim > 1 else (x * g).astype(np.float32)

def afftdn_perfil(x, trechos, nr=20, extra="", sr=SR, tmp=None):
    """afftdn com perfil de ruido amostrado: cola os 'trechos' (s,e) so de chiado no inicio, amostra (sample_noise)
       nesse prefixo, processa e corta o prefixo fora. Comprimento e tempo do audio original preservados."""
    import soundfile as sf, os, tempfile
    clip = np.concatenate([x[int(s * sr):int(e * sr)] for s, e in trechos])
    while len(clip) < sr: clip = np.concatenate([clip, clip])
    pre = np.concatenate([clip, x]); d = len(clip) / sr
    tmp = tmp or tempfile.mkdtemp(); p = os.path.join(tmp, "_pre.wav"); sf.write(p, pre, sr, subtype="FLOAT")
    af = f"asendcmd=c='0.0 afftdn sn start;{d - 0.01:.3f} afftdn sn stop',afftdn=nr={nr}:nf=-80:tr=1{extra}"
    y = load(p, sr=sr, ch=x.shape[1] if x.ndim > 1 else 1, af=af)
    return y[len(clip):len(clip) + len(x)]

# ---------------- cadeias finais ----------------
EQ_VOZ = "highshelf=f=10000:g=-3,lowpass=f=14000:p=2"
EQ_TRILHA = "lowpass=f=11500:p=2,lowpass=f=11500:p=2,highshelf=f=5000:g=-4"
def filtro(x, af, sr=SR):
    import soundfile as sf, tempfile, os
    d = tempfile.mkdtemp(); p = os.path.join(d, "f.wav"); sf.write(p, x, sr, subtype="FLOAT")
    y = load(p, sr=sr, ch=x.shape[1] if x.ndim > 1 else 1, af=af)
    os.remove(p); return y[:len(x)]
def limpar_voz(x, pw, q=35, k=2.0, piso_db=-18, eq=EQ_VOZ):
    """1) gate espectral >5 kHz com perfil medido na propria voz; 2) silencio real fora da fala (alinhamento+energia,
       rampas de 15 ms); 3) EQ suave (shelf -3 dB em 10 kHz + passa-baixa 14 kHz). Comprimento identico."""
    N, _ = perfil_ruido(x, q=q)
    y = portao_espectral(x, N, k=k, piso_db=piso_db, fmin=5000)
    mk, thr = mascara_fala(y, pw, pre=0.05, pos=0.08, rel_db=35, abs_db=-50, dil=0.02)
    z = portao_tempo(y, mk, fade=0.015, atn_db=-60)
    if eq: z = filtro(z, eq)
    return z, mk
def limpar_trilha(b, q=30, k=2.0, piso_db=-20, fmin=1500, eq=EQ_TRILHA):
    """trilha demucs: gate espectral acima de 1,5 kHz com perfil = percentil q de todos os quadros (chiado estacionario)
       + passa-baixa 11,5 kHz (24 dB/oit) + shelf -4 dB em 5 kHz (residuo de sibilantes da voz removida)"""
    m = b.mean(1) if b.ndim > 1 else b
    f, t, Z = stft(m, SR, nperseg=2048, noverlap=1536); P = np.abs(Z) ** 2
    tot = P.sum(0); act = tot > tot.max() * 1e-7
    N = np.sqrt(np.percentile(P[:, act], q, axis=1))
    y = portao_espectral(b, N, k=k, piso_db=piso_db, fmin=fmin)
    if eq: y = filtro(y, eq)
    return y
def lufs(x, sr=SR):
    import pyloudnorm as pyln
    return pyln.Meter(sr).integrated_loudness(x)
def ganho_lufs(x, alvo, sr=SR):
    return (x * 10 ** ((alvo - lufs(x, sr)) / 20)).astype(np.float32)
def true_peak_db(x, sr=SR):
    from scipy.signal import resample_poly
    return 20 * np.log10(np.abs(resample_poly(x, 4, 1, axis=0)).max() + 1e-20)
def finalizar_mix(mix, alvo=-16.0, tp=-1.5, sr=SR):
    """ganho estatico para 'alvo' LUFS; se o true peak passar de tp, limitador (alimiter) e reajuste"""
    y = ganho_lufs(mix, alvo, sr)
    for _ in range(4):
        if true_peak_db(y, sr) <= tp: break
        lim = 10 ** ((tp - 0.7) / 20)
        y = filtro(y, f"alimiter=limit={lim:.4f}:attack=2:release=60:level=false:latency=1")
        y = ganho_lufs(y, alvo, sr)
    return y

def dip_pausas(bed, mk, dip_db, sr=SR, min_pausa=0.25, rampa=0.15):
    """baixa a trilha dip_db nas pausas da voz com >= min_pausa s (rampas de 'rampa' s)"""
    if not dip_db: return bed
    from scipy.ndimage import uniform_filter1d
    p = (1 - mk).astype(np.float32)
    g = (uniform_filter1d(p, int(min_pausa * sr)) > 0.999).astype(np.float32)
    g = uniform_filter1d(g, int(rampa * sr))
    return (bed * (10 ** (-dip_db * g / 20))[:, None]).astype(np.float32)
