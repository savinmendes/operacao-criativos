import subprocess, sys
def pts_idx(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "frame=pts_time", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return sorted(int(round(float(x.split(",")[0]) * 30)) for x in r.stdout.split() if x.split(",")[0])
for p in sys.argv[1:]:
    i = pts_idx(p); falta = sorted(set(range(i[-1] + 1)) - set(i))
    print(p, len(i), "ultimo", i[-1], "buracos", falta[:20])
