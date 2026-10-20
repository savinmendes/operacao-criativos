def janelas():
    out = []
    for tipo, a, b, kw in EDL:
        A = 0.0 if a <= 0 else S(a)
        # início de trecho que cai logo depois de um corte: S(a) já desconta o corte
        out.append((tipo, A, S(b) if not any(abs(b - ra) < 1e-6 for ra, _ in REMOV) else S(b), a, b, kw))
    return out


def run(cmd, cwd=None):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd)
    if r.returncode:
        print(" ".join(map(str, cmd))[:3000]); print(r.stderr[-3000:]); sys.exit(1)
    return r


def crop_zoom(z, centro, W=1080, H=1920):
    if z <= 1.0:
        return ""
    cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    x = int(min(max(centro[0] - cw / 2, 0), W - cw)); y = int(min(max(centro[1] - ch / 2, 0), H - ch))
    return f"crop={cw}:{ch}:{x}:{y},"


def padre_full():
    out = M / "padre_full.mp4"
    partes = sorted(PA.glob("padre_parte*.mp4"))
    assert partes, "faltam padre_parte*.mp4"
    lst = M / "padre_lista.txt"
    lst.write_text("".join(f"file '{q.as_posix()}'\n" for q in partes), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-vf", "fps=30,format=yuv420p",
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-an", str(out)])
    return out


def render(i, tipo, T0, T1, a, kw, PADRE):
    out = M / f"seg_{i:02d}.mp4"
    n = round(T1 * FPS) - round(T0 * FPS)
    base = "scale=1080:1920:flags=lanczos,setsar=1"
    vel = 1.0
    if tipo == "img":
        W0, H0 = 1440, 2560
        z0, z1 = kw["z0"], kw["z1"]; cx, cy = kw["c"]
        # push-in suave: zoompan sobre a imagem 2x (evita tremido de arredondamento)
        zexp = f"{z0}+({z1}-{z0})*on/{max(1, n - 1)}"
        vf = (f"scale={W0 * 2}:{H0 * 2},zoompan=z='{zexp}':x='{cx * 2}-iw/zoom/2':y='{cy * 2}-ih/zoom/2':d={n}:"
              f"s=1080x1920:fps=30,setsar=1")
        inp = ["-loop", "1", "-framerate", "1", "-t", "1", "-i", str(kw["src"])]
        vf += f",trim=end_frame={n}"
    elif tipo == "take":
        dur_src = 5.0 - kw.get("ss", 0.0)
        vel = min(1.0, max(0.5, dur_src / (n / FPS)))
        fr = "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1," if (kw.get("interp") or vel < 0.97) else "fps=30,"
        vf = f"setpts=(PTS-STARTPTS)/{vel:.4f}," + fr + crop_zoom(kw.get("zoom", 1.0), kw.get("centro", (540, 960))) + base
        inp = ["-ss", f"{kw['ss']:.3f}", "-i", str(kw["src"])]
    elif tipo == "selfie":
        vf = "fps=30," + crop_zoom(kw["zoom"], ROSTO_SELF) + base
        inp = ["-ss", f"{a - T_SELF:.3f}", "-t", f"{n / FPS + 0.3:.3f}", "-i", str(SELFIE)]
    else:
        vf = "fps=30," + crop_zoom(kw["zoom"], ROSTO_SAC) + base
        inp = ["-ss", f"{a - T_PAD:.3f}", "-t", f"{n / FPS + 0.3:.3f}", "-i", str(PADRE)]
    vf += ",tpad=stop_mode=clone:stop_duration=1,format=yuv420p"
    run(["ffmpeg", "-v", "error", "-y", *inp, "-vf", vf, "-frames:v", str(n), "-an", "-r", "30", "-c:v", "libx264",
         "-preset", "fast", "-crf", "12", "-pix_fmt", "yuv420p", "-x264-params", "keyint=60", *TAGS, str(out)])
    return out, n, vel


def load(path, af=None):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path)] + (["-af", af] if af else []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs_norm(x, alvo):
    import pyloudnorm as pyln
    l = pyln.Meter(SR).integrated_loudness(x.astype(np.float64))
    return (x * 10 ** ((alvo - l) / 20)).astype(np.float32)


def narracao():
    """monta a narração em t (antes dos cortes) + palavras."""
    n = int(NARR_FIM * SR) + SR
    out = np.zeros((n, 2), np.float32)
    ws = []
    f = int(0.01 * SR)

    def put(x, t0):
        x = x.copy(); x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
        i = int(t0 * SR); out[i:i + len(x)] += x[:n - i]

    hook = lufs_norm(load(P / "hook.mp3"), -18.0)
    put(hook[:int(HOOK_FIM * SR)], 0.0)
    ws += [w for w in W_HOOK if w["fim"] <= HOOK_FIM]
    rz = load(PP / "reza.mp3")
    rz = lufs_norm(rz, -20.0)
    raw_r = M / "reza_n.f32"; raw_r.write_bytes(rz.astype(np.float32).tobytes())
    rz = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw_r),
                                       "-af", "aecho=0.8:0.5:45|95:0.22|0.12", "-f", "f32le", "-"], capture_output=True).stdout,
                       np.float32).reshape(-1, 2).copy(); raw_r.unlink()
    wr = [dict(w, personagem=SLUG, parte="reza") for w in mv.palavras(PP / "reza.alinhamento.json")]
    t = T_REZA
    for a, b in REZA:
        put(rz[int(a * SR):int(b * SR)], t)
        ws += [dict(w, ini=round(w["ini"] - a + t, 3), fim=round(min(w["fim"], b) - a + t, 3)) for w in wr if w["ini"] >= a and w["ini"] < b - 0.1]
        t += (b - a) + REZA_GAP
    sel = lufs_norm(load(P / "selfie.mp3"), -18.0)
    put(sel, T_SELF)
    ws += [dict(w, ini=round(w["ini"] + T_SELF, 3), fim=round(w["fim"] + T_SELF, 3)) for w in W_SELF]
    pad = load(PA / "padre.mp3")
    put(pad, T_PAD)
    ws += [dict(w, ini=round(w["ini"] + T_PAD, 3), fim=round(w["fim"] + T_PAD, 3), personagem="sacerdote") for w in W_PAD]
    return out[:int(NARR_FIM * SR)], ws


