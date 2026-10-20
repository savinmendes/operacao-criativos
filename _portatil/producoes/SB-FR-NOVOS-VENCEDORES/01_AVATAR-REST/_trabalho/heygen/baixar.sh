for i in $(seq 1 100); do
  falta=0
  while read id n; do
    [ -s ${n}_out.mp4 ] && continue
    code=$(curl -s -L -o $n.tmp -w "%{http_code}" "https://resource2.heygen.ai/video_translate/$id/original.mp4")
    if [ "$code" = 200 ] && ffprobe -v error $n.tmp >/dev/null 2>&1; then mv $n.tmp ${n}_out.mp4; echo "$n pronto"; else rm -f $n.tmp; falta=1; fi
  done < lista.txt
  [ $falta = 0 ] && break
  sleep 30
done
echo FIM
