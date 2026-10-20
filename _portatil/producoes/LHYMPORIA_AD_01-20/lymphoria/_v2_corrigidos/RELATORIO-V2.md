# Relatório v2: lote Lymphoria (correção do encaixar_edit)

> Este arquivo foi criado pela Parte B porque ainda não existia. A Parte A (ADs 01, 02, 03, 04, 09, 10, 11, 14, 16) acrescenta a seção dela aqui.

## Parte B: ADs 12, 13, 19 e 22

**Data:** 05/10/2026. **Custo:** zero. Nada de Kling nem de TTS: só reprocessamento local, com os mesmos edits do Kling que já estavam baixados.

### O que foi corrigido

| AD | Takes refeitos | Arquivo v2 |
|---|---|---|
| 12 | t1, t2 (bordas) + 1 quadro do `cobre_tela` (ver abaixo) | `AD 12 - LYMPHORIA-BANO-RESERVA-ES-LATAM v2.mp4` |
| 13 | t1, t2, t4, t5 | `AD 13 - LYMPHORIA-HERMANO-ES-LATAM v2.mp4` |
| 19 | t1, t3, t4 (o t2 **não** foi refeito: é um flash do original e não é defeito) | `AD 19 - LYMPHORIA-CELULITIS-ES-LATAM v2.mp4` |
| 22 | t2 (borda) | `AD 22 - LYMPHORIA-22-ANOS-ES-LATAM v2.mp4` |

Os takes que não estavam na lista entraram com o mesmo arquivo do AD entregue (`_trabalho/adNN/flora/*_final.mp4`). São eles: AD 13 t3, AD 19 t2, AD 22 t1 e o `cobre_tela` do AD 12.

### Como foi montado

O caminho de montagem foi conferido em `processar_ad.py`, `rNN.json`, `log_rNN.txt`, `trechos.json` e `receita_final.json`. Os horários dos arquivos batem: cada AD foi montado uma única vez e não passou por `remendar_ad.py`.

1. **Encaixe dos takes:** `kit/ferramentas/encaixar_edit.py`, a versão corrigida, com os mesmos argumentos (`--dur = quadros/30`). Saída em `flora/tN_final_b.mp4`. Os logs (quadros, fps, saltos) são iguais aos do lote antigo. O vídeo decodificado tem md5 idêntico ao `tN_final.mp4` que a Parte A gerou.
   - A Parte A já tinha provado que o caminho é reproduzível: rodando a versão antiga, com o bug, sobre as mesmas entradas, o resultado bate com o take entregue (`encaixe_v2.json`, `fora_px40` de 0 a 3).
2. **Etapas de vídeo, na mesma ordem do lote antigo:**
   - `substituir_trechos`;
   - `desfocar_regioes` (AD 13 e AD 22);
   - `trocar_texto_tela` (AD 13: 3 textos; AD 22: 2 textos).
3. **Parte 1:** vídeo novo com o áudio da `parte1.mp4` entregue, copiado sem reencode. O md5 do áudio é conferido no próprio script.
4. **Remontagem:** `montar_ad.py` com a mesma `receita_final.json`, trocando só os caminhos. A `parte2.mp4` é a mesma do AD entregue.

**Scripts da Parte B:** `_v2_trabalho/parteb_v2_b.py`, `revisar_v2_b.py` e `folha_faixa_b.py`. São cópias adaptadas dos scripts da Parte A e não alteram nenhum arquivo dela. Os intermediários levam o sufixo `_v2b` ou `_b`. Logs em `log_montar_adNN_b.txt` e `log_rev_adNN_b.txt`.

### Dois detalhes do lote antigo que precisaram ser reproduzidos

- **Quadros cortados pelo `-shortest`.** No lote antigo, o `-shortest` das passadas cortou quadros da parte 1:
  - AD 19: 2 quadros do fim;
  - AD 22: 3 quadros do fim;
  - AD 12: 1 quadro, o penúltimo (índice 8845). Ficou um buraco no PTS, e o `montar_ad` preenche esse buraco duplicando um quadro.

  A cópia do kit em `_v2_trabalho/kit` não usa `-shortest`. Por isso, o `parteb_v2_b.py` reproduz a lista de PTS exata da `parte1.mp4` entregue (corte no fim, ou `select` sem o quadro 8845, com `-fps_mode passthrough`). Sem isso, a duração e o áudio não batiam.
  - **Atenção, Parte A:** nos ADs 01, 09, 11 e 16 a contagem bateu, mas vale conferir o mesmo ponto nos ADs que ainda faltam.
