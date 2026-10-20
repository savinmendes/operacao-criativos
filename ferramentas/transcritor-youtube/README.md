# Transcritor de vídeos do YouTube

Salva links numa fila e transcreve todos de uma vez. Feito para juntar material
de referência ao longo da semana e processar em lote.

## Como funciona

Para cada vídeo, tenta nesta ordem:

1. **Legenda que o YouTube já tem.** Custa segundos, não baixa vídeo nem usa GPU.
   Prefere legenda feita por pessoa (tem pontuação e acerta nome de produto) e só
   depois a automática. Ordem de idioma: português, espanhol, inglês.
2. **Whisper local na GPU.** Só quando o vídeo não tem legenda nenhuma. Baixa
   apenas a faixa de áudio, transcreve e apaga o arquivo.

Custo zero nos dois caminhos e nada sai da máquina.

## Instalação

Já está tudo instalado nesta máquina. Numa máquina nova:

```bash
pip install yt-dlp requests faster-whisper
pip install nvidia-cublas-cu12 nvidia-cudnn-cu12   # só se tiver GPU NVIDIA
```

Precisa também do **ffmpeg** no PATH (usado para extrair o áudio).

## Comandos

### Salvar links

```bash
python transcritor.py add https://youtu.be/xxxx
python transcritor.py add https://youtu.be/xxxx https://youtu.be/yyyy
```

Aceita playlist e canal inteiro — expande em vídeos sozinho:

```bash
python transcritor.py add "https://www.youtube.com/@umcanal/videos"
python transcritor.py add "https://www.youtube.com/playlist?list=PLxxxx"
```

Em massa, de um arquivo com uma URL por linha (linhas com `#` são ignoradas):

```bash
python transcritor.py add --arquivo links.txt
```

O mesmo vídeo nunca entra duas vezes, mesmo se você colar o link em formatos
diferentes (`youtu.be/xxx` e `youtube.com/watch?v=xxx` são o mesmo item).

### Ver a fila

```bash
python transcritor.py lista
python transcritor.py lista --status pendente
```

### Transcrever

```bash
python transcritor.py rodar                    # tudo que está pendente
python transcritor.py rodar --limite 20        # em lotes
python transcritor.py rodar --motor legenda    # só legenda, nunca usa a GPU
python transcritor.py rodar --motor whisper    # sempre transcreve o áudio
python transcritor.py rodar --repetir-erros    # tenta de novo o que falhou
```

Opções úteis:

| Opção | Para quê |
|---|---|
| `--janela 15` | Blocos de timestamp mais curtos (padrão: 30s) |
| `--modelo small` | Whisper mais rápido e menos preciso (padrão: `large-v3`) |
| `--idioma-whisper pt` | Força português, em vez de deixar detectar |
| `--idiomas pt pt-BR en` | Ordem de preferência da legenda |
| `--dispositivo cpu` | Força CPU (padrão: `auto`, usa GPU e avisa se cair) |
| `--saida pasta/` | Outra pasta de destino |

A fila é salva depois de **cada** vídeo. Se travar no vídeo 80 de 200, é só rodar
de novo: o que já foi transcrito é pulado.

### Limpar

```bash
python transcritor.py limpar     # tira os concluídos da fila
```

Remove só as linhas da fila. As transcrições continuam em `transcricoes/`.

## Saída

Um arquivo `.md` por vídeo em `transcricoes/`, nomeado
`Título do vídeo__VIDEOID.md`. O ID no fim evita colisão quando dois vídeos têm
o mesmo título.

Cada arquivo abre com uma tabela de procedência — canal, duração, data de
publicação, URL, **origem da transcrição** (legenda manual, legenda automática ou
qual modelo do Whisper) e quando foi transcrito. Isso importa: legenda automática
e Whisper erram de formas diferentes, e depois de 200 arquivos você não lembra
qual veio de onde.

Depois vem a transcrição em blocos com timestamp:

```
**[00:00]** primeiro bloco...

**[00:30]** segundo bloco...
```

## Estado da fila

| Status | O que significa |
|---|---|
| `pendente` | Ainda não processado |
| `feito` | Transcrito, caminho do arquivo gravado na fila |
| `erro` | Falhou (o motivo fica registrado no item) |
| `sem-legenda` | Vídeo sem legenda e Whisper não foi usado |

`--repetir-erros` reprocessa `erro` e `sem-legenda`.

## Limitações conhecidas

- **Legenda automática do YouTube vem sem pontuação** e erra nome de produto e
  gíria. Quando a fidelidade importa, use `--motor whisper`.
- **Vídeo privado, restrito por idade ou geobloqueado** falha e é marcado como
  `erro` com o motivo. Não trava o lote.
- **Live em andamento** não transcreve.
- O Whisper pode alucinar frase curta em trecho de silêncio. O filtro de voz
  (VAD) está ligado para reduzir isso, mas não elimina.
- A detecção de idioma do Whisper usa os primeiros segundos. Em vídeo que começa
  com música ou em outro idioma, vale forçar com `--idioma-whisper pt`.

## Testes

```bash
python -m unittest discover -s tests -v
```

Cobrem a lógica pura: extração de ID de vídeo, formatação de timestamp, nome de
arquivo válido no Windows, agrupamento em blocos, parse de json3 e WebVTT, e o
comportamento da fila (deduplicação, persistência, arquivo corrompido). O caminho
de rede e GPU não é testado automaticamente — para validar, rode um vídeo curto
e confira o rótulo do motor na saída.

## Nota sobre a GPU

O `ctranslate2` carrega as bibliotecas CUDA em tempo de execução e, no Windows,
não as encontra sozinho dentro de `site-packages/nvidia/*/bin`. O módulo
`lib/whisper_local.py` registra esses diretórios na importação, tanto por
`os.add_dll_directory` quanto pelo `PATH` — os dois são necessários.

Antes de aceitar a GPU, o carregador roda o modelo em um segundo de silêncio.
Sem esse teste, `WhisperModel(device='cuda')` é construído sem reclamar e só
falha na primeira transcrição de verdade, com o lote já rodando. Se a GPU não
estiver disponível, o programa avisa na tela e segue em CPU, que funciona mas é
bem mais lenta.
