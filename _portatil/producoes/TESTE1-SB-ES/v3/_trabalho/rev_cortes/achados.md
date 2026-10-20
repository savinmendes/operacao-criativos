# Revisão de cortes, b-roll, áudio, legenda e texto: SB-ES_NOTICIA-AURELIO_v3_FICTICIO.mp4

**Versão revisada:** o arquivo foi regravado durante a revisão, às 16:22:36. Esta revisão vale para a versão nova: 169,20 s, 720x1280, 30 fps, md5 `c26a65afa5f328c3fb2feabd5f18ae53`, timeline de 16:17. Comecei pela versão das 15:17 (169,50 s). Os defeitos dela que a versão nova corrigiu estão no fim.

**Como verifiquei:**
- Detecção de corte quadro a quadro e comparação de cada plano com todos os outros (correlação em 3 a 5 quadros por plano, sem usar o timeline).
- Folhas de contato e quadros em resolução cheia em todas as emendas suspeitas.
- Whisper medium em espanhol do vídeo inteiro, mais whisper em trechos isolados.
- Pts dos pacotes de áudio com ffprobe, silencedetect, ebur128 por janela e procura de estalos nas fronteiras dos itens.
- Legenda: comparei os tempos do `leg.ass` com os tempos por palavra do whisper (389 palavras).
- OCR (RapidOCR) a 2 fps no vídeo todo e correlação do selo quadro a quadro.

Os arquivos de apoio ficam nesta pasta: `shots_*.jpg`, `seam2.jpg`, `preto.jpg`, `cuts2.jpg`, `b04_06.jpg`, `whisper.json`, `ocr.json`.

---

## GRAVE

### 1. Emenda da briga em 2,67 s (quadro 80): o carrinho muda de modelo e de lugar
O take não é contínuo na emenda Kling → Seedance. A versão nova cortou 0,065 s (`abertura0a` 0–2,67 e `abertura0b` a partir de 2,735), mas o salto continua visível. Ver `seam2.jpg`, quadros 77 a 82.
- No quadro 80 o carrinho ganha a prateleira lateral com o isopor branco, que antes não existia.
- O carrinho também desce e vai para a direita, e o agressor muda de pose.
- O PiP da mulher some exatamente nesse quadro, o que deixa o pulo ainda mais evidente.

**O que está certo nesse trecho:** os mesmos 2 homens do começo ao fim, sem vai-e-volta do carrinho de 2,73 s a 9,5 s (amostrei a cada 0,5 s em `briga_seq.jpg`), e sem corte no resto do take.

**Correção:** escolher um dos dois caminhos:
- Gerar o trecho de 0 a 2,7 s com o mesmo carrinho do Seedance (com prateleira e isopor). Pode ser um take único, ou um i2v a partir do primeiro quadro do Seedance.
- Ou esconder a troca: manter o PiP da mulher até depois da emenda, até ~3,2 s, e fazer um punch-in de 112% exatamente no quadro 80. Assim a troca vira um "corte de câmera" e não um pulo.

---

## MÉDIO

### 2. Quadro das 12 palavras (e19), de 80,67 s a 89,90 s: o texto da arte não bate com a narração e a legenda
- A arte mostra **"Cruz"**; a fala e a legenda dizem **"crux"**.
- A arte mostra **"Silentio"**; a fala e a legenda dizem **"silentium"**.

Confirmado no OCR de todos os quadros do intervalo.

**Correção:** trocar só esses dois rótulos na arte (o `e19.jpg` está em `final/mont`), com a mesma fonte e as mesmas plaquinhas. Outra saída é trocar a legenda para "cruz" e "silentio", mas aí a legenda deixa de seguir o roteiro aprovado.

### 3. Tela preta de 5 quadros entre "¡Claro!" e o padre (54,80–54,93 s, quadros 1644–1648)
- A moldura EN VIVO aparece sobre fundo preto, e a legenda "presten mucha" já está na tela antes de o padre aparecer (`preto.jpg`).
- Isso vem da regra `src="preto"` do `montar_v3.py` (entrada da live a partir do preto), então é intencional. Mesmo assim, 0,17 s de preto parece falha de render.

**Correção:** uma de duas:
- Alongar para ~0,4 s com um "conectando…" ou spinner sobre o preto, para ler como live entrando.
- Ou eliminar o preto e entrar direto no quadro 1649. Nesse caso, segurar a legenda "presten" até 54,97 s.

---

## LEVE

### 4. Setas TOCA «VER MÁS» entram 3 quadros antes do P07 (155,43 s)
- As setas entram 3 quadros antes do corte para o padre, que acontece em 155,53 s (quadro 4666).
- Nesses quadros, setas e legenda ficam sobre o b-roll das mãos com o colar (s20), ainda no fim do P06, com a legenda "oraciones" já na posição alta de CTA.

**Correção:** usar o quadro real do corte como `cta_t` (155,533), ou cortar o s20 em 155,448.

**O que está certo:** daí até o fim (169,2 s) as setas ficam o tempo todo. A legenda fica em y≈840, acima do "TOCA" (y≈975) e nunca encoberta. As pontas das setas encostam no topo da barra "Comentarios desactivados" (y≈1130) da moldura live. É aceitável, mas dá para subir as setas uns 15 px.

### 5. B04/B05 diferem um pouco do roteiro
- **B05 (12,5–15,5 s):** chegam **~7 pessoas**, contra "~5" no roteiro.
- **B04 (9,5–12,5 s):** o vendedor está sozinho e o carrinho vazio, mas ele aparece em pé atrás do carrinho, sem leitura clara de "cabeça baixa / triste".

