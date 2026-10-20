# -*- coding: utf-8 -*-
"""Monta comerciante.mp3 e sacerdote.mp3 a partir das partes do ElevenLabs,
insere pausas nas linhas latinas e grava alinhamento por palavra (texto CORRETO da legenda).

Saídas (em voz/):
  comerciante.mp3 + comerciante.alinhamento.json (chars, formato ElevenLabs) + comerciante.palavras.json
  sacerdote.mp3   + sacerdote.alinhamento.json + sacerdote.palavras.json
  narracao_completa.mp3 + narracao_completa.palavras.json (linha do tempo única, sacerdote deslocado)
"""
import json, re, subprocess
from pathlib import Path
import numpy as np
import soundfile as sf

AQUI = Path(__file__).resolve().parent
P = AQUI / "partes"
SR = 44100

# grafia fonética enviada ao TTS -> grafia correta da legenda
CORRIGE = {"míki": "mihi", "Sátana": "Satana", "Númcuam": "Numquam", "cue": "quae",
           "líbas": "libas", "bíbas": "bibas"}


def carregar(mp3):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp3), "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype=np.float32).copy()


def palavras(al_json):
    d = json.loads(Path(al_json).read_text(encoding="utf-8"))
    ch, ini, fim = d["characters"], d["character_start_times_seconds"], d["character_end_times_seconds"]
    txt = "".join(ch)
    # remove tags de áudio do v3 ([whispers] etc.)
    mask = [False] * len(txt)
    for m in re.finditer(r"\[[^\]]*\]", txt):
        for i in range(m.start(), m.end()):
            mask[i] = True
    ws, cur = [], None
    for i, c in enumerate(ch):
        if mask[i] or c.isspace():
            if cur:
                ws.append(cur); cur = None
            continue
        if cur is None:
            cur = {"w": c, "ini": ini[i], "fim": fim[i]}
        else:
            cur["w"] += c; cur["fim"] = fim[i]
    if cur:
        ws.append(cur)
    # pontuação solta (… sozinho) gruda na anterior
    out = []
    for w in ws:
        if out and not re.search(r"\w", w["w"]):
            out[-1]["w"] += w["w"]; continue
        out.append(w)
    return out


def corrigir(w):
    m = re.match(r"^([¡¿«]*)(.*?)([.,;:!?…»]*)$", w)
    a, core, b = m.groups()
    return a + CORRIGE.get(core, core) + b


def lufs(x):
    import pyloudnorm as pyln
    return pyln.Meter(SR).integrated_loudness(x.astype(np.float64))


def normalizar(x, alvo=-18.0):
    return (x * 10 ** ((alvo - lufs(x)) / 20)).astype(np.float32)


class Trilha:
    def __init__(self):
        self.audio = []; self.t = 0.0; self.ws = []

    def add(self, x, ws_rel, t0_src, tags=None):
        """x = trecho; ws_rel = palavras com tempos no arquivo-fonte; t0_src = início do trecho no fonte."""
        for w in ws_rel:
            d = dict(w); d["ini"] = round(w["ini"] - t0_src + self.t, 3); d["fim"] = round(w["fim"] - t0_src + self.t, 3)
            if tags: d.update(tags)
            self.ws.append(d)
        self.audio.append(x); self.t += len(x) / SR

    def silencio(self, s):
        self.audio.append(np.zeros(int(round(s * SR)), np.float32)); self.t += s

    def salvar(self, nome):
        a = np.concatenate(self.audio)
        wav = AQUI / f"{nome}.wav"; sf.write(wav, a, SR)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-c:a", "libmp3lame", "-b:a", "192k",
                        str(AQUI / f"{nome}.mp3")], check=True)
        wav.unlink()
        (AQUI / f"{nome}.palavras.json").write_text(json.dumps(self.ws, ensure_ascii=False, indent=1), encoding="utf-8")
        # alinhamento por caractere no formato ElevenLabs (para legenda.py --alinhamento)
        ch, si, ei = [], [], []
        for k, w in enumerate(self.ws):
            if k:
                ch.append(" "); si.append(self.ws[k - 1]["fim"]); ei.append(w["ini"])
            n = len(w["w"]); dur = (w["fim"] - w["ini"]) / n
            for j, c in enumerate(w["w"]):
                ch.append(c); si.append(round(w["ini"] + j * dur, 3)); ei.append(round(w["ini"] + (j + 1) * dur, 3))
        (AQUI / f"{nome}.alinhamento.json").write_text(json.dumps(
            {"characters": ch, "character_start_times_seconds": si, "character_end_times_seconds": ei},
            ensure_ascii=False), encoding="utf-8")
        return a


