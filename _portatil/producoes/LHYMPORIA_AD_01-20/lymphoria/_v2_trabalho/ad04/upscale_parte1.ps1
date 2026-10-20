# Upscale IA (Real-ESRGAN realesr-animevideov3, 3x) do trecho 0..107.6 s do AD 04 original 360p -> 1080x1920
$w   = "C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho\ad04"
$re  = "C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\_ferramentas_extras\realesrgan"
$src = "C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\AD 04.mp4"
$in  = "$w\frames_in"; $out = "$w\frames_up"
New-Item -ItemType Directory -Force $in, $out | Out-Null
ffmpeg -v error -y -i $src -t 107.6 -fps_mode passthrough "$in\%05d.png"
& "$re\realesrgan-ncnn-vulkan.exe" -i $in -o $out -n realesr-animevideov3 -s 3 -f png 2>&1 | Out-Null
ffmpeg -v error -y -framerate 30 -i "$out\%05d.png" -ss 0 -t 107.6 -i $src -map 0:v -map 1:a `
  -c:v libx264 -crf 15 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -ac 2 `
  -af "afade=t=out:st=107.48:d=0.12" -shortest "$w\parte1_up.mp4"
"frames_in: $((Get-ChildItem $in).Count)  frames_up: $((Get-ChildItem $out).Count)"
ffprobe -v error -show_entries format=duration:stream=width,height -of csv=p=0 "$w\parte1_up.mp4"
