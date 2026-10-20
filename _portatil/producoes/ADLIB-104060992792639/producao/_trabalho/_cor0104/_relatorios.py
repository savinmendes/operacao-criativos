# -*- coding: utf-8 -*-
# insere a secao "Correcao de cor" no topo dos RELATORIO dos ADs 01-04 (rodar uma vez)
from pathlib import Path
B = Path(__file__).resolve().parent; T = B.parent
comum = (B / "_comum_relatorio.txt").read_text(encoding="utf-8")
cab = lambda n: (f"## Correção de cor (08/10/2026, depois da REVISAO-LOTE-C)\n\n"
                 f"A versão anterior está em `_trabalho\\ad{n}\\_antes_cor\\`: vídeo, folhas, `base_lipsync`, `base_sem_legenda`, corpo, `montar_corpo.py` e relatório.\n\n{comum}\n")
sec = {}
sec["01"] = cab("01") + r"""**O que foi feito:** o `_trabalho\_cor0104\recolocar_cor_0102.py` refaz, **numa geração só**, a `base_sem_legenda` e a `base_lipsync` do 01 e também as do 02, que reaproveitam o corpo do 01 a partir do quadro 242.
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

"""
sec["02"] = cab("02") + r"""**O que foi feito:** a base do 02 sai pronta do mesmo `_trabalho\_cor0104\recolocar_cor_0102.py` que refez o 01, numa geração só. Ver o RELATORIO do 01.
- **Gancho (q0–285):**
  - `UNICOS_HD\02.mp4` + o LaMa do gancho (`_tmp\lama`, mesma máscara e EMA);
  - `ls_h1_speed.mp4` colado no recorte inteiro, como no `colar_h1.py`;
  - afim medida no recorte fora da boca. A saída estava −2,1/−1,4/−1,7 BGR.
- **Do quadro 286 em diante:** são os mesmos quadros do 01 a partir do 242, gravados direto da geração do 01, sem cópia intermediária.
  - Com isso entram os mesmos s03, s10 e s13 com `fechar.py` e o s08 em speed.
- **`montar_corpo.py`:** agora só monta o corpo, porque a base já vem pronta. A versão anterior está em `_antes_cor\`.
- **Remontagem:** `montar_ad.py receita_ad02.json`. Resultado: RESULTADO OK, 117,00 s, CTA em 106,44 s.
- **Conferência:** boca nova × anterior com diferença de estrutura de 1,71. Os picos ficam nas mesmas pausas fechadas do s13.

**Medidas** (`cor.py`/`brilho.py` com `loteC\escolha_02.json`; saídas em `revisao\loteC\cor0104\`):

| | Antes | Depois |
|---|---|---|
| Área colada − rosto (cor.py / brilho.py) | −5,0 / −5,1 | **+0,2 / 0,0** |
| Pior trecho | s07 −6,8 (s01resto −10,2, 3 amostras) | s13 −1,7 (s01resto −3,6 no brilho, 3 amostras; pela mediana +0,5) |
| Rosto × original | −10,7 (U +1,9 / V −3,0) | **−0,6** (U −0,2 / V −0,1) |
| Fundo × original | −7,6 | **−0,9** |
| Degrau pela mediana (elipse × anel) | — | 0 a ±1 em todos os trechos |

**Revisão** (`revisar_ad.py --lipsync`, PowerShell, `_lote\proibidos.txt`; trechos em `_cor_rev\`):
- es (1,00), nenhum termo proibido, nenhum silêncio, 2 cortes, setas no último quadro.
- **Índice de pausa do conjunto:** 0,21 antes e **0,23** depois.
  - Por trecho: s06 0,20 → 0,26 e s07 0,20 → 0,25, ainda aprovados. Os outros variam até ±0,04.
- **"PROBLEMA" s04 nos dois finais** (0,68/0,50 → 0,69/0,49): é o mesmo trecho antigo do 01, já aceito.
- **Pendente de antes, sem mudança:** os ~4 quadros do "ti" sem voz em 9,53 s. O vídeo não foi aberto.

---

"""
sec["03"] = cab("03") + r"""**O que foi feito:** `_trabalho\_cor0104\recolocar_cor_03.py`, numa geração só. Faz o mesmo que `_tmp\montar_base.py` + `lipsync\recolocar.py` + `_tmp\loteA.py quadro`.
- **Base:**
  - original + LaMa (`_tmp\lama` e `_tmp\mask`, mesma EMA e mesma zeragem nos cortes);
  - split 1198–1436 com a `_tmp\broll_cruz.mp4`, que já estava na leitura certa porque foi feita por ffmpeg (conferido contra o 06.mp4).
- **Trechos do HeyGen:** colados no recorte inteiro, como antes.
  - A afim foi medida no recorte fora da boca.
  - As saídas já batiam com a base (desvio de +0,1). Só o p07 estava −1/−3/−5 BGR.
  - O escuro do 03 era só da base.
- **Mantido:**
  - as mesmas emendas: 9 cortes e 5 crossfades de 2 quadros;
  - **o quadro 9,40 s (q282) com a boca do q283** (lote A);
  - o **ambiente de sala** do lote A (`_audio\room_tone.wav`, o mesmo `montar_corpo.py`).
- **Conferência:** boca nova × anterior com diferença de estrutura de 1,64 e máximo de 2,3. Não há quadro diferente.
- **Remontagem:** `montar_corpo.py` e `montar_ad.py receita_ad03.json`. Resultado: RESULTADO OK, 96,30 s, CTA em 60,46 s.

**Medidas** (`cor.py`/`brilho.py` com `loteC\escolha_03.json`; saídas em `revisao\loteC\cor0104\`):

| | Antes | Depois |
|---|---|---|
| Área colada − rosto (cor.py / brilho.py) | +0,7 / +0,8 | **+1,6 / +1,4** |
| Rosto × original | −8,5 (U +3,0 / V −2,6) | **+0,1** (U 0,0 / V +0,3) |
| Fundo × original (sem o p07, que tem a cruz) | −7,4 | **+1,6** |
| Degrau pela mediana (elipse × anel) | −2 (0 a −2 por trecho) | **+1** (0 a +1 por trecho) |

- **p08, p12, p13 e p15 ficam com +3,6 a +4,7 nas caixas fixas do `cor.py`. Não é cor:**
  - eles já davam +3 a +4 antes;
  - é a boca nova (fechada, de outro formato) dentro das caixas fixas do lábio e do queixo;
  - a mediana dentro da elipse contra o anel de pele, que ignora o ± do lábio, dá 0 a +1 em todos os trechos.

**Revisão** (`revisar_ad.py --lipsync`, PowerShell, `_lote\proibidos.txt`; trechos em `_cor_rev\`):
- es (0,96), nenhum termo proibido, nenhum silêncio.
- **Índice de pausa do conjunto:** 0,06 antes e **0,07** depois. Por trecho, a variação fica em ±0,02.
- **"PROBLEMA" que já existia antes:**
  - "quadro solto" em 9,13/9,27/9,37 s é o clarão do original (falso positivo já aceito);
  - p02 "acompanha mais o original" já aparecia antes (0,64/0,50, agora 0,58/0,48). É um trecho de 1,1 s.
- **Saiu** o falso "setas sobre a faixa escura".
- O vídeo não foi aberto.

---

"""
sec["04"] = cab("04") + r"""**O que foi feito:** `_trabalho\_cor0104\recolocar_cor_04.py`, numa geração só. Faz o mesmo que `_tmp\montar_base.py` + `lipsync\recolocar.py` com o `plano.json`.
- **Base:**
  - original + LaMa (`_tmp\lama` e `_tmp\mask`, inclusive o clarão refeito pelo `lama_flash.py`);
  - as mesmas trocas das cenas do depoimento pelo overlay dos anjos.
- **Trechos:** mesma colagem de antes.
  - MediaPipe na saída e elipse do nariz ao queixo com EMA.
  - Nos quadros sem rosto, usa a elipse final do trecho, como antes.
  - O w2 continua coberto pelo zoom no overlay.
  - O w11 e o w12 mantêm o crossfade linear na sobreposição.
- **Cor de cada trecho:** afim medida num **anel de pele** em volta da elipse (1,3x a 2,4x). A saída estava −1/−3/−5 BGR.
  - O g1 (menina de perfil) só tem rosto detectado em 11 de 290 quadros, então o ajuste dele usa 3 amostras. O desvio é o mesmo dos outros trechos.
- **Conferência:** boca nova × anterior com diferença de estrutura de 1,55 e máximo de 1,9. A montagem foi reproduzida quadro a quadro.
- **Remontagem:** `montar_corpo.py` e `montar_ad.py receita_ad04.json`. Resultado: RESULTADO OK, 83,10 s, CTA em 70,15 s.

**Medidas** (`cor.py`/`brilho.py` com `loteB\escolha_04.json`; saídas em `revisao\loteC\cor0104\`):

| | Antes | Depois |
|---|---|---|
| Área colada − rosto (cor.py / brilho.py) | −2,4 / −2,2 | **−0,6 / −0,4** |
| Pior trecho | w10 −3,2 | w10 −1,1 / w12 −1,0 |
| Rosto × original | −8,6 (U +2,7 / V −2,6) | **−0,1** (U +0,1 / V 0,0) |
| Fundo × original | −5,5 | **+0,2** |
| Degrau pela mediana (elipse × anel) | — | 0 a −1 em todos os trechos |

- **Linhas que não comparam rosto com rosto:**
  - o "w2coberto" é o zoom no overlay, não o rosto original;
  - o fundo de w8 e w10 é o overlay dos anjos no lugar do carro.

**Revisão** (`revisar_ad.py --lipsync`, 11 trechos, PowerShell, `_lote\proibidos.txt`; trechos em `_cor_rev\`):
- **OK, nenhum problema.** es (1,00), nenhum termo proibido, setas no último quadro.
  - O silêncio em 82,36–83,10 s é o fade final.
- **Índice de pausa do conjunto:** 0,30 antes e **0,26** depois.
  - Por trecho: w12 0,82 → 0,53, w1 0,56 → 0,48, e os outros variam ±0,03.
- **Saiu** o falso "quadro solto" do clarão em 9,67 s.
- O vídeo não foi aberto.

---

"""
for n, s in sec.items():
    p = T / f"ad{n}" / "RELATORIO.md"; t = p.read_text(encoding="utf-8-sig")
    if "Correção de cor (08/10/2026" in t: print("ja tem", n); continue
    i = t.index("\n") + 1
    p.write_text(t[:i] + "\n" + s + t[i:], encoding="utf-8"); print("ok", n)