def audio():
    voz, ws = narracao()
    # aplica os cortes
    keep, s0 = [], 0.0
    for a, b in sorted(REMOV):
        keep.append((s0, a)); s0 = b
    keep.append((s0, NARR_FIM))
    f = int(0.008 * SR); partes = []
    for a, b in keep:
        seg = voz[int(a * SR):int(b * SR)].copy()
        seg[:f] *= np.linspace(0, 1, f)[:, None]; seg[-f:] *= np.linspace(1, 0, f)[:, None]
        partes.append(seg)
    out_v = np.concatenate(partes)
    n = int(round(TOTAL * SR))
    out_v = np.pad(out_v, ((0, max(0, n - len(out_v))), (0, 0)))[:n]
    # 2 climas: tensão (reza/salão vazio) -> esperança a partir do corte p/ o salão cheio (crossfade 0,3 s)
    tt = np.arange(n) / SR
    g0, g1 = S(C), S(T_SELF)
    xf = 0.30
    ten = load(AQ / "audio" / "trilha_tensao.wav")
    esp = load(AQ / "audio" / "trilha_esperanca.wav")
    tr = np.zeros((n, 2), np.float32)
    k0 = int((g0 - xf / 2) * SR); k1 = int((g0 + xf / 2) * SR)
    a = ten[:k1].copy(); a = np.pad(a, ((0, max(0, k1 - len(a))), (0, 0)))
    a[k0:k1] *= np.linspace(1, 0, k1 - k0)[:, None]
    tr[:k1] += a
    b = esp[:n - k0].copy()
    b[:k1 - k0] *= np.linspace(0, 1, k1 - k0)[:, None]
    tr[k0:k0 + len(b)] += b
    # salão cheio sem voz: esperança +6 dB, volta à base (-32) quando a selfie começa
    x = np.clip(np.minimum((tt - g0) / 0.6, (g1 + 1.0 - tt) / 1.2), 0, 1)
    db = 6 * x + 3 * np.clip((tt - CTA) / 1.5, 0, 1)
    mix = out_v + tr * (10 ** (db / 20))[:, None]
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af",
             "loudnorm=I=-14:TP=-2.5:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-2.5:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']},"
          f"alimiter=limit=0.74:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", af,
         "-t", f"{TOTAL:.3f}", "-c:a", "pcm_s16le", str(M / "mix.wav")])
    raw.unlink()
    # palavras em T (legenda)
    wT = [dict(w, ini=S(w["ini"]), fim=S(w["fim"])) for w in ws]
    (M / "palavras_T.json").write_text(json.dumps(wT, ensure_ascii=False, indent=1), encoding="utf-8")
    print("audio ok", js["input_i"])


