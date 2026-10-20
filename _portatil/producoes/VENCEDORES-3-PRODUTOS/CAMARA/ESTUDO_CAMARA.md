# Estudo CÁMARA: câmera de segurança 4G com painel solar (COD Chile), 15/10/2026

Estudo sem custo e sem geração de mídia. Ferramentas: faster-whisper large-v3 (GPU, es, tempo por palavra), RapidOCR a 2 quadros/s (rodado depois do whisper), folhas de contato a 1 quadro/s e de 0–3 s a 4 quadros/s. Os vídeos originais não foram alterados.

**Arquivos de apoio nesta pasta** (prefixo `_`):
- `_<id>_transcricao.txt` / `.json` (tempos por palavra)
- `_<id>_ocr.txt`
- `_<id>_folha_1fps.jpg` e `_<id>_folha_0-3s_4fps.jpg`

**Apelidos usados neste estudo:**
| Apelido | Arquivo | Duração | Modelo que aparece |
|---|---|---|---|
| **V1** | `CAMARA_122120476155415302.mp4` | 57,4 s | A (preta) |
| **V2** | `CAMARA_122120866641415302.mp4` | 36,9 s | C (dupla lente, branca) |
| **V3** | `CAMARA_122120866821415302.mp4` | 58,8 s | C (dupla lente, branca) |
| **V4** | `CAMARA_122139509325352607.mp4` | 92,7 s | C (dupla lente, branca, logo «AOC») |
| **V5** | `CAMARA_122139971595352607.mp4` | 41,6 s | B (branca, lente única) |

> **Não é o produto Wyze** do lote de 05/10 (`WYZ-CAMARA-LATAM`). A Wyze Solar Cam Pan funciona por wifi. Aqui o argumento central é **4G, sem wifi e sem energia elétrica**, e não aparece nenhuma marca Wyze. É outro produto.
>
> Observação: a `lista.txt` tem 6 links CAMARA, mas só 5 vídeos estão na pasta. O 6º (`122145821439352607`) é o vídeo da podadora, como o ESTUDO_CESPED já apontou.

---

## 1. O produto (só o que aparece nos vídeos)

### ⚠️ Os vencedores mostram 3 câmeras diferentes
| Modelo | Onde | Como é |
|---|---|---|
| **A: preta, lente única** | V1 | Domo PTZ preto com 2 antenas e painel solar separado, num suporte. A caixa traz **2 câmeras** (V1 0,75–2,5 s) e a mesa final mostra 2 câmeras + 2 painéis (V1 54–57 s). Caixa: «4G LTE Pan Tilt Security Camera · Battery/Solar Powered · 4G LTE Network, No Wi‑Fi Needed» |
| **B: branca, lente única** | V5 | Domo PTZ branco com 2 antenas, painel separado e suporte de parede. No chão, 2 câmeras + 2 painéis + cabos + parafusos (V5 38–41 s) |
| **C: dupla lente, branca e preta** | V2, V3, V4 | Lente fixa em cima e domo PTZ preto embaixo, com painel solar «telhado» por cima e 2 antenas. Em V4 aparece o logo **«AOC»** na câmera. O domo de baixo do V3 tem uma janela larga, diferente do V4: podem ser 2 versões |

**Isso é decisivo para o lote:** num COD, mostrar um modelo e entregar outro gera recusa na entrega. Cada criativo só pode usar takes do modelo que a pessoa vende (ver §4 e as perguntas da §7).

### O que os vídeos dizem (sem conferir com ficha técnica)
| Atributo | Fala / tela | Fonte |
|---|---|---|
| Sem wifi e sem eletricidade | «no necesita Wi‑Fi ni Internet», «trabaja con pura señal 4G», tela «TRABAJA SIN WI‑FI Y SIN ENERGÍA ELÉCTRICA» | todos |
| 4G / chip | «funciona con 4G LTE»; «ya viene con su SIM card incorporada y trae internet… solo se pagan de 11 a 12 dólares el mes» | V1 48 s; **V4 52–59 s** |
| Solar | «viene con panel solar para que se cargue sola», «se carga con el sol» | V1, V2, V5 |
| Giro | «gira 360 grados»; «4 cámaras al precio de una» porque gira | V1, V2, V4, V5 |
| Imagem | «graba en 2K HD» | V1, V2 |
| Noite | «visión nocturna», «visión a color», «linterna», «tiene luces» | V1, V2, V3, V4; tomadas noturnas em V1 36–45 e V5 25–29 |
| Alerta | «sensor de movimiento», «te manda alerta al celular», «notificaciones al instante» | V1, V3, V5; app com retângulo verde de detecção em V1 33–35/42–45 e V5 21–24 |
| Áudio | «micrófono de doble vía», «hacer una conversación mediante ella», «sirena» | V3, V5 |
| Dupla lente (modelo C) | «tiene dos lentes… no va a tener punto ciego», «dos cámaras en uno» | V3 44–52 s, V4 |
| Clima | «a prueba de agua», «impermeable, contra el agua, la nieve, polvo»; teste com mangueira em V1 19–23 s | V1, V2, V4 |
| Ver de longe | «ver desde Estados Unidos», «desde cualquier parte del mundo», «mandarlo a tu país» | V1, V3, V5 |
| App | No V4 ele diz «yo si yo» (provável **Yoosee**). Nas telas de V1/V5 aparecem «Garage», «Activity Playback», «PTZ», «Intercom», «Cloud Service» | V4 58–76 s; V1, V5 |
| Assinatura | «no tienes que pagar membresía sobre almacenamiento» (V3) **×** «11 a 12 dólares el mes» do chip (V4) | conflito |
| Camuflagem | «estilo camuflaje tipo espía», «diseño camuflado la hace indetectable» | V1 31 s, V5 25 s. **As imagens mostram uma câmera branca/preta comum**, nada camuflado |

