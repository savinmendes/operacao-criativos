BS = chr(92)
s = open('RELATORIO.md', 'rb').read().decode('utf-8')
s = s.replace('revisao' + chr(13) + 'evisar_loteB_i1', 'revisao' + BS + 'revisar_loteB_i1')
open('RELATORIO.md', 'wb').write(s.encode('utf-8'))
