# Contexto completo do trabalho (para outro Claude continuar)

Atualizado em 06/10/2026. Este arquivo resume tudo o que foi feito e como trabalhar com a pessoa. Leia também `CLAUDE.md` (raiz do projeto) e `kit-edicao-criativos/CLAUDE.md` antes de executar qualquer coisa.

## 1. Quem é a pessoa e o que ela faz
Gestora de tráfego pago e produtora de criativos do **Grupo Chegou**, com três frentes (nunca misturar regras, métricas ou linguagem entre elas):
- **Dropshipping COD** (pagamento na entrega) — Chile, Colômbia, México, Guatemala, Equador, Romênia.
- **Infoprodutos** (VSL + quiz + upsell) — Onda Tesla 2.0, Glúteos Brasileños, Oração de San Benito.
- **X1 After-Pay** — nutracêutico vendido 1-a-1 por WhatsApp no Brasil, público 50+.

O dia a dia aqui é **produzir criativos de vídeo em lote** (adaptar, traduzir, variar) com agentes em paralelo.

## 2. Regras de trabalho (obrigatórias)
- **Nunca leia nem imprima chaves.** ElevenLabs em `kit-edicao-criativos/.env`; Vmake em `skills/vmake-skill/scripts/.env`. Os scripts carregam sozinhos.
- **Só pare para confirmar** antes de gastar dinheiro real (API paga) ou fazer algo destrutivo. O resto, siga direto. Nunca pergunte "quer que eu continue?".
- **Orçamento sempre com:** custo em US$ + tempo médio + opção paga mais rápida, lado a lado.
- **Processos longos:** mostrar progresso `[k/N]`, % e tempo restante.
- **Toda entrega:** abrir o vídeo/pasta (`Start-Process`) e dar link clicável (usar os atalhos `entregas-*`).
- **Resolução:** origem 360p → entregar 720x1280 (upscale 2x). 1080 só para vencedores ou origem alta.
- **Download:** sempre na maior qualidade disponível (≥720p). Na Biblioteca do Meta, pegar o `video_hd_url` dos dados da página (o player entrega 360p); deduplicar por md5.
- **Nunca inventar** dados, especificações, preços, ofertas ou resultados. Na dúvida, "precisa de revisão manual".
- **Narração mínima** entre ferramentas (VS Code): uma linha no começo e resumo no fim.
- **Voz:**
  - Criativos de **marca própria** (ex.: Mayaverra → Lymphoria): clonar o narrador original no ElevenLabs está autorizado sempre; reutilizar clones existentes.
  - Criativos de **criadores de terceiros** (ex.: Wyze): **a pessoa escolhe por lote/vídeo**. Padrão (B1): não clonar, voz de catálogo, rosto refeito com avatar HeyGen próprio + takes sem rosto. Mesmo criador (B2): permitido quando a pessoa confirma que o criador autorizou uso de imagem e voz → clone da voz + lipsync no vídeo original, com a autorização registrada no relatório. Perguntar no estudo do lote.
- **Pessoa dorme e pede produção noturna:** trabalhar sozinho, checar a cada ~25 min se algo travou, corrigir, e entregar relatório no fim.
- Global (`~/.claude/CLAUDE.md`): plano e abordagens antes de código, TDD, code review crítico no fim, entregar tudo de uma vez.

## 3. Ferramentas e MCPs
- **Kit de edição:** `kit-edicao-criativos/ferramentas/` (Python 3.12, ffmpeg 9 no PATH, Windows). Rodar com `PYTHONIOENCODING=utf-8` no Bash.
- **Skills do projeto** (`.claude/skills/`, fonte de verdade; cópia em `kit-edicao-criativos/.claude/skills/`): `editar-criativo`, `gerar-midia-ia`, `revisar-criativo`, **`traduzir-criativo`**, **`adaptar-marca`**, `organizacao-de-arquivos`, `clonar-loja-ecommerce`, `consultor-de-cases`, `vmake-skill`. Empacotar para o claude.ai: `python ferramentas/empacotar-skills.py <nomes>`.
- **MCPs usados:** Flora (Kling O1 Edit, US$ 0,706/clipe), HeyGen (avatares; plano Pro, ~9.000 créditos premium que zeram todo dia 30; ~15 créditos por vídeo de ~50 s), ElevenLabs (via kit), Google Drive (não sobe arquivo grande), winninghunter/dropkiller (pesquisa de anúncios).
- **Drive:** o MCP não sobe vídeos de 20+ MB. `rclone` está instalado (winget) mas **não autorizado**; a pessoa prefere pastas locais por enquanto.
- **Local:** faster-whisper (small, CPU int8, `cpu_threads=4` com outros agentes rodando), demucs (`--two-stems=vocals`, CPU — torch sem CUDA), Real-ESRGAN (GPU RTX 4070) via `upscale_video.py`.

