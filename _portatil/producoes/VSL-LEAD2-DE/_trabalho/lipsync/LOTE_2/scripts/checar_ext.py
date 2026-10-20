# -*- coding: utf-8 -*-
"""Indice de pausa com as bordas: trecho final <id>.mp4 + ate 0,6 s do vizinho da mesma cena de cada lado (os cortes
cairam nas pausas da fala DE, entao as pausas ficam nas bordas). Audio DE da narracao no mesmo intervalo. Original = es_
(esticado) dos mesmos trechos. Uso: python checar_ext.py [id...] -> _tmp/ext.json"""
import json, subprocess, sys, os, re
from pathlib import Path
R = Path(r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\lipsync\LOTE_2"); E = R / "_tmp" / "ext"; E.mkdir(exist_ok=True)
NARR = r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\voz\narracao_de_completa.wav"
KIT = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas\checar_lipsync.py"
P = json.load(open(R / "plano.json")); B = 18
J = E.parent / "ext.json"; res = json.load(open(J, encoding="utf-8")) if J.exists() else {}
so = set(sys.argv[1:])
for k, x in enumerate(P):
    i = x["id"]
    if x["crop"] or (so and i not in so) or (not so and i in res) or not (R / f"{i}.mp4").exists(): continue
    partes = []; a0, a1 = x["q0"], x["q1"]
    pv = P[k - 1] if k > 0 else None; nx = P[k + 1] if k + 1 < len(P) else None
    if pv and not pv["crop"] and (R / f"{pv['id']}.mp4").exists():
        partes.append((pv["id"], pv["N"] - B, pv["N"])); a0 -= B
    partes.append((i, 0, x["N"]))
    if nx and not nx["crop"] and (R / f"{nx['id']}.mp4").exists():
        partes.append((nx["id"], 0, B)); a1 += B
    for nome, pre in (("s", ""), ("o", "es_")):
        ins = []; fc = []
        for j, (pid, f0, f1) in enumerate(partes):
            src = R / f"{pid}.mp4" if nome == "s" else R / "in" / f"es_{pid}.mp4"
            ins += ["-i", str(src)]; fc.append(f"[{j}:v]trim=start_frame={f0}:end_frame={f1},setpts=PTS-STARTPTS[v{j}]")
        fc.append("".join(f"[v{j}]" for j in range(len(partes))) + f"concat=n={len(partes)}:v=1:a=0[v]")
        cmd = ["ffmpeg", "-v", "error", "-y", *ins]
        if nome == "o":  # audio ES esticado dos mesmos trechos
            for j, (pid, f0, f1) in enumerate(partes):
                fc.append(f"[{j}:a]atrim={f0/30:.4f}:{f1/30:.4f},asetpts=PTS-STARTPTS[a{j}]")
            fc.append("".join(f"[a{j}]" for j in range(len(partes))) + f"concat=n={len(partes)}:v=0:a=1[a]")
            cmd += ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-c:a", "aac"]
        else:
            cmd += ["-filter_complex", ";".join(fc), "-map", "[v]"]
        subprocess.run(cmd + ["-c:v", "libx264", "-crf", "16", "-preset", "veryfast", str(E / f"{nome}_{i}.mp4")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", NARR, "-af", f"atrim={a0/30:.5f}:{a1/30:.5f},asetpts=PTS-STARTPTS", "-ac", "1", str(E / f"de_{i}.wav")], check=True)
    r = subprocess.run([sys.executable, KIT, str(E / f"s_{i}.mp4"), "--audio-novo", str(E / f"de_{i}.wav"), "--original", str(E / f"o_{i}.mp4")],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    t = r.stdout.strip(); m = re.search(r"índice de pausa ([0-9.]+|-) \((\d+) quadros", t)
    st = re.findall(r"^(APROVADO|AVISO|REPROVADO)", t, re.M)
    res[i] = {"indice": (float(m.group(1)) if m and m.group(1) != "-" else None), "q_pausa": int(m.group(2)) if m else 0,
              "checar": st[-1] if st else "ERRO", "log": t}
    print(i, res[i]["checar"], res[i]["indice"], res[i]["q_pausa"], flush=True)
    json.dump(res, open(J, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
