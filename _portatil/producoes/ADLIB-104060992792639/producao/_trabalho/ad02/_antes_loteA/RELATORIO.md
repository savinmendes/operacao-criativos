# AD 02: relatório (PT → espanhol neutro LATAM), 08/10/2026

## Arquivo
`producao\AD 02 - ORACION-TRES-BENDICIONES-SHOPPING-ES-LATAM.mp4`: 117,0 s, 720x1280, 30 fps, 26,5 MB, sem selo. Setas a partir do 1º "Toca" (106,44 s) até o fim.

## Descoberta: o 02 é o AD 01 com outro gancho
- **Gancho (quadros 0–285, 0–9,53 s):** é novo. Uma mulher jovem de manto fala num shopping, e uma enfermeira chora sentada, calada.
- **Do quadro 286 em diante:** é idêntico ao 01.mp4 deslocado em 44 quadros. A diferença média é de 0,1–0,7, e a voz PT (demucs) tem correlação de 0,99.
- O cartão final "CLIQUE E RECEBA!" saiu, igual ao AD 01: o vídeo termina 0,7 s depois da última fala, com fade de 0,3 s.
- **Reaproveitado do AD 01:**
  - a legenda já removida com LaMa (`ad01\base_sem_legenda.mp4`);
  - a narração ES (`ad01\narracao_es.wav` e o alinhamento, a partir de 8,40 s do 01, deslocados +1,4667 s);
  - a `base_lipsync.mp4` do AD 01, já refeita em speed pelo agente do 01 (cópia de 22:03 em `_tmp\ad01_base_lipsync_snap.mp4`).

## Roteiro
- **Gancho (mulher do shopping):** "¿Eres tú, con ese celular en la mano? Dos personas vieron este video antes que tú, pero no era para ellas. Este mensaje es para ti."
  - São 3 pedaços, cada um encaixado na frase PT correspondente.
- **Resto:** o roteiro do AD 01, palavra por palavra, de "Yo soy la Desatadora de Nudos…" até "Toca el botón de abajo."
- Os tempos estão em `roteiro_es.txt`.

## Vozes
- **Gancho: voz nova**, "ORACAO-02 mulher shopping" `ErqTI1A8XA0CK8tS4IH7`, clonada dos 9,45 s do gancho (demucs).
  - Semelhança com as vozes que já existiam (Resemblyzer): Desatadora 0,84, ORACAO-11 mulher 0,78, Clara 0,84, ORACAO-13 mulher 0,84, menina 0,64.
  - Nenhuma chegou a 0,9, então é outra personagem.
- **Desatadora:** "ORACAO-11 mulher" `UNDKAyEJ2rTv99l7gCy5`, herdada do AD 01. Contra o 01, a semelhança é 0,999.
- Nenhuma voz foi apagada.

## Custos
- **TTS:** 131 caracteres (cerca de US$ 0,02). O corpo veio do AD 01.
- **HeyGen:** cerca de 25 créditos estimados.
  - h1 precision: 9,5 s, descartado (índice de pausa 0,69);
  - h1 speed: 9,5 s;
  - s08 do 01 refeito em speed: 11,3 s.
- **Saldo da conta:** 8.840 → 8.818 durante os ADs 02 e 03. A conta é compartilhada e a cobrança do speed atrasa, então esse número não fecha por AD.

## Lipsync (índice de pausa)
| Trecho | Tempo no 02 | Resultado |
|---|---|---|
| h1: gancho, recorte 360x640 em (290,200), só a mulher, speed | 0–9,53 | **0,17 APROVADO**. Em precision dava 0,69. Diferença fora do rosto na colagem: 1,2 (nível de ruído) |
| s02 do 01 (speed) | 9,87–17,37 | 0,41 |
| s03 e s04 do 01 (precision, aprovados pelo revisor do 01) | 17,37–22,43 | 0,65, com só 6 quadros de pausa; s04 sem pausa (aviso) |
| s05, s06 e s07 do 01 (speed) | 22,43–50,47 | 0,22 / 0,19 / 0,18 |
| **s08 do 01, refeito aqui em speed** (mesma entrada `crop_s08_pt.mp4`) | 50,47–61,73 | Sem pausa no ES. Corr. ES 0,25 × PT 0,19. Antes era REPROVADO (ES 0,15 × PT 0,30) |
| s09, s11 e s12 do 01 (speed) | 61,73–106,2 | 0,11 / 0,60 / 0,38 |
| s10 e s13 do 01 (precision) | | 0,49 / 0,59 |
| **Conjunto (13 trechos)** | | **0,37 APROVADO** |

## O que saiu ou foi trocado
- **Na fala:** o mesmo que no AD 01 (dinheiro, saúde, "tudo dobrado", "hoje").
- **Legenda PT do gancho:** removida com LaMa GPU, máscara justa (y 845–945, longe da boca).
- **Moeda ou marca do Brasil na imagem:** não havia.

## Revisão própria
- **`revisar_ad.py`** (proibidos completos e `--lipsync` com 13 trechos): **OK, nenhum problema.**
  - idioma es (0,99), nenhum termo proibido;
  - nenhum silêncio acima de 0,7 s, nenhum salto de pts;
  - 2 cortes, nenhum par a menos de 0,3 s;
  - setas no último quadro.
- **Português residual:** nenhum.
- **`folha_cortes.jpg`:** de 1 em 1 quadro, no corte do gancho (286) e nas 10 emendas do corpo. Sem quadro solto.
- **`_tmp\zoom_gancho.jpg`:** boca do gancho.

## Pontos para a pessoa olhar
1. **Voz do gancho:** o clone saiu de só 9,45 s. Vale ouvir.
2. **s03 e s04 (17,4–22,4 s), herdados do AD 01 em precision:** o kit dá aviso.
3. **Se o agente do 01 refizer mais trechos depois de 22:03:** basta rodar `montar_corpo.py` (antes, apague `_tmp\ad01_base_lipsync_snap.mp4`), depois `lipsync\trocar_s08.py`, `montar_corpo.py` de novo e `montar_ad.py`.
   - O job do agente do 01 para o s08 (`e6fc3f79…`) ainda rodava quando o s08 foi refeito aqui.
4. **9,53–9,66 s:** por cerca de 4 quadros depois do corte, a boca da Desatadora ainda termina o "ti", sem voz (resto do s01 do 01).
