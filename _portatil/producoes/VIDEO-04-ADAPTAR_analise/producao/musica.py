# -*- coding: utf-8 -*-
"""Trilhas instrumentais próprias (ElevenLabs /v1/music): tensão (até o ¡Alto!) e esperança (depois). cwd = kit-edicao-criativos."""
import sys, requests
from pathlib import Path
sys.path.insert(0, "ferramentas"); import tts_elevenlabs as T
P = Path(__file__).resolve().parent / "musica"
H = {"xi-api-key": T.chave()}
def saldo(): return requests.get("https://api.elevenlabs.io/v1/user/subscription", headers=H).json().get("character_count")
s0 = saldo(); print("antes", s0)
J = {"tensao": ("Dark cinematic suspense underscore, low sustained strings drone, slow deep pulsing heartbeat percussion, distant choir pad, "
                "mysterious ancient monastery atmosphere, rising tension, no melody hooks, no drums fills, instrumental only", 48000),
     "esperanca": ("Hopeful sacred cinematic instrumental, warm soft piano and gentle strings, subtle angelic choir pad, uplifting and emotional, "
                   "slow steady build, faith and light, calm, no percussion hits, instrumental only", 46000)}
for n, (pr, ms) in J.items():
    if (P / f"{n}.mp3").exists(): continue
    r = requests.post("https://api.elevenlabs.io/v1/music", headers=H, json={"prompt": pr, "music_length_ms": ms, "force_instrumental": True}, timeout=600)
    print(n, r.status_code)
    if r.ok: (P / f"{n}.mp3").write_bytes(r.content)
    else: print(r.text[:400])
print("depois", saldo(), "consumo", (saldo() or 0) - (s0 or 0))
