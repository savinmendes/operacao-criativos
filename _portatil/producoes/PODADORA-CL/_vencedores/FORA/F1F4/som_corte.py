# -*- coding: utf-8 -*-
"""Som sintético (local, grátis) de cortadora elétrica de disco + grama sendo cortada, para o gancho ASMR F1.
As tomadas originais não têm som de corte aproveitável (classificador AST: só música/resíduo de voz no no_vocals).
  python som_corte.py saida.wav  (linha do tempo em SEG abaixo, em segundos do gancho)
"""
import sys

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
rng = np.random.default_rng(11)

# (ini, fim, tipo, nível do motor, densidade de corte)  tipo: ambiente | arranque | corte | lento
SEG = [
    (0.00, 0.55, "ambiente", 0.0, 0.0),
    (0.55, 1.00, "arranque", 0.8, 0.0),
    (1.00, 2.40, "corte", 0.95, 1.0),     # o03 close: máquina entrando no mato alto
    (2.40, 3.40, "corte", 1.00, 0.9),     # POV no mato alto
    (3.40, 4.50, "corte", 0.95, 1.0),     # o03 close
    (4.50, 5.50, "corte", 0.70, 0.7),     # plano aberto (mais longe)
    (5.50, 7.233, "lento", 0.85, 0.8),    # câmera lenta 0,5x
]


def bp(x, lo, hi, o=4):
    return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lp(x, f, o=4):
    return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x)


def hp(x, f, o=4):
    return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x)


def suave(x, seg):
    n = max(1, int(seg * SR))
    k = np.hanning(n * 2 + 1)
    k /= k.sum()
    return np.convolve(x, k, mode="same")


def curva(T, pontos):
    t = np.arange(int(T * SR)) / SR
    xs, ys = zip(*pontos)
    return np.interp(t, xs, ys)


def comb_ruido(n, f0, fb=0.98):
    """Ruído com filtro pente na frequência de passagem das lâminas: zumbido elétrico 'vivo' (não senoidal)."""
    from scipy.signal import lfilter
    D = int(round(SR / f0))
    a = np.zeros(D + 1)
    a[0], a[D] = 1, -fb
    x = lfilter([1], a, rng.standard_normal(n))
    x = bp(x, 200, 7500, 2)
    rough = np.clip(1 + 8 * 0.3 * sosfilt(butter(2, 30, fs=SR, output="sos"), rng.standard_normal(n)), 0.2, 3)
    return x / (np.std(x) + 1e-9) * rough


def motor(carga, lento, arr, nivel):
    """Mistura versões do zumbido: livre (95 Hz), com carga (88 Hz), câmera lenta (47 Hz) e arranque (30/60 Hz)."""
    n = len(nivel)
    t = np.arange(n) / SR
    v_livre, v_carga, v_lento = comb_ruido(n, 95), comb_ruido(n, 88), lp(comb_ruido(n, 47), 2500)
    v30, v60 = comb_ruido(n, 30), comb_ruido(n, 60)
    whine = 0.15 * np.sin(2 * np.pi * 4200 * t + 0.5 * np.sin(2 * np.pi * 0.8 * t)) * 3
    normal = (1 - carga) * v_livre + carga * v_carga + whine * (1 - lento)
    # arranque: arr vai de 0 a 1 -> 30 Hz -> 60 Hz -> 95 Hz
    w30 = np.clip(1 - np.abs(arr - 0.15) / 0.3, 0, 1) * (arr > 0)
    w60 = np.clip(1 - np.abs(arr - 0.5) / 0.35, 0, 1) * (arr > 0)
    wn = np.where(arr > 0, np.clip((arr - 0.5) / 0.5, 0, 1), 1.0)
    m = w30 * v30 + w60 * v60 + wn * ((1 - lento) * normal + lento * v_lento * 1.3)
    return lp(m, 7500) * nivel * 0.12


