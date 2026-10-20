# DeWalt (taladro 20V MAX) COD Chile, Pre Black Friday

> Produção de ADs do kit DeWalt para o Chile a partir de 50 vídeos de referência das lojas da pessoa, com plano Andromeda e pacote de teste. Abra ao subir, ler resultado ou produzir mais DeWalt.

## Contexto de uso
- **Frente:** COD Chile. **Início:** 09/10/2026. **Revisão final dos vídeos:** 10/10/2026.
- **Produto:**
  - página da loja (rascunho, 09/10/2026): **DCD7771D2-B2** (taladro atornillador brushless 1/2" + 2 baterias DCB203 2.0 Ah + carregador DCB107 + maleta), CLP 179.990, produto Shopify em DRAFT na chileverificada (`Downloads\DEWALT-DCD777-CL\RELATORIO.md` e `ESTUDO.md`); o DCD777 saiu do dewalt.cl;
  - os vídeos produzidos são do **DCD7781** (mesmo corpo e kit, com percussão), nomes `DW7781_*`, porque os ADs 21, 37, 38 e 41 das referências mostram esse modelo. **Qual modelo será vendido precisa de revisão manual** (o fornecedor ainda precisava confirmar o kit D2-B2).
- **Decisões da pessoa:** tema **pre Black Friday**; **não falar preço**; os creators dos vídeos são das **lojas da própria pessoa** (vende DeWalt no mundo todo) → rosto, clone de voz e lipsync liberados; o vendedor chileno dos ADs 32 e 48 (Ferrevolt Chile, es-CL) é dela e pode ser o rosto local; objetivo = **máximo de vídeos com o material existente, barato**; orçamento de mídia "vamos conversando"; música trend do Chile ok; 9:16. O conceito C4 (original × réplica) fica fora até haver documento de procedência.
- **Pastas:** `Downloads\DEWALT-ADS\` — `_ref` (50 ADs + txt), `_transcricoes`, `_estudo`, `ESTUDO_ADS.md`, `entregas\` (+ `LEIA.md`), `enxuto\` (pacote Andromeda), `FINAL-DW7781\` (tudo para subir + `TEXTOS_DOS_ANUNCIOS.txt`, `estaticos`, `variantes-audio`), `TESTE-DW7781\` (seleção do 1º teste, prefixo CJ1–CJ5), `SUBIR_DW7781.md`.
- **Entregas:**
  - 10 ganchos × corpos `DW7781_G1–G5_C1/C2` (voz "Luis" chilena, música trend a −32 LUFS) + versões `_sem-musica`;
  - 4 traduções de vídeos da loja com voz clonada: `TR21`, `TR37`, `TR38`, `TR41` + `_fundo-original`;
  - pacote enxuto: `C1_obraIA`, `C1_ferrevolt`, `C2_casaIA`, `C2_muroReal`, `C7_ferrevolt`, `C7_anelReal` + estáticos C5 e C6 (9:16 e 4:5).
  - Todos terminam no cartão PRE BLACK FRIDAY · PAGAS AL RECIBIR · Envío a todo Chile.
- **Teste recomendado (`SUBIR_DW7781.md`):** 11 anúncios, 5 conjuntos ABO por conceito (C1, C2, C7, C6, C5), US$ 100/dia, campanha de vendas Chile Advantage+.
- **Planos e relatórios:** `Produtividade com ia\02-relatorios\2026-10_cod_plano_andromeda-dewalt-dcd7781.md` e `2026-10_cod_relatorio_copy-pre-teste-dewalt-dcd7781.md`.
- **Custo:** teto aprovado ~US$ 15 no Flora para o pacote enxuto; custo real precisa de revisão manual.
- **Pendências:** confirmar kit D2-B2 com o fornecedor; ouvir a pronúncia de "DeWalt" e o "Pre" do TR41 (28,3 s); decisões listadas no relatório de revisão.

## Lógica de uso
1. **Estudo das referências:** ficha por AD (formato, gancho, produto, idioma, resolução, uso T/B/F/D, nota 0–4). Aqui: nenhum vídeo servia como está; o valor estava nos roteiros e num banco de takes pequeno.
2. **Qualidade da fonte:** 47–48 dos 50 em 576x1024 → upscale para 720p antes de usar.
3. **Workflow DCD7781:** 4 traduções (voz clonada do narrador original) + 10 G×C (5 ganchos × 2 corpos sobre o banco de takes, voz TTS chilena).
4. **Pacote enxuto Andromeda:** conceitos C1, C2, C6, C7 + estático C5, com execuções de famílias diferentes (IA talking head, creator real, b-roll com título grande).
5. **Abertura da produção (checklist):** fechar oferta, preço e orçamento de mídia numa pergunta só; legenda pelo roteiro; música a −32 LUFS; transcrever os takes.
6. **Revisão:** proibidos (`edicao\proibidos.txt`: preço, $, CLP, 179, "más vendido", torque fora da ficha, português); sincronia de legenda ≤ 100 ms; áudio × vídeo; sem salto de pts.
7. **Montagem do teste:** auditoria de aberturas (`_andromeda\aberturas.json`, similaridade); nunca subir juntos `G#_C1` e `G#_C2` (abrem iguais, 0,99), nem `G2_*` com `C2_muroReal` (mesmo take); estático em 9:16 + 4:5 no mesmo anúncio; nome no gerenciador = nome do arquivo (`nomes_para_gerenciador.csv`).
- **Se a pessoa pedir mais:** fase 2 = gancho vencedor com o outro corpo; 2ª rodada com as reservas (`C1_ferrevolt`, TR21/TR37/TR38); com os creators Ferrevolt dá para fazer lipsync local em es-CL.

## Relacionados
- [../07-variacoes-gancho-corpo.md](../07-variacoes-gancho-corpo.md)
- [../05-traducao-de-criativos.md](../05-traducao-de-criativos.md)
- [../09-lipsync-e-avatar-heygen.md](../09-lipsync-e-avatar-heygen.md)
- [../04-fluxo-producao-criativos.md](../04-fluxo-producao-criativos.md)
- [yara-bf-chile.md](yara-bf-chile.md) (mesma campanha pre-BF na chileverificada)
