# uso: bash finalizar.sh P01 "<url>"
id=$1; curl -s -o takes/${id}_raw.mp4 "$2"
ffmpeg -v error -y -i takes/${id}_raw.mp4 -i audio/${id}.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 take_${id}.mp4
ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate,duration -of csv=p=0 take_${id}.mp4
PYTHONIOENCODING=utf-8 python qa_take.py ${id}
