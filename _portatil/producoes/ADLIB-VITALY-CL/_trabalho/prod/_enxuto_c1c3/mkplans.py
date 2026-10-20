# -*- coding: utf-8 -*-
import json
from pathlib import Path
A = r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho"
U = r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\_trabalho\ugc\prod"
V12 = r"C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\VIDEOS\12 - Mi Camino al Bienestar - 1313049140654830.mp4"
VIT = r"C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\_trabalho\prod"
T = {0: U + r"\P1_kit3.mp4", 1: U + r"\P2_frasco_miel.mp4", 2: U + r"\V1_gotero_hierbas.mp4", 3: U + r"\V2_frasco_cocina.mp4",
     4: U + r"\V3_frasco_mesa.mp4", 12: A + r"\ad03\flora\t2_edit.mp4", 20: A + r"\ad10\flora\t1_edit.mp4",
     25: A + r"\ad11\flora\t2_edit.mp4", 26: A + r"\ad11\flora\t3_edit.mp4", 27: A + r"\ad11\flora\t4_edit.mp4", 34: A + r"\ad13\flora\t4_edit.mp4",
     35: A + r"\ad13\flora\t5_edit.mp4", 38: A + r"\ad14\flora\t3_edit.mp4", 39: A + r"\ad14\flora\t4_edit.mp4",
     41: A + r"\ad14\flora2\t6_edit.mp4", 43: A + r"\ad16\flora\t2_edit.mp4", 45: A + r"\ad19\flora\t1_edit.mp4",
     47: A + r"\ad19\flora\t3_edit.mp4", 49: A + r"\ad22\flora\t1_edit.mp4", 50: A + r"\ad22\flora\t2_edit.mp4"}
B = lambda n: "../broll/%s.mp4" % n  # noqa
LEGS = dict(f=V12, ss=8.15, ate=8.95, crop="140,150,439,780")     # pernas inchadas POV (8.13-8.97)
SOFA = dict(f=V12, ss=51.95, ate=53.5, crop="170,150,439,780")    # pernas para cima no sofá (51.93-53.53)
MEIA = dict(f=V12, ss=58.65, ate=59.6, crop="140,150,439,780")    # pés com meia rosa (58.63-59.63)
def s(t0, t1, src, **kw):
    d = dict(src) if isinstance(src, dict) else {"f": src}
    d.update(t0=t0, t1=t1, **kw); return d
AV = lambda t0, t1: {"f": "av.mp4", "t0": t0, "t1": t1, "sync": True}  # noqa
planos = {
 "c1a": {"musica": [VIT + r"\V10\sep\htdemucs\orig\no_vocals.wav", 5.0], "segs": [
    AV(0, 1.7), s(1.7, 3.6, B("h_caja_pies"), ss=0.5), s(3.6, 5.7, LEGS), s(5.7, 7.6, B("h_zapato"), ss=2.4),
    AV(7.6, 9.6), s(9.6, 11.4, B("h_masaje"), ss=0.3), AV(11.4, 13.9), s(13.9, 15.3, T[20]), s(15.3, 17.6, T[2]),
    s(17.6, 21.3, T[45]), s(21.3, 24.0, T[43]), s(24.0, 25.5, T[1], ss=0.8), s(25.5, 27.9, T[41]), AV(27.9, 30.0),
    s(30.0, 32.3, SOFA), s(32.3, 35.7, T[38]), s(35.7, 38.9, T[27]), s(38.9, 99, T[12])]},
 "c1b": {"musica": [VIT + r"\V12\sep\htdemucs\orig\no_vocals.wav", 2.0], "segs": [
    s(0, 2.1, B("h_mesera"), ss=0.6), s(2.1, 5.3, B("h_zapato"), ss=0.8), s(5.3, 6.7, LEGS), s(6.7, 9.9, B("h_masaje"), ss=1.0),
    s(9.9, 12.6, B("h_sillon"), ss=0.4), s(12.6, 15.7, SOFA), s(15.7, 17.8, T[49]), s(17.8, 19.6, T[34]),
    s(19.6, 21.4, T[47]), s(21.4, 23.9, T[43]), s(23.9, 25.4, T[35]), s(25.4, 26.6, T[1], ss=1.0), s(26.6, 28.9, T[41]),
    s(28.9, 30.6, MEIA), s(30.6, 33.4, T[12]), s(33.4, 36.5, T[3]), s(36.5, 39.8, T[20]), s(39.8, 99, T[26])]},
 "c3a": {"musica": [VIT + r"\V26\sep\htdemucs\orig\no_vocals.wav", 0.0], "segs": [
    AV(0, 3.3), s(3.3, 5.4, B("h_anillo_no"), ss=0.8), AV(5.4, 8.0), s(8.0, 10.8, B("h_pies_mayor"), ss=0.5), AV(10.8, 12.0),
    s(12.0, 13.1, T[27], ss=0.6), s(13.1, 15.4, T[34]), s(15.4, 19.3, T[45]), AV(19.3, 22.0), s(22.0, 23.7, T[1], ss=0.6),
    s(23.7, 26.6, T[41]), AV(26.6, 28.4), s(28.4, 29.9, B("h_anillo1"), ss=2.9), s(29.9, 32.3, B("h_zapatos_mayor"), ss=0.6),
    s(32.3, 35.9, T[39]), s(35.9, 39.5, T[2]), s(39.5, 99, T[12])]},
 "c3b": {"musica": [r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\_trabalho\ad24\aud\htdemucs\orig\no_vocals.wav", 40.0], "segs": [
    s(0, 2.4, B("h_anillo_no"), ss=0.3), s(2.4, 5.9, B("h_pies_mayor"), ss=0.3), s(5.9, 8.7, B("h_masaje"), ss=0.5),
    s(8.7, 10.8, B("h_ventana"), ss=0.5), s(10.8, 12.6, T[27]), s(12.6, 15.4, T[20]), s(15.4, 17.6, T[2]),
    s(17.6, 19.6, T[47]), s(19.6, 21.9, T[43]), s(21.9, 23.6, T[35]), s(23.6, 25.0, T[1], ss=0.8), s(25.0, 27.9, T[41]),
    s(27.9, 30.5, B("h_anillo1"), ss=2.0), s(30.5, 33.2, B("h_parque"), ss=0.5), s(33.2, 36.8, T[4]), s(36.8, 40.4, T[38]),
    s(40.4, 99, T[35])]},
}
for k, p in planos.items():
    p.update(narr="narr.mp3", cauda=0.7, saida="corpo.mp4")
    json.dump(p, open(Path(k) / "plano.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