def grama(dens, lento, n):
    """Grãos curtos de ruído agudo (talos sendo cortados) + 'swish' médio. dens/lento por amostra."""
    out = np.zeros(n)
    t = 0.0
    T = n / SR
    while t < T:
        i = int(t * SR)
        d = dens[min(i, n - 1)]
        sl = lento[min(i, n - 1)]
        taxa = 25 + 140 * d
        if sl > 0.5:
            taxa *= 0.5
        t += rng.exponential(1 / taxa)
        if d < 0.02:
            continue
        dur = rng.uniform(0.004, 0.022) * (2 if sl > 0.5 else 1)
        L = int(dur * SR)
        j = int(t * SR)
        if j + L >= n:
            break
        g = rng.standard_normal(L) * np.exp(-np.linspace(0, 6, L)) * rng.uniform(0.3, 1.0) * d
        out[j:j + L] += g
    cr = hp(out, 2200) * 0.55 + bp(out, 700, 2200) * 0.35
    return cr


def main(saida):
    T = SEG[-1][1]
    n = int(T * SR)
    t = np.arange(n) / SR
    nivel = np.zeros(n)
    dens = np.zeros(n)
    lento = np.zeros(n)
    f0 = np.full(n, 128.0)
    for ini, fim, tipo, nv, ds in SEG:
        a, b = int(ini * SR), min(n, int(fim * SR))
        nivel[a:b] = nv
        dens[a:b] = ds
        if tipo == "lento":
            lento[a:b] = 1
        if tipo == "arranque":
            x = (t[a:b] - ini) / (fim - ini)
            f0[a:b] = 128 * (1 - np.exp(-4 * x)) / (1 - np.exp(-4)) + 4
            nivel[a:b] = nv * np.clip(x * 1.3, 0, 1)
    # variação por grama: a cada ~0,25 s a carga varia (mato mais denso), com micro-oscilações
    carga = suave(np.repeat(rng.uniform(0.4, 1.0, int(T * 4) + 2), SR // 4)[:n], 0.08) * dens
    dens = suave(dens * (0.6 + 0.4 * carga), 0.03)
    arr = np.zeros(n)
    for ini, fim, tipo, nv, ds in SEG:
        if tipo == "arranque":
            a, b = int(ini * SR), int(fim * SR)
            arr[a:b] = np.linspace(0.001, 1, b - a)
    nivel = suave(nivel, 0.04)
    lento_s = suave(lento, 0.05)
    m = motor(np.clip(carga, 0, 1), lento_s, arr, nivel)
    g = grama(dens, lento, n)
    g = np.where(lento > 0.5, lp(g, 4500) * 1.2, g)
    # transição para a câmera lenta: 'whoosh' grave descendo
    w = np.zeros(n)
    a = int(5.30 * SR)
    L = int(0.9 * SR)
    env = np.concatenate([np.linspace(0, 1, int(0.2 * SR)) ** 2, np.exp(-np.linspace(0, 4, L - int(0.2 * SR)))])
    w[a:a + L] = lp(rng.standard_normal(L), 900) * env * 0.5
    amb = lp(rng.standard_normal(n), 1200) * 0.006     # ambiente externo bem baixo
    clique = np.zeros(n)
    c0 = int(0.55 * SR)
    clique[c0:c0 + 600] = hp(rng.standard_normal(600), 1500) * np.exp(-np.linspace(0, 8, 600)) * 0.25
    mono = m + g * 0.9 + w + amb + clique
    # estéreo: motor no centro, grama/ambiente levemente descorrelacionados
    g2 = grama(dens, lento, n)
    g2 = np.where(lento > 0.5, lp(g2, 4500) * 1.2, g2)
    esq = mono
    dir_ = m + g2 * 0.9 + w + lp(rng.standard_normal(n), 1200) * 0.006 + clique
    st = np.stack([esq, dir_], 1)
    # fades: entra suave e sai em 0,2 s (emenda no corpo)
    fo = int(0.2 * SR)
    st[-fo:] *= np.linspace(1, 0, fo)[:, None]
    st /= np.max(np.abs(st)) + 1e-9
    st *= 0.7
    sf.write(saida, st.astype(np.float32), SR, subtype="PCM_16")
    print("ok", saida, round(T, 3), "s")


if __name__ == "__main__":
    main(sys.argv[1])
