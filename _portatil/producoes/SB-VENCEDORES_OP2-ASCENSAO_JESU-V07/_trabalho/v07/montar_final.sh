set -e
cd "$(dirname "$0")"
mkdir -p fonts; cp "/c/Users/PICHAU/Downloads/Produtividade com ia/kit-edicao-criativos/fonts/"*.ttf fonts/; cp fonts_extra/*.ttf fonts/
T0=$(python -c "import json;print(json.load(open('timeline.json'))['arrow'])")
TOT=$(python -c "import json;print(json.load(open('timeline.json'))['total'])")
ffmpeg -v error -y -i audio/voz_fr_full.wav -af "aresample=48000,loudnorm=I=-15:TP=-2:LRA=11" -ar 48000 -ac 2 audio/v_n.wav
ffmpeg -v error -y -i audio/bed_fr.wav -af "volume=-6.7dB" -ar 48000 -ac 2 audio/b_n.wav
ffmpeg -v error -y -i audio/v_n.wav -i audio/b_n.wav -filter_complex "[0][1]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,atrim=0:$TOT" -ar 48000 -ac 2 audio/mix_fr.wav
ffmpeg -v error -y -i base_fr.mp4 -loop 1 -i seta_amarela.png -i audio/mix_fr.wav -filter_complex \
"[0:v]ass=leg_fr.ass:fontsdir=fonts[l];[l][1:v]overlay=x=445:y='1548+27*(1-cos(2*PI*(t-$T0)/0.55))':enable='gte(t,$T0)':shortest=1[v]" \
-map "[v]" -map 2:a -c:v libx264 -crf 14 -preset medium -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -shortest bruto_fr.mp4
echo ok
