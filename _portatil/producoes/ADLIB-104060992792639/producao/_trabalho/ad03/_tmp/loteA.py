# -*- coding: utf-8 -*-
"""Lote A (08/10), sem credito:
1) quadro 282 (9,40 s): a boca original aparece aberta 1 q antes do p04. Cola a regiao boca+queixo do q283 (1o quadro do
   lipsync, mesma tomada, boca quase fechada) no q282 com borda suave. Reescreve base_lipsync.mp4 (antiga em _antes_loteA).
2) room tone: junta as janelas de 20 ms do orig.wav sem voz (vocals do demucs < pico-40 dB e sem efeito no no_vocals),
   faz um loop com crossfade e grava _audio/room_tone.wav (duracao do corpo) com o ambiente so nos silencios absolutos
   (< -50 dB por >= 0,5 s na mistura narracao+fundo), entrando/saindo em rampa de 120 ms. A fala nao e tocada."""
import sys, json, subprocess, shutil, cv2, numpy as np
from pathlib import Path
AD = Path(__file__).resolve().parent.parent
SR = 48000
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
def quadro():
    src = AD / "_antes_loteA/base_lipsync.mp4"
    cap = cv2.VideoCapture(str(src)); fr = []
    while True:
        ok, f = cap.read()
        if not ok: break
        fr.append(f)
    m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (358, 372), (78, 62), 0, 0, 360, 1.0, -1)
    m = cv2.GaussianBlur(m, (0, 0), 9)[..., None]
    fr[282] = np.clip(fr[283] * m + fr[282] * (1 - m), 0, 255).astype(np.uint8)
    ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-","-threads","4",
        "-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(AD / "base_lipsync.mp4")], stdin=subprocess.PIPE)
    for f in fr: ff.stdin.write(f.tobytes())
    ff.stdin.close(); ff.wait(); print("base ok", len(fr))
def rd(p):
    b = subprocess.run(["ffmpeg","-v","error","-i",str(p),"-ac","1","-ar",str(SR),"-f","f32le","-"], capture_output=True).stdout
    return np.frombuffer(b, np.float32).copy()
def db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
def room():
    O = rd(AD / "_audio/orig.wav"); V = rd(AD / "_audio/demucs/htdemucs/orig/vocals.wav"); NV = rd(AD / "_audio/demucs/htdemucs/orig/no_vocals.wav")
    w = int(0.02 * SR); n = min(len(O), len(V), len(NV)) // w
    ev = np.array([db(V[i*w:(i+1)*w]) for i in range(n)]); en = np.array([db(NV[i*w:(i+1)*w]) for i in range(n)])
    ok = (ev < ev.max() - 40) & (en < -50)
    # so janelas com vizinhas tambem sem voz (evita cauda de silaba)
    ok = ok & np.roll(ok, 1) & np.roll(ok, -1)
    pecas = [O[i*w:(i+1)*w] for i in np.where(ok)[0]]
    print(f"room tone: {len(pecas)} janelas de 20 ms ({len(pecas)*0.02:.2f} s), nivel mediano {np.median([db(p) for p in pecas]):.1f} dB")
    # loop com crossfade de 10 ms, ordem embaralhada
    rng = np.random.default_rng(3); xf = int(0.01 * SR); fade = np.linspace(0, 1, xf, dtype=np.float32)
    corpo = rd(AD / "_antes_loteA/corpo_ad03.mp4"); N = len(corpo)
    loop = np.zeros(0, np.float32)
    while len(loop) < N + SR:
        p = pecas[rng.integers(len(pecas))]
        if len(loop) == 0: loop = p.copy(); continue
        loop[-xf:] = loop[-xf:] * (1 - fade) + p[:xf] * fade; loop = np.concatenate([loop, p[xf:]])
    loop = loop[:N]
    loop -= np.convolve(loop, np.ones(480) / 480, mode="same")   # tira DC/rumble do loop
    # silencios absolutos na mistura atual (corpo antigo = narracao + fundo)
    w2 = int(0.05 * SR); m = len(corpo) // w2
    ec = np.array([db(corpo[i*w2:(i+1)*w2]) for i in range(m)]); sil = ec < -50
    env = np.zeros(N, np.float32); runs = []; k = 0
    while k < m:
        if sil[k]:
            j = k
            while j < m and sil[j]: j += 1
            if (j - k) * 0.05 >= 0.5: runs.append((k * 0.05, j * 0.05))
            k = j
        else: k += 1
    r = int(0.12 * SR)
    for a, b in runs:
        ia, ib = max(0, int(a * SR) - r // 2), min(N, int(b * SR) + r // 2)
        e = np.ones(ib - ia, np.float32); e[:r] = np.linspace(0, 1, r); e[-r:] = np.linspace(1, 0, r)
        env[ia:ib] = np.maximum(env[ia:ib], e)
    alvo = -50.0   # um pouco acima do ambiente real do original (-52 dB): "sala baixa", audivel so nas pausas
    g = 10 ** ((alvo - db(loop)) / 20)
    out = loop * g * env
    print("silencios cobertos:", ", ".join(f"{a:.2f}-{b:.2f}" for a, b in runs))
    st = np.stack([out, out], 1).astype(np.float32)
    subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","2","-i","-","-c:a","pcm_s16le",str(AD / "_audio/room_tone.wav")],
                   input=st.tobytes(), check=True)
    json.dump({"silencios": runs, "nivel_db": alvo, "janelas": len(pecas)}, open(AD / "_audio/room_tone.json", "w"), indent=1)
if __name__ == "__main__":
    if "quadro" in sys.argv: quadro()
    if "room" in sys.argv: room()
