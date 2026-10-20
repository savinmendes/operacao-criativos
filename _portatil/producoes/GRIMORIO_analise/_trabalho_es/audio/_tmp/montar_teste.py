# -*- coding: utf-8 -*-
"""Montagem final ES: base sem legenda (visual) + bocas do lip sync + textos de tela ES + produto (cena alongada S s)
+ desfoques/overlays do visual + selo + legenda ES palavra a palavra + mix ES. Cor: bt709 fixo na ida e na volta."""
import json, subprocess, sys, numpy as np
from pathlib import Path
from PIL import Image
AQ = Path(__file__).resolve().parent.parent; VIS = AQ.parent / "visual"
sys.path.insert(0, str(AQ)); import cor, legenda_es
SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"C:\Users\PICHAU\Downloads\GRIMORIO V2 - ES COLAR (VIDEO FICTICIO).mp4")
BASE = AQ / "_tmp/bve_teste.mp4"
PL = json.load(open(AQ / "plano_audio.json", encoding="utf-8"))
FA = 3779; NS = 120; FP_FIM = 3921            # cena do print: 3779..3920 (142 q) -> 262 q
NPROD = (FP_FIM - FA) + NS
SOLTO = {2622: 2621}              # quadros soltos da transição -> último quadro do b-roll
segs = json.load(open(AQ / "lipsync/segs.json"))["segs"]
EXCLUIR = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else {"L05a", "L05b"}
USAR = [s for s in segs if (AQ / "lipsync/patch" / f"{s['nome']}.pkl").exists() and s["nome"] not in EXCLUIR]
OV = json.load(open(AQ / "overlays_final.json", encoding="utf-8"))   # gerado a partir do visual\textos_tela.json
def src_de(j):
    if j < FA: return j
    if j < FA + NPROD: return FA + int((j - FA) * (FP_FIM - FA) / NPROD)
    return j - NS
def t_final(j): return j / 30
N_SRC = int(subprocess.check_output(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v", "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(BASE)]))
NOUT = N_SRC + NS
# leitor sequencial da base (quadros em ordem)
w, h, fps, full = cor.info(BASE)
pb = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(BASE), "-vf", cor.vf_ler(full), "-fps_mode", "passthrough", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
FR = 720 * 1280 * 3
import pickle
patches = {}
for s in USAR: patches.update(pickle.load(open(AQ / "lipsync/patch" / f"{s['nome']}.pkl", "rb")))
print("trechos com boca nova:", [s["nome"] for s in USAR])
print("quadros com boca nova:", len(patches))
leg = legenda_es.Legenda(AQ / "palavras_es.json")
def carrega_png(p):
    im = Image.open(p).convert("RGBA"); return im
cache_png = {}
def ov_png(p):
    if p not in cache_png: cache_png[p] = carrega_png(p)
    return cache_png[p]
selo = ov_png(OV["selo"]["png"])
enc = cor.escritor(AQ / "_tmp/video_es.mp4", crf=16)
cur_i, cur_f = -1, None
def base_frame(i):
    global cur_i, cur_f
    while cur_i < i:
        b = pb.stdout.read(FR)
        if len(b) < FR: break
        cur_i += 1; cur_f = np.frombuffer(b, np.uint8).reshape(1280, 720, 3)
    return cur_f
for j in range(NOUT):
    i = src_de(j); t = t_final(j)
    f = base_frame(i)
    if i == 2621: hold = f.copy()
    if i in SOLTO: f = hold
    elif i in patches:
        x, y, L = patches[i]; hh, ww = L.shape[:2]; al = L[..., 3:4].astype(np.float32) / 255
        f = f.copy(); f[y:y + hh, x:x + ww] = np.clip(L[..., :3] * al + f[y:y + hh, x:x + ww] * (1 - al) + 0.5, 0, 255).astype(np.uint8)
    im = Image.fromarray(f).convert("RGBA")
    for o in OV["itens"]:
        if o["ini"] <= t < o["fim"]:
            p = ov_png(o["png"]); x, y = o.get("x", 0), o.get("y", 0)
            if o.get("zoom"):
                z = 1 + o["zoom"] * (t - o["ini"]) / (o["fim"] - o["ini"])
                pw, ph = int(p.width * z), int(p.height * z); x -= (pw - p.width) // 2; y -= (ph - p.height) // 2; p = p.resize((pw, ph), Image.BILINEAR)
            if o.get("osc"): y += int(o["osc"] * np.sin(2 * np.pi * 1.6 * (t - o["ini"])))
            im.alpha_composite(p, (int(x), int(y))) if x >= 0 and y >= 0 else im.paste(p, (int(x), int(y)), p)
    lg = leg.em(t)
    if lg is not None: im.alpha_composite(lg)
    im.alpha_composite(selo, (OV["selo"]["x"], OV["selo"]["y"]))
    enc.stdin.write(np.asarray(im.convert("RGB")).tobytes())
    if j % 600 == 0: print(f"[{j}/{NOUT}] {100*j/NOUT:.0f}%", flush=True)
enc.stdin.close(); enc.wait(); pb.kill()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(AQ / "_tmp/video_es.mp4"), "-i", str(AQ / "mix_es.wav"), "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-shortest", "-movflags", "+faststart", str(SAIDA)], check=True)
print("ok", SAIDA, NOUT / 30, "s")
