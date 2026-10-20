# -*- coding: utf-8 -*-
"""Prints de WhatsApp em ES (ficticios) + tela de transferencia generica (sem marca real) -> chat_1..3.png (720x1280)
e o video mont/cena_chat.mp4 (n quadros, aproximacao lenta). Uso: python chat.py [n_quadros]"""
import sys, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = Path(__file__).resolve().parent; W, H = 720, 1280; WF = Path(r"C:\Windows\Fonts")
def F(n, t): return ImageFont.truetype(str(WF / n), t)
FT = F("segoeui.ttf", 27); FTB = F("seguisb.ttf", 29); FH = F("seguisb.ttf", 23); FEMO = F("seguiemj.ttf", 28)
BG = (239, 231, 222); IN = (255, 255, 255); OUT = (217, 253, 211); CINZA = (102, 119, 129)
REZA = "\U0001F64F"; CHORO = "\U0001F62D"; BRILHO = "\u2728"; MIC = "\U0001F3A4"
EMO = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")


def quebra(d, txt, maxw):
    linhas = []; cur = ""
    for w in txt.split(" "):
        c = (cur + " " + w).strip()
        if d.textlength(c, font=FT) > maxw and cur:
            linhas.append(cur); cur = w
        else:
            cur = c
    linhas.append(cur); return linhas


def escreve(d, x, y, linha, cor=(17, 27, 33)):
    for parte in re.split(f"({EMO.pattern})", linha):
        if not parte: continue
        if EMO.fullmatch(parte):
            d.text((x, y + 2), parte, font=FEMO, embedded_color=True); x += d.textlength(parte, font=FEMO)
        else:
            d.text((x, y), parte, font=FT, fill=cor); x += d.textlength(parte, font=FT)


def topo(im, nome, cor_av):
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 112], fill=(255, 255, 255)); d.line([(0, 112), (W, 112)], fill=(225, 225, 225), width=2)
    d.text((22, 58), "\u2190", font=FTB, fill=(40, 40, 40), anchor="lm")
    d.ellipse([58, 32, 110, 84], fill=cor_av); d.ellipse([74, 40, 94, 60], fill=(245, 245, 245))
    d.pieslice([66, 62, 102, 98], 180, 360, fill=(245, 245, 245))
    d.ellipse([56, 30, 112, 86], outline=(255, 255, 255), width=3)
    d.text((126, 46), nome, font=FTB, fill=(17, 27, 33), anchor="lm"); d.text((126, 78), "en l\u00ednea", font=FH, fill=CINZA, anchor="lm")
    d.text((690, 58), "\u22EE", font=F("seguisym.ttf", 34), fill=(60, 60, 60), anchor="mm")


def rodape(im):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([12, 1196, 620, 1262], radius=33, fill=(255, 255, 255))
    d.text((40, 1229), "Mensaje", font=FT, fill=(140, 150, 155), anchor="lm")
    d.ellipse([632, 1196, 698, 1262], fill=(0, 168, 132)); d.text((665, 1229), MIC, font=FEMO, embedded_color=True, anchor="mm")


def bolha(im, y, txt, saida, hora, img=None):
    d = ImageDraw.Draw(im); maxw = 470
    linhas = quebra(d, txt, maxw) if txt else []
    lw = max([d.textlength(l, font=FT) for l in linhas] + [0]); lh = 37
    iw, ih = (img.size if img else (0, 0))
    bw = max(lw + 110, iw + 16); bh = len(linhas) * lh + 34 + (ih + 10 if img else 0)
    x0 = W - 18 - bw if saida else 18; cor = OUT if saida else IN
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([x0, y + 2, x0 + bw, y + bh + 2], 14, fill=(0, 0, 0, 40))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(1.5)))
    d = ImageDraw.Draw(im); d.rounded_rectangle([x0, y, x0 + bw, y + bh], 14, fill=cor)
    yy = y + 10
    if img:
        im.paste(img, (int(x0 + 8), int(yy - 2))); yy += ih + 10
    for l in linhas:
        escreve(d, x0 + 16, yy, l); yy += lh
    d.text((x0 + bw - (40 if saida else 14), y + bh - 8), hora, font=F("segoeui.ttf", 18), fill=CINZA, anchor="rb")
    if saida: d.text((x0 + bw - 12, y + bh - 8), "\u2713\u2713", font=F("seguisym.ttf", 16), fill=(83, 189, 235), anchor="rb")
    return y + bh + 14


def data(im, y, t):
    d = ImageDraw.Draw(im); w = d.textlength(t, font=FH) + 30
    d.rounded_rectangle([(W - w) / 2, y, (W + w) / 2, y + 38], 10, fill=(255, 255, 255))
    d.text((W / 2, y + 19), t, font=FH, fill=CINZA, anchor="mm")
    return y + 56


