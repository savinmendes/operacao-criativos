# uso: bash compor.sh base.mp4 saida.mp4
B=${1:-base_final.mp4}; OUT=${2:-../SB-EN-ADS-24.mp4}
T=$(python -c "from mapa import TOTAL;print(TOTAL)")
read T2 TF < <(python -c "import json;h=json.load(open('hook_t.json'));print(h['t2'],min(h['fim'],4.70))")
TC=$(PYTHONIOENCODING=utf-8 python -c "
import json;b=json.load(open('blocos_en.json',encoding='utf-8'));print(next(x[0] for x in b if x[2].startswith('TAP')))")
TE=$(python -c "print($TC+4.3)")
IN="scale=720:1280:in_color_matrix=bt601:in_range=tv:out_color_matrix=bt601:out_range=tv,setsar=1,fps=30,format=yuv420p"
ffmpeg -v error -y -i $B -loop 1 -i hook1.png -loop 1 -i hook2.png -loop 1 -i seta_dir.png -loop 1 -i seta_esq.png -i audio/mix_en.wav -filter_complex "\
[0:v]$IN[b];\
[b][1:v]overlay=0:930:enable='between(t,0.05,$T2)':shortest=1[h1];\
[h1][2:v]overlay=0:916:enable='between(t,$T2,$TF)':shortest=1[h2];\
[h2]ass=leg_en.ass:fontsdir=fonts[l];\
[l][3:v]overlay=x='25+14*sin(2*PI*(t-$TC)/0.7)':y='1095+14*sin(2*PI*(t-$TC)/0.7)':enable='between(t,$TC,$TE)':shortest=0[a1];\
[a1][4:v]overlay=x='545-14*sin(2*PI*(t-$TC)/0.7)':y='1095+14*sin(2*PI*(t-$TC)/0.7)':enable='between(t,$TC,$TE)':shortest=0[o];\
[o]scale=out_color_matrix=bt601:out_range=tv,format=yuv420p[v]" \
 -map "[v]" -map 5:a -t $T -r 30 -c:v libx264 -crf 18 -preset medium -profile:v high -c:a aac -b:a 192k -ar 48000 \
 -color_range tv -colorspace smpte170m -color_primaries smpte170m -color_trc smpte170m -movflags +faststart $OUT
echo feito T=$T CTA=$TC-$TE hook2=$T2 fim=$TF
