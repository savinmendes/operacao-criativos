# -*- coding: utf-8 -*-
"""Fonte dos roteiros DCD7781 (ES-CL, Pre Black Friday, sem preço).
Gera ../roteiros.json (rascunho, sem tempos reais) e ../../voz/_trabalho/voz_cfg.json para gerar_voz.py.
Depois de gerar a voz, rode finalizar_roteiros.py para gravar os tempos reais e o roteiros.md.
"""
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent  # DEWALT-ADS

VOZ_MAESTRO = {"id": "ZuuXsIgssLuaZ8Slz3yX", "nome": "Luis - voz natural latina Chile (catálogo ElevenLabs, masculina)"}
VOZ_21 = {"id": "FgZfF59PvtYIb1ZcysY1", "nome": "DEWALT AD21 narradora (clone, vocals demucs 0-55 s)"}
VOZ_37 = {"id": "aGSKUtsBUESN8lwpt9Zd", "nome": "DEWALT AD37 narrador (clone, vocals demucs 0-72 s)"}
VOZ_41 = {"id": "IlvZL1ylCUSyCP1EAiAM", "nome": "DEWALT AD41 narrador (clone, vocals demucs 0-34,5 s)"}

CTA = "Pídelo hoy y pagas recién cuando te llegue."

# ---------------- A) TRADUÇÕES ----------------
# t = onde a fala começa no vídeo base (s); orig_* = trecho da fala original (PT) que ela substitui
traducoes = [
 {"id": "trad_37", "base": "base_limpa/37.mp4", "ad_origem": "37", "nome": "AD 37 · presentación técnica (estudio, solo manos)",
  "voz": VOZ_37, "duracao_base": 72.3,
  "observacoes": [
   "Fala original citava 1 batería, 0-500 rpm, 65 Nm, trava no gatilho, freio eletrônico, empunhadura emborrachada e capacidades 38/13/13 mm: tudo trocado por claims da ficha.",
   "PENDÊNCIA MONTAGEM: a base_limpa/37 manteve os números '38mm' e '13mm' dos cards de perfuração (madeira/aço/alvenaria). A capacidade de furo NÃO tem fonte oficial (Paris diz madeira 25 mm): cobrir esses números com os títulos ES 'MADERA' / 'METAL' / 'MURO' nas mesmas posições. O '13 mm' do mandril (16-20 s) pode ficar.",
   "Fim estendido com quadro congelado (~3 s) para caber o CTA Pre Black Friday."],
  "segmentos": [
   {"t": 0.0, "orig_ini": 0.0, "orig_fim": 11.0, "texto": "Hola, maestros. Hoy les voy a presentar el kit de taladro percutor y atornillador inalámbrico DeWalt, de veinte volts MAX, con baterías de ion de litio. Vamos a verlo.",
    "titulo": "TALADRO PERCUTOR Y ATORNILLADOR", "amarelo": ["percutor", "atornillador", "DeWalt"]},
   {"t": 11.0, "orig_ini": 11.0, "orig_fim": 16.5, "texto": "Trae cargador, dos baterías de dos amperes hora y una maleta para guardar y llevar todo.",
    "titulo": "2 BATERÍAS 2Ah + CARGADOR + MALETA", "amarelo": ["dos baterías", "maleta"]},
   {"t": 16.5, "orig_ini": 16.5, "orig_fim": 20.5, "texto": "Tiene mandril de ajuste rápido de media pulgada, trece milímetros.",
    "titulo": "MANDRIL 1/2\" · 13 mm", "amarelo": ["ajuste rápido"]},
   {"t": 20.5, "orig_ini": 20.5, "orig_fim": 24.5, "texto": "Así cambias brocas y puntas en segundos, sin necesidad de usar llave.",
    "titulo": None, "amarelo": ["en segundos"]},
   {"t": 24.5, "orig_ini": 24.5, "orig_fim": 26.5, "texto": "Es compacto y bien liviano en la mano.", "titulo": "COMPACTO Y LIVIANO", "amarelo": ["liviano"]},
   {"t": 26.5, "orig_ini": 26.5, "orig_fim": 29.5, "texto": "Viene con motor sin carbones, brushless.", "titulo": "MOTOR SIN CARBONES", "amarelo": ["sin carbones"]},
   {"t": 29.5, "orig_ini": 29.5, "orig_fim": 33.5, "texto": "Tiene dos velocidades mecánicas, con gatillo variable y reversa.",
    "titulo": "2 VELOCIDADES", "amarelo": ["dos velocidades"]},
   {"t": 33.5, "orig_ini": 33.5, "orig_fim": 40.5, "texto": "En la segunda velocidad llega hasta mil setecientas cincuenta revoluciones por minuto, para perforar rápido.",
    "titulo": "HASTA 1.750 RPM", "amarelo": ["mil setecientas cincuenta"]},
   {"t": 40.5, "orig_ini": 40.5, "orig_fim": 47.0, "texto": "Su anillo tiene quince posiciones de torque, para apretar justo cada tornillo sin dañar el material.",
    "titulo": "15 POSICIONES DE TORQUE", "amarelo": ["quince posiciones"]},
   {"t": 47.0, "orig_ini": 47.0, "orig_fim": 50.5, "texto": "Y cada batería tiene su indicador de carga incorporado.", "titulo": "INDICADOR DE CARGA", "amarelo": ["indicador de carga"]},
   {"t": 51.5, "orig_ini": 51.5, "orig_fim": 55.5, "texto": "Con él puedes perforar sin ningún problema en distintos tipos de madera,", "titulo": "MADERA", "amarelo": ["madera"]},
   {"t": 55.5, "orig_ini": 55.5, "orig_fim": 58.5, "texto": "y también en metal, para fierros y estructuras,", "titulo": "METAL", "amarelo": ["metal"]},
   {"t": 58.5, "orig_ini": 58.5, "orig_fim": 61.5, "texto": "y en muro o concreto, usando el modo percutor.", "titulo": "MURO Y CONCRETO (MODO PERCUTOR)", "amarelo": ["muro", "percutor"]},
   {"t": 61.5, "orig_ini": 61.5, "orig_fim": 64.5, "texto": "Tiene luz LED para trabajar en lugares oscuros.", "titulo": "LUZ LED", "amarelo": ["luz LED"]},
   {"t": 64.5, "orig_ini": 64.5, "orig_fim": 71.5, "texto": "Ideal para atornillar, armar muebles, estructuras metálicas y para la mantención de la casa o de la obra.",
    "titulo": None, "amarelo": ["la casa", "la obra"]},
   {"t": 71.6, "orig_ini": None, "orig_fim": None, "texto": "Pre Black Friday: " + CTA,
    "titulo": "PRE BLACK FRIDAY · PAGAS AL RECIBIR", "amarelo": ["Pre Black Friday", "pagas recién"], "extensao": True},
  ]},
 {"id": "trad_21", "base": "base_limpa/21.mp4", "ad_origem": "21", "nome": "AD 21 · versatilidad (kit en la tienda, manos)",
  "voz": VOZ_21, "duracao_base": 57.0,
  "observacoes": ["'Torque de 65 Nm' trocado por 'motor sin carbones + 20V MAX'. 'Concreto' trocado por 'muro'.",
                  "Fecho 'Invista na qualidade' virou o CTA Pre Black Friday no mesmo tempo (47-54 s): não precisa estender o vídeo."],
  "segmentos": [
   {"t": 0.27, "orig_ini": 0.27, "orig_fim": 6.77, "texto": "Si buscas versatilidad, potencia y libertad para perforar y atornillar sin cables, donde sea,",
    "titulo": None, "amarelo": ["versatilidad", "potencia", "sin cables"]},
   {"t": 6.77, "orig_ini": 6.77, "orig_fim": 12.27, "texto": "el kit de taladro percutor y atornillador DeWalt de veinte volts es la elección perfecta.",
    "titulo": None, "amarelo": ["DeWalt", "kit"]},
   {"t": 12.27, "orig_ini": 12.27, "orig_fim": 18.27, "texto": "Como atornillador, regulas el torque con sus quince posiciones, para no dañar el material con el que trabajas",
    "titulo": None, "amarelo": ["quince posiciones"]},
   {"t": 18.27, "orig_ini": 18.27, "orig_fim": 21.27, "texto": "y dejar cada uno de tus tornillos bien apretado y firme.", "titulo": None, "amarelo": ["bien apretado"]},
   {"t": 21.27, "orig_ini": 21.27, "orig_fim": 26.27, "texto": "Su mandril de ajuste rápido te deja cambiar brocas y puntas en un dos por tres,",
    "titulo": None, "amarelo": ["ajuste rápido"]},
   {"t": 26.27, "orig_ini": 26.27, "orig_fim": 28.27, "texto": "y así ahorras harto tiempo en cada pega.", "titulo": None, "amarelo": ["harto tiempo"]},
   {"t": 28.27, "orig_ini": 28.27, "orig_fim": 33.27, "texto": "Con su motor sin carbones, brushless, y su batería de veinte volts MAX,",
    "titulo": None, "amarelo": ["sin carbones", "veinte volts"]},
   {"t": 33.27, "orig_ini": 33.27, "orig_fim": 39.27, "texto": "este DeWalt te da la fuerza que necesitas, en la casa o en la obra, para perforar distintos materiales:",
    "titulo": None, "amarelo": ["fuerza"]},
   {"t": 39.27, "orig_ini": 39.27, "orig_fim": 41.27, "texto": "madera, metal y muro.", "titulo": None, "amarelo": ["madera", "metal", "muro"]},
   {"t": 41.27, "orig_ini": 41.27, "orig_fim": 47.27, "texto": "Y con sus dos velocidades mecánicas, ajustas la potencia según el trabajo que tengas en la mano.",
    "titulo": None, "amarelo": ["dos velocidades"]},
   {"t": 47.27, "orig_ini": 47.27, "orig_fim": 54.27, "texto": "Aprovecha el Pre Black Friday: pídelo hoy, con envío a todo Chile, y pagas recién cuando te llegue a la casa.",
    "titulo": "PRE BLACK FRIDAY", "amarelo": ["Pre Black Friday", "pagas recién", "todo Chile"]},
  ]},
 {"id": "trad_41", "base": "base_limpa/41.mp4", "ad_origem": "41", "nome": "AD 41 · unboxing corto (tienda, guante)",
  "voz": VOZ_41, "duracao_base": 37.5,
  "observacoes": ["'Carregador bivolt' removido (sem fonte). 'Compre agora' virou o CTA Pre Black Friday.",
                  "A fala original de 11,6-22,4 s virou 2 frases: maleta (11,6 s) e bateria + LED (17 s), no tempo da fala original."],
  "segmentos": [
   {"t": 0.0, "orig_ini": 0.0, "orig_fim": 5.97, "texto": "Taladro percutor y atornillador DeWalt.",
    "titulo": "TALADRO PERCUTOR Y ATORNILLADOR DEWALT", "amarelo": ["percutor", "DeWalt"]},
   {"t": 5.97, "orig_ini": 5.97, "orig_fim": 11.61, "texto": "Trae dos baterías de veinte volts MAX, de dos amperes hora, y su cargador,",
    "titulo": "2 BATERÍAS 20V MAX + CARGADOR", "amarelo": ["dos baterías", "cargador"]},
   {"t": 11.61, "orig_ini": 11.61, "orig_fim": 14.0, "texto": "y su maleta dura.", "titulo": "+ MALETA", "amarelo": ["maleta"]},
   {"t": 17.0, "orig_ini": 16.9, "orig_fim": 22.44, "texto": "La batería trae indicador de carga, y el taladro tiene luz LED para ver bien donde trabajas.", "titulo": "INDICADOR DE CARGA + LUZ LED", "amarelo": ["indicador de carga", "luz LED"]},
   {"t": 22.44, "orig_ini": 22.44, "orig_fim": 26.53, "texto": "Quince posiciones de torque, y modo percutor para muro.", "titulo": "15 POSICIONES DE TORQUE", "amarelo": ["quince posiciones", "percutor"]},
   {"t": 26.53, "orig_ini": 26.53, "orig_fim": 28.07, "texto": "Motor sin carbones.", "titulo": "MOTOR SIN CARBONES", "amarelo": ["sin carbones"]},
   {"t": 28.3, "orig_ini": 28.07, "orig_fim": 33.94, "texto": "Pre Black Friday: " + CTA,
    "titulo": "PRE BLACK FRIDAY · PAGAS AL RECIBIR", "amarelo": ["Pre Black Friday", "pagas recién"]},
  ]},
 {"id": "trad_38", "base": "base_limpa/38.mp4", "ad_origem": "38", "nome": "AD 38 · closes en la mano (sin habla en el original)",
  "voz": VOZ_MAESTRO, "duracao_base": 15.0,
  "observacoes": ["Original sem fala: narração nova curta encaixada nos closes (voz maestro).",
                  "Evitar quadro da etiqueta DCD7781 (5-8 s) se ficar legível demais; é o modelo certo, então pode ficar."],
  "segmentos": [
   {"t": 0.15, "orig_ini": 0.1, "orig_fim": 1.9, "texto": "Taladro DeWalt de veinte volts MAX, sin carbones.", "titulo": "DEWALT 20V MAX", "amarelo": ["sin carbones"],
    "take_visual": "0,1-1,9 s close lateral 20V MAX BRUSHLESS"},
   {"t": 2.6, "orig_ini": 2.0, "orig_fim": 7.0, "texto": "Gatillo de velocidad variable y luz LED.", "titulo": "LUZ LED", "amarelo": ["luz LED"],
    "take_visual": "2,0-7,0 s gatilho + mandril girando com LED"},
   {"t": 5.4, "orig_ini": 5.0, "orig_fim": 8.0, "texto": "Batería de dos amperes hora,", "titulo": "BATERÍA 2Ah", "amarelo": ["dos amperes"],
    "take_visual": "5-8 s bateria 2Ah"},
   {"t": 8.2, "orig_ini": 8.0, "orig_fim": 11.8, "texto": "motor brushless, compacto y liviano,", "titulo": "BRUSHLESS", "amarelo": ["brushless"],
    "take_visual": "8-11,8 s traseira BRUSHLESS MOTOR"},
   {"t": 11.9, "orig_ini": 11.9, "orig_fim": 15.0, "texto": "con indicador de carga. Pagas cuando lo recibes.", "titulo": "PAGAS AL RECIBIR", "amarelo": ["Pagas cuando lo recibes"],
    "take_visual": "11,9-15 s bateria com indicador verde"},
  ]},
]

