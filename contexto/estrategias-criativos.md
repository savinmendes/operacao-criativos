# Estratégias de criativos — memória da operação

Lida pela skill `estrategista-criativo` antes de planejar qualquer criativo. Só fatos observados, com data.
Acrescente aprendizados novos no fim de cada seção.

## Formatos que venceram

### COD perfumes árabes — "consultora IA + unboxing real" (Chile, página Comercial Andes, set/2026)
- Fonte: posts 122121238455420219 e 122121238329420219 (pack masculino 3x1). Estudo: `Downloads/YARA-CL/_ref/`.
- Duração de 53–57 s, em 9:16 720p.
- **Gancho (3–8 s):**
  - Vencedor B: consultora de perfumaria em IA falando para a câmera, com os frascos reais na bancada.
  - Vencedor A: moça dançando, no estilo TikTok.
- **Corpo:** narração em ES sobre takes reais de unboxing (só mãos, sem rosto), com troca de plano a cada 1,5–4 s.
  - Cada perfume ganha ~3 frases: nome + 3 adjetivos / sensação / ocasião.
- **CTA:** "Haz tu pedido ahora y paga solamente cuando lo recibas".
- **Na tela:**
  - Legenda palavra a palavra, branca, com a palavra-chave em amarelo, no meio da tela.
  - Faixa fixa no topo à esquerda: "PAGO CONTRA ENTREGA / ENVÍO EN 24 HORAS", com caminhão, em azul-marinho.
  - Adesivo fixo no rodapé com os frascos recortados.
- **Texto do anúncio:** "🔥 Los 3 perfumes árabes del momento en un solo pack", lista dos 3 nomes, 3 benefícios com emoji, "📦 Envío GRATIS en todo Chile / 💳 Pago contra entrega".

## Pipeline de IA validado (Flora)
- Projeto de referência: "Videos de Ganchos VEO3 Perfumes" (prj_ns76ea9xz3vj9xr5nkaxagt69h826xk1).
- **Cadeia:**
  1. Cena base (consultora na perfumaria).
  2. GPT Image 2 troca os perfumes pela referência do produto.
  3. (Opcional) GPT Image 2 troca a persona.
  4. Seedance 2.0 i2v com a fala em 8–11 s.
  - Montagem e legenda ficam fora do Flora.
- **Prompt de imagem (troca do produto):** "altere os perfumes da mesa e da mão da mulher pelos perfumes da referencia. coloque os perfumes com realismo. 3 PERFUMES".
  - Funciona melhor com a descrição exata de cada frasco e "não invente frascos".
- **Prompt de troca de persona:** "troque caracteristica fisicas da mulher e roupas/cores de roupas. matenha todo o cenario e obeto identicos."
- **Prompt de vídeo (Seedance):** "a mulher fala olhando para camera e com confiança em ESPANHOL: \"<fala>\". SEM CORTES DE CAMERA E NEM MUDANÇA DE ANGULO E NEM ZOOM, NEM EFEITOS DE AUDIO OU VIDEO."
  - Acrescente "NO FALE EM INGLÊS NEM PORTUGUÊS" e "SEM MÚSICA, SEM LEGENDAS".
- **Fala:** máx. ~20 palavras a cada 8 s. Palavras parecidas com o português ("stock") podem sair em PT ("estoque"); prefira sinônimos sem ambiguidade ("liquidación total").
- **Voz única: VALIDADO (09/10/2026).** Clone no ElevenLabs a voz do gancho aprovado e passe a fala nativa de cada take Seedance pelo **speech-to-speech** (`YARA-CL/producao/voz/sts.py`, eleven_multilingual_sts_v2). O tempo se mantém (sincronia de 0 a 5 ms), então dispensa o lipsync do HeyGen. As narrações sobre B-roll saem do TTS com o mesmo clone. O STS mantém a pronúncia original: palavra errada no take continua errada.
- **Montador com os macetes:** `YARA-CL/producao/edicao/montar.py`.
  - Faz punch-in alternado, whoosh, título de abertura, banner, sticker e selo no B-roll, legenda palavra a palavra e CTA final.
  - Por segmento aceita `legenda_y`; na legenda aceita `juntar`, `fundir` e `inicio`.
