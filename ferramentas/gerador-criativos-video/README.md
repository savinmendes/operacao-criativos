# Gerador de Criativos de Vídeo

Pipeline Python 100% local (linha de comando) para gerar criativos de vídeo
verticais (9:16) para anúncios de tráfego pago, a partir de um roteiro em
JSON. Combina serviços via API REST direta (sem MCP):

- **fal.ai** — gera b-roll (vídeo) e a imagem do avatar a partir de um prompt
  de texto direto, sem nenhuma configuração manual prévia. É o motor de
  geração usado pelo pipeline principal.
- **ElevenLabs** — converte o texto da fala em áudio, usando uma voz clonada.
- **HeyGen** — anima a imagem do avatar com lip-sync a partir do áudio gerado.
- **ffmpeg** — junta todos os clipes num MP4 final.
- **Flora AI** (`lib/flora_client.py`) — client alternativo, já pronto, mas
  **não usado por padrão** no pipeline principal. Rodar uma technique da
  Flora exige montá-la manualmente no canvas em app.flora.ai primeiro (sem
  atalho por API/MCP) — ver seção própria abaixo se quiser usar/retomar isso.

## 1. Instalação

```bash
cd ferramentas/gerador-criativos-video
python -m venv .venv        # opcional, mas recomendado
.venv\Scripts\activate       # Windows (PowerShell: .venv\Scripts\Activate.ps1)
pip install -r requirements.txt
```