Nada sobre este produto foi encontrado no disco além destes vídeos, e `07-notion-sync/` não existe. Tudo acima vem **só das falas** e precisa de confirmação antes de ir para um roteiro (§7).

---

## 2. Linha do tempo

### V1: «Esta cámara no necesita Wi‑Fi ni Internet» (narração + B-roll de fazenda)
- Narração masculina com sotaque mexicano («ahorita», «rancho», «no ocupa»).
- Sem legenda. Balão branco de 0 a 4,5 s. Ícone branco pequeno de câmera **no canto inferior direito o vídeo todo**. Setas vermelhas de 50 a 57 s.
- O cenário (galinheiro americano, galinhas, celeiro vermelho) tem **aparência de vídeo gerado por IA**; as telas do app são gravações reais. Precisa de confirmação.

| Tempo | Fala | Tela / cena |
|---|---|---|
| 0–4,5 | «Esta cámara no necesita Wi‑Fi ni Internet, así que la puedes instalar en tu rancho, en la montaña…» | Balão «Cámara no necesita corriente, ni wifi trae su panel solar.» Unboxing: caixa no colo, 2 câmeras pretas |
| 3–5 | | Close da câmera na mão |
| 5–9 | «…y aún así ver desde Estados Unidos exactamente qué está pasando en tu casa» | Furadeira fixando o suporte; homem de boné instalando no galinheiro |
| 9–14 | «graba en 2K HD, gira 360…» | Celular na horizontal com a imagem ao vivo do galinheiro (carimbo de data no vídeo do celular) |
| 14–18 | «…visión nocturna, sensor de movimiento…» | Câmera instalada, galinhas |
| 19–23 | «…a prueba de agua y viene con panel solar…» | Mão limpa o barro do painel; **jato de mangueira na câmera** |
| 24–28 | «Todo lo controlas desde la app…» | Dedo aponta a câmera e o painel; close |
| 29–32 | «…te manda alerta al celular» | iPhone com a lista de eventos «Activity detected» |
| 33–35 | «si llega el vecino chismoso o alguien que no debería estar ahí…» | Tela do app: **carro detectado** com retângulo verde |
| 36–41 | «…estilo camuflaje tipo espía…» / «más de 44,000 ventas y 4 estrellas» | **Noite**: câmera com LEDs acesos sobre o galinheiro |
| 42–45 | «ahorita está a más de mitad de precio…» | App noturno infravermelho: guaxinim detectado |
| 46–53 | «…como tener un guardia privado… 24 horas» / «funciona con 4G LTE» | Câmera numa árvore; galinhas; closes com dedo (seta vermelha de 50 s em diante) |
| 54–57 | «Sígueme para más productos que hagan tu vida más fácil» | Mesa com o kit (2 câmeras, 2 painéis, cabo, parafusos) |

### V2: «Se los dije que iba a bajar de precio» (talking head)
- Criador homem latino segurando o modelo C diante de uma porta branca.
- Legenda queimada palavra a palavra, branca em caixa-alta, a y≈984. Fala corrida de 26 s, sem cortes de cena.
- 0–26 s: lista de atributos (doble lente, «la de cuatro», sem luz nem wifi, 360, 2K, visión nocturna, video récord, painel, impermeável, «agua, la nieve, polvo», casa de campo/finca/granja), «¡mira qué bonita!», «viene con una súper oferta».
- 26–36,5 s: «te voy a dejar el enlace arribita de mi nombre, donde dice tienda. Corre porque se están agotando».

### V3: «la cámara que le llaman el ojo de Dios» (B-roll + narração)
- 58,8 s **só de takes reais do modelo C** no beiral de uma casa (estuque bege, porta de garagem, rua com carros). Não há rosto nem texto na tela: o OCR só achou ruído.
- Narração corrida: «ojo de Dios, no se le escapa ningún movimiento», sem wifi nem eletricidade, «no tienes que pagar membresía», 4G, «instalar en tu rancho, en la entrada o mandarlo a tu país para monitorear tu familia», micro de duas vias, sirene, lanterna, visão a cor, «esta semana la bajaron de precio», «dos lentes, no va a tener punto ciego», «carrito naranja».
- 0–13 s: o domo PTZ **girando** em close, a melhor prova do 360. 14–58 s: ângulos variados, de perto, de baixo, com céu e rua ao fundo, e LEDs acesos (47–49 s).

