# mapa de tempo ES (fonte) -> EN (saida). O=inicio da voz do anjo na saida
import numpy as np
O=5.75
_es=[0,4.10,5.12, 9.32,16.74,21.24,24.10,32.12,34.06,38.54,46.68,50.66,54.32,58.00,62.82,65.76,76.02,82.22,84.62,86.22,89.04,93.88,101.56,107.30,109.12,119.46,120.5,122.98,124.22,126.26,130.08,132.82,136.10,142.54,148.0]
_en=[0,4.75,0, 3.81,9.93,14.12,16.60,23.51,25.16,29.08,35.40,39.21,42.25,44.83,48.24,51.36,60.22,64.63,67.08,68.77,71.38,74.57,80.42,84.78,86.67,93.39,94.40,96.59,97.77,99.42,102.86,106.19,109.48,112.37,116.27]
ES=np.array(_es,float); EN=np.array(_en[:2]+[O+x for x in _en[2:]],float)
assert np.all(np.diff(ES)>0) and np.all(np.diff(EN)>0)
# so os cortes de plano viram ancoras (dentro de um plano o fator e uniforme)
CORTES=[0,4.10,5.3,9.05,9.4,33.83,34.05,38.37,38.6,46.6,48.5,50.55,53.13,62.57,65.6,86.47,88.8,93.87,118.97,119.4,120.6,122.87,124.1,148.0]
_EN=[round(float(np.interp(t,ES,EN))*30)/30 for t in CORTES]
ES=np.array(CORTES,float); EN=np.array(_EN,float)
TOTAL=round(EN[-1]*30)/30
def en2es(t): return float(np.interp(t,EN,ES))
def es2en(t): return float(np.interp(t,ES,EN))
if __name__=="__main__":
    print("TOTAL",TOTAL)
    for a,b,c,d in zip(ES[:-1],ES[1:],EN[:-1],EN[1:]): print(f"ES {a:6.2f}-{b:6.2f} -> EN {c:6.2f}-{d:6.2f} fator {(d-c)/(b-a):.2f}")
