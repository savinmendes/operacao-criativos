# encode final 2 passadas (<=30 MB), cor bt601/tv fixa (smpte170m), audio AAC 48k 128k
cd "$(dirname "$0")/_trab"
OUT="../../ENTREGA/SB-ES_RANKING01_RESTAURANTE-NOTICIA.mp4"
TAG="-color_range tv -colorspace smpte170m -color_primaries smpte170m -color_trc smpte170m"
ffmpeg -v error -y -i _video.mp4 -c:v libx264 -preset slow -profile:v high -b:v 2150k -pass 1 -passlogfile p2 $TAG -an -f null NUL
ffmpeg -v error -y -i _video.mp4 -i audio.wav -map 0:v -map 1:a -c:v libx264 -preset slow -profile:v high -b:v 2150k -pass 2 -passlogfile p2 $TAG -pix_fmt yuv420p -r 30 -c:a aac -b:a 128k -ar 48000 -ac 2 -shortest -movflags +faststart "$OUT"
ls -la "$OUT"; ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height,color_space -of compact "$OUT"
