---
name: analise-neural-criativo
description: "Prevê, antes de veicular, se um vídeo vai gerar emoção/atenção: timeline de picos de saliência visual e auditiva, risco de drop-off e diagnóstico de hook, inspirado no TRIBE v2 da Meta. Use para simular resposta cerebral a um criativo antes de subir pra mídia."
---

# Análise Neural-Preditiva de Criativo ("Neuro-Preview")

## Contexto

O TRIBE v2 (Meta FAIR) é um modelo que prevê atividade cerebral (fMRI, ~70 mil voxels, 1 predição/segundo) a partir de vídeo+áudio+texto, treinado em 1.100+ horas de scans de 720 pessoas. Não é acessível como ferramenta rodável aqui (pesos ficam no Hugging Face, fora do allowlist de rede deste ambiente, e são pesados demais pra baixar via anexo). Esta skill substitui o modelo por um **proxy heurístico**: em vez de prever ativação de voxel, o agente lê o vídeo (frames + áudio + transcrição) e razoa sobre os mesmos sinais que a literatura de neurociência associa a resposta cerebral forte, produzindo uma timeline interpretável de "chance de emoção/atenção" por trecho do vídeo.

Isso não é uma simulação de fMRI real — é uma leitura qualificada e estruturada, com o vocabulário e a granularidade (segundo a segundo) que o TRIBE v2 usaria, aplicada por um agente com visão e raciocínio.

## Quando usar

- Usuário manda um vídeo (anúncio, VSL, UGC, criativo de COD) e pergunta se vai "prender", "gerar emoção", "engajar", "funcionar", ou pede pra "rodar o TRIBE"/"simular o cérebro".
- Antes de escalar um criativo, como camada extra de diagnóstico junto com `diagnostico-criativo`.
- Para comparar 2+ variações do mesmo vídeo e decidir qual tem timeline de atenção mais forte.

## O que NÃO fazer

- Não afirmar que o resultado vem de um modelo de fMRI real ou que é cientificamente validado. Deixar claro (uma vez, não repetir toda hora) que é uma leitura heurística inspirada no TRIBE v2, não a saída do modelo.
- Não inventar números de ativação cerebral, regiões específicas do cérebro ativadas, ou métricas pseudo-científicas ("78% de ativação do córtex visual"). Isso é enganoso. Falar em termos de sinais observáveis e risco/oportunidade.

## Pipeline

### 1. Extração
Com o vídeo em mãos (ffmpeg disponível no shell):
- Extrair 1 frame a cada 1s (ou 0.5s nos primeiros 3s, onde a granularidade importa mais).
- Extrair o áudio e transcrever com timestamps (word-level se possível).
- Anotar duração total, formato (feed/stories/reels), presença de legendas embutidas.

### 2. Leitura visual, frame a frame
Para cada frame (ou a cada corte de cena), o agente registra:
- **Rosto em quadro?** Close-up de rosto humano é o gatilho mais forte de resposta cortical (face processing). Rosto + emoção expressa (surpresa, alegria, choque) pontua mais alto que rosto neutro.
- **Corte/mudança brusca?** Trocas de plano, zoom, movimento de câmera brusco, ou pattern interrupt visual geram pico de saliência (resposta a novidade/movimento), mesmo sem carga emocional — é engajamento "perceptual puro" (o TRIBE v2 mostra isso em conteúdo tipo ASMR/"satisfying": picos de saliência sem componente emocional/narrativo).
- **Texto na tela?** Chamada, número, promessa. Texto que contradiz ou reforça o que é dito gera picos de processamento de linguagem.
- **Contraste/cor/composição muda de forma abrupta?**

### 3. Leitura auditiva
- Silêncio → som súbito (ou o contrário) = pico de saliência auditiva.
- Mudança de prosódia na voz (fala mais rápida, sussurro, grito, pausa dramática).
- Música: entrada/corte de trilha, batida que sobe, sting.
- Efeitos sonoros (whoosh, notificação, risada) — gatilhos de atenção reflexiva.

### 4. Leitura narrativa/semântica (via transcrição)
- Hook nos primeiros 3s: pergunta, afirmação contra-intuitiva, promessa ousada, ou mistério/curiosity gap → prediz maior retenção inicial.
- Estrutura emocional: setup → tensão/conflito → virada/prova → payoff/CTA. Cada uma dessas transições é onde se espera pico de resposta (a mudança de estado é o que dispara sinal, não o platô).
- Prova social, depoimento, transformação (antes/depois) — ativa relevância pessoal/identificação, camada emocional mais forte que só saliência perceptual.
- Repetição sem variação (mesmo plano, mesmo tom, sem novidade por 5s+) = risco de queda de atenção (drop-off).

### 5. Síntese em timeline
Montar uma tabela por segundo (ou por cena) com:

| tempo | o que acontece | sinal visual | sinal auditivo | sinal narrativo | leitura |
|---|---|---|---|---|---|

"leitura" = classificação qualitativa: **pico perceptual** (saliência sem emoção — prende olho, não fideliza), **pico emocional** (identificação, tensão, payoff — o que gera ação/recall), **platô neutro** (sem gatilho — ok se curto, risco se longo), **risco de drop-off** (sem novidade por tempo demais, ritmo caindo).

### 6. Diagnóstico final
Responder objetivamente:
- **Hook (0-3s) passa ou não?** Por quê.
- **Onde estão os picos de emoção reais** (não só perceptuais) — são eles que geram lembrança e ação, então são o que mais importa pra conversão.
- **Onde tem risco de queda** — trechos longos sem gatilho, ritmo repetitivo, ausência de rosto/voz por tempo demais.
- **Timing do último pico vs. fim do vídeo/loop** — se o vídeo é pra feed que faz loop (Reels/TikTok/Kwai), um pico de saliência perto do fim que empurra pro replay é bom sinal (o TRIBE v2 mostrou isso em conteúdo "satisfying" que viraliza).
- **Nota geral de "chance de gerar emoção"**: baixa / média / alta, com justificativa em 2-3 frases — nunca um número falso de precisão científica.
- **Recomendação prática**: o que cortar, reordenar, ou reforçar (ex: "mover o depoimento pra depois do hook, o meio tá sem gatilho por 8s").

## Formato de output pro usuário

Resposta direta, sem markdown pesado (o usuário prefere output pronto pra produção): abrir com o veredito (hook passa/não passa, nota geral), depois a timeline resumida (só os pontos de virada, não segundo a segundo inteiro a não ser que peçam), depois recomendação de corte/ajuste. Se o usuário estiver comparando variações, montar tabela comparativa lado a lado.

## Limitação a declarar uma vez

No primeiro uso da sessão, deixar claro em uma frase: isso é uma leitura heurística inspirada nos princípios do TRIBE v2 (Meta), não a execução do modelo real — os pesos não são acessíveis neste ambiente. Depois disso, não repetir o disclaimer a cada resposta.