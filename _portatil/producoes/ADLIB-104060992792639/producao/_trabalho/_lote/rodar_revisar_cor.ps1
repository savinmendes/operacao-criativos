param([string]$n, [string]$quando = "depois")
# Correcao de cor (lote C): revisar_ad.py --lipsync no final novo ("depois") ou so o lipsync no anterior ("antes", --sem-whisper)
$env:PYTHONIOENCODING = "utf-8"
Set-Location "C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos"
$P = "C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao"
$R = "$P\_trabalho\ad$n\_cor_rev"
$proib = "$P\_trabalho\_lote\proibidos.txt"
$spec = Get-Content "$R\$quando\lipsync_arg.txt" -Raw -Encoding UTF8
if ($quando -eq "depois") {
  $f = (Get-ChildItem $P -Filter "AD $n - *-ES-LATAM.mp4").FullName
  python ferramentas\revisar_ad.py "$f" --idioma es --idioma-residual pt --proibidos $proib --lipsync $spec.Trim() *> "$R\revisar_depois.log"
} else {
  $f = (Get-ChildItem "$P\_trabalho\ad$n\_antes_cor" -Filter "AD $n - *-ES-LATAM.mp4").FullName
  python ferramentas\revisar_ad.py "$f" --sem-whisper --saida "$R\antes" --lipsync $spec.Trim() *> "$R\revisar_antes.log"
}
