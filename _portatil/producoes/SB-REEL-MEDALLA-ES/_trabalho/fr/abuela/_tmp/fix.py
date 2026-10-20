import re, sys
p, f = sys.argv[1], sys.argv[2]
L = open(p, encoding="utf-8").read().split("\n")
dur = re.search(r"\((\d+,\d s)\)", L[0]).group(1)
L[0] = L[0].split(" -> ")[0] + " -> C:/Users/PICHAU/Downloads/SB-MEDALLA-COMPLETA-FR/" + f + " (" + dur + ") + _narracion.txt"
open(p, "w", encoding="utf-8").write("\n".join(L)); print(L[0])
