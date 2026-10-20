import json
t=json.load(open('_audio/tempos_reais.json',encoding='utf-8'))
open('roteiro_es.txt','w',encoding='utf-8').write('\n\n'.join("[%s] (%.1f-%.1f s)\n%s"%(x['quem'],x['ini'],x['fim'],x['texto']) for x in t)+'\n')
