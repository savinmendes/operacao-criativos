# jump cuts nas pausas do comerciante (boca entreaberta nas pausas): quadros 386-401 e 465-478 saem (vídeo e voz); trilha contínua por baixo
cd "$(dirname "$0")"
A1=$(python -c "print(386/30)"); B1=$(python -c "print(402/30)"); A2=$(python -c "print(465/30)"); B2=$(python -c "print(479/30)")
TOT=$(python -c "print(round(62.3-(16+14)/30,3))")
ffmpeg -v error -y -i audio/voz_n.wav -af "aselect='not(between(t,$A1,$B1-0.00001)+between(t,$A2,$B2-0.00001))',asetpts=N/SR/TB" audio/voz_cut.wav
ffmpeg -v error -y -i demucs/htdemucs/es/no_vocals.wav -af "atrim=0:$TOT,loudnorm=I=-28:TP=-9:LRA=11,afade=t=in:d=0.05,afade=t=out:st=$(python -c "print($TOT-0.8)"):d=0.8" -ar 48000 -ac 2 audio/trilha_cut.wav
ffmpeg -v error -y -i audio/voz_cut.wav -i audio/trilha_cut.wav -filter_complex "[0:a][1:a]amix=inputs=2:normalize=0:duration=longest,atrim=0:$TOT" -ar 48000 audio/mix_final.wav
ffmpeg -v error -y -i bruto_fr.mp4 -i audio/mix_final.wav -filter_complex "[0:v]select='not(between(n,386,401)+between(n,465,478))',setpts=N/30/TB[v]" -map "[v]" -map 1:a \
  -c:v libx264 -crf 18 -preset medium -maxrate 10M -bufsize 20M -pix_fmt yuv420p -bsf:v h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1 \
  -c:a aac -b:a 192k -ar 48000 -t $TOT -movflags +faststart ../SB-FR-AVATAR-REST.mp4
ffprobe -v error -show_entries stream=codec_type,width,height,duration,nb_frames -of compact ../SB-FR-AVATAR-REST.mp4
ffmpeg -hide_banner -i ../SB-FR-AVATAR-REST.mp4 -af ebur128 -f null - 2>&1 | grep "  I:" | tail -1
