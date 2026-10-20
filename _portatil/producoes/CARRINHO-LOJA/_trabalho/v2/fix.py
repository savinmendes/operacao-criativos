bs = chr(92)
s = open('e2e_v2.py', encoding='utf-8').read()
s = s.replace('{OUT}' + bs, '{OUT}/').replace('OUT + r"' + bs + 'teste_log.txt"', 'OUT + "/teste_log.txt"')
open('e2e_v2.py', 'w', encoding='utf-8').write(s)
