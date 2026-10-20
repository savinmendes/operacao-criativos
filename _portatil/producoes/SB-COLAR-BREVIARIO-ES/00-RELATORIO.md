# SB Breviario + Collar (Pellorini) — PT → ES LATAM — 14/10/2026

**Vídeo:** `SB-ES_BREVIARIO-COLAR_FICTICIO.mp4` — 1080x1920, 30 fps, 2:19,2 (139,2 s), 53,6 MB, H.264 high + AAC 48 kHz. Volume final −15,2 LUFS, pico −1,9 dBFS.
**Texto do anúncio:** `00-TEXTO-ANUNCIO.txt` (título, texto principal, descrição, versão TikTok; botão "Más información" / LEARN_MORE).
**Trabalho:** `_trabalho\prod\` (scripts, vozes, lipsync, revisão).

## O que foi feito
1. **Áudio:** demucs (vocals / no_vocals). O fundo é o `no_vocals` do original a ~−33 LUFS sob a fala (−15/−17 LUFS), sem nenhuma fala PT por baixo (Whisper residual PT só "traduz" a fala ES; nenhum termo antigo).
2. **Vozes clonadas** (moça e padre, separadas) a partir das vocals do demucs.
   - A ElevenLabs recusou clone novo: **limite de 160/160 vozes da conta**. Não apaguei nenhuma voz.
   - Clonei no **HeyGen** e gerei a fala com o motor ElevenLabs `eleven_multilingual_v2` via HeyGen (`create_speech`, com tempo por palavra). Registro em `kit-edicao-criativos\VOZES-CLONADAS.md`:
     - moça: HeyGen `b345603c7c7a45e4a4bbe485408b8303`
     - padre: HeyGen `8d62d3c189e34dfdbc0b8b060c7471c4` (amostra curta, ~20 s de fala)
   - Roteiro do briefing exatamente como está (31 falas). "8 mil" é falado "ocho mil" e aparece "8 mil" na legenda. Pronúncia de "Breviario" e "San Benito" conferida no Whisper.
   - Ajuste de tempo: velocidade 1,0–1,1x por fala (máx. 1,1), cada fala perto do tempo PT; nada precisou de congelamento. Duração igual à do original (2:19).
3. **Legenda PT queimada** removida com LaMa (GPU, máscara justa, cor fixa bt601). Legenda ES nova no estilo do original (Anton, branco com contorno preto, 1 palavra vermelha por bloco, ~y 1200), pelo tempo exato da fala.
4. **Textos PT de tela trocados:** tarja da TV (21,5–23,2 s), rastreada no zoom do take:
   - "97 mil pessoas saem das dívidas em 24h" → "97 mil personas salen de sus deudas en 24 h" (mantido, compliance = manter)
   - "Oração que está fazendo milagres no mundo" → "Oración que está haciendo milagros en el mundo"
   - "Pessoas estão recebendo milagres da oração de São Bento." → "Personas están recibiendo milagros de la oración de San Benito."
   - A legenda PT borrada embaixo do take da TV ("será que existe" / "mesmo uma oração") foi apagada com LaMa.
5. **Perfil @sagradoverso** (119,2–121,8 s e 135,2–137,2 s) trocado pela gravação da página Pellorini **sem preço** (`_trabalho\pagina\pagina_completa.mp4`): 1º trecho = título "Breviario de Protección de San Benito" + "Tu pedido incluye"; 2º = lista de conteúdo + "La Medalla de San Benito en plata 925". Evitei de propósito os quadros da capa da galeria, porque a **imagem do produto na loja diz "GRIMORIO SAGRADO Y SECRETO"**.
6. **Lipsync** (só rostos; B-roll sem lipsync), 18 trechos recortados no rosto, PT original no vídeo de entrada, ES separado:
   - 17 trechos HeyGen `speed`: todos voltaram com o número exato de quadros, colados só na boca e no queixo.
   - **Gancho (0–5,7 s, m01): o HeyGen devolveu a boca intacta 6 vezes** (3 recortes diferentes, PiP borrado, áudio só-voz, espelhado, 2 metades, até `precision`). Resolvido com **Sync 3 (ElevenLabs, US$0,75)**: a boca muda em 100% dos quadros.
7. **Selo "VIDEO FICTICIO"**: o PNG do lote SB Medalla (`selo_ficticio_mini.png`, 18 px em 1080), no topo à direita, do 1º ao último quadro. Sem setas, conforme o briefing.
8. **Montagem final:** `montar_ad.py`, 1080x1920, `limite_mb` 60. Depois o áudio passou por um limitador (pico −0,8 → −1,9 dBFS), com o vídeo copiado sem recompressão.

## Revisão (`revisar_ad.py` pelo PowerShell + OCR + folhas)
- Decodificação OK; pts do áudio sem saltos; nenhum silêncio > 0,7 s.
- Whisper ES: o texto bate com o roteiro. Whisper residual PT: nenhuma fala antiga.
- **Termos proibidos** (Grimorio, Grimório, sagradoverso, Sagrado Verso, reais, bio, Pix): nenhum.
- **OCR (RapidOCR, 2 q/s, vídeo inteiro):** sem "sagradoverso", sem "R$" ou "$", sem "Grimorio", nenhuma palavra PT na tela.
- **Lipsync, índice de pausa do conjunto (18 trechos): 0,20 → APROVADO** (meta ≤ 0,6).
  - Trechos com pausa medida: m02 0,04 · m10 0,14 · m11 0,16 no recorte · p17 0,36 · p18 0,25 no recorte.
  - Avisos "sem pausa na fala nova" (m04–m08, m12, p15): é fala contínua, a boca muda em 74–100% dos quadros.
  - **m01 (gancho, Sync 3):** índice 1,44, mas medido em só ~14 quadros de pausa (0–0,15 s e 4,84–5,2 s). Na folha a boca articula a fala ES e fica quase fechada na pausa. Vale olhar (abaixo).
  - **p18** ("Tu hora de vencer llegó"): o revisor marca "boca igual ao original", porque a frase ES tem o mesmo ritmo da PT ("Sua hora de vencer chegou", corr. 0,87). No recorte a boca mudou em 100% dos quadros e o índice dá 0,25: falso alarme.
- **"Quadro solto"** em 5,7 / 21,4 / 23,4 / 27,2 / 36,6 s etc.: são as transições de zoom/flash do **próprio original**, mantidas.
- **Folha de contato conferida a olho:** selo pequeno no topo direito em todos os quadros, sem legenda PT, sem @sagradoverso, sem preço, legenda ES legível.

## Custo
- **HeyGen:** saldo 6.825 antes. Agora 6.805 (−20), mas a cobrança do speed atrasa até ~1 h.
  - Estimativa pelo uso: ~99 s de rosto nos 18 trechos + ~34 s nas 6 tentativas do gancho ≈ **125–135 créditos**.
  - Meça de novo daqui a ~1 h. Outros agentes podem estar usando a mesma conta.
- **ElevenLabs:** US$0,75 (Sync 3 no gancho). Os clones IVC recusados (limite) não cobraram. A fala saiu pelo HeyGen (motor ElevenLabs dentro do plano HeyGen), sem cobrança direta na ElevenLabs.
- **Total em dinheiro: ~US$0,75** + créditos HeyGen (já pagos).

## Pendências / para a pessoa olhar
1. **Gancho 0–5,7 s (Sync 3):**
   - Assistir a 30 qps: a boca segue o ES.
   - Em ~1,8 s ("chica") aparece um quadro com os dentes à mostra, típico do "ch", mas confira.
2. **ElevenLabs no limite de 160 vozes:** para clonar lá de novo é preciso liberar espaço. Não apaguei nada; a decisão é da pessoa.
3. **A imagem do produto na loja Pellorini ainda diz "GRIMORIO SAGRADO Y SECRETO"** (capa da galeria). O vídeo evita esses quadros, mas quem clicar vê "Grimorio" na página.
4. **Créditos HeyGen:** medir o saldo final ~1 h depois do último job (o último foi ~00:00 de 15/10).
5. A moça do PiP (0–5,6 s) ficou como no original, só reagindo, sem fala.
6. **Disco:** `_trabalho\prod\` tem os intermediários (base_sem_legenda, base_final, corpo, lipsync etc., ~1,3 GB). Apagar só com o ok da pessoa depois da aprovação.
