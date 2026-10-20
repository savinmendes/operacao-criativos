import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "ad14"))
from broll import take
D = Path(__file__).parent
# C1: closes do produto do proprio 16 (visao noturna, reflector, audio) - recorte a esquerda tira o rosto do criador e a legenda
take("16.mp4", 21.30, 27.55, (0, 60, 430, 764), None, D / "c1.mp4", vel=6.25/6.75)
# Emprestados do 14 (mesmo produto, sem rosto): instalacao na parede e gravacoes (desfocadas)
take("14.mp4", 28.45, 31.95, (90, 0, 540, 960), None, D / "c2.mp4")
take("14.mp4", 34.95, 38.60, (90, 0, 540, 960), (46, 156, 690, 516), D / "c3.mp4", vel=0.8)
