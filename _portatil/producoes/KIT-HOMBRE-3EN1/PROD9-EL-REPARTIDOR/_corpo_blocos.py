ZP = "zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"
segs, t = [], 0.0
# 1 gancho: no hall, a cliente o cheira (fala nativa)
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", 1.2, 3.5, None)], [(T / "V1_gancho.mp4", 1.2, 0, 3.5)], 3.5, SELO))
ali_palavras([("Espera…", 1.34, 2.06), ("¿qué", 2.06, 2.78), ("te", 2.78, 2.9), ("echaste?", 2.9, 3.26)], t); t += 3.5
# 2 selfie na rua (voz Aiden por STS, mesmo tempo)
segs.append(bloco("02_selfie", [(T / "V2_selfie.mp4", 0, 4.95, None)], [(AU / "v2_aiden.mp3", 0, 0, 4.95)], 4.95, SELO))
ali_palavras([("Soy", 0.0, 1.08), ("repartidor,", 1.08, 1.64), ("soltero…", 1.82, 2.82), ("bueno,", 2.86, 3.98), ("era", 4.04, 4.26), ("soltero.", 4.26, 4.82)], t); t += 4.95
# 3 oferta: close nos frascos da imagem do CTA sobre fundo desfocado (zoom lento) + TTS
segs.append(bloco("03_oferta", [(C / "S6_cta.png", 0, 2.3, "split[oa][ob];[oa]boxblur=20:2,eq=brightness=-0.08[obg];[ob]crop=720:330:0:290[ofg];[obg][ofg]overlay=0:475," + ZP + "|SELO")],
                  [(AU / "L4_oferta_c.mp3", 0, 0.1, None)], 2.3))
ali_tts(AU / "L4_oferta_c.alinhamento.json", t + 0.1); t += 2.3
# 4 dia: ela salva o WhatsApp dele (Kling, levemente mais lento) + Armaf
segs.append(bloco("04_dia", [(T / "V3_dia.mp4", 0, 5.3, "setpts=1.06*PTS|SELO"), (UB / "armaf_limpo.mp4", 0, 2.0, None)],
                  [(AU / "L5_dia_c.mp3", 0, 0.15, None)], 7.3))
ali_tts(AU / "L5_dia_c.alinhamento.json", t + 0.15); t += 7.3
# 5 noite: Asad + no bar a mesma mulher o cheira (still) + vão embora de mãos dadas (Kling)
segs.append(bloco("05_noche", [(UB / "asad_limpo.mp4", 0, 2.0, None), (C / "S4a_bar.png", 0, 2.0, ZP + "|SELO"), (T / "V4_noite.mp4", 0, 3.0, "|SELO")],
                  [(AU / "L6_noche_c.mp3", 0, 0.15, None)], 7.0))
ali_tts(AU / "L6_noche_c.alinhamento.json", t + 0.15); t += 7.0
# 6 fim de semana: Cerro San Cristóbal com a polola (still com zoom) + 9PM
segs.append(bloco("06_finde", [(C / "S5_finde.png", 0, 2.0, ZP + "|SELO"), (UB / "9pm_limpo.mp4", 0, 2.9, None)],
                  [(AU / "L7_finde_c.mp3", 0, 0.05, None)], 4.9))
ali_tts(AU / "L7_finde_c.alinhamento.json", t + 0.05); t += 4.9
# 7 CTA: o pack saindo da mochila térmica (still com zoom lento)
ZC = "zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.3':d=1:s=720x1280:fps=30"
segs.append(bloco("07_cta", [(C / "S6_cta.png", 0, 4.6, ZC)], [(AU / "L8_cta_c.mp3", 0, 0.2, None)], 4.6, SELO))
ali_tts(AU / "L8_cta_c.alinhamento.json", t + 0.2); t += 4.6

