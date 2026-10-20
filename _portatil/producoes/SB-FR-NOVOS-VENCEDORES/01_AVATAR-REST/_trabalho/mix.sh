# voz FR (loudnorm -15) + trilha sem voz do original (demucs) ~-32 LUFS reposicionada nas cenas? -> trilha contínua do original
cd "$(dirname "$0")"
ffmpeg -v error -y -i audio/voz_fr.wav -af "loudnorm=I=-12:TP=-1.5:LRA=11" -ar 48000 -ac 2 audio/voz_n.wav
ffmpeg -v error -y -i demucs/htdemucs/es/no_vocals.wav -af "atrim=0:62.3,loudnorm=I=-28:TP=-9:LRA=11,afade=t=in:d=0.05,afade=t=out:st=61.5:d=0.8" -ar 48000 -ac 2 audio/trilha.wav
ffmpeg -v error -y -i audio/voz_n.wav -i audio/trilha.wav -filter_complex "[0:a][1:a]amix=inputs=2:normalize=0:duration=longest,atrim=0:62.3" -ar 48000 audio/mix_fr.wav
ffmpeg -hide_banner -i audio/trilha.wav -af ebur128 -f null - 2>&1 | grep "  I:" | tail -1
ffmpeg -hide_banner -i audio/mix_fr.wav -af ebur128 -f null - 2>&1 | grep "  I:" | tail -1
