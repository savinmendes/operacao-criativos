param([string[]]$ads)
$env:PYTHONIOENCODING = "utf-8"
$P = "C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao"
$K = "C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas\revisar_ad.py"
$PROIB = "$P\_trabalho\revisao\proibidos_loteB.txt"
foreach ($n in $ads) {
  $d = "$P\_trabalho\ad$n"
  Set-Location $d
  $f = (Get-ChildItem $P -Filter "AD $n - *-ES-LATAM.mp4").FullName
  $ls = Get-Content "$d\lipsync\chk\lipsync_arg.txt" -Raw
  python $K "$f" --idioma es --idioma-residual pt --proibidos $PROIB --lipsync $ls.Trim() *> "$d\_revisar_loteB.log"
}
