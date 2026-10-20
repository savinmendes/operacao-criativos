# Onda 2: kit 3 Yara · Black Friday · COD Chile (10/10/2026)

São 7 criativos novos, um para cada conceito, para diversificar o teste no Meta (Andromeda).
Todos vendem o **kit dos 3 perfumes** com "pagas 2, te llevas 3", sem preço. Formato 9:16, 720p.
Os ângulos vieram da análise dos 50 virais orgânicos (`_ref/virais/_analise/matriz_andromeda_yara.md`).

| Arquivo | Conceito | Etapa do funil | Duração | Quem aparece |
|---|---|---|---|---|
| `C1_yara-kit3_hueles-a_es-cl.mp4` | Sensorial sem fala: "POV: hueles a…" | topo | 14 s | só frascos (banco) + música |
| `C2_yara-kit3_uno-para-cada-momento_es-cl.mp4` | Uno para cada momento (día / cita / noche) | meio | 27 s | especialista 45+ (voz Isa, chilena) |
| `C3_yara-kit3_1-2-gratis_es-cl.mp4` | "1, 2… ¡y el tercero gratis!" | fundo | 8 s | mãos abrindo o kit |
| `C4_yara-kit3_que-perfume-traes_es-cl.mp4` | A amiga pergunta "¿qué perfume traes?" | topo | 17 s | 2 jovens (carro + café) |
| `C5_yara-kit3_lo-estas-aplicando-mal_es-cl.mp4` | Educativo "lo estás aplicando mal" | topo/meio | 30 s | criadora de beleza 30 |
| `C6_yara-kit3_regalo-navidad_es-cl.mp4` | Presente de Natal | meio | 11 s | mãe e filha (**subir em novembro**) |
| `C7_yara-kit3_cuanto-pague_es-cl.mp4` | "Me preguntaron cuánto pagué…" | meio/fundo | 21 s | mulher 30, pronta para sair |

`sem-musica/` tem as mesmas versões sem trilha. A trilha das versões principais é própria, gerada por IA, a -32 LUFS sob a fala.

## Texto do anúncio (primary text, um por conceito)
- **C1:** 🌸 ¿Dulce, floral o intenso? Con este kit no eliges: te llevas los 3 Yara. 🖤 Black Friday: pagas 2 y te llevas 3 · ✅ Pagas al recibir · 🚚 Envío gratis a todo Chile.
- **C2:** ¿No sabes cuál elegir? Yara para el día, Yara Moi para una cita y Yara Elixir para la noche. 🖤 Black Friday: pagas 2 y te llevas los 3. ✅ Pagas al recibir · 🚚 Envío gratis.
- **C3:** 1… 2… ¡y el tercero gratis! 🎁 Kit Yara, Yara Moi y Yara Elixir. ✅ Pagas al recibir · 🚚 Envío gratis a todo Chile. Quedan pocas unidades 👇
- **C4:** "¿Qué perfume traes?" 😍 La pregunta que más vas a escuchar. Kit de 3 perfumes árabes: pagas 2 y te llevas 3. ✅ Pagas al recibir · 🚚 Envío gratis.
- **C5:** ¿Te frotas las muñecas después de echarte perfume? 😬 Error #1. Mira cómo aplicarlo bien y elige uno para cada momento. Kit 3 Yara: pagas 2, te llevas 3 · Pagas al recibir.
- **C6:** 🎄 Regalo de Navidad resuelto: 3 perfumes árabes en un solo kit, uno para regalar y dos para ti. Black Friday: pagas 2 y te llevas 3 · Pagas al recibir · Envío gratis.
- **C7:** "¿Cuánto pagaste?" 👀 Todos preguntan qué perfume es. Kit Yara, Yara Moi y Yara Elixir: pagas 2 y te llevas 3. ✅ Pagas al recibir · 🚚 Envío gratis.

Títulos: use os títulos do lote atual (`TESTE-7-criativos/texto_do_anuncio.txt`).

## Como subir (sugestão Andromeda)
- No teste atual, **troque CJ01 e CJ06** (quase iguais ao AD-C) por **C1 e C4**. Junte **C2, C3, C5 e C7** como novos conjuntos ou no lugar dos que perderem.
- No nome do anúncio, use o conceito (ex.: `C4_elogio_amiga_topo`) para ler o resultado por ângulo.
- Decida pelo **pedido entregue/pago** por anúncio, não pelo CPA do gerenciador.

## Revisão
- `revisar_ad.py` (whisper es, termos proibidos, quadro solto, silêncio, salto de áudio): **7/7 OK**. Os relatórios e as folhas de contato estão em `_revisao/`.
- Correções feitas antes da entrega:
  - "muñecas" mal pronunciado no C5: colado com a mesma voz.
  - Sobras de fala no fim dos takes do C2 e do C5: cortadas.
  - Selo sobre os textos do C1, C2 e C3: removido.
  - Take do Moi com legenda de terceiro (C1): trocado.
  - 2 quadros soltos (C2 e C3): corrigidos.

## Pontos para você decidir / conferir
1. **C7 ("¿cuánto pagué?")** foi feito na versão **sem citar nenhuma marca** e sem "cheiro de luxo". Se quiser mais agressivo ou mais suave, é decisão sua.
2. **Notas olfativas** no C1 e no C2 (vainilla/mandarina, jazmín/caramelo, frutos rojos): são as do roteiro do AD-C. Confira se batem com a ficha oficial.
3. **"Quedan pocas unidades"** aparece só no texto do C3, como você aprovou antes. Use só se for verdade.
4. **C4:** a amiga fala "Huele demasiado rico" (e não "Hueles"). O sentido é o mesmo, e a legenda acompanha o que ela fala.

## Custo
- **US$ 20,32 no Flora** (teto: US$ 25).
  - 7 imagens GPT Image 2: US$ 1,90.
  - 11 takes Seedance 2.0 (~88 s): US$ 18,41.
- ElevenLabs (vozes e narrações): sai da cota do plano.
