# VSL "Lead 2" San Benito: espanhol para alemão (aprovado com "confirmo" em 19/10/2026)

## Dados de entrada
- **Fonte:** `C:\Users\PICHAU\Downloads\Lead 2.mp4` (somente leitura).
  - 720x960, 30 fps, 42:43.
  - Selo "EN VIVO", contador de visualizações e legenda queimada branca embaixo.
- **Estudo:** `_estudo\`.
  - `transcricao_es.txt` / `.json`: whisper small, com palavras e tempos.
  - `folha_1por_min.jpg`.
- **Avatar:** o padre de óculos com casula verde, que fala ~35 min, é um avatar 100% da pessoa. O lipsync nele está autorizado.

## Decisões da pessoa
| Assunto | Decisão |
|---|---|
| Idioma | Só ALEMÃO, para a Alemanha. Tratamento formal "Sie", tom de padre católico, vocabulário católico alemão correto ("der heilige Benedikt", "Gebet", "Segen" etc.). |
| Papa Francisco, vídeo | CORTAR todos os trechos de vídeo em que ele aparece (entrevista com o Papa, ~min 5–7; confira quadro a quadro). |
| Papa Francisco, na fala | Rezar "pelo Papa" pode ficar. Toda frase que diga que o Papa Francisco ENTREGOU, indicou ou revelou a oração (ex.: 28:19 "el Papa me entregó algunas de las versiones originales", 26:51, 27:54) vira "ein Bischof" ou "die alten Archive des Vatikans", sem nomear o Papa como fonte. |
| Preço | 37 € (pagamento único), no lugar de todo "37 dólares" (31:47, 37:26, 38:47, 41:55). Garantia de 90 dias mantida. |
| FAQ 38:32–38:52 ("mi dinero no está en dólares… conversión") | Vira "Wie kann ich bezahlen?", sem conversão de moeda. |
| Valores da história | 90.000 € (16:48), 49,37 € (17:08), 35.000 € (20:22). |
| Selo | "EN VIVO" vira "LIVE". O contador de visualizações fica. |
| Voz | CLONAR a voz do padre no ElevenLabs. A vaga já foi liberada (a pessoa autorizou apagar "Voz Elon Musk"; a conta está com 159/160). Use áudio limpo do padre (demucs vocals, 2–3 min sem música, sem outras vozes). Nome da voz: "PADRE VSL LEAD2". Não apague nenhuma outra voz. |
| Compliance | Mantenha o teor do original (promessas, história, urgência), sem suavizar, exceto o ponto do Papa. |

## Regras
- Não altere a fonte nem nada fora de `C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\`.
- Cada agente trabalha só na sua subpasta de `_trabalho\`.
- Chave ElevenLabs: `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env`. Não imprima.
- **Antes de produzir:** leia `C:\Users\PICHAU\Downloads\Produtividade com ia\CLAUDE.md`, nas seções de armadilhas de lipsync, cor e chiado.
- **LaMa:**
  - Venv: `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Scripts\python.exe`.
  - Modelo: `...\_trabalho\_lote\lama_base.py`.
- **Receita de chiado:** `C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\RECEITA_LIMPAR_CHIADO.md`.
- **Painel:** `python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa vsl-de-<parte> "<título>" --texto "..."`.
- Não mate processos de outros agentes. Whisper e OCR pesados devem rodar em sequência, não em paralelo.
