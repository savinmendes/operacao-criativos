# AD 15: relatório (PT → espanhol neutro LATAM), 08/10/2026

## Arquivo final
- `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 15 - ORACION-REGALO-ES-LATAM.mp4`
- 18,00 s, 720x1280, 30 fps, AAC, 11,9 MB, sem selo. Tema: **REGALO** (o "presente" da Desatadora).
- O original tem 18,07 s e termina na fala (não tem tela parada). A fala ES termina em 17,60 s; o vídeo corta em 18,00 s, com fade de 0,3 s.
- Junto: `_frames.jpg`, `_revisao.jpg` e `_revisao.txt`.

## Roteiro em espanhol (tempos no final)
| Tempo | Fala |
|---|---|
| 0,11–4,44 | Yo soy la Desatadora de Nudos, y fuiste tú a quien escogí. Te traje un regalo. |
| 4,73–11,02 | En este video está la oración de nueve palabras que, al escucharla, desata tu nudo y abre camino a una gran bendición. |
| 11,26–13,16 | Toca el botón de abajo para escucharla. |
| 13,53–17,60 | No dejes pasar la bendición que separé para ti. Toca el botón de abajo ahora. |

Velocidade de 1,06x em todos os blocos (atempo). Duas pausas internas foram encurtadas: 0,15 s no b0 e 0,25 s no b3.

## Vozes
- **"ORACAO-11 mulher" `UNDKAyEJ2rTv99l7gCy5` (reaproveitada).** No Resemblyzer, a voz do 15 contra a fonte do clone do AD 11 dá **0,980**: é a mesma Desatadora. O tom médio é de 203 Hz contra 190 Hz.
- As outras comparações: AD 05 Desatadora 0,911, AD 13 mulher 0,872, menina 0,577.
- Nenhuma voz foi criada nem apagada.

## Custos
- **TTS:** 312 caracteres, 4 blocos gerados uma vez só, `eleven_multilingual_v2`, cerca de US$ 0,05.
- **HeyGen:** de 8.839 para 8.830, ou seja, **9 créditos** para 3 jobs `speed` somando 18,07 s.
  - A conta é compartilhada com outros agentes rodando ao mesmo tempo, então 9 é o máximo que este AD pode ter gasto.
  - A cobrança do speed pode aparecer com atraso (LICOES-LIPSYNC.md).

## Lipsync (segui o LICOES-LIPSYNC.md: `mode speed`, PT original no vídeo, ES separado)
- **Parâmetros:** `enable_dynamic_duration=false`, `keep_the_same_format=true`, `fps_mode cfr`, sem marca d'água.
- **Retorno:** os 3 trechos voltaram com o número exato de quadros e sem quadro de outra tomada.

| Trecho | Tempo | Entrada | Índice de pausa | Corr. ES | Kit |
|---|---|---|---|---|---|
| s1 | 0,00–4,70 | quadro inteiro (só 1 rosto) | 0,03 | 0,41 | APROVADO |
| s2 | 4,70–13,47 | quadro inteiro | 0,65 (só 10 quadros de pausa) | 0,13 | AVISO |
| s3 | 13,47–18,07 | recorte 216x384 em (247,120) no rosto pequeno (plano aberto nas nuvens), escalado 3,33x | 0,02 | 0,47 | APROVADO |
| **Conjunto** | | | **0,22** | | **APROVADO** |

- **O AVISO do s2 foi conferido na folha** `_tmp/boca_s2.jpg`:
  - na pausa de 11,02–11,25 s a boca fecha;
  - na pausa final, 13,16–13,47 s, ela fica num sorriso leve com os dentes aparecendo, sem articular. É isso que puxa o índice para 0,65.
  - A boca é nova (diferente do sorriso largo do original) e articula durante a fala.
- **Colagem:** só uma elipse suave na boca e no queixo, sobre a base limpa (`_lote/recolocar.py`).
- **Emenda s1/s2 (4,70 s, mesma tomada):** mistura de 2 quadros só na boca.
- **Emenda s2/s3:** cai num corte de câmera.

## O que saiu ou foi trocado
- **Dinheiro:** "liberam uma grande bênção **financeira**" virou "abre camino a una gran bendición".
- **"9 palavras":** virou "la oración de nueve palabras", para manter o motivo.
- **"Não ignore a bênção":** virou "No dejes pasar la bendición" (mais suave).
- **CTA:** "Clica no botão Saiba mais" virou "Toca el botón de abajo", que é genérico e não depende do botão do Meta.
- **Imagem:**
  - a legenda PT amarela (y 850–975) saiu com LaMa na GPU, com máscara justa (glifo, contorno e sombra);
  - a **seta vermelha animada** "MAIS ABAIXO" (15,8–18 s, y 995–1195) também saiu, com uma máscara fixa;
  - não há moeda, marca ou famoso na imagem.
- **Áudio:** narração no nível da voz original e fundo musical do demucs (`no_vocals`, −39 LUFS) mantido. O final tem −13,8 LUFS.
- **Legenda nova:** pelo alinhamento, em y 1358 (escala 1080), na altura da antiga e longe da boca. As setas entram no 1º "Toca" (11,25 s) e vão até o fim.

## Revisão própria
- **`revisar_ad.py`** (`--idioma es --idioma-residual pt`, com a lista completa de proibidos, inclusive "segundos" e "aire", e `--lipsync` nos 3 trechos): **OK, nenhum problema**.
  - idioma es (1,00), nenhum termo proibido, nenhum silêncio acima de 0,7 s, pts sem saltos;
  - 1 corte de cena, sem pares a menos de 0,3 s;
  - setas no último quadro;
  - índice de pausa do conjunto 0,22.
- **Transcrição:** bate com o roteiro. A passada em PT só "traduz" o espanhol, sem fala residual.
- **Folhas:**
  - `_tmp/cortes.jpg`: 1 em 1 quadro em 4,70, 13,47 e 17,8 s, sem quadro solto;
  - `_tmp/boca_s2.jpg` e `_tmp/boca_s3.jpg`: zoom na boca, de 2 em 2 quadros, final x original, com as barras de voz ES/PT;
  - `_tmp/z.png` e `_tmp/z2.png`: faixa da legenda e da seta.
- O vídeo não foi aberto.

## Pontos para a pessoa olhar
1. **Ritmo:** a fala ficou corrida (1,06x e pausas encurtadas) para caber nos 18 s, como já era o original.
2. **Fim:** só ~0,4 s depois do "ahora", com fade. O original não tinha folga.
3. **Plano das nuvens (13,5–18 s):** o lipsync foi feito num rosto pequeno, recortado e ampliado. A boca articula e fecha nas pausas, mas a região colada pode ficar um pouco mais suave que o resto.
4. **Onde ficava a seta vermelha antiga** (nuvens embaixo da túnica), o preenchimento do LaMa fica levemente mais liso. As setas novas passam por perto.

## Arquivos e scripts
- **Scripts reutilizáveis do lote** (`_trabalho\_lote\`):
  - `narracao.py`: monta a narração com atempo e cortes, e ajusta o alinhamento;
  - `lama_base.py`: legenda e seta;
  - `ls_prep.py`: entradas do HeyGen;
  - `baixar.sh`;
  - `recolocar.py`;
  - `montar_corpo.py`;
  - `folha_boca.py` e `folha_cortes.py`.
- **Deste AD:**
  - `pecas.json`, `lama.json`, `lipsync\segs.json`, `lipsync\ids.txt`, `receita_ad15.json`;
  - `lipsync\chk\` (trechos colados, com o ES e o original, para o `checar_lipsync`).
