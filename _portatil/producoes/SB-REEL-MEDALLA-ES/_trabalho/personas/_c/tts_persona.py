# -*- coding: utf-8 -*-
"""Gera reza (v3, falas 1+2) e selfie (multilingual_v2, falas 3+4+5) de uma persona. Rodar de kit-edicao-criativos.
uso: python tts_persona.py <slug> [reza|selfie|ambos]"""
import base64, json, sys
from pathlib import Path
import requests
sys.path.insert(0, "ferramentas")
import tts_elevenlabs as T
AQ = Path(__file__).resolve().parent
P = json.loads((AQ / "personas_c.json").read_text(encoding="utf-8"))
F1 = "Oh glorioso San Benito... hoy pronuncio las palabras grabadas en tu medalla."
F4 = "Hasta que, en una transmisión en vivo, un padre explicó la forma exacta de pedirle a San Benito."
slug = sys.argv[1]; qual = sys.argv[2] if len(sys.argv) > 2 else "ambos"
c = P[slug]; out = AQ.parent / slug / "voz"; out.mkdir(parents=True, exist_ok=True)
LOG = AQ / "caracteres.log"

def tts(texto, nome, modelo, est):
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{c['voz']}/with-timestamps", params={"output_format": "mp3_44100_128"},
                      headers={"xi-api-key": T.chave(), "Content-Type": "application/json"},
                      json={"text": texto, "model_id": modelo,
                            "voice_settings": {"stability": est, "similarity_boost": 0.75, "style": 0.0, "use_speaker_boost": True, "speed": 1.0}},
                      timeout=300)
    if r.status_code != 200:
        raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:300]}")
    d = r.json()
    (out / f"{nome}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    (out / f"{nome}.alinhamento.json").write_text(json.dumps(d.get("normalized_alignment") or d["alignment"], ensure_ascii=False), encoding="utf-8")
    (out / f"{nome}.txt").write_text(texto, encoding="utf-8")
    with open(LOG, "a", encoding="utf-8") as f: f.write(f"{slug}\t{nome}\t{len(texto)}\n")
    print("ok", nome, len(texto), "caracteres")

if qual in ("reza", "ambos"):
    tts(f"[whispers] {F1} [sighs] {c['f2'][0]} [whispers] {c['f2'][1]}", "reza", "eleven_v3", 0.5)
if qual in ("selfie", "ambos"):
    tts(f"{c['f3']} {F4} {c['f5']}", "selfie", "eleven_multilingual_v2", 0.5)
