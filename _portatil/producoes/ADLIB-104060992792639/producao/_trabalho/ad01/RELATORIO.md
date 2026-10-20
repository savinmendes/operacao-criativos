# Relatório: AD 01 (PT → espanhol neutro LATAM), 07/10/2026

## Correção de cor (08/10/2026, depois da REVISAO-LOTE-C)

A versão anterior está em `_trabalho\ad01\_antes_cor\`: vídeo, folhas, `base_lipsync`, `base_sem_legenda`, corpo, `montar_corpo.py` e relatório.

- **Causa:** a leitura pelo cv2 (matriz bt709 nos arquivos com essa etiqueta) e a gravação em bt601 escureciam ~2–3 níveis por passada. A base passava pelo LaMa e pela colagem, e o recorte enviado ao HeyGen levava mais uma ou duas passadas.
- **Leitura e gravação:** as do `ad13\lipsync3\comum3.py`, ou seja, ffmpeg bt601 com `accurate_rnd`, conversão inversa exata e etiqueta bt709/tv só no bitstream.
- **Base:** refeita a partir do original `UNICOS_HD`, com as faixas do LaMa já calculadas (nenhum LaMa novo). Os PNG do LaMa vieram da leitura cv2, então foram convertidos para a leitura nova por uma afim fixa, medida no próprio original (resíduo 0,97).
- **Cor de cada trecho do HeyGen:** antes de colar, uma afim BGR robusta leva a saída para a cor da base nova (`_trabalho\_cor0104\util.py`).
- **Nenhum crédito HeyGen e nenhum job novo.** As saídas já baixadas foram reaproveitadas.

**O que foi feito:** o `_trabalho\_cor0104\recolocar_cor_0102.py` refaz, **numa geração só**, a `base_sem_legenda` e a `base_lipsync` do 01 e também as do 02, que reaproveitam o corpo do 01 a partir do quadro 242.
- **Trechos refeitos** (`lipsync2\out\v1_*.mp4`):
  - mesma elipse e o mesmo recorte do `colar.py`;
  - a cor foi medida num **anel de pele** em volta da elipse (1,3x a 2,4x, fora da boca);
  - a saída estava cerca de −4/−4/−6 BGR mais escura que a base nova.
- **Trechos antigos** (`lipsync\ls_s03/s04/s10/s13`, quadro inteiro, parte de cima):
  - afim medida em y < 760, fora da boca (desvio de só +0,6);
  - o `fechar.py` de s03, s10 e s13 foi refeito em memória, com a mesma lógica e as mesmas pausas.
- **Emendas:** iguais às de antes, com corte em 477, 584, 629, 979 e 1470 e crossfade de 2 quadros nas outras 7.
- **Conferência da montagem** (`_cor0104\conferir_montagem.py`, boca nova × anterior com a cor descontada):
  - diferença de estrutura de 1,55 (nível de recodificação);
  - os picos (~6) ficam nas pausas fechadas do s10 e do s13;
  - na folha `_cor0104\chk_fechar01.jpg`, a boca fecha igual nas duas versões, e a anterior mostra a mancha escura na bochecha que saiu.
- **Remontagem:** `montar_corpo.py` e `montar_ad.py receita_ad01.json`. Resultado: RESULTADO OK, 115,50 s, CTA em 104,97 s.

**Medidas** (luma, final − original; `revisao\loteC\cor.py` e `brilho.py` com `loteA\escolha_01.json`; saídas em `revisao\loteC\cor0104\`):

| | Antes | Depois |
|---|---|---|
| Área colada − rosto (cor.py / brilho.py) | −4,2 / −4,3 | **−0,3 / −0,1** |
| Pior trecho | s07 −6,0 | s13 −1,6 / s10 −1,4 |
| Rosto × original | −6,6 (U +1,1 / V −1,6) | **−0,3** (U +0,1 / V 0,0) |
| Fundo × original | −5,0 | **−0,7** |
| Degrau pela mediana (elipse × anel, `_cor0104\degrau_mediana_esc.py`) | — | 0 a −1 em todos os trechos |

**Revisão** (`revisar_ad.py --lipsync`, PowerShell, proibidos de `_lote\proibidos.txt`; trechos recortados do final pelo `_lote\chk_final.py`, em `_cor_rev\antes` e `_cor_rev\depois`):
- es (1,00), nenhum termo proibido, nenhum silêncio, nenhum salto de pts, setas no último quadro.
- **Índice de pausa do conjunto:** 0,21 antes e **0,22** depois, medido igual nos dois finais.
  - Por trecho: s01 0,22 → 0,27, s07 0,17 → 0,21, s11 0,47 → 0,53, e os outros variam ±0,02.
- **"PROBLEMA" s04 nos dois finais**, com os mesmos números: antes 0,64/0,50, agora 0,66/0,50.
  - É o trecho antigo em precision, já aceito (aviso no lote A).
  - Não foi mexido além da cor.
- Logs: `_cor_rev\revisar_antes.log` (sem whisper) e `revisar_depois.log`. O vídeo não foi aberto.

---


## Arquivo final
- `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 01 - ORACION-TRES-BENDICIONES-ES-LATAM.mp4`
- 115,50 s, 720x1280, 30 fps, AAC, 26,3 MB, sem selo. Setas de CTA a partir de 104,97 s ("Toca el botón de abajo ahora").
- O original tem 131,2 s: de 0 a 115,77 s é a Desatadora falando, e de 115,77 s ao fim vem um cartão "CLIQUE E RECEBA!" em português, sem fala. O vídeo foi cortado 0,7 s depois da última fala (com fade de 0,3 s), como manda o briefing, e com isso o cartão em português saiu inteiro.

## Roteiro em espanhol (voz a 1,09x)
> ¿Eres tú, con ese celular en la mano? Dos personas vieron este video antes que tú, pero no era para ellas. Este mensaje es para ti.
> Yo soy la Desatadora de Nudos, y fue a ti a quien vine a buscar. Abre tu corazón ahora y recibe lo que vine a entregarte, porque vine a avisarte que tres cosas van a llegar a tu vida.
> La primera es una liberación. Abre la palma de tu mano ahora y recíbela por la fe. En este momento estoy desatando todos los nudos invisibles que ataban tu vida. Todo lo que el enemigo ató en tu camino se está deshaciendo ahora.
> La segunda es una provisión. Veo una bendición en camino, muy cerca de tocar la puerta de tu casa. Y la tercera, escucha con atención.
> La oración sagrada que vine a enseñarte va a llegar a ti. Una oración de nueve palabras, preparada antes de que nacieras, con el poder de destrabar lo que estaba atado, de mover lo que estaba detenido, y de devolverte la esperanza que el enemigo quiso robar. No llega a cualquiera, llega a quien fue escogido. Y si estás aquí, con este celular en la mano, es porque llegó tu momento.
> El mismo Dios que cambió la historia de Job está aquí para cambiar la tuya. Job lo perdió todo. Pero cuando oró de la manera correcta, Dios restauró su vida.
> Y te digo que, mientras ores estas nueve palabras, estaré desatando los nudos en todas las áreas de tu vida: en tu hogar, para que vuelva la paz; en tu familia, para que regrese la unión; en tu corazón, para que llegue el descanso; y en tus sueños, para que lo que estaba detenido vuelva a avanzar.
> Lo mejor de tu vida está por venir, y comienza cuando hagas la oración que preparé para ti. Toca el botón de abajo ahora. Recibe el orden correcto de las nueve palabras, y prepara tu corazón, porque esta oración fue hecha para ti. Toca el botón de abajo.

## Vozes
- **Clone reaproveitado:** "ORACAO-11 mulher" `UNDKAyEJ2rTv99l7gCy5`. Nenhuma voz nova foi criada e nenhuma foi apagada.
- **Semelhança medida com Resemblyzer** (cosseno):
  - voz do 01 contra a fonte do clone do AD 11: 0,887;
  - TTS do clone do AD 11 contra a voz do 01: 0,88–0,89 (contra a própria fonte, 0,94);
  - voz da menina do AD 11 contra a do 01: 0,57, ou seja, outra pessoa.
- **Conclusão:** a voz é a mesma personagem, ou uma muito próxima, e manter o clone garante a mesma voz da Desatadora nos dois ADs.

## Custos
- **TTS ElevenLabs:** 1.768 caracteres (8 blocos, `eleven_multilingual_v2`), cerca de US$ 0,29.
- **HeyGen:** 30 créditos medidos, de 8.947 para 8.917, para 13 trechos de lipsync somando 115,8 s. O teto era 120.

## O que saiu ou foi trocado
- **Dinheiro:**
  - "uma bênção… muito perto de chegar na tua conta" virou "muy cerca de tocar la puerta de tu casa";
  - "nas finanças, para o dinheiro chegar de todas as formas" virou "en tu hogar, para que vuelva la paz".
- **Saúde e cura:**
  - "na tua saúde, para o que os médicos não conseguiram" virou "en tu corazón, para que llegue el descanso";
  - "Jó perdeu tudo, saúde, família, bens" virou "Job lo perdió todo".
- **Promessas absolutas:**
  - "tudo foi restaurado e dobrado" virou "Dios restauró su vida";
  - "três coisas… vão ser inevitáveis" saiu;
  - "tua vida nunca mais será a mesma" virou "esta oración fue hecha para ti";
  - "trazer de volta o que o inimigo roubou" virou "devolverte la esperanza que el enemigo quiso robar".
- **Hora do dia:** "vim procurar hoje" perdeu o "hoje".
- **Ameaça:** o original não tinha.
- **Imagem:** não há moeda nem marca do Brasil. A única coisa em português na tela além da legenda era o cartão final "CLIQUE E RECEBA!", que saiu no corte.
- **Legenda queimada (amarela, y 830–975):**
  - foi removida com LaMa em todos os quadros, só dentro da máscara do texto e com EMA leve por tomada;
  - boca e queixo ficam em y≈450 e não foram tocados;
  - o fundo mediano (placa) foi testado e reprovado: o corpo dela se mexe e apareciam emendas.
- **Lipsync:**
  - 13 trechos de até 12,2 s, sem atravessar os 5 cortes de cena;
  - cada vídeo foi enviado com o áudio original em PT, e o espanhol foi como `audio`;
  - parâmetros: precision, sem duração dinâmica, mesmo formato, cfr, sem marca d'água;
  - todos conferidos: a diferença na boca ficou entre 6,6 e 8,7, contra ruído de cerca de 2,0;
  - na emenda entre trechos da mesma tomada, o salto do rosto foi de 4 a 6, igual ao de um quadro normal.
- **Áudio:**
  - a narração está a −16 LUFS por bloco;
  - o fundo musical do original (demucs `no_vocals`, sem fala residual, conferido com o whisper) foi mantido no mesmo nível relativo.

## Revisão própria
- **`revisar_ad.py --idioma es --idioma-residual pt --proibidos …`:** OK, nenhum problema.
  - Decodificação, pts e silêncio estão OK.
  - Nenhum termo proibido.
  - O idioma detectado é es (1,00).
  - A transcrição em espanhol bate com o roteiro.
- **Transcrição forçada em pt:** saiu só uma tradução do espanhol, sem fala residual em português.
- **"Toca":**
  - na transcrição longa, o whisper juntou "Toca" ao fim da frase anterior;
  - no recorte de 103,5 a 107,5 s, "Toca" aparece em 105,02 s.
- **Folha de contato com zoom na boca:** `producao\_trabalho\ad01\zoom_boca.jpg`, com 28 quadros mostrando boca e faixa. A boca está articulada, sem emenda visível na transição y 760–800 e sem resto de legenda.
- **Folhas do kit:** `producao\AD 01 - ORACION-TRES-BENDICIONES-ES-LATAM_frames.jpg` e `_revisao.jpg`.

## Pontos para a pessoa olhar
1. **A voz** é o clone do AD 11 (0,89 de semelhança com a original do 01). Vale ouvir se soa como ela.
2. **Velocidade da fala:** 1,09x, dentro do limite de 1,1x, para caber em 115 s sem cortar frases do roteiro.
3. **O cartão final "CLIQUE E RECEBA!" saiu.** O AD termina na fala, com 115,5 s em vez de 131 s. Se quiser o cartão de volta, dá para refazê-lo em espanhol ("¡TOCA Y RECIBE!").
4. **Na faixa sem legenda** (barriga e cinto), o cordão do cinto às vezes some ou aparece entre quadros. Fica quase todo sob a legenda nova.
5. **Cortes ocultos:** o original já tem cortes discretos dentro da fala (por volta de 12,4 s, 36,3 s, 67,9 s, 80,5 s e 105 s), e eles continuam no AD. Não são defeito da edição.
6. **Pronúncia:** "Job" é pronunciado "Hob", que é o correto em espanhol.

## Observação técnica
- Para a remoção da legenda, foi criado um ambiente Python com torch CUDA em `producao\_trabalho\_vg\` (RTX 4070, LaMa a 0,05 s por quadro, contra 6 s na CPU). Ele serve para os ADs 02 e 03.
- Comando: `..\_vg\Scripts\python _tmp\lama_worker.py 0 N 4`.
- Pode ser apagado depois do lote, se precisar liberar espaço.
- Scripts deste AD:
  - `_audio\montar_narracao.py` (atempo + encaixe);
  - `_tmp\analisar.py` (máscaras);
  - `_tmp\lama_worker.py`;
  - `_tmp\montar_base.py`;
  - `lipsync\cortar.py`, `lipsync\checar.py` e `lipsync\recolocar.py` (cola só o rosto do lipsync na base limpa);
  - `montar_corpo.py`;
  - `receita_ad01.json`.

---

# Refação do lipsync (v2), 08/10/2026, depois da reprovação do revisor

- **Causa:** no modo `precision`, o HeyGen só refaz a boca onde a fala PT original existe. Onde só o ES fala, ele devolve a boca do vídeo de entrada, e nas pausas do ES deixa a boca do PT.
  - O recorte sem o Jesus, sozinho, quase não ajudou: no s06, foi de 1,27 para 1,05. Trechos ≤ 8 s deram 0,97.
  - Mandar o vídeo sem áudio, com silêncio ou com o ES invertido é recusado pelo HeyGen.
- **O que resolveu:** recorte 9:16 só na mulher + áudio PT na entrada + **`mode: speed`**. No s06, o índice foi para 0,19. Detalhes em `..\LICOES-LIPSYNC.md`.
- **Trechos refeitos:** s01, s02, s05, s06, s07, s09, s11 e s12, em `lipsync2\out\v1_*.mp4`.
  - O **s08 ficou travado no HeyGen** ("running" por mais de 1,5 h) e segue a versão antiga.
- **Montagem (`lipsync2\recolocar2.py`):**
  - cola só a região de boca e queixo, com borda suave;
  - reamostra no tempo (nenhum trecho voltou com quadros a menos);
  - faz crossfade de 2 quadros nas 7 emendas sem corte de câmera;
  - as emendas de 19,47 s, 20,97 s e 49,00 s são cortes reais de câmera.
- **`fechar.py` nos trechos antigos aprovados** (s03, s10, s13): fecha a boca nas pausas do ES, sem custo.
- **Corpo e montagem:** corpo com a mesma narração (`montar_corpo.py`) e `montar_ad.py` com a mesma receita.
- **Versões anteriores guardadas:**
  - `AD01_v1_reprovado.mp4`;
  - `base_lipsync_v1.mp4`;
  - `corpo_ad01_v1.mp4`.
- **Índice de pausa no vídeo final** (conta do revisor, `lipsync2\metricas_final_pausas.txt`):
  - trechos refeitos: s01 0,20 · s02 0,39 · s05 0,26 · s06 0,16 · s07 0,20 · s09 0,10 · s11 0,51 · s12 0,43;
  - antigos com `fechar.py`: s03 0,03 · s10 0,03 · s13 0,04;
  - total: 0,19 (antes 0,86).
- **`revisar_ad.py --lipsync`:**
  - decodificação, áudio, silêncios e setas estão OK;
  - idioma: es (1,00);
  - nenhum termo proibido;
  - índice do conjunto: 0,19, APROVADO;
  - **1 problema: s08** (versão antiga, correlação com o ES de 0,13);
  - aviso no s04 (1,5 s, sem pausa).
- **HeyGen:** 89 créditos, de 8.914 para 8.825, **acima do teto de 60**. O speed custa cerca de 1 crédito/s e a cobrança chegou com atraso.

## s08 fechado (08/10/2026)
- **O job travado** (`e6fc3f79…`) continuava em "processing". Reenviei o s08 em speed com o mesmo recorte e os mesmos assets (`aacc3ea7ffb54e8baef698829063b120`). Voltou com 338 quadros, o número exato.
- **Créditos deste passo:** 6 até agora, de 8.824 para 8.818. A cobrança pode atrasar até ~1 h, e o job travado ainda pode ser cobrado.
- **Total da refação:** 96 créditos, de 8.914 para 8.818.
- **Métricas do s08:** o trecho não tem nenhuma pausa do ES de 8 quadros ou mais, por isso o índice de pausa padrão não é calculável (o checker dá AVISO, não REPROVADO). Medidas alternativas, antes → depois:
  - índice com pausas curtas (≥ 4 quadros, 14 quadros): 0,95 → **0,59**;
  - índice com pausas ≥ 3 quadros: 0,81 → 0,50;
  - correlação boca × ES: 0,13 → **0,24**;
  - correlação boca × PT: 0,27 → 0,18 (deixou de seguir o PT).
- **Vídeo final remontado:** `recolocar2.py`, depois `montar_corpo.py`, depois `montar_ad.py`. O `montar_ad.py` deu RESULTADO OK, 115,50 s e 26,4 MB.
- **`revisar_ad.py --lipsync`: OK, nenhum problema encontrado.**
  - Índice de pausa do conjunto: 0,19, APROVADO.
  - Avisos só em s04 e s08, ambos por "trecho sem pausa na voz nova".
  - Idioma: es (1,00). Nenhum termo proibido.
- **Índices finais por trecho:** s01 0,23 · s02 0,38 · s03 0,03 · s05 0,23 · s06 0,17 · s07 0,17 · s09 0,11 · s10 0,03 · s11 0,51 · s12 0,42 · s13 0,05 · total 0,19.
