# Briefing técnico: produções de persona dos perfumes no ElevenLabs (aprovado com "confirmo" em 15/10/2026)

O roteiro de cada persona está em `C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\PERSONAS_P2-P10.md`. **Siga o texto à risca.** Falas e piadas não se mudam: se precisar mudar, pare e relate.

A referência pronta é a produção 1 (Maestro), em `C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\PROD1-EL-MAESTRO\`. Leia `montar_corpo.py` e `receita.json` e copie-os para a sua pasta antes de adaptar.

## Decisões da pessoa (não reabrir)
- COD Chile, sem preço e sem domínio.
- Oferta: «Tres perfumes árabes al precio de uno» + «pagas cuando los recibes».
- Tom ousado, sem selo de vídeo fictício.
- Homem chileno comum, nada bonito.
- Uma voz por personagem.
- Sem porta abrindo e sem ninguém entrando ou saindo de veículo.
- Não usar «100 unidades» nem ESSENZALUX.

## Pasta e painel
- **Pasta:** use só `C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\PROD<N>-<NOME>\`, com as subpastas `cenas/`, `takes/`, `audio/` e `_seg/`.
- **Arquivos compartilhados, só leitura** (não modifique):
  - `PROD1-EL-MAESTRO\unbox\armaf_limpo.mp4` (2,0 s), `asad_limpo.mp4` (2,2 s) e `9pm_limpo.mp4` (4,0 s): unboxing em HD já sem legenda;
  - `LOTE-15-10\_trabalho\A\overlay_selo.png`: selo de pagamento na entrega no topo, em 720×1280;
  - `flora\image_n2.png`: os 3 frascos (referência do produto).
- **Painel:** `python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa p<N> "Perfumes P<N> <nome>" --texto "..." --k <k> --n 5`, depois `img p<N> <arquivo>` em cada folha e `fim p<N>` no final.

## Geração: só no ElevenLabs (MCP `mcp__claude_ai_ElevenLabs__*`; carregue pelo ToolSearch)
Crie 1 flow por persona com `creative_create_flow`. Teto: **35 mil créditos por persona**. Use `estimate_only` antes de cada vídeo e anote o gasto em `custos.md`.

1. **Referências.** Suba `image_n2.png` com `creative_create_asset_upload`, depois PUT com curl (Content-Type `image/png`) e `creative_finalize_asset_upload` com `flow_id`.
2. **Imagens.** Crie o nó com `creative_add_flow_node` (node_type `image-generation`, model `gpt-image-2.5-sunburst`, `model_parameters {"aspect_ratio":"9:16","resolution":"1K","quality":"high"}`). Gere com `creative_run_flow_nodes` e `generations_count: 1`.
   - O primeiro é o **retrato do personagem** (rosto, corpo e roupa conforme o roteiro).
   - As outras imagens usam esse retrato como referência (`connect_from`), para manter o mesmo rosto: gancho, selfie (boca fechada, olhando para a lente), dia, noite, fim de semana e CTA (este com o pack de `image_n2` como 2ª referência, frascos IDÊNTICOS e rótulos legíveis).
   - A esposa ou namorada é gerada só por texto, uma pessoa comum e bonita do jeito real.
   - Total: ~7 imagens.
   - Baixe cada imagem (a `content_url` vence em 2 h).
   - Monte uma folha das imagens e **confira o rosto e o pack com zoom** antes de gerar os vídeos.
3. **Vídeos.** Suba as imagens escolhidas como asset (create_asset_upload → PUT → finalize com `flow_id`) e ligue o nó de vídeo a elas pelo `connect_from` (porta `start_frame`).
   - **Gancho** e **selfie**: `bytedance-seedance-v2`, `{"aspect_ratio":"9:16","resolution":"720p","duration_secs":5,"generate_audio":true}` (~9,2 mil créditos cada). No prompt, a fala exata em espanhol chileno, «Only that line, no other words».
   - **Dia** e **noite**: `kling-2.5-turbo`, `{"aspect_ratio":"9:16","duration_secs":5}` (~2,1 mil cada), sem fala.
   - **Fim de semana** e **CTA**: só a imagem, com zoom lento na montagem.
4. **Status.** Consulte com `creative_get_flow_run_status`. Se a resposta for grande demais, ela é salva em arquivo; leia e baixe com Python (`json` + `urllib`), como fez `PROD1-EL-MAESTRO\_baixar_takes.py`. Não gere de novo para "tentar outra vez": cada chamada cobra.
5. **QA dos takes.**
   - Folha a 2 quadros/s.
   - Transcrição com faster-whisper large-v3 na GPU, com `word_timestamps`. Antes, rode `from lib.whisper_local import _registrar_dlls_cuda` de `C:\Users\PICHAU\Downloads\Produtividade com ia\ferramentas\transcritor-youtube`.
   - O Seedance inventa palavras: corte depois da última palavra certa.
   - Refaça no máximo 1 take, e só se houver defeito visível (rosto trocado, mão deformada, produto deformado ou fala errada).

## Voz (chave em `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env`; leia com `dotenv` e **nunca imprima**)
- **Voz do personagem masculino:** só a que está definida para a sua persona, abaixo. A conta está no limite de vozes: não clone e não apague vozes.
- **Selfie:** isole a voz (`/v1/audio-isolation`), passe por speech-to-speech (`/v1/speech-to-speech/{voz}`, `eleven_multilingual_sts_v2`) e use o tempo original.
- **Narrações** (oferta, dia, noite, fim de semana, CTA):
  - TTS `/v1/text-to-speech/{voz}/with-timestamps`, `eleven_multilingual_v2`, `language_code` es, e salve o alinhamento;
  - escreva «Afnan Nine PM» e troque para «9PM» no alinhamento, como no `montar_corpo.py` do P1.
- **Vozes femininas:** as nativas do Seedance.
- **Trilha:** 1 instrumental própria pelo `/v1/music`, com `force_instrumental` e ~40 s. Use um estilo diferente do P1 (cumbia, reggaetón suave, funk latino ou rock pop).
- **Verificação:** transcreva todas as narrações e confira as palavras.

## Montagem (~30–34 s, 720×1280, 30 fps)
Copie e adapte o `montar_corpo.py` do P1. A ordem dos blocos:
1. **Gancho:** take, com a fala nativa.
2. **Selfie:** take, com a voz STS.
3. **Oferta:** close nos frascos da imagem do CTA (zoom lento) + TTS «Tres perfumes árabes al precio de uno.»
4. **Dia:** Kling + `armaf_limpo` + TTS.
5. **Noite:** `asad_limpo` + Kling + TTS.
6. **Fim de semana:** imagem com zoom lento + `9pm_limpo` + TTS.
7. **CTA:** imagem com zoom lento + TTS.

Nas cenas de IA, aplique o `overlay_selo.png`. O unboxing já vem com selo e rodapé.

Depois rode `montar_ad.py` do kit (diretório `kit-edicao-criativos`), com a receita igual à do P1:
- legenda por alinhamento combinado, com chaves amarelas;
- manchete = título do gancho até o fim do gancho;
- cta com a palavra «pídelo» e `y` 1480;
- `resolucao` 720.

Saída: `PROD<N>-<NOME>\PERFUMES-CL_P<N>_<NOME>.mp4` + `_narracion.txt` (roteiro + texto do anúncio ES-CL: título ≤ 40, texto principal com os 3 perfumes e adjetivos, «Envío en 24 horas», «Pagas cuando lo recibes», sem preço).

## Lições da 1ª onda (P3, P5 e P6)
- **Manchete:** a posição y 330 cobriu rostos no gancho. Escolha o `y` olhando o 1º quadro, numa área sem rosto, e confira na folha.
- **Setas do CTA:** em y 1480 elas caíram sobre os rótulos dos frascos. Ponha as setas abaixo dos frascos (confira na imagem do CTA) ou componha o CTA com os frascos mais altos.
- **Oferta:** o close puro em 9:16 corta o Armaf e o 9PM. Use o close dos frascos sobre o fundo desfocado da própria imagem do CTA (como no P3).
- **Kling:** pode inventar movimento (no P6 a micro andou). Confira e corrija sem gerar de novo quando der.
- **Filtro de conteúdo do ElevenLabs:** pode bloquear imagens de cenas com toque. Suavize só até o ponto em que passa e anote no relatório.

## Revisão (obrigatória)
- Rode `python ferramentas/revisar_ad.py <video> --idioma es --proibidos "100 unidades,essenzalux,ahora o nunca" --passo 1.5`. O resultado precisa ser OK.
- Olhe a `_revisao.jpg` inteira: legenda que não cobre o rosto, setas no fim, nenhum quadro estranho.
- Abra o vídeo pronto com `Start-Process`.

## Retorno (curto, em português)
Caminho do vídeo, créditos gastos, voz usada e até 2 pontos de atenção.
