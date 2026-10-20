# -*- coding: utf-8 -*-
"""Monta gancho_G2.mp4 e gancho_G4.mp4 (720x1280, 30 fps, AAC 44,1k estéreo). uso: python montar_ganchos.py [g2|g4|ambos]"""
import sys, subprocess, numpy as np, soundfile as sf, librosa, pyloudnorm as pyln
from pathlib import Path
from legenda import gerar
W = Path(__file__).resolve().parent; O = W / "overlays"; A = W / "audio"; T = W / "trab"; SR = 44100
MUS = r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_es\audio\v4\sep\htdemucs\ini10\no_vocals.wav"
CORTE_V4 = 8.05   # a selfie começa em 8,05 s do v4: a trilha do gancho termina aí para emendar com a do corpo
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
       "-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]
med = pyln.Meter(SR)


def ld(p, mono=True):
    return librosa.load(str(p), sr=SR, mono=mono)[0]


def lufs(y, alvo):
    return y * 10 ** ((alvo - med.integrated_loudness(y)) / 20)


def fx(y, f):
    sf.write(T / "_in.wav", y, SR, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(T / "_in.wav"), "-af", f, "-c:a", "pcm_f32le", str(T / "_out.wav")], check=True)
    return sf.read(T / "_out.wav")[0]


def put(buf, y, t0, ini=0.0, dur=None, g=1.0):
    y = y[int(ini * SR):]
    y = y if dur is None else y[: int(dur * SR)]
    n = int(t0 * SR); k = min(len(y), len(buf) - n)
    if k > 0:
        buf[n: n + k] += y[:k] * g


def trilha(dur):
    m = ld(MUS, mono=False).T          # (n,2)
    return m[int((CORTE_V4 - dur) * SR): int(CORTE_V4 * SR)].mean(1)  # mesmo ganho do v4 (continua no corpo)


def limitar(y, teto=0.89):
    from scipy.ndimage import maximum_filter1d, uniform_filter1d
    env = maximum_filter1d(np.abs(y), size=int(0.010 * SR)); g = np.minimum(1.0, teto / np.maximum(env, 1e-9))
    return y * np.minimum(g, uniform_filter1d(g, int(0.005 * SR)))


def finaliza(vid_in, filtro_base, itens, wav, saida, dur):
    ins, fl, cur = [], [], "b"
    for k, (png, a, b) in enumerate(itens):
        ins += ["-loop", "1", "-framerate", "30", "-i", png]
        en = "" if a is None else f":enable='between(t,{a:.3f},{b - 0.001:.3f})'"
        fl.append(f"[{cur}][{k + 1}:v]overlay=0:0:shortest=1{en}[o{k}]"); cur = f"o{k}"
    fc = ";".join([f"[0:v]{filtro_base}[b]"] + fl)
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", vid_in] + ins + ["-i", str(wav), "-filter_complex", fc, "-map", f"[{cur}]",
           "-map", f"{len(itens) + 1}:a", "-t", f"{dur:.3f}"] + ENC + ["-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2",
                                                                       "-movflags", "+faststart", str(saida)]
    subprocess.run(cmd, check=True)


def g2():
    av = W / "heygen" / "g2_avatar_v2.mp4"; DUR = 6.60
    # áudio: sussurro (o mesmo que foi ao HeyGen, 0,3 s de entrada) + batidas fora de quadro + trilha do v4
    voz = fx(ld(A / "g2_heygen.mp3"), "highpass=f=90,aecho=0.8:0.6:28|55:0.18|0.10"); voz = lufs(voz, -13.5)
    bat = fx(ld(A / "sfx_batidas.mp3"), "lowpass=f=2600,highpass=f=50"); bat = lufs(bat[int(1.3 * SR):], -20)
    mix = np.zeros(int(DUR * SR) + SR)
    put(mix, voz, 0.0)
    put(mix, bat, 0.0, 0.0, 3.85); put(mix, bat, 3.85, 0.1)
    put(mix, trilha(DUR), 0.0)
    mix = limitar(mix[: int(DUR * SR)]); sf.write(T / "g2_mix.wav", np.stack([mix, mix], 1), SR, subtype="PCM_16")
    # cada batida -> sobressalto curto na câmera
    on = [t for t in librosa.onset.onset_detect(y=ld(A / "sfx_batidas.mp3"), sr=SR, units="time") if t >= 1.3]
    ks = sorted({round(t - 1.3, 2) for t in on if t - 1.3 < 3.85} | {round(t - 1.4 + 3.85, 2) for t in on if t - 1.4 + 3.85 < DUR})
    jolt = "+".join(f"exp(-pow((t-{k})/0.05\\,2))" for k in ks)
    x = f"(iw-720)/2+9*sin(2*PI*0.6*t)+4*sin(2*PI*1.9*t)+7*({jolt})"
    y = f"(ih-1280)/2+7*sin(2*PI*0.45*t+1)+3*sin(2*PI*2.6*t)-9*({jolt})"
    base = (f"fps=30,scale=780:1387,crop=720:1280:x='{x}':y='{y}',eq=brightness=-0.06:gamma=0.86:saturation=0.88,"
            f"vignette=angle=PI/3.6,noise=alls=7:allf=t,setsar=1")
    blocos = [[("SI", 0.30), ("ESTE", 0.52), ("VIDEO", 0.74)], [("SE", 1.00), ("CORTA…", 1.20)],
              [("BUSQUEN", 2.44), ("AL", 3.20), ("PADRE", 3.30)], [("JUAN", 3.58), ("MÉNDEZ.", 3.90)],
              [("ÉL", 5.08), ("TIENE", 5.24), ("LA", 5.52)], [("ORACIÓN.", 5.68), ("", 6.45)]]
    leg = gerar(blocos, T / "leg_g2")
    itens = [(str(O / "titulo_g2.png"), None, None)] + leg + [(str(O / "selo10.png"), None, None)]
    finaliza(str(av), base, itens, T / "g2_mix.wav", W / "gancho_G2.mp4", DUR)


