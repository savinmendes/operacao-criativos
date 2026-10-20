# Receita: ranking orgânico → anúncio San Benito ES

Usada pela skill `replicar-vencedor-organico`. Este é o arquivo da oferta: a skill não guarda nada disso.

## Oferta e funil
- **Frente:** infoproduto, oferta San Benito ES («Camino de Fe con San Benito»).
- **Funil:** o anúncio leva à VSL (oracionsagrada.site), que conta uma oração ao vivo com milhares de pessoas.
- **A VSL ensina outra oração.** O anúncio **nunca** revela as 12 palavras. Ele mostra só o começo da invocação («Oh poderoso San Benito, guardián de los arcanos sagrados, que venciste a las serpientes con la señal de la cruz…») e corta com «¡Alto! El resto no lo puedo decir aquí».
- **Nunca dizer:** Grimorio, libro, collar, «12/doce palabras», «24 horas», hora do dia («esta noche») ligada à live, «no sé por cuánto tiempo», nome de padre de outro perfil.
- **A linha METODO foi invalidada** por prometer uma live que a página não entrega. A promessa tem que ser a mesma da VSL: «la estoy rezando completa, en vivo, paso a paso».

## Anúncio
- **Página:** Padre Juan Méndez.
- **Título:** «🔴 EN VIVO: La oración a San Benito que casi nadie conoce 🙏».
- **Botão:** «Ver más» (LEARN_MORE / SEE_MORE).
- **Texto principal:** copiar inteiro de `Downloads/SAN-BENITO-ES-VENCEDORES/SB-ES_02_ADS-6.txt`.

## Persona: padre Juan Méndez (substitui a autoridade do original)
- **Rosto da página:** `Downloads/SB-ES_PADRE-CAPTURADO/_ref/padre_juan_mendez_PAGINA.png`. Homem de ~55 anos, óculos de aro fino, casula verde com bordô e dourado.
- **Retrato sério** (o retrato original sorri e o avatar mostrava os dentes): `Downloads/VIDEO-04-ADAPTAR_analise/producao/` (`jm_serio.png`).
- **Cenário:** sempre o do padre do original (fundo, ambão, microfone de haste), feito com gpt-image a partir da referência.
- **Voz:** clone `BskzYZ6zvapoZ3mBu93C`, eleven_multilingual_v2, firme e incisiva.
- **Moldura de live:** «padre.juanmendez», a partir de `Downloads/SB-ES_PADRE-CAPTURADO/corpo/_trab/ov/moldura_jm.png`.

## Padrões visuais e de som
- **Selo VIDEO FICTICIO:** 10% de opacidade, do primeiro ao último quadro. Arquivo: `Downloads/SB-ES_PADRE-CAPTURADO/corpo/_trab/ov/selo10.png`.
- **Legenda:** palavra a palavra, branca, com a palavra falada em verde.
- **Faixa vermelha de notícia** no idioma do anúncio. O logo de TV é inventado (ex.: «NV / NOTIVISIÓN»).
- **Efeitos fixos:** glitch com «TRANSMISIÓN ELIMINADA» no «¡Alto!», «🔴 EN VIVO» no trecho da live e setas vermelhas «TOCA EN «VER MÁS»» no fim.
- **Trilha:** `Downloads/VIDEO-04-ADAPTAR_analise/producao/musica/` (`tensao.mp3` → `esperanca.mp3`), a −32 LUFS.
- **B-roll:** banco `Downloads/SB-BANCO-BROLL/` (`indice_geral.json`).
- **Vozes dos personagens:** registradas em `Downloads/SB-ES_PADRE-CAPTURADO/_vozes.json`. A conta ElevenLabs está no limite de 160 vozes, então não clonar voz nova.

## Origem
- **Perfil:** @santaespiritualidade, da própria pessoa, com rostos e takes liberados.
- **Ranking:** `Downloads/SANTAESPIRITUALIDADE_TOP50-RANKING/` (junção `08-entregas/infoproduto_ref-santaespiritualidade-top50`). Foram carregados 482 de 520 posts.

