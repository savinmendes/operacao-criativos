# -*- coding: utf-8 -*-
"""Variação gancho × corpo (Lymphoria / Drenagem LATAM), mesmo método da podadora:
banco de tomadas (scdet) com margem nas bordas, sem repetir cena contínua, sem quadro solto.

  python gerar_var.py <VAR_NN> <G1..G10> <corpo NN> [semente]

- Gancho: fala nova com a MESMA voz clonada do narrador do corpo (tts_elevenlabs), tomadas dos ADs finais
  (preferindo o trecho antes do corte do próprio corpo, que não aparece no corpo), caixa de texto grande no estilo
  do kit cobrindo a legenda queimada original, fundo musical = a música do próprio corpo (demucs no_vocals) terminando
  exatamente no corte, para emendar sem pulo.
- Corpo: o .mp4 FINAL do AD (pasta producao) do ponto de corte até o fim (oferta COD).
Saída: producao/VARIACOES/VAR NN - G<k>-<GANCHO> x AD<corpo>.mp4
"""
import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

V = Path(__file__).resolve().parent
PROD = V.parent.parent
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
FB = str(KIT / "fonts" / "Poppins-Bold.ttf")
W, H, FPS = 720, 1280, 30
sys.path.insert(0, str(KIT / "ferramentas"))

VAR, GK, CC = sys.argv[1], sys.argv[2], sys.argv[3]
SEED = int(sys.argv[4]) if len(sys.argv) > 4 else int(VAR) * 7 + 3
random.seed(SEED)
CORPOS = json.load(open(V / "corpos.json", encoding="utf-8"))
GANCHOS = json.load(open(V / "ganchos.json", encoding="utf-8"))
cp = CORPOS[CC]
gen = cp["genero"]
g = GANCHOS[GK]
texto = g[gen]
nome_g = g.get(f"nome_{gen}", g["nome"])
T = V / "trab" / VAR
T.mkdir(parents=True, exist_ok=True)


def run(*a, **k):
    subprocess.run([str(x) for x in a], check=True, **k)


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True).stdout)


def final_de(nn):
    return Path((V / "fontes" / nn / "final.txt").read_text(encoding="utf-8").strip())


def lufs(f, ss=None, t=None):
    a = ["ffmpeg", "-hide_banner", "-nostats"]
    if ss is not None:
        a += ["-ss", str(ss)]
    if t is not None:
        a += ["-t", str(t)]
    a += ["-i", str(f), "-vn", "-af", "ebur128", "-f", "null", "-"]
    r = subprocess.run(a, capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])