### V4: «Esta es la cámara, mi gente» (criador no carro, 92 s)
- Criador latino no banco do carro, com o modelo C («AOC») colado ao rosto o vídeo todo.
- Faixa vermelha fixa no topo: «TRABAJA SIN WI‑FI Y SIN ENERGÍA ELÉCTRICA».
- 0–29 s: sem luz nem wifi, «compatible con cualquier teléfono», «estoy en el carro… no tengo ningún cable». **19–31 s:** celular com a imagem ao vivo.
- 29–52 s: «gira 360, detecta movimientos, tiene luces, vienen dos cámaras en uno… es una cámara movible».
- **52–59 s:** «ya viene con su SIM card incorporada y trae internet, y solo se pagan de 11 a 12 dólares el mes».
- 59–92 s: «graba 24/7 aunque tiemble la tierra, aunque se vaya la luz»; app «Yoosee» (72–76 s: lista de apps no celular, com marcas de terceiros); «contra agua», cupom de desconto.

### V5: «¿Cuatro cámaras por el precio de una?» (fazendeiro + B-roll)
- Narração masculina, ritmo de anúncio. Balão de 0 a 5,5 s. Setas vermelhas de 34 a 41 s.
- Fazendeiro americano de boné fala para a câmera diante de 4 câmeras numa parede metálica (0–5,5 s). O resto é B-roll de fazenda; **pode ser IA** (aparência parecida com o V1, e as mesmas telas de app «Garage»).

| Tempo | Fala | Cena |
|---|---|---|
| 0–5 | «¿4 cámaras de seguridad a precio de una? ¡Sí! Como esta cámara gira a 360 grados…» | Fazendeiro (rosto) + 4 câmeras na parede |
| 6–10 | «…ver todos los espacios de tu rancho sin necesidad de tener varias cámaras» | Câmera no poste; estrada de terra da fazenda |
| 11–14 | «…no necesita wifi ni electricidad» | Furadeira no suporte; homem na escada instalando (rosto) |
| 15–18 | «trabaja con pura señal 4G y se carga con el sol» | Close do painel; close da câmera |
| 19–24 | «las puedes ver en vivo desde tu teléfono… te avisa con notificaciones» | Celular com imagem ao vivo (tratores); app com **pessoa detectada** no estábulo à noite |
| 25–29 | «…hacer una conversación mediante ella / diseño camuflado» | **Noite**: LEDs acendendo |
| 30–33 | «por eso se están vendiendo como locas» | iPhone com a lista de eventos |
| 34–41 | «haz clic en el carrito naranja… doble descuento… envío súper rápido ¡Corre!» | Câmera de dia (setas); kit no chão (2 câmeras + 2 painéis) |

---

## 3. Raio-x (placar da `completar-criativo`, 0–2)

| | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| A. Quebra de transe | 1: unboxing + balão, sem conflito | 1: rosto + produto na mão, «se los dije» | 1: close do domo girando (bonito, mas sem tensão) | 1: rosto no carro, faixa vermelha | **2**: pergunta-promessa «¿4 cámaras por el precio de una?» + 4 câmeras visíveis |
| B. Segmentação | 1: «rancho, montaña, donde no llega señal» | 1: «casa de campo, finca, granja» | **2**: «rancho» e «mandarlo a tu país para monitorear tu familia» | 1: «mi gente» | 1: «tu rancho» |
| C. Tipo de gancho | Filtro (lugar sem sinal) | Origem validada (estilo TikTok Shop «se los dije») | Apelido «ojo de Dios» (curiosidade) | Contraintuitivo: sem luz e sem wifi | Contraintuitivo + promessa |
| D. Dor | 1–2: «vecino chismoso o alguien que no debería estar ahí» | 0: só atributos | 3: ver a família à distância | 1 | 1: «proteger tu propiedad» |
| E. 4 blocos | 1: mecanismo bom, CTA «sígueme» fraco | 1: lista + CTA de link | 1: lista longa, CTA no meio e no fim | 0–1: 92 s repetitivos | **2**: gancho → mecanismo → prova no app → CTA com urgência |
| F. Execução | **2**: troca de plano a cada 1–3 s, prova em tudo (instalação, mangueira, app, noite, kit) | 1: plano único | 1: só um cenário | 0–1: plano único, 92 s | **2**: ritmo, app, noite, kit |

**Por que vendem (o padrão comum):**
1. **A frase-mecanismo «sin wifi y sin luz»** está nos 5, sempre nos primeiros 8 s. É a quebra de crença: «câmera precisa de tomada e internet». Sustenta o vídeo sozinha.
2. **Lugar onde a câmera comum não chega:** rancho, campo, granja. Para o Chile, o equivalente é parcela, campo, casa de veraneio, obra e almacén.
3. **Prova no celular:** ver ao vivo + alerta com retângulo verde. É o «depois» do produto.
4. **Noite com LEDs** e **instalação sem fio** (furadeira + suporte) mostram que é simples.
5. **O 360 vendido como «4 em 1»** (V5) é o melhor gancho de valor sem preço.

