# Briefing — imagens + textos Linfarele (Itália), referência Erlona (07/10/2026)

A pessoa aprovou o trabalho. **Não pergunte nada.** Na dúvida, escolha o lado seguro e anote a decisão no relatório. **Nunca leia nem imprima arquivos `.env`.**

## Objetivo
Para **cada** conceito do seu lote, gerar **1 imagem nova** e escrever **título, texto principal e descrição em italiano, específicos para essa imagem**. São anúncios de imagem para o Meta, com CTA "Acquista ora", da marca **Linfarele**: gotas de drenagem linfática, 4 ervas (galio, stillingia, trifoglio rosso, frassino spinoso), poche gocce sotto la lingua ogni mattina, sa di miele.
- Oferta: **spedizione gratuita + 90 giorni di garanzia, soddisfatti o rimborsati**. Sem preço.

A referência é um concorrente (Erlona). Use o **ângulo** (quem fala, dor, virada, emoção), **nunca** copie a imagem nem o texto deles. Não suba a imagem deles no Flora: gere do zero (text-to-image).

**A imagem não mostra frasco nem produto nenhum.** É só a cena, como nos anúncios deles. Por isso, o texto não deve dizer "veja o frasco".

## Entrada
- `C:\Users\PICHAU\Downloads\ERLONA-REFERENCIA-2026-10-07\conceitos.json`: lista de conceitos `C001…C124`, com `imagem_ref`, `texto_ref_arquivo`, `gancho`, `titulo_ref` e `idioma` (alguns são do lote francês; mesmo assim, escreva em italiano).
- Abra a imagem de referência (Read) e o `.txt` completo de cada conceito antes de escrever.

## Regras de imagem (política do Meta: saúde e aparência)
**PROIBIDO:**
- antes/depois (duas fotos, dia 1 / dia 30, "prima/dopo");
- close de celulite, barriga, culote, pés ou pernas inchadas como "problema";
- corpo de lingerie ou biquíni focado na parte do corpo;
- balança com número;
- fita métrica;
- exames, raio-X, órgãos, sangue, pele com lesão;
- remédios, seringas, caixas de medicamento;
- médico ou enfermeiro receitando ou segurando produto;
- texto na imagem com promessa ("-9 kg").

**PERMITIDO** (escolha o que melhor traduz o ângulo de cada referência):
- **só o "depois", positivo:** mulher de 40 a 60 anos, vestida, leve, sorrindo; caminhando na praia de vestido; subindo escada; brincando com o neto; em viagem;
- **objeto como prova:** aliança que volta a servir, sapato ou bota que fecha, meia sem marca no tornozelo, calça jeans antiga que fecha, cinto, vestido no cabide;
- **cena da dor sem corpo:** mulher cansada no sofá às 14h, olhar para o espelho de costas (sem foco no corpo), carta de demissão, notebook à noite;
- **ilustração do mecanismo:** desenho limpo do sistema linfático em silhueta, "não é gordura, é líquido parado", fluxo de água/linfa estilizado (sem órgãos realistas);
- **ritual sem produto:** xícara de chá de manhã, janela com luz, caderno de hábitos;
- **profissional de bem-estar** (fisioterapeuta ou osteopata de roupa clínica neutra) **explicando**, sem receitar e sem estetoscópio de médico;
- **texto curto na imagem** (opcional, no máximo 6 palavras, italiano correto, sem promessa): ex. "Non è grasso. È ristagno."

**Estilo:** foto realista estilo UGC/celular (luz natural, casa italiana comum), **sem cara de banco de imagem**. Pessoas variadas (idade 40–65, tipos de corpo reais). 1:1 (1K).

## Regras de texto (italiano nativo, sem erro)
- **Título:** até ~40 caracteres, específico da imagem.
- **Texto principal:** 3–8 parágrafos curtos, em 1ª pessoa ou de profissional de bem-estar contando, com gancho na 1ª linha **ligado à imagem**, a virada "non era grasso, era ristagno linfatico", a solução Linfarele (4 erbe, gocce sotto la lingua, sa di miele) e o fecho "Spedizione gratuita e 90 giorni di garanzia: soddisfatti o rimborsati. 👇 Clicca su «Acquista ora»."
- **Descrição:** 1 linha ("Spedizione gratuita · 90 giorni di garanzia").
- **PROIBIDO no texto:**
  - nome de remédio (Levothyrox, Eutirox, Lasix, diuréticos, Ozempic);
  - doença como algo que o produto trata (tireoide/Hashimoto, endometriose, PCOS, linfedema, fígado, rim, diabetes, colesterolo);
  - kg ou números de resultado;
  - "dimagrire/perdere peso";
  - médico receitando;
  - "prima/dopo";
  - atributo pessoal dirigido ao leitor ("Hai la cellulite?", "Sei gonfia?"). Use 1ª pessoa ("Io avevo…").
- Pode citar sensação: gambe leggere, pancia sgonfia, i pantaloni chiudono, energia.

## Execução
1. Use o MCP do Flora, projeto **`prj_ns73srpqeednwwk30jzwzxfkgs8ftzsn`** (workspace `ws_qd750nr5tby8qpnr1kbqj7aft17v8ey8`).
   - Modelo **`t2i-gemini-3.1-flash-image`** (Nano Banana 2, US$ 0,072/imagem), `aspect_ratio` 1:1, `resolution` 1K.
   - Rode até 5 gerações em paralelo. Nos parâmetros de skill do Flora, use `skill_run_id` = o nome do seu lote.
2. **QA de cada imagem** (abrir e olhar): pessoa com anatomia ok (mãos, dedos), texto na imagem legível e em italiano correto, **nada da lista proibida**, nenhuma marca de terceiros, coerente com o título.
   - Reprovou: refaça **no máximo 1 vez** com o prompt ajustado.
   - Reprovou de novo: anote "revisão manual" e siga em frente.
3. Baixe cada imagem aprovada para `C:\Users\PICHAU\Downloads\ERLONA-REFERENCIA-2026-10-07\linfarele-it\imagens\L<conceito>.jpg` (ex.: `LC001.jpg`).
4. Grave **um JSON por conceito** em `...\linfarele-it\textos\L<conceito>.json`, com estas chaves: `conceito`, `ref_erlona` (lista dos anúncios), `angulo` (1 frase em PT), `prompt`, `flora_url`, `arquivo`, `titulo`, `testo_principale`, `descrizione`, `qa` ("ok" ou "revisão manual: motivo").
5. **Teto do seu lote:** número de conceitos × 2 gerações. Se passar, pare e relate.

## Relatório final (a sua resposta)
- Quantos conceitos foram feitos e quantas gerações (US$).
- Quais ficaram para "revisão manual" e por quê.
- 3 exemplos (conceito, título e 1ª linha do texto).
