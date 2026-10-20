# take Seedance: trecho da ação [0, A] em câmera lenta (vel V, interpolação mci) + resto normal -> takes/briga_slow.mp4 (30 fps, áudio esticado no trecho lento)
import subprocess, sys
A, V = 3.70, 0.627
src = "takes/seedance_briga2.mp4"; out = "takes/briga2_slow.mp4"
fc = (f"[0:v]trim=0:{A},setpts=(PTS-STARTPTS)/{V},minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1[v1];"
      f"[0:v]trim=start={A},setpts=PTS-STARTPTS,fps=30[v2];[v1][v2]concat=n=2:v=1:a=0[v];"
      f"[0:a]atrim=0:{A},asetpts=PTS-STARTPTS,atempo={V}[a1];[0:a]atrim=start={A},asetpts=PTS-STARTPTS[a2];[a1][a2]concat=n=2:v=0:a=1[a]")
r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "10", "-preset", "medium",
                    "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", "48000", out.replace(".mp4", ".mov")], capture_output=True, text=True)
print(r.returncode, r.stderr[-800:]); print("trecho lento termina em", A / V)
