# baixa as saidas prontas (que ainda nao existem localmente) e compara a boca
while read n id; do
  [ -s ls_$n.mp4 ] && continue
  code=$(curl -s -L -o ls_$n.tmp -w "%{http_code}" "https://resource2.heygen.ai/video_translate/$id/original.mp4")
  if [ "$code" = 200 ] && ffprobe -v error ls_$n.tmp >/dev/null 2>&1; then mv ls_$n.tmp ls_$n.mp4; python cmp_boca.py $n; else rm -f ls_$n.tmp; echo "$n pendente ($code)"; fi
done < ids.txt
