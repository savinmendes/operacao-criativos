# voz PL a -15 LUFS + trilha (demucs ES) a -32 LUFS, soma com limitador -> audio/mix_pl.wav
import subprocess, re
def lufs(f):
    r=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS",r)[-1])
gv=-15-lufs("audio/voz_pl.wav"); gt=-32-lufs("audio/trilha_pl.wav")
subprocess.run(["ffmpeg","-v","error","-y","-i","audio/voz_pl.wav","-i","audio/trilha_pl.wav","-filter_complex",
 f"[0:a]volume={gv:.2f}dB[v];[1:a]volume={gt:.2f}dB[t];[v][t]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89[a]",
 "-map","[a]","-ar","48000","-c:a","pcm_s16le","audio/mix_pl.wav"],check=True)
print("ganhos",round(gv,2),round(gt,2),"mix",lufs("audio/mix_pl.wav"))
