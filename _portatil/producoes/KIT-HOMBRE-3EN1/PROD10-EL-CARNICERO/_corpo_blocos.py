ZP = "zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"
segs, t = [], 0.0
# 1 gancho (fala nativa da cliente), começa em 0,8 s do take
G0 = 0.8
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", G0, 4.1, None)], [(T / "V1_gancho.mp4", G0, 0, 4.1)], 4.1, SELO))
ali_palavras([(w, a - G0, b - G0) for w, a, b in [("Deme", 1.84, 2.26), ("un", 2.26, 2.3), ("kilo", 2.3, 2.48), ("de", 2.48, 2.68), ("lomo…", 2.68, 3.0),
              ("¿y", 3.5, 3.76), ("qué", 3.76, 3.94), ("perfume", 3.94, 4.32), ("es", 4.32, 4.5), ("ese?", 4.5, 4.7)]], t); t += 4.1
# 2 selfie (voz Santiago por STS, palavras corrigidas, mesmo tempo)
segs.append(bloco("02_selfie", [(T / "V2_selfie.mp4", 0, 4.1, None)], [(AU / "v2_fix.mp3", 0, 0, 4.1)], 4.1, SELO))
ali_palavras([("Soy", 0.42, 0.6), ("carnicero…", 0.6, 1.4), ("y", 2.08, 2.16), ("ahora", 2.16, 2.36), ("las", 2.36, 2.5), ("clientas", 2.53, 2.9),
              ("vienen", 2.9, 3.1), ("todos", 3.1, 3.42), ("los", 3.42, 3.64), ("días.", 3.64, 3.92)], t); t += 4.1
# 3 oferta: close nos frascos da imagem do CTA sobre o fundo desfocado (zoom lento) + TTS
segs.append(bloco("03_oferta", [(C / "S6_cta.png", 0, 2.6, "split[oa][ob];[oa]boxblur=20:2,eq=brightness=-0.08[obg];[ob]crop=560:360:140:540,scale=720:463[ofg];[obg][ofg]overlay=0:400," + ZP + "|SELO")],
                  [(AU / "L4_oferta_c.mp3", 0, 0.1, None)], 2.6))
ali_tts(AU / "L4_oferta.alinhamento_c.json", t + 0.1); t += 2.6
# 4 dia: Armaf (nome dito) + Kling corte da carne, levemente desacelerado, com a piada sobre a fila
segs.append(bloco("04_dia", [(UB / "armaf_limpo.mp4", 0, 2.0, None), (T / "V3_dia.mp4", 0, 5.6, "setpts=1.12*PTS|SELO")],
                  [(AU / "L5_dia_c.mp3", 0, 0.15, None)], 7.6))
ali_tts(AU / "L5_dia.alinhamento_c.json", t + 0.15); t += 7.6
# 5 noite: Asad + esposa abraça na cozinha
segs.append(bloco("05_noche", [(UB / "asad_limpo.mp4", 0, 2.2, None), (T / "V4_noite.mp4", 0, 3.8, "|SELO")],
                  [(AU / "L6_noche_c.mp3", 0, 0.15, None)], 6.0))
ali_tts(AU / "L6_noche.alinhamento_c.json", t + 0.15); t += 6.0
# 6 fim de semana: asado com os amigos (still com zoom) + 9PM
segs.append(bloco("06_finde", [(C / "S5_finde.png", 0, 1.6, ZP + "|SELO"), (UB / "9pm_limpo.mp4", 0, 2.9, None)],
                  [(AU / "L7_finde_c.mp3", 0, 0.05, None)], 4.5))
ali_tts(AU / "L7_finde.alinhamento_c.json", t + 0.05); t += 4.5
# 7 CTA: pack sobre o balcão (still com zoom lento)
ZC = "zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.56':d=1:s=720x1280:fps=30"
segs.append(bloco("07_cta", [(C / "S6_cta.png", 0, 5.7, ZC)], [(AU / "L8_cta_c.mp3", 0, 0.2, None)], 5.7, SELO))
ali_tts(AU / "L8_cta.alinhamento_c.json", t + 0.2); t += 5.7

