# -*- coding: utf-8 -*-
"""Gera ROTEIRO_DE_PARA_APROVAR.md e o .txt com o alemao corrido (raiz da pasta VSL-LEAD2-DE)."""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
R = json.load(open(os.path.join(AQUI, "roteiro_de.json"), encoding="utf-8"))
PT = {}
for k in (1, 2):
    p = os.path.join(AQUI, "retro", f"saida_{k}.json")
    if os.path.exists(p): PT.update(json.load(open(p, encoding="utf-8")))
for b in R: b["pt"] = PT.get(b["id"], "")
json.dump(R, open(os.path.join(AQUI, "roteiro_de.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def mm(t): return f"{int(t//60):02d}:{t%60:04.1f}"
mant = [b for b in R if not b.get("cortar")]
wes = sum(len(b["es"].split()) for b in mant); wde = sum(len(b["de"].split()) for b in mant)
fala_es = sum(b["fim_es"] - b["ini_es"] for b in mant) / 60
fala_de = wde / 150
CORTE_INI, CORTE_FIM = 276.4, 403.8
video_es = 42 + 43/60 - (CORTE_FIM - CORTE_INI) / 60
video_de = video_es + (fala_de - fala_es)
cel = lambda s: (s or "").replace("|", "\\|").replace("\n", " ")

topo = f"""# VSL Lead 2 San Benito: roteiro em alemão para aprovar

**Status:** só o roteiro. Nada de voz nem vídeo foi gerado. Aguarda o seu "confirmo" (ou ajustes).

## Resumo

- **Duração estimada:** o original tem 42:43. Sem o corte do Papa, sobram ~{video_es:.1f} min no ritmo espanhol. A fala alemã tem {wde} palavras (o espanhol mantido tem {wes}). A ~150 palavras/min, isso dá **~{fala_de:.1f} min de fala**, contra {fala_es:.1f} min de fala no espanhol. **Vídeo final estimado: ~{video_de:.0f} min.**
- **Blocos:** {len(R)} no total, {len(R)-len(mant)} cortados.

### Trechos cortados
| Trecho | Tempo | O que é |
|---|---|---|
| Corte único | **04:36.4 → 06:43.8** (2 min 07 s) | Começa logo após o "Amén" de 04:36. Inclui o plano de transição do púlpito (04:38–04:47) e o padre apresentando a "mensagem do Papa Francisco" (04:48–05:27). Depois vem o **vídeo do Papa Francisco (05:27.10 → 06:33.87**, troca de cena medida no quadro). Termina no "Gracias, Santo Padre… Amén" (06:34–06:43). A fala retoma em "Hermanos, en los próximos 57 segundos" (06:43.9), emendando no Amen anterior. |

Conferi o vídeo quadro a quadro: o Papa não aparece em nenhum outro trecho. Usei 1 quadro/s entre 04:30 e 07:50 e 1 quadro a cada 5 s no resto do vídeo.

### Mudanças de conteúdo
- **Papa como fonte da oração:**
  - 13:09 (B072–B073): a "carta secreta do Papa Francisco" virou "um velho bispo", guardada "nos antigos arquivos do Vaticano".
  - 26:51 (B144): "só o Papa Francisco autorizava" virou "o guardião dos antigos arquivos do Vaticano".
  - 27:48–28:01 (B149–B150): a "reunião secreta com o Papa Francisco" virou "o bispo que, em Roma, cuida dos antigos arquivos do Vaticano". Ele continua "já muito doente na época e hoje descansando junto ao Pai".
  - 28:19 (B152): "o Papa me entregou" virou "o bispo me entregou".
- **Preço:** 37 dólares virou **37 Euro** em 31:47 (B171), 37:26 (B200), 38:47 (B208) e 41:55 (B230). A garantia de 90 dias foi mantida.
- **FAQ de pagamento** (38:32–39:00, B207–B209): virou "Wie kann ich bezahlen?". Agora diz: página segura, escolha entre as formas de pagamento mostradas, pagamento único de 37 Euro, sem conversão e sem custo escondido, pagamento criptografado. Não citei PayPal, Klarna nem cartão por nome, porque não sei o que o checkout aceita.
- **Valores da história:**
  - 90.000 Euro (16:48)
  - 49 Euro und 37 Cent (17:08)
  - 35.000 Euro (20:22)
  - O salário de 29.700 euros/ano já era em euro e foi mantido.
  - Os valores estão escritos por extenso para a TTS (neunzigtausend etc.).
- **"en español"** (41:15) virou "auf Deutsch".
- **Localização (precisa do seu ok):**
  - Pedidos do chat: San Miguel de Allende virou Dortmund, Cidade do México virou Berlin, Cajamarca/Peru virou uma vila na Baixa Baviera.
  - Nomes do FAQ: Rosa Martínez virou Renate Schneider, Carmen López virou Karin Wagner, Carlos Ramírez virou Klaus Becker, Elena Vargas virou Elena Vogel, Cristian Camilo virou Christian Krämer.
  - Mantive "Padre Juan Méndez" e "Bischof Felipe Santoro". A paróquia virou "Pfarrei St. Benedikt".
- **Transcrição revisada** com whisper medium nos trechos duvidosos:
  - Achei uma fala que o whisper small não tinha pegado, entre ~03:43 e 04:04 (Malaquias 3,10). Ela virou o bloco B019A.
  - Corrigi: "Te cibí" → "Recibí", "uno vispo" → "un obispo", "poso te dice" → "puedo decirte", "confés/sobra" → "con fe/obra" e "No sabías" → "No sabía".

### Pontos que precisam da sua decisão
1. **Intro 00:00–03:25:** quem fala é outro apresentador, de **batina e solidéu brancos (traje papal)**. Não é o Papa Francisco nem o padre de verde. O traje lembra um Papa. Manter esse visual, trocar a imagem ou cortar? E qual voz usar nele (a do padre clonado ou outra)?
2. **Depoimentos 09:44–11:46** (3 pessoas diferentes em vídeo: B047–B063): precisam de 3 vozes próprias e de lipsync em rostos que não são do seu avatar. Opções: dublar com voz clonada + lipsync, legendar em alemão mantendo o áudio original, ou trocar por depoimentos novos. O nome "Maria Fernández" (dito pela própria pessoa no vídeo) foi mantido.
3. **Localização** de lugares e nomes (lista acima): aprovar ou voltar aos originais?
4. **Nomes dos bônus** (B175–B178: „Schutz des Hauses“, „Wohlstands-Protokoll“, „Seelische Heilung“, „Geistliche Disziplin“): precisam bater com a página e a área de membros em alemão.
5. **B226:** o roteiro promete "orientações em alemão" dentro do programa. Confirmar que o material vai existir em alemão.
6. **Corte do Papa:** além do vídeo, cortei a fala do padre que apresenta e agradece o vídeo (04:48–05:27 e 06:34–06:43). Sem o vídeo, essas frases não fazem sentido. Se preferir outro caminho (por exemplo, uma ponte curta nova), me diga.

### Revisão
- Um revisor nativo de alemão (copy de resposta direta + vocabulário católico) leu todo o texto. Ele apontou cerca de 55 ajustes (calques, frases duras, um erro de gramática em B150, repetição de "heiliges Gebet des heiligen Benedikt", números para a TTS), e todos foram aplicados.
- O registro ficou assim: "Sie" com o espectador. As falas citadas de Deus e do bispo para o padre usam "du".
- A retrotradução para o português (coluna PT) foi feita por outro agente, só a partir do alemão, para conferência.

---

## Roteiro por bloco
Linhas ~~riscadas~~ / marcadas **CORTAR** não entram no vídeo.

| # | Tempo (ES) | Espanhol (original) | Alemão | Retrotradução PT | Notas |
|---|---|---|---|---|---|
"""
linhas = []
for b in R:
    c = b.get("cortar")
    tag = "**CORTAR** " if c else ""
    linhas.append(f"| {b['id']} | {mm(b['ini_es'])}–{mm(b['fim_es'])} | {tag}{cel(b['es'])} | {('~~'+cel(b['de'])+'~~') if c else cel(b['de'])} | {cel(b['pt'])} | {cel(b['notas'])} |")
open(os.path.join(RAIZ, "ROTEIRO_DE_PARA_APROVAR.md"), "w", encoding="utf-8").write(topo + "\n".join(linhas) + "\n")
with open(os.path.join(RAIZ, "ROTEIRO_DE_texto_corrido.txt"), "w", encoding="utf-8") as f:
    f.write("VSL Lead 2 San Benito – deutscher Sprechtext (ohne die gestrichenen Papst-Blöcke)\n\n")
    for b in mant: f.write(b["de"] + "\n\n")
print("ok", len(R), "pt faltando:", [b["id"] for b in R if not b["pt"]])
