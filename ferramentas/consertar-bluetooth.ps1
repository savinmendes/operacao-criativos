# Conserta a pilha Bluetooth: limpa registros fantasma e reinicia o radio.
#
# Precisa de administrador. O .bat ao lado eleva sozinho.
#
# O que faz, em ordem:
#   1. Mostra o estado antes.
#   2. Remove os dispositivos Bluetooth FANTASMA (Present = False). Sao restos de
#      pareamentos antigos; o Windows nao os limpa sozinho e o acumulo deixa a
#      conexao instavel. Nenhum dispositivo conectado e tocado.
#   3. Reinicia o radio Bluetooth que estiver em erro (disable + enable). E
#      reversivel: se nao resolver, o radio volta ao estado anterior.
#   4. Mostra o estado depois.
#
# O que NAO faz: nada que exija desconectar hardware. Se houver dois dongles
# Bluetooth ligados, o conflito volta assim que o Windows reenumerar — esse e o
# unico passo que depende de voce.

$ErrorActionPreference = 'Continue'

function Titulo($t) {
    Write-Host ""
    Write-Host ("=== " + $t + " ===") -ForegroundColor Cyan
}

Titulo "ANTES"
$radios = Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue |
          Where-Object { $_.FriendlyName -match 'radio|adapter|adaptador' -and $_.Present }
Write-Host ("radios Bluetooth conectados: " + @($radios).Count)
$radios | Select-Object Status, FriendlyName, InstanceId | Format-Table -AutoSize

$todos = Get-PnpDevice -ErrorAction SilentlyContinue |
         Where-Object { $_.Class -in @('Bluetooth','MEDIA','AudioEndpoint','System') -and
                        $_.InstanceId -match 'BTHENUM|BTHHFENUM|MMDEVAPI' }
$fantasmas = @($todos | Where-Object { -not $_.Present })
Write-Host ("registros fantasma a limpar: " + $fantasmas.Count)

if (@($radios).Count -gt 1) {
    Write-Host ""
    Write-Host "ATENCAO: ha mais de um radio Bluetooth conectado." -ForegroundColor Yellow
    Write-Host "O Windows usa um de cada vez. Enquanto os dois estiverem plugados," -ForegroundColor Yellow
    Write-Host "um vai continuar em erro, por mais que este script o reinicie." -ForegroundColor Yellow
    Write-Host "Desconecte um dos dongles antes de confiar no resultado." -ForegroundColor Yellow
}

# ---------------------------------------------------------------- 2. fantasmas
Titulo "LIMPANDO FANTASMAS"
$ok = 0; $falhou = 0
foreach ($d in $fantasmas) {
    try {
        & pnputil /remove-device $d.InstanceId 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) { $ok++ } else { $falhou++ }
    } catch { $falhou++ }
}
Write-Host ("removidos: " + $ok + " | nao removidos: " + $falhou)

# ---------------------------------------------------------------- 3. radio
Titulo "REINICIANDO RADIO EM ERRO"
$ruins = Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue |
         Where-Object { $_.Present -and $_.Status -ne 'OK' }
if (-not $ruins) {
    Write-Host "nenhum radio em erro."
} else {
    foreach ($r in $ruins) {
        Write-Host ("reiniciando: " + $r.FriendlyName + "  [" + $r.InstanceId + "]")
        try {
            Disable-PnpDevice -InstanceId $r.InstanceId -Confirm:$false -ErrorAction Stop
            Start-Sleep -Seconds 3
            Enable-PnpDevice -InstanceId $r.InstanceId -Confirm:$false -ErrorAction Stop
            Start-Sleep -Seconds 3
            $novo = Get-PnpDevice -InstanceId $r.InstanceId -ErrorAction SilentlyContinue
            Write-Host ("   status agora: " + $novo.Status)
        } catch {
            Write-Host ("   falhou: " + $_.Exception.Message) -ForegroundColor Red
        }
    }
}

# reinicia os servicos para a pilha subir limpa
Titulo "SERVICOS BLUETOOTH"
foreach ($s in 'bthserv','BTAGService') {
    try {
        Restart-Service $s -Force -ErrorAction Stop
        Write-Host ("  " + $s + ": reiniciado")
    } catch {
        Write-Host ("  " + $s + ": " + $_.Exception.Message)
    }
}
Start-Sleep -Seconds 3

# ---------------------------------------------------------------- 4. depois
Titulo "DEPOIS"
Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue |
  Where-Object { $_.FriendlyName -match 'radio|adapter|adaptador' -and $_.Present } |
  Select-Object Status, FriendlyName | Format-Table -AutoSize

Write-Host "saidas de audio ativas:"
Get-PnpDevice -Class AudioEndpoint -ErrorAction SilentlyContinue |
  Where-Object { $_.Present } |
  Select-Object Status, FriendlyName | Format-Table -AutoSize

Write-Host ""
Write-Host "Se o seu dispositivo ainda nao aparecer:" -ForegroundColor Yellow
Write-Host "  1. Desconecte UM dos dongles Bluetooth."
Write-Host "  2. Rode este script de novo."
Write-Host "  3. Pareie o dispositivo em Configuracoes > Bluetooth."
Write-Host ""
Read-Host "Enter para fechar"
