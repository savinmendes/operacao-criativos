# -*- coding: utf-8 -*-
"""Confere se um trecho com lipsync (HeyGen, Kling, Sync etc.) realmente mexeu a boca e se ela acompanha o áudio novo.

Tudo local e grátis (MediaPipe Face Landmarker + ffmpeg):
0. Rosto de quem fala: com vários rostos no plano (ex.: mulher falando e Jesus calado atrás), acha os rostos em
   5 quadros, mede cada um e fica com o que mudou em relação ao --original (o lipsync só refaz quem fala);
   se nenhum mudou claramente, fica com o que mais acompanha a energia do áudio novo. --rosto x,y,w,h força.
1. "A boca mudou?" (precisa de --original, o trecho de entrada alinhado no tempo): em cada quadro mede a diferença
   de pixels na região da boca entre saída e original e compara com a diferença numa região de controle
   (testa/entre os olhos), que só tem ruído de compressão. "mudou" = fração de quadros em que a boca ficou
   claramente mais diferente que o controle. Lipsync que devolveu a boca original dá "mudou" perto de 0.
2. "A boca acompanha o áudio novo?" — critério principal: ÍNDICE DE PAUSA = abertura média da boca nas pausas
   da voz nova (≥ 8 quadros abaixo de pico−30 dB, sem 2 quadros de cada borda) / abertura média na fala.
   Boca sincronizada fecha nas pausas: ≤ 0,60 APROVADO; 0,60–0,75 AVISO (conferir a olho); > 0,75 REPROVADO
   (boca sem sincronia com o áudio novo fica em 0,86–1,0). Sem pausa suficiente no trecho, cai no teste antigo de
   correlação abertura x energia (±200 ms) e sai no máximo AVISO.

Uso:
  python checar_lipsync.py saida.mp4 --audio-novo es.mp3 --original pt.mp4
  python checar_lipsync.py saida.mp4 --audio-novo es.mp3 --original pt.mp4 --rosto 320,280,400,440
  python checar_lipsync.py saida.mp4 --audio-novo es.mp3 --original pt.mp4 --audio-original pt.wav
  python checar_lipsync.py saida.mp4                     # só os testes de áudio, com o áudio da própria saída
  --sem-audio-original: não extrai o áudio do --original (ex.: original já vem com o áudio novo embutido).
  --rosto x,y,w,h: região (px do vídeo) onde está o rosto de quem fala; a ferramenta só segue o rosto ali dentro.
Imprime as métricas e APROVADO/AVISO/REPROVADO com o motivo; sai com código 1 se reprovar (2 se não achou rosto).
O modelo face_landmarker.task (3,7 MB, Google, grátis) é baixado na 1ª vez para ~/.cache/kit-edicao/.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

import cv2
import numpy as np

# ---- limiares (calibrados no lote ad11; tabela em tests/test_checar_lipsync.py) ----
# Boca x original separa os grupos com folga: ruins mudou=0,00 e corr. abertura >= 0,98; bons mudou >= 0,97 e
# corr. abertura <= 0,39. Boca x áudio é sinal fraco (0,2-0,5 mesmo quando certo; a dublagem segue as pausas
# do original, então o envelope novo e o antigo se parecem): só reprova o caso grosseiro.
MIN_MUDOU = 0.30        # fração mínima de quadros com a boca diferente do original
MAX_CORR_BOCA_ORIG = 0.80  # abertura da boca da saída quase idêntica à do original = não mudou
MIN_CORR_NOVO = 0.15    # correlação mínima abertura da boca x energia do áudio novo (ruins sem original: 0,03-0,05)
MARGEM_ORIGINAL = 0.10  # reprova se corr_original > corr_novo + margem (bom mais "colado": +0,08; AD 01 s08 ruim: +0,15)
MIN_CBO_NAO_MUDOU = 0.50  # "não mudou" só reprova se a abertura também segue a do original (ruins AD 11: 0,98-0,99;
                          # AD 13 j1, barba: pixels no nível do ruído mas corr. -0,08 -> AVISO)
MIN_Q_PAUSA_CONFIAVEL = 20  # com menos quadros de pausa (< ~0,67 s) a amostra é pequena: só reprova acima de
MAX_PAUSA_POUCA = 0.90      # este índice (AD 13 w09: 14 q, 0,79 bom; AD 01 s02: 13 q, 1,15 ruim)
# Índice de pausa (critério principal; calibração AD 11/AD 01/AD 13 em tests/test_checar_lipsync.py e no CLAUDE.md)
MAX_PAUSA_OK = 0.60     # AD 11 aprovado 0,38; AD 13 0,56
MAX_PAUSA_AVISO = 0.75  # AD 01 reprovado 0,86; boca sem sincronia (original x voz nova) 0,86-1,0
FAIXA_FALA_DB = 30      # "fala" = energia acima de pico - 30 dB
MIN_Q_PAUSA_RUN = 8     # pausa = corrida de >= 8 quadros (~0,27 s) sem fala
BORDA_PAUSA = 2         # descarta 2 quadros de cada ponta da pausa (boca fechando/abrindo)
MIN_Q_PAUSA = 6         # quadros de pausa mínimos para calcular o índice
MIN_MUDANCA_ROSTO = 2.0  # escolha do rosto: dif. boca / dif. controle a partir da qual o rosto "mudou"
FATOR_RUIDO = 2.0       # boca "diferente" no quadro = dif_boca > FATOR_RUIDO * dif_controle + PISO_RUIDO
PISO_RUIDO = 1.0        # níveis de cinza (0-255)
TOL_MS = 200            # tolerância de atraso entre boca e áudio

MODELO_URL = ("https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/"
              "face_landmarker.task")
MODELO = Path.home() / ".cache" / "kit-edicao" / "face_landmarker.task"

LABIOS_EXT = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185]
PARES_ABERTURA = [(13, 14), (82, 87), (312, 317)]   # lábio de cima x de baixo (parte interna)
ROSTO_LARG = (234, 454)
TESTA = [9, 151, 8, 107, 336]


# ---------------------------------------------------------------- sinais (puros)
def corr_lag(a, b, max_lag: int) -> tuple[float, int]:
    """Maior correlação de Pearson entre a e b com deslocamento em [-max_lag, max_lag] (NaN ignorado).
    lag > 0 = b atrasado em relação a a."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    best, best_lag = -1.0, 0
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            x, y = a[: n - lag], b[lag:]
        else:
            x, y = a[-lag:], b[: n + lag]
        m = np.isfinite(x) & np.isfinite(y)
        if m.sum() < 10:
            continue
        x, y = x[m], y[m]
        if x.std() < 1e-9 or y.std() < 1e-9:
            continue
        c = float(np.corrcoef(x, y)[0, 1])
        if c > best:
            best, best_lag = c, lag
    return best, best_lag


