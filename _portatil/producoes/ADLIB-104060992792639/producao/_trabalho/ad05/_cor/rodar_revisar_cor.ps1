param([string]$quando = "depois")
# AD 05, correcao de cor: revisar_ad.py --lipsync (11 trechos do cortar_final_cor.py; caminhos relativos -> roda na pasta dos trechos)
$env:PYTHONIOENCODING = "utf-8"
$K = "C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas\revisar_ad.py"
$P = "C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao"
$R = "$P\_trabalho\ad05\_cor_rev"
$proib = "$P\_trabalho\_lote\proibidos.txt"
Set-Location "$R\$quando"
$spec = (Get-Content "lipsync_arg.txt" -Raw -Encoding UTF8).Trim()
if ($quando -eq "depois") {
  $f = "$P\AD 05 - ORACION-FAMILIA-ES-LATAM.mp4"
  python $K "$f" --idioma es --idioma-residual pt --proibidos $proib --lipsync $spec *> "$R\revisar_depois.log"
} else {
  $f = "$P\_trabalho\ad05\_antes_cor\AD 05 - ORACION-FAMILIA-ES-LATAM.mp4"
  python $K "$f" --sem-whisper --saida "$R\antes" --lipsync $spec *> "$R\revisar_antes.log"
}
