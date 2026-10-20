src = open("montar_corpo.py", encoding="utf-8").read()
ini = src.index("segs, t = [], 0.0")
fim = src.index('lst = WK / "lista.txt"')
head = src[:ini].replace('«El Maestro»', '«El Mecánico»')
head = head.replace('T, AU, UB = P / "takes", P / "audio", P / "unbox"',
                    'T, AU, C = P / "takes", P / "audio", P / "cenas"\nUB = Path("C:/Users/PICHAU/Downloads/KIT-HOMBRE-3EN1/PROD1-EL-MAESTRO/unbox")')
old = '''        fc.append(f"[{i}:v]{BASE}{(',' + vx) if vx else ''},trim=duration={t},setpts=PTS-STARTPTS[v{i}]")'''
assert old in head
head = head.replace(old,
'''        sel = bool(vx) and vx.endswith("|SELO")
        if sel: vx = vx[:-5] or None
        fc.append(f"[{i}:v]{BASE}{(',' + vx) if vx else ''},trim=duration={t},setpts=PTS-STARTPTS[v{i}{'s' if sel else ''}]")
        if sel: selos.append(i)''')
assert '    ins, fc = [], []\n' in head
head = head.replace('    ins, fc = [], []\n', '    ins, fc, selos = [], [], []\n')
old2 = '''    n = len(partes)\n'''
assert old2 in head
head = head.replace(old2, '''    n = len(partes)
    for j, i in enumerate(selos):
        ins += ["-loop", "1", "-t", str(partes[i][2]), "-i", str(SELO)]
        fc.append(f"[v{i}s][{n + j}:v]overlay=0:0:shortest=1[v{i}]")
''')
assert "    k = n\n" in head
head = head.replace("    k = n\n", "    k = n + len(selos)\n")
corpo = open("_corpo_blocos.py", encoding="utf-8").read()
open("montar_corpo.py", "w", encoding="utf-8").write(head + corpo + src[fim:])
print("ok")
