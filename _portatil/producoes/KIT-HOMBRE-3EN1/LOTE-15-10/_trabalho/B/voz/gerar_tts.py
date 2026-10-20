# -*- coding: utf-8 -*-
"""TTS do agente B (vozes registradas em _vozes.json). Texto do áudio pode ter grafia fonética;
a legenda usa o texto do roteiro (textos_legenda.json) com alinhamento CTC, por isso o alinhamento do
ElevenLabs é guardado como .el.json (não é usado automaticamente)."""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import gerar  # noqa: E402

AQUI = Path(__file__).resolve().parent
DAMIAN = "BPwS5yO6aXvwg8auqNwS"   # homem A (04/06)
RICHARD = "Cpm6N9BNC1M75bYS7kO1"  # homem B (05)

# nome: (voz, texto do roteiro [legenda], texto falado [TTS])
FALAS = {
    "A1_heygen": (DAMIAN, "Me lo preguntan siempre. Y la verdad es que no uso uno… uso tres.",
                  "Me lo preguntan siempre. Y la verdad... es que no uso uno... uso tres."),
    "N4_club": (DAMIAN, "Armaf Club de Nuit: fresco, masculino y poderoso.",
                "Armaf Club de Nuí: fresco, masculino y poderoso."),
    "N4_asad": (DAMIAN, "Lattafa Asad: intenso, sofisticado y seductor.",
                "Lattafa Asad: intenso, sofisticado y seductor."),
    "N4_9pm": (DAMIAN, "Y Afnan 9PM: elegante, moderno y refinado.",
               "Y Afnan Nine P M: elegante, moderno y refinado."),
    "A2_heygen": (DAMIAN, "Vienen los tres en un pack: tres perfumes al precio de uno. Pídelo ahora y paga cuando lo recibas.",
                  "Vienen los tres en un pack: tres perfumes al precio de uno. Pídelo ahora... y paga cuando lo recibas."),
    "B1_heygen": (RICHARD, "Eso pensaba yo. Pero acá pagas cuando te llega: lo recibí en mi casa y recién ahí pagué.",
                  "Eso pensaba yo. Pero acá pagas cuando te llega: lo recibí en mi casa... y recién ahí pagué."),
    "N5_club": (RICHARD, "Llegaron los tres. Armaf Club de Nuit, fresco y poderoso.",
                "Llegaron los tres. Armaf Club de Nuí, fresco y poderoso."),
    "N5_asad": (RICHARD, "Lattafa Asad, intenso y seductor.", "Lattafa Asad, intenso y seductor."),
    "N5_9pm": (RICHARD, "Y Afnan 9PM, elegante y refinado.", "Y Afnan Nine P M, elegante y refinado."),
    "N5_cta": (RICHARD, "Tres perfumes al precio de uno. Si desconfías como yo, pídelo y paga solo cuando lo tengas en tus manos.",
               "Tres perfumes al precio de uno. Si desconfías como yo, pídelo... y paga solo cuando lo tengas en tus manos."),
}

if __name__ == "__main__":
    so = sys.argv[1:] or list(FALAS)
    total = 0
    for nome in so:
        voz, rot, fala = FALAS[nome]
        total += len(fala)
        mp3, js = gerar(fala, str(AQUI / f"{nome}.mp3"), voz, estabilidade=0.45)
        os.replace(js, str(AQUI / f"{nome}.el.json"))
        print("ok", nome)
    tx = AQUI / "textos_legenda.json"
    d = json.load(open(tx, encoding="utf-8")) if tx.exists() else {}
    d.update({k: v[1] for k, v in FALAS.items()})
    json.dump(d, open(tx, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("caracteres:", total, "≈ US$", round(total / 1000 * 0.165, 3))