def banco():
    """tela generica de app bancario (sem marca real): transferencia recibida US$ 13.000,00"""
    w, h = 400, 520; im = Image.new("RGB", (w, h), (246, 247, 251)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, 150], fill=(32, 64, 140))
    d.text((24, 36), "Mi cuenta", font=F("seguisb.ttf", 26), fill="white")
    d.text((24, 80), "Saldo disponible", font=F("segoeui.ttf", 19), fill=(200, 210, 235))
    d.text((24, 104), "US$ 13.240,57", font=F("seguisb.ttf", 24), fill="white")
    d.rounded_rectangle([16, 170, w - 16, 470], 16, fill="white")
    d.ellipse([w / 2 - 34, 190, w / 2 + 34, 258], fill=(222, 245, 230))
    d.text((w / 2, 224), "\u2713", font=F("seguisym.ttf", 40), fill=(20, 150, 70), anchor="mm")
    d.text((w / 2, 290), "Transferencia recibida", font=F("seguisb.ttf", 24), fill=(30, 30, 40), anchor="mm")
    d.text((w / 2, 345), "US$ 13.000,00", font=F("seguisb.ttf", 42), fill=(20, 130, 60), anchor="mm")
    f = F("segoeui.ttf", 18)
    d.text((40, 392), "Tipo", font=f, fill=(120, 120, 130)); d.text((w - 40, 392), "Transferencia", font=f, fill=(40, 40, 50), anchor="ra")
    d.text((40, 424), "Estado", font=f, fill=(120, 120, 130)); d.text((w - 40, 424), "Acreditada", font=f, fill=(20, 140, 60), anchor="ra")
    d.text((w / 2, 495), "Ver comprobante", font=f, fill=(32, 64, 140), anchor="mm")
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w, h], 12, fill=255)
    out = Image.new("RGB", (w, h), IN); out.paste(im, (0, 0), m); return out


def tela(nome, cor, msgs, data_txt="Hoy"):
    im = Image.new("RGBA", (W, H), BG + (255,)); topo(im, nome, cor); y = data(im, 140, data_txt)
    for m in msgs: y = bolha(im, y, *m)
    rodape(im); return im.convert("RGB"), y


T1 = [(f"Padre, lo vi hablando de esa oraci\u00f3n de San Benito\u2026 \u00a1qu\u00e9 cosa tan poderosa! Se me eriz\u00f3 la piel {REZA}", False, "10:33"),
      (f"\u00a1Qu\u00e9 bueno, Geralda! Es la oraci\u00f3n de las 12 palabras de San Benito. Muy poderosa {REZA}", True, "10:35"),
      ("Padre, mi hijo llevaba 11 meses sin trabajo\u2026 al tercer d\u00eda de hacer la oraci\u00f3n lo llamaron para una entrevista", False, "10:46"),
      (f"\u00a1Y ya firm\u00f3 contrato! {CHORO}{BRILHO}", False, "10:46"),
      (f"\u00a1Gloria a Dios! San Benito es muy poderoso {REZA}", True, "10:49")]
T2 = [("Padre, usted no lo va a creer. Hice la oraci\u00f3n de las 12 palabras durante 7 d\u00edas\u2026", False, "19:41"),
      (f"y me lleg\u00f3 esta transferencia {CHORO}{REZA}", False, "19:42"),
      ("", False, "19:42", "BANCO"),
      (f"\u00a1Gloria a Dios, Rosa! Vuelve a contarme las bendiciones {REZA}", True, "19:45")]
T3 = [("Hola, padre Andr\u00e9s", False, "15:38"),
      ("Vine a agradecer porque esta oraci\u00f3n cambi\u00f3 mi semana. Estaba desesperada con unas cuentas atrasadas. Hice la oraci\u00f3n con fe y ese mismo d\u00eda una clienta antigua me llam\u00f3 para un trabajo grande!!!", False, "15:38"),
      (f"Lleg\u00f3 justo el dinero que necesitaba. Parec\u00eda imposible, pero funcion\u00f3. Muchas gracias por ense\u00f1arnos {REZA}", False, "15:38"),
      (f"Qu\u00e9 bueno, querida. San Benito es muy poderoso {REZA}", True, "15:39")]

if __name__ == "__main__":
    b = banco()
    t2 = [(m[0], m[1], m[2], b) if len(m) == 4 else m for m in T2]
    telas = [tela("Geralda", (180, 150, 200), T1), tela("Rosa Mar\u00eda", (150, 190, 170), t2), tela("Carmen", (200, 170, 140), T3)]
    for i, (im, y) in enumerate(telas):
        im.save(AQ / f"chat_{i + 1}.png"); print(i + 1, "altura usada", y)
    if len(sys.argv) > 2:
        n = int(sys.argv[1]); ordem = [int(x) for x in sys.argv[2]]; out = AQ.parent / "mont" / f"cena_chat{sys.argv[2]}.mp4"
        m = len(ordem); tam = [n // m] * (m - 1) + [n - (m - 1) * (n // m)]
        ins, fc = [], []
        for i, (k, c) in enumerate(zip(tam, ordem)):
            ins += ["-loop", "1", "-framerate", "30", "-t", f"{k / 30 + 0.3:.3f}", "-i", str(AQ / f"chat_{c}.png")]
            fc.append(f"[{i}:v]scale=1440:2560,zoompan=z='1+0.035*on/{k}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30,"
                      f"trim=end_frame={k},setpts=PTS-STARTPTS[c{i}]")
        fc.append("".join(f"[c{i}]" for i in range(m)) + f"concat=n={m}:v=1:a=0,format=yuv420p[v]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-frames:v", str(n), "-r", "30",
                        "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
                        "-color_trc", "bt709", "-color_range", "tv", str(out)], check=True)
        print("ok", out)
