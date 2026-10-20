# Revisão independente: AD 05 - ORACION-FAMILIA-ES-LATAM.mp4 (versão "Correção v2", 07/10/2026)

Revisor independente. Nada foi editado.

## Veredito: **REPROVADO**

| Item | Situação |
|---|---|
| Boca em PT nos trechos cobertos (4,96–6,71 e 8,17–11,92 s) | **OK**: nenhuma boca falando português aparece |
| c1 (0–3,1 s, Clara) | **OK** |
| d1 (54,27–61,40 s) | **REPROVADO**: a boca é nova, mas não segue o espanhol |
| d2 (61,40–71,33 s) | **REPROVADO**: o mesmo defeito do d1, e o relatório não aponta |
| m1 (3,63–5,00 s) | Duvidoso: a boca ficou quase igual à original |
| m4 (36,80–47,20 s) | Aviso: índice de pausa 0,66–0,84 |
| Fala, imagem, áudio e CTA | OK. Há um ponto de compliance no depoimento do marido. |

---

## 1. Lipsync

### Método
- **Medida na saída do HeyGen:** usei o `checar_lipsync.py` atual do kit, que já tem a escolha do rosto e o índice de pausa, em cada `ls_*.mp4` contra o `pt_*.mp4`. No c1, o vídeo foi recortado só na Clara (`checar_lipsync_ad05.log`).
- **Medida no vídeo final:**
  - o final (30 fps) foi varrido contra o `05.mp4` (24 fps) no mesmo tempo, já descontado o corte de 70 quadros em 53,58 s;
  - a medida é sempre na boca de quem fala: a Clara é o rosto de cima no c1, e nos outros blocos vale o rosto maior;
  - scripts `varrer_boca05.py` e `analisar05.py`, resultado em `metricas_ad05.txt`.
- **Por que a coluna "mudou" do final não serve aqui:** a troca de 24 para 30 fps desalinha os quadros e enche a medida de ruído. Para "a boca mudou?", vale a medida na saída do HeyGen.
- **Meta do índice de pausa:** ≤ 0,6. Referência: AD 11 aprovado 0,38, AD 13 0,56, AD 01 reprovado 0,86.

### Resultado por bloco

| Bloco | Tempo no final | Quem | Boca mudou (HeyGen) | Índice de pausa (HeyGen / final) | Corr. ES (HeyGen / final) | Veredito |
|---|---|---|---|---|---|---|
| c1 | 0,00–3,13 | Clara | 100 % (recorte na Clara) | 0,48 / 0,68 | 0,71 / 0,50 | **aprovado** |
| m1 | 3,63–5,00 | marido | ver abaixo | — / 0,38 (só 4 quadros de pausa) | 0,67 / 0,89 | **duvidoso** |
| c2 | 11,93–17,93 | Clara | 100 % | sem pausa / 0,09 | 0,26 / 0,28 | aprovado |
| c3 | 17,93–27,20 | Clara | 100 % | 0,13 / 0,13 | 0,61 / 0,65 | aprovado |
| m3 | 27,20–36,80 | marido | 98 % | 0,62 / 0,61 | 0,22 / 0,27 | aprovado, no limite |
| m4 | 36,80–47,20 | marido | 97 % | 0,66 / 0,84 | 0,21 / 0,23 | **aviso**: abre nas pausas de 39,47, 41,97–42,47 e 43,80 s |
| m5 | 47,20–52,97 | marido | 99 % | 0,17 / 0,36 | 0,64 / 0,67 | aprovado |
| d1 | 54,27–61,40 | Desatadora | 99 % | **1,46 / 1,47** | 0,08 / 0,03 | **REPROVADO** |
| d2 | 61,40–71,33 | Desatadora | 99 % | **1,05 / 1,28** | 0,18 / 0,18 | **REPROVADO** |
| d3 | 71,33–83,00 | Desatadora | 100 % | 0,33 / 0,43 | 0,43 / 0,44 | aprovado |
| d4 | 83,00–89,60 | Desatadora | 99 % | 0,29 / 0,43 | 0,39 / 0,39 | aprovado |
| d5 | 89,60–95,50 | Desatadora | 95 % | 0,02 / 0,04 | 0,68 / 0,67 | aprovado |

- O índice total no final é 0,49, puxado pelos blocos bons.
- Todos os blocos têm o número certo de quadros. O m1 usa os 33 quadros reais dos 72 devolvidos.
- Nenhum bloco tem boca congelada no fim.

### Os pontos pedidos, conferidos no olho (zoom de 3 em 3 quadros, final em cima e original embaixo)

