# Relatório do agente C: vídeos sem narração (08, 10, 15, 17, 21, 44, 54) e textos dos anúncios

Data: 08/10/2026. **Custo: US$ 0.** Nenhuma chamada paga: sem TTS, sem clonagem de voz, sem Flora/Kling/HeyGen. Os originais não foram alterados.

## Como foi feito
- O `montar_ad.py` e o `preparar_corpo_traducao.py` do kit só geram 9:16 e exigem narração. Por isso escrevi um compositor próprio, `_C/compor.py`, que usa as setas do `overlays.py` e os metadados de cor do `comum.py`.
- Ele mantém o formato do original e cobre o texto em inglês com rótulos opacos (alpha 255) escritos em espanhol.
- Sobre isso entram o selo "PAGO CONTRA ENTREGA / ¡PAGAS AL RECIBIR!" e o CTA "Haz clic en / Más información", com as setas vermelhas do kit apontando para baixo.
- Saída: H.264 high, yuv420p, 30 fps, AAC 48 kHz estéreo 128k e faststart.
- Origem a 29,97 fps: os tempos dos cortes são convertidos por número de quadro (`fps_in`). Sem isso, sobrava 1 quadro com o rótulo da cena anterior.
- Arquivos de trabalho:
  - `videos/NN/spec.json`: receita de cada vídeo;
  - `videos/NN/NN AD - ES_revisao.txt` e `.jpg`: revisão;
  - `_C/sheet.py`: folhas de contato;
  - `_C/textos.py`: gera e confere os textos.
- Revisão: `revisar_ad.py` rodado pelo PowerShell, com `--idioma es --idioma-residual en` e a lista `_C/proibidos.txt` (FBX5, USA, UK, Canada, Shop now, código, cuotas, envío desde, 12 million, 1-year).
- Também conferi frame a frame cada corte com rótulo, para achar sobra de texto em inglês nos crossfades.

## Por vídeo
Os vídeos não têm narração, então não há voz nem caracteres de TTS: **voz = nenhuma; caracteres = 0** em todos.

### 08 (1:1, 720x720, 24,37 s, 4,0 MB). Música original
Textos na tela (EN → ES):
| Original | Espanhol |
|---|---|
| Introducing | Presentamos |
| 5-in-1 Steam Cleaning System | 5 EN 1 / SISTEMA DE LIMPIEZA / A VAPOR |
| With variable steam | CON VAPOR AJUSTABLE |
| Coração "12 Million sold worldwide" | Círculo verde "14 / MILLONES / VENDIDAS EN EL MUNDO" |
| 1. Powerful floor cleaner | 1. LIMPIADOR DE PISOS POTENTE |
| 2. Versatile hand held steamer | VAPORIZADOR DE MANO VERSÁTIL |
| 3. Window cleaner | LIMPIADOR DE VIDRIOS |
| 4. Carpet cleaner | LIMPIADOR DE ALFOMBRAS |
| 5. Garment cleaner | VAPORIZADOR DE ROPA |
| Change the way you clean | CAMBIA TU FORMA DE LIMPIAR |
| With the power of steam | CON EL PODER DEL VAPOR |

- Os números 2 a 5 dos círculos verdes ficaram como no original, porque não têm idioma.
- O "12 Million" virou "14 millones vendidas", como manda o briefing. O coração rotacionado não cabia num coração redesenhado sem deixar sobra, então virou um círculo opaco.
- Selo pequeno no canto superior direito de 2,2 s até o fim.
- CTA e setas na cena final do logo, de 21,2 s até o fim (3,2 s).
- **Revisão:** decodificação OK, nenhum salto de pts, nenhum silêncio, nenhum quadro solto, setas no último quadro e nenhum termo proibido. O whisper só ouve música.
  - RESULTADO = 1 "problema", que é a resolução 720x720. É falso positivo: a ferramenta só aceita 9:16, e o briefing manda manter o formato.

### 10 e 15 (4:5, 720x900, 8,90 s, 2,0 MB cada). Quadros idênticos, cada um com o próprio áudio
- A faixa branca "H2O X5 STEAM CLEANER" foi refeita em faixa branca opaca com "LIMPIADOR A VAPOR H2O X5", do início ao fim.
- Selo no topo direito o vídeo todo; CTA e setas sobre o mosaico de 5,0 s até o fim.
- **Revisão:** tudo OK, só aparece o falso positivo de resolução 720x900.

