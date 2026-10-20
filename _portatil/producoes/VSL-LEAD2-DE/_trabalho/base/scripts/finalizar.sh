set -e
cd "/c/Users/PICHAU/Downloads/VSL-LEAD2-DE/_trabalho/base"
ls blocos/b0*.mp4 | sort | sed "s/^/file '/; s/$/'/" > blocos/lista.txt
ffmpeg -v error -y -f concat -safe 0 -i blocos/lista.txt -c copy -an base_limpa.mp4
ffprobe -v error -count_packets -select_streams v -show_entries stream=nb_read_packets,width,height,r_frame_rate -of csv=p=0 base_limpa.mp4
