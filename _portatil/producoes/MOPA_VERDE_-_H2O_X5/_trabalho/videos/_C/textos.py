# -*- coding: utf-8 -*-
# Gera ES-LATAM/00-TEXTOS-ANUNCIOS-H2O-X5-ES.txt e confere limites (título <=40, TikTok <=100) e termos proibidos.
import re
import unicodedata
from pathlib import Path

BEN = """✅ 5 en 1: limpia pisos, cocina, tapizados, ventanas y más con un solo aparato.
✅ Listo en menos de 30 segundos.
✅ Vapor ajustable con un solo toque, según la superficie.
✅ Ligero: pesa menos de 2,3 kg y es fácil de mover.
✅ Se convierte en vaporizador de mano para lavabos, azulejos y superficies de la cocina.
✅ Elimina olores y deja las superficies frescas y limpias.
✅ Cabezal triangular que entra en esquinas y rincones.
✅ Pago contra entrega: pagas cuando lo recibes.
👇 Haz clic en Más información."""

CINCO = """🧼 ¿Te cansaste de usar 5 limpiadores distintos?
Este limpiador a vapor 5 en 1 limpia pisos, alfombras, ventanas, ropa y más: TODO en uno.
Menos cosas. Más resultados.
✅ Pago contra entrega: pagas cuando lo recibes.
👉 Mejora tu rutina de limpieza: haz clic en Más información."""

UNO = """Lleva tu limpieza a otro nivel con el H2O X5. De los pisos a las ventanas, es la solución para una casa impecable.
✅ Pago contra entrega: pagas cuando lo recibes.
👇 Haz clic en Más información."""

AHORRA55 = """❤️ ¡AHORRA $55 en la mopa a vapor H2O X5!
¡Solo por tiempo limitado!
✅ Pago contra entrega: pagas cuando lo recibes.
👇 Haz clic en Más información."""

AHORRA_MAS = """❤️ ¡AHORRA MÁS en la mopa a vapor H2O X5!
¡Solo por tiempo limitado!
✅ Pago contra entrega: pagas cuando lo recibes.
👇 Haz clic en Más información."""

OFERTA55 = """¿Estabas pensando en el H2O X5?
Ahora tienes una razón más para tenerlo.
Por tiempo limitado, AHORRA $55 en el limpiador a vapor H2O X5.
Un solo limpiador a vapor 5 en 1, ligero, para pisos, juntas, superficies de cocina, alfombras, ventanas, ropa y más, con el poder del vapor y sin químicos de limpieza.
Tu compra tiene garantía de devolución de 30 días y 2 años de garantía.
✅ Pago contra entrega: pagas cuando lo recibes.
👇 No te pierdas el ahorro de $55: haz clic en Más información."""

OCHO = """Quita la suciedad y las manchas de pisos de madera sellada, cerámica, tapetes y alfombras en una sola pasada con el ligero H2O Mop® X5.
✅ 14 millones vendidas en el mundo.
✅ Pago contra entrega: pagas cuando lo recibes.
👇 Haz clic en Más información."""

