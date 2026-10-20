"""Entrada do lipsync do gancho (quadros 0-285 = 0-9,533 s): recorte 360x640 em (290,200) da base limpa (so a mulher; a enfermeira fica fora),
escala 2x -> 720x1280, com o AUDIO ORIGINAL PT. ES separado em es_h1.mp3."""
import subprocess
X,Y,W,H=290,200,360,640; T=286/30
COR=["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
subprocess.run(["ffmpeg","-v","error","-y","-i","base_sem_legenda.mp4","-i","../../../UNICOS_HD/02.mp4","-filter_complex",
 f"[0:v]trim=end_frame=286,setpts=PTS-STARTPTS,crop={W}:{H}:{X}:{Y},scale=720:1280:flags=lanczos[v];[1:a]atrim=0:{T},asetpts=PTS-STARTPTS[a]",
 "-map","[v]","-map","[a]","-c:v","libx264","-crf","12","-preset","slow","-pix_fmt","yuv420p",*COR,"-r","30","-c:a","aac","-b:a","192k","lipsync/pt_h1.mp4"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i","narracao_es.wav","-af",f"atrim=0:{T}","-ac","1","-c:a","libmp3lame","-b:a","192k","lipsync/es_h1.mp3"],check=True)
