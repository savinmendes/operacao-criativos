ffmpeg -v error -y -i audio/voz_pl.wav -af "loudnorm=I=-15:TP=-1.5:LRA=11" -ar 48000 audio/voz_n.wav
ffmpeg -v error -y -i demucs/htdemucs/es/no_vocals.wav -af "atrim=0:31.6,loudnorm=I=-32:TP=-9:LRA=11,afade=t=out:st=31.1:d=0.5" -ar 48000 -ac 2 audio/trilha.wav
ffmpeg -v error -y -i audio/voz_n.wav -i audio/trilha.wav -filter_complex "[0:a][1:a]amix=inputs=2:normalize=0:duration=longest,atrim=0:31.6" -ar 48000 audio/mix_pl.wav
ffmpeg -hide_banner -i audio/mix_pl.wav -af ebur128 -f null - 2>&1 | grep -A2 "Integrated" | head -3
ffmpeg -hide_banner -i audio/trilha.wav -af ebur128 -f null - 2>&1 | grep "  I:" 
