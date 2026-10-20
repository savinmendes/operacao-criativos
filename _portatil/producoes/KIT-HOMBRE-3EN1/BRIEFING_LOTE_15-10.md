# Lote Perfumes Árabes, Kit Hombre 3 en 1 (COD Chile), 15/10/2026

## Decisões da pessoa (não reabrir)
- **Os anúncios vencedores são da pessoa.** Pode reaproveitar takes, cenas e vozes e clonar a voz da consultora.
- **Mercado e preço:** COD Chile, **sem preço** no vídeo. A oferta é «3 perfumes al precio de 1» + «paga al recibir» + envío en 24 horas.
- **Tirar «100 unidades / ahora o nunca».** Não há escassez real. Nenhum número de estoque.
- **Letreiro da loja:** ESSENZALUX vira **ARABESPERFUME**, nos takes reaproveitados e nos novos.
- **«Los perfumes que vuelven locas a las mujeres»:** fica como no vencedor (decisão pendente da pessoa; não suavizar sozinho).
- **Volume:** 12–14 criativos. **Teto total do lote:** US$ 15 em Flora/Kling/Seedance (cada agente tem o seu teto abaixo) + créditos HeyGen do plano.
- **Formato:** 9:16, 720×1280 ou maior, 30 fps.
- **Selo fixo:** «PAGO CONTRA ENTREGA · ENVÍO EN 24 HORAS» no topo.
- **Rodapé:** os 3 frascos, como no vencedor.

## Produto
**Armaf Club de Nuit Intense + Lattafa Asad + Afnan 9PM** (pack masculino).

**Página de destino:** `chileverificada.com/products/lattafa`. Nunca mostrar o domínio nem o preço no vídeo.

**Notas olfativas oficiais:** a pessoa não confirmou. Use só os adjetivos do vencedor:
- Armaf: fresco, masculino, poderoso
- Asad: intenso, sofisticado, seductor
- 9PM: elegante, moderno, refinado

## Material existente
- **Vencedor:** `C:\Users\PICHAU\Downloads\VENCEDORES-3-PRODUTOS\ARABE\ARABE_1.mp4` (360p; transcrição em `ARABE_1_transcricao.txt`). Estrutura:
  1. consultora no balcão (gancho + oferta, 0–8 s);
  2. unboxing com mãos de cada perfume (nome + 3 adjetivos + benefício);
  3. CTA COD.
- **Matriz Andromeda:** `C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\matriz_andromeda_hombre.md`, com os conceitos M1–M8 e as falas sugeridas. Leia antes.
- **Nós do Flora:** `KIT-HOMBRE-3EN1\flora\indice_flora.md`. Projeto "Videos de Ganchos VEO3 Perfumes" (`prj_ns76ea9xz3vj9xr5nkaxagt69h826xk1`). O nó `n2` traz os 3 frascos em fundo branco. Os 10 takes Seedance da consultora ESSENZALUX são de 28/09.
- **Bases:** vencedores em `C:\Users\PICHAU\Downloads\YARA-CL\_ref\venc_*.mp4` (unboxing em HD?) e virais em `YARA-CL\_ref\virais\_analise\`.
- **Pipeline validado** (ver `C:\Users\PICHAU\Downloads\Produtividade com ia\Contexto\estrategias-criativos.md`, lote Yara):
  1. GPT Image 2 para trocar o produto na imagem base;
  2. Seedance 2.0 i2v com fala nativa ≤ 20 palavras / 8 s;
  3. clone da voz + speech-to-speech do ElevenLabs para voz única;
  4. legenda pelo roteiro, música a −32 LUFS.
- **Lições** (skills `gerar-midia-ia`, `editar-criativo`, `revisar-criativo` e `contexto/22` do repositório):
  - sem porta ou gente entrando em veículo no Kling;
  - gancho com o contexto legível;
  - 1 voz por personagem;
  - transcrever cada take do Seedance, porque ele inventa palavras no fim;
  - CTA único;
  - selo/letreiro sem cobrir o rosto;
  - confirmar a olho os alarmes do QA de IA.

## Divisão (definida antes de gerar; cada agente usa só a sua subpasta)

Saída: `C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\LOTE-15-10\<NN>_<CODIGO>.mp4` + `_narracion.txt` (roteiro + texto do anúncio ES-CL: título ≤ 40 caracteres e texto principal, sem preço). Trabalho em `LOTE-15-10\_trabalho\<agente>\`.

| Agente | Criativos | Teto Flora |
|---|---|---|
| **A: vencedor HD** | 01 vencedor refeito em HD, fiel (consultora com o letreiro ARABESPERFUME + unboxing + CTA, sem «100 unidades»); 02 mesmo corpo com gancho novo de homem (M2 «¿Qué perfume usas?»); 03 versão curta de 30 s | US$ 3,50 |
| **B: M2 + M4** | 04 M2 elogio (homem chileno de 25–40 anos recebendo elogio, revela o pack); 05 M4 «paga al recibir» como ângulo (desconfiança de comprar perfume online → paga na porta); 06 variação de gancho de 04 | US$ 4 |
| **C: M5 + M1** | 07 M5 educativo «3 errores al comprar perfume» (homem falando para a câmera); 08 M1 ocasião (trabalho / noite / fim de semana, um perfume para cada); 09 variação de gancho de 08 | US$ 4 |
| **D: M7 + M6** | 10 M7 sensorial sem fala (macro dos frascos, borrifada, luz, texto na tela + música); 11 M6 teste às cegas (amigos cheiram e reagem); 12 variação de gancho de 11; 13 estático/carrossel opcional a partir dos melhores quadros | US$ 3,50 |

Cada agente:
- personagens novos de IA só por texto (homens chilenos de 25–40 anos, cenários chilenos);
- registra as vozes em `LOTE-15-10\_trabalho\_vozes.json` antes de gerar (1 voz por personagem; as vozes ES-CL nativas ou clones da pessoa);
- revisa com `revisar_ad.py --idioma es`, faz zoom nos takes de IA e abre os vídeos no fim.

**Painel:** `python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa arabe-<letra> "...".`
