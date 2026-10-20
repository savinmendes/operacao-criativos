# Estratégia criativa e copy

> O que já venceu, pipeline de IA validado, custos medidos, banco de copy, método Andromeda (persona × ângulo × consciência × formato) e como usar as skills `andromeda`, `estrategista-criativo` e `analista-de-copy`. Abra antes de planejar, auditar ou analisar um lote.

## Contexto de uso

### Onde vive a memória estratégica
- `Produtividade com ia/Contexto/estrategias-criativos.md`: formatos vencedores, pipeline de IA, custos medidos, macetes de retenção, banco de takes, decisões de compliance/oferta, retrospectiva Yara BF. Lido pela skill `estrategista-criativo`.
- `Produtividade com ia/Contexto/banco-de-copy.md`: padrões validados, reprovados, hipóteses e frases vencedoras por frente e mercado. Alimentado pela `analista-de-copy`.
- `Produtividade com ia/reports/Meta Andromeda criativos por ângulo.md` (estudo de 10/2026, com fonte de cada regra) e `research_notes/Meta Andromeda criativos por ângulo/` (notas e transcrições). Resumo operacional em `.claude/skills/andromeda/referencia.md`.
- Skills: `andromeda`, `estrategista-criativo`, `analista-de-copy`, `consultor-de-cases` (base de transcrições de cases).

### Formato que venceu: COD perfumes árabes, Chile (set/2026)
- Fonte: posts 122121238455420219 e 122121238329420219 (pack masculino 3x1, página Comercial Andes). Estudo em `Downloads/YARA-CL/_ref/`.
- 53–57 s, 9:16, 720p.
- Gancho (3–8 s): consultora de perfumaria em IA falando para a câmera com os frascos reais (vencedor B) ou moça dançando estilo TikTok (vencedor A).
- Corpo: narração ES sobre unboxing real (só mãos), troca de plano a cada 1,5–4 s; ~3 frases por perfume (nome + 3 adjetivos / sensação / ocasião).
- CTA: "Haz tu pedido ahora y paga solamente cuando lo recibas".
- Tela: legenda palavra a palavra branca com palavra-chave amarela no meio; faixa fixa topo-esquerda "PAGO CONTRA ENTREGA / ENVÍO EN 24 HORAS" azul-marinho com caminhão; adesivo no rodapé com os frascos.
- Texto do anúncio: "🔥 Los 3 perfumes árabes del momento en un solo pack", lista dos 3 nomes, 3 benefícios com emoji, "📦 Envío GRATIS en todo Chile / 💳 Pago contra entrega".

### Infoproduto: San Benito ES (11/10/2026)
- Título dos vencedores: "🔴 EN VIVO: La oración a San Benito que casi nadie conoce 🙏".
- Ângulo vencedor: bloqueio / "mala suerte" com causa espiritual e a oração "poco conocida" como saída. Variações vencedoras: solidão (JESU V07), o homem que carrega tudo em silêncio (AD 81).
- Vídeos longos (~2 min) dão volume; curtos (31–33 s) dão CTR de link ~10%. Detalhe em [13-analise-meta-ads-e-vencedores.md](13-analise-meta-ads-e-vencedores.md).

### Pipeline de IA validado (Flora), 09–10/10/2026
- Projeto de referência: "Videos de Ganchos VEO3 Perfumes" (`prj_ns76ea9xz3vj9xr5nkaxagt69h826xk1`).
- Cadeia: cena base → GPT Image 2 troca os produtos pela referência → (opcional) troca de persona → Seedance 2.0 i2v com fala de 8–11 s. Montagem e legenda fora do Flora.
- Prompts-padrão (verbatim em `estrategias-criativos.md`): troca de produto ("altere os perfumes da mesa… 3 PERFUMES", com descrição exata de cada frasco e "não invente frascos"); troca de persona; vídeo Seedance ("a mulher fala olhando para camera… SEM CORTES DE CAMERA…" + "NO FALE EM INGLÊS NEM PORTUGUÊS", "SEM MÚSICA, SEM LEGENDAS").
- Fala: máx. ~20 palavras a cada 8 s.
- **Voz única validada (09/10/2026):** clone ElevenLabs da voz do gancho aprovado + speech-to-speech em cada take (`YARA-CL/producao/voz/sts.py`, `eleven_multilingual_sts_v2`); sincronia 0–5 ms, dispensa lipsync. STS mantém a pronúncia original (palavra errada continua errada). Uma voz por avatar quando há várias pessoas.
- Montador com macetes: `YARA-CL/producao/edicao/montar.py` (punch-in, whoosh, título, banner, sticker, selo, legenda palavra a palavra, CTA).

