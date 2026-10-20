# -*- coding: utf-8 -*-
"""TTS das falas da P8 (ElevenLabs) + prep (pausas <= 0,25 s) -> voz/<id>.wav (48k mono) + voz/<id>.json (palavras)."""
import json, subprocess, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\TESTE1-SB-ES\_trabalho\voz")
from tts_elevenlabs import gerar
from palavras import palavras
AQ = Path(__file__).resolve().parent; SR = 48000; MAXP, LEAD, TAIL = 0.25, 0.10, 0.20
GAB = "hHjbwzYZW17oh0p05AKv"; TOM = "sJYGLUA6m2su09XOMEb8"
F = {
 "R00": (GAB, .5, .2, 1.20, "Imágenes impactantes: un vendedor fue echado de un bus… por su fe."),
 "R01": (GAB, .5, .2, 1.08, "Al día siguiente, don Tomás vendió toda su caja antes del mediodía."),
 "T1a": (TOM, .45, .3, 1.12, "Esa noche conté las monedas… no alcanzaba ni para el pasaje de vuelta."),
 "T1b": (TOM, .45, .3, 1.12, "Me sentí un viejo que ya no le sirve a nadie."),
 "T2":  (TOM, .45, .3, 1.12, "Mi hijo me mandó la transmisión del padre Juan Méndez. La hice esa misma noche, como él enseña."),
 "T3":  (TOM, .45, .3, 1.12, "Al otro día, la gente me paraba en la calle para comprarme."),
 "P1":  (TOM, .45, .3, 1.12, "Si tú también rezas y sientes que nadie te escucha… y que las cosas solo empeoran… no es que Dios no te escuche."),
 "P2":  (TOM, .45, .3, 1.12, "Es que, igual que yo, lo estabas pidiendo de la forma equivocada. El padre Juan Méndez me enseñó la forma correcta de pedirle a San Benito…"),
 "P3":  (TOM, .45, .3, 1.12, "y está haciendo la oración en vivo ahora mismo. ¿Usted puede pasar la transmisión para los que nos están viendo?"),
 "CTA": (GAB, .4, .4, 1.10, "¡Claro! Toquen el botón que está abajo del video y entren ahora a la oración en vivo."),
}
def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).copy()
for i in (sys.argv[1:] or F):
    v, est, sty, vel, t = F[i]
    if not (AQ / f"{i}.mp3").exists(): gerar(t, str(AQ / f"{i}.mp3"), v, estabilidade=est, estilo=sty, velocidade=vel)
    a = load(AQ / f"{i}.mp3"); P = palavras(AQ / f"{i}.alinhamento.json")
    t0 = max(0.0, P[0]["ini"] - LEAD); t1 = min(len(a) / SR, P[-1]["fim"] + TAIL); cortes = []
    for x, y in zip(P, P[1:]):
        g = y["ini"] - x["fim"]
        if g > MAXP: c0 = x["fim"] + MAXP / 2; cortes.append((c0, c0 + g - MAXP))
    keep, tt = [], t0
    for c0, c1 in cortes: keep.append((tt, c0)); tt = c1
    keep.append((tt, t1)); xf = int(0.008 * SR); out = np.zeros(0, np.float32)
    for x, y in keep:
        p = a[int(x * SR):int(y * SR)].copy()
        if len(out) and len(p) > xf: p[:xf] *= np.linspace(0, 1, xf); out[-xf:] *= np.linspace(1, 0, xf)
        out = np.concatenate([out, p])
    f = int(0.03 * SR); out[-f:] *= np.linspace(1, 0, f)
    def m(x): return round(x - t0 - sum(min(max(x - c0, 0), c1 - c0) for c0, c1 in cortes), 3)
    W = [dict(w=p["w"], ini=m(p["ini"]), fim=m(p["fim"])) for p in P]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", str(AQ / f"{i}.wav")], input=out.tobytes(), check=True)
    (AQ / f"{i}.json").write_text(json.dumps(dict(texto=t, voz=v, est=est, estilo=sty, vel=vel, dur=round(len(out) / SR, 3), palavras=W), ensure_ascii=False, indent=0), encoding="utf-8")
    print(i, f"{len(a)/SR:.2f} -> {len(out)/SR:.2f}")