**O que falta em todos:**
- Nenhum tem **cena de situação** (ladrão, cachorro, visita): a dor fica abstrata («proteger tu propiedad»).
- Elenco e sotaque são **mexicanos/centro-americanos nos EUA** («ahorita», «carrito naranja», «dólares», «Estados Unidos»), nada chileno.
- Nenhum fala **pagas al recibir**. As urgências («mitad de precio», «doble descuento», «se están agotando») são de TikTok Shop dos EUA.

---

## 4. Banco de takes reais (custo zero)

**Regra de uso:** só o modelo vendido. Os rostos de criadores (V2, V4, V5 0–5,5 s) e o homem instalando (V1 7–9, V5 13–14) **não entram**, porque são rostos de terceiros.

### Modelo A: preta (V1)
| Slot | Intervalo | O que mostra | Texto/marca queimados |
|---|---|---|---|
| A-UNBOX | 0,0–3,0 | Caixa aberta no colo, 2 câmeras | **Balão 0–4,5 s** + ícone no canto inferior direito |
| A-CLOSE | 3,0–5,0 | Câmera na mão, close | Balão + ícone |
| A-INSTAL | 5,0–7,0 | Furadeira fixando o suporte (só mão) | ícone |
| A-VIVO | 9,0–14,0 | Celular na horizontal com a imagem ao vivo | carimbo de data no vídeo do celular + ícone |
| A-INSTALADA | 14,0–18,0 | Câmera instalada, galinhas | ícone |
| A-AGUA | 19,0–23,5 | Limpa barro do painel + **jato de mangueira** | ícone |
| A-DEDO | 24,0–28,5 | Dedo aponta a câmera e o painel | ícone |
| A-EVENTOS | 29,0–32,5 | iPhone com a lista «Activity detected» | ícone (texto do app em inglês) |
| A-DETECTA-AUTO | 32,5–35,5 | Tela do app: carro detectado (retângulo verde) | idem |
| A-NOCHE | 36,0–41,5 | Câmera de noite com LEDs acesos | ícone |
| A-NOCHE-APP | 41,5–45,5 | App infravermelho: animal (guaxinim) detectado | idem. O guaxinim não existe no Chile |
| A-ARBOL | 46,0–49,5 | Câmera numa árvore; galinhas | ícone |
| A-CLOSES | 50,0–54,0 | Closes com dedo | **setas vermelhas 50–57 s** |
| A-KIT | 54,0–57,4 | Mesa com o kit | setas |

O **ícone no canto inferior direito** precisa de LaMa local ou de recorte. O balão do início e as setas do fim, idem.

### Modelo B: branca, lente única (V5)
| Slot | Intervalo | O que mostra | Texto/marca queimados |
|---|---|---|---|
| B-4CAM | 0,0–5,5 | 4 câmeras numa parede | **rosto do fazendeiro + balão**: só serve com recorte acima da cabeça |
| B-POSTE | 6,0–10,0 | Câmera no poste; estrada da fazenda | limpo |
| B-INSTAL | 11,0–12,8 | Furadeira no suporte | limpo |
| B-SOLAR | 15,0–17,9 | Close do painel | limpo |
| B-CLOSE | 18,0–19,0 | Close da câmera | limpo |
| B-VIVO | 19,0–21,0 | Celular com imagem ao vivo | limpo |
| B-DETECTA | 21,0–24,5 | App: pessoa detectada no estábulo à noite | texto do app em inglês |
| B-NOCHE | 25,0–30,0 | LEDs acendendo à noite | limpo |
| B-EVENTOS | 30,0–34,0 | iPhone com a lista de eventos | texto do app |
| B-DIA | 34,0–38,0 | Câmera de dia, céu nublado | **setas 34–41 s** |
| B-KIT | 38,0–41,6 | Kit no chão (2 câmeras + 2 painéis + cabos) | setas |

### Modelo C: dupla lente (V3 limpo; V2 e V4 só em recorte)
| Slot | Intervalo | O que mostra | Texto/marca queimados |
|---|---|---|---|
| C-GIRO | V3 0,0–13,5 | **Domo girando** em close (prova do 360) | limpo |
| C-ABERTA | V3 14,0–18,5 | Câmera no beiral, plano aberto | limpo |
| C-BAIXO | V3 19,0–24,5 | De baixo, céu e rua com carros | limpo (rua com carros de terceiros, sem placa legível nas folhas) |
| C-VARIOS | V3 25,0–46,5 | Ângulos variados no beiral | limpo |
| C-LEDS | V3 47,0–49,5 | Close com os LEDs | limpo |
| C-FINAL | V3 50,0–58,8 | Ângulos diversos | limpo |
| C-VIVO | V4 19,0–31,0 | Celular com a imagem ao vivo | **rosto do criador + faixa vermelha**: recorte só do celular; qualidade baixa |
| C-MANO | V2 0–36 | Câmera na mão | rosto + legenda: não usar |

**Lacunas do modelo C:** não há take real de instalação, noite, app/alerta nem kit. Se o vendido for o C, esses blocos precisam de filmagem nova da pessoa ou de IA (imagem com referência do produto), com o risco de deformar o domo duplo.

---

## 5. Os 10 conceitos (estilo das personas dos perfumes)