### 17 (9:16, 720x1280, 13,85 s, 5,5 MB). Música cantada original mantida
| Original | Espanhol |
|---|---|
| A cleaner that cleans every surface in your home | Un limpiador que limpia / todas las superficies de tu casa |
| Carpets | Alfombras |
| Floors | Pisos |
| Handheld steamer | Vaporizador de mano |
| Air fryer | Freidora de aire |
| Oven | Horno |
| Microwave and more | Microondas y más |

- Os textos estão em caixa branca opaca, com troca no quadro exato do corte.
- Selo no meio da tela; CTA e setas de 10,0 s até o fim.
- **Revisão:** RESULTADO **OK**.
  - O whisper em inglês transcreve a letra da música, que fica por decisão da dona.
  - "BOSCH" aparece impresso no micro-ondas (texto do aparelho, permitido).

### 54 (9:16, 720x1280, 9,53 s, 2,2 MB). Mestra do par
- Texto 1: "Pisos, cocina, ventanas, / alfombras y ropa: / ¡límpialo todo con / UN SOLO aparato!". "Counters" virou "cocina" para ficar neutro.
- Texto 2: "H2O X5 / Limpiador a vapor".
- Selo no meio da tela; CTA e setas de 6,0 s até o fim.
- **Revisão:** RESULTADO **OK**.

### 21 (4:5, 720x900, 9,53 s, 1,7 MB). Par 4:5 do 54
- Mesmo texto e tempos do 54, no enquadramento 4:5 nativo do original 21.
- O **áudio é o do 54**, para ficar igual à mestra. A trilha é a mesma (correlação 0,99, defasagem de 5 ms).
- **Revisão:** 2 "problemas":
  - a resolução (falso positivo);
  - um "quadro solto" em 7,67/7,73 s. É **do próprio original**: 1 quadro de movimento borrado no corte, que também existe no 54 original. Não é defeito da edição.

### 44 (1:1, 720x720, 3,37 s, 0,1 MB). Sem som
- Refeito a partir de `ES-LATAM\IMAGENS\01 AD - ES.jpg`, com a mesma animação do original: 1º quadro completo, depois os itens 2 e 3 e em seguida os 4 e 5 entram com wipe.
- Faixa de áudio **silenciosa** adicionada.
- Selo "PAGO CONTRA ENTREGA" no canto superior esquerdo.
- O botão do rodapé virou "Haz clic en / Más información", com duas setas pequenas apontando para ele a partir de 1,0 s.
- **Revisão:** 2 "problemas", ambos esperados pelo briefing: a resolução e o silêncio (o vídeo não tem som).

## Textos dos anúncios
- Arquivo: `ES-LATAM\00-TEXTOS-ANUNCIOS-H2O-X5-ES.txt` (UTF-8). Cobre os 27 criativos.
- Para cada um: título (≤40, conferido por script), texto principal, descrição, botão "Más información" e versão TikTok (≤100, conferida).
- Varredura automática sem: FBX5, USA, UK, Canada, EE. UU., Reino Unido, Shop now, código, cuotas, envío desde/gratis, hoy, links e 5lbs/1 año.
- "Pago contra entrega" está em todos.

## Pendências e revisão manual
1. **Link de destino** da loja COD por país: o arquivo de textos tem um marcador de pendência.
2. **Garantia:** os textos usam "2 años" (ficha), mas a imagem 45 traduzida diz "1 AÑO DE GARANTÍA GRATIS" e "ENVÍO GRATIS". A imagem precisa de ajuste ou de confirmação.
3. **"Vendidas" × "vendidos":** o 08 usa "14 millones vendidas" (briefing). A imagem 01 e o 44 usam "VENDIDOS" (arte das imagens). Escolher um padrão.
4. **"$55":** confirmar se é USD ou moeda local em cada país.
5. **08:**
   - mopa **vermelha** em 17,0–18,9 s (mantida, como decidido);
   - logo "THANE" no início e no fim (fabricante, mantido).
6. **17:** a letra da música é em inglês (mantida por decisão da dona).
7. **Selo "¡PAGAS AL RECIBIR!":** a fita vermelha segue o padrão do kit. Tire se quiser só "Pago contra entrega".
8. **Formatos 1:1 e 4:5:** o `revisar_ad.py` marca a resolução como problema porque só aceita 9:16. É limitação da ferramenta.