D_PCE = "Pago contra entrega"
# (id, tipo, arquivo ES, título, texto, descrição, tiktok, observação interna)
A = [
 ("01", "Imagen", "IMAGENS/01 AD - ES.jpg", "H2O X5: limpiador a vapor 5 en 1", UNO, "Pago contra entrega · 3026+ reseñas",
  "H2O X5: limpiador a vapor 5 en 1 para pisos, alfombras, ropa y vidrios. Pago contra entrega 👇", ""),
 ("07", "Video", "VIDEOS/07 AD - ES.mp4", "Elimina el 99% de los gérmenes", BEN, D_PCE,
  "Vapor que elimina el 99% de los gérmenes de tu cocina. H2O X5, pago contra entrega 👇", "Par 4:5 = 60."),
 ("08", "Video", "VIDEOS/08 AD - ES.mp4", "El limpiador a vapor 5 en 1 definitivo", OCHO, D_PCE,
  "5 en 1: pisos, mano, vidrios, alfombras y ropa. 14 millones vendidas. Pago contra entrega 👇",
  "El logo del final incluye la marca THANE (fabricante de la línea H2O)."),
 ("10", "Video", "VIDEOS/10 AD - ES.mp4", "H2O X5: el limpiador a vapor 5 en 1", BEN, D_PCE,
  "Un solo aparato para toda la casa: limpiador a vapor H2O X5 5 en 1. Pago contra entrega 👇",
  "Mismo video que el 15 (cambia solo el audio)."),
 ("11", "Imagen", "IMAGENS/11 AD - ES.jpg", "Elimina el 99% de gérmenes con vapor", BEN, D_PCE,
  "Limpia cada superficie de tu hogar con un solo aparato: H2O X5. Pago contra entrega 👇", ""),
 ("13", "Imagen", "IMAGENS/13 AD - ES.jpg", "5 limpiadores en 1 herramienta potente", CINCO, "Pago contra entrega · 4,000+ reseñas",
  "Solo agrega agua y deja que el vapor limpie. H2O X5 5 en 1, pago contra entrega 👇", ""),
 ("15", "Video", "VIDEOS/15 AD - ES.mp4", "Limpieza a vapor 5 en 1, sin químicos", BEN, D_PCE,
  "Pisos, cocina, ventanas y más con un solo aparato: H2O X5. Pago contra entrega 👇",
  "Mismo video que el 10 (cambia solo el audio)."),
 ("16", "Video", "VIDEOS/16 AD - ES.mp4", "5 limpiadores en 1 herramienta ligera", CINCO, D_PCE,
  "5 herramientas de limpieza en un solo vaporizador ligero: H2O X5. Pago contra entrega 👇", "Par 4:5 del 32."),
 ("17", "Video", "VIDEOS/17 AD - ES.mp4", "Alfombras, pisos, horno y mucho más", BEN, D_PCE,
  "Alfombras, pisos, freidora de aire, horno y microondas con un solo aparato. Pago contra entrega 👇",
  "La canción original (letra en inglés) se mantiene por decisión de la dueña."),
 ("21", "Video", "VIDEOS/21 AD - ES.mp4", "Limpia todo con un solo vaporizador", CINCO, D_PCE,
  "Pisos, cocina, ventanas, alfombras y ropa: ¡todo con UN SOLO aparato! Pago contra entrega 👇", "Par 4:5 del 54."),
 ("24", "Video", "VIDEOS/24 AD - ES.mp4", "Elimina el 99% de los gérmenes en casa", BEN, D_PCE,
  "El 99% de los gérmenes, fuera con vapor. Limpiador H2O X5, pago contra entrega 👇",
  "El video dice \"seguro con niños y mascotas\": no está en la ficha; revisión manual."),
 ("25", "Video", "VIDEOS/25 AD - ES.mp4", "Limpieza profunda en minutos, no horas", BEN, D_PCE,
  "Limpieza profunda en minutos, no en horas, con el H2O X5. Pago contra entrega 👇", ""),
 ("28", "Imagen", "IMAGENS/28 AD - ES.jpg", "¡Ahorra $55 en la mopa a vapor H2O X5!", AHORRA55, D_PCE,
  "¡Ahorra $55 en la mopa a vapor H2O X5! Unidades limitadas. Pago contra entrega 👇",
  "Se quitaron las cuotas (\"3 Easy Payments of $43\") y el envío gratis del original."),
 ("31", "Video", "VIDEOS/31 AD - ES.mp4", "Limpieza rápida que te facilita la vida", CINCO, D_PCE,
  "Limpieza rápida y efectiva que te hace la vida más fácil: H2O X5. Pago contra entrega 👇", "Par 4:5 del 46."),
 ("32", "Video", "VIDEOS/32 AD - ES.mp4", "5 herramientas de limpieza en 1", BEN, D_PCE,
  "5 herramientas de limpieza en un solo vaporizador ligero y potente. Pago contra entrega 👇",
  "Master 9:16 (par 4:5 = 16)."),
 ("33", "Imagen", "IMAGENS/33 AD - ES.jpg", "Una mopa. Toda la casa limpia.", CINCO, "Pago contra entrega · 4,000+ reseñas",
  "Una mopa, toda la casa limpia: 5 modos y vapor potente. Pago contra entrega 👇", ""),
 ("36", "Imagen", "IMAGENS/36 AD - ES.jpg", "Oferta: limpiador a vapor H2O X5", AHORRA_MAS, D_PCE,
  "Oferta en el limpiador a vapor H2O X5. ¡Unidades limitadas! Pago contra entrega 👇",
  "Se quitó el código de descuento del original."),
 ("44", "Video", "VIDEOS/44 AD - ES.mp4", "H2O X5: 5 limpiadores en 1", UNO, "Pago contra entrega · 3026+ reseñas",
  "14 millones vendidos en el mundo. H2O X5, limpiador a vapor 5 en 1. Pago contra entrega 👇",
  "Es la imagen 01 animada (sin sonido)."),
 ("45", "Imagen", "IMAGENS/45 AD - ES.jpg", "Ahorra $55 en el H2O X5", OFERTA55, "Pago contra entrega · Garantía de 2 años",
  "¡Ahorra $55 en el H2O X5! Vapor potente, sin químicos. Pago contra entrega 👇",
  "La imagen 45 dice \"1 AÑO DE GARANTÍA GRATIS\" y \"ENVÍO GRATIS\"; la ficha dice 2 años. Revisión manual."),
 ("46", "Video", "VIDEOS/46 AD - ES.mp4", "Limpieza rápida y efectiva con vapor", BEN, D_PCE,
  "Limpieza rápida y efectiva que ahorra tiempo: H2O X5 5 en 1. Pago contra entrega 👇", "Master 9:16 (par 4:5 = 31)."),
 ("47", "Imagen", "IMAGENS/47 AD - ES.jpg", "1 aparato, 5 soluciones de limpieza", BEN, D_PCE,
  "Un solo aparato, 5 soluciones de limpieza para cada rincón. Pago contra entrega 👇", ""),
 ("54", "Video", "VIDEOS/54 AD - ES.mp4", "Pisos, cocina, ventanas y ropa en 1", BEN, D_PCE,
  "Pisos, cocina, ventanas, alfombras y ropa con UN SOLO aparato: H2O X5. Pago contra entrega 👇",
  "Master 9:16 (par 4:5 = 21)."),
 ("58", "Imagen", "IMAGENS/58 AD - ES.jpg", "Ligera y fácil de mover", CINCO, "Pago contra entrega · 4,000+ reseñas",
  "Ligera y fácil de mover: limpia arriba, abajo y en todas partes. Pago contra entrega 👇", ""),
 ("59", "Imagen", "IMAGENS/59 AD - ES.jpg", "$55 de descuento en el H2O X5", OFERTA55, "Pago contra entrega · Garantía de 2 años",
  "$55 de descuento en el H2O X5: vapor potente, resultados reales. Pago contra entrega 👇", ""),
 ("60", "Video", "VIDEOS/60 AD - ES.mp4", "Desinfecta tu cocina con vapor", CINCO, D_PCE,
  "Vapor que elimina el 99% de los gérmenes de la cocina: H2O X5. Pago contra entrega 👇", "Par 4:5 del 07."),
 ("61", "Imagen", "IMAGENS/61 AD - ES.jpg", "Oferta exclusiva: ahorra $55",
  OFERTA55 + "\n*Según pruebas de laboratorio controladas. La eficacia varía según el tiempo de aplicación y la superficie.",
  "Pago contra entrega · Devolución en 30 días",
  "Oferta exclusiva: ahorra $55 en el limpiador a vapor H2O X5. Pago contra entrega 👇", ""),
 ("62", "Imagen", "IMAGENS/62 AD - ES.jpg", "Oferta por tiempo limitado: H2O X5", AHORRA_MAS, D_PCE,
  "Oferta por tiempo limitado en el limpiador a vapor H2O X5. Pago contra entrega 👇",
  "Se quitó el código de descuento del original."),
]

