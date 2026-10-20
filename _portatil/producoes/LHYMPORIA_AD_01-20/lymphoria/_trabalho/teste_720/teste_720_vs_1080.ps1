# Teste 720p (2x) vs 1080p (3x): mede tempo de upscale+gravação em 30 s do AD 03 e monta comparação
$up  = "C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas\upscale_video.py"
$src = "C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\AD 03.mp4"
$w   = "C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho\teste_720"
ffmpeg -v error -y -ss 0 -t 30 -i $src -c copy "$w\ad03_30s.mp4"
$t0 = Get-Date; python $up "$w\ad03_30s.mp4" "$w\ad03_720.mp4" --escala 2 --modelo realesr-animevideov3; $s720 = [int]((Get-Date) - $t0).TotalSeconds
$t0 = Get-Date; python $up "$w\ad03_30s.mp4" "$w\ad03_1080.mp4" --escala 3 --modelo realesr-animevideov3; $s1080 = [int]((Get-Date) - $t0).TotalSeconds
"RESULTADO: 720p levou $s720 s | 1080p levou $s1080 s (para 30 s de video)"
# lado a lado (720 ampliado para a mesma altura de exibição, como no celular)
ffmpeg -v error -y -i "$w\ad03_720.mp4" -i "$w\ad03_1080.mp4" -filter_complex "[0:v]scale=1080:1920:flags=bicubic,drawbox=x=0:y=0:w=1080:h=90:color=black@0.6:t=fill[a];[1:v]drawbox=x=0:y=0:w=1080:h=90:color=black@0.6:t=fill[b];[a][b]hstack" -c:v libx264 -crf 18 -an "$w\comparacao_720_x_1080.mp4"
Start-Process "$w\comparacao_720_x_1080.mp4"