### Scripts-chave do kit (todos com `--help`)
| Script | Uso |
|---|---|
| `montar_ad.py receita.json` | montagem final (legenda, hook, selo, setas, compressão, `_frames.jpg`) |
| `tts_elevenlabs.py` / `clonar_voz.py` | narração com alinhamento / clone de voz |
| `upscale_video.py --escala 2` | 360p → 720p (rodar em **fila única de GPU**) |
| `encaixar_edit.py` / `substituir_trechos.py` | encaixar take do Kling no tempo original |
| `trocar_rotulo_faixa.py --auto/--caixa/--seguir` | trocar nome no rótulo **sem IA** (grátis) |
| `gerar_variacao.py banco/fundo/montar` | matriz gancho × corpo |
| `montar_corpo_avatar.py plano.json` | avatar HeyGen + B-roll sem rosto |
| `preparar_corpo_traducao.py prep.json` | tradução: faixa sobre legenda, título novo, cortes, desfoque, troca de áudio |
| `revisar_ad.py video --idioma es --idioma-residual en --proibidos "..."` | revisão automática (sai com código 1 se achar problema) |
| `desfocar_regioes.py`, `trocar_texto_tela.py`, `trocar_trecho_audio.py`, `finalizar.py` | utilitários |

### Armadilhas que já custaram retrabalho
- Kling recusa clipe < 3 s: cortar com `-ss -t` + `tpad=stop_mode=clone`; nunca `-frames:v`.
- **Kling em personagem Pixar/3D troca o rosto** → usar `trocar_rotulo_faixa.py` ou colar só a região do produto.
- `encaixar_edit.py` copiava pixel branco do quadro inteiro (rótulo antigo voltava) → **corrigido** (só faixa 0,62–0,90 da altura). Conferir rótulo com zoom 3x; a folha de contato não mostra.
- `montar_ad_rapido.py`: corpo concatenado com `-c copy` misturando HeyGen + vídeo original (metadados de cor diferentes) fazia o ffmpeg reiniciar o filtro → buraco de 3 s no áudio e setas sumindo → **corrigido** (`-reinit_filter 0`). `silencedetect` não pega; checar salto de pts.
- Whisper e OCR juntos disputam CPU (até 10× mais lento): rodar em sequência.
- Faixa sobre texto queimado precisa de alpha ≥ 250.
- Em 720p com faixa no rodapé: selo `y≈1110`, setas `cta.y≈1490`.
- Revisão por subagente (whisper + folha + zoom) pega defeitos que a `_frames.jpg` não mostra.

## 4. Lotes feitos (status em 06/10/2026)

### Lymphoria (marca própria; antes Mayaverra) — COD Chile/Guatemala/Equador
- Oferta: envío gratis · pagas al recibir · 90 días de garantía · **sem preço no vídeo**. Produto: 4 hierbas (galio, stillingia, trébol rojo, fresno espinoso), gotas bajo la lengua cada mañana, sabe a miel.
- **Lote antigo** `Downloads/LHYMPORIA AD 01-20/` (atalho `08-entregas/cod_lymphoria-cl/`) — ADs entregues + **13 versões v2 corrigidas** do bug do encaixar em `lymphoria/_v2_corrigidos/` (ADs 03, 09, 22, 13, 01 ainda têm restos dentro da faixa da legenda; um "v3" grátis resolve).
- **Lote Drenagem** `Downloads/DRENAGEM-LATAM/` (atalho `08-entregas/cod_drenagem-latam/`) — **55 criativos entregues**: 20 ADs (10 longos + 10 curtos: 01, 03, 04, 05, 18, 20, 21, 24, 25, 30), 5 UGC HeyGen, 30 variações (10 ganchos × corpos AD20/AD05/AD30). Custo real ~US$ 24,75. Pasta numerada 01–55 + índice + relatório + **textos de anúncio** (`00 - TEXTOS-ANUNCIOS-LYMPHORIA-LATAM.txt`) em `DRENAGEM-LATAM/PARA-O-DRIVE/`.
- Referência Flora (frasco neutro): Lymphoria = nó n59, projeto `prj_ns7cvmdqvtn37b53wfnywhr9q58fjte1`. Linfarele (Itália) = nó n6, projeto `prj_ns7f6r91ft66e7jpk9d8mrapph8fn291`.