def trecho(x, ws, i0, i1, pad=0.06):
    """palavras ws[i0:i1]; corta no meio da pausa (limitado a pad... usa metade da pausa vizinha)."""
    a = ws[i0]["ini"]; b = ws[i1 - 1]["fim"]
    prev_fim = ws[i0 - 1]["fim"] if i0 > 0 else 0.0
    nxt_ini = ws[i1]["ini"] if i1 < len(ws) else len(x) / SR
    t0 = max(prev_fim + (a - prev_fim) / 2, 0.0) if i0 > 0 else 0.0
    t1 = b + (nxt_ini - b) / 2 if i1 < len(ws) else len(x) / SR
    y = x[int(t0 * SR):int(t1 * SR)].copy()
    f = int(0.01 * SR)  # micro fade
    y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    return y, ws[i0:i1], t0


def idx_frase(ws, termina_em):
    """índices de fim (exclusivo) de cada frase (palavra terminando em . ! ? …)."""
    return [i + 1 for i, w in enumerate(ws) if re.search(r"[.!?…]$", w["w"])]


def main():
    # ---------- COMERCIANTE ----------
    a = normalizar(carregar(P / "com_a_v3.mp3"), -20.0)  # reza: um pouco mais baixa
    wa = palavras(P / "com_a_v3.alinhamento.json")
    b = normalizar(carregar(P / "com_b.mp3"), -18.0)
    wb = palavras(P / "com_b.alinhamento.json")
    T = Trilha()
    y, w, t0 = trecho(a, wa, 0, len(wa)); T.add(y, w, t0, {"personagem": "comerciante", "parte": "reza"})
    T.silencio(max(0.0, 11.9 - T.t))  # 2ª fala começa ~00:12 como no roteiro
    y, w, t0 = trecho(b, wb, 0, len(wb)); T.add(y, w, t0, {"personagem": "comerciante", "parte": "selfie"})
    com = T.salvar("comerciante")
    com_ws = T.ws

    # ---------- SACERDOTE ----------
    s = normalizar(carregar(P / "sac.mp3"))
    ws = palavras(P / "sac.alinhamento.json")
    L = normalizar(carregar(P / "sac_latim.mp3"))
    wl = palavras(P / "sac_latim.alinhamento.json")
    for w in wl:
        w["w"] = corrigir(w["w"])
    texto = [w["w"] for w in ws]
    i_conm = next(i for i, w in enumerate(texto) if w.startswith("conmigo")) + 1
    i_esta = next(i for i, w in enumerate(texto) if w == "Esta")
    S = Trilha()
    y, w, t0 = trecho(s, ws, 0, i_conm); S.add(y, w, t0, {"personagem": "sacerdote"})
    S.silencio(0.35)
    fins = idx_frase(wl, None)  # 12 frases: latim, tradução, latim, ...
    assert len(fins) == 12, [wl[i - 1]["w"] for i in fins]
    ini = 0
    for k, fe in enumerate(fins):
        y, w, t0 = trecho(L, wl, ini, fe)
        latim = k % 2 == 0
        S.add(y, w, t0, {"personagem": "sacerdote", "latim": latim, "linha": k // 2 + 1,
                         "papel": "latim" if latim else "traducao"})
        S.silencio(0.12 if latim else 0.22)  # + metade das pausas naturais => ~0,45 / ~0,6 s
        ini = fe
    S.silencio(0.15)
    y, w, t0 = trecho(s, ws, i_esta, len(ws)); S.add(y, w, t0, {"personagem": "sacerdote"})
    sac = S.salvar("sacerdote")

    # ---------- LINHA DO TEMPO ÚNICA ----------
    gap = 0.45
    off = len(com) / SR + gap
    tot = np.concatenate([com, np.zeros(int(gap * SR), np.float32), sac])
    sf.write(AQUI / "narracao_completa.wav", tot, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(AQUI / "narracao_completa.wav"), "-c:a", "libmp3lame",
                    "-b:a", "192k", str(AQUI / "narracao_completa.mp3")], check=True)
    (AQUI / "narracao_completa.wav").unlink()
    allw = [dict(w) for w in com_ws] + [dict(w, ini=round(w["ini"] + off, 3), fim=round(w["fim"] + off, 3)) for w in S.ws]
    (AQUI / "narracao_completa.palavras.json").write_text(json.dumps(allw, ensure_ascii=False, indent=1), encoding="utf-8")
    info = {"comerciante_dur": round(len(com) / SR, 2), "sacerdote_dur": round(len(sac) / SR, 2),
            "sacerdote_offset": round(off, 2), "total": round(len(tot) / SR, 2)}
    (AQUI / "timeline.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    print(info)


if __name__ == "__main__":
    main()