**Correção:** só se a pessoa fizer questão. A sequência vazio → poucas pessoas → fila cheia funciona e a ordem está certa.

**Trilha triste:** entra no B04. Ela é específica (`trilha/triste_1.mp3`, piano e cordas em tom menor) e soa a ≈ -17,5 LUFS na janela de 9,6 a 12,4 s, bem audível. Depois passa para a trilha de esperança no B05 e no B06 (≈ -19,3 e -16,9 LUFS) e abaixa sob a repórter.

### 6. Cutaway da vela acesa (k13) sobre a repórter (21,43–22,27 s), na frase "volverse viral, el carrito"
Ninguém fala de vela ou oração nesse momento, então o plano destoa do assunto.

**Correção (opcional):** trocar o k13 por um plano de rua ou carrinho, ou mover o k13 para o bloco do padre. Os outros cutaways da entrevista combinam com a fala: rosário em "San Benito" (34,8 s) e homem no morro em "Al día siguiente" (39,6 s).

### 7. Primeiro evento do `leg.ass` com início negativo (`-1:59:59.96`)
O render saiu correto: "gente después" aparece desde 0,00 s. Mesmo assim, é um tempo inválido que outro player ou o libass pode descartar.

**Correção:** limitar o início a `0:00:00.00` no gerador da legenda.

---

## OK: verificado, sem problema

- **B-roll sem repetição:** são 69 planos detectados. Comparei todos os pares e nenhum plano de b-roll aparece duas vezes.
  - Os únicos pares parecidos são planos diferentes da mesma cena do carrinho (B04×B06, briga×B05: correlação ≈ 0,87).
  - Dentro do padre, as semelhanças são takes da própria live (esperado).
  - O s24 (homem rezando com vela, 135,8 s) agora entra no lugar do não usado. É outro homem e outro plano em relação ao e10 (75,2 s).
- **Quadros soltos ou flash:** não há plano de 1 quadro. Os da versão anterior (114,77 s e 130,43 s) sumiram, e as emendas em 114,5 s e 130,13 s estão limpas (`cuts2.jpg`).
  - Os pulos em 39,6, 43,9, 56,1, 128,2 e 141,4 s são punch-in 100/112% propositais nos cortes de fala e não são defeito.
- **Tela preta:** só a do item 3.
- **Texto em português:** o OCR em 338 quadros não achou nenhum dos termos procurados ("ao vivo", "notícia", "perfil", "Pix", "R$", "você", "não", "ção", "ç", "ã").
  - Os prints usam "US$ 13.000,00", "Mi cuenta" e "Transferencia recibida".
  - A moldura live diz "EN VIVO" e "Comentarios desactivados"; o cabeçalho diz "Fe en Noticias / Trabajador es humillado y algo impactante sucede".
- **Mancha da legenda antiga:** não há área borrada sem legenda por cima. Conferi em resolução cheia os intervalos sem legenda (9,53–18,55 s e 89,08–89,56 s).
- **Selo "VIDEO FICTICIO":** está no topo direito em todos os 5076 quadros (correlação mínima de 0,96 com o modelo).
- **Áudio, texto:** o whisper medium em espanhol bate com o roteiro do B01 ao P08.
  - Inclui "disponible **en este sitio** para que puedan hacerla…" (139,7–141,7 s) e a frase do colar inteira: "Y quien obtenga el Grimorio hoy recibirá de regalo un collar de plata de San Benito, el mismo que se usaba en sus oraciones." (145,6–155,4 s).
  - O "excursión" (~110,6 s) sumiu na transcrição longa, mas o whisper no trecho isolado ouve "una excursión que hice a Italia" com probabilidade 0,97.
  - A oração com as 12 palavras está completa.
- **Salto de pts:** nenhum. São 7930 pacotes, com folga máxima de 1 µs, e o áudio decodificado tem 169,13 s.
- **Silêncios acima de 0,7 s:** nenhum, nem com limiar de -40 dB nem de -30 dB.
- **Loudness:** o integrado é -14,4 LUFS, com pico real de -3,1 dBFS. A trilha do padre foi mixada a -32 LUFS antes da normalização (≈ -31,4 depois). Nas pausas da fala o fundo fica em torno de -33 a -36 dBFS RMS.
- **Estalos:** nenhum nas fronteiras dos itens (todas têm fade de 12 ms), incluindo as emendas novas A01a/b (27,68 s) e A02a/b (43,89 s).
- **Legenda:** 389 palavras alinhadas ao whisper, todas as do roteiro e sem cortes. A legenda adianta em média 0,08 s, e 95% das palavras ficam a menos de 0,21 s da fala.
  - Pontos amostrados (legenda → fala): 5,03 / 19,98 / 33,07 / 45,03 / 60,19 / 94,45 / 115,07 / 139,63 / 149,99 / 159,86 / 167,09 s, com diferenças de -0,15 a 0,00 s.
  - "siete" aparece por extenso, de acordo com o roteiro.

## Corrigido na versão nova (era defeito na das 15:17)
- **Quadro solto com fantasma** da mulher rezando em 114,77 s: corrigido.
- **Flash de 1 quadro** do grimório em 130,43 s: corrigido.
- **Repetição de um mesmo trecho de áudio:** não houve nas emendas novas da entrevista.