Também é preciso ter o **ffmpeg** instalado e disponível no PATH do sistema
(`ffmpeg -version` deve funcionar no terminal). Baixe em
[ffmpeg.org/download.html](https://ffmpeg.org/download.html) caso não tenha.

## 2. Configurar as chaves de API

Copie `.env.example` para `.env`:

```bash
copy .env.example .env
```

E preencha cada chave:

| Variável | Onde conseguir |
|---|---|
| `FAL_KEY` | [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys) — crie uma conta, gere uma API key. |
| `ELEVENLABS_API_KEY` | [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys) |
| `ELEVENLABS_VOICE_ID` | No painel do ElevenLabs, em **Voices**, clique na voz clonada que você quer usar e copie o **Voice ID**. |
| `HEYGEN_API_KEY` | [app.heygen.com/settings/api](https://app.heygen.com/settings/api) |
| `FLORA_API_KEY`/`FLORA_TECHNIQUE_ID_*` *(opcional, só se for usar `lib/flora_client.py`)* | Ver seção "Flora AI" abaixo. |

O arquivo `.env` nunca deve ser commitado (já está no `.gitignore`).

## 3. Editar o roteiro

Edite `roteiro.json` — uma lista de cenas, na ordem em que devem aparecer no
vídeo final. Cada cena é um destes dois tipos:

**B-roll** (vídeo gerado por IA a partir de um prompt):
```json
{ "tipo": "broll", "prompt": "descrição da cena em inglês, estilo cinematográfico...", "duracao": 5 }
```

**Avatar falando** (imagem gerada por IA + fala convertida em áudio + lip-sync):
```json
{ "tipo": "avatar", "imagem_prompt": "descrição do avatar em inglês...", "fala": "texto que o avatar vai falar, em espanhol" }
```

**Avatar com cutaways** (o clássico "avatar fala, corta pro b-roll ilustrando o
que ele tá dizendo, volta pro avatar" — áudio da fala toca contínuo, só o
vídeo alterna): adicione `cutaways` na cena `avatar`, uma lista de janelas de
corte em segundos **relativos ao início da fala daquele avatar**:
```json
{
  "tipo": "avatar",
  "imagem_prompt": "...",
  "fala": "...",
  "cutaways": [
    { "a_partir_segundo": 2.0, "duracao": 3.0, "prompt": "descrição do b-roll em inglês..." },
    { "a_partir_segundo": 8.0, "duracao": 3.0, "prompt": "outro b-roll..." }
  ]
}
```
Cada cutaway gera seu próprio clipe de b-roll (mesmo motor fal.ai usado pelas
cenas `broll` comuns) e é encaixado na janela de tempo indicada. As janelas
não podem se sobrepor, e `a_partir_segundo + duracao` de cada uma não deve
passar da duração real da fala gerada (que só se sabe depois que o TTS roda —
se um cutaway ficar maior que o áudio, ele é simplesmente cortado no fim do
áudio).

O `roteiro.json` incluído já tem um exemplo completo (nicho fé/prosperidade,
em espanhol, com um cutaway) pronto para rodar.

## 4. Rodar o pipeline

```bash
python main.py
```

Opções:
```bash
python main.py --roteiro outro_roteiro.json --aspect-ratio 9:16
```

O terminal mostra o progresso cena a cena. Se uma cena falhar (erro de API,
timeout etc.), o erro é logado e o pipeline **continua** para as próximas
cenas — a cena que falhou simplesmente não entra no vídeo final (fica listada
no resumo, no fim da execução). Ao terminar, o caminho do MP4 final é
impresso e a pasta `output/` é aberta automaticamente.

## 5. Testar sem gastar créditos de API

```bash
python -m pytest tests/test_smoke.py -v
```

Isso só confirma que todos os módulos importam sem erro e que `.env.example`
está completo — não faz nenhuma chamada de API real (não precisa de chaves
preenchidas para passar).

## Estrutura do projeto

```
main.py                    orquestrador do pipeline
config.py                  carrega variáveis de ambiente (.env)
lib/
  retry.py                 requisição HTTP com retry/backoff (rate limit, timeout)
  fal_client.py             geração de vídeo/imagem via fal.ai (motor usado por main.py)
  elevenlabs_client.py      text-to-speech com voz clonada
  heygen_client.py          avatar com lip-sync
  flora_client.py           roda uma technique salva no canvas da Flora AI (alternativa, não usada por padrão)
  ffmpeg_merge.py           baixa assets, normaliza e concatena o MP4 final
roteiro.json                exemplo de roteiro
tests/test_smoke.py         teste de fumaça (import + .env.example)
output/                     onde os clipes/áudios temporários e o MP4 final são salvos
```

## Trocando modelos/prompts

- Modelos do fal.ai: os padrões usados são `fal-ai/bytedance/seedance/v1/pro/text-to-video`
  (vídeo) e `fal-ai/flux-pro/v1.1` (imagem). Para trocar, edite o padrão em
  `lib/fal_client.py` ou passe `model=` nas chamadas. Catálogo completo em
  [fal.ai/models](https://fal.ai/models).
- Prompts de b-roll/avatar/cutaways: edite diretamente `roteiro.json`.
- Voz: troque `ELEVENLABS_VOICE_ID` no `.env`.

## Nota sobre a API da HeyGen

A integração usa o fluxo clássico da HeyGen (upload de asset em
`/v3/assets`, geração em `/v2/video/generate`, status em
`/v1/video_status.get`) — é o fluxo que dá controle preciso a partir de uma
imagem e um áudio prontos. A HeyGen também tem uma API mais nova ("v3 video
agents") para geração autônoma a partir de um prompt de texto, que **não** é
o que este projeto usa. Os endpoints foram conferidos em setembro/2026; como
a documentação da HeyGen muda com frequência, se `lib/heygen_client.py`
começar a falhar, confira a versão atual em
[developers.heygen.com](https://developers.heygen.com/).

## Flora AI (alternativa disponível, não usada por padrão)

`main.py` usa fal.ai por padrão porque a Flora exige um passo manual que o
fal.ai dispensa: ela não tem endpoints fixos de "gerar vídeo"/"gerar imagem" —
ela executa uma **"technique"** (um workflow que você monta e salva
visualmente no canvas em [app.flora.ai](https://app.flora.ai/)). Não existe
atalho por API nem pelo MCP oficial da Flora para criar uma technique — em
ambos os casos só dá pra **rodar** uma technique já existente, a criação é
sempre manual no canvas.

**Problema conhecido**: ao tentar montar uma technique em set/2026, o botão
"Build Technique" travou o canvas da Flora de forma consistente (testado após
reload e vale testar também em aba anônima/projeto novo). Pode ser um bug
pontual da Flora — se for tentar de novo, vale abrir as DevTools (F12 >
Console) no momento do clique pra capturar o erro real, e reportar ao suporte
da Flora se persistir.

Se quiser usar a Flora mesmo assim (depois de resolver o travamento e ter as
techniques prontas):

1. Monte e salve uma technique de texto-para-vídeo (b-roll) e uma de
   texto-para-imagem (avatar) no canvas — pode ser a mesma technique pros dois
   casos.
2. Pegue o `technique_id` (ou slug) de cada uma na página dela em app.flora.ai.
3. Preencha `FLORA_API_KEY`, `FLORA_TECHNIQUE_ID_VIDEO` e
   `FLORA_TECHNIQUE_ID_IMAGEM` no `.env` (ver `.env.example`).
4. Confira o nome do campo de prompt que a technique espera e ajuste
   `FLORA_PROMPT_INPUT_KEY` no `.env` se não for `prompt`.
5. Em `main.py`, troque o import de `fal_client` por `flora_client` e ajuste
   `processar_cena_broll`/`processar_cena_avatar` para chamar
   `flora_client.generate(technique_id, inputs)` no lugar de
   `fal_client.generate_video(...)`/`generate_image(...)` (assinaturas
   documentadas nos docstrings de `lib/flora_client.py`).

`flora_client.generate(technique_id, inputs)` submete a execução
(`POST /techniques/{id}/runs`) e aguarda a conclusão
(`GET /techniques/{id}/runs/{runId}`). Para acompanhar o progresso
manualmente ou tratar múltiplos outputs, use `run_technique(...)` +
`poll_run(...)` separadamente.

## Segurança

- Nunca commite `.env` (já ignorado no `.gitignore`).
- As chaves só são lidas de variáveis de ambiente — nenhuma chave fica
  hardcoded em nenhum arquivo do projeto.