def envelope(x: np.ndarray, sr: int, fps: float, n: int) -> np.ndarray:
    """Energia (dB) do áudio por quadro de vídeo: RMS numa janela de 2 quadros centrada em cada quadro."""
    hop = sr / fps
    win = int(2 * hop)
    out = np.empty(n)
    for k in range(n):
        c = int((k + 0.5) * hop)
        s = x[max(0, c - win // 2): c + win // 2]
        rms = float(np.sqrt(np.mean(s.astype(np.float64) ** 2))) if len(s) else 0.0
        out[k] = 20 * np.log10(rms + 1e-4)
    return out


def mascara_fala(env_db, faixa_db: float = FAIXA_FALA_DB) -> np.ndarray:
    """Quadros com fala: energia acima de (pico - faixa_db)."""
    env_db = np.asarray(env_db, dtype=float)
    return env_db > np.nanmax(env_db) - faixa_db


def mascara_pausas(fala, min_q: int = MIN_Q_PAUSA_RUN, borda: int = BORDA_PAUSA) -> np.ndarray:
    """Quadros de pausa: corridas de >= min_q quadros sem fala, sem `borda` quadros em cada ponta."""
    fala = np.asarray(fala, dtype=bool)
    p = np.zeros(len(fala), dtype=bool)
    run = 0
    for i, v in enumerate(list(fala) + [True]):
        if not v:
            run += 1
            continue
        if run >= min_q and run > 2 * borda:
            p[i - run + borda: i - borda] = True
        run = 0
    return p


def somas_pausa(ab, env_db) -> dict:
    """Somas para o índice de pausa (permitem juntar vários trechos): abertura nas pausas e na fala."""
    ab = np.asarray(ab, dtype=float)
    env_db = np.asarray(env_db, dtype=float)
    n = min(len(ab), len(env_db))
    ab, env_db = ab[:n], env_db[:n]
    fala = mascara_fala(env_db) if n else np.zeros(0, bool)
    pausa = mascara_pausas(fala)
    ok = np.isfinite(ab)
    mp, mf = pausa & ok, fala & ok
    return {"soma_ab_pausa": float(ab[mp].sum()), "n_pausa": int(mp.sum()),
            "soma_ab_fala": float(ab[mf].sum()), "n_fala": int(mf.sum())}


def indice_agregado(itens) -> float | None:
    """Índice de pausa de vários trechos juntos (média dos quadros de todos eles). None se faltar pausa/fala."""
    sp = sum(i.get("soma_ab_pausa", 0.0) or 0.0 for i in itens)
    npau = sum(i.get("n_pausa", 0) or 0 for i in itens)
    sf = sum(i.get("soma_ab_fala", 0.0) or 0.0 for i in itens)
    nf = sum(i.get("n_fala", 0) or 0 for i in itens)
    if npau < MIN_Q_PAUSA or nf < 10 or sf <= 0:
        return None
    return (sp / npau) / (sf / nf)


def indice_pausa(ab, env_db) -> tuple[float | None, int]:
    """(abertura média nas pausas da voz / abertura média na fala, quadros de pausa). None se pausa insuficiente."""
    s = somas_pausa(ab, env_db)
    return indice_agregado([s]), s["n_pausa"]


def classificar_pausa(idx: float | None) -> str | None:
    if idx is None:
        return None
    if idx <= MAX_PAUSA_OK + 1e-9:
        return "APROVADO"
    if idx <= MAX_PAUSA_AVISO + 1e-9:
        return "AVISO"
    return "REPROVADO"


def veredito(m: dict) -> tuple[str, str]:
    """m: mudou (0-1 ou None), corr_boca_original (opcional), indice_pausa (ou None), corr_novo, corr_original.
    Devolve (status, motivo), status em APROVADO / AVISO / REPROVADO."""
    mudou, cn, co = m.get("mudou"), m.get("corr_novo"), m.get("corr_original")
    cbo, ip = m.get("corr_boca_original"), m.get("indice_pausa")
    nq = m.get("n_pausa")
    partes, aviso = [], False
    if mudou is not None and mudou < MIN_MUDOU:
        if cbo is None or cbo >= MIN_CBO_NAO_MUDOU:
            return "REPROVADO", (f"a boca NÃO mudou em relação ao original (só {mudou:.0%} dos quadros diferentes; "
                                 f"mínimo {MIN_MUDOU:.0%}): o lipsync devolveu a boca original")
        partes.append(f"aviso: pixels da boca quase iguais aos do original ({mudou:.0%} dos quadros), mas a abertura "
                      f"não segue a do original (corr. {cbo:.2f}); barba/rosto pequeno? confira a boca na folha")
        aviso = True
    if cbo is not None and cbo > MAX_CORR_BOCA_ORIG:
        return "REPROVADO", (f"a boca abre e fecha igual à do original (corr. {cbo:.2f} > {MAX_CORR_BOCA_ORIG}): "
                             f"o lipsync devolveu a boca original")
    if mudou is not None and not aviso:
        partes.append(f"boca mudou em {mudou:.0%} dos quadros")
    if ip is not None:
        st = classificar_pausa(ip)
        pouca = nq is not None and nq < MIN_Q_PAUSA_CONFIAVEL
        if st == "REPROVADO" and pouca and ip <= MAX_PAUSA_POUCA:
            st = "AVISO"
        if st == "REPROVADO":
            return "REPROVADO", (f"a boca não acompanha o áudio novo: fica aberta nas pausas da voz (índice de "
                                 f"pausa {ip:.2f} > {MAX_PAUSA_POUCA if pouca else MAX_PAUSA_AVISO}; "
                                 f"sincronizado <= {MAX_PAUSA_OK})")
        partes.append(f"fecha nas pausas da voz nova (índice de pausa {ip:.2f})")
        if st == "AVISO":
            partes.append(f"aviso: índice de pausa acima de {MAX_PAUSA_OK}"
                          + (f" com só {nq} quadros de pausa" if pouca else "")
                          + "; confira a boca nas pausas da voz na folha de contato")
        if aviso:
            st = "AVISO"
        return st, "; ".join(partes)
    # sem pausa suficiente: só a correlação (sinal fraco), no máximo AVISO
    if cn is None or cn < MIN_CORR_NOVO:
        return "REPROVADO", (f"a boca não acompanha o áudio novo (correlação {cn if cn is None else round(cn, 2)}; "
                             f"mínimo {MIN_CORR_NOVO}; trecho sem pausa para o índice de pausa)")
    if co is not None and co > cn + MARGEM_ORIGINAL:
        return "REPROVADO", f"a boca acompanha mais o áudio original ({co:.2f}) do que o novo ({cn:.2f})"
    partes.append(f"correlação com o áudio novo {cn:.2f}" + (f" (original {co:.2f})" if co is not None else ""))
    partes.append("aviso: trecho sem pausa na voz nova, o índice de pausa não foi calculado; confira a boca "
                  "na folha de contato")
    return "AVISO", "; ".join(partes)


def ler_rosto(s) -> tuple[int, int, int, int]:
    """'x,y,w,h' (ou 'x;y;w;h') -> (x, y, w, h) em px do vídeo."""
    if isinstance(s, (tuple, list)):
        v = list(s)
    else:
        v = [c.strip() for c in re.split(r"[;,\s]+", str(s).strip()) if c.strip()]
    if len(v) != 4:
        raise ValueError(f"--rosto precisa de 4 números x,y,w,h: {s!r}")
    try:
        x, y, w, h = (int(round(float(c))) for c in v)
    except (TypeError, ValueError):
        raise ValueError(f"--rosto inválido: {s!r}") from None
    if x < 0 or y < 0 or w < 8 or h < 8:
        raise ValueError(f"--rosto inválido (x,y >= 0; w,h >= 8): {s!r}")
    return x, y, w, h


def agrupar_rostos(deteccoes) -> list[dict]:
    """deteccoes: por quadro amostrado, lista de caixas (x, y, w, h). Junta a mesma pessoa entre quadros.
    Devolve [{'caixa': (x, y, w, h) mediana, 'n': nº de quadros em que apareceu}], do mais visto ao menos."""
    grupos: list[dict] = []
    for q, caixas in enumerate(deteccoes):
        for (x, y, w, h) in caixas:
            cx, cy, t = x + w / 2, y + h / 2, max(w, h)
            melhor, dist = None, None
            for g in grupos:
                gx, gy, gt = np.median(g["cx"]), np.median(g["cy"]), np.median(g["t"])
                d = float(np.hypot(cx - gx, cy - gy))
                if d < 0.5 * max(t, gt) and 0.5 <= t / gt <= 2.0 and (dist is None or d < dist):
                    melhor, dist = g, d
            if melhor is None:
                melhor = {"cx": [], "cy": [], "t": [], "c": [], "q": set()}
                grupos.append(melhor)
            melhor["cx"].append(cx)
            melhor["cy"].append(cy)
            melhor["t"].append(t)
            melhor["c"].append((x, y, w, h))
            melhor["q"].add(q)
    out = []
    for g in grupos:
        c = np.median(np.array(g["c"], dtype=float), axis=0)
        out.append({"caixa": tuple(int(round(v)) for v in c), "n": len(g["q"])})
    out.sort(key=lambda g: (-g["n"], -g["caixa"][2]))
    return out


def escolher_rosto(cands: list[dict]) -> int:
    """cands: [{'mudanca': dif.boca/dif.controle x original (ou None), 'corr_audio', 'atividade'}].
    Quem fala é o rosto que o lipsync refez (mudou claramente e bem mais que os outros); se nenhum se destaca,
    o que mais acompanha a energia do áudio novo; empate: o que mais mexe a boca."""
    def num(v, padrao=-1.0):
        return padrao if v is None or not np.isfinite(v) else float(v)
    mud = [num(c.get("mudanca"), 0.0) for c in cands]
    ordem = sorted(range(len(cands)), key=lambda i: -mud[i])
    if ordem and mud[ordem[0]] >= MIN_MUDANCA_ROSTO and (
            len(ordem) == 1 or mud[ordem[0]] >= 1.5 * max(mud[ordem[1]], 1e-9)):
        return ordem[0]
    return max(range(len(cands)), key=lambda i: (round(num(cands[i].get("corr_audio")), 2),
                                                 num(cands[i].get("atividade"))))


# ---------------------------------------------------------------- mídia
def ler_audio(path: str | Path, sr: int = 16000) -> np.ndarray | None:
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", str(sr),
                        "-f", "f32le", "-"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        return None
    return np.frombuffer(p.stdout, dtype=np.float32)


def _modelo() -> Path:
    if not MODELO.exists():
        MODELO.parent.mkdir(parents=True, exist_ok=True)
        print(f"baixando modelo do MediaPipe para {MODELO} ...", flush=True)
        urllib.request.urlretrieve(MODELO_URL, MODELO)
    return MODELO


class Rastreador:
    """Face Landmarker em recortes ao redor do rosto. O detector do MediaPipe só acha rosto grande no quadro
    (curta distância); rosto pequeno (plano aberto) é procurado em janelas e depois seguido pelo recorte."""

    def __init__(self, alvo=None, multi=False):
        """alvo: (x, y, w, h) = só segue o rosto cujo centro está nessa região (o mais perto do centro dela).
        multi: detecta até 4 rostos por recorte (para achar_rostos)."""
        os.environ.setdefault("GLOG_minloglevel", "2")      # cala o log do MediaPipe
        os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
        import mediapipe as mp
        from mediapipe.tasks import python as mpt
        from mediapipe.tasks.python import vision
        self.mp = mp
        n = 4 if (alvo is not None or multi) else 1
        opts = vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=str(_modelo())),
                                            running_mode=vision.RunningMode.IMAGE, num_faces=n)
        self.det = vision.FaceLandmarker.create_from_options(opts)
        self.alvo = tuple(alvo) if alvo is not None else None
        self.centro = None         # centro do rosto seguido no último quadro (modo alvo)
        self.caixa = None          # (x0, y0, lado) do recorte atual
        self.espera = 0            # quadros até tentar a busca de novo depois de falhar

    def _todos(self, fr, x0, y0, lado):
        h, w = fr.shape[:2]
        x0, y0 = max(0, int(x0)), max(0, int(y0))
        x1, y1 = min(w, x0 + int(lado)), min(h, y0 + int(lado))
        rec = np.ascontiguousarray(cv2.cvtColor(fr[y0:y1, x0:x1], cv2.COLOR_BGR2RGB))
        if rec.shape[0] < 32 or rec.shape[1] < 32:
            return []
        r = self.det.detect(self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=rec))
        rh, rw = rec.shape[:2]
        return [np.array([(x0 + p.x * rw, y0 + p.y * rh) for p in f]) for f in (r.face_landmarks or [])]

    def _no_alvo(self, pts) -> bool:
        x, y, w, h = self.alvo
        cx, cy = pts.mean(0)
        return x <= cx <= x + w and y <= cy <= y + h

    def _detectar(self, fr, x0, y0, lado):
        fs = self._todos(fr, x0, y0, lado)
        if self.alvo is not None:
            fs = [p for p in fs if self._no_alvo(p)]
            if not fs:
                return None
            x, y, w, h = self.alvo
            ref = self.centro if self.centro is not None else np.array([x + w / 2, y + h / 2])
            return min(fs, key=lambda p: float(np.linalg.norm(p.mean(0) - ref)))
        return fs[0] if fs else None

    def _buscar_alvo(self, fr):
        x, y, w, h = self.alvo
        H, W = fr.shape[:2]
        cx, cy = x + w / 2, y + h / 2
        for f in (1.0, 1.6, 2.4):
            lado = int(min(min(W, H), max(160, f * max(w, h))))
            x0 = int(np.clip(cx - lado / 2, 0, W - lado))
            y0 = int(np.clip(cy - lado / 2, 0, H - lado))
            p = self._detectar(fr, x0, y0, lado)
            if p is not None:
                return p
        return None

    def todos_rostos(self, fr) -> list[tuple[int, int, int, int]]:
        """Caixas (x, y, w, h) de todos os rostos do quadro (janelas em várias escalas; pode repetir rosto)."""
        h, w = fr.shape[:2]
        out = []
        for lado in (max(w, h), min(w, h), min(w, h) // 2, min(w, h) // 3):
            passo = max(1, lado // 2)
            for y0 in range(0, max(1, h - lado + 1), passo):
                for x0 in range(0, max(1, w - lado + 1), passo):
                    for p in self._todos(fr, x0, y0, lado):
                        (a, b), (c, d) = p.min(0), p.max(0)
                        out.append((int(a), int(b), int(c - a), int(d - b)))
        return out

    def _recentrar(self, pts, shape):
        h, w = shape[:2]
        larg = np.linalg.norm(pts[ROSTO_LARG[0]] - pts[ROSTO_LARG[1]])
        lado = int(min(min(w, h), max(160, 3.0 * larg)))
        cx, cy = pts.mean(0)
        x0 = int(np.clip(cx - lado / 2, 0, w - lado))
        y0 = int(np.clip(cy - lado / 2, 0, h - lado))
        self.caixa = (x0, y0, lado)

    def _buscar(self, fr):
        h, w = fr.shape[:2]
        achados = []
        for lado in (max(w, h), min(w, h), min(w, h) // 2, min(w, h) // 3):
            passo = max(1, lado // 2)
            for y0 in range(0, max(1, h - lado + 1), passo):
                for x0 in range(0, max(1, w - lado + 1), passo):
                    p = self._detectar(fr, x0, y0, lado)
                    if p is not None:
                        achados.append(p)
            if achados:
                break
        if not achados:
            return None
        return max(achados, key=lambda p: np.linalg.norm(p[ROSTO_LARG[0]] - p[ROSTO_LARG[1]]))

    def pontos(self, fr):
        pts = None
        if self.caixa is not None:
            pts = self._detectar(fr, *self.caixa)
        if pts is None:
            if self.espera > 0:
                self.espera -= 1
                return None
            pts = self._buscar_alvo(fr) if self.alvo is not None else self._buscar(fr)
            if pts is None:
                self.caixa, self.espera, self.centro = None, 15, None
                return None
        self._recentrar(pts, fr.shape)
        self.centro = pts.mean(0)
        return pts

    def close(self):
        self.det.close()


def _abertura(pts) -> float:
    larg = np.linalg.norm(pts[ROSTO_LARG[0]] - pts[ROSTO_LARG[1]])
    if larg < 1:
        return np.nan
    return float(np.mean([np.linalg.norm(pts[a] - pts[b]) for a, b in PARES_ABERTURA]) / larg)


def _caixa(pts, idx, margem, shape):
    p = pts[idx]
    x0, y0 = p.min(0)
    x1, y1 = p.max(0)
    mx, my = (x1 - x0) * margem, (y1 - y0) * margem
    h, w = shape[:2]
    return (int(max(0, x0 - mx)), int(max(0, y0 - my)), int(min(w, x1 + mx)), int(min(h, y1 + my)))


def _dif(a, b, cx) -> float:
    x0, y0, x1, y1 = cx
    if x1 - x0 < 4 or y1 - y0 < 4:
        return np.nan
    ga = cv2.GaussianBlur(cv2.cvtColor(a[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY), (5, 5), 0).astype(np.float32)
    gb = cv2.GaussianBlur(cv2.cvtColor(b[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY), (5, 5), 0).astype(np.float32)
    return float(np.mean(np.abs(ga - gb)))


def _caixa_testa(pts, shape):
    """Quadrado entre as sobrancelhas/testa, com lado = 1/4 da largura do rosto."""
    larg = np.linalg.norm(pts[ROSTO_LARG[0]] - pts[ROSTO_LARG[1]])
    c = pts[9]
    s = larg / 8
    h, w = shape[:2]
    return (int(max(0, c[0] - s)), int(max(0, c[1] - s)), int(min(w, c[0] + s)), int(min(h, c[1] + s)))


def series_video(saida: Path, original: Path | None, alvo=None):
    """Por quadro: abertura da boca na saída e no original, dif. de pixels na boca e no controle.
    alvo: (x, y, w, h) = segue só o rosto dessa região (nos dois vídeos)."""
    det_s = Rastreador(alvo=alvo)
    det_o = Rastreador(alvo=alvo) if original else None
    cs = cv2.VideoCapture(str(saida))
    fps = cs.get(cv2.CAP_PROP_FPS) or 30.0
    co = cv2.VideoCapture(str(original)) if original else None
    ab_s, ab_o, d_boca, d_ctrl = [], [], [], []
    while True:
        ok, fs = cs.read()
        if not ok:
            break
        fo = None
        if co is not None:
            ok2, fo = co.read()
            if not ok2:
                break
            if fo.shape != fs.shape:
                fo = cv2.resize(fo, (fs.shape[1], fs.shape[0]))
        ps = det_s.pontos(fs)
        ab_s.append(_abertura(ps) if ps is not None else np.nan)
        if fo is not None:
            po = det_o.pontos(fo)
            ab_o.append(_abertura(po) if po is not None else np.nan)
            ref = po if po is not None else ps
            if ref is not None:
                d_boca.append(_dif(fs, fo, _caixa(ref, LABIOS_EXT, 0.35, fs.shape)))
                d_ctrl.append(_dif(fs, fo, _caixa_testa(ref, fs.shape)))
            else:
                d_boca.append(np.nan)
                d_ctrl.append(np.nan)
    cs.release()
    if co is not None:
        co.release()
    det_s.close()
    if det_o is not None:
        det_o.close()
    return fps, np.array(ab_s), np.array(ab_o), np.array(d_boca), np.array(d_ctrl)


def achar_rostos(video: Path, amostras: int = 5) -> list[dict]:
    """Rostos que aparecem em pelo menos 2 de `amostras` quadros espalhados pelo vídeo (ou o mais visto)."""
    cap = cv2.VideoCapture(str(video))
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    det = Rastreador(multi=True)
    dets = []
    for k in range(amostras):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int((k + 0.5) * max(n, 1) / amostras))
        ok, fr = cap.read()
        if ok:
            dets.append(det.todos_rostos(fr))
    cap.release()
    det.close()
    g = agrupar_rostos(dets)
    fortes = [c for c in g if c["n"] >= 2]
    return fortes or g[:1]


def _expandir(caixa, shape, f=0.5):
    """Região de busca do rosto: a caixa do rosto com f x o tamanho a mais de cada lado (cabe o movimento)."""
    x, y, w, h = caixa
    H, W = shape[:2]
    x0, y0 = max(0, int(x - f * w)), max(0, int(y - f * h))
    x1, y1 = min(W, int(x + w + f * w)), min(H, int(y + h + f * h))
    return x0, y0, x1 - x0, y1 - y0


def _tamanho(video: Path):
    cap = cv2.VideoCapture(str(video))
    shape = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    cap.release()
    return shape


def _tem_audio(path: Path) -> bool:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return bool(r.stdout.strip())


def _mudanca(d_boca, d_ctrl):
    m = np.isfinite(d_boca) & np.isfinite(d_ctrl) if len(d_boca) else np.zeros(0, bool)
    if m.sum() < 10:
        return None
    return float(np.median(d_boca[m]) / max(np.median(d_ctrl[m]), 0.5))


def checar(saida, audio_novo=None, original=None, audio_original=None, rosto=None) -> dict:
    """audio_novo: None = áudio da própria saída. audio_original: None = extrai do original (se tiver áudio);
    False = não usar. rosto: (x, y, w, h) ou 'x,y,w,h' = região do rosto de quem fala (pula a escolha automática).
    Devolve dict com métricas, 'status' (APROVADO/AVISO/REPROVADO), 'aprovado' (status != REPROVADO) e 'motivo'."""
    saida = Path(saida)
    original = Path(original) if original else None
    an = ler_audio(audio_novo if audio_novo else saida)

    # 0) rosto de quem fala
    if rosto is not None:
        caixa = ler_rosto(rosto)
        cands = [{"caixa": caixa, "alvo": caixa}]
        escolha = "forçado (--rosto)"
    else:
        achados = achar_rostos(saida)
        shape = _tamanho(saida)
        if len(achados) <= 1:
            cands = [{"caixa": achados[0]["caixa"] if achados else None, "alvo": None}]
            escolha = "único rosto" if achados else "-"
        else:
            cands = [{"caixa": c["caixa"], "alvo": _expandir(c["caixa"], shape)} for c in achados]
            escolha = None
    for c in cands:
        c["series"] = series_video(saida, original, alvo=c["alvo"])
    if len(cands) > 1:
        for c in cands:
            fps_c, ab_c, _, db_c, dc_c = c["series"]
            c["mudanca"] = _mudanca(db_c, dc_c) if original is not None else None
            c["atividade"] = float(np.nanstd(ab_c)) if np.isfinite(ab_c).sum() >= 10 else None
            c["corr_audio"] = None
            if an is not None and len(an) and np.isfinite(ab_c).mean() >= 0.3:
                c["corr_audio"] = corr_lag(ab_c, envelope(an, 16000, fps_c, len(ab_c)),
                                           max(1, round(TOL_MS / 1000 * fps_c)))[0]
        i = escolher_rosto(cands)
        m = cands[i]["mudanca"]
        escolha = (f"{len(cands)} rostos; escolhido o que "
                   + ("mudou em relação ao original" if m is not None and m >= MIN_MUDANCA_ROSTO
                      else "mais acompanha o áudio novo"))
        cands = [cands[i]] + [c for j, c in enumerate(cands) if j != i]
    esc = cands[0]
    fps, ab_s, ab_o, d_boca, d_ctrl = esc["series"]
    n = len(ab_s)
    r: dict = {"saida": saida.name, "quadros": n, "fps": fps,
               "rosto": float(np.isfinite(ab_s).mean()) if n else 0.0,
               "rosto_caixa": esc["caixa"], "rosto_escolha": escolha,
               "rostos_candidatos": [(c["caixa"], c.get("mudanca"), c.get("corr_audio")) for c in cands]}
    if n == 0 or r["rosto"] < 0.3:
        r.update(status="REPROVADO", aprovado=False, sem_rosto=True,
                 motivo=f"rosto não encontrado (em {r['rosto']:.0%} dos quadros)")
        return r
    lag = max(1, round(TOL_MS / 1000 * fps))

    # 1) a boca mudou?
    r["mudou"] = None
    if original is not None and len(d_boca):
        m = np.isfinite(d_boca) & np.isfinite(d_ctrl)
        if m.sum() >= 10:
            db, dc = d_boca[m], d_ctrl[m]
            r["dif_boca"] = float(np.median(db))
            r["dif_controle"] = float(np.median(dc))
            r["mudou"] = float(np.mean(db > FATOR_RUIDO * dc + PISO_RUIDO))
        r["corr_boca_original"] = corr_lag(ab_s, ab_o, 0)[0] if len(ab_o) else None

    # 2) a boca acompanha o áudio? índice de pausa (principal) + correlação
    r["corr_novo"], r["lag_novo_ms"], r["indice_pausa"] = None, None, None
    r.update(soma_ab_pausa=0.0, n_pausa=0, soma_ab_fala=0.0, n_fala=0)
    if an is not None and len(an):
        env_n = envelope(an, 16000, fps, n)
        c, l = corr_lag(ab_s, env_n, lag)
        r["corr_novo"], r["lag_novo_ms"] = c, round(l * 1000 / fps)
        r.update(somas_pausa(ab_s, env_n))
        r["indice_pausa"] = indice_agregado([r])
    r["corr_original"] = None
    ao = None
    if audio_original is not False:
        if audio_original:
            ao = ler_audio(audio_original)
        elif original is not None and _tem_audio(original):
            ao = ler_audio(original)
    if ao is not None and len(ao):
        r["corr_original"] = corr_lag(ab_s, envelope(ao, 16000, fps, n), lag)[0]

    r["status"], r["motivo"] = veredito(r)
    r["aprovado"] = r["status"] != "REPROVADO"
    return r


def ler_especificacao(s: str) -> list[tuple[str, str | None, str | None, str | None]]:
    """'saida1.mp4:es1.mp3:pt1.mp4:x;y;w;h,saida2.mp4::pt2.mp4' -> [(saida, audio_novo, original, rosto), ...].
    O ':' de letra de unidade (C:\\ ou C:/) não separa campos. O rosto (4º campo, opcional) usa ';' entre os números."""
    out = []
    for item in (x.strip() for x in s.split(",")):
        if not item:
            continue
        campos = [c.strip() or None for c in re.split(r":(?![\\/])", item)]
        campos += [None] * (4 - len(campos))
        out.append(tuple(campos[:4]))
    return out


def formatar(r: dict) -> str:
    def f(x, nd=2):
        return "-" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))
    cx = r.get("rosto_caixa")
    linhas = [f"LIPSYNC: {r['saida']} ({r['quadros']} quadros, rosto em {r['rosto']:.0%}"
              + (f", rosto {','.join(map(str, cx))} [{r.get('rosto_escolha')}]" if cx else "") + ")"]
    if "dif_boca" in r:
        linhas.append(f"  boca x original: dif. boca {f(r['dif_boca'])} | dif. controle {f(r['dif_controle'])} | "
                      f"mudou em {'-' if r['mudou'] is None else format(r['mudou'], '.0%')} dos quadros | "
                      f"corr. abertura saída x original "
                      f"{f(r.get('corr_boca_original'))}")
    if "indice_pausa" in r:
        linhas.append(f"  pausas da voz nova: índice de pausa {f(r.get('indice_pausa'))} "
                      f"({r.get('n_pausa', 0)} quadros de pausa; <= {MAX_PAUSA_OK} aprovado, "
                      f"<= {MAX_PAUSA_AVISO} aviso)")
    linhas.append(f"  boca x áudio: corr. novo {f(r.get('corr_novo'))} (atraso {f(r.get('lag_novo_ms'))} ms) | "
                  f"corr. original {f(r.get('corr_original'))}")
    linhas.append(f"{r.get('status', 'APROVADO' if r['aprovado'] else 'REPROVADO')}: {r['motivo']}")
    return "\n".join(linhas)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("saida", help="vídeo devolvido pelo lipsync")
    ap.add_argument("--audio-novo", default=None, help="áudio novo (padrão: áudio da própria saída)")
    ap.add_argument("--original", default=None, help="trecho original (mesma duração, boca antiga)")
    ap.add_argument("--audio-original", default=None, help="áudio original (padrão: extrai do --original)")
    ap.add_argument("--sem-audio-original", action="store_true", help="não comparar com o áudio original")
    ap.add_argument("--rosto", default=None, help="x,y,w,h: região do rosto de quem fala (px do vídeo)")
    a = ap.parse_args()
    ao = False if a.sem_audio_original else a.audio_original
    try:
        rosto = ler_rosto(a.rosto) if a.rosto else None
    except ValueError as e:
        ap.error(str(e))
    r = checar(a.saida, a.audio_novo, a.original, ao, rosto=rosto)
    print(formatar(r), flush=True)
    sys.exit(0 if r["aprovado"] else (2 if r.get("sem_rosto") else 1))


if __name__ == "__main__":
    main()
