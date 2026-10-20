# voz PL -> -14,3 LUFS (mesmo nivel do voz_norm EN) + bed.wav do EN (demucs no_vocals a -32 LUFS + live final) -> mix_pl.wav
import subprocess, json, re
BED = "C:/Users/PICHAU/Downloads/SB-EN-OFERTA-LIVE/01_ADS-9/_trabalho/audio/bed.wav"
def lufs(p):
    o = subprocess.run(["ffmpeg", "-nostats", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])
g = -14.3 - lufs("audio/voz_pl.wav"); print("ganho voz", round(g, 2))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "audio/voz_pl.wav", "-af", f"volume={g:.2f}dB,alimiter=limit=0.84:attack=2:release=50:level=false",
                "-ar", "48000", "audio/voz_norm.wav"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "audio/voz_norm.wav", "-i", BED, "-filter_complex",
                "[0:a][1:a]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.89:attack=2:release=50:level=false[a]",
                "-map", "[a]", "-ar", "48000", "-c:a", "pcm_s16le", "audio/mix_pl.wav"], check=True)
print("voz", lufs("audio/voz_norm.wav"), "mix", lufs("audio/mix_pl.wav"))