## Produzido
| Ranking | Original | Saída | Custo real | Observações |
|---|---|---|---|---|
| 01 (628 mil likes) | Notícia: restaurante vazio → lotado + dono + frade | `_analise_01/ENTREGA/`: v3 + 5 ganchos (G1 EN VIVO, G2 VACIO, G3 BORRADO, G4 PUERTA, G5 MONEDAS) | ~US$ 1,15 + ~30 créditos HeyGen | O LaMa borrou o rosto do dono; ele foi refeito com retrato novo + avatar. Saíram carro com logo VW, planta e pés como b-roll. Duração ~1:40 |
| 02 (331 mil likes) | Patrão humilha funcionária na loja + selfie + padre | `_analise_02/ENTREGA/SB-ES_RANKING02_JEFE-HUMILLA.mp4` | ~US$ 0,62 + ~23 créditos HeyGen | O patrão está de perfil e ficou sem lipsync (a pessoa aceitou). A voz gritada (eleven_v3) e a da mulher chiavam: corrigido com de-esser + shelf por trecho |
| 04 (252 mil likes) | Apresentadora (PIP) + bispo revela oração do salário + depoimento de celebridade no sofá | `_analise_04/ENTREGA/SB-ES_RANKING04_SUELDO.mp4` (1:41) | ~US$ 0,86 + ~33 créditos HeyGen (estimado: a conta caiu 67 com o R03 rodando junto) | Tudo avatar (Juan, apresentadora, senhor anônimo no sofá do original), sem lipsync. O nó gpt-image saiu 16:9 por padrão e custou uma refação do Juan (US$ 0,11): setar `aspect_ratio` 9:16 antes. Legenda PT dos b-rolls coberta por caixa opaca. Apresentadora e senhor chiavam (HF −17/−21 dB): de-esser + shelf por trecho. Duração acima da estimativa (1:31): Juan fala devagar |
| 03 (288 mil likes) | Telejornal: vítima em chroma sobre câmera de segurança (patrão demite) + selfie + padre | `_analise_03/ENTREGA/SB-ES_RANKING03_DESPEDIDA-CAMARA.mp4` (1:44) | ~US$ 0,74 + ~31–34 créditos HeyGen (estimado: a conta caiu 67 com o R04 rodando junto) | Voz nova da mulher: Gabriela (já na conta, ≠ Carolina do R02). A mulher do chroma tinha legenda PT na cabeça: apagada com LaMa (fora do rosto) e trocada por Avatar IV em fundo verde, recolocado na frente do rodapé NV. O Avatar IV da selfie «triste» sorriu com dentes na 1ª metade: coberto por b-roll. Carro do original tinha logo na calota: trocado por banco SB (dinheiro no balcão + porta abrindo). Nó gpt-image em 16:9 custou 2 refações (US$ 0,18). Folha de contato com `-ss` antes do `-i` derivou ~7 s depois de 1:30: conferir os tempos dos b-rolls com seek na saída |

## Lições para o próximo
- **Rosto com legenda queimada:** nunca usar LaMa. Gerar retrato novo e animar no avatar.
- **Legenda sobre corpo ou fundo:** cobrir com caixa opaca no mesmo lugar.
- **Rosto de perfil:** não sincroniza no HeyGen. Avisar antes e deixar a pessoa decidir.
- **Duração:** as falas literais ficam em ~1:25–1:45. Para encurtar, cortar fala (o bloco do Salmo ou da lenda) com o ok da pessoa.
- **Chiado:** conferir os agudos por trecho em toda voz gritada ou TTS brilhante antes de entregar.
- **Retrato no gpt-image (flow ElevenLabs):** o nó sai 16:9 mesmo com «9:16» no prompt. Rodar `creative_update_node` com `aspect_ratio: 9:16` antes de gerar.
- **Celebridade ou rosto real no original:** trocar a pessoa inteira por um personagem anônimo novo no mesmo cenário (retrato novo + avatar), como no senhor do R04.
