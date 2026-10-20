# Compõe o SB-PL-ADS-7: corpo HeyGen (a, b1, b2, c) -> 1080x1920, legenda ASS PL, setas nos 2 CTAs, voz PL (Brian) + trilha FR (demucs)
T=23.90
ffmpeg -v error -y -reinit_filter 0 -i heygen/a_pl_heygen.mp4 -reinit_filter 0 -i heygen/b1_pl_heygen.mp4 -reinit_filter 0 -i heygen/b2_pl_heygen.mp4 -reinit_filter 0 -i heygen/c_pl_heygen.mp4 \
 -i audio/narr_pl_pad.wav -i demucs/fr_no_vocals.wav -loop 1 -i seta_amarela.png \
 -filter_complex "[0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0,setpts=PTS-STARTPTS,fps=30,tpad=stop_mode=clone:stop_duration=1,trim=duration=$T,scale=1080:1920:flags=lanczos,ass=leg_pl.ass:fontsdir=fonts[l];
 [6:v]scale=170:-1,split[s1][s2];
 [l][s1]overlay=x=235:y='1590-26*sin(2*PI*t/0.56)':enable='between(t,13.17,15.70)+gte(t,19.83)'[o1];
 [o1][s2]overlay=x=675:y='1590-26*sin(2*PI*t/0.56)':enable='between(t,13.17,15.70)+gte(t,19.83)',format=yuv420p[v];
 [4:a]volume=9.3dB,alimiter=limit=0.89[va];[5:a]atrim=0:$T,asetpts=PTS-STARTPTS,volume=-1.5dB,afade=t=out:st=22.9:d=1[ba];
 [va][ba]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.85:level=false,aresample=48000[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 16 -preset medium -r 30 -c:a aac -b:a 192k -ar 48000 -t $T \
 -bsf:v h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1 \
 -movflags +faststart ../SB-PL-ADS-7.mp4
