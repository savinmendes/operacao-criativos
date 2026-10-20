# Instalar a operação em outro PC (Windows)

O repositório traz o código, as skills, as regras, os relatórios, a memória do Claude, os mods e os scripts de produção de cada lote. Ficam de fora as **chaves** e a **mídia** (vídeos, áudios, imagens e modelos), porque o GitHub não guarda arquivos grandes e chave não pode ir para a internet.

## 1. Programas (uma vez)
- Git: `winget install Git.Git`
- GitHub CLI: `winget install GitHub.cli`, depois `gh auth login` com a sua conta.
- VS Code + a extensão **Claude Code**. Entre com a conta do Claude.
- Python 3.12: `winget install Python.Python.3.12`
- ffmpeg: `winget install Gyan.FFmpeg`
- (opcional) rclone, para puxar a mídia do Drive: `winget install Rclone.Rclone`

## 2. Baixar o projeto
Use **o mesmo caminho do PC original**. Os scripts de produção e a memória citam pastas de Downloads, e assim tudo bate:
```
cd %USERPROFILE%\Downloads
gh repo clone savinmendes/operacao-criativos "Produtividade com ia"
cd "Produtividade com ia"
powershell -ExecutionPolicy Bypass -File _portatil\restaurar.ps1
```
O `restaurar.ps1` copia para o seu `~/.claude` o CLAUDE.md global, os hooks (voz «Sávio, terminei»), o mod de progresso e a memória do projeto. Ele também liga o mod pela variável `CLAUDE_CODE_PLUGIN_DIRS`.

## 3. Dependências Python
```
pip install -r kit-edicao-criativos\requirements.txt
pip install faster-whisper demucs rapidocr_onnxruntime pyloudnorm librosa soundfile scipy opencv-python requests
```
Cada ferramenta em `ferramentas\` tem o próprio `requirements.txt` quando precisa. Os modelos (Whisper, demucs, LaMa) baixam sozinhos no primeiro uso. O Real-ESRGAN vem de https://github.com/xinntao/Real-ESRGAN/releases (versão ncnn-vulkan) e vai em `kit-edicao-criativos\_ferramentas_extras\realesrgan\`.

## 4. Chaves (criar à mão, nunca subir)
- `kit-edicao-criativos\.env` → `ELEVENLABS_API_KEY=...`
- `ferramentas\gerador-criativos-video\.env` → as chaves que esse gerador usar (fal.ai, ElevenLabs, HeyGen)

## 5. Conectores do Claude
Os conectores (Meta Ads, HeyGen, ElevenLabs, Flora, Google Drive, Shopify, Utmify etc.) ficam **na conta do claude.ai**. Na mesma conta do Claude, eles já aparecem. Numa conta diferente, conecte de novo em claude.ai → Configurações → Conectores. Os MCPs deste projeto (`.mcp.json`: dropkiller, chegou-operacoes, winninghunter) pedem login na primeira vez.

## 6. Mídia (vídeos de produção, bancos de b-roll, entregas)
Ficam no Google Drive (rclone `gdrive:`). Para ter os bancos no PC novo, por exemplo:
```
rclone copy "gdrive:ARQUIVO-PROJETOS/<pasta>" "%USERPROFILE%\Downloads\<pasta>" --progress
```

## 7. Manter os dois PCs iguais
- **Antes de trabalhar:** `git pull`.
- **Depois de trabalhar:** `python _portatil\coletar.py` (atualiza memória, mods e scripts dos lotes), depois `git add -A`, `git commit -m "..."` e `git push`.
- A memória do Claude só sincroniza por esse ciclo. Rode o `coletar.py` no PC onde você trabalhou e o `restaurar.ps1` no outro depois do `git pull`.
