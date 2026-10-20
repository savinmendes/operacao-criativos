# Briefing comum — produção noturna Drenagem LATAM (04→05/10/2026)

A pessoa está dormindo e aprovou o orçamento (~US$ 35 no total). **Não pare para perguntar nada.** Quando houver dúvida, decida pelo mais seguro e anote a decisão no relatório.

**Nunca leia nem imprima os arquivos `.env`** (nem `kit-edicao-criativos/.env`, nem `skills/vmake-skill/scripts/.env`). Os scripts do kit carregam as chaves sozinhos.

## Onde estão as coisas
- **Vídeos originais (360p):** `C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\originais\NN.mp4`
- **Estudo e análise:**
  - `DRENAGEM-LATAM\ESTUDO-DRENAGEM-LATAM.md`
  - transcrições em `DRENAGEM-LATAM\_analise\fala\NN.json` (`[ini, fim, texto]`)
  - relatórios dos agentes de análise em `_analise\agentes\G1..G6.md`
  - folhas de contato em `_analise\folhas2\`
- **Trabalho:** `DRENAGEM-LATAM\producao\_trabalho\adNN\`
  - O upscale 2x para 720x1280 roda numa fila de GPU. Ele grava `adNN\full_up720.mp4`; o progresso fica em `producao\_trabalho\log_upscale.txt`.
  - **Não rode upscale você mesmo.** Para esperar, use um loop em background: `until [ -f .../full_up720.mp4 ]; do sleep 30; done`.
  - Enquanto espera, adiante o trabalho em cima do `originais\NN.mp4`: escolher o ponto de corte, mapear as cenas do frasco e gerar a voz.
- **Saída final:** `DRENAGEM-LATAM\producao\AD NN - LYMPHORIA-<TEMA>-ES-LATAM.mp4` e, para a versão curta, `AD NN CURTO - LYMPHORIA-<TEMA>-ES-LATAM.mp4`.

## Método (o mesmo do lote LHYMPORIA, já validado)
**Leia antes:**
- a memória `C:\Users\PICHAU\.claude\projects\c--Users-PICHAU-Downloads-Produtividade-com-ia\memory\project_lymphoria-adaptacao-ads.md`;
- `C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\CLAUDE.md`;
- os exemplos prontos em `C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho\`: `processar_ad.py`, as receitas `r*.json`, as pastas `ad04`, `ad07`, `ad13` (com `voz.txt`, `narr_fim.*` e `flora/`), `transcrever_lote.py` e `cortar_takes.py`.

Já existem cópias prontas para esta produção em `producao\_trabalho\`:
- `processar_ad.py`;
- `cortar_takes.py`;
- `montar_fim_universal.py`, já apontando para as fotos do produto da Lymphoria;
- `fim_A.txt`, `fim_B.txt` e `fim_C.txt`.

O `processar_ad.py` grava a saída em `TRAB.parent`, que é `producao\`.

**Passos:**
1. **Ponto de corte.** Use a transcrição por palavra (faster-whisper small, `cpu_threads=4`, porque outros agentes estão rodando ao mesmo tempo). Corte antes do trecho em que o narrador apresenta a marca ou a oferta ("La marca que te da…", "Maya Verra", preço, link).
   - O fim é universal e serve para CL, GT e EC. Escolha `fim_A` (quando a narração já citou as 4 ervas), `fim_B` ou `fim_C`.
   - Mantenha as libras como estão.
2. **Cenas com o frasco ou o nome Maya Verra.** Ache-as com uma folha de contato do `full_up720` (`kit-edicao-criativos\ferramentas\folhas_contato.py`) e corte com `cortar_takes.py adNN ini:quadros …`.
   - O take precisa ter pelo menos 3 s: use `-t` + `tpad`.
   - Mande cada take ao **Kling O1 Edit no Flora**:
     - Use o MCP do Flora no projeto `prj_ns7cvmdqvtn37b53wfnywhr9q58fjte1`. A referência neutra do frasco Lymphoria é o **nó n59**.
     - Faça o upload com `kit-edicao-criativos\ferramentas\flora_upload.py --lote`.
     - O prompt começa com: "@Image1 is ONLY a reference for the bottle label design; do not use its background… local edit only, every pixel outside the bottle identical".
   - Custo: US$ 0,706 por take. **O teto por AD é o número de cenas do orçamento + 2.**
   - Se o Kling falhar ou estragar o rosto, cubra com a cena vizinha, desfoque a região (`desfocar_regioes.py`) ou mantenha o original quando a marca não for legível.
3. **Texto na tela** com Maya Verra, preço, garantia de 60 dias, "hecho en EE.UU." etc.: use `trocar_texto_tela.py` ou `desfocar_regioes.py`.
4. **Voz.**
   - Clone o narrador original a partir de um trecho limpo (`clonar_voz.py`). Antes, veja se já existe um clone dessa mesma voz: a do lote antigo é `FNIhgYgEcJsdWbHRFiz6`; confira os `voz.txt` das pastas do lote LHYMPORIA. Reutilize quando for a mesma voz.
   - **Não apague vozes de ninguém.** Se faltar vaga para clone novo, reutilize o clone com o timbre mais parecido e anote no relatório.
   - Gere `narr_fim.mp3` com o alinhamento (`tts_elevenlabs.py`, igual ao `ad07`) e as falas trocadas no meio (`trocar_trecho_audio.py`).
5. **Receita e montagem.** Escreva a receita `rNN.json` e rode `python processar_ad.py rNN.json` (com `PYTHONIOENCODING=utf-8`).
6. **Versão CURTA (60–90 s):**
   - Gancho (os primeiros ~8–15 s) + 2 ou 3 trechos fortes do corpo (o problema, o mecanismo "no es grasa, es retención/lodo" e a prova) + o mesmo fim COD.
   - Use as partes já tratadas (`parte1.mp4` ou `b*.mp4`), para nada da Maya Verra voltar.
   - Monte com `montar_fim_universal.py`, passando como `parte1` o trecho curto concatenado.
   - A fala tem que fazer sentido: corte em fim de frase, olhando a transcrição por palavra.
7. **Revisão obrigatória antes de entregar.** Faça em cada vídeo final:
   - Whisper (es) no final inteiro, procurando: "Maya Verra", "mayaverra", "sesenta días", "60 días", "hecho en Estados Unidos", "Ozempic", "TikTok", "COFEPRIS", "cáncer", preço, "link".
   - Folha de contato do vídeo final (1 quadro a cada 2 s), procurando o rótulo Maya Verra legível, cena de sexo explícita, antes/depois com kg, quadro solto nos cortes e silêncio no fim.
   - Corrija o que achar e revise de novo.

## Regras de conteúdo (Meta e oferta)
- **Oferta:** Lymphoria, envío gratis, pago contra entrega / pagas al recibir, 90 días de garantía o te devolvemos tu dinero. **Sem preço.**
- **Tirar:**
  - Ozempic e doenças nomeadas como cura;
  - "hecho en EE.UU." e "probado por terceros";
  - garantias de 60 ou 45 dias;
  - menção a TikTok;
  - registro sanitário;
  - cenas sexuais explícitas (cortar a cena ou cobrir com a vizinha);
  - promessa de kg exatos.
- Traição, ciúme e drama podem ficar: são o ângulo do criativo.
- **Não invente** dados, depoimentos novos com números nem estudos.

## CPU / GPU
- A GPU está ocupada pela fila de upscale.
- Whisper e OCR disputam a CPU: use `cpu_threads=4` e não rode OCR em massa (prefira folhas de contato).
- No Bash, use sempre `PYTHONIOENCODING=utf-8`.

## Relatório final (a sua resposta)
Por AD, informe:
- o arquivo final e o curto (caminhos);
- a duração;
- os takes no Kling (quantos e US$);
- os caracteres de TTS;
- o que foi tirado ou trocado;
- o resultado da revisão;
- o que ficou pendente ou para revisão manual.

Escreva também um resumo em `producao\_trabalho\adNN\RELATORIO.md`.
