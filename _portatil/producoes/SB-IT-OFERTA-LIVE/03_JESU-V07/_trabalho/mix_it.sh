set -e
cd "$(dirname "$0")"
# voz -16 LUFS (ganho fixo), trilha -32 LUFS sob a fala, limitador -1 dBTP
VI=$(ffmpeg -hide_banner -i audio/voz_it_cut.wav -af ebur128 -f null - 2>&1 | grep "I:" | tail -1 | awk '{print $2}')
BI=$(ffmpeg -hide_banner -i audio/bed_it.wav -af ebur128 -f null - 2>&1 | grep "I:" | tail -1 | awk '{print $2}')
GV=$(python -c "print(-16-($VI))"); GB=$(python -c "print(-32-($BI))")
ffmpeg -v error -y -i audio/voz_it_cut.wav -i audio/bed_it.wav -filter_complex \
"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=${GV}dB[v];[1:a]volume=${GB}dB[b];[v][b]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.89:level=false[o]" \
-map "[o]" -c:a pcm_s16le -ar 48000 audio/mix_it.wav
ffmpeg -hide_banner -i audio/mix_it.wav -af ebur128 -f null - 2>&1 | grep "I:" | tail -1
