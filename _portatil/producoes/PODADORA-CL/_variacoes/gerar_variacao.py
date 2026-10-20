# -*- coding: utf-8 -*-
"""Gera uma variação gancho × corpo da podadora a partir do banco de tomadas dos 4 originais.
  python gerar_variacao.py <NN> <H1|H2|H3|H4> <A|B|C> [semente]
Saída: _variacoes/trab/<NN>/corpo.mp4 + alinhamento.json + receita_final.json (depois rodar montar_ad.py)."""
import json
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
V = BASE / "_variacoes"
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
FB, FM = str(KIT / "fonts" / "Poppins-Bold.ttf"), str(KIT / "fonts" / "Poppins-Medium.ttf")
EMOJI = r"C:\Windows\Fonts\seguiemj.ttf"
W, H = 720, 1280
NN, HK, CP = sys.argv[1], sys.argv[2], sys.argv[3]
random.seed(int(sys.argv[4]) if len(sys.argv) > 4 else int(NN))
T = V / "trab" / NN
T.mkdir(parents=True, exist_ok=True)
AVISO = ["Solo con fines demostrativos. Algunas escenas están aceleradas.",
         "El rendimiento real puede variar según el tipo y grosor del pasto,",
         "el nivel de batería y las condiciones de uso."]
GANCHOS = {
    "H1": dict(src=1, ini=4 / 30, fim=3.4, fala="gancho_H1", caixa=dict(linhas=["Me dijeron que necesitaba un jardinero.", "Encontré esto 😏🌾"], px=29, cy=235, de=0, ate=3.0)),
    "H2": dict(src=2, ini=0.0, fim=10.0, fala=None, caixa=dict(linhas=["Un hueso…", "y mi perro se cambió de equipo 💀"], px=33, cy=778, cobrir_w=524, cobrir_h=118, de=0, ate=2.75)),
    "H3": dict(src=3, ini=0.0, fim=3.3, fala="gancho_H3", caixa=dict(linhas=["Quien inventó esto", "merece un aumento 🙌"], px=31, cy=235, de=0, ate=3.0)),
    "H4": dict(src=4, ini=0.0, fim=7.5, fala=None, caixa=dict(linhas=["Bueno… creo que ya no la puedo devolver 😅"], px=25, negrito=False, cy=470, cobrir_w=484, cobrir_h=52, de=0, ate=6.1)),
}
CORPOS = {"A": ("corpo_A_vA", "vA", (1, 3.4)), "B": ("corpo_B_vB", "vB", (3, 3.3)), "C": ("corpo_C_vA", "vA", (2, 12.2))}
MESA, APRESENTA, EXCLUI = [31, 41], [8, 33, 43], {8, 13, 23, 31, 33, 41, 43}


def run(*a):
    subprocess.run([str(x) for x in a], check=True)


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True).stdout)


def e_emoji(ch):
    return ord(ch) > 0x2000 and ch not in "…–—“”‘’¡¿"


def caixa_gancho(spec, destino):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FB if spec.get("negrito", True) else FM, spec["px"])
    fe = ImageFont.truetype(EMOJI, spec["px"])
    larg = lambda s: sum(d.textlength(c, font=fe if e_emoji(c) else f) for c in s)
    lh = int(spec["px"] * 1.3)
    ws = [larg(l) for l in spec["linhas"]]
    bw = max(max(ws) + 44, spec.get("cobrir_w", 0))
    bh = max(lh * len(ws) + 26, spec.get("cobrir_h", 0))
    x0, y0 = W / 2 - bw / 2, spec["cy"] - bh / 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=16, fill=(255, 255, 255, 255))
    ty = spec["cy"] - lh * len(ws) / 2 + 4
    for l, w in zip(spec["linhas"], ws):
        x = W / 2 - w / 2
        for c in l:
            if e_emoji(c):
                d.text((x, ty + int(spec["px"] * 0.05)), c, font=fe, embedded_color=True)
                x += d.textlength(c, font=fe)
            else:
                d.text((x, ty), c, font=f, fill=(0, 0, 0, 255))
                x += d.textlength(c, font=f)
        ty += lh
    img.save(destino)


def faixa_aviso(destino, topo=1150):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for y in range(topo - 40, H):
        d.line([(0, y), (W, y)], fill=(0, 0, 0, 252 if y >= topo else int(252 * (y - topo + 40) / 40)))
    f = ImageFont.truetype(FM, 19)
    y = topo + (H - topo - 25 * len(AVISO)) / 2
    for l in AVISO:
        d.text(((W - d.textlength(l, font=f)) / 2, y), l, font=f, fill=(235, 235, 235, 255))
        y += 25
    img.save(destino)


