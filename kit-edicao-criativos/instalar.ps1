# Rode uma vez dentro da pasta do kit:  powershell -ExecutionPolicy Bypass -File .\instalar.ps1
$kit = Split-Path -Parent $MyInvocation.MyCommand.Path
New-Item -ItemType Directory -Force "$kit\.claude\skills" | Out-Null
Copy-Item "$kit\_instalar\skills\*" "$kit\.claude\skills\" -Recurse -Force
Copy-Item "$kit\_instalar\mcp.json" "$kit\.mcp.json" -Force
if (-not (Test-Path "$kit\.env")) { Copy-Item "$kit\_instalar\env.exemplo" "$kit\.env" }
python -m pip install -r "$kit\requirements.txt"
Write-Host "Skills e MCPs instalados. Cole sua chave do ElevenLabs no arquivo .env e abra a pasta no VS Code."
