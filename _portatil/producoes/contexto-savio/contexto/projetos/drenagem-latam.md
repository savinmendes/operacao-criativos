# Drenagem LATAM (Lymphoria): 55 criativos

> Segundo lote Lymphoria (COD LATAM): 20 ADs adaptados, 5 UGC com avatar e 30 variações de gancho. Abra ao continuar esse lote, ao criar variações sobre os corpos que venceram ou ao trocar rótulo em vídeo Pixar.

## Contexto de uso
- **Frente:** COD. **Mercados:** Chile, Guatemala e Equador, com oferta universal (envío gratis, pagas al recibir, 90 días de garantía), sem preço; libras mantidas.
- **Pasta:** `Downloads\DRENAGEM-LATAM\` (atalho `entregas-drenagem/`). Estudo dos 38 vídeos de referência em `ESTUDO-DRENAGEM-LATAM.md` (04/10/2026, 6 agentes); produção em `producao\` com `00-RELATORIO-PRODUCAO.md`; relatório por AD em `producao\_trabalho\adNN\RELATORIO.md`; textos em `producao\00 - TEXTOS-ANUNCIOS-LYMPHORIA-LATAM.txt`; cópia para o Drive em `PARA-O-DRIVE\`.
- **Entregue em 05/10/2026 (noite de 04→05/10), tudo em 720x1280 e revisado:**
  - ADs 01, 03, 04, 05, 18, 20, 21, 24, 25 e 30, cada um em versão longa e CURTA (~1:20–1:30);
  - UGC 01–05 (avatar HeyGen, ~50 s): CARRITO, PIRATAS, DISCULPA, HINCHAMOS, PAGAS-AL-RECIBIR;
  - VARIACOES VAR 01–30: 10 ganchos × corpos AD 20 (masculino), AD 05 e AD 30.
- **Decisão da pessoa:** os ADs 18 (Herbalia), 20 e 21 ("Lymphoria EUA") foram tratados como dela e produzidos.
- **Custo real:** ≈ US$ 24,75 (orçado US$ 35): Kling US$ 22,59, ElevenLabs US$ 2,16, + 76 créditos HeyGen nos UGC.
- **Validados no TikTok pela pessoa (08/10/2026),** cópias em `Downloads\APROVADOS E VALIDADOS TIKTOK\`: AD 30 CURTO EXESPOSO-FILA, VAR 06 (G6-DISCULPA × AD20), VAR 21 (G1-ESPOSO-AMIGA × AD30), VAR 28 (G8-POR-QUE-NOS-HINCHAMOS × AD30), VAR 29 (G9-PAGAS-AL-RECIBIR × AD30), além do AD 23 SUPERMERCADO do lote antigo.
  - **Sinal:** o corpo do AD 30 (exesposo na fila) e os ganchos de confissão, mecanismo e COD performam.
- **Pendências / revisão manual:**
  - textos do anúncio (título e texto principal) não tinham sido gerados no relatório;
  - risco Meta: corpo e antes/depois no AD 25 (3:24), AD 24 (1:24, 3:20), AD 21 (moletom → vestido), AD 30 (semanas 1/3/6 e decote); gancho "fingí" no AD 01; fala "no necesitas más hormonas" ficou no AD 25;
  - AD 21: rótulo em inglês "lymphatic drainage";
  - restos de legenda queimada de 0,3–0,8 s em emendas dos curtos e nos longos encurtados (03 e 24);
  - ouvir a emenda das VAR 15, 17 e 19;
  - UGC: cenas de produto 3D contrastam com o avatar; no UGC 05 (33 s) o selo cobre parte do rótulo;
  - integração ElevenLabs no HeyGen com o "key ID" no lugar da chave (VOICE_CONFIG_ERROR), a corrigir nas configurações do HeyGen;
  - arquivos longos e variações têm 35–54 MB (acima dos 30 MB do kit, mas o Meta aceita).

## Lógica de uso
1. **Estudo antes:** classificar os vídeos por marca/dono (própria, já Lymphoria, Herbalia, Vitaly, terceiros, descartar) e listar os melhores ganchos (ver tabela do estudo).
2. **ADs longos:** o mesmo método do lote LHYMPORIA (corte antes da marca + fim universal com voz clonada + Kling nos takes com frasco). Receitas `producao\_trabalho\rNN.json` e `processar_ad.py`; fins em `fim_A/B/C.txt`.
3. **Pixar/IA:** **não usar Kling** (troca o rosto). Usar `trocar_rotulo_faixa.py` do kit (nasceu como `ad25\band_fix.py`, com variantes `band_fix2/3` em ad03/ad24): acha a faixa do rótulo pela cor, apaga o texto e reescreve a marca no mesmo ângulo, sem custo. Usado nos ADs 01, 03, 04, 24, 25 e 30.
4. **Versão CURTA** (~1:20–1:30) de cada longo: `curto.py`/`curto2.py` em `_trabalho`.
5. **UGC:** avatar HeyGen falando roteiro novo (créditos do plano) + cenas de produto.
6. **Variações:** 10 ganchos novos colados sobre 3 corpos (hoje: `gerar_variacao.py` do kit). Gancho adaptado ao gênero do corpo (masculino no AD 20).
7. **Revisão:** whisper es + folha de contato + zoom no rótulo.
- **Armadilha que custou retrabalho:** o `encaixar_edit.py` copiava todo pixel branco do original por cima do take do Kling e o "MAYA VERRA" voltava (só visível com zoom). Corrigido em 05/10/2026; ADs 05, 18, 25 e VAR 11–20 refeitos de graça; o lote antigo ganhou v2.
- **Se a pessoa pedir mais:** priorizar o corpo do AD 30 e ganchos de confissão/mecanismo/COD (validados); seguir a lista de ganchos do estudo ainda não usados (ex.: 11 "Lo tuve en el carrito", 38 "¿Por qué te dejamos pagar al recibir?"); gerar os textos do anúncio que faltam.

## Relacionados
- [../06-troca-de-marca.md](../06-troca-de-marca.md)
- [../07-variacoes-gancho-corpo.md](../07-variacoes-gancho-corpo.md)
- [../09-lipsync-e-avatar-heygen.md](../09-lipsync-e-avatar-heygen.md)
- [../04-fluxo-producao-criativos.md](../04-fluxo-producao-criativos.md)
- [lymphoria-adaptacao-ads.md](lymphoria-adaptacao-ads.md), [vitaly-lymphoria-cl.md](vitaly-lymphoria-cl.md)