# ---------- narração (frase do gancho + corpo) e alinhamento ----------
g = GANCHOS[HK]
corpo_nome, voz, bed = CORPOS[CP]
VZ = V / "voz"
partes, al = [], {"characters": [], "character_start_times_seconds": [], "character_end_times_seconds": []}
cursor = 0.0
if g["fala"]:
    fala = VZ / f"{g['fala']}_{voz}.mp3"
    partes.append(fala)
    a = json.load(open(str(fala).replace(".mp3", ".alinhamento.json"), encoding="utf-8"))
    a = a.get("alignment") or a
    for k in al:
        al[k] += a[k]
    cursor = dur(fala) + 0.3
    al["characters"].append(" "); al["character_start_times_seconds"].append(cursor - 0.3); al["character_end_times_seconds"].append(cursor - 0.3)
fc_corpo = VZ / f"{corpo_nome}.mp3"
a = json.load(open(str(fc_corpo).replace(".mp3", ".alinhamento.json"), encoding="utf-8"))
a = a.get("alignment") or a
al["characters"] += a["characters"]
al["character_start_times_seconds"] += [t + cursor for t in a["character_start_times_seconds"]]
al["character_end_times_seconds"] += [t + cursor for t in a["character_end_times_seconds"]]
narr = T / "narr.wav"
if g["fala"]:
    run("ffmpeg", "-v", "error", "-y", "-i", partes[0], "-i", fc_corpo, "-filter_complex",
        "[0:a]aresample=48000,aformat=channel_layouts=mono,apad=pad_dur=0.3[x];[1:a]aresample=48000,aformat=channel_layouts=mono[y];[x][y]concat=n=2:v=0:a=1",
        narr)
    t_narr = 0.15
else:
    run("ffmpeg", "-v", "error", "-y", "-i", fc_corpo, "-ar", "48000", "-ac", "1", narr)
    t_narr = g["fim"] - g["ini"]
for k in ("character_start_times_seconds", "character_end_times_seconds"):
    al[k] = [round(t + t_narr, 3) for t in al[k]]
