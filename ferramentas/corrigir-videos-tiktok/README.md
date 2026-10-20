# Corretor de Vídeo — resolução e bitrate em massa

Site local que acha os vídeos recusados pela plataforma por **resolução** ou
**bitrate** e corrige em lote. Os originais nunca são tocados.

## Como rodar

Clique duplo em `abrir-corretor.bat`, ou:

```
python ferramentas/corrigir-videos-tiktok/servidor.py
```

Abre em `http://127.0.0.1:8750/`. Deixe a janela preta aberta enquanto usa —
é ela que faz o trabalho. `Ctrl+C` encerra.

Opções: `servidor.py 9000` troca a porta · `--sem-navegador` não abre a aba.

## O que ele faz

1. Varre a pasta que você indicar e mede cada vídeo com `ffprobe`.
2. Marca quem reprova, e em qual critério.
3. Converte os selecionados com `ffmpeg` para uma subpasta `corrigidos`.
4. **Remede o resultado** e avisa se algum arquivo saiu fora do alvo mesmo
   assim — o código de saída do ffmpeg sozinho não é garantia.

## Os limites, ditos na cara

**Esticar não cria detalhe.** Um 360×640 vira 540×960 e passa a ser aceito, mas
continua com a nitidez de 360×640. **Aumentar bitrate não devolve qualidade
perdida** — o arquivo é reencodado a partir do que sobrou, não do original.

A ferramenta resolve a **recusa**, não a qualidade. Se o material existir em
resolução maior em algum lugar, exportar de lá sempre dá resultado melhor.

**O bitrate de saída é aproximado.** O comando fixa `b:v = minrate = maxrate`,
que é o mais perto de uma garantia que o x264 oferece, mas em clipe curto ele
ainda pode entregar ~15% abaixo do alvo. É por isso que o alvo nunca encosta no
mínimo da plataforma: parte de um piso de 600 kbps e sobe conforme o tamanho do
quadro. Medido na prática, um 360×640 de 193 kbps saiu em 1058 kbps — três vezes
o mínimo exigido.

## Perfis

| Perfil | Lado curto | Lado longo | Bitrate |
|---|---|---|---|
| TikTok Ads | 540 | 960 | 350 kbps |
| Meta Ads | 500 | 500 | — |

Estão em `lib/correcao.py`, no dicionário `PERFIS`. Mudaram os mínimos? É só
editar ali — nada mais no código depende desses números.

A comparação é por **lado curto e lado longo**, não por largura e altura: um
vídeo deitado de 1024×576 cumpre "pelo menos 540×960" tanto quanto um em pé de
576×1024, e tratar largura/altura ao pé da letra reprovaria o deitado sem motivo.

## Segurança

- O original nunca é lido para escrita, e `comando_ffmpeg` recusa saída igual à
  entrada.
- Colisão de nome no destino vira `_2`, `_3`: nada é sobrescrito, nem uma
  correção anterior feita com outro perfil.
- Conversão interrompida tem o arquivo parcial apagado — meio arquivo engana
  mais do que ajuda.
- O servidor escuta só em `127.0.0.1`. Ele lê e escreve arquivos da máquina,
  então não tem por que estar visível na rede.

## Estrutura

```
servidor.py           HTTP + fila de conversão
lib/correcao.py       diagnóstico e plano (lógica pura, testável sem disco)
lib/sonda.py          ffprobe: mede um vídeo de verdade
web/index.html        a interface
tests/                34 testes da lógica
```

A separação entre `correcao` e `sonda` é proposital: toda a sujeira de lidar com
arquivo real (container que não declara bitrate, arquivo corrompido) fica na
sonda, e a decisão fica testável sem precisar de vídeo nenhum.

## Testes

```
python -m unittest discover -s tests
```

Os casos usam resoluções e bitrates medidos em arquivos reais, não inventados.
O teste que mais importa é `TestOResultadoPassaNaPropriaRegra`: pega cada formato
reprovado, aplica o plano, e confere que o resultado passaria.

## Depende de

`ffmpeg` e `ffprobe` no PATH. O servidor confere na partida e recusa subir sem
eles, em vez de falhar vídeo a vídeo depois.
