# Lote SB PL: oferta "modlitwa na żywo" (aprovado com "confirmo" em 16/10/2026)
- **Mercado:** Polônia. Polonês natural e neutro, tom espiritual e católico (a Polônia é muito católica, então use o vocabulário litúrgico correto).
- **Nome do santo:** "San Benito" vira **"Święty Benedykt"**, declinado corretamente (św. Benedykta, do św. Benedykta…).
- **Destino:** a oração ao vivo em polonês.
- **CTA final padrão:** **"Dotknij «Dowiedz się więcej» poniżej i dołącz do modlitwy na żywo"**. O botão do Meta é LEARN_MORE, que em polonês é "Dowiedz się więcej".
- O vídeo nunca mostra produto nem preço.
- **Compliance:** mesmo teor do original/EN (promessas e urgência), sem suavizar. É decisão da pessoa.

## Base: o lote EN pronto e o lote IT recém-feito
- **Base EN:** cada vídeo PL parte da versão EN do mesmo número, em `C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\<pasta EN>\`. O `_trabalho\` dela tem a base limpa, o heygen_in com o áudio ORIGINAL, o demucs e os scripts.
- **Base IT, que é o modelo mais recente e já corrigido:** `C:\Users\PICHAU\Downloads\SB-IT-OFERTA-LIVE\<mesma pasta>\`.
  - Leia o `_roteiro-it.txt` e os scripts `_trabalho\*_it.*`. Copie e adapte para PL.
  - Os agentes do IT corrigiram defeitos do EN. Reaproveite as correções:
    - OP2: offset do clipA.
    - ADS 9: 1 quadro com "EN DIRECT".
    - JESU V07: jump cut na pausa e sem vírgula em "Oggi ascolterai".
    - ADS 12.1 GD: carimbo "SCADUTO" no gancho, que no PL vira "PRZETERMINOWANE" ou "ZALEGŁE".
    - ADS 6: cartão do topo.
- **Não escreva nada nas pastas EN e IT.** Copie para o seu `_trabalho` o que precisar.
- Leia também `C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\BRIEFING_LOTE_EN.md` e `C:\Users\PICHAU\Downloads\SB-IT-OFERTA-LIVE\BRIEFING_LOTE_IT.md`.

## Método B
1. **Roteiro PL** a partir do EN/IT:
   - tradução natural, duração parecida;
   - CTA da live;
   - texto na tela (títulos, cartões, selo LIVE → "NA ŻYWO") em polonês;
   - o polonês costuma ficar mais longo: enxugue sem perder promessa nem urgência.
2. **Voz ElevenLabs:**
   - Chave em `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env`. Não imprima.
   - Use eleven_multilingual_v2 (ou v3) com language_code "pl", se aceitar.
   - Use a MESMA voz do EN/IT: Jesus The Chosen AkQxVSf1kENGmX9WjeDE ou Brian nPczCjzI2devNBz1zQrb.
   - A conta está no LIMITE de vozes: não crie, não clone e não apague.
   - Confira com o whisper `pl` se a pronúncia saiu polonesa (ś, ć, ż, ł, rz, cz).
3. **Lipsync HeyGen** mode **speed**:
   - Entrada com o áudio ORIGINAL (heygen_in do EN), áudio PL separado, trechos ≤ ~12 s.
   - Aceite: `checar_lipsync.py` com pausa ≤ 0,6. Fora disso, corte nas fronteiras de palavra e cubra a pausa com b-roll ou jump cut. Não retoque a boca.
   - Job parado há mais de 45 min: reenvie igual. **Não reenvie antes disso**: no IT houve job duplicado por reenvio aos 2 min.
   - Cor bt601 fixa e `-reinit_filter 0`. Confira se há salto de pts no áudio.
4. **Legenda PL** palavra a palavra, no estilo do EN/IT.
   - **A fonte precisa ter os diacríticos poloneses** (ĄĆĘŁŃÓŚŹŻ em caixa alta). Teste a fonte antes. Se a Anton/fonte do EN não tiver algum glifo, troque por uma equivalente que tenha.
   - Setas no CTA (mesma cor do EN daquele vídeo), música do original a ~-32 LUFS.
5. Resolução igual à do EN.

## QA
- **`revisar_ad.py` do kit:**
  - Rode de `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\`, com PYTHONIOENCODING=utf-8 e whisper **pl**.
  - Os proibidos vão num .txt UTF-8:
    - resíduo de inglês: "Tap", "Learn More", "live prayer", "Saint Benedict";
    - resíduo de italiano: "Scopri", "preghiera", "San Benedetto", "diretta";
    - resíduo de espanhol/francês: "San Benito", "en vivo", "oración";
    - preço: "zł", "$", "€".
- Confira a folha de contato, os diacríticos na legenda (zoom), a boca nas pausas, o silêncio no fim e os quadros soltos.
- Depois, 1 subagente revisor independente rápido. Corrija o que ele achar. **Ele não pode matar processos (taskkill) de outros agentes.**
- NÃO abra os vídeos.

## Saída
Na pasta `C:\Users\PICHAU\Downloads\SB-PL-OFERTA-LIVE\<NN>_<NOME>\`:
- `SB-PL-<NOME>.mp4`;
- `SB-PL-<NOME>_roteiro-pl.txt`, com o roteiro EN × PL e as decisões;
- `SB-PL-<NOME>_texto-anuncio.txt`:
  - campos: Tytuł ≤40, Tekst główny, Wersja krótka ≤125 e Przycisk: LEARN_MORE "Dowiedz się więcej";
  - adaptado do texto IT/EN, sem preço, chamando para a modlitwa na żywo;
  - notas internas só depois de uma linha "Notatki:";
- `SB-PL-<NOME>_frames.jpg`.

Regras de trabalho:
- Trabalhe só em `<NN>_<NOME>\_trabalho\`.
- No fim, crie `PRONTO.txt`.
- Apague os intermediários pesados e mantenha os scripts e o mp4.

**Painel:** `python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa sbpl-<nome> "<título>" --texto "..."` (e img/custo/fim).

**Custos:**
- ElevenLabs custa centavos e o HeyGen speed usa os créditos do plano.
- Não meça o saldo.
- Nada pago fora disso.

**Relatório final (curto):** arquivo, duração, voz, nº de jobs HeyGen e o que ficou imperfeito, com os tempos.
