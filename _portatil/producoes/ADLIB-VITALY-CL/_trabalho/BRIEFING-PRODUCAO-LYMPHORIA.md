# Briefing: produção Vitaly → Lymphoria (Chile, 09/10/2026)

A pessoa aprovou a produção.
- **Não pergunte nada.**
- **Nunca leia `.env`.**
- **Não abra players.**

**Escopo:** só os vídeos e imagens da sua tarefa. Não mexa em loja, tema nem produtos.

## Decisões da pessoa
- **Marcas e autorizações:** a marca Vitaly é da pessoa. Clonar a voz da narradora ou criadora do próprio vídeo é **permitido**, e o lipsync HeyGen também. A criadora do V09 **autorizou** o uso.
- **Dose:** use **a mesma que o próprio vídeo diz**.
- **Oferta Lymphoria (Chile), para o fim e para os textos:**
  - Compre 1, Reciba 2: $34.990;
  - Compre 2, Reciba 4: $59.990;
  - Compre 3, Reciba 6: $79.990;
  - Envío gratis, **Pagas al recibir**, garantia de **90 días**.

  Onde o vídeo cita "2x1", "Lleva 2 Paga 1", "70% OFF" ou Cyber Day, troque por **"Compre 1, Reciba 2"**. Tire Cyber Day, meses vencidos e "150 mil mamás". Onde aparecer garantia de 45 ou 60 dias, troque por **90 días**.
- **Marca:**
  - toda aparição de **Vitaly** (falada, escrita ou no rótulo) vira **Lymphoria**;
  - frascos de outra marca (Nature's Sunshine etc.) viram Lymphoria ou são cortados ou desfocados;
  - URL vira o CTA "Toca el botón de abajo".
- **Corte obrigatório:** a camiseta política "ABOLISH ICE" (V01 em 6–7 s e V25 em 10 s). Corte, ou desfoque.

## Suavização (só nos vídeos marcados; o resto fica igual)
**Regra:** a frase nova tem **sentido parecido** com a original e **o mesmo tempo** do trecho trocado (±0,2 s). Não muda a duração do vídeo.
- **Fala:**
  - voz clonada da própria pessoa que fala, no mesmo ritmo e LUFS;
  - se o rosto fala no trecho, HeyGen lipsync em `mode speed`, conforme o `CLAUDE.md`.
- **Texto na tela:** caixa opaca no mesmo estilo e posição, com o texto novo.
- **O que suavizar** (os tempos estão em `_estudo\VNN.md`):
  - **Peso em kg vira desinchar ou medidas:**
    - "Bajé 7 kilos" → "Me deshinché y bajé tallas";
    - "-7 kg de HINCHAZÓN" → "Adiós hinchazón";
    - "114 kg → 84 kg" → "Antes / Después" ou "Adiós hinchazón";
    - "bajaste de peso" → "te deshinchaste".
  - **Doença ou câncer vira inchaço e bem-estar:** "infecciones y células cancerosas" / "migrañas… enferma" → "pesadez, cansancio e hinchazón".
  - **Interação com remédio:** "no interfiere con la mayoría de los medicamentos" → "100% natural, sin estimulantes" (mesmo tempo). "Consulta a tu médico si estás en tratamiento" pode ficar.
  - **"Médica" ou "nutrióloga" como prova:** pode se apresentar, mas sem prometer cura.
- **Toda troca vai para o registro** `TROCAS.md` da sua tarefa: vídeo, tempo inicial e final, texto ou fala original → nova, e tipo (voz em off, voz + lipsync ou texto na tela).

## Material
- **Estudos:** `C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\_estudo\VNN.md` (tempos de cada troca) e `_estudo\_dados\` (transcrição e OCR).
- **Originais:** `ADLIB-VITALY-CL\VIDEOS\`.
- **Ativos Lymphoria (reaproveite antes de gerar):**
  - `C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\` e `_trabalho\`;
  - `C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\` e `_v2_corrigidos\`;
  - vencedores em `C:\Users\PICHAU\Downloads\APROVADOS E VALIDADOS TIKTOK\`, como referência do fim;
  - frasco neutro no projeto Flora da Lymphoria, nó n59.
- **Kit:** `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\`. Leia o `CLAUDE.md` e as skills `editar-criativo`, `adaptar-marca` e `revisar-criativo`. Use `PYTHONIOENCODING=utf-8` e `-threads 3`.

## Como trocar (do mais barato ao mais caro)
1. Texto na tela: caixa opaca (alpha ≥ 250).
2. Rótulo: `trocar_rotulo_faixa.py`, ou um take do frasco Lymphoria já produzido.
3. Fala: voz clonada (off) ou voz + lipsync (rosto).
4. Frasco legível em movimento: Kling O1 Edit + `encaixar_edit.py`, só se necessário.

**Fim:** todos encerram com a oferta Lymphoria, selo "Pago contra entrega" e setas, via `montar_ad.py`, em 720x1280.

## Teto e revisão
- **Teto por vídeo:** US$ 1,50 (V10 e V11 até US$ 3,00).
- **Revisão:** `revisar_ad.py` pelo PowerShell, com proibidos em `.txt` UTF-8: Vitaly, Vitali, vitaly-chile, Cyber, "45 días", "60 días", "2x1", kilos, kg, cancer.
  - Se houver lipsync: `--lipsync`, índice ≤ 0,6.
  - Folha nas emendas.
  - RESULTADO precisa sair OK.

## Saída
- **Todos os finais:** `ADLIB-VITALY-CL\LYMPHORIA-ES-CL\VNN - LYMPHORIA-<TEMA>.mp4`.
- **Suavizados** (V03, V10, V11, V19, V26): também em `ADLIB-VITALY-CL\LYMPHORIA-ES-CL\SUAVIZADOS\`:
  - `VNN - ORIGINAL.mp4` (cópia do original);
  - `VNN - SUAVIZADO.mp4`;
  - acrescente as linhas do vídeo em `SUAVIZADOS\00-TROCAS.md`. Um agente por vídeo escreve sua seção `## VNN`, sem apagar a dos outros.
- **Trabalho:** `ADLIB-VITALY-CL\_trabalho\prod\VNN\`, com `RELATORIO.md` (trocas, custo, voz, revisão).
- **Painel:** python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa VNN "Lymphoria VNN" --texto ... --k N --n M; img; custo; fim VNN.