### Estrutura comum (~30–35 s, ~27 mil créditos do ElevenLabs por produção)
| Bloco | Tempo | O que é | Origem |
|---|---|---|---|
| 1. Gancho | 0–4 s | A situação cômica + 1 fala + título na tela | **IA**: imagem + Seedance 2 com fala (~9,2 mil) |
| 2. Ele/ela se apresenta | 4–9 s | Selfie, 1 frase engraçada | **IA**: imagem + Seedance 2 com fala (~9,2 mil) |
| 3. Mecanismo | 9–13 s | «No necesita wifi ni enchufe…» | **Real**: GIRO/CLOSE/SOLAR + narração TTS |
| 4. Dia | 13–19 s | A situação vista pela câmera + alerta no celular | **IA**: Kling sem fala, estilo câmera de segurança (~2,1 mil) + **real** VIVO/EVENTOS + TTS |
| 5. Noite | 19–25 s | A situação à noite + LEDs | **IA**: Kling sem fala (~2,1 mil) + **real** NOCHE/DETECTA + TTS |
| 6. Instalação | 25–29 s | «La pones donde quieras, sin cables» | **Real**: INSTAL + ABERTA/POSTE + TTS |
| 7. CTA | 29–34 s | Persona com a câmera instalada atrás | **IA**: só imagem com zoom lento + KIT real + TTS + setas |

Créditos: ~7 imagens (~4 mil) + 2 Seedance (~18,4 mil) + 2 Kling (~4,2 mil) + TTS/trilha ≈ **27 mil por produção**, **~270 mil no total dos 10**. São os números do briefing dos perfumes; não foram medidos para este produto.

**Narração comum** (voz do personagem; só a piada final de cada bloco muda). Os atributos vêm dos vencedores e precisam de confirmação (§7):
- Mecanismo: «No necesita wifi ni enchufe: funciona con señal 4G y se carga sola con el sol.»
- Dia: «Gira en 360 y la veo en vivo desde el celular, esté donde esté. *[piada]*»
- Noite: «De noche ve igual, y si alguien se acerca me llega la alerta al tiro. *[piada]*»
- Instalação: «La pones en el techo, en la reja o en un poste. Sin cables.»
- CTA: «Te llega a la casa y pagas cuando la recibes. ¡Pídela ahora!»

**Regras do lote** (iguais às dos perfumes + do produto):
- Chileno ou chilena comum, nada bonito, pode ser caricato.
- Uma voz por personagem.
- Sem porta abrindo e sem ninguém entrando ou saindo de veículo.
- **A câmera nunca é gerada em movimento pela IA.** Nas cenas de IA ela fica de fora, ou só como imagem parada com referência do produto (CTA). Giro, LEDs, instalação e app vêm sempre de take real.
- **Telas de celular nunca são geradas por IA.** Elas vêm dos takes reais (VIVO, EVENTOS, DETECTA).
- Cenas «vistas pela câmera»: plano alto, grande-angular, personagem com ~25% da altura e a ação legível no 1º quadro. O carimbo REC/data entra na edição, não na IA.

---

### C1 · LA VECINA COPUCHENTA
**Ele:** don Hernán, 61 anos, jubilado, careca com bigode, chaleco de lã, chinelos. Casa de pasaje com pandereta.
- **Gancho:** a vizinha de rolos e bata se debruça sobre a pandereta e aponta a câmera. Fala: «¡Don Hernán! ¿Y esa cámara? ¿Me está grabando a mí?» · Tela: **LA VECINA YA NO SE ASOMA 😂**
- **Selfie:** no pátio. «Soy jubilado… y ahora el que sabe todo lo que pasa en mi patio soy yo.»
- **Mecanismo:** GIRO / CLOSE + TTS.
- **Dia:** Kling «câmera de segurança» mostrando o próprio pátio dele com a vizinha espiando por cima do muro, e ela some. Real: VIVO + EVENTOS. Piada: «La copuchenta ahora saluda a la cámara.»
- **Noite:** Kling do gato da vizinha passeando no telhado dele. Real: NOCHE. Piada: «Hasta el gato de ella sale en la tele.»
- **Instalação:** INSTAL + ABERTA.
- **CTA:** don Hernán de braços cruzados, satisfeito, com a câmera no beiral atrás.

### C2 · EL LANZA DE LAS ENCOMIENDAS
**Ela:** Daniela, 34 anos, compra tudo online, moletom e coque desarrumado.
- **Gancho:** na reja, segurando uma caixa vazia rasgada. Fala: «Me robaron la encomienda tres veces… a la cuarta, lo pillé en vivo.» · Tela: **A LA CUARTA LO PILLÉ 📦**
- **Selfie:** no sofá, com o celular. «Compro todo por internet… y el lanza del barrio también lo sabía.»
- **Mecanismo:** CLOSE + SOLAR + TTS.
- **Dia:** Kling «câmera» com um repartidor genérico (sem logo) deixando a caixa e um tipo de capuz se aproximando, que se assusta com a luz e sai correndo (sem veículo). Real: DETECTA + VIVO. Piada: «Le hablé por la cámara y salió arrancando.»
- **Noite:** Kling com a caixa no portão e a luz acesa. Real: NOCHE. Piada: «Ahora mis paquetes duermen tranquilos.»
- **Instalação:** INSTAL + ABERTA.
- **CTA:** Daniela abraçando a caixa, com a câmera no beiral atrás.