# ---------------- B) CORPOS ----------------
corpos = [
 {"id": "corpo_1", "nome": "Corpo 1 · todo lo que trae el kit", "voz": VOZ_MAESTRO, "alvo_s": "35-45",
  "segmentos": [
   {"texto": "Mira todo lo que trae este kit DeWalt.", "takes": ["caixa_01.mp4", "caixa_03.mp4"], "amarelo": ["todo lo que trae"]},
   {"texto": "Viene en su maleta dura, para llevarlo a cualquier pega.", "takes": ["maleta_02.mp4", "maleta_01.mp4"], "amarelo": ["maleta"]},
   {"texto": "Adentro: el taladro percutor y atornillador,", "takes": ["kit_completo_05.mp4", "kit_completo_09.mp4"], "amarelo": ["percutor", "atornillador"]},
   {"texto": "dos baterías de veinte volts, de dos amperes hora,", "takes": ["bateria_02.mp4"], "amarelo": ["dos baterías"]},
   {"texto": "y su cargador.", "takes": ["kit_completo_06.mp4"], "amarelo": ["cargador"]},
   {"texto": "Mandril de trece milímetros, de ajuste rápido.", "takes": ["mandril_02.mp4"], "amarelo": ["ajuste rápido"]},
   {"texto": "Con el anillo eliges el modo:", "takes": ["anel_06.mp4"], "amarelo": ["modo"]},
   {"texto": "taladro, para madera y metal;", "takes": ["furando_madeira_01.mp4", "furando_madeira_02.mp4"], "amarelo": ["taladro"]},
   {"texto": "percutor, para muro y concreto;", "takes": ["furando_concreto_01.mp4"], "amarelo": ["percutor"]},
   {"texto": "y atornillador, con quince posiciones de torque.", "takes": ["parafusando_madeira_01.mp4", "anel_02.mp4"], "amarelo": ["atornillador", "quince posiciones"]},
   {"texto": "Dos velocidades, hasta mil setecientas cincuenta revoluciones por minuto.", "takes": ["seletor_velocidade_01.mp4"], "amarelo": ["dos velocidades"],
    "titulo": "HASTA 1.750 RPM"},
   {"texto": "Y luz LED, para ver bien donde trabajas.", "tts": "Y luz led, para ver bien donde trabajas.", "takes": ["led_01.mp4"], "amarelo": ["luz LED"]},
   {"texto": "Todo esto, en un solo kit.", "takes": ["kit_completo_07.mp4"], "amarelo": ["un solo kit"]},
   {"texto": "Pre Black Friday: " + CTA + " Envío a todo Chile.", "takes": ["kit_completo_04.mp4"], "amarelo": ["Pre Black Friday", "pagas recién", "todo Chile"],
    "titulo": "PRE BLACK FRIDAY · PAGAS AL RECIBIR"},
  ]},
 {"id": "corpo_2", "nome": "Corpo 2 · pega pesada", "voz": VOZ_MAESTRO, "alvo_s": "35-45",
  "segmentos": [
   {"texto": "Pones el anillo en modo percutor,", "takes": ["anel_04.mp4"], "amarelo": ["modo percutor"]},
   {"texto": "y la broca entra en el muro sin pelear.", "takes": ["furando_concreto_02.mp4"], "amarelo": ["muro"]},
   {"texto": "En madera, pasa limpiecita.", "takes": ["furando_madeira_02.mp4"], "amarelo": ["madera"]},
   {"texto": "Y para atornillar, quince posiciones de torque: aprietas justo, sin pasarte.", "takes": ["parafusando_madeira_02.mp4", "anel_03.mp4"],
    "amarelo": ["quince posiciones"]},
   {"texto": "¿El secreto? Motor sin carbones.", "takes": ["lateral_brushless_01.mp4", "motor_01.mp4"], "amarelo": ["sin carbones"]},
   {"texto": "DeWalt dice que es diecisiete por ciento más eficiente que un motor con carbones.", "takes": ["motor_02.mp4", "motor_03.mp4"],
    "amarelo": ["diecisiete por ciento"], "titulo": "17% MÁS EFICIENTE*", "rodape": "*vs. motor con carbones, según DeWalt"},
   {"texto": "Dos velocidades: fuerza en la primera, rapidez en la segunda.", "takes": ["seletor_velocidade_02.mp4"], "amarelo": ["dos velocidades"]},
   {"texto": "Y trae dos baterías con indicador de carga: mientras una trabaja, la otra se carga.", "takes": ["bateria_04.mp4", "bateria_05.mp4"], "amarelo": ["dos baterías", "indicador de carga"]},
   {"texto": "Compacto y liviano, para trabajar todo el día.", "takes": ["gatilho_01.mp4", "led_03.mp4"], "amarelo": ["liviano"]},
   {"texto": "Aprovecha el Pre Black Friday. " + CTA + " Envío a todo Chile.", "tts": "Aprovecha el Pre Black Friday. Pídelo hoy, y pagas recién cuando te llegue. Envío a todo Chile.", "takes": ["kit_completo_02.mp4", "kit_completo_04.mp4"],
    "amarelo": ["Pre Black Friday", "pagas recién", "todo Chile"], "titulo": "PRE BLACK FRIDAY · PAGAS AL RECIBIR"},
  ]},
]

