T=$(python -c "import json;print(json.load(open('tempos.json'))['TOTAL'])")
TC=$(PYTHONIOENCODING=utf-8 python -c "
import json;b=json.load(open('blocos_en.json',encoding='utf-8'));print(next(x[0] for x in b if x[2].startswith('TAP')))")
IN="scale=720:1280:in_color_matrix=bt601:in_range=tv:out_color_matrix=bt601:out_range=tv,setsar=1,fps=30,format=yuv420p"
ffmpeg -v error -y -i heygen/hook_en_heygen.mp4 -i base_limpa.mp4 -loop 1 -i titulo_en.png -loop 1 -i seta_amarela.png -i audio/mix_en.wav -filter_complex "\
[0:v]$IN,trim=end_frame=128,setpts=PTS-STARTPTS[h];\
[1:v]$IN,trim=start_frame=128,setpts=PTS-STARTPTS[s0];\
[2:v]format=rgba,gblur=sigma=0.6[tt];[s0][tt]overlay=0:0:shortest=1[s];\
[h][s]concat=n=2:v=1:a=0[c];\
[c]ass=leg_en.ass:fontsdir=fonts[l];\
[3:v]scale=136:-1[ar];[l][ar]overlay=x=292:y='1090-18*sin(2*PI*(t-$TC)/0.6)':enable='gte(t,$TC)':shortest=0[o];\
[o]scale=out_color_matrix=bt601:out_range=tv,format=yuv420p[v]" \
 -map "[v]" -map 4:a -t $T -r 30 -c:v libx264 -crf 18 -preset medium -profile:v high -c:a aac -b:a 192k -ar 48000 \
 -color_range tv -colorspace smpte170m -color_primaries smpte170m -color_trc smpte170m -movflags +faststart ../SB-EN-ADS-20.mp4
echo feito $T $TC