# ---------------- 1) fala do gancho (voz clonada do narrador do corpo) ----------------
VZ = V / "voz"
VZ.mkdir(exist_ok=True)
fala = VZ / f"{CC}_{GK}.mp3"
alin = VZ / f"{CC}_{GK}.alinhamento.json"
if not fala.exists():
    import tts_elevenlabs as TTS
    TTS.gerar(texto, str(fala), voz=cp["voz"])
    reg = V / "custo_tts.json"
    c = json.load(open(reg, encoding="utf-8")) if reg.exists() else {}
    c[f"{CC}_{GK}"] = len(texto)
    json.dump(c, open(reg, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
al = json.load(open(alin, encoding="utf-8"))
al = al.get("alignment") or al
D = dur(fala)
LEAD, TAIL = 0.12, 0.30
Hd = round((LEAD + D + TAIL) * FPS) / FPS

# ---------------- 2) tomadas do gancho ----------------
def tomadas(nn, ini, fim):
    b = json.load(open(V / "fontes" / nn / "banco.json", encoding="utf-8"))
    out = []
    for t in b:
        if t["ini"] < ini - 0.01 or t["fim"] > fim + 0.01:
            continue
        a0, a1 = t["ini"] + 0.15, t["fim"] - 0.2  # margem: o corte do scdet não é exato
        if a1 - a0 >= 0.9:
            out.append({"src": nn, "a0": a0, "a1": a1, "grupo": f"{nn}:{t['grupo']}"})
    return out

pools = []
for nn, ini, fim in cp["pool"]:
    if (V / "fontes" / nn / "banco.json").exists():
        p = tomadas(nn, ini, fim)
        random.shuffle(p)
        pools.append(p)
cand = []
# intercala: 2 do próprio corpo para 1 de fora, mantendo a preferência pelo trecho antes do corte
p0 = pools[0] if pools else []
outros = [x for p in pools[1:] for x in p]
random.shuffle(outros)
cand = p0 + outros  # primeiro o trecho antes do corte do próprio corpo (não aparece no corpo); depois os outros
segs, usados, falta, ult = [], set(), Hd, None
for c in cand:
    if falta <= 0.01:
        break
    if c["grupo"] in usados or c["grupo"] == ult:
        continue
    disp = c["a1"] - c["a0"]
    L = min(disp, random.uniform(1.5, 2.5))
    if falta - L < 0.8:  # não deixar sobra curta: absorve na tomada atual se couber
        L = falta if falta <= disp else min(disp, falta - 0.8)
    L = round(min(L, falta) * FPS) / FPS
    if L < 0.8 - 1e-6:
        continue
    a0 = c["a0"] + (disp - L) / 2
    segs.append({"src": c["src"], "ini": round(a0, 3), "dur": L})
    usados.add(c["grupo"]); ult = c["grupo"]
    falta = round(falta - L, 4)
if falta > 0.01:
    raise SystemExit(f"banco insuficiente para o gancho ({falta:.2f}s faltando)")
json.dump(segs, open(T / "tomadas.json", "w"), indent=0)

lista = []
for k, s in enumerate(segs):
    o = T / f"s{k:02d}.mp4"
    n = int(round(s["dur"] * FPS))
    run("ffmpeg", "-v", "error", "-y", "-ss", f"{s['ini']:.3f}", "-i", final_de(s["src"]), "-an", "-frames:v", n,
        "-vf", f"fps={FPS},scale={W}:{H},setsar=1", "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-pix_fmt", "yuv420p", o)
    lista.append(f"file '{o.as_posix()}'")
(T / "lista.txt").write_text("\n".join(lista))
run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", T / "lista.txt", "-c", "copy", T / "gancho_v.mp4")

# ---------------- 3) caixas de texto (frase a frase, cobrindo a legenda queimada) ----------------
chars = al["characters"]
st = al["character_start_times_seconds"]
frases, buf, ini_f = [], "", None
for ch, t0 in zip(chars, st):
    if ini_f is None and ch.strip():
        ini_f = t0
    buf += ch
    if ch in ".?!" and buf.strip():
        frases.append((buf.strip(), ini_f)); buf, ini_f = "", None
if buf.strip():
    frases.append((buf.strip(), ini_f))


def caixa(txt, destino, cy, minw, minh, px=46):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FB, px)
    pal, linhas, cur = txt.split(), [], ""
    for w in pal:
        tst = (cur + " " + w).strip()
        if d.textlength(tst, font=f) > 620 and cur:
            linhas.append(cur); cur = w
        else:
            cur = tst
    linhas.append(cur)
    lh = int(px * 1.28)
    bw = max(max(d.textlength(l, font=f) for l in linhas) + 48, minw)
    bh = max(lh * len(linhas) + 30, minh)
    x0, y0 = W / 2 - bw / 2, cy - bh / 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=18, fill=(255, 255, 255, 255))
    ty = cy - lh * len(linhas) / 2 - px * 0.08
    for l in linhas:
        d.text((W / 2 - d.textlength(l, font=f) / 2, ty), l, font=f, fill=(0, 0, 0, 255))
        ty += lh
    img.save(destino)


ovs = []
for k, (txt, t0) in enumerate(frases):
    de = 0 if k == 0 else round(LEAD + t0 - 0.05, 3)
    ate = Hd + 1 if k == len(frases) - 1 else round(LEAD + frases[k + 1][1] - 0.05, 3)
    png = T / f"cx{k}.png"
    caixa(txt, png, cp["cap_cy"], cp["cap_w"], cp["cap_h"])
    ovs.append((png, de, ate))

# ---------------- 4) áudio: música do corpo terminando no corte + fala ----------------
fonte = final_de(CC)
F = V / "fontes" / CC
# fim do corpo: corta o silêncio da cauda do AD (deixa no máx. 0,6 s)
DF = dur(fonte)
r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{DF - 8:.2f}", "-i", str(fonte), "-vn", "-af",
                    "silencedetect=noise=-45dB:d=0.6", "-f", "null", "-"], capture_output=True, text=True).stderr