> A fala «le hablé por la cámara» só entra se o áudio de duas vias for confirmado. Se não for, a piada vira «salió arrancando con la luz».

### C3 · EL CHOCOLO QUE SE ARRANCA
**Ele:** don Jaime, 47 anos, gordinho, camiseta do Colo‑Colo e boné, com o quiltro caramelo «Chocolo».
- **Gancho:** no pátio, com a coleira vazia na mão. Fala: «¿Saben cuántas veces se me arrancó el Chocolo este año? Once.» · Tela: **EL CHOCOLO SE ARRANCA… Y YO LO VEO 🐶**
- **Selfie:** com o cachorro no colo. «Este perro es un artista del escape… pero ahora lo tengo cachado.»
- **Mecanismo:** GIRO + TTS.
- **Dia:** Kling «câmera» com o Chocolo cavando debaixo da reja. Real: VIVO + EVENTOS. Piada: «Me llegó la alerta antes de que terminara el hoyo.»
- **Noite:** Kling com o Chocolo voltando de madrugada pela reja, culpado. Real: NOCHE. Piada: «Ahora sé que va a ver a la perrita del pasaje.»
- **Instalação:** INSTAL + POSTE/ABERTA.
- **CTA:** Jaime e o Chocolo no pátio, com a câmera atrás.

### C4 · LA SUEGRA SORPRESA
**Ele:** Cristián, 38 anos, magro, bigode ralo, pijama do Chavo.
- **Gancho:** no sofá, de pijama, olhando o celular em pânico. Fala: «¡Amor! ¡Escóndete, viene tu mamá por el pasaje!» · Tela: **AHORA LA VEO VENIR 👀**
- **Selfie:** no pátio. «Mi suegra llega sin avisar… pero ahora yo me entero primero.»
- **Mecanismo:** CLOSE + SOLAR + TTS.
- **Dia:** Kling «câmera» com a sogra caminhando pelo pasaje com bolsas e um tupper, a caminho da reja (sem porta abrindo). Real: VIVO. Piada: «Me da tiempo de ponerme pantalones.»
- **Noite:** Kling com a sogra de novo, de noite, com outro tupper. Real: NOCHE. Piada: «Y de noche igual… pero trae cazuela.»
- **Instalação:** INSTAL + ABERTA.
- **CTA:** Cristián, vestido e sorrindo, com a câmera atrás.

### C5 · EL UNIVERSITARIO TRASNOCHADO
**Ela:** Carolina, 46 anos, mãe, de bata e rolos, com o filho Benja, 19 anos (universitário, **maior de idade**).
- **Gancho:** na cozinha, às 3 da manhã, com o celular na mão. Fala: «Benjamín, dijiste que llegabas a las doce… la cámara dice otra cosa.» · Tela: **MAMÁ 1 – BENJA 0 😂**
- **Selfie:** de bata. «Tengo un hijo universitario… y ahora tengo pruebas.»
- **Mecanismo:** GIRO + TTS.
- **Dia:** Kling «câmera» com o Benja saindo de mochila e voltando 5 minutos depois para pedir dinheiro. Real: EVENTOS. Piada: «Sale a estudiar… y vuelve a pedir plata.»
- **Noite:** Kling com o Benja pulando a reja na ponta dos pés, de madrugada, e a luz acendendo nele. Real: NOCHE. Piada: «Se le prendió la luz justo en la cara.»
- **Instalação:** INSTAL + ABERTA.
- **CTA:** Carolina e o Benja no pátio; ele de castigo, varrendo.

### C6 · EL MICHI LADRÓN
**Ela:** la señora Paty, 55 anos, baixinha, avental florido, ama de casa de bairro.
- **Gancho:** no pátio, entre vasos de flores quebrados, de vassoura na mão. Fala: «Pensé que me estaban robando las plantas… y era el gato.» · Tela: **EL LADRÓN ERA EL MICHI 🐱**
- **Selfie:** com o gato no colo. «Tres meses culpando al vecino… y el culpable dormía en mi cama.»
- **Mecanismo:** CLOSE + SOLAR + TTS.
- **Dia:** Kling «câmera» com o gato derrubando um vaso da mureta. Real: VIVO. Piada: «Lo vi en vivo… y le grité por el celular.»
- **Noite:** Kling com os olhos do gato brilhando no pátio e outro vaso caindo. Real: NOCHE. Piada: «Hasta de noche lo pillo.»
- **Instalação:** INSTAL + ABERTA.
- **CTA:** Paty e o gato com cara de inocente; câmera atrás.

> Tom de humor puro. Serve de contraponto aos de medo (C2, C7, C8): o ângulo «câmera para cuidar da casa e dos bichos» sem ameaça.