**(1) Trechos cobertos: OK.** Folhas `ad05_cobertos_4.7-12.2.jpg`, `ad05_coberto_4.9-6.8.jpg` e `ad05_clara_coberto_8.2-11.9.jpg`.
- **4,96–6,71 s:** só mãos, prato e mesa. Nenhum rosto até 6,5 s, quando aparece o pai, calado.
- **6,71–8,17 s** (close do pai, sem cobertura): a Clara diz "Toma, papá…", mas só aparecem o tronco e o avental dela. A boca dela não aparece.
- **8,17–11,92 s:** quem fala é o marido, e ele saiu do quadro. A Clara aparece de perfil, olhando para baixo, com a boca fechada. Pelo whisper do áudio PT, ela não fala até 12,1 s.
  - Nos últimos 3–4 quadros (cerca de 11,8 s) os lábios dela se entreabrem de leve, sem articular. Aceitável.
- Os dois enquadramentos começam e terminam em cortes de câmera do original, então não há salto de zoom no meio de uma tomada.
- O recorte ampliado 1,6–1,8x fica um pouco mais suave que o resto. Gravidade baixa.

**(2) c1: aprovado.** Folha `ad05_c1_m1_0-5.jpg`.
- A boca da Clara é diferente da original em todos os quadros e articula durante "Toma, mi amor, aquí está tu comida" (0,1–1,9 s).
- De 1,9 a 2,7 s o PT ainda falava "a sua comida", mas o ES já acabou. Ali a boca nova fica num sorriso parado, sem articular, que é o certo.

**(3) d1: reprovado.** Folha `ad05_d1_54-61.jpg`.
- A boca é nova (99 % dos quadros), mas segue mal o espanhol:
  - 57,6–57,9 s: quase fechada enquanto a voz fala;
  - 58,40 s e 59,00 s: aberta, com os dentes, nas micropausas do ES;
  - **60,90–61,40 s:** o ES já acabou ("…a una persona más", fim em 61,16 s) e a boca continua aberta, articulando, igual ao original, que ainda falava em PT.
- O relatório diz que "nas pausas a boca fecha". A medida e a folha mostram o contrário: o índice é 1,46, ou seja, a boca fica mais aberta nas pausas do que na fala.

**d2: reprovado.** Este bloco não estava na lista do relatório. Folha `ad05_d2_61-71.jpg`.
- 61,43–61,67 s: boca aberta num sorriso, com os dentes, na pausa entre os blocos.
- 63,73–64,00 s: lábios abertos na pausa depois de "esa persona eres tú".
- 67,63–67,90 s: boca entreaberta na pausa.
- O índice é 1,05 na saída do HeyGen e 1,28 no final.

**m1: duvidoso.** Folhas `ad05_c1_m1_0-5.jpg` e `ad05_m1_heygen_x_entrada.jpg`.
- Nos 33 quadros reais, a maior mudança foi de 8,3/255 na região da boca, contra 13,8 no c3 e ruído de 1,6.
- No olho, a boca do HeyGen é quase o mesmo sorriso largo com dentes do original "Obrigado, minha rainha", só com pequenas diferenças em 3 ou 4 quadros.
- O kit, rodado nos 72 quadros (39 deles de enchimento congelado), deu "mudou 44 %, corr. abertura saída × original 0,72".
- A fala tem 0,9 s, tem visemas parecidos ("reina"/"rainha") e o rosto está sorrindo. Ninguém lê "português" nesse trecho, mas pela regra (nenhuma boca igual à original) fica como ressalva.

**Outros rostos fora do lipsync:**
- **3,13–3,63 s:** não há fala em ES nem em PT.
- **52,97–54,27 s** (plano aberto da família e clarão):
  - a voz ES está em silêncio, e o PT original tinha "e ontem mesmo… fazia tempo";
  - os rostos são pequenos e as bocas não dão para ler (`ad05_plano_aberto_52.6-54.6.jpg`).
  - Gravidade baixa.
- **Família ao fundo da Desatadora:** o kit confirma que só a boca dela mudou. Ao fundo não há ninguém falando.

## 2. Fala
- **`revisar_ad.py --idioma es --idioma-residual pt --proibidos "real,reales,dinero,depósito,cantidad,riqueza,cura,curada,enfermedad,cáncer,horas,segundos,borrada"`:** **OK** (`AD 05 - …_revisao.txt`).
  - Idioma: es (0,98). Nenhum termo proibido.
  - A passada em PT só traduz o espanhol.
