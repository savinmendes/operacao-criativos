param([string[]]$ads)
$env:PYTHONIOENCODING = "utf-8"
Set-Location "C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos"
$P = "C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao"
$S = "$P\_trabalho\revisao\loteB\revisar"
$proib = "real,reales,dinero,depósito,cantidad,riqueza,cura,curada,enfermedad,cáncer,horas,segundos,aire,borrada,rápido,rápida,pocos,minuto,salud,dolor,sanar,sanación,milagro,enfermo,hospital,hoy,noche"
foreach ($n in $ads) {
  $f = (Get-ChildItem $P -Filter "AD $n - *-ES-LATAM.mp4").FullName
  python ferramentas\revisar_ad.py "$f" --idioma es --idioma-residual pt --proibidos $proib --saida $S *> "$S\log_$n.txt"
}
