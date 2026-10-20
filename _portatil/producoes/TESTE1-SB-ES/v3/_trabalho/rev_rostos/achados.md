# Revisão ROSTOS e COLAR: SB-ES_NOTICIA-AURELIO_v3_FICTICIO.mp4 (1º corte)

Versão revisada: arquivo de 14/10 15:17:25, 54.777.022 bytes. Conferi de novo no fim da revisão e o arquivo não mudou.
Método: extraí todos os 5085 quadros a 30 fps e montei folhas com zoom de boca/rosto em cada take com fala (mulher react, briga, reportera, Aurelio, padre) e no colar (pescoço do Aurelio, insert e take P06, b-rolls s19/s20). Os tempos de pausa saíram dos `palavras_whisper` dos manifests, convertidos para o tempo do vídeo final pela `timeline_v3.json`.
Folhas usadas como evidência: `rev_rostos/s/*.jpg`. Os quadros soltos estão em `rev_rostos/f/` (nº do arquivo = quadro + 1).

## GRAVE

1. **1:29.30–1:30.32 (P06, take do padre com o colar na mão): a medalha some e se funde com a mão.**
   - 2:29.43–2:29.57: a corrente desce entre os dedos e não tem medalha na ponta. Ela some por 5 quadros.
   - 2:29.37 e 2:29.60: aparece só um pedaço da medalha.
   - 2:30.00–2:30.10: a medalha aparece através dos dedos, translúcida e fundida com a mão.
   - É exatamente o defeito "COLAR" que o manifest marcou no take. O insert Kling só cobre até 2:29.30.
   - Correção: estender o `insert_P06_colar_kling.mp4` até 2:30.32 (hoje ele usa 0,3–1,72 s; o arquivo tem 5,04 s e a medalha fica estável no insert inteiro). Outra opção: manter o P06 só com o rosto (zoom 1.12 cortando acima de y≈700, sem mãos).
   - Folhas: `s/p06med.jpg`, `s/p06hands.jpg`.

## MÉDIO

2. **0:00.00–0:18.46 × 0:27.30 em diante: o colar do comerciante muda entre a abertura e a entrevista.**
   - Na briga e nos takes B04/B05/B06, Don Aurelio usa um pingente pequeno, dourado e triangular numa corrente fina. Dá para ver bem em 0:01.00, 0:06.67, 0:10.00, 0:13.33 e 0:17.33.
   - Na entrevista, ele usa a medalha redonda de prata de San Benito.
   - É o mesmo personagem com colar diferente, e o roteiro diz que "Don Aurelio lo lleva al cuello". Folha: `s/pend_ab.jpg`.
   - Correção: trocar o pingente na abertura por uma medalha de prata (troca de região/`trocar_rotulo` ou inpaint nos quadros, porque o pingente é pequeno). A alternativa barata é aceitar, já que na abertura ele aparece pequeno e de longe. **Decisão da pessoa.**

3. **Rosto do comerciante: abertura × entrevista (era a reclamação da v2).** Melhorou muito em relação à v2: cabelo grisalho, camisa cinza e tom de pele batem. Ainda assim, ele parece outra pessoa:
   - Abertura (0:00–0:18): rosto mais magro e marcado, pele mais escura, cabelo mais ralo.
   - Entrevista (0:27.30–0:54.30): rosto largo e redondo, bochechas cheias, pele mais clara, cabelo mais volumoso.
   - Entre a briga e B04/B05/B06 o rosto fica coerente.
   - Folhas: `s/rosto_cmp.jpg`, `s/comp_com.jpg`.
   - Correção, se a pessoa achar que incomoda: refazer só a imagem-base da entrevista (`aurelio_colar_v1.png`) a partir de um quadro do rosto da abertura, o que custa HeyGen de A01–A03. A outra saída é aceitar, porque a câmera e a distância diferentes justificam parte da mudança.

