# -*- coding: utf-8 -*-
"""Alinhamento forcado do texto do roteiro sobre o audio LIMPO de cada fala (sem whisper no video final).

  palavras_fonte(audio, texto)  -> [(palavra_do_roteiro, ini, fim), ...] no tempo do arquivo de audio
      - se houver <audio>.alinhamento.json (ElevenLabs) ao lado do audio: usa os tempos por caractere dele
        (metodo="auto"); senao alinhamento forcado CTC (wav2vec2 espanhol, quadros de 20 ms, Viterbi com o texto exato).
      - metodo="ctc" forca o CTC (usado na medicao, como referencia independente do ElevenLabs).
  palavras_timeline(segmentos, raiz, textos, ...) -> [(palavra, ini, fim, idx_segmento)] na linha do tempo final
      - cada segmento usa SO as palavras cujo inicio cai na janela [audio_de, audio_ate) do seu audio,
        deslocadas pelo inicio do segmento na montagem.
Cache: _legenda_sinc/cache/<md5 do audio + texto + metodo>.json
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unicodedata
from pathlib import Path

import numpy as np

SR16 = 16000
MODELO_CTC = "jonatasgrosman/wav2vec2-large-xlsr-53-spanish"
CACHE = Path(__file__).resolve().parent / "_legenda_sinc" / "cache"
_ctc = None


def _pcm16(p) -> np.ndarray:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-map", "0:a:0", "-ac", "1", "-ar", str(SR16),
                        "-f", "s16le", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.int16).astype(np.float32) / 32768


def norm_tok(w: str) -> str:
    """palavra -> so letras do vocabulario do modelo (minusculas, acentos agudos mantidos)"""
    w = w.lower().replace(" ", " ")
    return re.sub(r"[^a-záéíóúñü]", "", w)


def palavras_texto(texto: str) -> list[str]:
    return [w for w in texto.split() if norm_tok(w)]


# ------------------------------------------------------------------ ElevenLabs
def _alinhamento_el(json_path, texto):
    a = json.load(open(json_path, encoding="utf-8"))
    ch, st, en = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
    ws, cur = [], None
    for c, s, e in zip(ch, st, en):
        if c.isspace():
            if cur:
                ws.append(cur)
            cur = None
            continue
        if cur is None:
            cur = [c, s, e, norm_tok(c) != ""]
            if not cur[3]:
                cur[1] = None
        else:
            cur[0] += c
            cur[2] = e
            if norm_tok(c) and cur[1] is None:
                cur[1] = s
    if cur:
        ws.append(cur)
    el = [(w, s, e) for w, s, e, _ in ws if norm_tok(w)]
    return _mapear(palavras_texto(texto), el)


# ------------------------------------------------------------------ CTC
def _modelo():
    global _ctc
    if _ctc is None:
        import torch
        from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
        proc = Wav2Vec2Processor.from_pretrained(MODELO_CTC)
        mod = Wav2Vec2ForCTC.from_pretrained(MODELO_CTC).eval()
        _ctc = (torch, proc, mod)
    return _ctc


def _viterbi(lp: np.ndarray, toks: list[int], blank=0):
    """CTC forced alignment: lp (T, C) log-probs; devolve, por token, (quadro_ini, quadro_fim)."""
    T = lp.shape[0]
    S = 2 * len(toks) + 1
    ext = [blank if i % 2 == 0 else toks[i // 2] for i in range(S)]
    NEG = -1e30
    dp = np.full((T, S), NEG)
    bp = np.zeros((T, S), np.int8)
    dp[0, 0] = lp[0, ext[0]]
    if S > 1:
        dp[0, 1] = lp[0, ext[1]]
    for t in range(1, T):
        prev = dp[t - 1]
        c0 = prev
        c1 = np.concatenate([[NEG], prev[:-1]])
        c2 = np.concatenate([[NEG, NEG], prev[:-2]])
        ext_a = np.array(ext)
        pode2 = np.zeros(S, bool)
        pode2[2:] = (ext_a[2:] != blank) & (ext_a[2:] != ext_a[:-2])
        c2 = np.where(pode2, c2, NEG)
        m = np.stack([c0, c1, c2])
        arg = m.argmax(0)
        dp[t] = m[arg, np.arange(S)] + lp[t, ext_a]
        bp[t] = arg
    s = S - 1 if dp[T - 1, S - 1] >= dp[T - 1, S - 2] else S - 2
    path = [0] * T
    for t in range(T - 1, -1, -1):
        path[t] = s
        s -= int(bp[t, s])
    spans = {}
    for t, s in enumerate(path):
        if s % 2 == 1:
            k = s // 2
            a, b = spans.get(k, (t, t))
            spans[k] = (min(a, t), max(b, t))
    return [spans.get(k) for k in range(len(toks))]


def _alinhamento_ctc(audio, texto):
    torch, proc, mod = _modelo()
    x = _pcm16(audio)
    with torch.no_grad():
        iv = proc(x, sampling_rate=SR16, return_tensors="pt").input_values
        lg = mod(iv).logits[0]
        lp = torch.log_softmax(lg, -1).numpy()
    T = lp.shape[0]
    hop = len(x) / SR16 / T   # ~0,02 s
    voc = proc.tokenizer.get_vocab()
    pal = palavras_texto(texto)
    toks, dono = [], []
    for i, w in enumerate(pal):
        if i:
            toks.append(voc["|"]); dono.append(None)
        for c in norm_tok(w):
            toks.append(voc.get(c, voc["<unk>"])); dono.append(i)
    sp = _viterbi(lp, toks, blank=voc["<pad>"])
    out = []
    for i, w in enumerate(pal):
        fr = [sp[k] for k, d in enumerate(dono) if d == i and sp[k] is not None]
        a = min(f[0] for f in fr) * hop
        b = (max(f[1] for f in fr) + 1) * hop
        out.append((w, round(a, 3), round(b, 3)))
    return out


# ------------------------------------------------------------------ mapear (difflib) texto do roteiro x palavras com tempo
def _mapear(roteiro: list[str], com_tempo: list[tuple]):
    import difflib
    a = [norm_tok(w) for w in roteiro]
    b = [norm_tok(w[0]) for w in com_tempo]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    t = [None] * len(roteiro)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                t[i1 + k] = (com_tempo[j1 + k][1], com_tempo[j1 + k][2])
        elif op == "replace":   # n x m: espalha o trecho de tempo proporcionalmente
            t0, t1 = com_tempo[j1][1], com_tempo[j2 - 1][2]
            n = i2 - i1
            for k in range(n):
                t[i1 + k] = (t0 + (t1 - t0) * k / n, t0 + (t1 - t0) * (k + 1) / n)
    for i in range(len(t)):   # sobras (delete): interpola entre vizinhos
        if t[i] is None:
            ant = next((t[j][1] for j in range(i - 1, -1, -1) if t[j]), 0.0)
            prox = next((t[j][0] for j in range(i + 1, len(t)) if t[j]), ant + 0.3)
            t[i] = (ant, prox)
    return [(w, round(x[0], 3), round(x[1], 3)) for w, x in zip(roteiro, t)]


def palavras_fonte(audio, texto, metodo="auto"):
    audio = Path(audio).resolve()
    el = audio.with_suffix(".alinhamento.json")
    usar_el = metodo == "auto" and el.exists()
    h = hashlib.md5(audio.read_bytes() + texto.encode("utf-8") + (b"el" if usar_el else b"ctc")).hexdigest()[:16]
    CACHE.mkdir(parents=True, exist_ok=True)
    cf = CACHE / f"{audio.stem}_{h}.json"
    if cf.exists():
        return [tuple(x) for x in json.load(open(cf, encoding="utf-8"))]
    r = _alinhamento_el(el, texto) if usar_el else _alinhamento_ctc(audio, texto)
    json.dump(r, open(cf, "w", encoding="utf-8"), ensure_ascii=False)
    return r


def texto_de(fonte: Path, textos: dict):
    """texto do roteiro para um arquivo de audio: chave = nome do arquivo sem extensao; N_*.mp3 sem chave usa o
    texto do proprio .alinhamento.json do ElevenLabs."""
    if fonte.stem in textos:
        return textos[fonte.stem]
    el = fonte.with_suffix(".alinhamento.json")
    if el.exists():
        return "".join(json.load(open(el, encoding="utf-8"))["characters"]).strip()
    return None


def palavras_timeline(segmentos, raiz: Path, faixas, textos: dict, metodo="auto"):
    """segmentos = cfg['segmentos']; faixas = [(ini, fim, tipo)] de cada segmento na montagem."""
    out = []
    for i, (s, (t0, t1, _)) in enumerate(zip(segmentos, faixas)):
        if s.get("audio"):
            fonte = (raiz / s["audio"]).resolve()
            a0 = float(s.get("audio_de", 0))
        else:
            fonte = (raiz / s["video"]).resolve()
            a0 = float(s.get("de", 0))
        a1 = a0 + (t1 - t0)
        txt = texto_de(fonte, textos)
        if txt is None:
            raise SystemExit(f"legenda modo roteiro: sem texto para {fonte.name} (adicione em legenda.textos)")
        for w, a, b in palavras_fonte(fonte, txt, metodo):
            if a0 - 1e-6 <= a < a1 - 0.02:
                out.append((w, round(t0 + a - a0, 3), round(t0 + min(b, a1) - a0, 3), i))
    return out
