# Sobe pastas antigas para o Google Drive (rclone direto, sem cache local) e confere por checksum.
# Uso: powershell -File subir_arquivo.ps1   (log em logs\)
$R   = "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe\rclone-v1.75.1-windows-amd64\rclone.exe"
$Base = (Resolve-Path "$PSScriptRoot\..\..\01-arquivos-organizados").Path
$Logs = "$PSScriptRoot\logs"
New-Item -ItemType Directory -Force $Logs | Out-Null

$lotes = @(
  @{ src = "$Base\materiais-legado-por-pasta"; dst = "gdrive:ARQUIVO-PROJETOS/legado-carticuri-x1" },
  @{ src = "$Base\trabalho";                    dst = "gdrive:ARQUIVO-PROJETOS/trabalho-brutos" }
)

foreach ($l in $lotes) {
  $nome = Split-Path $l.dst -Leaf
  "$(Get-Date -f s) INICIO $nome" | Add-Content "$Logs\status.txt"
  & $R copy $l.src $l.dst --transfers 4 --checkers 8 --drive-chunk-size 64M `
      --stats 30s --stats-one-line --log-level INFO --log-file "$Logs\copy_$nome.log"
  "$(Get-Date -f s) COPIA_FIM $nome (exit $LASTEXITCODE)" | Add-Content "$Logs\status.txt"
  & $R check $l.src $l.dst --one-way --log-file "$Logs\check_$nome.log" --log-level NOTICE
  "$(Get-Date -f s) CHECK_FIM $nome (exit $LASTEXITCODE; 0 = identico)" | Add-Content "$Logs\status.txt"
}
"$(Get-Date -f s) TUDO_FIM" | Add-Content "$Logs\status.txt"