4. **0:27.63–0:27.87 (A01, pausa depois de "Sí,"): boca aberta com dentes à mostra no silêncio** (quadros #829–836). Correção: cobrir 0:27.64–0:27.88 com um b-roll curto (por exemplo `k13_vela_encendiendo` ou `s16_rosario_manos`, que já são usados no bloco) ou fechar a boca por colagem de um quadro neutro do próprio take.

5. **0:50.37–0:50.73 (A03, pausa depois de "cayó,"): boca escancarada com dentes por cerca de 0,35 s sem fala** (quadros #1511–1522). Correção: cobrir 0:50.40–0:50.60 com b-roll (por exemplo um quadro de `e01_teclado`, que combina com "transmisión en vivo") ou encurtar a pausa no corte.

6. **0:39.77–0:40.03 (início do A02): a mão entra de repente na frente da medalha e a medalha aparece por cima e através dos dedos.** Nos quadros #1194 e #1199, os dedos parecem translúcidos sobre a medalha. Além disso, o corte de A01 para A02 em 0:39.77 é um salto seco: a cabeça muda de posição e já entra sorrindo. Folha: `s/medz_3975.jpg`.
   - Correção: no plano A02, usar zoom 1.12 (só o rosto, sem a medalha) de 0:39.78 a ~0:40.10. Ou começar o A02 com um b-roll de 0,3 s, que também esconde o salto.

7. **1:29.97–1:30.27 (início do P03) e 0:55.10–0:55.27 (início do P01): o padre começa com um sorriso de dentes cerrados, estilo careta.** É o resíduo da entrada do HeyGen. Há fala ("Esta"/"Presten"), mas o formato de boca não bate com a palavra.
   - Correção: avançar o `vt` do P03 para ~0,35 s e o do P01 para ~0,2 s. Ou entrar com o corte de b-roll anterior estendido por 0,2–0,3 s, porque o e19 e o R02 terminam ali.

## LEVE

8. **0:00.37–0:00.70 e 0:02.43–0:02.73 (mulher react, pausas depois de "Gente," e de "existe."): dentes à mostra em expressão de choque.** Combina com o tom de reação e eu aceitaria. Folha: `s/mulher.jpg`.

9. **0:02.67–0:02.73 (junção Kling para Seedance na briga): a mão estendida do agressor vira um borrão esbranquiçado em 2–3 quadros** (#80–82). É rápido e o rosto dele não muda entre os dois takes. Para corrigir, dá para cortar 2 quadros na junção. Folha: `s/junc_28.jpg`.

10. **0:18.57 (1º quadro do R01): a reportera entra com um sorriso de dentes que vira rosto neutro no quadro seguinte (salto).** Correção: começar 1 quadro depois.

11. **0:26.80–0:27.30 (fim do R01): a reportera fica sorrindo com dentes depois de "país"** (fala termina em 0:27.06). Corte em 0:27.07.

12. **0:43.93–0:44.13 (A02, pausa depois de "clientes."): dentes e boca entreaberta**, e depois a boca fica em "o" antecipando "No" (já marcado no manifest como leve). Se for cobrir, use 0,2 s de b-roll de clientes.

13. **0:54.13–0:54.30 (fim do A03): boca aberta com dentes no silêncio depois de "poderosa".** Para corrigir, cortar para o R02 em 0:54.13.

14. **2:27.88–2:29.30 (insert P06): o colar do insert está próximo da referência, mas não igual.** A medalha é mais clara e "achatada", e a corrente é fina em vez da corrente veneziana grossa da foto. As mãos do insert não seguram o microfone, enquanto o padre do take segura o microfone na mão direita. É aceitável. Nos b-rolls s19 e s20 (2:30.33–2:35.77) a fidelidade à foto ficou boa: corrente veneziana, argola e anel de letras.

## Conferido sem problema

- **Moldura EN VIVO:** aparece em 100% dos quadros do padre (P01, P02, P03, P04, P05, insert P06, P06, P07 e P08), conferido quadro a quadro pela cor do selo. Nos b-rolls de narração ela não aparece, o que é esperado pelo plano.
- **Agressor:** o mesmo rosto e a mesma roupa nos takes Kling e Seedance. Não vi troca de rosto.
- **Aurelio, pausas cobertas ou fechadas:** 0:29.46–0:29.71 com a boca fechada, 0:35.59–0:35.84 coberto por s16 e 0:40.96–0:41.06 com a boca fechada.
- **Colar no pescoço do Aurelio:** estável, opaco e fiel à foto em 0:27.30–0:54.30. A única exceção é o item 6.
- **Padre, pausas apontadas como graves no manifest já cobertas por b-roll:** P03 em 1:32.89–1:33.14, P04 (as duas), P05 em 2:16.83–2:17.08 e P05 "sitio," (pausa removida no corte 2:21.72, só há troca de zoom). As entradas de P05, P07 e P08 (vt 0,1) começam já articulando a palavra.
- **Rosto do padre:** consistente em todos os takes. Não vi rosto mole ou deformado em nenhum personagem.
