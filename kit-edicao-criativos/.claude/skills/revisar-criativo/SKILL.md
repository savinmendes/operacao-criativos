---
name: revisar-criativo
description: Revisão obrigatória antes de entregar um criativo de vídeo (revisar_ad.py, termos proibidos, folha de contato, zoom nos takes editados, compliance Meta, texto do anúncio). Use antes de dizer que um vídeo está pronto.
---

# Revisar criativo

1. Rode em **todo** arquivo final:
   `python ferramentas/revisar_ad.py "<arquivo>.mp4" --idioma <alvo> --idioma-residual <idioma de origem> --proibidos termos.txt [--formato 4:5|1:1]` (sem `--formato` aceita qualquer resolução de entrega 9:16/4:5/1:1 em 720 ou 1080; com ele, só as do formato)
   Ele faz: Whisper no idioma alvo + no residual (fala original por baixo), busca de termos proibidos, folha de contato 1 quadro/s, quadro solto nos cortes, silêncio no fim, **salto de pts** (o `silencedetect` não pega; só o pts mostra buraco de áudio/vídeo) e setas fora da faixa/legenda. RESULTADO tem que ser OK.
2. Monte `termos.txt` pela categoria da adaptação (sem depender de memória; conferir em áudio e em tela):
   - **Tradução:** preço, moeda, país/cidade, nome de plataforma de origem (ex.: "TikTok"), "link", cupom/desconto, estação ou data comemorativa, unidade estrangeira (pés, libras se o mercado não usa).
   - **Troca de marca:** nome da marca antiga (e grafias coladas/soletradas), garantia antiga (dias), origem "hecho en …", registro sanitário, claims não confirmados na página oficial, menção a remédio/doença como cura.
   - **Sempre:** hora do dia, promessa de kg/resultado, "ao vivo", botão/plataforma diferente do destino real.
   **Trecho com lipsync (HeyGen etc.):** confira cada trecho antes de encaixar, e de novo no final com `--lipsync "saida1.mp4:audio_novo1.mp3:original1.mp4,..."` no `revisar_ad.py` (ou sozinho: `python ferramentas/checar_lipsync.py saida.mp4 --audio-novo novo.mp3 --original original.mp4`). Passe sempre o original: "a boca mudou" pega o lipsync que devolveu a boca antiga, e com vários rostos no plano é ele que indica quem fala (o calado não muda). Confira na saída qual rosto foi medido; se for o errado, force com `--rosto x,y,w,h` (no `--lipsync`, 4º campo `x;y;w;h`). "Acompanha o áudio novo" = **índice de pausa** (boca sincronizada fecha nas pausas da voz): ≤0,60 APROVADO, 0,60–0,75 AVISO, >0,75 REPROVADO. Boca refeita mas sem sincronia passa no "mudou" e reprova aqui. O índice por trecho é ruidoso: o AD é decidido pelo índice do conjunto que o `revisar_ad.py` imprime. Trecho em AVISO ou REPROVADO isolado num AD que passa no conjunto: olhe a boca nas pausas (folha de 3 em 3 quadros) antes de refazer. REPROVADO confirmado = refazer o lipsync (ex.: mandar o vídeo sem o áudio antigo embutido, ou recortado só no rosto de quem fala).
3. **Abra o `_frames.jpg`** (Read na imagem) e a folha do `revisar_ad.py`. Em trecho de take editado por IA ou faixa de rótulo, gere **zoom 3x** (`folhas_contato.py` na região) — rótulo antigo reaparecendo não aparece na folha normal.
4. Checklist (tudo sim):
   - [ ] Nome `AD NN - ...` na sequência certa da oferta; resolução da receita (720×1280 ou 1080×1920); decodifica sem erro; duração conferida.
   - [ ] Tamanho: ≤30 MB quando o kit comprime; vídeo longo pode passar (a plataforma aceita) — registrar o MB real.
   - [ ] Legenda grande e legível, nada cobrindo rosto/boca; sem legenda junto de manchete no meio; sem legenda/texto em outro idioma sobrando (inclusive por 0,3 s nas emendas).
   - [ ] Setas vermelhas na palavra do CTA até o fim, apontando para baixo, fora da faixa/selo; nenhum "botão falso".
   - [ ] Corpo começa na frase certa; nenhum resto do hook/fim antigo; emendas em fim de frase (ouvir as emendas da versão curta e das variações).
   - [ ] Nenhum take repetido; produto idêntico ao original em todos os takes; rótulo novo em todas as cenas (zoom 3x conferido).
   - [ ] Áudio: voz clara (−15 LUFS), trilha baixa, sem estalo, sem buraco (pts), sem fala original por baixo (Whisper residual vazio).
   - [ ] Texto do anúncio (.txt): título + principal, botão do Meta igual ao que o vídeo manda tocar.
   - [ ] Custo real ≤ custo informado.