### Custos medidos (cobrado, não cotação)
| Data | Item | Cotação | Cobrado |
|---|---|---|---|
| 09/10/2026 | GPT Image 2, 2k high | US$ 0,25 | US$ 0,53 (1k ≈ US$ 0,27) |
| 09/10/2026 | Seedance 2.0 i2v, 11 s 720p | US$ 1,06 | US$ 2,33 (~US$ 0,21/s) |
| 09/10/2026 | AD-C completo, 48 s | — | ~US$ 10 no Flora (com refação) |
| 10/10/2026 | Onda 2 Yara BF, 7 criativos | — | US$ 20,32 no Flora |

### Macetes de retenção (reel de referência, 09/10/2026)
Gancho visual antes da fala (título grande, elementos e som no quadro 1); movimento na primeira cena; ângulo diferente a cada frase e troca de local por bloco; legenda palavra a palavra no centro, às vezes palavra gigante; inserções (prints/vídeos) sobre a fala; final com ação clara.

### Banco de copy (estado em 13/10/2026)
- **COD Chile perfumes árabes:**
  - Reprovados: palavras parecidas com PT saem em PT na IA de vídeo ("stock" → "estoque"; use "liquidación total"); nomes mal pronunciados pela IA de voz ("Moi" → "muy", "Orquídea" → "Orquía", "frutilla" → "frutita", "grosella" → "grosilla"); "ñ" ("muñecas" → "mullegas").
  - Hipóteses em teste (YARA-BF, 7 criativos, mesma música): H1 oferta + tema; H2 oferta direta ("Pagas dos y te llevas los tres"); H3 sensorial + pergunta; H4 unboxing real + voz; H5 lista visual dos 3 nomes. Pré-teste: H4 deve vencer em CPA, H2 em segundo, H3 bom hook rate e CTR pior; AD-C (consultora + unboxing) > AD-A (só consultora). Não validado.
  - Próximo lote (hipótese): ângulo de presente ("¿Buscando regalo?…") e CTA "Pídelo hoy y pagas recién cuando te llegue a la casa".
  - Frases vencedoras: ainda vazio.
- **COD Chile DeWalt DCD7781 (10/10/2026):** G5 ("Dos baterías, cargador y maleta: todo incluido") deve vencer em CPA; G2 ("¿Sigues peleando con un taladro débil?") em hook rate; corpo C2 (demonstração) > C1 (inventário). Whisper ouviu "DeWalt" como "de Waltz" e "Pre Black Friday" como "Free Black Friday": marca e "Pre" escritos na tela. Não validado.
- Decisão da pessoa (Kit Yara BF, 09/10/2026): "pagas dos y el tercero gratis", "muy por debajo del precio de mercado", tema liquidação de BF, **sem falar preço**.

### Andromeda: o que é oficial × mito (estudo 10/2026)
- Oficial: Andromeda é o motor de **retrieval**; diversificar mensagem, visual e formato é a principal alavanca; o criativo faz a segmentação; anúncios que "parecem ou soam iguais" contam como variações do mesmo criativo.
- Mito de agência: "Entity ID", "1 ticket no leilão", limiar 60%/40%. Heurística de praticante: "8–15 conceitos por campanha".
- Números de praticante são ponto de partida para calibrar com dado da conta, não benchmark. Quando o dado da conta contradiz, vale o dado.

## Lógica de uso

### Divisão de trabalho entre as skills
| Pergunta | Skill |
|---|---|
| Quais conceitos o produto precisa? O lote é diverso? Como ler por eixo? Estrutura de campanha? | `andromeda` |
| O que produzir e como (roteiro por take, formato, orçamento, teste) a partir de vencedores/referências | `estrategista-criativo` |
| A copy está boa antes de subir? O que funcionou depois de rodar? | `analista-de-copy` |
| Alguém do mercado já fez isso? Quem discorda? | `consultor-de-cases` |
| Execução | `gerar-midia-ia`, `editar-criativo`, `revisar-criativo`, `traduzir-criativo`, `adaptar-marca` |

