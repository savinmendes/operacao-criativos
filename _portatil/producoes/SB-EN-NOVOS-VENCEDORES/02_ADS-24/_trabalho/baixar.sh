for i in $(seq 1 120); do
  falta=0; n_ids=$(wc -l < ids.txt)
  while read n id; do
    [ -s heygen_out/$n.mp4 ] && continue
    code=$(curl -s -L -o heygen_out/$n.tmp -w "%{http_code}" "https://resource2.heygen.ai/video_translate/$id/original.mp4")
    if [ "$code" = 200 ] && ffprobe -v error heygen_out/$n.tmp >/dev/null 2>&1; then mv heygen_out/$n.tmp heygen_out/$n.mp4; echo "$n pronto $(date +%H:%M)"; else rm -f heygen_out/$n.tmp; falta=1; fi
  done < ids.txt
  [ $falta = 0 ] && [ $n_ids -ge 14 ] && break
  sleep 30
done
echo FIM
