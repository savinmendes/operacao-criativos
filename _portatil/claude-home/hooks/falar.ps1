param([string]$tipo = "fim")
# Toca a voz gravada (ElevenLabs, voz "Luciana"); se faltar o arquivo, cai na voz do Windows.
$arq = Join-Path $PSScriptRoot ("vozes\" + $tipo + ".wav")
if (Test-Path $arq) { (New-Object Media.SoundPlayer $arq).PlaySync(); exit }
$textos = @{ fim = "Sávio, terminei"; aviso = "Sávio, preciso de você" }
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
try { $s.SelectVoice("Microsoft Maria Desktop") } catch {}
$s.Speak($textos[$tipo])