json.dump(al, open(T / "alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
d_narr = dur(narr)

# ---------- montagem das tomadas ----------
gancho_len = max(g["fim"] - g["ini"], (d_narr if False else 0))
if g["fala"]:
    falalen = dur(VZ / f"{g['fala']}_{voz}.mp3") + 0.35
    gancho_len = max(g["fim"] - g["ini"], falalen)
total = t_narr + d_narr + 0.8
alvo = total - gancho_len
banco = json.load(open(V / "banco.json"))
for t in banco:  # margem de segurança nas bordas (o corte detectado não é exato)
    t["ini"] = round(t["ini"] + 0.15, 3); t["fim"] = round(t["fim"] - 0.2, 3); t["dur"] = round(t["fim"] - t["ini"], 3)
GRUPOS = [{10, 11}, {18, 19, 20}, {21, 22}]  # pedaços da mesma cena contínua: usar só um por vídeo
def marcar(i):
    usados.add(i)
    for gr in GRUPOS:
        if i in gr:
            usados.update(gr)
usados = set()
segs = [(g["src"], g["ini"], g["ini"] + gancho_len)]
ult_src = g["src"]
if CP == "C":
    m = [i for i in MESA if banco[i]["src"] != ult_src] or MESA
    i = random.choice(m)
    t = banco[i]; L = min(t["dur"], 4.5); a0 = t["ini"] + (t["dur"] - L) / 2
    segs.append((t["src"], a0, a0 + L)); ult_src = t["src"]; alvo -= L
meio = [i for i in range(len(banco)) if i not in EXCLUI]
random.shuffle(meio)
fim_ap = [i for i in APRESENTA]
random.shuffle(fim_ap)
reserva_fim = 3.5
while alvo > reserva_fim + 0.5 and meio:
    cand = [i for i in meio if banco[i]["src"] != ult_src and i not in usados]
    if not cand:
        cand = [i for i in meio if i not in usados]
        if not cand:
            break
    i = cand[0]; marcar(i); meio.remove(i)
    t = banco[i]
    L = min(t["dur"], random.uniform(3.0, 4.3), alvo - reserva_fim)
    if L < 1.3:
        if alvo - reserva_fim < 1.3:
            break
        continue  # tomada curta demais: pula para a próxima
    a0 = t["ini"] + (t["dur"] - L) / 2
    segs.append((t["src"], a0, a0 + L)); ult_src = t["src"]; alvo -= L
ap = next((i for i in fim_ap if banco[i]["src"] != ult_src), fim_ap[0])
t = banco[ap]; L = max(1.5, min(t["dur"], alvo)); a0 = t["ini"] + max(0, t["dur"] - L)
segs.append((t["src"], a0, a0 + min(L, t["dur"])))
json.dump(segs, open(T / "segmentos.json", "w"), indent=0)

# vídeo: cortes + concat
lista = []
for k, (s, a0, a1) in enumerate(segs):
    o = T / f"s{k:02d}.mp4"
    run("ffmpeg", "-v", "error", "-y", "-ss", f"{a0:.3f}", "-t", f"{a1 - a0:.3f}", "-i", BASE / f"original_0{s}.mp4",
        "-an", "-vf", "fps=30,scale=720:1280,setsar=1", "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", o)
    lista.append(f"file '{o.as_posix()}'")
(T / "lista.txt").write_text("\n".join(lista))
run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", T / "lista.txt", "-c", "copy", T / "video.mp4")
dv = dur(T / "video.mp4")

# áudio: fundo do gancho (mesmo trecho) + cama contínua do corpo + narração
SEP = BASE / "_audio" / "sep" / "htdemucs"
faixa_aviso(T / "faixa.png")
caixa_gancho(g["caixa"], T / "caixa.png")
bsrc, bini = bed
fc = [
    f"[1:a]atrim={g['ini']}:{g['ini'] + gancho_len},asetpts=PTS-STARTPTS,volume=2.0,aresample=48000[ga]",
    f"[2:a]atrim=start={bini},asetpts=PTS-STARTPTS,aloop=loop=3:size=2e9,atrim=0:{dv - gancho_len + 0.5},volume=1.6,"
    f"afade=t=in:d=0.4,aresample=48000[cb]",
    "[ga][cb]concat=n=2:v=0:a=1[bg]",
    f"[3:a]adelay={int(t_narr * 1000)}|{int(t_narr * 1000)}[nv]",
    "[bg][nv]amix=inputs=2:duration=first:normalize=0[a]",
    "[0:v][4:v]overlay=0:0[v1]",
    f"[v1][5:v]overlay=0:0:enable='between(t,{g['caixa']['de']},{g['caixa']['ate']})'[v]",
]
run("ffmpeg", "-v", "error", "-y", "-i", T / "video.mp4", "-i", SEP / f"orig_0{g['src']}" / "no_vocals.wav",
    "-i", SEP / f"orig_0{bsrc}" / "no_vocals.wav", "-i", narr, "-i", T / "faixa.png", "-i", T / "caixa.png",
    "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", f"{dv:.3f}", T / "corpo.mp4")

# receita final do kit
sys.path.insert(0, str(KIT / "ferramentas"))
import legenda as LEG  # noqa: E402
pal = LEG.palavras_por_alinhamento(str(T / "alinhamento.json"), 0)
t_desp = next(a for w, a, b in pal if LEG._limpa(w).startswith("despacho"))
NOMES_H = {"H1": "JARDINERO", "H2": "PERRO", "H3": "AUMENTO", "H4": "DEVOLVER"}
NOMES_C = {"A": "FUNCIONES", "B": "CUCHILLA", "C": "KIT"}
saida = BASE / f"AD {NN} - PODADORA-INALAMBRICA-{NOMES_H[HK]}-{NOMES_C[CP]}-ES-CL.mp4"
rec = {"saida": str(saida), "estilo": "drop", "corpo": str(T / "corpo.mp4"),
       "legenda": {"fonte": "alinhamento:" + str(T / "alinhamento.json"),
                   "chaves": ["podadora", "ruedas", "baterías", "batería", "metal", "gratis", "recibir", "noventa",
                              "garantía", "toca", "inalámbrica", "caja", "cuchilla"]},
       "selo": {"linhas": ["DESPACHO GRATIS A DOMICILIO", "PAGO CONTRA", "ENTREGA", "¡PAGAS AL RECIBIR!"], "x": 160, "y": 1110,
                "desde": round(t_desp, 2)},
       "cta": {"palavra": "toca", "y": 1490}, "limite_mb": 30, "resolucao": "720"}
json.dump(rec, open(T / "receita_final.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"ok {NN} {HK}x{CP} | {len(segs)} tomadas | vídeo {dv:.1f}s | narração {t_narr:.1f}–{t_narr + d_narr:.1f}s")