- **AD 12, `cobre_tela.mp4` (fora da lista, corrigido mesmo assim):** o 1º quadro desse extra (218.87 s) não está coberto e mostra o site com a marca **MAYAVERRA** por 1 quadro.
  - No entregue, o encode a 900 kbps borrou esse quadro.
  - Na v2, por causa do não determinismo do encoder (`-threads 4`), ele saía nítido.
  - Corrigi com `flora/cobre_tela_b.mp4`: o mesmo clipe, com o 1º quadro trocado pelo 2º (diferença média de 0.9 a 1.0 nos demais quadros, só reencode). É a única diferença intencional fora dos takes.

### Resultado da revisão (entregue × v2)

| AD | Áudio (md5 decodificado) | Duração / quadros | Parte 1 fora dos takes (px > 40, máx.) | Final fora dos takes |
|---|---|---|---|---|
| 12 | idêntico | 316.40 s / 9491 = igual | 146 px (só borda de texto). Exceção: o quadro 6566 (218.87 s), corrigido de propósito | PSNR médio 40.0. Único quadro > 15 000 px: o 6566 |
| 13 | idêntico | 694.50 s / 20834 = igual | 65 px (2 quadros > 50) | PSNR mín. 31.9, médio 38.9 |
| 19 | idêntico | 67.00 s / 2006 = igual | 41 px (o t2 mantido entra aqui: igual ao entregue) | PSNR mín. 37.2, médio 42.7 |
| 22 | idêntico | 248.80 s / 7463 = igual | 84 px (12 quadros > 50, ponto mínimo na borda da legenda em 58.4 s) | PSNR mín. 28.0, médio 38.3 (ruído do encode a 900 kbps em partículas, conferido) |

- **Por que a comparação de imagem usa a parte 1.** A imagem fora dos takes foi comparada antes da compressão final, porque o encode final a 900 kbps sempre gera ruído. As diferenças pequenas que sobram vêm de uma geração extra de crf 15 nas partes 1 que precisaram ser cortadas.
- **Folhas de zoom 3x:** `revisao/AD12_takes_zoom3x.jpg`, `AD13_…`, `AD19_…` e `AD22_…` (entregue × v2 nos takes). Elas mostram as manchas e bordas brancas sumindo:
  - AD 12: barra branca na borda do t2;
  - AD 13: listras brancas no logo da folha no t2 e letras do rótulo no t1;
  - AD 19: "fantasma" da luminária no t4;
  - AD 22: pontos brancos na borda do conta-gotas.
- **Arquivos de referência:**
  - `_frames.jpg` de cada v2: gerado pelo `finalizar`, com resultado OK em todos;
  - o CTA ficou no mesmo tempo do entregue;
  - JSONs detalhados em `revisao/adNN_revisao_v2.json`.

### O que NÃO foi corrigido (fica para decisão)

- **Faixa da legenda (62% a 90% da altura).** A correção do kit só limpa fora dessa faixa. Onde o rótulo do produto cai dentro dela, pedaços brancos do rótulo antigo continuam voltando, iguais ao entregue:
  - **AD 22, t2 (cerca de 85.9 a 86.6 s):** aparece "RRA" (de MAYAVERRA) logo abaixo de "LYMPHORIA" no rótulo, nos quadros em que a legenda some. O edit do Kling está limpo; isso vem da restauração da legenda. Veja `revisao/AD22_faixa_legenda.jpg`.
  - **AD 13, t1 (fim do take, cerca de 334 a 334.8 s):** a legenda queimada fica falhada ("os om res… ella"), igual ao entregue.
  - Corrigir esses dois pontos exige mudar a regra de restauração da legenda no `encaixar_edit` (por exemplo, restaurar só as palavras da legenda e não todo branco da faixa). Isso foge do "mesmos argumentos com o encaixar corrigido", por isso não foi feito.
- **AD 19 t2:** mantido como no entregue, conforme a instrução (flash do original).
- **Tamanho dos arquivos:** a v2 do AD 22 tem 30.3 MB (o entregue tinha 29.3 MB, com limite de 30 MB) e a do AD 19 tem 25.7 MB. Os dois saem a 900 kbps pelo mesmo `montar_ad`; a diferença é variação do encoder.


