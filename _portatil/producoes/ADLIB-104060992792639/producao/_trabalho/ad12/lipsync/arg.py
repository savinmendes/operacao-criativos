import numpy as np, json, sys
AD = sys.argv[1]
segs = [s["nome"] for s in json.load(open(AD + '/segmentos.json'))["segmentos"]]
parts = []
for n in segs:
    P = np.load(f'{AD}/lipsync/in/geo_{n}.npz')["P"]; P = P[~np.isnan(P).any(axis=(1,2))]
    x0, y0 = np.percentile(P[:,:,0].min(1), 5), np.percentile(P[:,:,1].min(1), 5); x1, y1 = np.percentile(P[:,:,0].max(1), 95), np.percentile(P[:,:,1].max(1), 95)
    ro = f"{int(x0-20)};{int(y0-20)};{int(x1-x0+40)};{int(y1-y0+40)}"
    parts.append(f"{AD}/lipsync/out/full_{n}.mp4:{AD}/lipsync/in/es_{n}.mp3:{AD}/lipsync/in/pt_{n}.mp4:{ro}")
print(",".join(parts))
