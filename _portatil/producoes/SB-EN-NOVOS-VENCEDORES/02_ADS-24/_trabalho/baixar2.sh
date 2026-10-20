for i in $(seq 1 120); do
  falta=0; n_ids=$(wc -l < $1)
  while read n id; do
    [ -s $2/$n.mp4 ] && continue
    code=$(curl -s -L -o $2/$n.tmp -w "%{http_code}" "https://resource2.heygen.ai/video_translate/$id/original.mp4")
    if [ "$code" = 200 ] && ffprobe -v error $2/$n.tmp >/dev/null 2>&1; then mv $2/$n.tmp $2/$n.mp4; echo "$n pronto $(date +%H:%M)"; else rm -f $2/$n.tmp; falta=1; fi
  done < $1
  [ $falta = 0 ] && [ $n_ids -ge $3 ] && break
  sleep 30
done
echo FIM