def final():
    run([sys.executable, str(P / "legenda_comp.py")])
    fonts = M / "fonts"
    if not fonts.exists():
        fonts.mkdir()
        for fz in (AQ / "fonts").glob("*.ttf"):
            (fonts / fz.name).write_bytes(fz.read_bytes())
    ins = ["-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav"]
    pngs = [("titulo_gancho.png", 0, T_REZA), ("cta_masinfo_unico.png", CTA, TOTAL), ("selo_ficticio_mini.png", 0, TOTAL)]
    fc = []
    for k, (pg, a, b) in enumerate(pngs):
        ins += ["-loop", "1", "-framerate", "30", "-t", f"{TOTAL + 1:.3f}", "-i", str(GR / pg)]
        fc.append(f"[{k + 2}:v]format=rgba[p{k}]")
    fc.append("[0:v]ass=leg_comp2.ass:fontsdir=fonts[l]"); ult = "[l]"
    for k, (pg, a, b) in enumerate(pngs):
        en = "" if (a <= 0 and b >= TOTAL) else f":enable='between(t,{a:.3f},{b - 0.001:.3f})'"
        fc.append(f"{ult}[p{k}]overlay=0:0:format=auto{en}[o{k}]"); ult = f"[o{k}]"
    fc.append(f"{ult}format=yuv420p[v]")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "1:a", "-af", "apad",
         "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-profile:v", "high", "-pix_fmt", "yuv420p", *TAGS,
         "-r", "30", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
         "-t", f"{TOTAL:.3f}", str(SAIDA)], cwd=M)
    print("final ok", SAIDA, TOTAL)


if __name__ == "__main__":
    J = janelas()
    for (_, a0, b0, *_), (_, a1, *_) in zip(J, J[1:]):
        assert abs(b0 - a1) < 1e-6, (b0, a1)
    (M / "mapa_cenas.json").write_text(json.dumps(
        [dict(i=i, tipo=t, T_ini=round(A, 3), T_fim=round(B, 3), narr_ini=round(a, 3), narr_fim=round(b, 3),
              fonte=Path(str(kw.get("src", t))).name) for i, (t, A, B, a, b, kw) in enumerate(J)],
        ensure_ascii=False, indent=1), encoding="utf-8")
    (M / "tempos.json").write_text(json.dumps({"total": TOTAL, "cta": CTA, "T_SELF": T_SELF, "T_PAD": T_PAD,
                                               "remov": REMOV}, indent=1), encoding="utf-8")
    if "--plano" in sys.argv:
        for j in J: print(j[0], round(j[1], 2), round(j[2], 2), round(j[2] - j[1], 2))
        print("TOTAL", TOTAL, "CTA", CTA); sys.exit()
    if "--so-audio" not in sys.argv and "--so-final" not in sys.argv:
        PADRE = padre_full()
        lista, tot = [], 0
        for i, (t, A, B, a, b, kw) in enumerate(J):
            out, nq, vel = render(i, t, A, B, a, kw, PADRE); lista.append(out); tot += nq
            print(f"[{i + 1}/{len(J)}] {t:6s} {A:6.2f}-{B:6.2f} vel {vel:.2f}", flush=True)
        assert tot == round(TOTAL * FPS), (tot, TOTAL * FPS)
        (M / "lista.txt").write_text("".join(f"file '{q.name}'\n" for q in lista), encoding="utf-8")
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(M / "lista.txt"), "-c", "copy", str(M / "corpo.mp4")])
    if "--so-final" not in sys.argv:
        audio()
    if "--so-audio" not in sys.argv:
        final()