- **Voz (histórico):** cada geração do Seedance sai com uma voz diferente. Num vídeo inteiro com a mesma pessoa, use uma voz única (ElevenLabs, clone da voz aprovada) + lipsync (HeyGen speed, trechos ≤12 s) ou um modelo com áudio de entrada.

## Custos medidos
| Data | Item | Cotação do catálogo | Cobrado |
|---|---|---|---|
| 09/10/2026 | GPT Image 2 (is2i), 2k high | US$ 0,25 | **US$ 0,53** (use 1k para baratear) |
| 09/10/2026 | Seedance 2.0 i2v, 11 s 720p | US$ 1,06 | **US$ 2,33** (~US$ 0,21/s: cobra por segundo) |
| 09/10/2026 | Seedance 2.0 i2v, 5 s / 6 s / 9 s / 10 s | US$ 1,06 | US$ 1,06 / 1,27 / 1,91 / 2,12 |
| 09/10/2026 | AD-C completo, 48 s (gancho + 4 consultoras + 3 B-rolls reais) | — | ~US$ 10 no Flora (com refação do gancho); ElevenLabs desprezível |

## Macetes de retenção (reel de referência, 09/10/2026)
- **Gancho visual antes da fala:** título grande e colorido, elementos e efeito sonoro já no quadro 1.
- **Movimento na primeira cena:** câmera na mão, pessoa fazendo algo. Nada estático.
- **Dinamismo, que é o principal:** um ângulo diferente a cada frase (aberto, médio, close, zoom rápido no rosto) e troca de local a cada bloco de assunto.
- **Legenda e títulos:** palavra a palavra no centro; às vezes uma palavra gigante na tela.
- **Inserções sobre a fala:** prints e vídeos de exemplo entram por cima da pessoa.
- **Final com ação clara:** comentar uma palavra, pedir agora, pagar ao receber.

## Banco de takes reais
- `Downloads/YARA-CL/banco/`: 43 takes de mãos com Yara, Yara Moi e Yara Elixir. Índice em `indice.json`.
  - Os takes moi_01 a moi_06 têm legenda pequena queimada.
  - Nenhum take mostra o kit dos 3 juntos nem o borrifo.

## Decisões de compliance e oferta (da pessoa)
- 09/10/2026, Kit Yara (COD Chile), Black Friday:
  - Oferta: "pagas dos y el tercero gratis" e "muy por debajo del precio de mercado", com tema de liquidação de estoque de Black Friday.
  - **Não falar o preço** no vídeo.

## Volume barato e legenda (09/10/2026)
- **Rotação de ganchos a custo zero:** 5 ganchos × 3 músicas = 15 versões sobre o mesmo corpo. Os ganchos são montados com material existente:
  - oferta primeiro;
  - pessoa cheirando o frasco + pergunta em texto;
  - unboxing real com a voz por cima;
  - closes com o nome de cada frasco.
  - Teste sugerido: os 5 ganchos na mesma música e depois o vencedor nas 3 músicas.
- **Legenda:** nunca transcrever o vídeo montado com whisper, porque erra até 0,7 s. Use o texto do roteiro com alinhamento forçado no áudio limpo de cada segmento (`montar.py` `"modo": "roteiro"` + `alinhar_roteiro.py`, CTC wav2vec2 espanhol).
- **Loja movimentada no Seedance:** pedir "clientes desfocados ao fundo" gera loja bem cheia e pouco desfocada; funciona, mas não fica bokeh forte.
- **Música de fundo:** -32 LUFS sob a fala, com ducking de 11 dB. A -24/-27 a pessoa achou alta.

## Retrospectiva da produção Yara BF (09/10/2026): erros, bugs e loops que não devem se repetir

