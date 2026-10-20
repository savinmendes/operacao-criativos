# Entradas do HeyGen PL (video com o audio ORIGINAL ES; audio PL separado).
# s1: cena 1 do ES (5,1 s) desacelerada para 5,6 s (0,905x). s2: igual ao EN/IT (4,933 s).
# s7 (CTA, 6,5 s): o original sorri com dentes em 1,05-1,5 / 2,4-2,8 / 3,6-4,4 s (no IT o HeyGen manteve o sorriso
# em ~29,7 s). Montado so com os trechos neutros, com jump cut nas fronteiras de palavra do PL
# (pausa depois de "zywo." e entre "cud," e "zanim") e vai-e-volta curto dentro de cada trecho neutro.
import subprocess, json
SRC7="heygen_in/s7_src.mp4"
# (ini_src, fim_src, dur_saida); fim<ini = trecho invertido
SEG7=[(0.00,1.00,1.20),(1.00,0.70,0.375), # ate 1,575 (entre "wiecej»" e "ponizej") -> jump cut (pula a risada 1,05-1,5)
      (1.55,2.30,0.95),(2.30,1.60,0.85),(1.60,1.85,0.325),  # ate 3,70 (pausa depois de "zywo.") -> jump cut
      (2.90,3.50,0.70),(3.50,3.00,0.59),   # ate 4,99 (entre "cud," e "zanim") -> jump cut
      (4.50,5.40,1.05),(5.40,4.95,0.46)]   # ate 6,50
ENC=["-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","48000"]
def run(a): subprocess.run(["ffmpeg","-v","error","-y"]+a,check=True)
# s1
f=5.6/5.067
run(["-i","heygen_in/s1_src.mp4","-filter_complex",f"[0:v]setpts=PTS*{f:.6f},fps=30[v];[0:a]atempo={1/f:.6f}[a]",
     "-map","[v]","-map","[a]","-t","5.6"]+ENC+["heygen_in/s1_in.mp4"])
run(["-i","heygen_in/s2_src.mp4","-c","copy","heygen_in/s2_in.mp4"])
# s7
fc=[];cat=""
for i,(a,b,d) in enumerate(SEG7):
    lo,hi=min(a,b),max(a,b); sp=(hi-lo)/d; rv=b<a
    fc.append(f"[0:v]trim={lo}:{hi},setpts=PTS-STARTPTS{',reverse' if rv else ''},setpts=PTS/{sp:.6f},fps=30,trim=0:{d},setpts=PTS-STARTPTS[v{i}]")
    fc.append(f"[0:a]atrim={lo}:{hi},asetpts=PTS-STARTPTS{',areverse' if rv else ''},atempo={max(sp,0.5):.6f},apad,atrim=0:{d},asetpts=PTS-STARTPTS[a{i}]")
    cat+=f"[v{i}][a{i}]"
fc.append(cat+f"concat=n={len(SEG7)}:v=1:a=1[v][a]")
run(["-i",SRC7,"-filter_complex",";".join(fc),"-map","[v]","-map","[a]","-t","6.5"]+ENC+["heygen_in/s7_in.mp4"])
# audio PL por trecho
for k,a,b in [("s1",0,5.6),("s2",5.6,10.533),("s7",26.633,33.133)]:
    run(["-i","audio/voz_pl.wav","-ss",str(a),"-t",f"{b-a:.3f}","-c:a","libmp3lame","-b:a","192k",f"heygen_in/{k}_pl.mp3"])
for k in ["s1","s2","s7"]:
    for p in [f"heygen_in/{k}_in.mp4",f"heygen_in/{k}_pl.mp3"]:
        print(p,subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip())
