T=$(python -c "import json;print(json.load(open('tempos.json'))['TOTAL'])")
TC=$(PYTHONIOENCODING=utf-8 python -c "
import json;b=json.load(open('blocos_fr.json',encoding='utf-8'));print(next(x[0] for x in b if x[2].startswith('APPUIE')))")
BASE=C:/Users/PICHAU/Downloads/SB-EN-OFERTA-LIVE/07_ADS-20/_trabalho/base_limpa.mp4
IN0="scale=720:1280:in_color_matrix=bt601:in_range=tv:out_color_matrix=bt601:out_range=tv,setsar=1,format=yuv420p"
# gancho: quadros 0-126 do HeyGen + 1 clone (o quadro 127 do HeyGen ja e ceu sem titulo); 128 quadros
# ceu: base a partir do quadro 128 + ultimos 100 quadros em reverso (base tem 141,17 s; o FR precisa de 144,1 s)
ffmpeg -v error -y -i heygen/hook_fr_heygen.mp4 -i $BASE -loop 1 -framerate 30 -i titulo_fr.png -loop 1 -framerate 30 -i seta_amarela.png -i audio/mix_fr.wav -filter_complex "\
[0:v]$IN0,setpts=N/30/TB,trim=end_frame=127,tpad=stop_mode=clone:stop=1,setpts=PTS-STARTPTS[h];\
[1:v]$IN0,setpts=N/30/TB,split[b1][b2];\
[b1]trim=start_frame=128,setpts=PTS-STARTPTS[x1];\
[b2]trim=start_frame=4135,setpts=PTS-STARTPTS,reverse,trim=start_frame=1,setpts=PTS-STARTPTS[x2];\
[x1][x2]concat=n=2:v=1:a=0,setpts=N/30/TB[s0];\
[2:v]format=rgba,gblur=sigma=0.6[tt];[s0][tt]overlay=0:0:shortest=1[s];\
[h][s]concat=n=2:v=1:a=0,setpts=N/30/TB[c];\
[c]ass=leg_fr.ass:fontsdir=fonts[l];\
[3:v]scale=136:-1[ar];[l][ar]overlay=x=292:y='1090-18*sin(2*PI*(t-$TC)/0.6)':enable='gte(t,$TC)':shortest=0[o];\
[o]scale=out_color_matrix=bt601:out_range=tv,format=yuv420p[v]" \
 -map "[v]" -map 4:a -t $T -r 30 -c:v libx264 -crf 18 -preset medium -profile:v high -c:a aac -b:a 192k -ar 48000 \
 -color_range tv -colorspace smpte170m -color_primaries smpte170m -color_trc smpte170m -movflags +faststart ../SB-FR-ADS-20.mp4
echo feito $T $TC
