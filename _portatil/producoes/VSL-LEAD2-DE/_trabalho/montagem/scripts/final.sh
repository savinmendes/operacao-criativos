#!/bin/bash
# concat dos blocos (sem recodificar) + mix final AAC; etiqueta bt709/tv so via h264_metadata
set -e
cd "/c/Users/PICHAU/Downloads/VSL-LEAD2-DE/_trabalho/montagem"
rm -f blocos/lista.txt
for f in blocos/bl0*.mp4; do echo "file '$(basename $f)'" >> blocos/lista.txt; done
cat blocos/lista.txt
NF=$(python -c "import json;print(json.load(open('params.json'))['NF'])")
DUR=$(python -c "print($NF/30)")
ffmpeg -v error -y -f concat -safe 0 -i blocos/lista.txt -i audio/mix_final.wav -map 0:v -map 1:a -c:v copy \
  -bsf:v "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1" \
  -c:a aac -b:a 192k -ar 48000 -t $DUR -movflags +faststart "${1:-/c/Users/PICHAU/Downloads/VSL-LEAD2-DE/VSL-LEAD2-DE.mp4}"
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames,duration,color_space,color_range:format=duration,size "${1:-/c/Users/PICHAU/Downloads/VSL-LEAD2-DE/VSL-LEAD2-DE.mp4}"
