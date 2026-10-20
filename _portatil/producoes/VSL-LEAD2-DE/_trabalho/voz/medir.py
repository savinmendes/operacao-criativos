import json, glob, sys, os
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import palavras
R = r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho"
BL = {b['id']: b for b in json.load(open(R + r"\roteiro\roteiro_de.json", encoding="utf-8"))}
tot_de = tot_es = 0
for p in sorted(glob.glob("tts/*.alinhamento.json")):
    bid = os.path.basename(p).split('.')[0]; pw = palavras(p)
    d = pw[-1][2] - pw[0][1]; es = BL[bid]['fim_es'] - BL[bid]['ini_es']; tot_de += d; tot_es += es
    if len(sys.argv) > 1: print(bid, 'w', len(pw), 'dur %.2f' % d, 'es %.2f' % es, 'ratio %.2f' % (d / es), 'wpm %.0f' % (len(pw) / d * 60))
print('total de %.1f es %.1f ratio %.3f' % (tot_de, tot_es, tot_de / tot_es))
