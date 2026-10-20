# Sobe o servidor do painel (porta 8765) se ainda não estiver rodando.
$ok = (Test-NetConnection -ComputerName 127.0.0.1 -Port 8765 -InformationLevel Quiet -WarningAction SilentlyContinue)
if (-not $ok) {
  Start-Process -WindowStyle Hidden -FilePath (Get-Command python).Source `
    -ArgumentList "-m","http.server","8765","--bind","127.0.0.1" -WorkingDirectory "$PSScriptRoot"
}