### Andromeda, modo 1: planejar a matriz
1. Leia `referencia.md`, `estrategias-criativos.md` e `banco-de-copy.md`. Identifique modelo de venda, país, idioma e oferta.
2. Pesquisa antes do formato: linguagem real do cliente (avaliações, comentários, atendimento). Sem isso, personas = hipótese.
3. 2–4 personas por **identidade + micro-momento** (não demografia).
4. Matriz, uma linha por conceito: `ID | modelo/país | persona | ângulo | desejo | consciência | estado mental | formato 1/2/3 | elenco/voz | abertura visual | oferta/CTA | risco de compliance | hipótese em 1 frase`.
   - Ângulos: dor/alívio, aspiração/status, prova/autoridade, mecanismo, ocasião, oferta/remoção de risco, quebra de objeção, comparativo, identidade/tribo, rotina, sensorial.
   - Consciência (Schwartz): inconsciente → problema → solução → produto → pronto para comprar.
   - **Conceito = persona + ângulo + oferta.** Formato vem por último. Remoção de risco ("paga ao receber", garantia) é ângulo, não rodapé. O elenco (idade, sotaque) segmenta.
5. Aponte lacunas (consciência sem cobertura, um formato só, sem ângulo de oferta).
6. Tamanho do lote pela verba: com verba baixa, menos conceitos bem diferentes. Entregue ao `estrategista-criativo`.

### Andromeda, modo 2: auditar antes de subir
1. Grade de aberturas (grátis): `python .claude/skills/andromeda/scripts/aberturas.py <pasta-do-lote> --saida <pasta>/_andromeda`. Limiar 0,85 (calibrado em 10/2026: mesmo gancho 0,89–1,00; ganchos diferentes 0,45–0,64). Sai com código 1 se achar par parecido. Confirme olhando a grade.
2. Ficha por criativo (persona, ângulo, consciência, formato, elenco, cenário, voz, mensagem), pelo arquivo/roteiro, nunca de memória.
3. Agrupe em famílias. **Não conta como diferente:** cor, fonte, título, música, legenda nova sobre a mesma filmagem, mesma pessoa trocando roupa, gancho só em texto sobre a mesma abertura. **Conta:** outra pessoa/cenário, outro formato, outra voz/estrutura, outra proposta de valor. Meta: **≥ 4 famílias, cada uma diferente das outras em ≥ 2 dimensões**.
4. Coerência gancho × corpo × página; elenco e sotaque batem com o país.
5. Compliance: liste e **pergunte** manter × suavizar.
6. Veredito: pode subir / subir com ressalvas / refazer N peças (dizendo o quê).

### Andromeda, modo 3: estrutura e leitura
Ver [13-analise-meta-ads-e-vencedores.md](13-analise-meta-ads-e-vencedores.md) (KPI por frente, funil topo/meio/fundo, corte e escala).

### Estrategista criativo (fluxo)
1. Carregue o contexto (estratégias, oferta, frente). Preço/oferta/garantia só se estiverem numa fonte.
2. Checklist de abertura numa mensagem só (ver [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md) §11). Enquanto isso, só estudo.
3. Estude referências em paralelo (1 agente por fonte): vencedores ≥720p (folha de contato, transcrição, `scdet`), canvas do Flora (`flora_get_canvas`, subagente parseia), reels (macetes acionáveis). Saída: "o que o vencedor faz → como replicamos → ferramenta".
4. Desenhe por take: cena, enquadramento, ação, fala (≤20 palavras/8 s), duração. Aplique os macetes de retenção. Mesma persona/roupa/voz no vídeo todo. Texto do anúncio + 3 títulos.
5. Compliance: perguntar. Registrar decisão em `estrategias-criativos.md`.
6. 3 abordagens com custo em US$ e tempo; recomende uma; aprovação só com gasto real. Teste de 1 cena quando o método for novo/caro.
7. Padrões de produção: transcrever cada take IA antes de usar; voz única (clone + STS); legenda pelo roteiro com alinhamento forçado (nunca whisper do vídeo montado, erra até 0,7 s); música -32 LUFS; nada de quase-duplicata; ferramenta compartilhada alterada por um agente de cada vez.
8. Fechamento: pasta de teste com N criativos = o que o orçamento de mídia comporta, nomes no padrão do gerenciador, estrutura de campanha em txt. Registre custo real e aprendizados em `estrategias-criativos.md`.

### Fluxo enxuto que funcionou (Yara BF)
Estudo em paralelo → checklist respondida → teste de 1 cena → cenas em lote com a mesma persona → clone da voz do gancho + STS → montagem (`montar.py`, legenda pelo roteiro, música -32 LUFS) → `revisar_ad.py` + sincronia + folha de contato → volume por rotação de ganchos (ex.: 5 ganchos × 3 músicas = 15 versões a custo zero; testar os 5 na mesma música e depois o vencedor nas 3) → pasta de teste + estrutura de campanha.

