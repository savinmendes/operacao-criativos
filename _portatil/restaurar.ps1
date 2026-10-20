# Coloca no ~/.claude deste PC o que veio do outro PC (rodar UMA vez, depois do clone).
# Uso:  powershell -ExecutionPolicy Bypass -File _portatil\restaurar.ps1
$ErrorActionPreference = "Stop"
$Proj  = (Resolve-Path "$PSScriptRoot\..").Path
$Home2 = Join-Path $env:USERPROFILE ".claude"
$Src   = Join-Path $PSScriptRoot "claude-home"
New-Item -ItemType Directory -Force $Home2 | Out-Null

# 1. CLAUDE.md global, hooks e mods (não apaga nada que já exista: só acrescenta/atualiza)
Copy-Item "$Src\CLAUDE.md" "$Home2\CLAUDE.md" -Force
foreach ($d in "hooks","mods") { if (Test-Path "$Src\$d") { Copy-Item "$Src\$d" $Home2 -Recurse -Force } }

# 2. Memória do projeto: a pasta usa o caminho do projeto neste PC no nome
$slug = ($Proj -replace '[:\\/ ]', '-')
$Mem  = Join-Path $Home2 "projects\$slug\memory"
New-Item -ItemType Directory -Force $Mem | Out-Null
Copy-Item "$Src\memory\*" $Mem -Recurse -Force

# 2b. Skills do claude.ai como skills do usuário (funcionam em qualquer conta e em qualquer pasta)
if (Test-Path "$Src\skills-claude-ai") {
  New-Item -ItemType Directory -Force "$Home2\skills" | Out-Null
  Get-ChildItem "$Src\skills-claude-ai" -Directory | ForEach-Object { Copy-Item $_.FullName "$Home2\skills\" -Recurse -Force }
}
# 2c. Permissões já liberadas no projeto (menos pedidos de confirmação)
if ((Test-Path "$Src\settings.local.projeto.json") -and -not (Test-Path "$Proj\.claude\settings.local.json")) {
  Copy-Item "$Src\settings.local.projeto.json" "$Proj\.claude\settings.local.json"
}
# 2d. Plugins (skills de documentos da Anthropic etc.)
if (Get-Command claude -ErrorAction SilentlyContinue) {
  claude plugin marketplace add anthropics/skills 2>$null
  Get-Content "$Src\plugins.txt" | ForEach-Object {
    $p = ($_ -split "`t")[0]
    if ($p -and $p -notlike "central@*") { claude plugin install $p 2>$null }
  }
}

# 3. settings.json: só cria se não existir (o seu fica intacto); o mod de progresso entra pela variável abaixo
if (-not (Test-Path "$Home2\settings.json")) { Copy-Item "$Src\settings.exemplo.json" "$Home2\settings.json" }
[Environment]::SetEnvironmentVariable("CLAUDE_CODE_PLUGIN_DIRS", (Join-Path $Home2 "mods\progresso"), "User")

Write-Host "Pronto. Memoria em: $Mem"
Write-Host "Feche e abra o VS Code. Falta criar os .env com as chaves (ver _portatil\INSTALAR-NO-OUTRO-PC.md)."
