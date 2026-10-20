# -*- coding: utf-8 -*-
"""TTS ElevenLabs das falas da P7 (Antonio = Pa Gabriel; reportera = Gabriela) + encurta pausas > 0,25 s -> <id>.wav 48k + <id>.json
Uso: python gerar.py [ids...]"""
import json, subprocess, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\TESTE1-SB-ES\_trabalho\voz")
from tts_elevenlabs import gerar
from palavras import palavras
AQ = Path(__file__).resolve().parent; SR = 48000; MAXP, LEAD, TAIL = 0.25, 0.12, 0.20
ANT = "Zkg9LlmGNlBWLgWjzTnu"; REP = "hHjbwzYZW17oh0p05AKv"
F = {
 "R00": (REP, 0.5, 0.2, 1.16, "Imágenes impactantes: un jubilado fue humillado en la fila del banco… por su fe."),
 "R01": (REP, 0.5, 0.2, 1.08, "Días después, la historia de don Antonio conmovió a todo el país."),
 "A1": (ANT, 0.45, 0.3, 1.04, "Esa noche no quise comer. Cuarenta años trabajando… y me trataron como si yo no valiera nada."),
 "A2": (ANT, 0.45, 0.3, 1.06, "Mi nieta me mandó la transmisión del padre Juan Méndez. La hice esa misma noche, como él enseña. Al día siguiente, me sentí en paz por primera vez en años."),
 "P1": (ANT, 0.45, 0.3, 1.06, "Si tú también rezas y sientes que nadie te escucha… y que las cosas solo empeoran… no es que Dios no te escuche."),
 "P2": (ANT, 0.45, 0.3, 1.06, "Es que, igual que yo, lo estabas pidiendo de la forma equivocada. El padre Juan Méndez me enseñó la forma correcta de pedirle a San Benito…"),
 "P3": (ANT, 0.45, 0.3, 1.06, "y está haciendo la oración en vivo ahora mismo. ¿Usted puede pasar la transmisión para los que nos están viendo?"),
 "CTA": (REP, 0.4, 0.4, 1.06, "¡Claro! Toquen el botón que está abajo del video y entren ahora a la oración en vivo."),
}
def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).copy()
for i in (sys.argv[1:] or list(F)):
    v, est, sty, vel, t = F[i]
    if not (AQ / f"{i}.mp3").exists(): gerar(t, str(AQ / f"{i}.mp3"), v, "eleven_multilingual_v2", est, 0.75, sty, vel)
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
    def m(q): return round(q - t0 - sum(min(max(q - c0, 0), c1 - c0) for c0, c1 in cortes), 3)
    W = [dict(w=p["w"], ini=m(p["ini"]), fim=m(p["fim"])) for p in P]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", str(AQ / f"{i}.wav")], input=out.tobytes(), check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(AQ / f"{i}.wav"), "-c:a", "libmp3lame", "-b:a", "192k", str(AQ / f"{i}_hg.mp3")], check=True)
    (AQ / f"{i}.json").write_text(json.dumps(dict(texto=t, voz=v, est=est, estilo=sty, vel=vel, dur=round(len(out) / SR, 3), palavras=W, cortes=cortes), ensure_ascii=False, indent=0), encoding="utf-8")
    print(i, f"{len(a)/SR:.2f} -> {len(out)/SR:.2f}", "cortes", len(cortes))
