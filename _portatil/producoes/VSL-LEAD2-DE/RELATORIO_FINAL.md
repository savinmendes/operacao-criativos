# VSL Lead 2 em alemão: relatório da montagem final

**Data:** 20/10/2026.

**Arquivos entregues:**
- `VSL-LEAD2-DE.mp4`
- `VSL-LEAD2-DE_frames.jpg` (folha com um quadro a cada 30 s)
- este relatório

**Pasta de trabalho:** `_trabalho\montagem\`. Lá ficam os scripts, os trechos com a boca colada (`comp\`), os blocos renderizados, o áudio e as revisões.

## Saída

| Item | Valor |
|---|---|
| Duração | 38:19,9 (2299,9 s) |
| Quadros | 68.997 |
| Vídeo | 720x960, 30 fps, H.264 (crf 21), etiqueta bt709/tv aplicada só por `h264_metadata` |
| Áudio | AAC 192k, 48 kHz |
| Volume | -16,0 LUFS integrado, pico real -1,6 dBTP |
| Tamanho | 451 MB |

**Cor:** leitura e gravação em bt601 fixo. A luma do vídeo final ficou igual à da base, com diferença média de +0,02 nível em 17 pontos (base, lipsync e b-roll).

## Cortes feitos

1. **Abertura inteira cortada.** Saíram o apresentador de traje papal e o b-roll de 0 a 03:25 do original, ou seja, os blocos B001 a B019 e os trechos L001 a L021.
   - Também saiu a maior parte da tomada geral da igreja que vinha depois (original 205,7–223,1 s).
   - O vídeo começa em T0 = 247,3 s da timeline DE antiga, que corresponde a 223,07 s do original. Toda a timeline foi deslocada para começar em 0.
2. **Início:** abre na igreja vazia com fade-in de 0,3 s, no vídeo e na trilha.
   - A primeira palavra, "Meine Lieben", entra em 0,48 s, sem corte.
   - O padre aparece em 2,9 s.
3. **Trecho do Papa** (original 276,4–403,8 s): já estava fora da timeline e continua fora.

## Como foi montado

### Vídeo
- **Base:** `base_limpa_live` reajustada no tempo pelo fator de cada seção.
- **Os 271 trechos de lipsync (L022–L292):**
  - Do mp4 do lipsync entrou SÓ a elipse de boca e queixo, achada com MediaPipe em cada quadro, suavizada e com borda suave.
  - Essa elipse foi colada sobre a base limpa.
  - Cada quadro do lipsync foi alinhado ao quadro certo da base (busca de ±4 quadros). O erro médio de alinhamento ficou entre 0,7 e 1,5 nível.
  - As caixas da legenda ES (OCR) ficam fora da máscara.
  - Resultado: nenhuma legenda ES nem "EN VIVO" vem dos mp4 dos lotes.
- **Legenda alemã:**
  - Vem do `alinhamento_de.json`, com o texto do roteiro.
  - São 1.065 blocos de até 2 linhas, sincronizados pelas palavras.
  - Texto branco em caixa escura translúcida embaixo (Segoe UI Semibold, que tem äöüß), no estilo da original.
  - Os números longos aparecem em algarismos: 29.700 / 90.000 / 35.000 Euro, 99 Prozent, 23./24.
- **Render:** 8 blocos de 5 min, concat sem recodificar e um único mux de áudio.

### Áudio
- **Voz:** `narracao_de_completa.wav`, cortada em T0.
- **Trilha:**
  - É o `no_vocals.wav` reajustado no tempo com os mesmos fatores (atempo por seção).
  - Tem micro-fade no salto do corte do Papa e passou pela limpeza de chiado da receita (`chiado.py`, `limpar_trilha`).
  - Fica em -32 LUFS, com dip de 3 dB nas pausas.
- **Mix:** -16 LUFS e pico real ≤ -1,5 dBTP, com ganho estático e alimiter `latency=1`.

### Sincronia
- **Pacotes de áudio:** nenhum salto de pts.
- **Duração:** áudio e vídeo com 2299,9 s.
- **Fala × boca:** medida em 10 pontos (correlação da abertura da boca com o envelope do áudio). Atraso de 0 a 1 quadro nas janelas de 20 s.
- **Revisor independente:** conferiu a olho em 6 pontos, quadro a quadro: 0 a 1 quadro.

## Trechos cobertos com b-roll

O b-roll vem só de tomadas da própria igreja, sem rosto falando: nave, púlpito vazio, altar ao longe, estátua e igreja com altar.

- **Contador:** o contador de espectadores é colado do momento correspondente, para não pular.
- **Parte close (31:30–38:20, que não tem selo):** o b-roll entra com zoom de 1,12x, sem selo e sem contador.
- **Pausas:** as pausas próximas foram agrupadas em blocos maiores, para não picotar.
- **Repetição:** o mesmo tipo de tomada não se repete em sequência.

| Tempo no vídeo final | Trecho | B-roll | Motivo |
|---|---|---|---|
| 05:22.0–05:28.6 | L058 | nave → púlpito vazio | pausas da depoente 3 |
| 05:31.7–05:39.6 | L059 | altar → estátua → igreja | pausas da depoente 3 |
| 05:42.8–05:45.6 | L060 | nave | pausas da depoente 3 |
| 06:58.9–07:08.1 | L070 | púlpito → altar → estátua | trecho inteiro (sem pausa medível) |
| 07:51.2–08:02.7 | L077 | igreja → nave → púlpito | trecho inteiro |
| 08:07.5–08:15.9 | L079 | altar → estátua → igreja | trecho inteiro |
| 09:50.4–09:56.3 | L091 | nave → altar | trecho inteiro |
| 10:49.3–10:52.6 | L098 | púlpito vazio | pausas |
| 11:31.2–11:37.1 | L103 | estátua → igreja | trecho inteiro |
| 12:32.4–12:38.3 | L110 | nave → altar | trecho inteiro |
| 19:24.7–19:25.7 | L160 | púlpito vazio | pausa |
| 21:50.7–21:58.0 | L178 | estátua → igreja → nave | trecho inteiro |
| 31:15.3–31:17.3 | L244 | altar | depois de 5,27 s (mão no rosto) até o crucifixo do original |
| 33:47.0–33:54.2 | L261 | púlpito → estátua → igreja (zoom) | trecho inteiro (sem pausa) |
| 34:06.2–34:09.2 | L263 | nave (zoom) | pausas |
| 35:39.8–35:43.9 | L274 | altar → púlpito (zoom) | pausas |

No total são cerca de 92 s de b-roll em 33 tomadas. Nenhum retoque foi feito na boca.

## Correções feitas depois da revisão independente

1. **"EN VIVO" no fade para preto em 31:26–31:29.** O `selo_live` da base não pegava no fade. Agora o selo LIVE do quadro anterior entra escurecendo junto. A tomada da nave escura saiu das coberturas.
2. **Legenda ES que tinha escapado na base:**
   - "y la llevaría a la muerte en un", em 11:02–11:05 (68 quadros);
   - um "ú" solto, em 14:20–14:24 (95 quadros).
   - Os dois foram limpos com LaMa (mesmo método da base) só nesses quadros.
   - Uma varredura de todos os quadros usados, procurando pixels de texto na faixa da legenda, não achou outros resíduos de linha.
3. **Contador pulando no b-roll:** agora mostra o número do momento.
4. **B-roll na parte close sem selo:** entra com zoom, sem selo.
5. **Depoimento picotado:** as coberturas foram agrupadas. Estátua e púlpito se repetem menos.
6. **Legenda:** números longos em algarismos e "seelische" com minúscula.
7. **Pretos do original:** 3 quadros pretos soltos vindos do original (18:35,1 e 24:44,1) foram trocados pelo quadro anterior. Um quadro solto de lipsync antes de cada cobertura também foi eliminado.

## Imperfeições conhecidas (com tempos)

- **Lipsync "aviso" (~150 trechos):** são trechos sem pausa medível no áudio DE. A boca articula, mas não dá para provar a sincronia com o índice. A olho estão ok nos pontos conferidos.
- **Resíduos da base na depoente 3:** um traço horizontal laranja em ~05:37 e uma mancha pequena em ~05:45, na faixa da legenda, ficaram da limpeza da base. A legenda alemã cobre em parte.
- **Ponto colorido no cabelo do padre** (ex.: 15:05, 18:30, 24:18, 29:05): já vem do vídeo original.
- **Fade para preto de 0,47 s em 31:28:** é a transição do original antes do close.
- **Contador do original:** cai de ~52 mil para 1.458 entre 29:58 e 30:40 e fica em 1.458 até 31:26. Já era assim no original.
- **Trilha na parte de FAQ (31:30–38:20):** a música do original é bem baixa ali. Em algumas pausas curtas sobra quase só silêncio.
- **"Padre Juan" / "Padre, ich verstehe…" (36:30):** está no roteiro aprovado e na voz. Em alemão o mais natural seria "Pater". Mudar exigiria regravar a voz: decisão da pessoa.
- **Resolução 720x960:** o `revisar_ad.py` acusa formato fora da lista, mas é a mesma do original. Não é defeito.

## QA

**`revisar_ad.py`** (whisper `de`, proibidos em `.txt` UTF-8):
- Idioma detectado: de (0,87).
- Nenhum termo proibido.
- Sem saltos de pts, sem silêncios longos e sem par de cortes a menos de 0,3 s.

**OCR a cada 15 s:** sem texto em espanhol nem "EN VIVO".

**Folha de contato:** `VSL-LEAD2-DE_frames.jpg`.

**Revisor independente:**
- Whisper `de` em 9 trechos: só alemão, "37 Euro" correto, primeira palavra "Meine Lieben".
- 24 zooms de boca: sem costura e sem boca dupla.
- Emendas dos blocos de 300 s: ok.
- Os 5 bloqueantes e os médios que ele apontou foram corrigidos (ver acima). O resultado da segunda verificação dele está no fim deste relatório.
