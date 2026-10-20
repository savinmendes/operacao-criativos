# -*- coding: utf-8 -*-
"""Fim Lymphoria: takes do frasco (já produzidos) até a palavra 'compre' + card de oferta (zoom lento) até o fim.
python build_fim.py narr.mp3 saida.mp4"""
import subprocess, sys, json
from pathlib import Path
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas"))
import legenda as LEG
AQUI = Path(__file__).parent
TAKES = [r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\_trabalho\ugc\prod\V1_gotero_hierbas.mp4",
         r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\_trabalho\ugc\prod\V3_frasco_mesa.mp4",
         r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\_trabalho\ugc\prod\V2_frasco_cocina.mp4"]
RENDER = r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho\ad04\render_parte2.py"
narr, saida = sys.argv[1], sys.argv[2]
wk = Path(saida).parent / "_fim_wk"; wk.mkdir(exist_ok=True)
ali = str(Path(narr).with_suffix("")) + ".alinhamento.json"
pal = LEG.palavras_por_alinhamento(ali, 0)
tc = next(a for w, a, *_ in pal if LEG._limpa(w).startswith("compre"))
tc = round(tc * 30) / 30
dn = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",narr],capture_output=True,text=True).stdout)
D = dn + 0.6
# takes até tc
ins, fc, rest, k = [], [], tc, 0
for t in TAKES:
    if rest <= 0.01: break
    dt = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",t],capture_output=True,text=True).stdout)
    use = min(dt, rest); rest -= use
    ins += ["-i", t]
    fc.append(f"[{k}:v]trim=0:{use:.3f},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,format=yuv420p[v{k}]"); k += 1
if rest > 0.01:  # takes acabaram: congela o último
    fc[-1] = fc[-1].replace("[v%d]" % (k-1), ",tpad=stop_mode=clone:stop_duration=%.3f[v%d]" % (rest, k-1))
fc.append("".join(f"[v{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0[o]")
subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",";".join(fc),"-map","[o]","-c:v","libx264","-crf","16","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",str(wk/"a.mp4")],check=True)
# card do tc ao fim
subprocess.run(["ffmpeg","-v","error","-y","-i",narr,"-ss",f"{tc:.3f}",str(wk/"resto.wav")],check=True)
subprocess.run([sys.executable,RENDER,str(wk/"resto.wav"),str(wk/"b.mp4"),f"{AQUI/'oferta_card.jpg'}:0"],check=True)
lst = wk/"l.txt"; lst.write_text(f"file '{(wk/'a.mp4').as_posix()}'\nfile '{(wk/'b.mp4').as_posix()}'\n")
subprocess.run(["ffmpeg","-v","error","-y","-i",str(wk/"a.mp4"),"-i",str(wk/"b.mp4"),"-i",narr,"-filter_complex",
  "[0:v]setsar=1,format=yuv420p[x];[1:v]setsar=1,format=yuv420p[y];[x][y]concat=n=2:v=1:a=0[v];[2:a]aresample=48000,apad=pad_dur=0.6[a]",
  "-map","[v]","-map","[a]","-t",f"{D:.3f}","-c:v","libx264","-crf","16","-pix_fmt","yuv420p","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",
  "-c:a","aac","-b:a","192k","-ar","48000","-ac","2",saida],check=True)
json.dump({"t_compre": tc, "dur": D}, open(str(Path(saida).with_suffix(".json")),"w"))
print("ok", saida, tc, D)
