# -*- coding: utf-8 -*-
import json, re
WPS = 2.7  # ritmo medio ElevenLabs ES (palavras/s) — estimativa, medir no audio real
def est(t): n = len(re.findall(r"[\wáéíóúñü$.]+", t)); return n, round(n / WPS, 1)

ganchos = [
  {"id": "H1", "angulo": "escassez / Black Friday",
   "fala": "Solo por Black Friday: Yara, Yara Moi y Yara Elixir, los tres juntos en un solo kit. Aprovecha ahora.",
   "manchete_sugerida": "SOLO POR BLACK FRIDAY 🖤",
   "pendencias": ["CONFIRMAR COM A PESSOA: o kit/preço vale só durante a Black Friday? No prod.json o preço $59.900 é o preço normal (compare_at_price vazio). Se não houver condição exclusiva de BF, 'solo por Black Friday' vira afirmação enganosa."]},
  {"id": "H2", "angulo": "elogio / rastro do aroma",
   "fala": "Te recuerdan por el aroma que dejas. Este Black Friday, llévate tres perfumes árabes y deja tu huella donde vayas.",
   "manchete_sugerida": "EL AROMA QUE TODOS RECUERDAN ✨",
   "pendencias": []},
  {"id": "H3", "angulo": "presente / autopresente",
   "fala": "¿Buscas un regalo que sorprenda? O mejor, regálatelo tú: tres perfumes árabes en un kit, a precio Black Friday.",
   "manchete_sugerida": "EL REGALO PERFECTO 🎁",
   "pendencias": ["CONFIRMAR COM A PESSOA: 'a precio Black Friday' pressupõe preço promocional de BF; hoje $59.900 é o preço da página sem 'de/por'."]},
  {"id": "H4", "angulo": "os perfumes árabes que todas perguntam",
   "fala": "Los perfumes árabes que todas me preguntan: Yara, Yara Moi y Yara Elixir. Este Black Friday, juntos.",
   "manchete_sugerida": "LOS PERFUMES ÁRABES QUE TODAS PREGUNTAN 👀",
   "pendencias": ["Fala em 1ª pessoa de consultora fictícia (IA) dizendo que 'todas me preguntan' = depoimento encenado; risco leve de compliance/IA não declarada — decisão da pessoa."]},
]
for g in ganchos:
    g["palavras"], g["seg_estimados"] = est(g["fala"])

corpo = [
  {"bloco": "abertura", "fala": "Mira todo lo que trae este kit.", "takes": "unboxing: mãos abrindo a caixa / mostrando os 3 frascos", "chaves": ["kit"]},
  {"bloco": "Yara", "fala": "Primero, Yara. Dulce, cremosa y femenina.", "takes": "frasco rosa (anel prata) em close", "chaves": ["Yara"]},
  {"bloco": "Yara", "fala": "Abre con orquídea, heliotropo y mandarina, sobre un fondo suave de vainilla y almizcle.", "takes": "borrifando / girando o frasco", "chaves": ["vainilla"]},
  {"bloco": "Yara", "fala": "Perfecta para el día a día, para la pega o para salir a juntarte con amigas.", "takes": "frasco na mão, luz natural", "chaves": ["pega"]},
  {"bloco": "Yara Moi", "fala": "Después, Yara Moi. Floral, luminosa y elegante.", "takes": "frasco branco (anel dourado) saindo da caixa", "chaves": ["Moi"]},
  {"bloco": "Yara Moi", "fala": "Jazmín y durazno al inicio, con un fondo cálido de ámbar y caramelo.", "takes": "close no medalhão dourado", "chaves": ["jazmín"]},
  {"bloco": "Yara Moi", "fala": "Ideal para una cita o una ocasión especial.", "takes": "frasco ao lado dos outros dois", "chaves": ["cita"]},
  {"bloco": "Yara Elixir", "fala": "Y Yara Elixir. Intensa, golosa y envolvente.", "takes": "frasco rosa-salmão (anel rosé) em close", "chaves": ["Elixir"]},
  {"bloco": "Yara Elixir", "fala": "Frutilla y grosella negra que terminan en caramelo, vainilla y ámbar.", "takes": "borrifando no pulso", "chaves": ["frutilla"]},
  {"bloco": "Yara Elixir", "fala": "Para la noche, cuando quieres que se note que llegaste.", "takes": "os 3 frascos lado a lado", "chaves": ["noche"]},
  {"bloco": "fecho", "fala": "Cada frasco trae cien mililitros: un aroma para cada momento.", "takes": "mãos segurando os 3", "chaves": ["cien"]},
]
for c in corpo:
    c["palavras"], c["seg_estimados"] = est(c["fala"])

