# AD 14: relatório (PT → espanhol neutro LATAM), 08/10/2026

## Arquivo final
- `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 14 - ORACION-SERPIENTES-CASA-ES-LATAM.mp4`
- 97,60 s, 720x1280, 30 fps, AAC, 26,4 MB, sem selo.
- Setas a partir do 1º "Toca" (75,89 s) até o fim. Legenda em y 1493 (escala 1080), na altura da antiga.
- O corte é 0,7 s depois da última fala, com fade de 0,3 s. O original (393 s) tinha a tela parada da cruz depois de ~106 s.

## Relação com o AD 12
- **O 14 é o mesmo vídeo do 12 com outro gancho.** De 9,63 s em diante, imagem e áudio são idênticos (diferença de ~1,5/255, só compressão).
- Só os primeiros ~9,5 s são próprios do 14: a Desatadora num interior escuro, com a serpente na mão.
- Do 12 foram reaproveitados: o corpo inteiro (base sem legenda, os 14 trechos de lipsync do corpo e a colagem), a narração, o alinhamento e a receita.
- Feito só para o 14:
  - a remoção da legenda do gancho (LaMa GPU, quadros 0–230);
  - o lipsync do gancho;
  - a trilha do gancho, com o `no_vocals` do próprio 14 até 9,6 s e crossfade para a do 12.
- Detalhes do corpo: `producao\_trabalho\ad12\RELATORIO.md`.

## Roteiro
- É idêntico ao do AD 12 (tabela completa no relatório dele). O gancho é: "En este momento estoy quitando de tu camino las serpientes que se enredaron en tu vida, y que no dejan llegar tu bendición."
- O PT original do 14 é o mesmo texto do 12, falado em outra tomada.

## Voz
- "ORACAO-13 mulher" `ZsipxX9wNYg2lJhEScWc`, reaproveitada. Nenhuma voz nova, nenhuma apagada.
- A voz do gancho do 14 dá 0,969 com a do gancho do 12 e 0,946 com o corpo do 12. É a mesma personagem.

## Custos
- **TTS:** 0 caractere novo, porque o 14 usa a mesma narração do 12.
- **HeyGen:** 1 job `speed` (o gancho, 9,54 s).
  - **Estimativa:** cerca de 10 créditos.
  - A cobrança do speed atrasa até ~1 h e a conta é compartilhada com outros agentes. Saldo lido: 8.818, sem o débito ainda.
  - O corpo foi pago no lote do AD 12.

## Lipsync
- **Gancho:** recorte que acompanha o rosto, com o PT original do 14 no vídeo e o ES como `audio`. Parâmetros: speed, sem duração dinâmica, mesmo formato, cfr, sem marca d'água.
  - Voltou com 229/229 quadros.
  - **h (0,00–9,54 s):** boca mudou em 100 %, índice de pausa **0,08**, corr. ES 0,44 (PT 0,08). **APROVADO.**
- **Corpo:** são os mesmos trechos do AD 12, todos aprovados (s01–s13, índices de 0,02 a 0,58; o s09 não tem pausa e tem corr. 0,58).
- **Índice de pausa do conjunto (15 trechos): 0,23, APROVADO.**

## O que saiu ou foi trocado
- **Fala:** as mesmas trocas do AD 12.
  - Saiu a promessa financeira: "bênção financeira", dinheiro sumindo, escassez e pobreza, fartura e multiplicação, conta paga.
  - Saiu o sono e "aperto no peito".
  - Saíram "vai ser removida", "poucos segundos", "no ar", "hoje" e "o que já é seu por direito".
  - Ficaram a fé, a Desatadora, o nó e o CTA "Toca el botón de abajo".
- **Imagem:**
  - legenda PT do gancho e do corpo removidas com LaMa GPU e máscara justa;
  - seta vermelha do original removida (78–106 s);
  - nenhuma moeda, marca ou famoso do Brasil.

## Revisão própria
- **Comando:** `revisar_ad.py --idioma es --idioma-residual pt --proibidos "…,horas,segundos,aire,borrada" --lipsync <15 trechos>`, rodado pelo PowerShell.
- **Checagens que passaram:**
  - idioma es (0,99) e nenhum termo proibido;
  - nenhum silêncio acima de 0,7 s e nenhum salto de pts;
  - setas no último quadro;
  - transcrição igual ao roteiro, sem português residual.
- **O script acusou um "PROBLEMA: quadro solto? cortes em 9,53 s e 9,60 s (67 ms)". É falso positivo:**
  - é o clarão de transição do próprio original (gancho → plano com Jesus);
  - a folha de 1 em 1 quadro (`_tmp\trans_final.jpg`) contra o original (`_tmp\trans_orig.jpg`) mostra a mesma sequência de quadros lavados de luz;
  - não há quadro de outra tomada no meio;
  - no 14, a transição tem dois picos de mudança, que o detector pega como dois cortes. No 12, a mesma transição deu um só.
- **Emendas do corpo:** são as mesmas do AD 12, com folhas de 1 em 1 quadro em `ad12\_tmp\cortes_a.jpg` e `cortes_b.jpg`. Sem quadro solto.
- **Folhas do kit:** `producao\AD 14 - …_revisao.jpg/.txt` e `_frames.jpg`.
- O vídeo não foi aberto.

## Pontos para a pessoa olhar
1. **12 e 14 têm o mesmo corpo.** Só o gancho muda: olival no 12, interior escuro no 14. Servem como teste A/B de gancho.
2. **Voz:** é o clone do AD 13, igual ao 12. A mesma personagem usa o clone do 11 no AD 01.
3. **Transição com clarão (9,5–9,7 s):** é a do original. O revisor automático acusa "quadro solto", mas não é.
4. **Créditos:** conferir o saldo cerca de 1 h depois.
5. **s07 (62,5–72,5 s):** índice 0,58, perto do limite, igual no 12.

## Arquivos (`producao\_trabalho\ad14\`)
- `_tmp\lama\` (gancho), `_tmp\base_gancho.mp4`, `base_sem_legenda.mp4` (gancho do 14 + corpo do 12), `base_lipsync.mp4`, `corpo_ad14.mp4`, `audio_corpo.wav`, `receita_ad14.json`.
- `lipsync\in\` e `lipsync\out\`: `ls_h.mp4` e `full_h.mp4` próprios, mais as cópias dos trechos do corpo do 12.
- Os scripts são os do `ad12`.