def g4():
    av = W / "heygen" / "g4_avatar.mp4"; OFF = 0.6
    TA, TB, TC, TD = 2.40, 23 / 30, 8 / 30, 83 / 30        # A fala | B mão tira o celular | C queda | D transmissão interrompida
    DUR = TA + TB + TC + TD
    p = T / "g4p"; p.mkdir(exist_ok=True)
    run = lambda c: subprocess.run(["ffmpeg", "-v", "error", "-y"] + c, check=True)
    run(["-ss", f"{OFF}", "-t", f"{TA}", "-i", str(av), "-vf", "fps=30,setsar=1", "-frames:v", "72", "-an"] + ENC + [str(p / "a.mp4")])
    # B: tremida crescente + rotação (o celular sai do tripé) + borrão de movimento + mão escura passando na frente
    rot = f"pow(t/{TB}\\,2)*1.25"; sh = f"(6+70*pow(t/{TB}\\,2))"
    fb = (f"[0:v]fps=30,scale=900:1600,rotate=a='{rot}':ow=900:oh=1600:c=black,"
          f"crop=720:1280:x='90+{sh}*sin(t*61)':y='160+{sh}*cos(t*47)+150*pow(t/{TB}\\,3)',tmix=frames=3,"
          f"eq=brightness='-0.25*t/{TB}':eval=frame,setsar=1[v];"
          f"[1:v]format=rgba[m];[v][m]overlay=x='760-1250*t/0.42':y='-60+120*t':enable='lt(t,0.5)'[o]")
    run(["-ss", f"{OFF + TA}", "-t", f"{TB}", "-i", str(av), "-loop", "1", "-i", str(O / "mao.png"),
         "-filter_complex", fb, "-map", "[o]", "-frames:v", "23", "-an"] + ENC + [str(p / "b.mp4")])
    # C: impacto: quadro escuro, borrado e girado, com ruído forte
    fc_ = ("fps=30,scale=900:1600,rotate=a=2.6:ow=900:oh=1600:c=black,crop=720:1280:90:160,boxblur=18:2,"
           "eq=brightness=-0.42,noise=alls=60:allf=t,setsar=1")
    run(["-ss", f"{OFF + TA + TB - 0.30}", "-i", str(av), "-vf", fc_ + ",tpad=stop_mode=clone:stop_duration=1", "-frames:v", "8", "-an"] + ENC + [str(p / "c.mp4")])
    # D: cartão com glitch nos primeiros 0,4 s e um repique em 1,3 s
    fd = ("[0:v]fps=30,format=yuv420p,split[x][y];"
          "[x]rgbashift=rh=-14:bh=14:gv=6,noise=alls=45:allf=t,crop=696:1280:x='mod(n*37\\,24)':y=0,scale=720:1280[g];"
          "[y][g]overlay=0:0:enable='lt(t,0.40)+between(t,1.30,1.40)',setsar=1[o]")
    run(["-loop", "1", "-framerate", "30", "-t", f"{TD}", "-i", str(O / "interrompida.png"),
         "-filter_complex", fd, "-map", "[o]", "-frames:v", "83", "-an"] + ENC + [str(p / "d.mp4")])
    (p / "lista.txt").write_text("".join(f"file '{(p / n).as_posix()}'\n" for n in ("a.mp4", "b.mp4", "c.mp4", "d.mp4")))
    run(["-f", "concat", "-safe", "0", "-i", str(p / "lista.txt"), "-c", "copy", str(p / "base.mp4")])
    # áudio
    voz = fx(ld(A / "g4_heygen.mp3"), "highpass=f=90,aecho=0.8:0.55:45|90:0.2|0.12"); voz = lufs(voz, -12.5)
    mix = np.zeros(int(DUR * SR) + SR)
    put(mix, voz, 0.0, OFF, TA + 0.02)
    q = lufs(ld(A / "sfx_queda.mp3"), -15); put(mix, q, TA - 0.45, 0.0)            # 1º golpe do SFX (0,46 s) na pegada
    gl = lufs(ld(A / "sfx_glitch.mp3"), -17)
    put(mix, gl, TA + TB + TC - 0.02, 0.0, 0.45); put(mix, gl, TA + TB + TC + 1.28, 0.1, 0.14, g=0.8)
    tr = trilha(DUR); env = np.ones(len(tr)); env[int((TA + TB + TC) * SR):] = 0.55          # trilha mais baixa na tela preta
    put(mix, tr * env, 0.0)
    mix = limitar(mix[: int(DUR * SR)]); sf.write(T / "g4_mix.wav", np.stack([mix, mix], 1), SR, subtype="PCM_16")
    blocos = [[("OH", 0.30), ("PODEROSO", 0.54)], [("SAN", 1.10), ("BENITO,", 1.34)], [("GUAR—", 2.18), ("", TA + 0.30)]]
    leg = gerar(blocos, T / "leg_g4")
    itens = [(str(O / "moldura_live.png"), 0.0, TA + TB)] + leg + [(str(O / "selo10.png"), None, None)]
    finaliza(str(p / "base.mp4"), "setsar=1", itens, T / "g4_mix.wav", W / "gancho_G4.mp4", DUR)


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "ambos"
    if q in ("g2", "ambos"):
        g2(); print("ok G2")
    if q in ("g4", "ambos"):
        g4(); print("ok G4")