# ---------------- C) GANCHOS ----------------
ganchos = [
 {"id": "gancho_1_3b", "inspiracao": "AD 19 · las 3B", "texto": "¿Buscas un taladro bueno, bonito y barato?",
  "titulo": "LAS 3B: BUENO, BONITO Y BARATO", "amarelo": ["bueno", "bonito", "barato"], "take": "led_01.mp4",
  "por_que_take": "mandril já girando com LED aceso no 1º quadro", "par_sugerido": "corpo_2",
  "nota": "'barato' sem valor: não citar preço nem desconto."},
 {"id": "gancho_2_debil", "inspiracao": "AD 36 · taladro débil", "texto": "¿Sigues peleando con un taladro débil?",
  "titulo": "¿TU TALADRO NO DA MÁS?", "amarelo": ["taladro débil"], "take": "furando_concreto_01.mp4",
  "por_que_take": "broca entrando na parede desde o 1º quadro", "par_sugerido": "corpo_1 (no corpo, trocar o take da frase 'percutor, para muro y concreto' de furando_concreto_01 para anel_04)",
  "nota": "Não usar furando_concreto_01 e _02 no mesmo vídeo (mesmo plano)."},
 {"id": "gancho_3_pega", "inspiracao": "AD 46 · pega pesada", "texto": "Maestro, este taladro aguanta pega pesada.",
  "titulo": "PARA PEGA PESADA", "amarelo": ["pega pesada"], "take": "furando_madeira_01.mp4",
  "por_que_take": "broca entrando na madeira com cavaco voando (câmera lenta)", "par_sugerido": "corpo_2"},
 {"id": "gancho_4_bf", "inspiracao": "tema Pre Black Friday", "texto": "¡Llegó el Pre Black Friday, maestro!",
  "titulo": "PRE BLACK FRIDAY · DEWALT 20V", "amarelo": ["Pre Black Friday"], "take": "maleta_01.mp4",
  "por_que_take": "maleta abrindo rápido, mostra o kit no fim do take", "par_sugerido": "corpo_2 (corpo_1 já abre a maleta com o mesmo take)"},
 {"id": "gancho_5_kit", "inspiracao": "AD 18 · todo lo que trae el kit", "texto": "Dos baterías, cargador y maleta: todo incluido.",
  "titulo": "KIT COMPLETO: 2 BATERÍAS + CARGADOR + MALETA", "velocidade": 1.08, "amarelo": ["Todo incluido"], "take": "kit_completo_08.mp4",
  "por_que_take": "maleta aberta na obra com taladro + 2 baterias, câmera em movimento", "par_sugerido": "corpo_1",
  "nota": "kit_completo_08 tem marcas de uso (obra): se preferir produto novo, usar bateria_02 (pan nas 2 baterias)."},
]

