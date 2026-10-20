# uso: sh encode3.sh NOME arquivo_saida.mp4   (2 passadas <=30 MB, cor bt601/tv fixa)
cd "$(dirname "$0")/_trab"
N=$1; OUT="../../ENTREGA/$2"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 v3_${N}_video.mp4)
BR=$(python -c "print(min(2600, int((29.0*8*1024)/float('$DUR') - 140)))")
TAG="-color_range tv -colorspace smpte170m -color_primaries smpte170m -color_trc smpte170m"
ffmpeg -v error -y -i v3_${N}_video.mp4 -c:v libx264 -preset slow -profile:v high -b:v ${BR}k -pass 1 -passlogfile p3_$N $TAG -an -f null NUL
ffmpeg -v error -y -i v3_${N}_video.mp4 -i v3_${N}_audio.wav -map 0:v -map 1:a -c:v libx264 -preset slow -profile:v high -b:v ${BR}k -pass 2 -passlogfile p3_$N $TAG -pix_fmt yuv420p -r 30 -c:a aac -b:a 128k -ar 48000 -ac 2 -shortest -movflags +faststart "$OUT"
echo "$2 br=${BR}k"; ffprobe -v error -show_entries format=duration,size -of compact "$OUT"