### Decisões que mudaram no meio e custaram retrabalho
| O que aconteceu | Custo | Regra daqui pra frente |
|---|---|---|
| Overlays e roteiro feitos com preço ($59.900). Depois a oferta virou "paga 2 lleva 3, sem falar preço" | Overlays e roteiro refeitos | **Fechar a oferta ANTES de produzir**: mecânica, se fala preço, escassez, tema (BF etc.) |
| Música entrou alta (-24/-27 LUFS). A pessoa pediu mais baixa | 6 versões remixadas | **Padrão: -32 LUFS sob a fala**, com ducking de 11 dB |
| Legenda feita por whisper no vídeo montado, com até 0,7 s de atraso | 21 vídeos remontados | **Padrão: legenda pelo roteiro** com alinhamento forçado (`montar.py` modo roteiro) |
| O gancho saiu com "estoque" (PT) em vez de "stock" | US$ 2,12 para regenerar | Evitar palavra parecida com o português na fala do Seedance e **transcrever cada take antes de usar** |
| A pessoa entendeu "vídeo inteiro" de outro jeito: AD-C × opção A | Uma rodada de explicação | Nomear versões pelo que mostram (ex.: "consultora em tudo" × "consultora + unboxing") e dizer o que é cada uma |
| Muitas pendências repetidas em várias mensagens (A/B/C, stock/estoque, escassez…) | Loop de perguntas | **Juntar todas as decisões numa checklist só, no início**, e não repetir depois |
| H1 ficou quase igual ao AD-C | Criativo duplicado | Não produzir quase-duplicata; variação tem que mudar o gancho de verdade |
| 25 vídeos produzidos para US$ 100/dia de mídia, que comporta ~7 | Volume que não cabe no teste | **Perguntar o orçamento diário de mídia no início** e dimensionar o volume por ele |

### Bugs técnicos e a solução
- **Posts do Facebook pelo Playwright:** depois de ~2 posts pede login. Pedir o link da Biblioteca de Anúncios ou o arquivo, em vez de insistir.
- **Heredoc no Git Bash** estraga barra invertida em script Python: criar `.py` com a ferramenta Write.
- **Emoji/acentos no Windows (cp1252):** rodar com `PYTHONIOENCODING=utf-8` / `PYTHONUTF8=1`.
- **faster-whisper:** a GPU falha (`cublas64_12.dll`). Usar `device='cpu', compute_type='int8'`.
- **Preço real no Flora:** imagem 2k sai a US$ 0,53 (a cotação diz 0,25) e o Seedance cobra ~US$ 0,21/s. Orçar com o preço real, nunca com a cotação do catálogo.
- **`flora_list_generations`** às vezes dá timeout: esperar ~60 s e consultar de novo (o job continua rodando).
- **Pronúncia no Seedance:** nomes de marca e palavras raras escorregam (Moi→"muy", Orquídea→"Orquía", frutilla→"frutita"). O STS mantém o erro. Transcrever cada take; se errar, colar a palavra em TTS com a voz clonada ou escrever a grafia fonética no prompt.
- **Dois agentes editando o mesmo script** (`montar.py`) ao mesmo tempo: arriscado. Uma etapa que altera ferramenta compartilhada roda sozinha; as outras esperam.
- **Legenda modo roteiro (`montar.py`, achado na revisão DeWalt 10/10/2026):** (1) `_ajustar_por_segmento` procurava o segmento do primeiro para o último; como o `_snap()` põe o início 12 ms antes do corte, o 1º bloco depois do gancho caía no segmento anterior e ficava com duração zero (não aparecia). Corrigido no `DEWALT-ADS/edicao/montar.py` (busca do último para o primeiro); o `montar.py` do Yara tem o mesmo código. (2) O alinhamento do ElevenLabs adianta até 190 ms palavras depois de pausa: agora o início vem da energia da fala, limitado a ±80 ms do CTC. Medir sempre com `medir_sinc.py` e conferir `faladas_sem_legenda`.
- **Upload staged no Shopify:** o tamanho do arquivo é travado. Se o vídeo for re-renderizado depois, pedir novo staged upload. Subir só a versão final.

