import sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import gerar
T = "Chcesz poznać perfumy, przez które kobiety oszaleją na twoim punkcie? Lattafa Asad. Intensywny, wyrafinowany i uwodzicielski."
V = {"vera":"xjlfQQ3ynqiEyRpArrT8","lola":"FM3ChNOHGKKULNhmx5m2","natasha":"kCx3Qoh3lfILbbTZftSq","sarah":"EXAVITQu4vr4xnSDxMaL","cristina":"1CeqBeXMOqCleeQjfYfO","jessica":"cgSgspJ2msm6clMCkdW9"}
for k,v in V.items():
    gerar(T, f"{k}.mp3", voz=v); print(k, flush=True)