- **O texto bate com o roteiro do relatório.**
- **Sem dinheiro explícito, cura ou ameaça.** A ameaça "se rejeitar… a bênção fica presa" e os "segundos" saíram.
- **Ponto de compliance (média):** o depoimento do marido liga o sustento da casa à oração. A cena é montada em cima de dinheiro:
  - Clara: "mi papá no trabaja, y yo tampoco… trato de ahorrar";
  - marido: "La comida que compro es para todos, **porque este mes se desató un nudo**… la bendición que estaba detenida **empezó a llegar**".
  - Sem dizer "dinheiro", é um depoimento com resultado financeiro implícito, o que o briefing manda suavizar.

## 3. Imagem
- Folha de 1 q/s (`AD 05 - …_revisao.jpg`) e faixa da legenda antiga (`ad05_faixa_legenda_antiga.jpg`):
  - nenhuma legenda nem texto em português;
  - a mancha do LaMa ficou quase invisível;
  - 8 cortes, sem pares a menos de 0,3 s;
  - nenhum quadro solto, cena duplicada ou espelhada.
- A emenda do corte em 53,58 s cai dentro do clarão do original e fica natural.

## 4. Áudio
- −15,0 LUFS, LRA 3,6. Nenhum silêncio acima de 0,4 s, nem no meio nem no fim.
- Três vozes coerentes por personagem. Nenhum corte no meio de palavra.

## 5. CTA
- As setas entram com o primeiro "Toca" (73,4 s) e ficam até o último quadro.
- A legenda (y 1537 na escala 1080) fica no tronco, legível e longe da boca, inclusive com as setas.

---

## Defeitos

| # | Tempo | Defeito | Gravidade | Correção sugerida |
|---|---|---|---|---|
| 1 | 54,27–61,40 (d1) | Lipsync não segue o espanhol: a boca fica aberta e articulando nas pausas, sobretudo em 60,90–61,40, depois do fim da fala, como no PT original. Índice de pausa 1,46. | **Alta** | Refazer o d1 com recorte só na Desatadora (sem a família no quadro) e o PT baixo ou mudo no vídeo de entrada. Aceitar só com índice ≤ 0,6. Opcional: congelar ou fechar a boca nos 7 quadros finais depois de 61,16 s. |
| 2 | 61,40–71,33 (d2) | O mesmo defeito do d1: boca aberta nas pausas de 61,43, 63,73 e 67,63 s. Índice 1,05–1,28. | **Alta** | Refazer igual ao d1 (cerca de 10 s). |
| 3 | 36,80–47,20 (m4) | Boca abre em 3 pausas do ES. Índice de 0,66 (HeyGen) e 0,84 (final). | Média | Refazer se a nova rodada já for feita, ou conferir assistindo. |
| 4 | 3,63–5,00 (m1) | A boca do "Gracias, mi reina" ficou quase igual à original (sorriso com dentes, mudança pequena). | Média | Refazer o m1 com o PT mudo na entrada. Se continuar igual, aceitar como sorriso: são 0,9 s de visemas parecidos. |
| 5 | 31–52 s (fala do marido) | Depoimento com resultado financeiro implícito ("la comida que compro es para todos porque se desató un nudo… la bendición empezó a llegar"). | Média | Trocar por algo como "Tu papá no es ninguna carga… En esta casa volvió la paz desde que recé la oración…", tirando a relação entre comida e oração. Exige refazer o TTS e o lipsync do m3/m4. Pode ser decidido pela pessoa. |
| 6 | 4,96–6,71 e 8,17–11,92 | Recortes cobertos ampliados 1,6–1,8x, um pouco mais suaves que o resto. | Baixa | Aceitar. |
| 7 | 52,97–54,27 | Plano aberto com o PT original falando ao fundo e a voz ES muda. As bocas são pequenas e não dão para ler. | Baixa | Aceitar, ou encurtar o plano até o clarão. |

## Arquivos desta revisão (`_trabalho\revisao\`)
- **Folhas de boca (final × original):** `ad05_c1_m1_0-5.jpg`, `ad05_d1_54-61.jpg`, `ad05_d2_61-71.jpg`, `ad05_m1_heygen_x_entrada.jpg`.
- **Trechos cobertos:** `ad05_cobertos_4.7-12.2.jpg`, `ad05_coberto_4.9-6.8.jpg`, `ad05_clara_coberto_8.2-11.9.jpg`.
- **Outras folhas:** `ad05_plano_aberto_52.6-54.6.jpg`, `ad05_faixa_legenda_antiga.jpg`, `AD 05 - …_revisao.jpg/.txt`.
- **Dados:** `boca_ad05.csv`, `metricas_ad05.txt`, `checar_lipsync_ad05.log`.
- **Scripts:** `varrer_boca05.py`, `analisar05.py`, `folha_quadro05.py`, `folha_boca.py` (com o caso do AD 05).
