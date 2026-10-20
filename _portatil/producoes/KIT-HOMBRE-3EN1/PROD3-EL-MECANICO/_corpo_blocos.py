ZP = "zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"
segs, t = [], 0.0
# 1 gancho (fala nativa da cliente)
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", 0, 4.8, None)], [(T / "V1_gancho.mp4", 0, 0, 4.8)], 4.8, SELO))
ali_palavras([("¿Y", 0.7, 1.3), ("mi", 1.3, 1.46), ("auto?", 1.46, 1.76), ("Ya", 1.76, 2.5), ("no", 2.5, 2.62), ("importa…", 2.62, 2.92),
              ("¿qué", 3.9, 4.12), ("te", 4.12, 4.26), ("echaste?", 4.26, 4.64)], t); t += 4.8
# 2 selfie (voz Richard por STS, mesmo tempo)
segs.append(bloco("02_selfie", [(T / "V2_selfie.mp4", 0, 4.7, None)], [(AU / "v2_richard.mp3", 0, 0, 4.7)], 4.7, SELO))
ali_palavras([("Soy", 0.0, 0.54), ("mecánico…", 0.54, 1.08), ("y", 1.08, 1.32), ("ahora", 1.32, 2.0), ("las", 2.0, 2.16), ("clientas", 2.16, 2.62),
              ("vienen", 2.62, 2.84), ("aunque", 2.84, 3.4), ("el", 3.4, 3.6), ("auto", 3.6, 3.84), ("no", 3.84, 4.02), ("tenga", 4.02, 4.28), ("nada.", 4.28, 4.48)], t); t += 4.7
# 3 oferta: close nos frascos da imagem do CTA (zoom lento) + TTS
segs.append(bloco("03_oferta", [(C / "S6_cta.png", 0, 2.3, "crop=405:720:157:540,scale=720:1280," + ZP + "|SELO")],
                  [(AU / "L4_oferta.mp3", 0, 0.1, None)], 2.3))
ali_tts(AU / "L4_oferta.alinhamento.json", t + 0.1); t += 2.3
# 4 dia: debaixo do capô + Armaf
segs.append(bloco("04_dia", [(T / "V3_dia.mp4", 0, 4.6, "|SELO"), (UB / "armaf_limpo.mp4", 0, 1.6, None)],
                  [(AU / "L5_dia.mp3", 0, 0.15, None)], 6.2))
ali_tts(AU / "L5_dia.alinhamento.json", t + 0.15); t += 6.2
# 5 noite: Asad + polola
segs.append(bloco("05_noche", [(UB / "asad_limpo.mp4", 0, 2.0, None), (T / "V4_noite.mp4", 0, 4.4, "|SELO")],
                  [(AU / "L6_noche.mp3", 0, 0.15, None)], 6.4))
ali_tts(AU / "L6_noche.alinhamento.json", t + 0.15); t += 6.4
# 6 fim de semana: carrete (still com zoom) + 9PM
segs.append(bloco("06_finde", [(C / "S5_finde.png", 0, 1.8, ZP + "|SELO"), (UB / "9pm_limpo.mp4", 0, 2.4, None)],
                  [(AU / "L7_finde.mp3", 0, 0.05, None)], 4.2))
ali_tts(AU / "L7_finde.alinhamento.json", t + 0.05); t += 4.2
# 7 CTA: pack sobre o capô (still com zoom lento)
segs.append(bloco("07_cta", [(C / "S6_cta.png", 0, 4.8, ZP)], [(AU / "L8_cta.mp3", 0, 0.2, None)], 4.8, SELO))
ali_tts(AU / "L8_cta.alinhamento.json", t + 0.2); t += 4.8