cta = {"fala": "Llévate los tres por cincuenta y nueve mil novecientos pesos, con envío gratis. Haz tu pedido ahora y paga solamente cuando lo recibas.",
       "fala_curta": "Los tres por cincuenta y nueve mil novecientos, con envío gratis. Pide ahora y paga al recibir.",
       "chaves": ["tres", "gratis", "pedido", "recibas"],
       "palavra_seta": "pedido",
       "pendencias": ["Sem 'aprovechando el Black Friday' de propósito: o BF fica no visual (selo/cartão). Se a pessoa confirmar condição exclusiva de BF, dá para voltar ao 'Puedes llevarte los tres... aprovechando esta promoción de Black Friday' do vencedor.",
                      "Preço por extenso para o TTS; na legenda corrigir para '$59.900'."]}
cta["palavras"], cta["seg_estimados"] = est(cta["fala"])
cta["palavras_curta"], cta["seg_estimados_curta"] = est(cta["fala_curta"])

texto_anuncio = {
  "primary_text": "🖤 BLACK FRIDAY: los 3 perfumes árabes del momento en un solo kit\n\nYara · Yara Moi · Yara Elixir — Lattafa, 100 ml cada uno\n\n🌸 Yara: dulce y cremoso, para el día a día\n🤍 Yara Moi: floral y elegante, para una cita o una ocasión especial\n🍓 Yara Elixir: intenso y goloso, para la noche\n\n💰 Kit completo: $59.900\n📦 Envío GRATIS\n💳 Pago contra entrega: pagas al recibir\n\n👇 Pide el tuyo aquí",
  "headlines": ["Black Friday: Kit 3 Perfumes Yara", "3 perfumes árabes · Pagas al recibir", "Kit Yara a $59.900 · Envío gratis"],
  "cta_botao": "SHOP_NOW (Comprar)",
  "link": "https://chileverificada.com/products/kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml",
  "pendencias": ["O vencedor dizia 'Envío GRATIS en todo Chile'; aqui ficou só 'Envío GRATIS' até confirmar cobertura nacional.",
                 "Garantia de 90 dias aparece na imagem do produto e no body_html; não usei no texto. Pode entrar se a pessoa confirmar."]
}

total = sum(c["seg_estimados"] for c in corpo)
rot = {"produto": "Kit 3 Perfumes Árabes Mujer | Yara + Yara Moi + Yara Elixir Lattafa 100ml",
       "loja": "chileverificada.com", "preco_clp": 59900, "compare_at_price": None, "estoque": "não informado (inventory_management null)",
       "mercado": "Chile (ES-CL)", "frente": "COD", "tema": "Black Friday", "publico": "mulheres",
       "estrutura": "gancho consultora IA (Seedance 8 s) → corpo narrado ElevenLabs sobre unboxing (mãos) → CTA",
       "ritmo_estimado_palavras_s": WPS,
       "ganchos": ganchos, "corpo": corpo, "corpo_seg_estimados": round(total, 1),
       "corpo_texto_tts": " ".join(c["fala"] for c in corpo), "cta": cta,
       "texto_anuncio": texto_anuncio,
       "notas_fontes": "ver roteiro.md (Notas olfativas)"}
json.dump(rot, open(r"C:\Users\PICHAU\Downloads\YARA-CL\preprod\roteiro.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for g in ganchos: print(g["id"], g["palavras"], g["seg_estimados"])
print("corpo", sum(c["palavras"] for c in corpo), total, "cta", cta["palavras"], cta["seg_estimados"], cta["palavras_curta"], cta["seg_estimados_curta"])
