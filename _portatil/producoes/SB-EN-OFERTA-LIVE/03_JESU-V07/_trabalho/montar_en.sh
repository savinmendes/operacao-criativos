set -e
cd "$(dirname "$0")"
T0=$(python -c "import json;print(json.load(open('timeline.json'))['arrow']-0.2)")
TOT=$(python -c "import json;print(json.load(open('timeline.json'))['total'])")
ffmpeg -v error -y -i base_en.mp4 -loop 1 -i seta_amarela.png -i audio/mix_en.wav -filter_complex \
"[0:v]ass=leg_en.ass:fontsdir=fonts[l];[l][1:v]overlay=x=445:y='1548+27*(1-cos(2*PI*(t-$T0)/0.55))':enable='gte(t,$T0)':shortest=1,scale=out_color_matrix=bt601:out_range=tv,format=yuv420p[v]" \
-map "[v]" -map 2:a -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 -t $TOT bruto_en.mp4
echo ok
