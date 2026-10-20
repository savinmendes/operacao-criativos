# uso: sh baixar.sh ids.txt -> ../work/<id>/out.mp4 ; tenta ate todos prontos (max ~60 min)
cd "$(dirname "$0")/../work"
for i in $(seq 1 120); do
  falta=0
  while read n id; do
    [ -s $n/out.mp4 ] && continue
    code=$(curl -s -L -o $n/out.tmp -w "%{http_code}" "https://resource2.heygen.ai/video_translate/$id/original.mp4")
    if [ "$code" = 200 ] && ffprobe -v error $n/out.tmp >/dev/null 2>&1; then mv $n/out.tmp $n/out.mp4; echo "$n pronto"; else rm -f $n/out.tmp; falta=1; fi
  done < "$1"
  [ $falta = 0 ] && break
  sleep 30
done
echo FIM
