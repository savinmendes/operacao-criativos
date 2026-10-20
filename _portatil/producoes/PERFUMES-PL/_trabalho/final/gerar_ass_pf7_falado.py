# Legenda do PL_PF-7 com hook falado (Lily, pausas encurtadas, início 0,15 s) — mesmo estilo dos hooks 17/18.
src = open(__file__.replace("gerar_ass_pf7_falado.py", "gerar_ass.py"), encoding="utf-8").read()
exec(src.split("\nA = T + ")[0])
P = T + r"\pf7hook"
gerar("leg_pf7_falado.ass", 7.8333, P + r"\hookpf7_lily_curta.alinhamento.json", {"trzy": "3", "jednych": "1", "sto": "100"}, 0.15)
print("ok")