cfg = {"itens": []}
for t in traducoes:
    cfg["itens"].append({"id": t["id"], "voz_id": t["voz"]["id"], "velocidade": 1.0,
                         "segmentos": [{"t": s["t"], "texto": s["texto"], "tts": s.get("tts"), "velocidade": s.get("velocidade", 1.0),
                                        "orig_ini": s["orig_ini"], "orig_fim": s["orig_fim"]} for s in t["segmentos"]]})
for c in corpos:
    cfg["itens"].append({"id": c["id"], "voz_id": c["voz"]["id"], "velocidade": 1.0,
                         "segmentos": [{"texto": s["texto"], "tts": s.get("tts"), "pausa": s.get("pausa", 0.22)} for s in c["segmentos"]]})
for g in ganchos:
    cfg["itens"].append({"id": g["id"], "voz_id": VOZ_MAESTRO["id"], "velocidade": 1.0, "cauda": 0.15,
                         "segmentos": [{"texto": g["texto"], "tts": g.get("tts"), "velocidade": g.get("velocidade", 1.0)}]})

(RAIZ / "voz" / "_trabalho" / "voz_cfg.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
(AQUI / "fonte.json").write_text(json.dumps({"traducoes": traducoes, "corpos": corpos, "ganchos": ganchos,
                                             "voz_maestro": VOZ_MAESTRO}, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(cfg["itens"]), "itens")
