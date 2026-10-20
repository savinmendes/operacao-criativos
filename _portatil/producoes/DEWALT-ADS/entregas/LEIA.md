# DeWalt DCD7781: vídeos para subir (COD Chile · Pre Black Friday)

Kit DCD7781D2-B2: taladro percutor/atornillador 20V MAX brushless + 2 baterías 2Ah + cargador + maleta.
Os vídeos estão em espanhol chileno, em 9:16 (720x1280, 30 fps), **sem preço**, com "pagas al recibir" e "envío a todo Chile". Revisados em 10/10/2026.

## O que é cada vídeo

### Ganchos × corpos (10 vídeos, voz "Luis" chilena, música trend a -32 LUFS sob a fala)
Nome = `DW7781_G<gancho>_C<corpo>.mp4`. Os 3 primeiros segundos são o gancho; o resto é o corpo.

| Gancho | Fala | Título na tela | Abre com |
|---|---|---|---|
| G1 | ¿Buscas un taladro bueno, bonito y barato? | LAS 3B: BUENO · BONITO · BARATO | taladro com LED aceso na loja |
| G2 | ¿Sigues peleando con un taladro débil? | ¿TU TALADRO NO DA MÁS? | broca entrando no muro |
| G3 | Maestro, este taladro aguanta pega pesada. | PARA PEGA PESADA | broca na madeira em câmera lenta |
| G4 | ¡Llegó el Pre Black Friday, maestro! | PRE BLACK FRIDAY · DEWALT 20V MAX | maleta abrindo |
| G5 | Dos baterías, cargador y maleta: todo incluido. | KIT COMPLETO: 2 BATERÍAS + CARGADOR + MALETA | maleta aberta com o kit |

| Corpo | O que mostra | Duração com gancho |
|---|---|---|
| C1 · "todo lo que trae" | unboxing do kit inteiro: maleta, taladro, 2 baterías, cargador, mandril, 3 modos, 15 posiciones, 2 velocidades/1.750 rpm, LED | ~48 s |
| C2 · "pega pesada" | demonstração: muro, madera, atornillar, motor sin carbones (17 % según DeWalt), 2 velocidades, baterías | ~42 s |

Versões extras: `_sem-musica` = mesmo vídeo só com a voz (reserva, caso a música dê problema de direitos).

### Traduções de vídeos da própria loja (4 vídeos, voz clonada do narrador original)
| Arquivo | O que é | Duração |
|---|---|---|
| DW7781_TR21 | "versatilidad": kit na loja, mãos, narradora | 55 s |
| DW7781_TR37 | apresentação técnica em estúdio (só mãos), com cartões MADERA / METAL / MURO Y CONCRETO | 76 s |
| DW7781_TR41 | unboxing curto com luva | 33 s |
| DW7781_TR38 | closes na mão, curto | 16 s |

Versões extras: `_fundo-original` = voz + o som de fundo do vídeo original (sem a música trend). A principal leva voz + música trend.

Todos terminam no cartão PRE BLACK FRIDAY · PAGAS AL RECIBIR · Envío a todo Chile.

## Sugestão de teste
1. **Fase 1: os 5 ganchos no mesmo corpo (C1)**, um conjunto de anúncios: `DW7781_G1_C1` … `DW7781_G5_C1`. Muda só o gancho, então a diferença de hook rate/CPA é do gancho.
2. **Fase 1b (opcional, outro conjunto):** as 4 traduções (`TR21`, `TR37`, `TR41`, `TR38`), formatos diferentes (loja, estúdio, unboxing, close).
3. **Fase 2:** o gancho vencedor com o C2 (`DW7781_G<vencedor>_C2`), para comparar os corpos.
- Evitar o `DW7781_G2_C2`: o gancho e o corpo usam o mesmo plano da broca entrando no muro (parece repetido).
- Os `_sem-musica` e `_fundo-original` ficam de reserva.
- Nome do anúncio no gerenciador = nome do arquivo sem `.mp4` (lista pronta em `nomes_para_gerenciador.csv`, separado por `;`).

## Antes de subir (decisões pendentes)
Ver a lista de perguntas no relatório da revisão. Principais pontos:
- O fornecedor ainda precisa confirmar que o kit é o **D2-B2** (2 baterías + maleta dura). Todas as falas citam isso.
- Ouvir a pronúncia de "DeWalt" e o "Pre" do TR41 (28,3 s).
- A análise de copy está em `Produtividade com ia/02-relatorios/2026-10_cod_relatorio_copy-pre-teste-dewalt-dcd7781.md`.

## Revisão (10/10/2026)
- **Todos os 28 arquivos:** abrem sem erro e não têm termo proibido (preço, $, CLP, 179, "más vendido", torques/números fora da ficha, "Tork", português). Áudio e vídeo têm a mesma duração (diferença ≤ 0,067 s) e não há salto no áudio.
- **Sincronia da legenda:** nos 18 vídeos com legenda própria, 100 % dos blocos ficam a ≤ 100 ms da fala (máx. 51–97 ms) e todos aparecem no quadro esperado.
- **Corrigido nesta revisão (todos remontados):**
  1. O 1º bloco de legenda do corpo ("MIRA TODO LO" / "PONES EL ANILLO") tinha duração zero e não aparecia nos 10 ganchos × corpos.
  2. Algumas legendas entravam até 190 ms antes da fala (palavras depois de pausa, como "y", "Si", "Aprovecha").
- **Alertas que não são defeito:**
  - "quadro solto?" em ~8 s (C1) e 0,8–1,6 s (G4): conferido quadro a quadro, é corte normal e maleta abrindo.
  - "silêncio no fim" nos `_sem-musica`: é o cartão final sem música.
- Relatórios e folhas de contato: `_revisao_final/` (lista de termos em `_revisao_final/proibidos_final.txt`). Sincronia: `edicao/_legenda_sinc/_resumo_sinc.json`.