### Analista de copy
- **Antes de subir (sem custo):** nota 0–5 por critério: gancho (0–3 s, claro sem som), oferta (entendida em 1 frase, até ~8 s), concretude, fluxo, CTA (ação única + remoção de risco), linguagem do mercado (pronúncia da IA), compliance (listar e perguntar), coerência texto × tela × anúncio. Saída: tabela, 3 pontos fortes e 3 fracos do lote, até 2 reescritas por criativo fraco, aposta como hipótese. Lote grande: 1 agente por criativo.
- **Depois de rodar:** gasto, impressões, CPM, hook rate (3 s ÷ impressões), retenção, CTR, CPC, compras, CPA; em COD, efetividade por anúncio da fonte operacional. Amostra mínima: gasto ≥ ~1× CPA-alvo e ≥ ~1.000 impressões, senão "inconclusivo". Hook rate = 3 primeiros segundos; queda de retenção = frase daquele segundo; CTR/CPA = corpo, oferta, CTA. Compare só criativos que diferem em UMA variável.
- Conclusão no formato: padrão → evidência → confiança (alta/média/baixa) → ação.
- **Chave de ligação: nome do anúncio = nome do arquivo.**

### Consultor de cases
- Identifique a frente antes de buscar. Procure primeiro o contra-caso (quem falhou, quem discorda, sob que condições).
- `python scripts/buscar.py <pasta> "termo" "variação" "sinônimo" --contexto 1` (legenda automática destrói termo técnico: "ROAS" vira "ruas", "upsell" vira "opcel").
- Toda afirmação com episódio + timestamp e força (declarado / convergente / verificado). Número de entrevista é sempre "declarado".
- Tática só transfere com os pressupostos (recompra, custo marginal, onde entra o dinheiro, unidade de diluição, ticket, estrutura). Se não bate, diga que não transfere.

### Registrar aprendizado (sempre)
- Só fatos observados, com data, mercado, anúncios de origem e confiança.
- `banco-de-copy.md`: padrões, frases exatas vencedoras, palavras a evitar.
- `estrategias-criativos.md`: formato vencedor, macete validado, custo medido, armadilha, decisão de compliance, contradições entre heurística e dado da conta.
- Análise longa → relatório em `02-relatorios/`.

### Armadilhas
- Seedance: fala mais curta que a duração pedida → o take repete parte da frase ou inventa palavras no fim. Transcreva (`producao/onda2/verificar_takes.py`) e corte após a última palavra. Palavra errada: `producao/onda2/colar_palavra.py` (cola a palavra em TTS com a mesma voz).
- Seedance demora 5–10 min em paralelo; um take levou ~18 min. Espere até ~30 min antes de regerar.
- `flora_list_generations` às vezes dá timeout: espere ~60 s e consulte de novo.
- Posts do Facebook via Playwright pedem login depois de ~2: peça o link da Biblioteca ou o arquivo.
- Dois agentes editando o mesmo `montar.py`: arriscado. Uma etapa que altera ferramenta compartilhada roda sozinha.
- Legenda modo roteiro do `montar.py`: bug do 1º bloco após o gancho com duração zero (corrigido no `DEWALT-ADS/edicao/montar.py`; o do Yara tem o mesmo código). Medir com `medir_sinc.py` e conferir `faladas_sem_legenda`.

### Lacunas
- Frases vencedoras validadas com dado: nenhuma registrada ainda (aguardando resultados YARA-BF e DeWalt). **Precisa de revisão manual** quando os testes tiverem dados.
- Banco de copy de Infoproduto e X1: vazio no `banco-de-copy.md`. **Precisa de revisão manual.**
- Políticas de saúde vigentes da Meta (página oficial deu 404 no estudo): **precisa de revisão manual**.

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [04-fluxo-producao-criativos.md](04-fluxo-producao-criativos.md)
- [07-variacoes-gancho-corpo.md](07-variacoes-gancho-corpo.md)
- [08-voz-e-dublagem.md](08-voz-e-dublagem.md)
- [11-revisao-e-qualidade.md](11-revisao-e-qualidade.md)
- [13-analise-meta-ads-e-vencedores.md](13-analise-meta-ads-e-vencedores.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [projetos/](projetos/)