### Onda 2 Yara BF (10/10/2026): o que se aprendeu
- **Seedance no fim do take:** quando a fala é mais curta que a duração pedida, o take às vezes **repete parte da frase ou inventa palavras** no final (C2 gancho, C5 gancho). Transcreva cada take (`producao/onda2/verificar_takes.py`, whisper GPU com tempo por palavra) e corte depois da última palavra do roteiro.
- **"ñ" no Seedance:** "muñecas" saiu "mullegas" / "muy jegas" em 2 takes diferentes. Correção sem regerar: `producao/onda2/colar_palavra.py` (silencia o trecho e cola a palavra em TTS com a mesma voz; duração preservada). Confira com whisper depois.
- **Uma voz por avatar:** STS (`sts.py --voz <id>`) com vozes de catálogo diferentes por pessoa (Isa Pro chilena, Gaby, Karly, Carolina, Cristina) + "Chilena" e "Consultora Yara BF". Mantém o tempo (±0,05 s).
- **Tempo do Seedance:** 10 takes em paralelo saíram em 5–10 min; um deles levou ~18 min. Esperar até ~30 min antes de regerar.
- **Banco de takes:** moi_01–06 têm legenda queimada de terceiros e moi_11–12 têm prateleira com outras marcas ao fundo. Para frasco limpo use moi_07–09.
- **Selo BF redondo** (canto superior direito no B-roll) colide com texto grande no topo: desligue o selo (`"selo": null`) quando o segmento tiver título/rótulo próprio no topo.
- **Mixador genérico:** `producao/musica/mixar_generico.py video leito saida [base_db]` (trilha própria A/B/C; C1 sem fala usou base +6).
- Custo real da onda (7 criativos): US$ 20,32 no Flora (7 imagens GPT Image 2 1k a ~US$ 0,27 + 11 takes Seedance 2.0 a ~US$ 0,21/s).

### Shopify (loja da pessoa)
- O conector **bloqueia gravar no tema publicado** e **publicar tema**. Caminho: `themeDuplicate` → gravar na cópia → testar com `?preview_theme_id=` → a pessoa clica em Publicar.
- `templates/product.json` é usado por todos os produtos. Para mostrar algo só numa categoria, colocar uma seção no `footer-group.json` com filtro por coleção (ex.: `pa-produto-video`).
- Depois de publicar, **mandar a URL exata e onde rolar** ("fim da lista de produtos") e conferir no ar com o Playwright.

### Formato "depoimento + autoridade" aprovado pela pessoa (série SB Medalla, 14/10/2026)
Sem dado de performance ainda: é o formato que a pessoa aprovou depois do raio-x (`completar-criativo`), não um vencedor medido.
1. **Gancho (0–6 s):** persona ajoelhada rezando no próprio lugar vazio, com o vazio legível no 1º quadro. Fala firme: "Recé … y esto fue lo que pasó". Título vermelho e branco de "algo inesperado".
2. **Reza curta sussurrada** → **virada visual** (o lugar cheio), sem fala, com a trilha trocando de tensão para esperança.
3. **Frustração:** a persona olhando o próprio vazio, na 1ª frase da dor.
4. **Selfie emocionada:** a dor no nível de identidade ("me sentía un fracasado") + "un padre explicó algo que nadie me había dicho sobre la medalla".
5. **Autoridade (padre):** o mecanismo (o que dizem as letras da medalha; "no es falta de fe") + a projeção do futuro.
6. **CTA único**, com motivo verdadeiro (transmissão 24 h confirmada pela pessoa). Nada depois.

Personas feitas no formato: comerciante, motorista de app, costureira, avó, mãe solo, agricultor, desempregado de 50+, acompanhante de UTI, feirante, casal e dona de pensão. Cada uma tem voz própria e o mesmo padre. Os vídeos estão em `Downloads/SB-MEDALLA-COMPLETA-ES/`. Ao subir, registrar aqui o resultado por persona.

### Checklist de abertura (perguntar tudo numa mensagem só)
1. Link do produto e da página de destino.
2. Oferta: mecânica (ex.: paga 2 leva 3), **fala preço ou não**, escassez real, tema (BF, Natal…).
3. Mercado e idioma; avatar/cena base (imagem da pessoa?).
4. Vencedores de referência (arquivo ou link da Biblioteca de Anúncios) e projeto do Flora.
5. **Orçamento diário de mídia** (define quantos criativos) e teto de produção em US$.
6. Música (trend real liberada pela pessoa) e formato (9:16; precisa 4:5?).

### Fluxo enxuto que funcionou (ordem)
1. Estudo em paralelo (vencedores + Flora + referências).
2. Checklist de abertura respondida.
3. **Teste de 1 cena** (imagem + vídeo) para aprovar a qualidade.
4. Cenas em lote com a mesma persona.
5. Clone da voz do gancho aprovado + STS em todos os takes.
6. Montagem (`montar.py`, legenda pelo roteiro, música -32 LUFS).
7. `revisar_ad.py` + sincronia da legenda + folha de contato.
8. Volume por rotação de ganchos, dimensionado pelo orçamento de mídia.
9. Pasta de teste + estrutura de campanha.