PROIB = ["fbx5", "usa", "uk", "canada", "ee. uu.", "reino unido", "shop now", "codigo", "cuotas", "envio desde",
         "envio gratis", "hoy", "esta noche", "x5mop", "h2oforyou", "tinyurl", "5lbs", "1 ano", "1-year", "http"]


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


assert len(A) == 27 and len({a[0] for a in A}) == 27
out = ["TEXTOS DE ANUNCIOS H2O X5 - ESPAÑOL NEUTRO LATAM (27 creativos: 15 videos + 12 imágenes)",
       "Fecha: 08/10/2026",
       "Botón (Meta): Más información (LEARN_MORE). TikTok: \"Más información\".",
       "Link de destino: [PENDIENTE: link de la tienda COD de cada país]",
       "Nombres en Meta: conjunto = anuncio = \"AD NN\" (mismo NN del creativo).",
       "Se mantienen las alegaciones de la dueña ($55, 14 millones, 99 %, 30 días de devolución). Garantía según",
       "la ficha oficial: 2 años. Se quitaron envíos desde otros países, cuotas, links extranjeros y códigos de",
       "descuento. Se agregó \"Pago contra entrega\". Las líneas \"Nota interna\" NO se publican.",
       ""]
errs = []
for (n, tipo, arq, tit, txt, desc, tk, obs) in A:
    if len(tit) > 40:
        errs.append(f"{n} título {len(tit)}")
    if len(tk) > 100:
        errs.append(f"{n} tiktok {len(tk)}")
    for campo in (tit, txt, desc, tk):
        for p in PROIB:
            if re.search(r"(?<!\w)" + re.escape(p) + r"(?!\w)", norm(campo)):
                errs.append(f"{n} proibido '{p}'")
    if "pago contra entrega" not in norm(txt + desc):
        errs.append(f"{n} sem PCE")
    out += ["=" * 70, f"AD {n} | {tipo} | ES-LATAM/{arq}", "=" * 70,
            f"Título ({len(tit)}/40): {tit}", "", "Texto principal:", txt, "",
            f"Descripción: {desc}", "Botón: Más información",
            f"TikTok ({len(tk)}/100): {tk}"]
    if obs:
        out.append(f"Nota interna (no publicar): {obs}")
    out.append("")
Path(r"C:\Users\PICHAU\Downloads\MOPA VERDE - H2O X5\ES-LATAM\00-TEXTOS-ANUNCIOS-H2O-X5-ES.txt").write_text(
    "\n".join(out), encoding="utf-8")
print("erros:", errs or "nenhum")