---

## Parte A: ADs 01, 02, 03, 04, 09, 10, 11, 14 e 16

**Data:** 05/10/2026. **Custo:** zero. Não usei Kling nem TTS: só reprocessamento local, com os edits do Kling que já estavam baixados.

Os arquivos entregues em `lymphoria\` e a pasta `_trabalho\` não foram tocados. Todo o trabalho foi feito em cópia, em `_v2_trabalho\adNN`.

### O que foi corrigido (os 9 ADs foram gerados)

| AD | Takes refeitos | Arquivo v2 |
|---|---|---|
| 01 | t3 | `AD 01 - LYMPHORIA-ESPOSA-ES-LATAM v2.mp4` |
| 09 | t1, t2 | `AD 09 - LYMPHORIA-SESENTA-ES-LATAM v2.mp4` |
| 11 | t1, t2, t3, t4, t5 | `AD 11 - LYMPHORIA-GIMNASIO-ES-LATAM v2.mp4` |
| 16 | t2, t3 | `AD 16 - LYMPHORIA-VESTIDO-ES-LATAM v2.mp4` |
| 03 | t1, t2 (com o 2º edit, `t*_edit2.mp4`, como no entregue) | `AD 03 - LYMPHORIA-ESQUELETO-30DIAS-ES-LATAM v2.mp4` |
| 14 | t1, t2, t3, t4, t5 (o remendo t6 ficou como no entregue) | `AD 14 - LYMPHORIA-VIAJE-ES-LATAM v2.mp4` |
| 02 | t1, t2, t3 | `AD 02 - LYMPHORIA-28-ANOS-ES-LATAM v2.mp4` |
| 04 | take1, take34, take67, r4, r5 | `AD 04 - LYMPHORIA-ESQUELETO-CERVEZA-ES-LATAM v2.mp4` (1080x1920, como o entregue) |
| 10 | t1 (2º edit), t3 (o t2 e o remendo t4p ficaram como no entregue) | `AD 10 - LYMPHORIA-MATRIMONIO-ES-LATAM v2.mp4` |

**Itens da lista que não existem no AD entregue (não há o que corrigir):**
- **AD 01, t2:** nunca entrou no AD.
  - O `trechos.json` usa só t1 e t3. O t1 nem é Kling: é um vai-e-volta do próprio original.
  - Na janela de 267.57 a 268.83 s, o entregue mostra o vídeo original: a avó abrindo a caixa, com o frasco pequeno em cerca de 268.6 s.
  - **Precisa de revisão manual** para ver se o rótulo antigo aparece legível nesse frasco.
- **AD 04, take2 e take5:** no lote antigo, foram trocados pelos refeitos r2 e r5 e não entram no AD.

### Como cada AD tinha sido montado (levantado antes de refazer)

**Fontes consultadas:**
- `processar_ad.py`, `rNN.json` e `log_r*.txt`;
- `trechos.json`, `trechos_remendo.json` e `receita_final.json`;
- horários dos arquivos;
- histórico de comandos da sessão que montou o lote.

**Caminho de cada AD:**
- **ADs 02, 09, 11, 14 e 16:** montados pelo `processar_ad.py`, nesta ordem:
  1. encaixe com `--dur quadros/30`;
  2. substituir;
  3. blur;
  4. textos;
  5. áudios;
  6. `montar_fim_universal`.

  O AD 14 passou depois pelo `remendar_ad.py` (t6 em 382.167 s).
- **ADs 01, 03 e 10:** mesmo fluxo, mas rodado à mão. Os comandos foram recuperados do histórico, com os mesmos parâmetros de textos e áudios. Valores de `--dur`:
  - AD 01: 2.37;
  - AD 03: 5.4 e 5.067;
  - AD 10: 1.37 e 2.5.

  O AD 10 passou depois pelo `remendar_ad.py` (t4p em 285.3 s).
- **AD 04:** é um AD do 1º dia.
  - Os takes foram encaixados em `parte1_up.mp4`, gerando `parte1_lymphoria.mp4`, sem etapas depois.
  - Foi montado pelo `montar_ad.py` **clássico**, porque o caminho rápido ainda não existia. A v2 foi montada com `--classico`.
  - A conta de bitrate do `finalizar` dá o mesmo valor (1657 kbps) nas duas versões.

**Prova de que o caminho é reproduzível:** para cada take refeito, também rodei a versão antiga do `encaixar_edit`, com o bug, sobre os mesmos arquivos. Ela está guardada em `kit/ferramentas/encaixar_edit_antigo_bug.py`.
- O resultado bate com o take que entrou no AD entregue: 0 a 6 pixels por quadro com diferença > 40 fora da faixa da legenda, ou seja, só ruído de encode.
- As medidas estão em `_v2_trabalho/adNN/encaixe_v2.json`; o resumo sai com `resumo_encaixe.py`.

### Como foi refeito

1. **Re-encaixe (`encaixar_v2.py`):** `encaixar_edit.py` corrigido do kit, com os mesmos argumentos. Nenhum take usava `--sem-legenda`. O take antigo ficou ao lado, como `*_final_v1.mp4`.
2. **Remontagem (`montar_v2.py`):**
   - As etapas de vídeo foram refeitas na mesma ordem: substituir, blur, textos e remendo.
   - As etapas de áudio só mexiam no áudio (`-c:v copy`). Por isso, o áudio da parte 1 foi **copiado sem reencode** da parte 1 entregue, e o script confere o md5.
   - A `parte2.mp4` é a mesma do entregue.
   - A remontagem usa a mesma `receita_final.json`, só com os caminhos trocados.
3. **Cópia do kit em `_v2_trabalho/kit`** (detalhes em `kit/LEIA.txt`): `-threads 4` em todo libx264 e **sem `-shortest`**.
   - **Por que tirei o `-shortest`:** com `-threads 4`, ele cortava 1 quadro por passada. Isso aconteceu na 1ª versão do AD 11, que foi refeita.
   - **Cortes do lote antigo:** lá, o `-shortest` cortou quadros do fim da parte 1 no AD 14 (12 762 → 12 751, no remendo) e no AD 10.
   - **Sem buraco no PTS:** nenhum AD da Parte A tem buraco no PTS (conferido com `pts_chk.py`).
   - **Como a v2 reproduz o corte:**
     1. corta o vídeo no mesmo número de quadros da parte 1 entregue, recodificando sem perda (qp 0);
     2. só depois junta o áudio.

     O `-frames:v` aplicado junto com o áudio cortava o áudio também. Isso aconteceu numa 1ª tentativa do AD 14, que foi refeita.

### Resultado da revisão (entregue × v2)

| AD | Takes refeitos | Áudio (md5 decodificado) | Duração / quadros | Parte 1 fora dos takes (px > 40, máx.) | Final fora dos takes (PSNR médio / mín.) | Folha zoom 3x |
|---|---|---|---|---|---|---|
| 01 | t3 | idêntico | igual (367.57 s, 11 026 q) | 89 | 37.5 / 20.6 dB | `revisao/AD01_takes_zoom3x.jpg` |
| 09 | t1, t2 | idêntico | igual (341.30 s, 10 237 q) | 290 (borda do texto trocado em 121.9 s; conferido, visualmente igual) | 38.1 / 28.2 dB | `AD09_…` |
| 11 | t1 a t5 | idêntico | igual (562.60 s, 16 877 q) | 29 | 38.0 / 26.5 dB | `AD11_…` |
| 16 | t2, t3 | idêntico | igual (520.70 s, 15 618 q) | 19 | 39.2 / 29.7 dB | `AD16_…` |
| 03 | t1, t2 | idêntico | igual (92.80 s, 2 781 q) | 19 | 42.9 / 37.9 dB | `AD03_…` |
| 14 | t1 a t5 | idêntico | igual (449.40 s, 13 479 q) | 41 | 37.9 / 30.1 dB | `AD14_…` |
| 02 | t1, t2, t3 | idêntico | igual (421.93 s, 12 656 q) | 159 (borda de texto, 1 quadro > 50) | 36.9 / 27.7 dB | `AD02_…` |
| 04 | take1, take34, take67, r4, r5 | idêntico | igual (127.98 s, 3 836 q) | 9 | 38.7 / 25.5 dB | `AD04_…` |
| 10 | t1, t3 | idêntico | igual (439.00 s, 13 165 q) | 57 | 38.7 / 27.9 dB | `AD10_…` |

- **Fora dos takes, a imagem é a mesma.**
  - A comparação justa é a da parte 1, antes da compressão final. Lá, o máximo foi de 9 a 290 pixels num quadro de 921 600, só em bordas.
  - No arquivo final, o encode a 900 kbps dá PSNR médio de 37 a 43 dB. É taxa média e não é determinístico quando muda o número de threads.
  - Os mínimos caem em quadros de corte de cena onde o **entregue** tinha mais blocos de compressão que a v2. Exemplo conferido: AD 01 em 241.3 s.
- **`_frames.jpg` do finalizar:** RESULTADO OK nos 9, e o CTA ficou no mesmo tempo do entregue.
- **O que as folhas mostram (entregue → v2):**
  - **AD 01, t3, e AD 09, t1:** some a folha do logo antigo que ficava por cima do logo novo.
  - **AD 11, t1:** somem as letras "Ma…" sobre "LYMPHORIA".
  - **AD 11, t4, e AD 14, t5:** somem as manchas brancas na mesa e na borda do frasco.
  - **AD 16, t2, e AD 03, t1:** somem as letras soltas sobre "LYMPHORIA" e "TRADICIONAL".
  - **ADs 02 e 10:** somem os riscos brancos nas bordas do frasco.

### O que NÃO foi corrigido / precisa de decisão

1. **Faixa da legenda (62% a 90% da altura):** é o mesmo limite que a Parte B viu.
   - Onde o rótulo cai dentro dessa faixa, o branco do rótulo antigo ainda volta, igual ao entregue.
   - Casos vistos nas folhas `revisao/ADNN_faixa_legenda.jpg`:
     - **AD 03, t1 e t2:** o frasco fica dentro da faixa quase o take todo. O rótulo aparece com pedaços de letra e manchas ("drenajo", "…ONAL").
     - **AD 09, t2:** marcas brancas sobre "linfático".
     - **AD 01, t3:** pontinhos brancos na borda esquerda do frasco.
     - **Demais ADs:** conferir as folhas `_faixa_legenda`.
   - **Teste já feito, sem gerar AD:** `kit/ferramentas/encaixar_edit_v3_teste.py` só restaura dentro da faixa o que estiver perto das letras da legenda (usa a função `letras_grandes` do próprio script).
     - Comparação em `_v2_trabalho/teste_v3/cmp_v2_v3.jpg`.
     - Limpa o AD 01, t3, e o AD 09, t2, e a legenda continua certa.
     - Reduz o defeito do AD 03, t1. O que sobra ali vem do próprio edit do Kling.
     - Se for aprovado, dá para gerar um v3 de todos os ADs com os mesmos scripts, só localmente e sem custo.
2. **Takes fora da lista que usam o mesmo `encaixar_edit`:** AD 10 t2 e t4p, AD 14 t6, AD 16 t1, AD 04 r2 e r7.
   - Rodei a versão corrigida neles. A diferença é pequena (até cerca de 300 px por quadro, na borda do frasco) e não muda a leitura.
   - Por isso, ficaram iguais ao entregue.
3. **AD 19, t2 (é da Parte B; fica só o registro):**
   - Na minha conferência, a versão corrigida difere muito do entregue: até 463 543 px num quadro.
   - No entregue aparece uma **mancha branca grande cobrindo o fundo**, além de marcas do rótulo antigo sobre "drenaje". Veja as linhas do AD 19 em `_v2_trabalho/_chk_naolistados.jpg`.
   - A Parte B manteve esse take por ser "flash do original". Vale olhar essa imagem antes de decidir.

### Arquivos da Parte A

- **Scripts:** `_v2_trabalho/config_v2.py`, `encaixar_v2.py`, `montar_v2.py`, `revisar_v2.py`, `folha_faixa.py`, `resumo_encaixe.py`, `tabela_v2.py` e `pts_chk.py`.
- **Logs:** `log_encaixe.txt`, `log_montar_adNN.txt` e `log_final_10_14.txt`.
- **JSONs:** `revisao/adNN_revisao_v2.json`.
- **Espaço em disco:** as pastas `_v2_trabalho/adNN` guardam intermediários grandes: `v2_b*.mp4` em todos e `v2_parte1_so_video.mp4` (sem perda) no AD 10 e no AD 14. Dá para apagá-los depois de aprovar as v2; eu não apaguei.
