"""Mixa trilha sob o AD pronto (video -c:v copy). Uso: python mixar.py A [base_db]"""
import json,re,subprocess,sys
V=r"C:\Users\PICHAU\Downloads\YARA-CL\entregas\AD-C_yara-kit3_bf_es-cl.mp4"
n=sys.argv[1]; base=float(sys.argv[2]) if len(sys.argv)>2 else -4.0
OUT=rf"C:\Users\PICHAU\Downloads\YARA-CL\entregas\AD-C_yara-kit3_bf_es-cl_musica-{n}.mp4"
dur=float(subprocess.check_output(["ffprobe","-v","error","-select_streams","a","-show_entries","stream=duration","-of","csv=p=0",V]).decode())
TIT,CTA=1.5,1.8
LEITO=f"_leito_{n}.wav"
_e=subprocess.run(["ffmpeg","-hide_banner","-nostats","-i",LEITO,"-af","ebur128","-f","null","-"],capture_output=True,text=True).stderr
I_leito=float(re.findall(r"I:\s+(-?[\d.]+) LUFS",_e)[-1]); g0=-16-I_leito; cta0=dur-CTA; fo=dur-0.8
mus=(f"[1:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
     f"volume={g0+base:.2f}dB,"
     f"volume='if(lt(t,{TIT}),1.6,if(gt(t,{cta0:.3f}),1.5,1))':eval=frame[m0];"
     f"[0:a]asplit=2[v][sc];"
     f"[m0][sc]sidechaincompress=threshold=0.05:ratio=3:attack=20:release=400:makeup=1[md];"
     f"[md]afade=t=out:st={fo:.3f}:d=0.8,asplit=2[m][mstem];"
     f"[v][m]amix=inputs=2:duration=first:normalize=0[mx]")
def run(extra, af_final, out, maps, sink=""):
    cmd=["ffmpeg","-hide_banner","-y","-i",V,"-i",LEITO,"-filter_complex",mus+";[mx]"+af_final+"[a]"+sink]+maps+extra+[out]
    return subprocess.run(cmd,capture_output=True,text=True,encoding="utf-8",errors="replace")
# passo 1: medir
r=run(["-f","null"],"loudnorm=I=-14.5:TP=-1.5:LRA=11:print_format=json","NUL",["-map","[a]","-map","[mstem]"])
js=json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}",r.stderr)[-1])
ln=(f"loudnorm=I=-14.5:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
    f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true,"
    f"aresample=48000,alimiter=limit=0.89:level=false")
# passo 2: gravar video + stem da musica (p/ medir)
r=run(["-c:v","copy","-c:a","aac","-b:a","160k","-ar","48000","-movflags","+faststart"],ln,OUT,["-map","0:v","-map","[a]"],";[mstem]anullsink")
if r.returncode: print(r.stderr[-2000:]); sys.exit(1)
cmd=["ffmpeg","-hide_banner","-y","-i",V,"-i",LEITO,"-filter_complex",mus+";[mx]anullsink","-map","[mstem]",f"_stem_{n}.wav"]
subprocess.run(cmd,capture_output=True)
print("ok",OUT,"base",base)
