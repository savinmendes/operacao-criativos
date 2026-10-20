# Instalação do kit no PC (Windows + VS Code + Claude Code)

Faça uma vez. Depois é só abrir a pasta `kit-edicao-criativos` no VS Code e pedir ao Claude
("edite esse vídeo com legenda e setas", "gere 5 imagens base no Flora"...). Ele lê o `CLAUDE.md` e as skills sozinho.

## 1. Programas (PowerShell)
```powershell
winget install Python.Python.3.12
winget install Gyan.FFmpeg
winget install astral-sh.uv
```
Feche e abra o terminal e confira: `python --version`, `ffmpeg -version`, `uvx --version`.

## 2. Instalar skills, MCPs e bibliotecas (na pasta do kit)
```powershell
cd "C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos"
powershell -ExecutionPolicy Bypass -File .\instalar.ps1
```
(copia `_instalar\skills` para `.claude\skills`, cria `.mcp.json` e `.env`, e roda o `pip install`.)
(O `faster-whisper` baixa o modelo de transcrição na primeira legenda — ~250 MB no modelo `small`.)

## 3. Chave do ElevenLabs
Crie em elevenlabs.io → Settings → API Keys. Depois:
```powershell
setx ELEVENLABS_API_KEY "sua_chave"
```
(ou cole a chave no arquivo `.env` que o instalar.ps1 criou — o `.env` não deve ser compartilhado).

## 4. Conectar os MCPs no Claude Code
O arquivo `.mcp.json` desta pasta já declara os 3; na primeira vez o Claude Code pergunta se pode usá-los — aceite.
Se preferir deixar disponível em qualquer pasta (escopo do usuário):
```powershell
claude mcp add --transport http -s user flora https://agents.flora.ai/mcp
claude mcp add --transport http -s user heygen https://mcp.heygen.com/mcp/v1/
claude mcp add -s user elevenlabs -e ELEVENLABS_API_KEY=sua_chave -- uvx elevenlabs-mcp
```
Depois, dentro do Claude Code, digite `/mcp` → selecione **flora** e **heygen** → *Authenticate* (abre o navegador para login).
Confira com `claude mcp list` (os 3 devem aparecer como conectados).

## 5. Teste rápido
```powershell
python ferramentas\overlays.py seta -o teste_seta.png
python ferramentas\finalizar.py "algum_video.mp4" --so-revisar
```

## O que tem aqui
- `CLAUDE.md` — regras do Savin (lido automaticamente pelo Claude Code).
- `.claude/skills/` — `editar-criativo`, `gerar-midia-ia`, `revisar-criativo`.
- `ferramentas/` — scripts: legenda, remover_legenda, video (vertical, dividida, montagem, hook, takes, concat),
  audio (mix, trocar, pausas, normalizar), overlays (manchete, faixa SB, selo COD, seta), tts_elevenlabs, finalizar, montar_ad.
- `fonts/` — Anton e Poppins Bold (usadas nas legendas e textos).
- `exemplos/` — receitas JSON de um AD drop e um San Benito.

Emojis coloridos na manchete usam a fonte do Windows (Segoe UI Emoji) automaticamente.