### Podadora Inalámbrica Césped Ruedas — COD Chile
- `Downloads/PODADORA-CL/` (atalho `08-entregas/cod_podadora-cl/`): 4 traduzidos EN→ES + 8 variações + 11 estáticos. Oferta: pago contra entrega, despacho gratis, 90 días de garantía.
- Drive: os 12 vídeos já estão na pasta "PODADORA CL - Criativos (ES-CL)"; faltam as imagens 13–23 e o txt de textos (arrastar de `PODADORA-CL/PARA-O-DRIVE/`).

### Wyze Solar Cam Pan 2K — LATAM (a pessoa vende a **Wyze original**, marca pode ficar)
- `Downloads/WYZ-CAMARA-LATAM/` (atalho `08-entregas/cod_wyze-latam/`): **16 ADs ES entregues** (vídeo 17 excluído). Custo ~US$ 2,40 + ~115 créditos HeyGen.
- Só especificações oficiais (wyze.com): 2K, 360°/70°, visão noturna a cor, refletor, sirene 105 dB, áudio 2 vias, IP65, 1 h de sol/dia, cabo 3 m, microSD, sem assinatura obrigatória.
- Rostos de criador (01, 06, 12, 14, 16) refeitos com avatar "WYZE Review Latino 35" (id `430f346689b68545f1adbea9f186bd83`).
- **Sem selo de oferta**: a pessoa ainda não confirmou a oferta. Cada `producao/_trabalho/adNN/receita_com_selo.json` está pronta para renderizar.

### TikTok EN (Tarte CC Serum + Sungboon Toner) — **adiado pela pessoa**
- Estudo pronto em `Downloads/TIKTOK-EN-30-criativos/ESTUDO-EDICOES.md`. Não iniciar sem pedido.

## 5. Pendências abertas
1. **Wyze:** confirmar a oferta (COD / frete / garantia) → renderizar selo nos 16 (grátis, ~20 min); AD 02 saiu com voz feminina (trocar por masculina ~US$ 0,05 se pedir); gerar textos de anúncio se pedir.
2. **Lymphoria v3:** limpar restos de rótulo dentro da faixa da legenda nos ADs v2 03, 09, 22, 13, 01 (teste em `_v2_trabalho/teste_v3/`).
3. **Drive:** subir só quando a pessoa pedir (ela prefere local agora).
4. **vmake-skill** falha no empacotador (`name` diverge da pasta) — não mexido.
5. Limite: Fable bateu o teto de 50% da cota semanal (reseta 07/10 12h); Opus/Sonnet continuam.

## 6. Como produzir um lote novo (resumo do método)
1. Copiar originais para `<LOTE>/originais/NN.mp4` + `indice-arquivos.csv` (nunca mexer nos originais em Downloads).
2. Estudo com agentes em paralelo (transcrição + folhas de contato) → `ESTUDO-*.md` com o que não serve, classificação, orçamento (custo + tempo + opção rápida) e perguntas de bloqueio.
3. Após aprovação: `producao/_trabalho/BRIEFING-AGENTES.md` único → 1 agente por 1–2 vídeos, em background. Upscale em fila única de GPU.
4. Seguir a skill do caso: **`adaptar-marca`** (marca própria) ou **`traduzir-criativo`** (outro idioma/mercado); montagem por `editar-criativo`; mídia IA por `gerar-midia-ia`; revisão por `revisar-criativo` + `revisar_ad.py`.
5. Repassar descobertas entre agentes por `SendMessage` (ex.: truque grátis, bug).
6. Entrega: `producao/00-RELATORIO-PRODUCAO.md` (custo real × orçado, decisões, "para você olhar"), pasta numerada, textos de anúncio, memória do projeto atualizada, abrir a pasta e dar o link.