ss = [float(l.split("silence_start:")[1]) for l in r.splitlines() if "silence_start" in l]
es = [float(l.split("silence_end:")[1].split("|")[0]) for l in r.splitlines() if "silence_end" in l]
fim_corpo = DF
if ss and (len(es) < len(ss) or es[-1] > 8 - 0.1):
    fim_corpo = DF - 8 + ss[-1] + 0.6
bed = F / "bed_no_vocals.wav"
if not bed.exists():
    pre = F / "pre.wav"
    run("ffmpeg", "-v", "error", "-y", "-t", f"{cp['corte']:.3f}", "-i", fonte, "-vn", "-ac", "2", "-ar", "44100", pre)
    env = dict(os.environ, OMP_NUM_THREADS="4", MKL_NUM_THREADS="4")
    run(sys.executable, "-m", "demucs", "--two-stems=vocals", "-n", "htdemucs", "-o", F / "sep", pre, env=env)
    (F / "sep" / "htdemucs" / "pre" / "no_vocals.wav").replace(bed)
bdur = dur(bed)
corpo_I = cp.get("lufs_corpo") or lufs(fonte, cp["corte"], 30)
fala_I = lufs(fala)
ganho = corpo_I - fala_I - 0.5
# fundo: os últimos Hd s da música antes do corte (emenda contínua); se o trecho for curto, repete o começo antes
if bdur >= Hd:
    fbg = f"[1:a]atrim={bdur - Hd:.3f}:{bdur:.3f},asetpts=PTS-STARTPTS[bg]"
else:
    extra = Hd - bdur + 0.3
    fbg = (f"[1:a]asplit[b1][b2];[b1]atrim=0:{extra:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={extra - 0.3:.3f}:d=0.3[e];"
           f"[b2]afade=t=in:d=0.3[m];[e][m]acrossfade=d=0.3[bgx];[bgx]atrim=0:{Hd:.3f}[bg]")
fc = [
    fbg,
    f"[2:a]aresample=44100,aformat=channel_layouts=stereo,volume={ganho:.2f}dB,adelay={int(LEAD * 1000)}|{int(LEAD * 1000)}[nv]",
    f"[bg][nv]amix=inputs=2:duration=first:normalize=0,aresample=48000,atrim=0:{Hd:.3f}[ga]",
]
vin = "[0:v]"
for k, (png, de, ate) in enumerate(ovs):
    fc.append(f"{vin}[{3 + k}:v]overlay=0:0:enable='between(t,{de},{ate})'[o{k}]")
    vin = f"[o{k}]"
# corpo: final do corte até o fim
n_in = 3 + len(ovs)
fc += [f"{vin}fps={FPS},format=yuv420p,setsar=1[gv]",
       f"[{n_in}:v]fps={FPS},scale={W}:{H},setsar=1,format=yuv420p[cv]",
       f"[{n_in}:a]aresample=48000,aformat=channel_layouts=stereo[ca]",
       "[gv][ga][cv][ca]concat=n=2:v=1:a=1[v][a]"]
nome = f"VAR {int(VAR):02d} - {GK}-{nome_g} x AD{CC}.mp4"
saida = PROD / "VARIACOES" / nome
vb = cp.get("vbitrate", 900)
args = ["ffmpeg", "-v", "error", "-y", "-i", T / "gancho_v.mp4", "-i", bed, "-i", fala]
for png, _, _ in ovs:
    args += ["-loop", "1", "-t", f"{Hd:.3f}", "-i", png]
args += ["-ss", f"{cp['corte']:.3f}", "-t", f"{fim_corpo - cp['corte']:.3f}", "-i", fonte, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "medium", "-b:v", f"{vb}k", "-maxrate", f"{int(vb * 1.6)}k", "-bufsize", f"{vb * 3}k",
         "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", saida]
env = dict(os.environ)
subprocess.run([str(x) for x in args], check=True)
info = {"var": VAR, "gancho": GK, "corpo": CC, "genero": gen, "texto": texto, "Hd": Hd, "fala_s": round(D, 2),
        "tomadas": segs, "corte": cp["corte"], "frases": frases, "saida": str(saida), "seed": SEED}
json.dump(info, open(T / "info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"ok VAR {VAR} {GK} x AD{CC} | gancho {Hd:.2f}s ({len(segs)} tomadas) | total {dur(saida):.1f}s | {saida.name}")