### C7 · DON SEGUNDO Y EL ZORRO (parcela sem luz)
**Ele:** don Segundo, 64 anos, huaso com chupalla, poncho e bigode branco, com galinhas e uma parcela simples.
- **Gancho:** na frente do galinheiro. Fala: «En mi parcela no llega ni la luz… y igual veo mis gallinas desde Santiago.» · Tela: **SIN LUZ NI WIFI 🐔**
- **Selfie:** no galinheiro. «El zorro me tenía la guerra declarada… hasta que puse esto.»
- **Mecanismo:** SOLAR + CLOSE + TTS («No necesita enchufe ni wifi…»).
- **Dia:** Kling «câmera» com as galinhas soltas e o neto correndo atrás delas. Real: VIVO (V1 no galinheiro, se for o modelo A). Piada: «Mi nieto corre más que las gallinas.»
- **Noite:** Kling com um zorro culpeo se aproximando do galinheiro, a luz acende e ele foge. Real: NOCHE. Piada: «El zorro ahora pasa de largo.»
- **Instalação:** INSTAL + POSTE/ARBOL.
- **CTA:** don Segundo apoiado num poste de madeira, com a câmera e o painel no alto.

> É o que está mais perto dos vencedores (rancho/granja → parcela/campo). Se o modelo for o A, os takes do galinheiro do V1 casam com a cena.

### C8 · EL MAESTRO DE LA OBRA
**Ele:** Rigo, 50 anos, maestro «chasquilla», capacete, colete refletivo sujo de cimento e barriga.
- **Gancho:** na obra sem muro, apontando um canto vazio. Fala: «Aquí había una betonera… ahora la obra se cuida sola.» · Tela: **ME ROBARON LA BETONERA 🏗️**
- **Selfie:** entre tijolos. «En la obra no hay luz ni internet… y esta cámara no los necesita.»
- **Mecanismo:** SOLAR + GIRO + TTS.
- **Dia:** Kling «câmera» com os pedreiros na hora do almoço, dormindo sobre os sacos de cimento. Real: VIVO. Piada: «Ahora sé por qué la obra va tan lenta.»
- **Noite:** Kling com uma figura de capuz se aproximando dos materiais; a luz acende e ela foge. Real: NOCHE + DETECTA. Piada: «Esta vez la betonera se quedó.»
- **Instalação:** INSTAL + POSTE.
- **CTA:** Rigo na obra com a câmera num poste e o painel ao sol.

### C9 · EL MINERO DE TURNO
**Ele:** Luis, 45 anos, mineiro em turno 7×7 no norte, macacão laranja, capacete com lanterna, bronzeado de deserto.
- **Gancho:** no acampamento, à noite, olhando o celular e rindo. Fala: «Trabajo a mil quinientos kilómetros… y veo mi casa en vivo.» · Tela: **7 DÍAS LEJOS, TRANQUILO ⛏️**
- **Selfie:** na faena. «Trabajo siete por siete… y ahora no me pierdo nada de lo que pasa en mi casa.»
- **Mecanismo:** CLOSE + SOLAR + TTS.
- **Dia:** Kling «câmera» com a filha chegando do colégio e acenando para a câmera. Real: VIVO + EVENTOS. Piada: «Mi hija me saluda por la cámara todos los días.»
- **Noite:** Kling com o pátio tranquilo e o cachorro deitado sob a luz. Real: NOCHE. Piada: «Y el perro… durmiendo en mi sillón. Lo vi.»
- **Instalação:** INSTAL + ABERTA.
- **CTA:** Luis de volta em casa, de capacete na mão, com a câmera atrás.

> É a dor mais funda do lote (estar longe da família, nível 3). Vem do «mandarlo a tu país para monitorear tu familia» do V3, adaptado ao Chile.

### C10 · EL ALMACENERO Y LAS 4 CÁMARAS
**Ele:** don Washington, 58 anos, dono de almacén de bairro, avental azul, lápis atrás da orelha, óculos na ponta do nariz.
- **Gancho:** atrás do balcão, com um orçamento enorme na mão. Fala: «Me cobraban por instalar cuatro cámaras… y puse una sola que gira.» · Tela: **4 CÁMARAS EN 1 🔄**
- **Selfie:** na porta do almacén. «Treinta años en el almacén… y nunca había visto todo el frente de una.»
- **Mecanismo:** **GIRO** (o 360 é o protagonista) + B-4CAM recortado, se for o modelo B + TTS.
- **Dia:** Kling «câmera» com as vecinas fazendo fila e um menino roubando um doce da vitrine de fora. Real: VIVO. Piada: «Ahora sé quién se lleva los dulces.»
- **Noite:** Kling com o almacén fechado de noite e a luz acesa. Real: NOCHE. Piada: «Y en la noche, el almacén tiene guardia.»
- **Instalação:** INSTAL + ABERTA.
- **CTA:** don Washington atrás do balcão, com a câmera visível na fachada.

> É o gancho de valor do V5 («4 cámaras por el precio de una»), sem falar preço.

### Resumo de custo e diversidade
| | Por produção | 10 produções |
|---|---|---|
| Créditos do ElevenLabs | ~27 mil | ~270 mil |
| Tempo (referência dos perfumes) | ~1–1,5 h | ~2,5–3,5 h em 2 ondas paralelas (5 + 5) |

