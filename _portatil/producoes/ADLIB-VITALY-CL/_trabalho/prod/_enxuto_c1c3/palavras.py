import sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import legenda as LEG
for c in sys.argv[1:]:
    pal = LEG.palavras_por_alinhamento(c + "/narr.alinhamento.json", 0)
    print("==", c, len(pal))
    print(" ".join(f"{w}@{a:.2f}" for w, a, *_ in pal))
