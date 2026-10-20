import sys, numpy as np, cv2, importlib.util, json
sys.argv = ["x", "__nenhum__"]
src = open("montar_base.py", encoding="utf-8").read().split("TV = {")[0]
exec(src)
nm = sys.argv_nm if hasattr(sys, "argv_nm") else None