**Famílias (Andromeda):**
1. Humor doméstico: C1, C3, C4, C5, C6.
2. Medo/proteção: C2, C8.
3. Lugar sem luz nem wifi: C7, C8.
4. Distância/família: C9.
5. Valor 360: C10.

Os 10 ganchos abrem com cenas, pessoas e idades diferentes. **Corpo comum** (mecanismo, instalação e CTA iguais): para o Meta não juntar tudo, os blocos 3 e 6 alternam takes diferentes do banco em cada produção.

**Opção mais barata, lado a lado (sem selfie Seedance):** gancho Seedance + 2 Kling + takes reais + TTS ≈ **~18 mil créditos** por vídeo. Perde a apresentação do personagem e encurta o vídeo para ~25 s.

---

## 6. Compliance (a pessoa decide manter ou suavizar; nada foi suavizado)

| # | Ponto | Onde | Risco |
|---|---|---|---|
| 1 | **«No necesita internet / wifi»** | todos | Ela usa **dados 4G** (V4: chip + «11 a 12 dólares el mes»). Se o cliente chileno precisar comprar um chip com plano, «sin internet» vira propaganda enganosa e motivo de recusa ou devolução no COD. Proposta: «sin wifi ni enchufe, funciona con chip 4G». Manter ou trocar? |
| 2 | «No tienes que pagar membresía» (V3) × plano mensal (V4) | V3, V4 | Contradição. Só usar com confirmação |
| 3 | «Camuflaje tipo espía», «indetectable» | V1, V5 | Não é verdade nas imagens (câmera branca comum) e soa como vigilância oculta. A Meta restringe «spy cam». Manter? |
| 4 | Gravar o **vizinho** (C1 e o «vecino chismoso» do V1) | C1, V1 | Privacidade: gravar a propriedade alheia. No C1 a câmera mostra o **próprio pátio** e a vizinha só se debruça no muro. Manter o tom ou suavizar? |
| 5 | Cenas «de câmera de segurança» geradas por IA (ladrão, zorro, sogra) | C2–C10 | Encenação apresentada como gravação real, com carimbo REC. Nos perfumes a pessoa aprovou tom ousado sem selo de vídeo fictício. Repetir aqui ou pôr selo «recreación»? |
| 6 | Ladrão e medo do crime (C2, C8) | novos | Medo como gatilho; a Meta aceita em tom leve. Sem armas, violência ou «portonazo». Manter? |
| 7 | Filho de 19 anos pulando a reja (C5) | novo | Personagem maior de idade e humor familiar. Manter? |
| 8 | Specs: 2K, 360°, visão a cor, sirene, áudio de duas vias, impermeável, «graba 24/7 aunque se vaya la luz» | vencedores | Só entram as confirmadas para o modelo vendido |
| 9 | «44,000 ventas y 4 estrellas», «mitad de precio», «doble descuento», «se están agotando» | V1, V5, V2 | Prova social e urgência dos EUA. **Não reutilizar** sem número real e oferta verdadeira |
| 10 | Logo **«AOC»** na câmera (V4) | V4 | Marca de terceiro (AOC é marca de monitores). Se a loja vende sem essa marca, borrar |
| 11 | Ícone no canto (V1), setas e balões queimados | V1, V5 | Remover com LaMa ou recorte nos takes |
| 12 | Animal norte-americano (guaxinim) e textos do app em inglês | V1 42–45 | Inocente, mas soa «gringo». Usar só de relance ou evitar |
| 13 | Takes de fazenda com aparência de IA (V1, V5) | V1, V5 | Se forem IA, vale o mesmo critério do item 5 |

---

## 7. Perguntas para a pessoa (só o que os vídeos não respondem)

1. **Qual modelo você vende?** A (preta, V1), B (branca de lente única, V5) ou C (dupla lente, V2/V3/V4)? É **1 câmera ou kit de 2** (V1 e V5 mostram 2 na caixa)?
2. **4G no Chile:** vem com chip? Precisa de plano de dados (Entel, Movistar, WOM, Claro…)? Tem custo mensal? Grava em microSD sem nuvem paga? Isso define a frase-mecanismo (§6 item 1).
3. **Specs confirmadas do modelo vendido:** 2K? 360°? Visão noturna a cor? Sirene? Áudio de duas vias? Impermeável? Qual app?
4. **Oferta:** só «pagas al recibir» ou também despacho grátis, prazo (24/48 h), garantia, 2×1? Confirmo que vai **sem preço**.
5. **Takes do modelo C:** se for o C, você tem filmagem real de instalação, app, noite e kit? O V3 é o único limpo e não tem nada disso.
6. Os takes de **fazenda do V1 e do V5** podem ser usados? São seus/IA (eles têm cara de IA)?
7. **Compliance:** manter ou suavizar nos itens 1, 3, 4, 5 e 6 da §6.
8. **Volume:** confirma os 10 a ~27 mil créditos cada (~270 mil no total) ou prefere a versão de ~18 mil?
9. Nome do produto e da loja (marca d'água?) e música: trend liberada ou trilha própria?
