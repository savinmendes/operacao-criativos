import sys, subprocess, os
f, t_out = sys.argv[1], sys.argv[2]
tmp = f + ".tmp.mp4"
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f,"-t",t_out,"-an","-c:v","libx264","-crf","22","-preset","medium",
 "-vf","format=yuv420p","-colorspace","smpte170m","-color_primaries","smpte170m","-color_trc","smpte170m","-color_range","tv","-movflags","+faststart",tmp],check=True)
os.replace(tmp, f); print("cortado", f, t_out)
