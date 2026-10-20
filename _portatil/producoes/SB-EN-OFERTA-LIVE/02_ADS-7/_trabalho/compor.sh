# Compõe o SB-EN-ADS-7: corpo HeyGen (3 trechos) -> 1080x1920, legenda ASS, setas no CTA, voz EN + trilha FR (demucs)
T=22.40
ffmpeg -v error -y -i heygen/a_en_heygen.mp4 -i heygen/b_en_heygen.mp4 -i heygen/c_en_heygen.mp4 \
 -i audio/narr_en_pad.wav -i demucs/htdemucs/fr/no_vocals.wav -loop 1 -i seta_amarela.png \
 -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0,setpts=PTS-STARTPTS,fps=30,tpad=stop_mode=clone:stop_duration=1,trim=duration=$T,scale=1080:1920:flags=lanczos,ass=leg_en.ass:fontsdir=fonts[l];
 [5:v]scale=170:-1,split[s1][s2];
 [l][s1]overlay=x=235:y='1590-26*sin(2*PI*t/0.56)':enable='between(t,12.93,15.25)+gte(t,18.38)'[o1];
 [o1][s2]overlay=x=675:y='1590-26*sin(2*PI*t/0.56)':enable='between(t,12.93,15.25)+gte(t,18.38)',format=yuv420p[v];
 [3:a]volume=9.3dB,alimiter=limit=0.89[va];[4:a]atrim=0:$T,asetpts=PTS-STARTPTS,volume=-1.5dB,afade=t=out:st=21.4:d=1[ba];
 [va][ba]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.85:level=false,aresample=48000[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 16 -preset medium -r 30 -c:a aac -b:a 192k -ar 48000 -t $T \
 -bsf:v h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1 \
 -movflags +faststart ../SB-EN-ADS-7.mp4
