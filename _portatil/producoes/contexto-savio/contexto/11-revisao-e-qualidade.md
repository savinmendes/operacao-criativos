# Revisão e controle de qualidade de criativos

> O que conferir antes de dizer que um vídeo está pronto: revisão automática (`revisar_ad.py`, `finalizar.py`), folhas de contato, revisor independente, checagens manuais e as armadilhas de ambiente (PowerShell × Git Bash, encoding, CPU). Abra no fim de toda produção.

## Contexto de uso

**Regra.** Nenhum criativo é entregue sem passar pela skill `revisar-criativo`. O núcleo é o `revisar_ad.py` do kit, que junta os revisores que os lotes criaram. Ele sai com **código 1** quando acha problema.

**O que o `revisar_ad.py` checa no vídeo inteiro.**
- Decodificação completa, resolução de entrega (9:16 720×1280/1080×1920, 4:5 720×900/1080×1350, 1:1 720×720/1080×1080; com `--formato`, só as do formato), áudio, duração e tamanho.
- Whisper no idioma alvo (`--idioma`), com tempo por segmento, + busca de **termos proibidos** (`--proibidos`; acentos e maiúsculas ignorados; termo com `|`, `[`, `\` ou `(` vira regex; `#` = comentário no .txt).
- Whisper num 2º idioma (`--idioma-residual`), para achar fala residual do original, + detecção automática de idioma.
- Folha de contato (1 quadro a cada `--passo` s) em `<nome>_revisao.jpg`.
- Cortes de cena (scdet) a menos de 0,3 s um do outro = **quadro solto**.
- Silêncio no fim (`--silencio-fim`, padrão 1 s) e silêncios longos no meio.
- **Salto de pts no áudio** (ffprobe `packet=pts_time`) e áudio mais curto que o vídeo. O `silencedetect` NÃO pega esse defeito.
- Setas de CTA: estão no último quadro? ficam em cima da faixa escura do rodapé? (`--faixa y0,y1` se a detecção falhar).
- `--lipsync`: roda o `checar_lipsync.py` por trecho e dá o índice do conjunto.
- Saída: `<nome>_revisao.txt` + `<nome>_revisao.jpg`, ao lado do vídeo ou em `--saida`.
- **Não mede loudness.** LUFS/true peak ficam na checklist manual.

**O que o `finalizar.py` faz.** Reencoda no padrão (H.264 high, yuv420p, 30 fps, AAC 48 kHz 128k, +faststart) com bitrate para caber no limite (padrão 30 MB), decodifica o arquivo inteiro, confere duração/resolução e gera `<nome>_frames.jpg`. Modo só conferência: `--so-revisar`.

**Defeitos que só apareceram com revisão extra (histórico).**
- Subagentes revisores (whisper es/en + OCR + folha) pegaram o que a `_frames.jpg` não mostra: quadros soltos nos cortes, silêncio no fim e setas sobre o aviso.
- Rótulo branco antigo voltando por cima do take do Kling (bug do `encaixar_edit.py`, corrigido em 05/10/2026): só aparece com zoom.
- Buraco de 3 s no áudio por reinit do filtergraph (Wyze AD 06, 8,49 → 11,49 s): só aparece no pts.
- No lote Oración, 10 de 18 vídeos voltaram ao menos 1 vez pelo revisor independente de lipsync.
- O revisor independente achou em lotes reais: volume final fora de −16…−13 LUFS; caixa/legenda 1 quadro atrasada depois de ~15 s em vídeo 29,97 qps; pares 9:16 × 4:5 com texto/tempo diferentes; selo/setas cobrindo produto ou boca.
- San Benito FR (13/10/2026): o revisor comparou também luma ES × FR, nitidez do rosto, OCR da tela e folhas da boca por trecho (`SB-VENCEDORES_OP2-ASCENSAO_JESU-V07\_trabalho\revisor\`). Daí saiu a v2 dos dois ADs.

**Inconsistência conhecida.** A skill `revisar-criativo` escreve `--residual <idioma>`, mas o argumento real do script é **`--idioma-residual`**. `--residual` não é aceito pelo argparse — precisa de revisão manual na skill.

## Lógica de uso

### 1. Revisão automática (todo arquivo final)
```
python ferramentas/revisar_ad.py "AD 25 - X.mp4" --idioma es --idioma-residual en --proibidos "maya verra,60 días,tiktok"
python ferramentas/revisar_ad.py "AD 06 - X.mp4" --proibidos proibidos.txt --passo 2 --saida _revisao
python ferramentas/revisar_ad.py "AD NN.mp4" --idioma es --proibidos lista.txt --formato 4:5 --passo 1
```
Outras opções: `--modelo small`, `--sem-whisper`, `--ate N` (transcreve só até N s), `--faixa y0,y1`, `--silencio-fim 1.0`, `--lipsync "saida:audio:original[:x;y;w;h],..."`. RESULTADO tem que ser OK.

### 2. Lista de termos proibidos (`termos.txt`, um por linha)
Montar pela categoria, conferindo em áudio e em tela:
- **Tradução:** preço, moeda, país/cidade, plataforma de origem ("TikTok", "carrito naranja"), "link", cupom, estação/data, unidade estrangeira, e as palavras do idioma original (ex.: `proibidos_fr.txt` do SB FR listou "cierra", "milagro", "toca", "san benito"…).
- **Troca de marca:** marca antiga (e grafias coladas/soletradas), garantia antiga, "hecho en …", registro sanitário, claims não confirmados, remédio/doença como cura.
- **Sempre:** hora do dia ("ce soir", "esta noche"), promessa de kg/resultado, "ao vivo", botão/plataforma diferente do destino.
- Base por país: `kit-edicao-criativos\exemplos\termos-por-pais.md`.

### 3. Olhar de verdade
1. Abrir o `_frames.jpg` e o `_revisao.jpg` (Read na imagem).
2. Take editado por IA ou faixa de rótulo: **zoom 3x** na região (`folhas_contato.py`):
   ```
   python ferramentas/folhas_contato.py --cada 1 --de 0 --ate 60 --saida pasta video.mp4 [--colunas 12] [--largura 150]
   ```
3. Lipsync: folha da boca de 3 em 3 quadros nos trechos em AVISO.
4. Ouvir as emendas (versão curta, variações, trechos trocados).

### 4. Checagens manuais que a ferramenta não faz
- **Pts do áudio** (se o `revisar_ad` não rodou ou para confirmar): `ffprobe -select_streams a -show_entries packet=pts_time`; ou comparar a duração do áudio decodificado com a do corpo.
- **Loudness:** final entre −16 e −13 LUFS, TP ≤ −1 dBTP; voz clara (−15 LUFS), trilha baixa (−32 LUFS sob a fala), sem estalo.
- **Quadro a quadro nos cortes** em vídeo 29,97 qps: alinhar caixa/legenda pelo número do quadro.
- **Par de formato** (9:16 × 4:5): mesmo texto e mesmo tempo.
- **Selo e setas:** não cobrem produto nem boca; mesmo tamanho e posição em todo o lote.
- **Cor:** luma média original × final.
- **Whisper residual:** em idioma próximo (ES sobre áudio FR), ele "traduz" a fala nova. Procurar frases do roteiro original, não contar linhas.
- **Seta amarela** (estilo SB-JESU): o `revisar_ad` avisa "não achei setas vermelhas no último quadro". É falso alerta; conferir a olho.

### 5. Checklist do `revisar-criativo` (tudo sim)
- [ ] Nome `AD NN - …` na sequência; resolução da receita; decodifica; duração conferida.
- [ ] ≤30 MB quando o kit comprime (longo pode passar; registrar o MB real).
- [ ] Legenda grande e legível, nada cobrindo rosto/boca, sem legenda junto de manchete no meio, sem texto de outro idioma (nem por 0,3 s nas emendas).
- [ ] Setas vermelhas na palavra do CTA até o fim, fora da faixa/selo; nenhum "botão falso".
- [ ] Corpo começa na frase certa; nada do hook/fim antigo; emendas em fim de frase.
- [ ] Nenhum take repetido; produto idêntico ao original; rótulo novo em todas as cenas (zoom 3x).
- [ ] Áudio sem buraco (pts) e sem fala original por baixo (residual vazio).
- [ ] Texto do anúncio: título + principal, botão do Meta = o que o vídeo manda tocar.
- [ ] Custo real ≤ informado.
- [ ] Compliance Meta:
  - sem atributo pessoal de quem vê;
  - sem kg exato, "cura", médico/doença como prova ou remédio;
  - antes/depois de corpo → marcar risco;
  - sem hora do dia, "ao vivo" ou ranking/estoque inventado.
- [ ] Nicho espiritual/fé/"manifestação": **perguntar** manter × suavizar. Listar por vídeo, com tempo:
  - promessa de dinheiro;
  - cura;
  - ameaça ou contagem regressiva;
  - depoimento com resultado;
  - famoso;
  - cenas de hospital, remédio ou dinheiro.

  Aplicar só o que a pessoa escolher.

### 6. Revisor independente (lote ≥10 vídeos, ou lipsync)
Subagente sem acesso ao que o editor achou. Faz whisper alvo + residual, OCR, folha e índice de pausa no rosto de quem fala, e devolve uma lista de defeitos por vídeo com tempo. Dividir em lotes A/B/C e repetir até passar. Corrigir, revisar de novo e dizer em 1 linha o que foi corrigido. O que não der para corrigir vai como "revisão manual", com tempo e motivo.

### Armadilhas de ambiente
- **PowerShell × Git Bash:** rodar `revisar_ad.py --lipsync "a:b:c,..."` pelo PowerShell; o Git Bash converte os `:` como caminhos.
- **Termos com acento:** lista de proibidos num `.txt` UTF-8. Dentro de um `.ps1`, o PowerShell 5.1 corrompe os acentos.
- **Encoding:** scripts que imprimem "≈" ou acentos quebram no cp1252. Usar `PYTHONIOENCODING=utf-8` (ou `PYTHONUTF8=1`).
- **CPU:** Whisper e OCR em paralelo ficam até 10x mais lentos; rodar em sequência (`cpu_threads=4`, `-threads 4`).
- **faster-whisper na GPU** falhou com `cublas64_12.dll` (Yara): `device='cpu', compute_type='int8'`.
- **Avatar HeyGen inteiro** reprova no `checar_lipsync` (falso positivo, Vitaly): conferir a olho.

### Checklist de saída
- [ ] `revisar_ad.py` OK (ou avisos explicados) em todos os vídeos.
- [ ] Folhas abertas e zoom nos trechos editados.
- [ ] Loudness e pts conferidos.
- [ ] Relatório com o que foi corrigido e o que ficou para revisão manual.

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [02-regras-gerais-e-seguranca.md](02-regras-gerais-e-seguranca.md)
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [04-fluxo-producao-criativos.md](04-fluxo-producao-criativos.md)
- [05-traducao-de-criativos.md](05-traducao-de-criativos.md)
- [06-troca-de-marca.md](06-troca-de-marca.md)
- [08-voz-e-dublagem.md](08-voz-e-dublagem.md)
- [09-lipsync-e-avatar-heygen.md](09-lipsync-e-avatar-heygen.md)
- [10-limpeza-cor-e-qualidade-de-video.md](10-limpeza-cor-e-qualidade-de-video.md)
- [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md)
- [13-analise-meta-ads-e-vencedores.md](13-analise-meta-ads-e-vencedores.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)
- [projetos/](projetos/)
