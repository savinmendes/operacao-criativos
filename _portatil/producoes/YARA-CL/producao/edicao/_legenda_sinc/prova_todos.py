# -*- coding: utf-8 -*-
"""Prova final: mede a sincronia legenda x fala nos 21 videos finais (ASS da montagem + quadros do video queimado)
e confere que a voz das versoes com musica esta no mesmo tempo da base (correlacao cruzada)."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import medir_sinc as ms

Y = Path(r"C:\Users\PICHAU\Downloads\YARA-CL")
ED = Y / "producao" / "edicao"
lista = []
for h in ["H1", "H2", "H3", "H4", "H5"]:
    base = Y / "entregas" / "volume" / f"YARA-BF_{h}_sem-musica.mp4"
    for v in ["sem-musica", "bbywow", "bambam"]:
        lista.append((h, ED / "volume" / f"cfg_{h}.json", AQUI / "saidas" / f"YARA-BF_{h}_sem-musica.ass", base,
                      Y / "entregas" / "volume" / f"YARA-BF_{h}_{v}.mp4"))
bc = Y / "entregas" / "AD-C_yara-kit3_bf_es-cl.mp4"
for suf in ["", "_musica-A", "_musica-B", "_musica-C", "_trend-bbywow", "_trend-bambam", "_trend-superestrella"]:
    lista.append(("AD-C", ED / "ad_C_final.json", AQUI / "saidas" / "AD-C_yara-kit3_bf_es-cl.ass", bc,
                  Y / "entregas" / f"AD-C_yara-kit3_bf_es-cl{suf}.mp4"))


def pcm(p, t=20.0):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-t", str(t), "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                       capture_output=True)
    return np.frombuffer(r.stdout, np.int16).astype(np.float32)


def atraso_ms(a, b):
    """atraso de b em relacao a a (ms), pela correlacao cruzada (FFT), janela +-300 ms"""
    n = min(len(a), len(b))
    a, b = a[:n] - a[:n].mean(), b[:n] - b[:n].mean()
    N = 1 << (2 * n - 1).bit_length()
    c = np.fft.irfft(np.fft.rfft(b, N) * np.conj(np.fft.rfft(a, N)), N)
    lags = np.r_[np.arange(0, 2400), np.arange(N - 2400, N)]
    k = lags[np.argmax(c[lags])]
    k = k if k < N // 2 else k - N
    return round(k / 8000 * 1000, 1)


res = []
for h, cfg, ass, base, vid in lista:
    r = ms.medir(cfg, ass, vid, h)
    lag = 0.0 if vid == base else atraso_ms(pcm(base), pcm(vid))
    linha = {"video": vid.name, "blocos": r["blocos_medidos"], "erro_medio_ms": r["erro_medio_abs_ms"],
             "erro_max_ms": r["erro_max_abs_ms"], "pct_100ms": r["pct_dentro_100ms"],
             "erro_energia_max_ms": r["erro_energia_max_abs_ms"], "texto_errado": r["blocos_texto_errado"],
             "faladas_sem_legenda": len(r["faladas_sem_legenda"]),
             "quadros_ok": f'{r["quadros"]["aparecem_no_quadro_esperado"]}/{r["quadros"]["eventos_conferidos"]}',
             "voz_vs_base_ms": lag}
    print(json.dumps(linha, ensure_ascii=False), flush=True)
    res.append(linha)
json.dump(res, open(AQUI / "prova_final.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