5. **Compliance Meta** (reprovar ou marcar "revisão manual"):
   - [ ] Sem afirmar atributo pessoal de quem vê ("você está acima do peso"); 1ª pessoa do narrador é ok.
   - [ ] Sem kg exatos, sem "cura", sem médico/doença como prova, sem remédio citado.
   - [ ] Antes/depois de corpo (barriga, decote, semanas) → marcar como risco; cena sexual → cortar ou cobrir.
   - [ ] Sem hora do dia, sem "ao vivo", sem estoque/ranking inventado ("#1", "esgotou X vezes").
   - [ ] **Nicho espiritual, fé ou "manifestação": PERGUNTAR à pessoa antes de mexer.** Não corte, troque nem suavize nada disso por conta própria. No estudo, liste por vídeo (com tempo) o que aparece:
     - promessa de dinheiro (depósito, PIX, valores, riqueza);
     - cura ou doença;
     - ameaça ("se pular, a bênção some"), contagem regressiva ou "sé rápido";
     - depoimento com resultado concreto;
     - pessoa famosa;
     - cenas de hospital, cadeira de rodas, remédio, cédula de dinheiro ou tela de banco/PIX.

     Pergunte, por lote (ou por item), se quer **manter como está** ou **suavizar para o Meta**, e mostre o risco de reprovação de cada um. Aplique só o que ela escolher e registre a escolha no relatório.
5b. **Áudio e tempo** (o revisor independente achou isso em lotes reais):
   - [ ] Volume final entre −16 e −13 LUFS e true peak ≤ −1 dBTP. Original estourado se normaliza só no áudio, sem tocar no vídeo.
   - [ ] Vídeo a 29,97 qps: caixa ou legenda trocada no corte pode atrasar 1 quadro depois de ~15 s. Alinhe pelo número do quadro e confira cada corte quadro a quadro.
   - [ ] Pares do mesmo vídeo em outro formato (9:16 × 4:5): mesmo texto e mesmo tempo da fala.
   - [ ] Selo e setas não cobrem o produto nem a boca; mesmo tamanho e posição em todo o lote.
5c. **Olho humano** (defeitos que a revisão automática não pega e a pessoa achou ao assistir):
   - [ ] **Rosto do avatar:** sorriso com dentes em fala triste; rosto parado, "fantasma" (dois rostos sobrepostos) ou salto perto das pausas; reflexo piscando em óculos. Olhe a 30 qps nos trechos de avatar.
   - [ ] **Takes de IA:** porta, mãos, objetos e bordas sem deformar (zoom); pessoa ou ombro entrando pela borda.
   - [ ] **Continuidade:** mesmo rosto, roupa e cenário (estação, vegetação, luz) em todas as cenas do personagem.
   - [ ] **Gancho:** o 1º quadro conta a dor sozinho (personagem visível e contexto legível), e o título não cobre o personagem.
   - [ ] **B-roll** casa com a persona e com a fala; nenhum take aparece 2 vezes.
   - [ ] **Trilha:** muda de clima na virada; selo de aviso pequeno no topo; um CTA só.
   - [ ] **Falsos alarmes conhecidos:** o QA por modelo de visão reprova takes limpos (confirme a olho antes de refazer); o Whisper inventa frase de despedida ("gracias por ver el video", "obrigado por assistir") em trecho só de trilha; o `checar_lipsync` não mede quando a edição tirou todas as pausas do rosto (valide a olho). Nenhum desses é defeito por si só.
   - [ ] **Texto do anúncio:** não suavize nem reescreva por conta própria; se achar risco, liste e pergunte (regra de compliance acima). Já houve agente suavizando o `.txt` sem pedido.
6. **Lote grande (≥10 vídeos):** revisão por **subagente independente** (whisper alvo + residual + OCR + folha), sem acesso ao que o editor achou; ele devolve lista de defeitos por vídeo com tempo. Rode Whisper e OCR em sequência, não em paralelo.
7. Se algo falhar, corrija antes de entregar, revise de novo e diga o que foi corrigido em 1 linha. O que não dá para corrigir vai na resposta como "revisão manual", com tempo e motivo.
