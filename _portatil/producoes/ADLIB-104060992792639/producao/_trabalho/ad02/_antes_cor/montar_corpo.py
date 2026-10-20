"""base_lipsync.mp4 do 02 = gancho com lipsync (_tmp/gancho_ls.mp4, quadros 0-285) + base_lipsync.mp4 do AD 01 a partir do quadro 242
(mesmas imagens deslocadas 44 quadros; lipsync do AD 01 refeito em speed, ver LICOES-LIPSYNC.md). Emenda em 286 = corte real.
Depois corpo_ad02.mp4 = base + narracao_es.wav + fundo (demucs no_vocals do 02), cortado 0,7 s depois da ultima fala, fade 0,3 s."""
import json, subprocess, cv2, shutil
from pathlib import Path
AD=Path(__file__).resolve().parent
COR=["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
# lote A (08/10): copia da base_lipsync FINAL do AD 01 (s03/s10/s13 com fechar.py e s08 em speed). A de 22:03 era anterior a isso.
src01=AD/"_tmp/ad01_base_lipsync_snap_loteA.mp4"
if not src01.exists(): shutil.copy2(AD.parent/"ad01/base_lipsync.mp4", src01)
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-","-threads","4",
    "-c:v","libx264","-crf","13","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(AD/"base_lipsync.mp4")],stdin=subprocess.PIPE)
g=cv2.VideoCapture(str(AD/"_tmp/gancho_ls.mp4")); n=0
while True:
    ok,f=g.read()
    if not ok: break
    ff.stdin.write(f.tobytes()); n+=1
assert n==286, n
b=cv2.VideoCapture(str(src01)); b.set(cv2.CAP_PROP_POS_FRAMES,242)
while True:
    ok,f=b.read()
    if not ok: break
    ff.stdin.write(f.tobytes()); n+=1
ff.stdin.close(); ff.wait(); print("base quadros",n)
t=json.load(open(AD/"_audio/tempos_reais.json",encoding="utf-8")); fim=round(t[-1]["fim"]+0.7,3)
subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/"base_lipsync.mp4"),"-i",str(AD/"narracao_es.wav"),"-i",str(AD/"_audio/demucs/htdemucs/orig/no_vocals.wav"),"-filter_complex",
    f"[0:v]trim=0:{fim},setpts=PTS-STARTPTS[v];[1:a]aformat=channel_layouts=stereo,atrim=0:{fim}[n];[2:a]aformat=channel_layouts=stereo,atrim=0:{fim}[f];"
    f"[n][f]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95,afade=t=out:st={fim-0.3}:d=0.3,asetpts=PTS-STARTPTS[a]",
    "-map","[v]","-map","[a]","-threads","4","-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,
    "-c:a","aac","-b:a","192k","-ar","48000",str(AD/"corpo_ad02.mp4")],check=True)
print("ok corpo",fim)
